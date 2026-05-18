"""
Build n8n Client Onboarding - Welcome Email workflow via API.

Flow: Webhook → Get Gmail Token → Append to Sheets → Draft with Claude
      → Send via SMTP → Mark Email Sent in Sheets
"""

import json, os
import requests
import uuid
from dotenv import load_dotenv
load_dotenv()

N8N_URL = "http://localhost:5678/api/v1"
N8N_KEY = os.environ["N8N_API_KEY"]
HEADERS = {"X-N8N-API-KEY": N8N_KEY, "Content-Type": "application/json"}

ANTHROPIC_KEY  = os.environ["ANTHROPIC_API_KEY"]
SPREADSHEET_ID = os.environ["GOOGLE_SPREADSHEET_ID"]
SMTP_CRED_ID   = os.environ["N8N_SMTP_CRED_ID"]
CLIENT_ID      = os.environ["GOOGLE_CLIENT_ID"]
CLIENT_SECRET  = os.environ["GOOGLE_CLIENT_SECRET"]
REFRESH_TOKEN  = os.environ["GOOGLE_REFRESH_TOKEN"]
FROM_EMAIL     = os.environ["FROM_EMAIL"]

# Expression shortcuts
WH = "$('Intake Form').item.json.body"   # webhook body reference
TK = "$('Get Gmail Token').item.json"    # token node reference


def node(name, ntype, version, pos, params, credentials=None):
    n = {
        "id": str(uuid.uuid4()),
        "name": name,
        "type": ntype,
        "typeVersion": version,
        "position": pos,
        "parameters": params,
    }
    if credentials:
        n["credentials"] = credentials
    return n


# ── Sheets append body (values must be a 2-D array)
sheets_append_body = (
    '={{"values":[[' +
    f'"={{{{ $now.toFormat(\'yyyy-MM-dd HH:mm:ss\') }}}}",' +
    f'"={{{{ {WH}.name }}}}",' +
    f'"={{{{ {WH}.business }}}}",' +
    f'"={{{{ {WH}.industry }}}}",' +
    f'"={{{{ {WH}.goal }}}}",' +
    f'"={{{{ {WH}.source }}}}",' +
    f'"={{{{ {WH}.email }}}}",' +
    '"FALSE","FALSE","FALSE"' +
    "]]}}"
)

# ── Claude prompt assembled as a JS expression so we can interpolate fields
claude_prompt_expr = (
    "={{ "
    "'You are writing on behalf of Shant, an AI automation consultant.\\n\\n"
    "A new prospective client just filled out an intake form. "
    "Write a warm, professional welcome email under 150 words. "
    "Include this Calendly booking link: https://calendly.com/yourname/20min\\n\\n"
    "Client details:\\n"
    "- Name: ' + " + WH + ".name + '\\n"
    "- Business: ' + " + WH + ".business + '\\n"
    "- Industry: ' + " + WH + ".industry + '\\n"
    "- Primary goal: ' + " + WH + ".goal + '\\n\\n"
    "Write as Shant. Reference their actual goal. End with one CTA. No subject line.' }}"
)

claude_body = json.dumps({
    "model": "claude-sonnet-4-6",
    "max_tokens": 300,
    "messages": [{"role": "user", "content": claude_prompt_expr}]
})

# ── Row number extracted from Sheets append response, e.g. "Leads!A6:J6" → 6
row_expr = "$('Log to Sheets').item.json.updates.updatedRange.match(/\\d+/)[0]"

sheets_update_url = (
    "=`https://sheets.googleapis.com/v4/spreadsheets/"
    + SPREADSHEET_ID
    + "/values/Leads!H${"
    + row_expr
    + "}?valueInputOption=USER_ENTERED`"
)

