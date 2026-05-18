"""
Re-authorizes Google OAuth with all required scopes, including gmail.send.

Run this when the existing refresh token is missing a scope:
  python "c:/Users/shant/projects/Solo Agent Proect/reauth_google.py"

Steps:
  1. Opens a browser auth URL — approve all scopes shown
  2. Paste the code back here
  3. Saves new refresh_token to google_token.json
  4. Prints the new refresh_token so you can update patch_n8n_workflow.py
"""

import json, os
from dotenv import load_dotenv
load_dotenv()
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_ID     = os.environ["GOOGLE_CLIENT_ID"]
CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]
REDIRECT      = "urn:ietf:wg:oauth:2.0:oob"
SECRET_FILE   = r"c:\Users\shant\projects\Solo Agent Proect\client_secret.json"
TOKEN_FILE    = r"c:\Users\shant\projects\Solo Agent Proect\google_token.json"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/gmail.send",
]

flow = InstalledAppFlow.from_client_secrets_file(
    SECRET_FILE, scopes=SCOPES, redirect_uri=REDIRECT
)

auth_url, _ = flow.authorization_url(access_type="offline", prompt="consent")

print("\n" + "="*60)
print("Open this URL in your browser and approve all scopes:")
print("="*60)
print(auth_url)
print("="*60)

code = input("\nPaste the authorization code here: ").strip()

print("\nExchanging code for tokens...")
flow.fetch_token(code=code)
creds = flow.credentials

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

print(f"\nSaved to {TOKEN_FILE}")
print(f"\nNew refresh_token:\n{creds.refresh_token}")
print("\nNext: paste that token into patch_n8n_workflow.py as REFRESH_TOKEN, then re-run it.")
