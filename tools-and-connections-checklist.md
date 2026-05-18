# Phase 0 — Tools & Connections Checklist

**Goal:** Get to a working Rinata invoice reconciliation agent for **under $100 all-in across 4 weeks**, with a clear path to scale spend in Phase 1 only when revenue justifies it.

Companion to: `business-plan.md` and `phase-0-rinata-implementation.md`

---

## Part A — Tools & Software

### A1. Free / already have

- [ ] **Personal Windows PC** — you have it. Used for development + initial agent hosting.
- [ ] **WSL2 (Windows Subsystem for Linux)** — free, built into Windows 11. Run `wsl --install` in an admin PowerShell. This lets you run Hermes locally without paying for a Linux VPS during Phase 0.
- [ ] **Personal Google account** — used to create the dedicated Rinata-AI Gmail and to access Drive/Sheets. Free.
- [ ] **Git** — free. Install from git-scm.com. Used to sync the Obsidian vault between Windows and (eventually) the VPS.
- [ ] **VS Code** — free. Best for editing the agent code, vault files, and viewing Markdown.

### A2. Free tier — sign up and use the free plan

| Tool | What it's for | Free tier limit | When you outgrow it |
|---|---|---|---|
| [ ] **Hermes Agent** | Agent harness — the brain | Fully open source, no limit | Never (it's open source) |
| [ ] **Composio** | OAuth + connectors to Gmail/Drive/Sheets | 20,000 tool calls/month | When you add customer #1 — upgrade to $29 Standard |
| [ ] **Obsidian** | Per-customer knowledge vault | Unlimited for personal use | Never for Phase 0 |
| [ ] **Loom** | Demo recordings | 25 videos, 5 min each | Phase 1 — upgrade to $15/mo for unlimited |
| [ ] **Google Workspace** (or regular Gmail) | Dedicated `rinata.ai.invoices@gmail.com` inbox | Free with any Google account | Never for Phase 0 |
| [ ] **Google Sheets** | Vendor invoice audit ledger | Free | Never |
| [ ] **Google Drive** | Storing PDFs the agent processes | 15GB free | Never for Phase 0 |
| [ ] **GitHub** (private repo) | Versioning the Obsidian vault + agent code | Free for private repos | Never |

### A3. Paid — minimum necessary spend (Phase 0)

| Tool | Cost | Why it's required | Cheapest path |
|---|---|---|---|
| [ ] **Anthropic API credits** | $30–$75 across 4 weeks | Model calls for invoice extraction and verification | Set a hard $50 prepaid budget. Use Sonnet 4.6 for runtime, Opus 4.7 only when stuck. |
| [ ] **(Optional) Always-on host** | $0 if you use Oracle Cloud Always Free; $4/mo Hetzner CX11; $20/mo Hetzner CCX13 | Only needed if you want the agent processing invoices 24/7 during Phase 0 | **Recommended for Phase 0: skip the VPS entirely.** Run Hermes inside WSL2 on your PC during build. Trigger invoice processing manually from Telegram. Add the VPS only in week 4 or in Phase 1. |

**Realistic Phase 0 total spend: $30–$75** if you skip the VPS and stay on free tiers everywhere else.

### A4. Do NOT buy yet (deferred to Phase 1 or later)

- ❌ **Orgo cloud VMs** — not needed until you have paying customers requiring isolation. Phase 0 runs fine on your local machine.
- ❌ **Composio Standard ($29/mo)** — free tier covers Phase 0 volume.
- ❌ **Obsidian Sync ($10/mo)** — git via GitHub is free and works fine.
- ❌ **AgentMail** — use a normal dedicated Gmail. No customer is asking for a branded agent email yet.
- ❌ **Superhuman ($30/mo)** — defer until your customer email volume justifies it (probably Phase 2).
- ❌ **Linear / Asana / Notion paid tiers** — Trello free tier or a single Markdown file in your project directory is enough.
- ❌ **Granola / Fathom paid tiers** — free tiers work for your meeting volume right now.
- ❌ **A domain name** — until you have a website worth pointing it at. Use the Gmail address directly in Phase 0.
- ❌ **SOC 2 audit** — budgeted in the business plan for end of year 1, not Phase 0.
- ❌ **LLC formation** — only needed before signing the first paid contract. Defer to end of Phase 0 or start of Phase 1.

### A5. Phase 1 add-ons (budget for week 5 onward, not now)

| Tool | Cost | Trigger to buy |
|---|---|---|
| VPS (Hetzner CX22 or Fly.io) | $5–$15/mo | When you need 24/7 uptime for a paying customer |
| Composio Standard | $29/mo | When tool calls exceed 20K/mo (first paid customer) |
| Loom Pro | $15/mo | When you need more than 5-min demos |
| Anthropic API budget | $200–$400/mo | Per paying customer |
| LLC formation | $200–$800 one-time | Before first signed contract |
| MSA/SOW/DPA templates (Bonsai or Lawpath) | $200–$500 one-time | Before first paid customer |
| Stripe or LawPay (for invoicing) | Free + 2.9% transaction fee | First customer invoice |

---

## Part B — Rinata Data Sources & Connections

These are the actual data you need access to from Rinata to build the invoice reconciliation agent. Group by required vs. recommended vs. future.

### B1. Required for Phase 0 (must-have, week 1)

- [ ] **Written consent from Rinata's other two co-owners.** Plain-English statement that they approve (a) the agent accessing vendor invoice data and (b) anonymized usage of results in external sales material. Get this in writing before any other connection.
- [ ] **Scoped access to Rinata's existing email inbox** (`info@rinatarestaurant.com`). Don't create a new email address — vendors are already sending to `info@`. Instead, use a **Gmail filter + label** approach:
  - [ ] Verify what hosts the mailbox: Google Workspace (Composio works directly), Microsoft 365 (use Outlook connector), or forwarded-only via a web host (find where it forwards to first).
  - [ ] Confirm admin access to set up filters and labels on the mailbox.
  - [ ] Scroll the last 60 days of mail and capture the vendor sender domains + recurring invoice subject patterns.
  - [ ] Create a Gmail filter: `from:(vendor domains) OR subject:(invoice OR statement OR remittance) OR has:attachment` → apply label `Invoices/Auto`.
  - [ ] Configure the agent's skills to only ever query `label:Invoices/Auto`. The OAuth scope still technically grants full mailbox access — the label is an in-agent convention, not a Google-enforced boundary. Fine for your own restaurant; revisit for paying customers in Phase 1.
- [ ] **List of approved/active vendors.** Just a list. Name, contact email, what they supply, typical order cadence. Top 5–10 by volume is enough to start.
- [ ] **60–90 days of historical vendor invoices.** Used to build the price-history baseline. Acceptable formats:
  - Forward existing emails containing PDF invoices to the dedicated Gmail
  - OR dump PDFs into a shared Google Drive folder the agent can access
  - OR export from accounting system as PDFs
- [ ] **Approval workflow contact.** Who at Rinata receives the agent's weekly exception report? Who clicks "approve" or "dispute"? Define this in writing — likely you, possibly the GM or another owner.

### B2. Recommended for Phase 0 (improves accuracy materially)

- [ ] **Current vendor pricing sheets or contracts** (where they exist). Some suppliers send quarterly price lists. Drop them in Drive. The agent uses them as the ground-truth comparison.
- [ ] **SKU/product list with typical pack sizes.** Even informally — "Sysco delivers olive oil in 6×3L cases" beats letting the agent guess unit conversions.
- [ ] **Typical weekly order volume per vendor.** Used for quantity sanity-checks. Can be hand-entered into Obsidian; agent will refine over time.
- [ ] **Read-only access to Rinata's accounts payable inbox.** Either a shared inbox label in Gmail, delegated mailbox access, or a forwarding rule. This is the most reliable invoice source.
- [ ] **Rinata's vendor disputes / credit memo history.** Helps the agent distinguish legitimate vendor errors from one-off accounting noise.

### B3. Required for Phase 0.5 extension tracks (added 2026-05-13)

These are needed only for the two extension tracks (walk-in receipt capture + QBO auto-coding), which run Days 11–14 and Days 22–28 respectively. If the extensions are deferred to Phase 1, defer these too.

#### For walk-in receipt capture (Days 11–14)
- [ ] **Agreement on the receipt-capture channel.** Pick ONE:
  - Email photos to `info@rinatarestaurant.com` with subject prefix `Receipt:` (simplest — uses existing pipeline)
  - Send to Hermes Telegram bot (lower-friction for staff if they already use Telegram; agent is already on Telegram from Day 2)
- [ ] **A second Gmail filter rule** on `info@rinatarestaurant.com`: `subject:Receipt` → label `Receipts/Auto`.
- [ ] **A list of which staff/owners do the wholesale runs.** Each needs the capture channel set up on their phone and a 5-minute training: take the photo, send it, done.
- [ ] **Costco Business / Restaurant Depot / Sam's account numbers and member IDs.** Helpful for the agent to verify which member made which purchase. Drop these into `vault/vendors/wholesale-club-accounts.md`.

#### For QuickBooks Online auto-coding (Days 22–28)
- [ ] **Confirm Rinata uses QuickBooks Online** (not Desktop — QBO is required for the Composio connector to work).
- [ ] **Admin or accountant access to QBO.** You (or whoever owns the books) needs to be able to authorize OAuth for an external app to read the Chart of Accounts and write bills.
- [ ] **Composio QuickBooks Online connector** — already included in your Composio free tier; just needs OAuth authentication on Day 22.
- [ ] **Export of Rinata's Chart of Accounts.** Agent reads this once on Day 22; cached. Anyone with QBO access can export this in 30 seconds.
- [ ] **Export of last 90 days of categorized transactions from QBO.** Used by the agent as training examples to learn Rinata's categorization patterns. CSV export from QBO is sufficient.
- [ ] **Designated approver for QBO posts.** Phase 0/0.5 has strict human-in-the-loop — every QBO post requires explicit approval. Who is this person? When are they available to review (daily / weekly)?
- [ ] **(Optional) QBO Classes or Locations.** If Rinata uses classes/locations to track different revenue centers (bar vs. kitchen, lunch vs. dinner, etc.), tell the agent about it so it can suggest those too.

### B4. Optional for Phase 0, valuable for Phase 1+ (defer if friction is high)

- [ ] **POS sales data export.** Most likely Toast — Toast has a developer API. If Rinata uses Square, Clover, or Lightspeed, those also have APIs. **For Phase 0:** skip the integration; use a weekly CSV export emailed to the agent. The agent doesn't *need* sales data to verify invoices but having it enables higher-order checks (food cost % drift, theoretical-vs-actual).
- [ ] **Inventory system data.** If Rinata uses MarginEdge, xtraCHEF, BlueCart, or Toast's built-in inventory, this enables receiving-vs-invoice quantity verification. Defer to Phase 1 — pricing reconciliation is higher-value at this stage.
- [ ] **Bank statement access (read-only).** For matching invoice payments to bank disbursements. Useful for closing the loop but not needed in Phase 0. Plaid integration is the path when you want it.

### B5. Do NOT need in Phase 0

- ❌ POS real-time event streams
- ❌ Recipe/menu costing software
- ❌ Reservation system (OpenTable/Resy) — irrelevant to invoice work
- ❌ Reviews (Google/Yelp) — irrelevant to invoice work
- ❌ Payroll system — irrelevant to invoice work
- ❌ Customer CRM / loyalty data — irrelevant

---

## Part C — Connection Setup Order (Sequenced)

Do these in order. Each unlocks the next.

1. [ ] Get the co-owner consent conversation done. Document in writing.
2. [ ] Verify what hosts `info@rinatarestaurant.com` (Workspace, M365, or forwarded). Confirm admin access.
3. [ ] Scroll the last 60 days of `info@` mail; capture vendor sender domains and invoice subject patterns.
4. [ ] Set up the Gmail filter on `info@` → label `Invoices/Auto`. Verify it tags new invoices correctly without catching reservations or customer mail.
5. [ ] Install WSL2 on your Windows PC; install Hermes inside WSL2.
6. [ ] Get an Anthropic API key with a $50 prepaid hard cap.
7. [ ] Sign up for Composio free tier; connect `info@rinatarestaurant.com` (Gmail/Outlook), Drive, and Sheets.
8. [ ] Create the Obsidian vault on your PC; init as a git repo; push to a private GitHub repo.
9. [ ] Populate the vendor list and SKU notes in the Obsidian vault from what you know about Rinata's supply chain.
10. [ ] Set up a shared Google Drive folder; drop 60–90 days of historical invoices into it (export from `Invoices/Auto` if they're already in the inbox).
11. [ ] Build and test the `process_invoice` skill on 3 historical invoices. Hard-code the skill to only ever read `label:Invoices/Auto`.
12. [ ] Run live for one full week. Tune filter rules and extraction prompts.
13. [ ] Record Loom demos and produce case study.

---

## Part D — Total Cost Summary

| Phase | Recurring monthly | One-time | Notes |
|---|---|---|---|
| Phase 0 (weeks 1–4) | $0 if you stay disciplined on API spend | $0 | Pure API consumption: $30–$75 across the full 4 weeks |
| Phase 1 (months 2–6) | $50 – $150/mo | $400 – $1,300 (legal templates + LLC) | VPS + Composio + Loom + heavier API usage + per-customer costs |
| Phase 2 (months 6–12) | $300 – $800/mo | — | Scales with paying customer count |
| Phase 3 (months 12–24) | $1,500 – $3,000/mo | $10,000 – $15,000 (SOC 2) | Productization + first hire |

**Phase 0 worst-case total cost: $75.** That is the answer to "how little can I spend to validate this." Anything above that is optional optimization, not capability.

---

## Part E — What to Do If a Free Tier Runs Out

| Free tier | Symptom of exhaustion | Cheapest upgrade path |
|---|---|---|
| Composio (20K calls/mo) | Tool calls start failing with quota error | $29/mo Standard tier (200K calls) — likely month 2 |
| Anthropic free credits (if you signed up with them) | API returns 429 | Pay-as-you-go at standard rates; budget $50–$100/mo |
| Loom (25 videos, 5 min each) | Recording cuts off at 5 min | $15/mo Loom Pro, or just record outside Loom (OBS Studio is free) |
| Oracle Cloud Always Free | Instance terminated for non-use | Hetzner CX11 at $4/mo, or Fly.io free-allowance machine |
| Google Drive (15GB) | Upload fails | Google One 100GB at $2/mo |

---

## Bottom Line

You can stand up the Phase 0 Rinata agent on free tiers plus **~$50 of Claude API consumption** across four weeks. Everything else in the previous cost estimate was optimization for paying customers, not for validation. Spend that $50, hit the success criteria, and let Phase 1 paying revenue fund every subsequent upgrade.
