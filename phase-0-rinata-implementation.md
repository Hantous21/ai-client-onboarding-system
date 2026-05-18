# Phase 0 — Rinata Implementation Starter Plan
## Vendor Invoice Reconciliation Agent

**Duration:** 28 days (4 weeks) + optional Phase 0.5 extension tracks
**Audience:** Founder (implementation guide)
**Companion document:** `business-plan.md`
**Date:** 2026-05-13

**Scope discipline rule:** No further scope changes to Phase 0 after the docs below are finalized. New feature ideas go into `phase-1-backlog.md` for evaluation after Day 28. Two extensions have already been negotiated in (see Section 8): walk-in receipt capture, and QuickBooks auto-coding. Both are gated on the core Days 1–21 schedule staying on track.

---

## 1. Why This Use Case (Recommendation Rationale)

Of the realistic Rinata workflows that an AI agent can handle today, **vendor invoice reconciliation** is the single strongest choice. Here is the reasoning, made explicit so it can be challenged.

### What it is
Restaurants receive invoices weekly from food, beverage, paper, and equipment suppliers. Someone at Rinata currently has to: open each invoice, read line items, compare to what was ordered, compare to what was delivered, compare to prior pricing, look for duplicate billing, approve or dispute, and file. This is hours per week, every week, forever.

### Why this beats the other restaurant use cases I considered

| Candidate use case | Why I did not pick it |
|---|---|
| Daily/weekly P&L drafting | Requires deep POS integration; high data variance; weak demo narrative for surety/FC buyers |
| Supplier email triage and reply drafting | Useful but low-value visually; the agent looks like a glorified inbox tool |
| Google/Yelp review monitoring and replies | Easy and pretty, but the workflow shape is unrelated to construction-finance pitching |
| Staff scheduling | High variance, high context dependency, weak demo |
| Reservation/waitlist optimization | Heavy POS-vendor dependency; restaurant-specific narrative does not translate |
| Marketing content generation | Low value, generic, does not differentiate |

### Why vendor invoice reconciliation is uniquely strong

1. **Identical workflow shape to the target sales pitch.** The construction industry calls this same activity "pay application review" — invoices arrive, get matched against a schedule of values, exceptions get flagged, the result gets approved or kicked back. When you walk a surety underwriter or funds-control ops director through your Rinata workflow, you are showing them their workflow, with different nouns. This is the cleanest possible analogue.

2. **Document-extraction heavy.** PDF parsing, line-item structuring, cross-document comparison — these are the exact capabilities you will need to demonstrate on lien waivers and AIA G702/G703 forms in Phase 1.

3. **Real, measurable financial value.** Vendor overcharges, duplicate billings, and undetected price increases are common in restaurant operations. Surfacing two or three of these in a four-week build window makes the case study self-funding.

4. **Low-stakes failure mode.** If the agent gets a line item wrong, you catch it before approving. Nobody loses money on a bad disbursement. This is the right place to learn before you touch a customer's funds-control workflow.

5. **Demoable in 90 seconds.** "Watch the agent open this PDF, extract eighteen line items, compare them to the last four invoices from this supplier, flag two price increases over five percent, and email me an approval-ready summary." That is a recordable, narrate-able event.

6. **You learn the integration layer.** Composio + Gmail + Google Drive + Google Sheets is exactly the same plumbing you will reuse on customer one.

### Sales narrative bridge
Once Phase 0 completes, the cold email to a surety / FC prospect reads approximately like this:

> "I run an Italian restaurant in Minneapolis and built an AI agent to handle our weekly vendor invoice reconciliation — it processes invoices, matches line items against expected pricing, and flags exceptions for review. We caught $X in supplier errors in the first month. The exact same workflow shape applies to funds-control draw processing — invoices in, schedule of values cross-check, lien waiver verification, exception report out. Worth a 20-minute conversation to see the demo?"

That message gets warmer responses than any "we do AI for surety firms" message will.

---

## 2. Success Criteria (Define Done Before Starting)

Phase 0 is complete when **all** of the following are true:

