"""
Build Make.com scenarios for the Client Onboarding Emailer.
Run once after creating your Google Sheet.

Google Sheet columns (A-J, row 1 = headers):
  A: Timestamp | B: Name | C: Business | D: Industry | E: Goal
  F: Source | G: Email | H: Email Sent | I: Booking Link Clicked | J: Follow-up Sent
"""
import json, os, requests, sys
from dotenv import load_dotenv
load_dotenv()

# ── Config ─────────────────────────────────────────────────────────────────────
MAKE_TOKEN    = os.environ["MAKE_API_TOKEN"]
BASE          = "https://us2.make.com/api/v2"
TEAM_ID       = 2225534
GOOGLE_CONN   = 8635321   # "Make Academy" Google OAuth

ANTHROPIC_KEY = os.environ["ANTHROPIC_API_KEY"]
YOUR_NAME     = "Shant"
CALENDLY_URL  = "https://calendly.com/yourname/20min"
YOUR_SERVICE  = "AI automation consulting"

# Update after creating the Google Sheet
SPREADSHEET_ID = "REPLACE_WITH_YOUR_SPREADSHEET_ID"
SHEET_NAME     = "Leads"

API_HEADERS = {"Authorization": f"Token {MAKE_TOKEN}", "Content-Type": "application/json"}

# ── Prompts ────────────────────────────────────────────────────────────────────
WELCOME_PROMPT = (
    f"You are writing on behalf of {YOUR_NAME}, an AI automation consultant.\\n\\n"
    "A new prospective client just filled out an intake form. "
    "Write a warm, professional welcome email under 150 words. "
    f"Include this Calendly booking link: {CALENDLY_URL}\\n\\n"
    "Client details:\\n"
    "- Name: {{1.name}}\\n- Business: {{1.business}}\\n"
    "- Industry: {{1.industry}}\\n- Primary goal: {{1.goal}}\\n\\n"
    f"Write as {YOUR_NAME}. Reference their actual goal. "
    "End with one CTA. No subject line."
)

# In Scenario 2, data comes from BasicFeeder (module 2): value[1]=Name, [2]=Business, [4]=Goal
FOLLOWUP_PROMPT = (
    f"Write a short follow-up email (under 80 words) to {{{{2.value[1]}}}} at {{{{2.value[2]}}}}. "
    f"They expressed interest in {YOUR_SERVICE} two days ago but have not booked. "
    "Their goal: {{{{2.value[4]}}}}. "
    f"Soft CTA, no pressure. Sign off as {YOUR_NAME}."
)

def claude_body(prompt, max_tokens=300):
    return json.dumps({
        "model": "claude-sonnet-4-6",
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}]
    })

