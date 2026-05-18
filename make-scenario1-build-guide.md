# Make.com Scenario 1: Welcome Email — Manual Build Guide

Build this scenario in the Make.com UI. Five modules in order.

---

## Module 1: Webhooks → Custom Webhook

- Click **+** → search "Webhooks" → select **Custom Webhook**
- Webhook: select **Client Onboarding** (already created)
- Click OK

---

## Module 2: Google Sheets → Add a Row

- Module: **Google Sheets → Add a Row**
- Connection: **Make Academy** (connection ID 8635321)
- Spreadsheet: **Client Leads**
- Sheet name: **Leads**
- Column A (Timestamp): `{{formatDate(now; "YYYY-MM-DD HH:mm:ss")}}`
- Column B (Name): `{{1.name}}`
- Column C (Business): `{{1.business}}`
- Column D (Industry): `{{1.industry}}`
- Column E (Goal): `{{1.goal}}`
- Column F (Source): `{{1.source}}`
- Column G (Email): `{{1.email}}`
- Column H (Email Sent): `FALSE`
- Column I (Booking Link Clicked): `FALSE`
- Column J (Follow-up Sent): `FALSE`

---

## Module 3: HTTP → Make a Request (Claude API)

- Module: **HTTP → Make a Request**
- URL: `https://api.anthropic.com/v1/messages`
- Method: **POST**
- Headers (add each separately):
  - Name: `x-api-key` | Value: *(your Anthropic API key from .env)*
  - Name: `anthropic-version` | Value: `2023-06-01`
  - Name: `content-type` | Value: `application/json`
- Body type: **Raw**
- Content type: **JSON (application/json)**
- Request content (paste exactly):

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 300,
  "messages": [
    {
      "role": "user",
      "content": "You are writing on behalf of Shant, an AI automation consultant.\n\nA new prospective client just filled out an intake form. Write a warm, professional welcome email under 150 words. Include this Calendly booking link: https://calendly.com/yourname/20min\n\nClient details:\n- Name: {{1.name}}\n- Business: {{1.business}}\n- Industry: {{1.industry}}\n- Primary goal: {{1.goal}}\n\nWrite as Shant. Reference their actual goal. End with one CTA. No subject line."
    }
  ]
}
```

- Parse response: **Yes (enabled)**

---

## Module 4: Google Email → Send an Email

- Module: **Google Email → Send an Email**
- Connection: **My Gmail connection** (connection ID 8912353)
- To: `{{1.email}}`
- Subject: `{{1.name}}, re: {{1.goal}}`
- Content: `{{3.data.content[].text}}`
- Content type: **Text**

> **Note:** If this module still fails with an smtpHost error, try the alternative below.

### Alternative Module 4: Gmail via HTTP (if Google Email module fails)

Use **HTTP → Make a Request** instead:
- URL: `https://gmail.googleapis.com/upload/gmail/v1/users/me/messages/send?uploadType=media`
- Method: **POST**
- Headers:
  - Name: `Content-Type` | Value: `message/rfc822`
  - Name: `Authorization` | Value: `Bearer {{token}}` *(requires token refresh step first)*
- Body type: **Raw**
- Request content:
```
From: hantous93@gmail.com
To: {{1.email}}
Subject: {{1.name}}, re: {{1.goal}}
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8

{{3.data.content[].text}}
```

---

## Module 5: Google Sheets → Update a Row

- Module: **Google Sheets → Update a Row**
- Connection: **Make Academy**
- Spreadsheet: **Client Leads**
- Sheet name: **Leads**
- Row number: `{{2.rowNumber}}`
- Column H (Email Sent): `TRUE`

---

## Testing

1. Open Scenario 1 → click **Run once**
2. Submit a test form entry to the Tally webhook URL:
   `https://hook.us2.make.com/mcgsw76ybzep6bc4fg7a1o1twhp4slrn`
3. Verify:
   - Green checkmarks on all 5 modules
   - New row appears in Google Sheet (Client Leads → Leads tab)
   - Email arrives in test inbox within ~30 seconds
   - Email content references the specific goal entered in the form

---

## Key IDs (reference)

| Item | Value |
|------|-------|
| Sheets connection | 8635321 (Make Academy) |
| Gmail connection | 8912353 (My Gmail connection) |
| Spreadsheet ID | 1wwALFtmtgubd5apZ3-TURNRP4irNhJpveTmLrYYaDl4 |
| Webhook URL | https://hook.us2.make.com/mcgsw76ybzep6bc4fg7a1o1twhp4slrn |
| Scenario 2 ID | 5089536 (48hr follow-up — build after Scenario 1 works) |
