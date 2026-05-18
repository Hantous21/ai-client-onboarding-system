# AI Client Onboarding System

An n8n automation that responds to new lead form submissions in under 30 seconds — logs the lead, generates a personalized email using Claude, sends it via Gmail, and follows up automatically at 48 hours if the prospect hasn't booked.

**Built for:** service businesses (consultants, bookkeepers, agencies, coaches) that lose deals to slow or generic follow-up.

---

## Results

| Metric | Before | After |
|---|---|---|
| Time to first response | Hours (manual) | **Under 30 seconds** |
| Follow-up consistency | Inconsistent | **100% — never missed** |
| Manual time per lead | 5–10 min | **0 min** |
| Cost per lead | ~$5–15 in labor | **~$0.03 (API only)** |

---

## How It Works

```
Form submit (Tally)
  → n8n webhook triggered immediately
  → Lead logged to Google Sheet
  → Prospect's goal sent to Claude API
  → Claude generates personalized email in founder's voice
  → Gmail API sends email  (<30 seconds from form submit)
  → 48-hour wait node
  → [If no Calendly booking] → follow-up email sent
  → Sequence ends
```

No templates. No mail merge. Each email is generated fresh based on what the prospect actually wrote.

---

## Tech Stack

- **n8n** — workflow orchestration and scheduling
- **Claude API** (`claude-sonnet-4-6`) — email generation
- **Gmail API** — sending outbound email
- **Google Sheets API** — lead logging
- **Tally Forms** — intake form with webhook trigger
- **Calendly** — booking link embedded in emails

---

## Sample Output

**Form input:**
```
Name:     Sarah Chen
Business: Chen & Associates Bookkeeping
Industry: Accounting
Goal:     Automate my monthly client reporting so I stop spending Sundays on spreadsheets
```

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

---

## Project Structure

```
Solo Agent Project/
├── README.md
├── business-plan.md              ← service business strategy around this automation
├── case-study-onboarding.md      ← written case study (markdown)
├── case-study-onboarding.pdf     ← PDF export
├── directive-client-onboarding-emailer.md  ← build spec / architecture notes
├── build_n8n_workflow.py         ← script to programmatically build the n8n workflow
├── build_make_scenarios.py       ← Make.com alternative build
├── build_followup_workflow.py    ← 48-hour follow-up sequence builder
├── build_calendly_workflow.py    ← Calendly booking detection node
├── patch_n8n_workflow.py         ← workflow update/patch utility
├── add_tally_node.py             ← Tally webhook node setup
├── make-scenario1-build-guide.md ← Make.com build guide
├── google_auth_setup.py          ← Google OAuth setup
└── Example_Projects.docx         ← reference examples
```

---

## Extensions for Financial Services

For accounting and financial services clients, this system extends to:

- Send an engagement letter via PandaDoc for e-signature immediately after the welcome email
- Trigger a client portal invite (Karbon, Canopy, or similar)
- Log the lead directly to a CRM or practice management tool

Saves 45–90 minutes per new client onboarding. At 5 new clients/month, that's 4–7 hours recovered monthly.

---

## Contact

**Sammi Hantous** — AI Automation Consultant  
[hantous93@gmail.com](mailto:hantous93@gmail.com) · [calendly.com/hantous93](https://calendly.com/hantous93)