# ── Scenario 1: Welcome Email ──────────────────────────────────────────────────
# Webhook → addRow (A-J) → Claude HTTP → google-email send → updateRow (H=TRUE)
S1 = {
    "name": "Client Onboarding - Welcome Email",
    "flow": [
        {   # 1. Tally/Typeform webhook
            "id": 1, "module": "gateway:CustomWebHook", "version": 1,
            "mapper": {}, "metadata": {"designer": {"x": -600, "y": 0}}, "parameters": {}
        },
        {   # 2. Log lead (all 10 columns)
            "id": 2, "module": "google-sheets:addRow", "version": 2,
            "mapper": {
                "from": "drive", "mode": "select",
                "values": {
                    "0": '{{formatDate(now; "YYYY-MM-DD HH:mm:ss")}}',
                    "1": "{{1.name}}", "2": "{{1.business}}", "3": "{{1.industry}}",
                    "4": "{{1.goal}}", "5": "{{1.source}}", "6": "{{1.email}}",
                    "7": "FALSE", "8": "FALSE", "9": "FALSE"
                },
                "sheetId": SHEET_NAME, "spreadsheetId": SPREADSHEET_ID,
                "includesHeaders": True, "insertDataOption": "INSERT_ROWS",
                "valueInputOption": "USER_ENTERED", "insertUnformatted": False
            },
            "metadata": {"designer": {"x": -300, "y": 0}},
            "parameters": {"__IMTCONN__": GOOGLE_CONN}
        },
        {   # 3. Call Claude API
            "id": 3, "module": "http:ActionSendData", "version": 3,
            "mapper": {
                "url": "https://api.anthropic.com/v1/messages", "method": "POST",
                "headers": [
                    {"name": "x-api-key",        "value": ANTHROPIC_KEY},
                    {"name": "anthropic-version", "value": "2023-06-01"},
                    {"name": "content-type",      "value": "application/json"}
                ],
                "bodyType": "raw", "parseResponse": True,
                "contentType": "application/json",
                "data": claude_body(WELCOME_PROMPT)
            },
            "metadata": {"designer": {"x": 0, "y": 0}}, "parameters": {}
        },
        {   # 4. Send welcome email
            "id": 4, "module": "google-email:ActionSendEmail", "version": 1,
            "mapper": {
                "to": "{{1.email}}",
                "subject": "{{1.name}}, re: {{1.goal}}",
                "content": "{{3.data.content[].text}}",
                "contentType": "text"
            },
            "metadata": {"designer": {"x": 300, "y": 0}},
            "parameters": {"__IMTCONN__": GOOGLE_CONN}
        },
        {   # 5. Mark H (Email Sent) = TRUE
            "id": 5, "module": "google-sheets:updateRow", "version": 2,
            "mapper": {
                "from": "drive", "mode": "select",
                "values": {"7": "TRUE"},
                "rowNumber": "{{2.rowNumber}}",
                "sheetId": SHEET_NAME, "spreadsheetId": SPREADSHEET_ID,
                "valueInputOption": "USER_ENTERED", "insertUnformatted": False
            },
            "metadata": {"designer": {"x": 600, "y": 0}},
            "parameters": {"__IMTCONN__": GOOGLE_CONN}
        }
    ],
    "metadata": {"instant": True, "version": 1, "designer": {"orphans": []}}
}

# ── Scenario 2: 48hr Follow-up ─────────────────────────────────────────────────
# Daily: GET all Sheets rows (A2:J1000) → BasicFeeder iterate → filter on module 3
# → Claude HTTP → google-email send → updateRow (J=TRUE)
#
# Filter (blueprint "filter" property on module 3):
#   H (value[7]) = TRUE  → email was sent
#   I (value[8]) = FALSE → booking not clicked
#   J (value[9]) = FALSE → follow-up not yet sent
#   age >= 48 hours
#
# Row number: range starts at A2, so sheet_row = __idx__ + 1 (__idx__ is 1-based)
S2 = {
    "name": "Client Onboarding - 48hr Follow-up",
    "flow": [
        {   # 1. GET all data rows via Google Sheets API (A2:J1000 skips header)
            "id": 1, "module": "http:ActionSendData", "version": 3,
            "mapper": {
                "url": f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{SHEET_NAME}!A2:J1000",
                "method": "GET", "parseResponse": True
            },
            "metadata": {"designer": {"x": -700, "y": 0}},
            "parameters": {"__IMTCONN__": GOOGLE_CONN}
        },
        {   # 2. Iterate over each row
            "id": 2, "module": "builtin:BasicFeeder", "version": 1,
            "mapper": {"array": "{{1.data.values}}"},
            "metadata": {"designer": {"x": -450, "y": 0}}, "parameters": {}
        },
        {   # 3. Call Claude — filter conditions attached here (Make.com pattern)
            "id": 3, "module": "http:ActionSendData", "version": 3,
            "filter": {
                "name": "48hr non-booker",
                "conditions": [[
                    {"a": "{{2.value[7]}}", "b": "TRUE",  "o": "text:equal"},
                    {"a": "{{2.value[8]}}", "b": "FALSE", "o": "text:equal"},
                    {"a": "{{2.value[9]}}", "b": "FALSE", "o": "text:equal"},
                    {
                        "a": '{{dateDifference(now; parseDate(2.value[0]; "YYYY-MM-DD HH:mm:ss"); "hours")}}',
                        "b": "48", "o": "number:greaterThanEquals"
                    }
                ]]
            },
            "mapper": {
                "url": "https://api.anthropic.com/v1/messages", "method": "POST",
                "headers": [
                    {"name": "x-api-key",        "value": ANTHROPIC_KEY},
                    {"name": "anthropic-version", "value": "2023-06-01"},
                    {"name": "content-type",      "value": "application/json"}
                ],
                "bodyType": "raw", "parseResponse": True,
                "contentType": "application/json",
                "data": claude_body(FOLLOWUP_PROMPT, max_tokens=200)
            },
            "metadata": {"designer": {"x": -150, "y": 0}}, "parameters": {}
        },
        {   # 4. Send follow-up email
            "id": 4, "module": "google-email:ActionSendEmail", "version": 1,
            "mapper": {
                "to": "{{2.value[6]}}",
                "subject": "Still thinking it over, {{2.value[1]}}?",
                "content": "{{3.data.content[].text}}",
                "contentType": "text"
            },
            "metadata": {"designer": {"x": 150, "y": 0}},
            "parameters": {"__IMTCONN__": GOOGLE_CONN}
        },
        {   # 5. Mark J (Follow-up Sent) = TRUE
            "id": 5, "module": "google-sheets:updateRow", "version": 2,
            "mapper": {
                "from": "drive", "mode": "select",
                "values": {"9": "TRUE"},
                "rowNumber": "{{add(2.__idx__; 1)}}",
                "sheetId": SHEET_NAME, "spreadsheetId": SPREADSHEET_ID,
                "valueInputOption": "USER_ENTERED", "insertUnformatted": False
            },
            "metadata": {"designer": {"x": 450, "y": 0}},
            "parameters": {"__IMTCONN__": GOOGLE_CONN}
        }
    ],
    "metadata": {"instant": False, "version": 1, "designer": {"orphans": []}}
}

