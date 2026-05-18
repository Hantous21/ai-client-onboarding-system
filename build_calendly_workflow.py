"""
Build n8n Calendly Booking Tracker workflow.

When someone books via Calendly, this workflow:
  1. Receives the invitee.created webhook
  2. Looks up the invitee's email in the Leads sheet (column G)
  3. Marks column I (Booking Link Clicked) = TRUE for that row

This prevents the 48hr follow-up from being sent to people who already booked.

After running, set up the Calendly webhook at:
  calendly.com/event-types → your event → Integrations → Webhooks
  URL: https://<ngrok-url>/webhook/calendly-booking
  Event: invitee.created
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

TK = "$('Get Gmail Token').item.json"
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


# Code node: find the row number for the Calendly invitee's email
FIND_ROW_CODE = """\
const email = $('Calendly Hook').first().json.body.payload.email?.toLowerCase();
if (!email) return [];

const values = $input.first().json.values || [];
let rowNum = -1;
for (let i = 0; i < values.length; i++) {
  if (values[i][0]?.toLowerCase() === email) {
    rowNum = i + 2; // i=0 is sheet row 2 (row 1 is header)
  }
}

if (rowNum < 0) return []; // not in sheet — stop silently
return [{ json: { rowNum, email } }];
"""

nodes = [
    # 1 — Receive Calendly invitee.created event
    node("Calendly Hook", "n8n-nodes-base.webhook", 2, [0, 0], {
        "httpMethod": "POST",
        "path": "calendly-booking",
        "responseMode": "onReceived",  # reply 200 immediately, don't wait
        "options": {}
    }),

    # 2 — Refresh OAuth token for Sheets
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

    # 3 — Fetch all emails from column G (skip header row)
    node("Get Sheet Emails", "n8n-nodes-base.httpRequest", 4.2, [560, 0], {
        "method": "GET",
        "url": f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/Leads!G2:G",
        "sendHeaders": True,
        "specifyHeaders": "keypair",
        "headerParameters": {"parameters": [
            {"name": "Authorization", "value": AUTH},
        ]},
        "options": {}
    }),

    # 4 — Find matching row number
    node("Find Row", "n8n-nodes-base.code", 2, [840, 0], {
        "jsCode": FIND_ROW_CODE
    }),

    # 5 — Mark column I = TRUE for that row
    node("Mark Booking Clicked", "n8n-nodes-base.httpRequest", 4.2, [1120, 0], {
        "method": "PUT",
        "url": (
            "={{ 'https://sheets.googleapis.com/v4/spreadsheets/"
            + SPREADSHEET_ID
            + "/values/Leads!I' + $('Find Row').item.json.rowNum"
            + " + '?valueInputOption=USER_ENTERED' }}"
        ),
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
    "name": "Calendly Booking Tracker",
    "nodes": nodes,
    "connections": connections,
    "settings": {"executionOrder": "v1"},
    "staticData": None,
}

r = requests.post(f"{N8N_URL}/workflows", headers=HEADERS, json=workflow)
if r.status_code == 200:
    wf = r.json()
    print(f"Workflow created! ID: {wf['id']}")
    print(f"Webhook URL: http://localhost:5678/webhook/calendly-booking")
    print(f"Public URL:  https://<ngrok-url>/webhook/calendly-booking")
    print()
    print("Next: activate this workflow, then add the webhook in Calendly:")
    print("  calendly.com > Integrations > Webhooks > New Webhook")
    print("  Event: invitee.created")
else:
    print(f"FAILED {r.status_code}: {r.text[:500]}")
