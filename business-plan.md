# Business Plan
## A Vertical AI Agent Practice for the Surety, Funds-Control, and Construction-Finance Industries

**Working company name:** TBD *(candidates: Bondline, Draftline, Lienpath, Cornerstone Agents — see Appendix A)*
**Prepared by:** [Founder Name]
**Date:** 2026-05-13
**Document type:** Internal operating plan (not for external distribution)
**Companion document:** `phase-0-rinata-implementation.md`

---

## 1. Executive Summary

This document outlines a phased plan to build a vertically-focused AI agent practice serving the contract surety, funds-control, and construction-finance markets. The business begins as a high-touch services practice and graduates to a productized SaaS over a 24-month horizon.

**Why now.** Agent harnesses (Hermes, Claude/OpenAI), integration layers (Composio), and cloud document-extraction capability have matured to the point where a single operator can deliver outcomes that previously required a fractional finance team. The incumbents in surety and funds control (Tinubu, Surety2000, NetSol, Ebix) are systems of record, not agentic platforms. An 18-month window exists before larger players enter this niche.

**Why us.** The founder brings (a) deep insider knowledge of contract surety bonds and funds-control / escrow account management, (b) a finance degree and familiarity with construction billing operations, and (c) one-third ownership of Rinata Restaurant in Minneapolis — providing a free, controllable operational environment in which to build and demonstrate the agent technology before introducing risk to paying customers.

**Strategy in one line.** Use Rinata as a credibility-building proof-of-concept, lead with surety and funds-control firms as the first paid wedge, expand to small-contractor back-office services as a parallel revenue stream, and graduate to a construction-finance SaaS product in year two — all funded from services revenue, with no outside capital required.

**Honest year-one target.** $250,000–$500,000 in annual recurring revenue from 3–8 paying customers. Year-two target: $800K–$1.2M ARR combined services + early SaaS revenue.

---

## 2. Mission and Positioning

**Mission.** Apply modern AI agent technology to the back-office workflows of small and mid-size firms operating in the surety, funds-control, and construction-finance value chain — delivering the throughput of additional headcount at a fraction of the cost while preserving the human judgment these workflows require.

**Positioning statement.** We are not an AI consultancy. We are not a horizontal agent agency. We are a vertical operations practice that builds and runs purpose-built AI workers for a single industry we know better than any generalist competitor.

**Brand promise.** Our customers do not touch tokens, models, infrastructure, or vendor integrations. They receive measurable output — reconciled invoices, drafted disbursement memos, flagged exceptions, completed renewal packets — within a defined service-level agreement.

---

## 3. Market Analysis

### 3.1 Primary market: Contract surety and funds control

- **U.S. surety bond market:** approximately $8–9 billion in annual premium volume.
- **Carriers:** 250–300 active surety carriers (Travelers, Liberty Mutual, Zurich, CNA, Hartford, plus specialty players).
- **Distribution:** several thousand independent surety bond agencies; NASBP (National Association of Surety Bond Producers) lists approximately 5,000 member professionals across roughly 500 firms.
- **Funds control / construction escrow:** smaller and more fragmented — a mix of bank trust departments, specialty firms (North American Construction Services, FundsControl Plus, regional firms), and surety-affiliated funds-control arms. Single mid-size general contractor portfolios commonly produce $20M–$200M in annual disbursements requiring controlled release.

**Customer pain.** Surety underwriting and funds-control workflows are document-heavy, multi-party, deadline-sensitive, and dependent on judgment that is currently performed by experienced staff. The dominant operating system is still email plus PDF. Existing software platforms maintain records but do not perform the underlying work.

**Technology penetration.** Low. Most agencies and FC firms have not adopted AI in any meaningful operational capacity. The few attempts to date are general-purpose tools (ChatGPT in a browser tab) rather than integrated workflow agents.

### 3.2 Secondary market: Small general contractors and specialty subcontractors

- **Total addressable contractor base:** approximately 700,000 construction firms in the United States; roughly 250,000 with five or more employees.
- **Target subsegment:** general contractors and specialty subcontractors with $2M–$20M in annual revenue and 10–80 employees.
- **Customer pain:** monthly pay application generation (AIA G702/G703), lien waiver tracking across subcontractor tiers, retainage management, change-order documentation, draw schedule preparation, vendor invoice reconciliation.
- **Why this segment after surety:** the workflows are upstream and downstream of funds control. Lien waivers our FC customers verify originate at contractors. Cross-sell potential is structural, not coincidental.

### 3.3 Competitive landscape