1. **Functional accuracy.** Agent has processed at least 10 real Rinata invoices end-to-end with at least 90% line-item extraction accuracy verified against a hand-checked sample.
2. **Real exceptions surfaced.** Agent has identified at least 2 genuine exceptions (price increase, duplicate, quantity mismatch) that the restaurant can act on.
3. **Speed improvement.** Per-invoice processing time under 2 minutes end-to-end, versus current manual baseline of 10–15 minutes.
4. **Demo asset.** One 4–6 minute Loom video walking through a live invoice reconciliation, suitable for cold outreach.
5. **Written case study.** One-page document, clean format, includes problem statement, solution architecture diagram, before/after metric, anonymized screenshot.
6. **Sales translation document.** One-page companion document translating the Rinata workflow into surety / FC language, with construction-specific examples mapped from the restaurant examples.
7. **Co-owner sign-off.** Documented written approval from Rinata co-owners to use the work as a public case study.

Anything not on this list is out of scope for Phase 0.

---

## 3. Stack Decisions (Concrete Picks, Not Options)

| Layer | Decision | Cost | Why |
|---|---|---|---|
| Agent harness | Hermes Agent (Nous Research) | Free (open source) | Multi-channel gateway, portable, no vendor lock-in |
| Compute | Hetzner CCX13 cloud VPS (Ubuntu 22.04, Frankfurt or Ashburn region) | $20/month | Cheapest credible host; if Hetzner unavailable, Fly.io Machine 1x-cpu at $15–25/month |
| Integrations | Composio Standard tier | $29/month | Gmail, Drive, Sheets connectors with managed OAuth |
| Document extraction | Claude vision (built into model calls) | API usage | No separate OCR vendor needed for v1 |
| Memory and knowledge | Obsidian vault, git-synced from local Windows to VPS | Free + $10/month Obsidian Sync (optional) | Portable, model-agnostic, becomes the per-customer template later |
| Primary model | Claude Sonnet 4.6 | API usage | Best cost/capability for production agent work |
| Build-phase model | Claude Opus 4.7 | Higher API cost | Used only during agent construction, not runtime |
| Email channel | Dedicated Gmail account (e.g. rinata.ai@gmail.com) | Free | No need for AgentMail at this stage |
| Demo recording | Loom Starter | $15/month (or free tier) | Industry standard |
| Spreadsheet ledger | Google Sheets | Free | Composio connector + human-readable audit trail |
| Observability | Hermes built-in logs + cron-based daily summary email to founder | Free | Sufficient for Phase 0 scale |

**Total Phase 0 monthly run cost:** approximately $85–$110.
**Total Phase 0 one-time setup cost:** approximately $50 (domain optional, software trials).
**Total Phase 0 API consumption budget:** allocate $200 across build and run.

**Grand total Phase 0 budget:** approximately $400–$500 across the full 4 weeks.

---

## 4. Day-by-Day Plan

### Week 1 — Foundation and Ingestion

