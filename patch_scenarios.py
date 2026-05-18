import json, os, requests, urllib.parse
from dotenv import load_dotenv
load_dotenv()

MAKE_TOKEN = os.environ["MAKE_API_TOKEN"]
BASE = "https://us2.make.com/api/v2"
HEADERS = {"Authorization": f"Token {MAKE_TOKEN}", "Content-Type": "application/json"}
SHEETS_CONN = 8635321
SPREADSHEET_ID = os.environ["GOOGLE_SPREADSHEET_ID"]
ANTHROPIC_KEY = os.environ["ANTHROPIC_API_KEY"]

REFRESH_BODY = urllib.parse.urlencode({
    "grant_type": "refresh_token",
    "client_id": os.environ["GOOGLE_CLIENT_ID"],
    "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
    "refresh_token": os.environ["GOOGLE_REFRESH_TOKEN"],
})

# Token refresh module (shared by both scenarios)
# contentType must be a Make.com-accepted value; actual Content-Type is set via header
TOKEN_REFRESH_MODULE = {
    "module": "http:ActionSendData", "version": 3,
    "mapper": {
        "url": "https://oauth2.googleapis.com/token",
        "method": "POST",
        "headers": [{"name": "Content-Type", "value": "application/x-www-form-urlencoded"}],
        "bodyType": "raw",
        "contentType": "application/json",
        "parseResponse": True,
        "data": REFRESH_BODY
    },
    "parameters": {}
}

# Gmail send module template — call with id, bearer_ref, to_ref, subject_ref, body_ref, x
def gmail_send_module(mid, to_ref, subject_ref, body_ref, token_module_id, x):
    bearer = "Bearer {{" + str(token_module_id) + ".data.access_token}}"
    return {
        "id": mid, "module": "http:ActionSendData", "version": 3,
        "mapper": {
            "url": "https://gmail.googleapis.com/upload/gmail/v1/users/me/messages/send?uploadType=media",
            "method": "POST",
            "headers": [
                {"name": "Authorization", "value": bearer},
                {"name": "Content-Type",  "value": "message/rfc822"}
            ],
            "bodyType": "raw",
            "contentType": "application/json",
            "parseResponse": True,
            "data": f"From: hantous93@gmail.com\nTo: {to_ref}\nSubject: {subject_ref}\nMIME-Version: 1.0\nContent-Type: text/plain; charset=UTF-8\n\n{body_ref}"
        },
        "parameters": {},
        "metadata": {"designer": {"x": x, "y": 0}}
    }

# ── Scenario 1: 6 modules (webhook→addRow→Claude→tokenRefresh→gmailSend→updateRow)
S1_BP = {
    "name": "Client Onboarding - Welcome Email",
    "flow": [
        {
            "id": 1, "module": "gateway:CustomWebHook", "version": 1,
            "mapper": {}, "parameters": {"hook": 2318330},
            "metadata": {"designer": {"x": -750, "y": 0}}
        },
        {
            "id": 2, "module": "google-sheets:addRow", "version": 2,
            "mapper": {
                "from": "drive", "mode": "select",
                "values": {
                    "0": '{{formatDate(now; "YYYY-MM-DD HH:mm:ss")}}',
                    "1": "{{1.name}}", "2": "{{1.business}}", "3": "{{1.industry}}",
                    "4": "{{1.goal}}", "5": "{{1.source}}", "6": "{{1.email}}",
                    "7": "FALSE", "8": "FALSE", "9": "FALSE"
                },
                "sheetId": "Leads", "spreadsheetId": SPREADSHEET_ID,
                "includesHeaders": True, "insertDataOption": "INSERT_ROWS",
                "valueInputOption": "USER_ENTERED", "insertUnformatted": False
            },
            "parameters": {"__IMTCONN__": SHEETS_CONN},
            "metadata": {"designer": {"x": -450, "y": 0}}
        },
        {
            "id": 3, "module": "http:ActionSendData", "version": 3,
            "mapper": {
                "url": "https://api.anthropic.com/v1/messages", "method": "POST",
                "headers": [
                    {"name": "x-api-key", "value": ANTHROPIC_KEY},
                    {"name": "anthropic-version", "value": "2023-06-01"},
                    {"name": "content-type", "value": "application/json"}
                ],
                "bodyType": "raw", "parseResponse": True, "contentType": "application/json",
                "data": json.dumps({
                    "model": "claude-sonnet-4-6", "max_tokens": 300,
                    "messages": [{"role": "user", "content": (
                        "You are writing on behalf of Shant, an AI automation consultant.\n\n"
                        "A new prospective client just filled out an intake form. "
                        "Write a warm, professional welcome email under 150 words. "
                        "Include this Calendly booking link: https://calendly.com/yourname/20min\n\n"
                        "Client details:\n"
                        "- Name: {{1.name}}\n- Business: {{1.business}}\n"
                        "- Industry: {{1.industry}}\n- Primary goal: {{1.goal}}\n\n"
                        "Write as Shant. Reference their actual goal. End with one CTA. No subject line."
                    )}]
                })
            },
            "parameters": {},
            "metadata": {"designer": {"x": -150, "y": 0}}
        },
        {
            **TOKEN_REFRESH_MODULE,
            "id": 4,
            "metadata": {"designer": {"x": 150, "y": 0}}
        },
        gmail_send_module(
            mid=5, token_module_id=4,
            to_ref="{{1.email}}",
            subject_ref="{{1.name}}, re: {{1.goal}}",
            body_ref="{{3.data.content[].text}}",
            x=450
        ),
        {
            "id": 6, "module": "google-sheets:updateRow", "version": 2,
            "mapper": {
                "from": "drive", "mode": "select",
                "values": {"7": "TRUE"},
                "rowNumber": "{{2.rowNumber}}",
                "sheetId": "Leads", "spreadsheetId": SPREADSHEET_ID,
                "valueInputOption": "USER_ENTERED", "insertUnformatted": False
            },
            "parameters": {"__IMTCONN__": SHEETS_CONN},
            "metadata": {"designer": {"x": 750, "y": 0}}
        }
    ],
    "metadata": {"instant": True, "version": 1, "designer": {"orphans": []}}
}