| Category | Examples | Threat level |
|---|---|---|
| AI-native vertical entrants in surety/FC | Effectively none today | The window |
| Adjacent construction AI plays | Document Crunch, Trunk Tools, Briq | Low — different workflow focus |
| Incumbent surety platforms | Tinubu, Surety2000, NetSol, Ebix | Low — systems of record, slow to add agentic features |
| Horizontal AI agencies | The Nick Orgo playbook in the source video | Low for our verticals — lack domain depth |
| Large potential entrants | Procore (acquisition), Acrisure (internal tech arm), AON | Medium — 18–24 month watch |

### 3.4 TAM / SAM / SOM (conservative bottom-up)

- **TAM:** $200M+ addressable spend on AI-driven back-office automation across surety, FC, and contractor segments by 2028.
- **SAM (firms we could realistically reach as a single operator):** approximately 400 surety agencies and 50–80 FC firms within the United States that match our ICP.
- **SOM (year 1–2 capture target):** 8–15 paying customers, representing $0.5M–$1.5M in ARR. This is approximately 3% market penetration of the immediately addressable subset.

---

## 4. Products and Services

The business operates three nested product tiers, introduced sequentially.

### 4.1 Tier 1 — Surety and Funds-Control Agent Services *(launches Phase 1)*

White-glove monthly retainer. The customer receives one or more agents trained on their workflows, integrated with their email and document systems, with continuous monitoring and improvements.

**Workflows supported:**

| Surety | Funds-Control |
|---|---|
| Bond request intake and triage | Draw request intake (PDF/email) |
| Underwriting prep and document gathering | Invoice → schedule-of-values matching |
| Bond form selection and drafting | Lien waiver verification |
| Obligee delivery and tracking | Budget reconciliation and retainage tracking |
| Renewal tracking and first-draft underwriting | Disbursement memo drafting |
| Indemnity agreement review | Exception flagging |

**Pricing:**

| Tier | Customer profile | Monthly retainer | Implementation fee |
|---|---|---|---|
| Starter | Small surety producer (1–5 employees) | $3,000 – $5,000 | $2,500 |
| Standard | Mid-size surety agency, small FC firm | $7,500 – $12,000 | $5,000 |
| Enterprise | Bank trust department, established FC firm | $15,000 – $25,000 | $10,000 – $25,000 |

**Service-level commitments:**
- Onboarding completion within 30 days of signed agreement
- Weekly written update plus monthly review call
- Documented change-request process; up to two workflow modifications per month included
- Monitored uptime with first-response inside four business hours on agent failures

### 4.2 Tier 2 — Contractor AI Back-Office Service *(launches Phase 2)*

Retainer-priced operations bureau for small general contractors and specialty subcontractors. Handles month-end finance flow end-to-end.

