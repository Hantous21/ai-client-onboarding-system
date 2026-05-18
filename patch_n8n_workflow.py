"""
Patch the n8n workflow: fix HTTP node bodies and Authorization headers.

Root causes found:
  1. n8n ignored `body` param → stored as empty keypair. Fix: specifyBody=string + body=JSON.stringify expr
  2. Authorization header missing 'Bearer ' prefix. Fix: ={{ 'Bearer ' + token }}
"""

import json, requests, os
from dotenv import load_dotenv
load_dotenv()

N8N_URL  = "http://localhost:5678/api/v1"
N8N_KEY  = os.environ["N8N_API_KEY"]
WF_ID    = os.environ["N8N_WORKFLOW_1_ID"]
HEADERS  = {"X-N8N-API-KEY": N8N_KEY, "Content-Type": "application/json"}

ANTHROPIC_KEY  = os.environ["ANTHROPIC_API_KEY"]
SPREADSHEET_ID = os.environ["GOOGLE_SPREADSHEET_ID"]
CLIENT_ID      = os.environ["GOOGLE_CLIENT_ID"]
CLIENT_SECRET  = os.environ["GOOGLE_CLIENT_SECRET"]
REFRESH_TOKEN  = os.environ["GOOGLE_REFRESH_TOKEN"]
SMTP_CRED_ID   = os.environ["N8N_SMTP_CRED_ID"]
FROM_EMAIL     = os.environ["FROM_EMAIL"]

# Short aliases for n8n expressions
WH = "$('Parse Tally Data').item.json"
TK = "$('Get Gmail Token').item.json.access_token"

# Bearer token expression (correct n8n concat syntax)
AUTH_EXPR = f"={{{{ 'Bearer ' + {TK} }}}}"

# ── Node parameter overrides keyed by node name ────────────────────────────────

# Google OAuth form body (unchanged — was working, but let's be explicit)
token_body_expr = (
    "={{ JSON.stringify({"
    "grant_type:'refresh_token',"
    f"client_id:'{CLIENT_ID}',"
    f"client_secret:'{CLIENT_SECRET}',"
    f"refresh_token:'{REFRESH_TOKEN}'"
    "}) }}"
)

# Sheets append: 2-D array via JSON.stringify expression
sheets_append_expr = (
    "={{ JSON.stringify({values:[["
    f"$now.toFormat('yyyy-MM-dd HH:mm:ss'),"
    f"{WH}.name,"
    f"{WH}.business,"
    f"{WH}.industry,"
    f"{WH}.goal,"
    f"{WH}.source,"
    f"{WH}.email,"
    "'FALSE','FALSE','FALSE'"
    "]]}) }}"
)

# Claude body: entire JSON built as expression so fields are interpolated
claude_prompt = (
    "'You are writing on behalf of Sammi Hantous, an AI automation consultant.\\n\\n"
    "A new prospective client just filled out an intake form. "
    "Write a warm, professional welcome email under 150 words. "
    "Include this Calendly booking link: https://calendly.com/hantous93\\n\\n"
    "Client details:\\n"
    "- Name: ' + " + WH + ".name + '\\n"
    "- Business: ' + " + WH + ".business + '\\n"
    "- Industry: ' + " + WH + ".industry + '\\n"
    "- Primary goal: ' + " + WH + ".goal + '\\n\\n"
    "Write as Sammi Hantous. Reference their actual goal. End with one CTA. No subject line.'"
)

claude_body_expr = (
    "={{ JSON.stringify({"
    "model:'claude-sonnet-4-6',"
    "max_tokens:300,"
    f"messages:[{{role:'user',content:{claude_prompt}}}]"
    "}) }}"
)

# Sheets update URL — use string concatenation, not template literals, to avoid
# n8n expression-closer `}}` being confused with template literal syntax.
row_num_expr = "$('Log to Sheets').item.json.updates.updatedRange.match(/\\d+/)[0]"
sheets_update_url_expr = (
    "={{ 'https://sheets.googleapis.com/v4/spreadsheets/"
    + SPREADSHEET_ID
    + "/values/Leads!H' + "
    + row_num_expr
    + " + '?valueInputOption=USER_ENTERED' }}"
)

sheets_update_body = '{"values":[["TRUE"]]}'