# ── Scenario 2: token refresh before gmail send
S2_BP = {
    "name": "Client Onboarding - 48hr Follow-up",
    "flow": [
        {
            "id": 1, "module": "http:ActionSendData", "version": 3,
            "mapper": {
                "url": f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/Leads!A2:J1000",
                "method": "GET", "parseResponse": True
            },
            "parameters": {"__IMTCONN__": SHEETS_CONN},
            "metadata": {"designer": {"x": -900, "y": 0}}
        },
        {
            "id": 2, "module": "builtin:BasicFeeder", "version": 1,
            "mapper": {"array": "{{1.data.values}}"},
            "parameters": {},
            "metadata": {"designer": {"x": -600, "y": 0}}
        },
        {
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
                    {"name": "x-api-key", "value": ANTHROPIC_KEY},
                    {"name": "anthropic-version", "value": "2023-06-01"},
                    {"name": "content-type", "value": "application/json"}
                ],
                "bodyType": "raw", "parseResponse": True, "contentType": "application/json",
                "data": json.dumps({
                    "model": "claude-sonnet-4-6", "max_tokens": 200,
                    "messages": [{"role": "user", "content": (
                        "Write a short follow-up email (under 80 words) to {{2.value[1]}} at {{2.value[2]}}. "
                        "They expressed interest in AI automation consulting two days ago but have not booked. "
                        "Their goal: {{2.value[4]}}. "
                        "Soft CTA, no pressure. Sign off as Shant."
                    )}]
                })
            },
            "parameters": {},
            "metadata": {"designer": {"x": -300, "y": 0}}
        },
        {
            **TOKEN_REFRESH_MODULE,
            "id": 4,
            "metadata": {"designer": {"x": 0, "y": 0}}
        },
        gmail_send_module(
            mid=5, token_module_id=4,
            to_ref="{{2.value[6]}}",
            subject_ref="Still thinking it over, {{2.value[1]}}?",
            body_ref="{{3.data.content[].text}}",
            x=300
        ),
        {
            "id": 6, "module": "google-sheets:updateRow", "version": 2,
            "mapper": {
                "from": "drive", "mode": "select",
                "values": {"9": "TRUE"},
                "rowNumber": "{{add(2.__idx__; 1)}}",
                "sheetId": "Leads", "spreadsheetId": SPREADSHEET_ID,
                "valueInputOption": "USER_ENTERED", "insertUnformatted": False
            },
            "parameters": {"__IMTCONN__": SHEETS_CONN},
            "metadata": {"designer": {"x": 600, "y": 0}}
        }
    ],
    "metadata": {"instant": False, "version": 1, "designer": {"orphans": []}}
}

for sid, bp in [(5089535, S1_BP), (5089536, S2_BP)]:
    r = requests.patch(f"{BASE}/scenarios/{sid}",
                       headers=HEADERS,
                       json={"blueprint": json.dumps(bp)})
    if r.status_code == 200:
        print(f"Scenario {sid} patched OK")
    else:
        print(f"Scenario {sid} FAILED {r.status_code}: {r.text[:500]}")