**Workflows supported:** AIA G702/G703 pay application generation, subcontractor invoice reconciliation, lien waiver tracking across project tiers, retainage management, change-order tracking, draw schedule preparation, **field-purchase receipt capture (Home Depot, Lowe's, lumber yards) with automatic job-cost coding into QuickBooks**.

**Pricing:** $2,500 – $5,000 per month. Volume of customers higher than Tier 1; per-customer attention lower.

**Capability provenance.** The receipt-capture and QuickBooks auto-coding skills shipped to Tier 2 customers are the same skills built and proven in the Rinata Phase 0.5 extension tracks. This is the operational evidence that closes deals — every Tier 2 sales call demos the agent processing a real (anonymized) Rinata receipt → categorized → posted to QBO, then explains the same logic running on a contractor's Home Depot purchase coded to Job 234 → Materials → Framing. The restaurant-to-construction translation is direct because the workflow shape is identical; only the chart of accounts differs.

### 4.3 Tier 3 — Construction-Finance SaaS Product *(launches Phase 3)*

A focused software product, productizing the workflow with the strongest paid demand observed during Phases 1 and 2. Initial candidate: AI-powered pay application generation plus lien waiver verification.

**Pricing:** $300 – $900 per contractor per month; $1,500 – $5,000 per surety / FC firm per month with multi-user seats. Implementation light or self-serve.

---

## 5. Go-to-Market Strategy

### 5.1 Phase 1 acquisition motion (months 1–6)

- **Warm network primary.** Founder's existing surety and construction relationships are the first 15–20 outreach targets. This channel is expected to produce customers 1 and 2.
- **Targeted cold outbound secondary.** Approximately 300 surety bond agencies and FC firms identified via NASBP, state insurance department records, and industry directories. Sequence: personalized email plus LinkedIn. Conversion target: 30 first calls produce 3 pilots produce 1–2 paid conversions.
- **Demo content from Rinata.** Two Loom walkthroughs and one written case study produced during Phase 0 become the primary outbound conversion asset. The narrative bridge is explicit: "this is the same workflow shape as your draw processing — here it is running today on real invoice data."

### 5.2 Phase 2 acquisition motion (months 6–12)

- **Referral flywheel.** Surety customers refer contractor principals; contractor customers create natural demand back to surety/FC accounts. Formalize with a referral fee structure.
- **Content motion.** Begin biweekly long-form content publishing: industry-specific case studies on LinkedIn, guest writing in surety industry publications (Pro Surety Bulletin, NASBP The Surety Magazine), participation in AGC chapters and surety LinkedIn groups.
- **Trade event presence.** Attend two industry events in year two — Surety & Fidelity Association annual meeting and one regional AGC conference.

### 5.3 Phase 3 launch motion (months 12–24)

- **Existing customer base as design partners.** All Phase 1–2 customers offered preferred pricing on SaaS migration.
- **Bottom-up adoption within surety distribution channels.** Surety agencies introduce the product to their contractor principals — channel sales motion with a 15–25% revenue share.

### 5.4 Customer acquisition cost assumptions

- Phase 1 effective CAC: $500–$1,500 per customer in tools and direct selling time at imputed founder rate.
- Phase 2 effective CAC: $200–$600 per customer once content and referral flywheel are operational.
- Phase 3 SaaS CAC target: under $400 per customer at scale.

---

## 6. Operations Plan

### 6.1 Delivery model

Each paid customer receives a dedicated agent instance with isolated data and a per-customer knowledge layer ("vault") in Obsidian. The founder operates a manager-tier interface that monitors all customer agents.

### 6.2 Technical stack (decisions, not options)

| Layer | Selection | Rationale |
|---|---|---|
| Agent harness | Hermes Agent (Nous Research) | Self-evolving, multi-channel gateway, open source — avoids vendor lock-in |
| Compute | Hetzner or Fly.io VPS instances initially; reassess Orgo in Phase 2 | Predictable cost, mature providers |
| Integrations | Composio Standard tier | Managed OAuth and 500+ connectors |
| Memory and knowledge | Obsidian Markdown vault per customer, git-synced | Open format, portable, model-agnostic |
| Primary model | Claude Sonnet 4.6 for production; Claude Opus 4.7 for build phase only | Cost/capability balance verified empirically |
| Secondary models | GLM 5.1, Kimi K-series available for lighter tasks | Cost optimization |
| Communication | Dedicated Gmail per customer, Loom for updates, Trello for request queue | Low-friction, customer-familiar |
| Observability | Hermes built-in logs plus a watchdog agent that emails the founder on gateway failure | Day-one requirement, not deferred |

### 6.3 Security and compliance commitments

- All customer data encrypted at rest and in transit.
- No customer data used to train or fine-tune any model.
- Per-customer isolation; data segregation by VPS instance and vault.
- Documented deletion policy: full purge within 30 days of contract termination.
- Funds-control engagements include explicit human-in-the-loop on every disbursement; agent drafts, human signs.
- SOC 2 Type I targeted by end of year one; budgeted $10,000–$15,000.
- Data Processing Agreement template available before first paid engagement.

### 6.4 Service quality control

- Weekly written update to every customer, regardless of activity.
- Monthly review call with each customer.
- Internal weekly metric review: agent uptime, exception accuracy, response latency, customer-flagged errors.
- All customer issues logged in a single Linear or Trello board; root-cause analysis on any incident over four hours.

---

## 7. Phased Roadmap

### Phase 0 — Foundation (weeks 1–4)
*Detailed plan: see `phase-0-rinata-implementation.md`*

**Objective:** Build a working AI vendor-invoice reconciliation agent for Rinata Restaurant. Use it to produce two on-camera Loom demonstrations and one written case study.

**Core success criteria:**
- Agent processes at least 10 real invoices end-to-end at over 90% line-item extraction accuracy.
- Two Loom demonstration videos recorded.
- One-page written case study completed.
- One sales-analogue document drafted, translating the restaurant workflow into the language of surety and funds-control buyers.

**Phase 0.5 extension tracks** (gated on the core schedule staying on track through Day 21):
- **Walk-in receipt capture** (Days 11–14, parallel to verification work). Adds Costco Business / Restaurant Depot / Sam's Club paper-receipt capture via phone photo, with the same extraction → ledger → exception flow. Introduces a cross-vendor SKU normalization layer that becomes Phase 1 product IP.
- **QuickBooks Online auto-coding** (Days 22–28, parallel to case study production). Adds a categorization-and-posting workflow with strict human-in-the-loop. Saves Rinata 4–8 hours/week of bookkeeping labor and creates a near-direct demo of the contractor job-cost coding pitch.

If the core slips, extension tracks defer to Phase 1 Week 1 — Rinata still receives them within ~5 weeks, but never at the cost of sales-asset production.

**Budget:** Approximately $150 in setup costs plus $80–$100 per month in ongoing operating costs. Extensions add ~$10–$20 in additional API consumption; no new paid tooling.

**Decision gate to enter Phase 1:** core success criteria met, and at least one warm-intro surety or FC contact has agreed to a discovery call after seeing the demonstration. Extension-track completion is a bonus signal of feasibility but not a gate.

### Phase 1 — Paid Pilots in Surety and Funds Control (weeks 5–14)

**Objective:** Land three pilot customers and convert two to paying retainers.

**Activities:**
- Complete warm-intro audit; identify 15 prospects in surety, FC, and contractor finance.
- Build outbound list of approximately 300 firms; sequence outreach.
- Run discovery calls; convert three to 60-day pilots at $1,500–$2,500 per month.
- Build per-customer agents focused on a single workflow each — primary candidate: funds-control draw processing.
- Convert two pilots to paid retainers at $5,000–$8,000 per month.

**Budget:** Approximately $500 per month in operating costs plus $1,000 in legal documentation (MSA, SOW, DPA templates).

**Success criteria:** Two paid customers at month 6 end, generating $10,000–$16,000 in monthly recurring revenue.

### Phase 2 — Build the Practice (months 4–6 — overlaps Phase 1)

**Objective:** Establish operating cadence and produce repeatable runbook.

**Activities:**
- Document every customer interaction, integration, and skill into a versioned runbook.
- Recruit warm-intro pipeline for customers 3–5.
- Begin content publishing motion: one long-form piece every two weeks.
- Raise pricing floor from pilot rate to $5,000–$7,500 standard retainer.

**Success criteria:** 5 paying customers averaging $6,000 monthly retainer; $30,000 monthly recurring revenue by end of month 6.

### Phase 3 — Expansion and Productization Decision (months 7–12)

**Objective:** Add Tier 2 (contractor) customers and validate SaaS product hypothesis.

**Activities:**
- Begin Tier 2 contractor outbound using surety customer referrals.
- Identify which workflow has been delivered 5+ times with consistent customer outcomes — this becomes the SaaS candidate.
- Hire one contractor: engineer or surety-trained customer success.
- Begin parallel SaaS build with existing customers as design partners.

**Success criteria (month 9 gate):** 8 or more paying customers, or clear pipeline to 8 within 60 days. If gate is not met, kill SaaS path, focus on services optimization and pricing increases.

### Phase 4 — SaaS Launch (months 12–24)

**Objective:** Launch productized version of strongest workflow; transition revenue mix toward product.

**Activities:**
- MVP build and design-partner deployment in months 12–18.
- Public launch in months 18–24.
- Services business continues to operate as primary revenue source through month 18.

**Year-two end target:** $800,000–$1,200,000 ARR combined services and early SaaS; product accounts for 20–30% of revenue.

---

## 8. Financial Projections

### 8.1 Cost structure

**Fixed monthly operating costs (single operator, full-time):**

| Category | Monthly cost |
|---|---|
| VPS hosting (3–8 customer instances) | $80 – $200 |
| Composio Standard | $29 |
| Anthropic + OpenAI API consumption | $300 – $1,200 |
| Software (Granola, Loom, Calendly, Linear, Obsidian Sync, etc.) | $150 |
| Domain, email, SSL, miscellaneous | $50 |
| Founder living costs (placeholder) | [excluded from business projection] |
| **Total operating cost** | **$600 – $1,600 / month** |

**One-time setup and legal:**

| Item | Cost |
|---|---|
| Legal: MSA, SOW, DPA, NDA templates | $500 – $1,500 |
| Entity formation (LLC) | $200 – $800 |
| SOC 2 Type I (year-end target) | $10,000 – $15,000 |
| Domain, branding, simple website | $300 – $800 |
| **Total setup** | **$11,000 – $18,100** |

### 8.2 Revenue projections (base case)

| Period | Active customers | Avg retainer | Monthly recurring | Annual run rate |
|---|---|---|---|---|
| End of month 3 | 1 (pilot) | $2,000 | $2,000 | $24,000 |
| End of month 6 | 3 paid | $6,000 | $18,000 | $216,000 |
| End of month 9 | 5 paid | $6,500 | $32,500 | $390,000 |
| End of month 12 | 7 paid | $7,000 | $49,000 | $588,000 |
| End of month 18 | 11 paid + early SaaS | mixed | $75,000 | $900,000 |
| End of month 24 | 14 paid + SaaS scale | mixed | $100,000 | $1,200,000 |

### 8.3 Gross margin

- Variable cost per services customer: $200–$600 per month.
- Gross margin per services customer: 88–96%.
- Effective margin after founder time at $150/hour imputed: 60–75%.

### 8.4 Capital requirements

No outside capital is required under this plan. Phase 0 and Phase 1 are bootstrappable within the $1,000–$10,000 initial budget. SOC 2 spending in months 10–12 is funded from services revenue.

---

## 9. Risk Analysis

| Risk | Likelihood | Severity | Mitigation |
|---|---|---|---|
| Vendor (Hermes / Composio / model provider) deprecation or breaking change | Medium | Medium | Stack abstraction; Obsidian vault and customer skills are portable; no proprietary lock-in to single agent harness |
| Pricing pressure as competing AI vendors enter | Medium | Medium | Vertical depth as moat; raise prices on workflow specificity, not feature count |
| Customer incident (agent fails on a high-stakes disbursement) | Medium | High | Human-in-the-loop contractual; observability and watchdog from day one; insurance |
| Regulatory enforcement (state insurance, fiduciary duty in FC) | Low | High | Customer is the regulated party; we are back-office. Documented compliance posture; SOC 2; legal review of every customer engagement |
| Founder capacity ceiling at 8–12 customers | High | Medium | Hire contractor at customer 5; productize at customer 8 |
| Slow sales cycle in conservative buyer segments | High | Medium | Warm-intro emphasis; expect 60–90 days first-call to close; pipeline 3× target conversion volume |
| Large entrant (Procore / Acrisure) launches competing offer | Low this year, rising | Medium | 18-month head start; deep customer relationships; vertical depth and integration density compound |
| Rinata co-owner objection to public case study | Low | Low | Explicit consent prior to Phase 0 launch; redacted numbers in any external material |

---

## 10. Founder Background

[Founder Name] brings:

- One-third ownership in Rinata Restaurant, a successful Italian restaurant in South Minneapolis, Minnesota — providing an operational testbed and credibility-building case study environment.
- Deep working knowledge of the contract surety bond industry and funds control / escrow account management, gained through [add specifics: years of experience, prior roles, certifications].
- Finance degree and familiarity with construction billing operations.
- Hands-on capability in modern AI tooling, including Claude Code, agent harness configuration, and low-code integration platforms.

This combination — domain expertise, financial fluency, ownership of a credible operational asset, and technical capability — is uncommon and constitutes the primary competitive moat.

---

## 11. Decision Framework

Proceed with the plan if, by end of Phase 0:

1. Rinata vendor invoice reconciliation agent achieves the technical success criteria.
2. At least one warm-intro surety, FC, or contractor finance contact agrees to a Phase 1 discovery call after seeing the Phase 0 demo.
3. Founder has confirmed personal commitment to a 12-month runway on this plan over alternative paths.

Hard pivot points:
- **Month 6:** fewer than 2 paid customers → revisit ICP, pricing, or motion.
- **Month 9:** fewer than 5 paid customers → kill SaaS hypothesis, optimize services only.
- **Month 12:** fewer than 7 paid customers → reconsider full strategy.

---

## Appendix A — Candidate Working Names

- **Bondline** — direct, surety-evocative, single-word brandability
- **Draftline** — references both construction draws and document drafting
- **Lienpath** — funds-control and lien waiver association
- **Cornerstone Agents** — construction-finance metaphor, "agents" double meaning
- **Surepoint** / **Surepath** — surety-adjacent
- **Bondcraft** — quality and craft connotation

Selection criteria: domain availability, no existing surety industry trademark, pronounceability over the phone, ability to extend the brand to contractor and SaaS tiers later.

## Appendix B — Reference Documents

- `phase-0-rinata-implementation.md` — detailed week-by-week Phase 0 plan
- Source plan: `C:\Users\shant\.claude\plans\i-ve-been-thinking-a-glistening-parasol.md` — original decision memo

## Appendix C — Industry Reference Sources

- National Association of Surety Bond Producers (NASBP)
- The Surety & Fidelity Association of America (SFAA)
- Associated General Contractors of America (AGC)
- AIA Contract Documents (G702/G703 reference)
- State insurance department records for surety agency licensing