# ── Helpers ────────────────────────────────────────────────────────────────────
def create_scenario(blueprint, scheduling):
    r = requests.post(f"{BASE}/scenarios", headers=API_HEADERS, json={
        "blueprint": json.dumps(blueprint),
        "scheduling": json.dumps(scheduling),
        "teamId": TEAM_ID,
    })
    return r.status_code, r.json()

def get_webhook_url(scenario_id):
    r = requests.get(f"{BASE}/hooks", headers=API_HEADERS,
                     params={"teamId": TEAM_ID, "scenarioId": scenario_id})
    hooks = r.json().get("hooks", [])
    return hooks[0].get("url") if hooks else None

# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Creating Scenario 1: Welcome Email...")
    c1, r1 = create_scenario(S1, {"type": "indefinitely", "interval": 900})
    if c1 != 200:
        print(f"  FAILED HTTP {c1}:", json.dumps(r1, indent=2)); sys.exit(1)
    s1_id = r1["scenario"]["id"]
    webhook = get_webhook_url(s1_id)
    print(f"  ID={s1_id}  Webhook={webhook or '(check Make.com Webhooks)'}")

    print("\nCreating Scenario 2: 48hr Follow-up...")
    c2, r2 = create_scenario(S2, {"type": "indefinitely", "interval": 86400})
    if c2 != 200:
        print(f"  FAILED HTTP {c2}:", json.dumps(r2, indent=2)); sys.exit(1)
    s2_id = r2["scenario"]["id"]
    print(f"  ID={s2_id}")

    print(f"""
{'='*60}
BOTH SCENARIOS CREATED
{'='*60}
Scenario 1 (Welcome Email) : {s1_id}
Webhook URL                : {webhook or 'check Make.com > Webhooks tab'}
Scenario 2 (48hr Follow-up): {s2_id}

NEXT STEPS:
1. Create a Google Sheet named 'Client Leads' with these headers in row 1:
   Timestamp | Name | Business | Industry | Goal | Source | Email |
   Email Sent | Booking Link Clicked | Follow-up Sent

2. Copy Sheet ID from the URL, set SPREADSHEET_ID in this file,
   then update the spreadsheet ID in Make.com for each Sheets module.

3. Update CALENDLY_URL to your real Calendly link, then update
   the prompt in Scenario 1 > module 3 (HTTP/Claude) in Make.com.

4. Paste the Webhook URL above into your Tally form
   (Integrations > Webhooks).

5. Activate both scenarios in Make.com (toggle switch).

6. Submit a test form entry — email should arrive in <30 seconds.
""")
