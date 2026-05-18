# Directive: AI-Powered Client Onboarding Emailer

**Version:** 1.0  
**System:** Make.com + Claude AI + Gmail + Google Sheets  
**Maintained by:** [YOUR NAME]

---

## What This System Does

When a new prospect fills out your intake form, this system automatically:

1. Logs their information to your Client Leads Google Sheet
2. Sends them a personalized welcome email (written by Claude AI, in your voice) within 30 seconds
3. If they haven't clicked your booking link within 48 hours, sends one gentle follow-up

No manual copy-paste. No missed leads. Every submission gets a response that references their specific situation.

---

## Trigger

**Source:** Tally or Typeform form submission  
**Form fields captured:**
- Full Name
- Business Name
- Industry
- Primary Goal (what they want to achieve)
- How they heard about you

---

## Step-by-Step Process

### Step 1 — Log Submission
New form data is written to the **Client Leads** Google Sheet with a timestamp.

**Sheet columns:**
`Timestamp | Name | Business | Industry | Goal | Source | Email Sent | Booking Link Clicked | Follow-up Sent`

### Step 2 — Draft Welcome Email
The form data is sent to Claude API with this prompt:

> You are writing on behalf of [YOUR NAME], an AI automation consultant.
> 
> A new prospective client just filled out an intake form. Write a warm, professional welcome email under 150 words. Address their specific goal directly. Include this Calendly booking link: [YOUR_LINK].
> 
> Client details:
> - Name: {{name}}
> - Business: {{business}}
> - Industry: {{industry}}
> - Primary goal: {{goal}}
> 
> Rules:
> - First person, write as [YOUR NAME]
> - No generic filler — reference their actual goal
> - End with one clear CTA: book a 20-minute call
> - Do not include a subject line

**Model:** claude-sonnet-4-6  
**Max tokens:** 300  
**Temperature:** default (1.0)

### Step 3 — Send Welcome Email
- **From:** your Gmail account
- **To:** prospect's email (captured from form)
- **Subject:** "Welcome, {{name}} — let's talk about {{goal}}" *(customize as needed)*
- **Body:** Claude's output

### Step 4 — Update Sheet
Mark `Email Sent = TRUE` and record timestamp in the sheet.

### Step 5 — 48-Hour Follow-Up Check (Scheduled Scenario)
Every morning at 9am, the system scans the sheet for rows where:
- `Email Sent = TRUE`
- `Booking Link Clicked = FALSE`
- `Timestamp` is more than 48 hours ago
- `Follow-up Sent = FALSE`

For each matching row, Claude drafts a short follow-up using this prompt:

> Write a short, friendly follow-up email (under 80 words) to {{name}} at {{business}}. They expressed interest in [YOUR SERVICE] two days ago but haven't booked a call yet. Reference their goal: {{goal}}. One soft CTA — no pressure. Sign off as [YOUR NAME].

The follow-up is sent, and `Follow-up Sent = TRUE` is written to the sheet.

---

## Booking Link Click Tracking

Use a redirect link (e.g., bit.ly or a simple redirect on your domain) as your booking link. Configure the redirect destination as your Calendly URL, and also set up a Make.com webhook on that redirect URL so that when it's clicked, it updates `Booking Link Clicked = TRUE` in the sheet.

This prevents follow-up emails from going to prospects who already booked.

---

## Error Handling

| Scenario | What Happens |
|---|---|
| Claude API returns error | Make.com stops the scenario and logs error to execution history |
| Gmail send fails | Make.com retries up to 3 times |
| Form field missing | Scenario continues; Claude prompt uses "your business" as fallback |

---

## Make.com Scenario Map

**Scenario 1 — Welcome Email:**
```
Tally/Typeform Webhook → Google Sheets (Add Row) → HTTP Module (Claude API) → Gmail (Send) → Google Sheets (Update Row)
```

**Scenario 2 — Follow-Up:**
```
Schedule (daily 9am) → Google Sheets (Search Rows) → Iterator → HTTP Module (Claude API) → Gmail (Send) → Google Sheets (Update Row)
```

---

## Customization Points

- **Email subject line:** Edit in the Gmail module
- **Claude tone:** Add/remove adjectives in the prompt (e.g., "warm and direct" vs. "formal and professional")
- **Follow-up timing:** Change the 48-hour threshold in Scenario 2's filter
- **Booking link:** Update in both prompts and in the tracking redirect

---

## What's Not Automated

- Replies from prospects — you respond to those manually
- Calls themselves — booked via Calendly, conducted by you
- Follow-ups beyond the first one — extend Scenario 2 or build a drip sequence for that

---

## Deliverables Included

- Working Make.com Scenario 1 (welcome email)
- Working Make.com Scenario 2 (48hr follow-up)
- This Directive document
- 30-day support for questions and adjustments