nodes = [
    # 1 — Webhook trigger
    node("Intake Form", "n8n-nodes-base.webhook", 2, [0, 0], {
        "httpMethod": "POST",
        "path": "client-onboarding",
        "responseMode": "lastNode",
        "options": {}
    }),

    # 2 — Google OAuth token refresh
    node("Get Gmail Token", "n8n-nodes-base.httpRequest", 4.2, [280, 0], {
        "method": "POST",
        "url": "https://oauth2.googleapis.com/token",
        "sendBody": True,
        "contentType": "form-urlencoded",
        "bodyParameters": {"parameters": [
            {"name": "grant_type",    "value": "refresh_token"},
            {"name": "client_id",    "value": CLIENT_ID},
            {"name": "client_secret","value": CLIENT_SECRET},
            {"name": "refresh_token","value": REFRESH_TOKEN},
        ]},
        "options": {}
    }),

    # 3 — Append row to Google Sheets
    node("Log to Sheets", "n8n-nodes-base.httpRequest", 4.2, [560, 0], {
        "method": "POST",
        "url": (
            f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}"
            "/values/Leads!A:J:append?valueInputOption=USER_ENTERED"
        ),
        "sendHeaders": True,
        "headerParameters": {"parameters": [
            {"name": "Authorization", "value": f"={{{{ {TK}.access_token }}}}"},
        ]},
        "sendBody": True,
        "contentType": "json",
        "body": sheets_append_body,
        "options": {}
    }),

    # 4 — Claude API: draft personalized email
    node("Draft Email", "n8n-nodes-base.httpRequest", 4.2, [840, 0], {
        "method": "POST",
        "url": "https://api.anthropic.com/v1/messages",
        "sendHeaders": True,
        "headerParameters": {"parameters": [
            {"name": "x-api-key",         "value": ANTHROPIC_KEY},
            {"name": "anthropic-version", "value": "2023-06-01"},
            {"name": "content-type",      "value": "application/json"},
        ]},
        "sendBody": True,
        "contentType": "json",
        "body": claude_body,
        "options": {}
    }),

    # 5 — Send via SMTP
    node("Send Welcome Email", "n8n-nodes-base.emailSend", 2.1, [1120, 0], {
        "fromEmail": FROM_EMAIL,
        "toEmail":   f"={{{{ {WH}.email }}}}",
        "subject":   f"={{{{ {WH}.name }}}}, re: {{{{ {WH}.goal }}}}",
        "emailType": "text",
        "message":   "={{ $('Draft Email').item.json.content[0].text }}",
        "options": {}
    }, credentials={"smtp": {"id": SMTP_CRED_ID, "name": "SMTP account"}}),

    # 6 — Update Sheets row: mark Email Sent = TRUE
    node("Mark Email Sent", "n8n-nodes-base.httpRequest", 4.2, [1400, 0], {
        "method": "PUT",
        "url": sheets_update_url,
        "sendHeaders": True,
        "headerParameters": {"parameters": [
            {"name": "Authorization", "value": f"={{{{ {TK}.access_token }}}}"},
        ]},
        "sendBody": True,
        "contentType": "json",
        "body": '{"values":[["TRUE"]]}',
        "options": {}
    }),
]

# Linear connections: each node → next
connections = {}
for i in range(len(nodes) - 1):
    connections[nodes[i]["name"]] = {
        "main": [[{"node": nodes[i + 1]["name"], "type": "main", "index": 0}]]
    }

workflow = {
    "name": "Client Onboarding - Welcome Email",
    "nodes": nodes,
    "connections": connections,
    "settings": {"executionOrder": "v1"},
    "staticData": None,
}

r = requests.post(f"{N8N_URL}/workflows", headers=HEADERS, json=workflow)
if r.status_code == 200:
    result = r.json()
    wf_id = result["id"]
    print(f"Workflow created! ID: {wf_id}")
    print(f"Test webhook URL : http://localhost:5678/webhook-test/client-onboarding")
    print(f"Prod webhook URL : http://localhost:5678/webhook/client-onboarding")
    print()
    print("Next steps:")
    print("1. Open http://localhost:5678 and verify the workflow appears")
    print("2. Click 'Test workflow', then POST a test payload to the test webhook URL")
    print("3. Confirm: Sheets row created, email received, row marked TRUE")
else:
    print(f"FAILED {r.status_code}")
    print(r.text[:2000])
