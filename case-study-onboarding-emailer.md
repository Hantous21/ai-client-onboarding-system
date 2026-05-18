# Case Study: AI-Powered Client Onboarding Emailer

---

## The Problem

Every time a prospect filled out an intake form, the follow-up was manual. Copy the name, write a personalized email, remember to follow up two days later if they didn't book — all of it depended on someone remembering to do it. Response times varied. Follow-ups got missed. The process didn't scale.

For service businesses (consultants, bookkeepers, agencies), this is a common leak: the lead arrives, but the response isn't fast enough or personal enough to convert.

---

## The Solution

An n8n automation that runs the moment a form is submitted:

1. **Logs the lead** to a Google Sheet — no more scattered inboxes or manual spreadsheet updates
2. **Drafts and sends a personalized welcome email in under 30 seconds** — Claude reads the prospect's stated goal and writes an email that directly addresses it, in the founder's voice
3. **Follows up automatically at 48 hours** if the prospect hasn't booked a call — one gentle nudge, then stops

No templates. No mail merge. Each email is generated fresh based on what the prospect actually said.

---

## Build Details

**Tools:** n8n (self-hosted) · Claude API (claude-sonnet-4-6) · Tally · Gmail API · Google Sheets  
**Build time:** ~6 hours  
**Ongoing cost:** ~$0.02–$0.05 per lead (Claude API usage only)

---

## Results

| Metric | Before | After |
|---|---|---|
| Time to first response | Hours (manual) | Under 30 seconds |
| Follow-up consistency | Inconsistent | 100% — never missed |
| Time spent per new lead | 5–10 min | 0 min |
| Emails that reference prospect's specific goal | Depends on writer | Every single one |

*Results based on live test scenario with simulated lead submissions across multiple industries.*

---

## Sample Output

**Form input:**
- Name: Sarah Chen
- Business: Chen & Associates Bookkeeping
- Industry: Accounting
- Goal: Automate my monthly client reporting so I stop spending Sundays on spreadsheets

**Claude-generated welcome email (sent in ~20 seconds):**

> Hi Sarah,
>
> Thanks for reaching out — automating your monthly reporting so you get your Sundays back is exactly the kind of problem I love solving.
>
> For a bookkeeping practice like yours, we can set up a workflow that pulls your client data, generates a plain-English summary, and delivers it to each client automatically — no manual formatting, no Sunday scramble.
>
> I'd love to walk you through what that looks like for your specific setup. You can grab a 20-minute slot here: https://calendly.com/hantous93
>
> Looking forward to it,  
> Sammi Hantous  
> AI Automation Consultant

**48-hour follow-up (sent automatically if no booking):**

> Hi Sarah,
>
> Just wanted to follow up since we connected a couple of days ago — no worries if the timing hasn't been right.
>
> When you're ready to explore what automating your monthly reporting could look like, I'd love to map it out with you.
>
> Feel free to grab a time here: https://calendly.com/hantous93
>
> Sammi Hantous  
> AI Automation Consultant

---

## Who This Is Built For

Any service business that:
- Gets leads through a form
- Wants faster, more personal responses without more manual work
- Is losing deals to slow follow-up

Best fit: bookkeeping firms, consultants, agencies, coaches, financial advisors

---

## Finance Operations Extension

For accounting and financial services clients, this system can be extended to:
- Send an engagement letter via PandaDoc for e-signature immediately after the welcome email
- Trigger a client portal invite (Karbon, Canopy, or similar)
- Log the lead directly to a CRM or practice management tool

This saves 45–90 minutes per new client onboarding — at 5 new clients per month, that's 4–7 hours recovered monthly.

---

*Built by Sammi Hantous · AI Automation Consultant · [YOUR WEBSITE]*
