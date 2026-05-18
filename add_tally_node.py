"""
Inserts a "Parse Tally Data" Code node between Intake Form and Get Gmail Token.

The Code node handles two incoming formats:
  - Tally webhook payload  (body.data.fields[])
  - Direct test JSON       (body.name, body.business, etc.)

Both paths output the same flat shape: {name, business, industry, goal, source, email}
so all downstream nodes are unaffected.
"""

import json, requests, os
from dotenv import load_dotenv
load_dotenv()

N8N_URL = "http://localhost:5678/api/v1"
N8N_KEY = os.environ["N8N_API_KEY"]
WF_ID   = os.environ["N8N_WORKFLOW_1_ID"]
HEADERS = {"X-N8N-API-KEY": N8N_KEY, "Content-Type": "application/json"}

JS_CODE = """\
const body = $input.first().json.body;

// Tally webhook format: { data: { fields: [{label, value}] } }
if (body && body.data && body.data.fields) {
  const fields = body.data.fields;
  const get = (label) => {
    const f = fields.find(f => f.label === label);
    if (!f) return '';
    return Array.isArray(f.value) ? f.value[0] : f.value;
  };
  return [{ json: {
    name:     get('Full Name'),
    business: get('Business Name'),
    industry: get('Industry'),
    goal:     get('Primary Goal'),
    source:   get('How did you find me?'),
    email:    get('Email'),
  }}];
}

// Direct / test JSON format: { name, business, industry, goal, source, email }
return [{ json: {
  name:     body.name     || '',
  business: body.business || '',
  industry: body.industry || '',
  goal:     body.goal     || '',
  source:   body.source   || '',
  email:    body.email    || '',
}}];
"""

r = requests.get(f"{N8N_URL}/workflows/{WF_ID}", headers=HEADERS)
wf = r.json()

ALLOWED = {"name", "nodes", "connections", "settings", "staticData", "pinData"}
wf = {k: v for k, v in wf.items() if k in ALLOWED}

# Skip if already added
if any(n["name"] == "Parse Tally Data" for n in wf["nodes"]):
    print("Parse Tally Data node already exists — skipping insert")
else:
    # Place between Intake Form (0,0) and Get Gmail Token (280,0)
    wf["nodes"].append({
        "id": "parse-tally-data",
        "name": "Parse Tally Data",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [140, 0],
        "parameters": {
            "jsCode": JS_CODE
        }
    })

    # Rewire: Intake Form → Parse Tally Data → Get Gmail Token
    wf["connections"]["Intake Form"] = {
        "main": [[{"node": "Parse Tally Data", "type": "main", "index": 0}]]
    }
    wf["connections"]["Parse Tally Data"] = {
        "main": [[{"node": "Get Gmail Token", "type": "main", "index": 0}]]
    }

    r2 = requests.put(f"{N8N_URL}/workflows/{WF_ID}", headers=HEADERS, json=wf)
    if r2.status_code == 200:
        print("Parse Tally Data node inserted OK")
    else:
        print(f"FAILED {r2.status_code}: {r2.text[:500]}")
