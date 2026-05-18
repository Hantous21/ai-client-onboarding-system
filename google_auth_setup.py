"""
Run this script in your terminal:
  python3 "c:/Users/shant/projects/Solo Agent Proect/google_auth_setup.py"

It will:
1. Print an auth URL — open it in your browser
2. Prompt you to paste the code
3. Create the Google Sheet and save credentials
"""
import json, os, sys
from dotenv import load_dotenv
load_dotenv()
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

CLIENT_ID     = os.environ["GOOGLE_CLIENT_ID"]
CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]
REDIRECT      = "urn:ietf:wg:oauth:2.0:oob"
TOKEN_URI     = "https://oauth2.googleapis.com/token"
SCOPES        = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file"
]

SECRET_FILE = r"c:\Users\shant\projects\Solo Agent Proect\client_secret.json"
TOKEN_FILE  = r"c:\Users\shant\projects\Solo Agent Proect\google_token.json"
PROJECT_DIR = r"c:\Users\shant\projects\Solo Agent Proect"

# ── Step 1: Generate auth URL (flow stores PKCE verifier internally) ───────────
flow = InstalledAppFlow.from_client_secrets_file(
    SECRET_FILE, scopes=SCOPES, redirect_uri=REDIRECT
)

auth_url, _ = flow.authorization_url(access_type="offline", prompt="consent")

print("\n" + "="*60)
print("STEP 1: Open this URL in your browser:")
print("="*60)
print(auth_url)
print("="*60)

# ── Step 2: Get code from user ─────────────────────────────────────────────────
code = input("\nPaste the authorization code here: ").strip()

# ── Step 3: Exchange code — use flow.fetch_token so PKCE verifier is included ──
print("\nExchanging code for tokens...")
flow.fetch_token(code=code)
creds = flow.credentials
print("Tokens obtained. Refresh token present:", creds.refresh_token is not None)

# Save tokens
token_data = {
    "access_token":  creds.token,
    "refresh_token": creds.refresh_token,
    "token_uri":     creds.token_uri,
    "client_id":     creds.client_id,
    "client_secret": creds.client_secret,
    "scopes":        list(creds.scopes)
}
with open(TOKEN_FILE, "w") as f:
    json.dump(token_data, f, indent=2)
print(f"Tokens saved to {TOKEN_FILE}")

# ── Step 4: Create Google Sheet ────────────────────────────────────────────────

service = build("sheets", "v4", credentials=creds)

print("\nCreating 'Client Leads' Google Sheet...")
result = service.spreadsheets().create(body={
    "properties": {"title": "Client Leads"},
    "sheets": [{"properties": {
        "title": "Leads",
        "gridProperties": {"rowCount": 1000, "columnCount": 10}
    }}]
}).execute()

sheet_id  = result["spreadsheetId"]
sheet_url = result["spreadsheetUrl"]

# Add headers
headers = [["Timestamp","Name","Business","Industry","Goal",
            "Source","Email","Email Sent","Booking Link Clicked","Follow-up Sent"]]
service.spreadsheets().values().update(
    spreadsheetId=sheet_id,
    range="Leads!A1:J1",
    valueInputOption="RAW",
    body={"values": headers}
).execute()

# Bold header row
service.spreadsheets().batchUpdate(
    spreadsheetId=sheet_id,
    body={"requests": [{
        "repeatCell": {
            "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1},
            "cell": {"userEnteredFormat": {"textFormat": {"bold": True}}},
            "fields": "userEnteredFormat.textFormat.bold"
        }
    }]}
).execute()

# Freeze header row
service.spreadsheets().batchUpdate(
    spreadsheetId=sheet_id,
    body={"requests": [{
        "updateSheetProperties": {
            "properties": {"sheetId": 0, "gridProperties": {"frozenRowCount": 1}},
            "fields": "gridProperties.frozenRowCount"
        }
    }]}
).execute()

print(f"\nSheet created successfully!")
print(f"URL: {sheet_url}")
print(f"ID : {sheet_id}")

# ── Step 5: Update .env ────────────────────────────────────────────────────────
env_path = os.path.join(PROJECT_DIR, ".env")
with open(env_path, "r") as f:
    env_content = f.read()

env_content = env_content.replace(
    "GOOGLE_SPREADSHEET_ID=REPLACE_WITH_YOUR_SPREADSHEET_ID",
    f"GOOGLE_SPREADSHEET_ID={sheet_id}"
)

with open(env_path, "w") as f:
    f.write(env_content)
print(f"\n.env updated with GOOGLE_SPREADSHEET_ID={sheet_id}")
print("\nDONE. Next: update the spreadsheet ID in your Make.com scenarios.")
