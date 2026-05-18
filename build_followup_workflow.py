"""
Build n8n 48hr Follow-up workflow.

Runs on a schedule (every hour). For each lead where:
  - Email Sent = TRUE      (column H)
  - Booking Clicked = FALSE (column I) — already booked, skip them
  - Follow-up Sent = FALSE  (column J)
  - Timestamp > 48 hours ago (column A)

Claude drafts a short follow-up (<80 words), sends it via Gmail API,
and marks column J = TRUE.
"""

import json, requests, uuid, os
from dotenv import load_dotenv
load_dotenv()

N8N_URL = "http://localhost:5678/api/v1"
N8N_KEY = os.environ["N8N_API_KEY"]
HEADERS = {"X-N8N-API-KEY": N8N_KEY, "Content-Type": "application/json"}

SPREADSHEET_ID = os.environ["GOOGLE_SPREADSHEET_ID"]
CLIENT_ID      = os.environ["GOOGLE_CLIENT_ID"]
CLIENT_SECRET  = os.environ["GOOGLE_CLIENT_SECRET"]
REFRESH_TOKEN  = os.environ["GOOGLE_REFRESH_TOKEN"]
ANTHROPIC_KEY  = os.environ["ANTHROPIC_API_KEY"]
FROM_EMAIL     = os.environ["FROM_EMAIL"]

TK   = "$('Get Gmail Token').item.json"
FR   = "$('Filter Rows').item.json"
AUTH = f"={{{{ 'Bearer ' + {TK}.access_token }}}}"


def node(name, ntype, version, pos, params):
    return {
        "id": str(uuid.uuid4()),
        "name": name,
        "type": ntype,
        "typeVersion": version,
        "position": pos,
        "parameters": params,
    }


# Filter rows meeting all follow-up criteria
FILTER_CODE = """\
const rows = $input.first().json.values || [];
const cutoff = Date.now() - 48 * 60 * 60 * 1000;

return rows.reduce((acc, row, i) => {
  const [ts, name, business, industry, goal, source, email,
         emailSent, bookingClicked, followupSent] = row;

  if (emailSent !== 'TRUE')       return acc; // welcome email not sent yet
  if (bookingClicked === 'TRUE')  return acc; // already booked — skip
  if (followupSent === 'TRUE')    return acc; // already followed up

  const t = new Date(ts.replace(' ', 'T')).getTime();
  if (isNaN(t) || t > cutoff)    return acc; // less than 48hrs ago

  acc.push({ json: { rowNum: i + 2, name, business, industry, goal, email } });
  return acc;
}, []);
"""

# Claude follow-up prompt expression
followup_body_expr = (
    "={{ JSON.stringify({"
    "model:'claude-sonnet-4-6',"
    "max_tokens:200,"
    "messages:[{role:'user',content:"
    "'Write a short follow-up email under 80 words to '"
    f" + {FR}.name + ' at ' + {FR}.business + "
    "'. They expressed interest in AI automation two days ago but haven\\'t booked a call yet."
    " Their goal: ' + "
    f"{FR}.goal + "
    "'. One gentle CTA to book: https://calendly.com/hantous93."
    " Warm tone, no pressure. Sign off as Sammi Hantous, AI Automation Consultant. No subject line.'"
    "}]}) }}"
)

# RFC 2822 email body expression
followup_rfc822_expr = (
    "={{ "
    "'From: hantous93@gmail.com\\r\\n'"
    f" + 'To: ' + {FR}.email + '\\r\\n'"
    f" + 'Subject: Quick follow-up, ' + {FR}.name + '\\r\\n'"
    " + 'MIME-Version: 1.0\\r\\n'"
    " + 'Content-Type: text/plain; charset=UTF-8\\r\\n'"
    " + '\\r\\n'"
    " + $('Draft Follow-up').item.json.content[0].text"
    " }}"
)

# Mark column J URL
mark_followup_url = (
    "={{ 'https://sheets.googleapis.com/v4/spreadsheets/"
    + SPREADSHEET_ID
    + "/values/Leads!J' + "
    f"{FR}.rowNum"
    + " + '?valueInputOption=USER_ENTERED' }}"
)

nodes = [
    # 1 — Schedule trigger: every 1 hour
    node("Schedule", "n8n-nodes-base.scheduleTrigger", 1.2, [0, 0], {
        "rule": {
            "interval": [{"field": "hours", "hoursInterval": 1}]
        }
    }),

    # 2 — Refresh OAuth token
    node("Get Gmail Token", "n8n-nodes-base.httpRequest", 4.2, [280, 0], {
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
        "options": {}
    }),

    # 3 — Fetch all data rows (skip header)
    node("Get All Rows", "n8n-nodes-base.httpRequest", 4.2, [560, 0], {
        "method": "GET",
        "url": f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/Leads!A2:J",
        "sendHeaders": True,
        "specifyHeaders": "keypair",
        "headerParameters": {"parameters": [
            {"name": "Authorization", "value": AUTH},
        ]},
        "options": {}
    }),

    # 4 — Filter: one output item per lead needing follow-up
    node("Filter Rows", "n8n-nodes-base.code", 2, [840, 0], {
        "jsCode": FILTER_CODE
    }),

    # 5 — Claude drafts short follow-up per lead
    node("Draft Follow-up", "n8n-nodes-base.httpRequest", 4.2, [1120, 0], {
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
        "body": followup_body_expr,
        "options": {}
    }),

    # 6 — Send follow-up via Gmail API
    node("Send Follow-up", "n8n-nodes-base.httpRequest", 4.2, [1400, 0], {
        "method": "POST",
        "url": "https://gmail.googleapis.com/upload/gmail/v1/users/me/messages/send?uploadType=media",
        "sendHeaders": True,
        "specifyHeaders": "keypair",
        "headerParameters": {"parameters": [
            {"name": "Authorization", "value": AUTH},
        ]},
        "sendBody": True,
        "contentType": "raw",
        "rawContentType": "message/rfc822",
        "body": followup_rfc822_expr,
        "options": {}
    }),

    # 7 — Mark column J = TRUE
    node("Mark Follow-up Sent", "n8n-nodes-base.httpRequest", 4.2, [1680, 0], {
        "method": "PUT",
        "url": mark_followup_url,
        "sendHeaders": True,
        "specifyHeaders": "keypair",
        "headerParameters": {"parameters": [
            {"name": "Authorization", "value": AUTH},
        ]},
        "sendBody": True,
        "contentType": "raw",
        "rawContentType": "application/json",
        "body": '{"values":[["TRUE"]]}',
        "options": {}
    }),
]

connections = {}
for i in range(len(nodes) - 1):
    connections[nodes[i]["name"]] = {
        "main": [[{"node": nodes[i + 1]["name"], "type": "main", "index": 0}]]
    }

workflow = {
    "name": "Client Onboarding - 48hr Follow-up",
    "nodes": nodes,
    "connections": connections,
    "settings": {"executionOrder": "v1"},
    "staticData": None,
}

r = requests.post(f"{N8N_URL}/workflows", headers=HEADERS, json=workflow)
if r.status_code == 200:
    wf = r.json()
    print(f"Workflow created! ID: {wf['id']}")
    print("Activate in n8n UI to start the hourly schedule.")
    print("To test immediately: manually trigger from n8n UI.")
else:
    print(f"FAILED {r.status_code}: {r.text[:500]}")