**Day 1 — VPS, Hermes, and accounts**
- Provision Hetzner CCX13, Ubuntu 22.04, SSH key configured.
- Install Hermes Agent following [official docs](https://hermes-agent.nousresearch.com/docs/).
- Create dedicated Gmail account (suggestion: `rinata.ai@gmail.com`) and connect it to Composio.
- Create Composio account, configure Standard plan, connect Gmail and Google Drive.
- Create Google Sheet titled "Rinata Vendor Ledger 2026" with columns: invoice_date, vendor, invoice_number, line_item, quantity, unit_price, line_total, prior_price, price_change_pct, status, notes.

**Day 2 — Telegram channel and first run**
- Set up Hermes Telegram gateway following docs.
- Send first test message: "Hello, list your available tools." Confirm agent responds with Composio tool list.
- Test the Gmail integration with a manual prompt: "Read the most recent unread email and summarize."

**Day 3–4 — Build the Rinata Knowledge Base in Obsidian**
- Create local Obsidian vault: `C:\Users\shant\Documents\rinata-vault\`.
- Folder structure:
  - `00-meta/` — vault README, agent operating instructions
  - `vendors/` — one file per supplier (Sysco, US Foods, local farms, beer/wine distributors, etc.)
  - `skus/` — SKU catalog with current contract pricing where known
  - `invoices/processed/` — agent writes one Markdown record per processed invoice
  - `invoices/exceptions/` — agent writes exception reports here
  - `runbook/` — agent's own operating procedures
- Populate the top 5 vendor files by volume with: business name, contact email, typical delivery schedule, top SKUs ordered, expected price range, historical patterns.
- Set up git remote and clone to the VPS at `/opt/hermes/vaults/rinata/`.

**Day 5–7 — Build the invoice ingestion skill**
- Write a Hermes skill named `process_invoice` with the following behavior:
  - Triggered by an email landing in the dedicated Gmail with PDF attachment, or by manual command.
  - Downloads the PDF.
  - Uses Claude vision to extract: vendor name, invoice number, invoice date, line items (description, quantity, unit price, line total), invoice total.
  - Writes a structured Markdown record to `invoices/processed/YYYY-MM-DD-vendor-invnum.md`.
  - Appends rows to the Google Sheet ledger.
  - Confirms in Telegram: "Processed invoice [number] from [vendor], [N] line items, total $[X]."
- Test against 3 real Rinata invoices manually emailed to the agent.
- Hand-check accuracy. Tune the extraction prompt until extraction hits 95%+ accuracy on the test set.

**End of Week 1 checkpoint:** Agent can ingest an invoice and produce a clean structured record. No verification logic yet.

### Week 2 — Verification Logic

**Day 8–10 — Price-change detection**
- Extend `process_invoice` to: for each line item, look up prior invoices from the same vendor for the same SKU, calculate price-change percentage, flag any line over 5% change.
- Write findings to the invoice's Markdown record under an "Exceptions" heading.
- Test against the 3 already-processed invoices plus 2 new ones.

**Day 11–12 — Quantity and pattern checks**
- Add sanity-check logic: compare line-item quantities against the vendor's typical order pattern (mean ± standard deviation from prior 8 weeks). Flag outliers.
- For now, "typical pattern" is hand-coded into vendor files in Obsidian. Future: agent updates it autonomously.

**Day 13–14 — Duplicate detection and exception report drafting**
- Add duplicate detection: scan prior 30 days of invoices from the same vendor for matching invoice numbers or near-duplicate totals + dates.
- When at least one exception is flagged on an invoice, agent drafts an exception summary email addressed to the Rinata owners with: invoice metadata, flagged items, recommended action, link to the full record in the vault.

**End of Week 2 checkpoint:** Agent processes invoices and surfaces real exceptions in plain English.

### Week 3 — Reporting and Human-in-the-Loop

**Day 15–17 — Weekly digest**
- Build a cron-triggered skill that runs every Monday at 8am Central, summarizing the prior week's invoices: total processed, total dollars, exceptions flagged, exceptions still open.
- Digest is emailed to the founder and Rinata co-owners (with their consent).

**Day 18–19 — Approval flow**
- When an exception is flagged, agent waits for owner reply. Replies parse as either "approve" (closes the exception), "dispute" (agent drafts a vendor dispute email for human send), or free-text comment (logged as note).
- All decisions written back to the invoice Markdown record for audit trail.

**Day 20–21 — Stress test**
- Run agent on 2 full weeks of real Rinata invoice traffic.
- Track: extraction accuracy, exceptions surfaced, false positives, owner satisfaction.
- Tune prompts and verification thresholds based on observed performance.

**End of Week 3 checkpoint:** Agent is in production-style operation for Rinata's real invoice flow.

### Week 4 — Case Study Production

**Day 22–24 — Loom demos**
- Record Demo 1: "How the agent processes a vendor invoice end-to-end." 4–6 minutes. Live screen share. Real invoice (numbers redacted on camera if needed).
- Record Demo 2: "The week the agent caught a $400 supplier overcharge." Narrative case-study format. 3–5 minutes.

**Day 25–26 — Written case study and sales translation**
- Write `case-study-rinata.md`: one page, problem-solution-outcome format. Include before/after metric, screenshot of the dashboard, single quote from a Rinata co-owner.
- Write `sales-translation-surety.md`: same workflow, translated into surety / funds-control vocabulary. Side-by-side table mapping restaurant nouns to construction nouns:

| Rinata workflow | Surety / FC analogue |
|---|---|
| Vendor invoice | Subcontractor invoice / pay application |
| SKU price history | Schedule-of-values line item |
| Duplicate invoice detection | Lien waiver tier matching |
| Vendor delivery pattern | Project disbursement schedule |
| Exception report to owner | Disbursement memo to underwriter |

**Day 27 — Co-owner sign-off**
- Walk through the case study with Rinata's other two owners.
- Obtain written approval to use the case study in external sales contexts.
- Adjust language or redactions as requested.

**Day 28 — Phase 1 launch readiness check**
- Confirm all Section 2 success criteria met.
- If yes: schedule the first three discovery calls with warm-intro prospects for week 5.
- If no: identify the failing criterion, extend Phase 0 by up to 2 weeks, do not advance to Phase 1 prematurely.

---

## 5. Risks Specific to Phase 0

| Risk | Mitigation |
|---|---|
| Rinata co-owners not aligned with public case study use | Have the conversation in week 1, not week 4. Get written consent before building. |
| Vendor invoice formats too inconsistent for clean extraction | Start with the top 3 vendors by volume; expand only after those work. Accept lower accuracy on edge formats in v1. |
| Hermes Agent breaking change during the build | Pin a specific Hermes version; do not auto-update during Phase 0. |
| Composio connector limitations or downtime | Have a fallback plan: direct Gmail API access via `googleapis` SDK is approximately one day of work if needed. |
| Founder learning curve on Hermes longer than planned | Build the simplest possible version first; advanced features (self-evolution, sub-agents) deferred to Phase 1. |
| Sensitive supplier pricing in public demo | All Loom demos use redacted numbers; case study uses representative ranges, not actual figures. |
| Phase 0 succeeds technically but Phase 1 outreach produces no calls | The Phase 0 demo is necessary but not sufficient; warm-intro list quality matters more. Begin warm-intro outreach planning in parallel during week 3. |

---

## 6. What Comes Next

When Phase 0 completes successfully, the Phase 1 launch checklist activates:

1. The warm-intro contact list of 15 surety / FC / contractor finance prospects is finalized.
2. The cold outbound list of approximately 300 firms is built.
3. The Phase 0 demo and case study are added to a simple one-page website at the working company name domain.
4. The Phase 1 pilot offer document is drafted: $1,500–$2,500 per month, 60-day pilot, paid conversion option, signed permission to use as case study.
5. The first three discovery calls are booked for weeks 5–6.

Phase 1 detail is in the main business plan, section 7.

---

## 7. Definition of Phase 0 Failure

Phase 0 has failed (not delayed) if any of the following are true at the end of week 6:

- The agent cannot reliably extract line items at acceptable accuracy across at least 3 vendors.
- Rinata co-owners decline to permit external case study use.
- The founder concludes the workflow is materially harder than estimated and Phase 1 customer work would amplify those problems.

If Phase 0 fails:
- The technical work is not wasted — Rinata still benefits from the working agent.
- Revisit the recommended-path decision in the source memo. Consider whether the contractor-back-office segment (Tier 2) might be a better entry point.
- Do not advance to selling customers on capability that has not been proven in the controlled environment.

---

## 8. Extension Tracks (Phase 0.5)

These two tracks were added after initial scoping, in response to additional Rinata co-owner input. Both deliver real operational value to Rinata and create a stronger Phase 1 sales story. Both are **strictly gated** on the core Days 1–21 schedule staying on track. If the core slips, these defer to Phase 1 Week 1 — Rinata still gets them within ~5 weeks, but never at the cost of the demo and case study production.

### 8.1 Track A — Walk-In Receipt Capture (Days 11–14, parallel to verification work)

**Problem:** A meaningful fraction of Rinata's purchasing happens at Costco Business, Restaurant Depot, Sam's Club, and similar cash-and-carry wholesalers. These produce paper receipts, not emailed PDFs, and are currently outside the reconciliation flow.

**Capture channel:**
Whoever buys at the wholesaler takes a phone photo of the receipt before leaving the parking lot and emails it to `info@rinatarestaurant.com` with subject prefix `Receipt:` — OR sends it as a photo to the Hermes Telegram bot (set up Day 2). The Gmail filter routes anything matching `subject:Receipt` to a new label `Receipts/Auto`.

**Skill: `process_receipt`**
- Pulls photos from `Receipts/Auto` label (and from Telegram if configured).
- Runs Claude vision on the image. Handles multi-photo stitching for long Costco receipts.
- Extracts: vendor, date, time, cashier/member ID, line items (description, quantity, unit price, line total), subtotal, tax, total, payment method.
- Handles negative lines (returns/refunds) and "instant rebates" / member pricing.
- Writes structured Markdown to `vault/receipts/processed/`.
- Appends rows to the same Google Sheets ledger with new `source: receipt` column.

**SKU normalization layer (the actually-hard part):**
Costco labels olive oil as `KS OLIVE OIL EV 3L`. Sysco calls the same product `OLIVE OIL XV 3L CASE`. The agent maintains a canonical SKU map at `vault/skus/canonical.md`:

```markdown
## olive_oil_extra_virgin_3L
- costco: "KS OLIVE OIL EV 3L"
- sysco: "OLIVE OIL XV 3L CASE"
- rdepot: "OLIVE OIL 100% PURE 3L"
```

First time the agent sees an unmapped SKU, it sends a Telegram message asking which canonical SKU this is (or proposing a new one). User confirms once; agent caches forever.

**Payoff:**
1. Cross-vendor price comparison ("Costco's olive oil is 18% cheaper than Sysco this week").
2. Stronger surety/FC sales story — same logic applies to a contractor's mixed Home Depot / Lowe's / lumber yard receipts.

**Receipt-specific edge cases (build for these in week 2):**
- Long receipts requiring 2–3 photos stitched by overlap.
- Negative lines (returns/refunds) on same receipt — track or you'll over-count spend.
- Tax handling — line prices are pre-tax; total tax is at bottom. Match invoice convention.
- Member pricing vs. instant rebates vs. statement credits — flag deferred adjustments as "pending."
- Faded or crumpled receipts — agent requests re-photo via Telegram rather than guessing.

**Day-by-day:**
- **Day 11:** Build `process_receipt` skill core extraction. Test on 3 receipts (1 Costco, 1 Restaurant Depot, 1 other).
- **Day 12:** Multi-photo stitching, returns/refund handling, tax handling.
- **Day 13:** SKU normalization layer; backfill canonical map for top 20 SKUs by hand-confirming aliases.
- **Day 14:** Integration test — run full pipeline (capture → extract → normalize → ledger → exception detection) end-to-end on a real week of receipts.

**Gating to advance:** at least 5 receipts processed end-to-end with line-item accuracy ≥90% and SKU normalization correctly matching at least 10 canonical SKUs.

### 8.2 Track B — QuickBooks Auto-Coding (Days 22–28, parallel to case study production)

**Problem:** Currently every receipt and invoice line item gets manually categorized and entered into QuickBooks. This is 4–8 hours/week of low-leverage work for whoever owns Rinata's books.

**Required new connection:** Composio QuickBooks Online connector (free tier on Composio includes it; see updated `tools-and-connections-checklist.md`).

**Skill: `draft_qbo_entries`**
- Triggered on a configurable cadence (default: end of each business day at 9 PM Central, weekly batch is fine too).
- Reads new invoice + receipt records from the vault.
- For each line item, classifies into the most likely QBO category using:
  - The categorization-patterns file (built up over time from corrections — see learning layer below).
  - Rinata's Chart of Accounts (read once on Day 22; cached).
  - 90 days of historical categorized transactions (read once on Day 22; used as training examples in the prompt).
- Splits multi-category receipts (Costco purchase with food + paper + cleaning supplies) into multiple QBO bill line items.
- Drafts the QBO entries (does NOT post yet).
- Sends a single summary message via email or Telegram: "I'm ready to post 12 transactions totaling $X — review and approve."

**Approval flow (Phase 0/0.5 — strict human-in-the-loop):**
- Owner replies "approve" → agent posts all draft entries to QBO via Composio.
- Owner replies "approve except 3, 7, 9" → agent posts subset, asks for corrections on the rest.
- Owner edits a category in the reply → agent updates `vault/qbo/categorization-patterns.md` and re-asks for approval.
- Posting never happens without explicit "approve" — no auto-post in Phase 0.

**Learning layer: `vault/qbo/categorization-patterns.md`**

Markdown file the agent reads on every run and updates whenever the owner corrects a categorization. Structure:

```markdown
## Food Cost — Produce
- Sysco: any line matching /TOMATO|PEPPER|ONION|LETTUCE/
- Costco: any line matching /KS PRODUCE/ or member-club produce SKUs
- Restaurant Depot: aisles 12-14 (per RD layout) — confirm in description text

## Food Cost — Protein
- Sysco: any line matching /BEEF|CHICKEN|PORK|FISH|SHELLFISH/ unless prepared
- Local farms: any invoice from farm vendor list

## Paper & Disposables
- Costco: napkins, cups, takeout containers, foil, film
- Restaurant Depot: any "DISPOSABLE" or "TO-GO" lines

[and so on for each Rinata GL account]
```

Every time the owner overrides the agent's suggested category, the agent appends a new pattern rule to this file. After 30–60 days, the agent should be hitting 95%+ correct categorization on first pass.

**Day-by-day:**
- **Day 22:** Connect Composio QBO. Pull Rinata's Chart of Accounts. Export 90 days of categorized transactions. Build the initial `categorization-patterns.md` by analyzing those historicals.
- **Day 23:** Build `draft_qbo_entries` skill core — classification + entry drafting. Test on 10 historical invoices/receipts (dry run, no posting).
- **Day 24:** Build the approval flow (email or Telegram reply parsing). Test approval, partial approval, edit cycles.
- **Day 25:** Multi-category split logic for mixed receipts. Multi-day testing.
- **Day 26:** First real-money approval cycle — agent drafts a week of real entries; owner approves; entries actually post to QBO.
- **Day 27:** Tune categorization patterns based on owner corrections.
- **Day 28:** Acceptance test: process and post one full business week of entries with ≤10% correction rate.

**Gating to advance:** Days 1–21 of the core plan must be on track. If not, defer this whole track to Phase 1 Week 1 (which delivers it to Rinata about 2–3 weeks later than this plan, but doesn't risk the core deliverables).

**Why this is real money for the sales pitch:**

The construction contractor analogue is direct and material. Contractors using QBO need every receipt and subcontractor invoice coded to a *job* + *cost category* for accurate job costing — and job costing is what determines whether a contractor knows their real profit per project. The same skill that codes Rinata's olive oil to "Food Cost — Produce" codes a 2×4 stud purchase to "Job 234 — Materials — Framing." This is precisely the workflow surety underwriters wish their bonded contractors did better, because clean job costing means cleaner financials means cleaner underwriting.

**Why this is real money for Rinata:**

If categorization currently takes 4–8 hours/week at an imputed $25–$50/hour, this skill saves Rinata $400–$1,600/month in direct labor while improving categorization consistency. That's the kind of "we use it ourselves" testimonial that closes Phase 1 customers.

### 8.3 Backlog discipline

Any feature idea that surfaces during Phase 0 from co-owners, your own thinking, or customer conversations goes here, not into the Phase 0 schedule:

**File to create on Day 1:** `phase-1-backlog.md` in the vault. Single-line bullets, dated. Reviewed at the Day 28 completion gate, not before.