# Gmail send — raw RFC 2822 message built as an n8n expression.
# uploadType=media with Content-Type: message/rfc822 is the simplest Gmail API send path.
gmail_send_body_expr = (
    "={{ "
    "'From: hantous93@gmail.com\\r\\n'"
    " + 'To: ' + " + WH + ".email + '\\r\\n'"
    " + 'Subject: ' + " + WH + ".name + ', re: ' + " + WH + ".goal + '\\r\\n'"
    " + 'MIME-Version: 1.0\\r\\n'"
    " + 'Content-Type: text/plain; charset=UTF-8\\r\\n'"
    " + '\\r\\n'"
    " + $('Draft Email').item.json.content[0].text"
    " }}"
)

NODE_PATCHES = {
    "Get Gmail Token": {
        "method": "POST",
        "url": "https://oauth2.googleapis.com/token",
        "sendBody": True,
        "contentType": "form-urlencoded",
        "specifyBody": "keypair",
        "bodyParameters": {"parameters": [
            {"name": "grant_type",    "value": "refresh_token"},
            {"name": "client_id",    "value": CLIENT_ID},
            {"name": "client_secret","value": CLIENT_SECRET},
            {"name": "refresh_token","value": REFRESH_TOKEN},
        ]},
        "sendHeaders": False,
        "options": {}
    },
    # contentType "raw" + rawContentType sends the body string as-is with the given Content-Type.
    # "json" mode was treating the string as a form key — raw avoids that.
    "Log to Sheets": {
        "method": "POST",
        "url": (
            f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}"
            "/values/Leads!A1:J1:append?valueInputOption=USER_ENTERED"
        ),
        "sendHeaders": True,
        "specifyHeaders": "keypair",
        "headerParameters": {"parameters": [
            {"name": "Authorization", "value": AUTH_EXPR},
        ]},
        "sendBody": True,
        "contentType": "raw",
        "rawContentType": "application/json",
        "body": sheets_append_expr,
        "options": {}
    },
    "Draft Email": {
        "method": "POST",
        "url": "https://api.anthropic.com/v1/messages",
        "sendHeaders": True,
        "specifyHeaders": "keypair",
        "headerParameters": {"parameters": [
            {"name": "x-api-key",         "value": ANTHROPIC_KEY},
            {"name": "anthropic-version", "value": "2023-06-01"},
        ]},
        "sendBody": True,
        "contentType": "raw",
        "rawContentType": "application/json",
        "body": claude_body_expr,
        "options": {}
    },
    "Send Welcome Email": {
        "method": "POST",
        "url": "https://gmail.googleapis.com/upload/gmail/v1/users/me/messages/send?uploadType=media",
        "sendHeaders": True,
        "specifyHeaders": "keypair",
        "headerParameters": {"parameters": [
            {"name": "Authorization", "value": AUTH_EXPR},
        ]},
        "sendBody": True,
        "contentType": "raw",
        "rawContentType": "message/rfc822",
        "body": gmail_send_body_expr,
        "options": {}
    },
    "Mark Email Sent": {
        "method": "PUT",
        "url": sheets_update_url_expr,
        "sendHeaders": True,
        "specifyHeaders": "keypair",
        "headerParameters": {"parameters": [
            {"name": "Authorization", "value": AUTH_EXPR},
        ]},
        "sendBody": True,
        "contentType": "raw",
        "rawContentType": "application/json",
        "body": sheets_update_body,
        "options": {}
    },
}

# ── Fetch, patch, and PUT back ──────────────────────────────────────────────

r = requests.get(f"{N8N_URL}/workflows/{WF_ID}", headers=HEADERS)
wf = r.json()

# Keep only fields the PUT endpoint accepts
ALLOWED = {"name", "nodes", "connections", "settings", "staticData", "pinData"}
wf = {k: v for k, v in wf.items() if k in ALLOWED}

patched = 0
for node in wf["nodes"]:
    if node["name"] in NODE_PATCHES:
        node["parameters"] = NODE_PATCHES[node["name"]]
        if node["name"] == "Send Welcome Email":
            node["type"] = "n8n-nodes-base.httpRequest"
            node["typeVersion"] = 4.2
            node.pop("credentials", None)  # remove SMTP — auth is in the Authorization header
        patched += 1

print(f"Patching {patched} nodes...")

r2 = requests.put(f"{N8N_URL}/workflows/{WF_ID}", headers=HEADERS, json=wf)
if r2.status_code == 200:
    print("Workflow patched OK")
    print(f"Test webhook URL: http://localhost:5678/webhook-test/client-onboarding")
else:
    print(f"FAILED {r2.status_code}: {r2.text[:1000]}")
