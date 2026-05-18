# Phase 0 — Day 1 Task List

**Date:** [tomorrow's date]
**Goal of the day:** End the day with co-owner consent secured, accounts created, dev environment running, and the Obsidian vault scaffolded with real Rinata vendor data. **No agent code yet** — that's Day 2.

**What "done" looks like at end of day:**
- ✅ Written consent from Rinata co-owners
- ✅ You know exactly what hosts `info@rinatarestaurant.com`
- ✅ A captured list of Rinata's top 5–10 vendor sender domains and invoice subject patterns
- ✅ Anthropic API account with a $50 prepaid hard cap
- ✅ Composio account on the free tier, Gmail/Outlook connector authenticated
- ✅ WSL2 running on your Windows machine
- ✅ A private GitHub repo for the Obsidian vault, with the folder structure committed
- ✅ Top 5 vendor files in the vault populated with what you already know

---

## Morning Block — Conversations & Verification (2–3 hours)

The first three tasks gate everything else. Do not skip ahead.

### 1. Co-owner consent conversation (45–60 min) ⛔ BLOCKING

- [ ] Call or meet with both co-owners.
- [ ] Walk them through: what you're building, why you're building it (also helps Rinata operations), what data the agent will see, what you want to do with the case study externally.
- [ ] Be specific about what they're approving:
  - Agent reads invoice email from `info@rinatarestaurant.com` (filtered to invoice mail only)
  - Agent stores extracted invoice data in a vault you control
  - Agent's findings shared with all three owners weekly
  - Anonymized, number-redacted results may appear in your sales material starting in 4 weeks
- [ ] Get their consent **in writing.** A simple email reply from each of them saying "I'm OK with this as discussed" is enough. Save it.

**If they have concerns:** stop and resolve before continuing. Don't proceed on a verbal "sure, sounds fine" — you need durable consent because the case study only works if they're comfortable with you using it.

### 2. Verify email host (10–15 min)

- [ ] Open the email settings for `info@rinatarestaurant.com`. Find the MX records or check the login URL.
- [ ] Determine: Google Workspace, Microsoft 365, or web-host-forwarded?
- [ ] If Workspace or M365: continue.
- [ ] If forwarded-only: figure out where it actually lands (the destination is what Composio connects to).
- [ ] Note who has admin access to set up filters and labels. If it's not you, schedule a 30-min session with whoever does (could be one of the co-owners, the bookkeeper, or the GM).

### 3. Skim the inbox for vendor patterns (30–45 min)

- [ ] Open `info@` and sort by sender (or use `from:` searches).
- [ ] Capture in a notepad or directly into your Obsidian vault:
  - The 5–10 vendor sender domains that send invoices most frequently (e.g., `sysco.com`, `usfoods.com`, plus your specialty Italian importer, beer/wine distributors, local farms)
  - The 3–5 recurring subject-line patterns (e.g., "Invoice #", "Statement", "Remittance Advice")
  - Anything that looks like an invoice but probably isn't (statements, delivery confirmations, marketing) — these are what your filter must *exclude*
- [ ] Save this list as `vendor-patterns.md` in the Obsidian vault folder you'll create later.

---

## Midday Block — Accounts & Dev Environment (2 hours)

Order matters here too — some accounts depend on others.

### 4. Anthropic API account with hard cap (15–20 min)

- [ ] Sign up at console.anthropic.com.
- [ ] Add $50 in prepaid credits.
- [ ] Set a **monthly spend limit of $50** in the usage settings — this is the hard cap that protects you from a runaway loop.
- [ ] Create an API key named `rinata-phase-0`. Copy it somewhere secure (1Password, Bitwarden, or a `.env` file you'll never commit).
- [ ] Verify: `curl` a test message against the API with the key to confirm it works.

### 5. Composio free tier account (15–20 min)

- [ ] Sign up at composio.dev.
- [ ] Confirm you're on the free tier (20K tool calls/month).
- [ ] In Composio's dashboard, connect:
  - [ ] The Gmail (or Outlook) account hosting `info@rinatarestaurant.com`
  - [ ] Google Drive (same account or whichever owns the invoice files)
  - [ ] Google Sheets (same account)
- [ ] Authenticate each via OAuth. Confirm in Composio dashboard that all three show "Connected."

### 6. WSL2 install (30–45 min — variable, may need a restart)

- [ ] Open PowerShell as administrator.
- [ ] Run `wsl --install`. Restart if prompted.
- [ ] After restart, open Ubuntu from the Start menu, set username/password.
- [ ] Inside WSL Ubuntu, run `sudo apt update && sudo apt upgrade -y` (takes a few minutes).
- [ ] Install basics: `sudo apt install -y git curl wget python3 python3-pip nodejs npm build-essential`
- [ ] Verify: `git --version`, `python3 --version`, `node --version` all return.

### 7. Git + GitHub setup (15 min)

- [ ] Configure git inside WSL2: `git config --global user.name "Your Name"` and `git config --global user.email "your@email.com"`.
- [ ] Generate an SSH key in WSL2: `ssh-keygen -t ed25519 -C "your@email.com"`. Accept defaults.
- [ ] Add the public key (`cat ~/.ssh/id_ed25519.pub`) to your GitHub account at github.com/settings/keys.
- [ ] Create a new **private** GitHub repo named `rinata-vault`. Don't initialize with anything (no README, no .gitignore).

---

## Afternoon Block — Vault Foundation (2–3 hours)

This is the work that will feel most useful — you're building the agent's knowledge base.

### 8. Create the Obsidian vault structure (30 min)

- [ ] Install Obsidian on Windows from obsidian.md if not installed.
- [ ] Create a folder at `C:\Users\shant\Documents\rinata-vault\`.
- [ ] In Obsidian, "Open folder as vault" → point at that folder.
- [ ] Create this folder structure inside the vault:
  ```
  rinata-vault/
  ├── 00-meta/
  │   ├── README.md
  │   └── agent-operating-instructions.md
  ├── vendors/
  ├── skus/
  ├── invoices/
  │   ├── processed/
  │   └── exceptions/
  └── runbook/
  ```
- [ ] In `00-meta/README.md`, write a paragraph: what this vault is, who owns it, what the agent uses it for. Date it.

### 9. Init git, push to GitHub (15 min)

- [ ] Open a WSL terminal in the vault directory (`cd /mnt/c/Users/shant/Documents/rinata-vault`).
- [ ] `git init`
- [ ] Create a `.gitignore` containing at minimum: `.obsidian/workspace*`, `.DS_Store`, `*.tmp`
- [ ] `git add . && git commit -m "Initial vault structure"`
- [ ] `git remote add origin git@github.com:[yourusername]/rinata-vault.git`
- [ ] `git push -u origin main`
- [ ] Verify on github.com that the folder structure is there.

### 10. Populate top 5 vendor files (45–60 min)

For each of the top 5 vendors by invoice volume (from the patterns you captured in Task 3), create a file at `vendors/[vendor-name].md` with this template:

```markdown
# [Vendor Name]

## Basics
- **Sender domain:** [e.g., orders@sysco.com]
- **Category:** [broadline / specialty / produce / beverage / paper / equipment]
- **Typical delivery cadence:** [e.g., 2x weekly Tues/Fri]
- **Account contact:** [name, email, phone if known]
- **Account number:** [if known]

## What we order
- [Top 5–10 SKUs by frequency, with typical pack size if known]

## Pricing notes
- [Any known contract pricing, recent changes, or pricing quirks]

## Patterns to watch
- [Anything the agent should know — e.g., "Sysco occasionally bills for a substituted product at a higher price without flagging it"]
```

Don't over-engineer this — you're capturing what you already know. The agent will refine and extend it over weeks 2–3.

### 11. (Stretch — only if time) SKU catalog scaffolding (30 min)

- [ ] Create `skus/_index.md` with a simple table: SKU description, primary vendor, typical pack size, last-known price, last-known date.
- [ ] Populate 10–20 high-volume SKUs you already know off the top of your head (olive oil, San Marzano tomatoes, flour, wine list staples, etc.). Don't aim for completeness — the agent fills the rest in over time.

---

## End of Day — Wrap-Up (15 min)

- [ ] Commit and push everything: `git add . && git commit -m "End of Day 1: vault foundation" && git push`.
- [ ] In `00-meta/`, create `day-1-log.md` and jot down: what worked, what was harder than expected, anything blocking Day 2.
- [ ] Look at Day 2 of `phase-0-rinata-implementation.md` so tomorrow has no friction starting.

---

## What NOT to do today

- ❌ Don't install Hermes yet. That's Day 2.
- ❌ Don't write any agent skills yet.
- ❌ Don't set up email forwarding or filters yet — you'll do that on Day 2 after you have Hermes running and have decided exactly which label name and filter rules to use.
- ❌ Don't process any real invoices yet. Tomorrow.
- ❌ Don't optimize the vault structure. It'll evolve. Get something committed.

---

## If You Hit a Blocker

| Blocker | What to do |
|---|---|
| Co-owners not available today | Reschedule. Move all other tasks to a different day. Consent is non-negotiable as a starting point. |
| WSL2 install fails | Check Windows version (requires Win 10 2004+ or Win 11). Enable virtualization in BIOS. Try `wsl --install -d Ubuntu-22.04` explicitly. |
| Composio OAuth fails for the Rinata Gmail | Check whether two-factor auth or admin restrictions are blocking app passwords. May need a Workspace admin to grant the OAuth scope. |
| Anthropic console won't accept a card | Try a different payment method. Worst case, use the OpenAI API with GPT-4-class model as a temporary substitute for Day 2 testing — switch back once Anthropic clears. |
| You realize `info@` is forwarded from somewhere weird | Find the actual mailbox. If it's an IMAP-only host without OAuth, you'll need a different connector approach — log it and move on to other Day 1 tasks while you figure it out. |

---

## Realistic time estimate

- **If everything goes well:** 6 hours of focused work.
- **If you hit one normal-sized snag** (WSL install needs a Windows update, OAuth needs an admin nudge): 8 hours.
- **If two things go wrong:** budget into Day 2 and accept that's fine.

The goal isn't to finish every item — it's to finish items 1–7 (consent, verification, accounts, dev env). Everything from item 8 onward can slide a day without breaking the schedule.

Good luck. Day 2 starts with Hermes install and your first agent message.
