# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> Business rules, tone, FUB workflow, and skill behaviors are in `~/.claude/CLAUDE.md` (global config). This file covers workspace layout and project architecture.

## MCP Servers

| Server | Command | Purpose | Known failure mode |
|---|---|---|---|
| `fub` | `python3.11 fub_extended_mcp.py` (defined in `~/.claude.json`) | Lightweight FUB reads (inbox, overdue tasks) | `~/.claude.json` is authoritative for this server — confirmed via `claude mcp list`. A stale duplicate in `~/.claude/settings.json` (pointing at `fub_mcp_wrapper.py`, a thin exec-wrapper around the same file) was removed 2026-08-03; it was always shadowed and never actually loaded |
| `fub-full` | `node followupboss-mcp-server/index.js` | Full FUB read/write (creates, updates, notes, tasks) | -32000 reconnect = check for a stale/placeholder path in `~/.claude.json` or `~/.claude/settings.json` (both define this one identically, no conflict) |
| `kapture` | `npx kapture-mcp@latest bridge` | Reads FUB inbox threads/SMS (API can't) + Bentley (bentley.realtymx.com) navigation | — |
| `claude-in-chrome` | `npx @anthropic-ai/mcp-server-claude-in-chrome` | General browser automation (StreetEasy, building sites) | — |
| `github` | HTTP, `api.githubcopilot.com/mcp/` | GitHub API access | Currently failing — `HTTP 400: Authorization header is badly formatted` |
| `noteplan` | `npx @noteplanco/noteplan-mcp` | NotePlan integration | — |
| `paste` (`.claude.json` only) | HTTP, `127.0.0.1:39725/mcp` | Local paste helper | Not running — connection refused |

**Kapture** is the right tool for reading FUB inbox threads and SMS conversations (the API can't). **FUB MCP** handles all data mutations. Use Kapture for Bentley (bentley.realtymx.com) navigation.

**Precedence note:** when the same MCP server name is defined in both `~/.claude.json` and `~/.claude/settings.json`, `~/.claude.json` wins — confirmed via `claude mcp list`, which shows the actually-connected command. Check there first instead of assuming either file is authoritative.

## Key Files to Check First

- **Inventory** → run `/rics-listings` (live StreetEasy check, not a static file) before recommending any apartment
- **Voice/format** → Google Doc ID `1NMJQ9djEF0_fjEMrW6RqOOKASo9b6YPNPfdYSqRSH9A` ("6 6 How To Build Emails") — use Drive MCP to read before drafting HTML. The old `Email Drafting Playbook.docx` is superseded.
- **Pipeline context** → `~/Claude/Projects/FUB & Tools/FUB_Project_Instructions.md` for lead prioritization rules
- **Past outputs** → `~/Claude/Projects/FUB & Tools/FUB Email – *.html` to avoid repeating already-sent blasts

## Inventory Sheet Sources

Sheets in `~/Claude/Projects/FUB & Tools/`:
- **Chestnut Holdings Snapshot.xlsx** — Chestnut (OP)
- **Gilardian Snapshot 2026.xlsx** — Gilardian (OP)
- **GPG spreadsheet.xlsx** — GPG (OP)
- **MGM Snapshot 2026.xlsx** — MGM (OP)
- **Mango Snapshot.xlsx** — Mango (OP)
- **Village Dwellings Update.xlsx** — Village Dwellings (always TRPA)
- **BLDG_Update.pdf** — BLDG Management (OP)
- **NYC Tenant Representation.gsheet** — Margules + others (always TRPA)

## Skills & Live Data

`~/claude-skills/` — skills + live tracking data, separate from `~/Claude/commands/`. Register new skills here, not in cwd.

| File | What it does |
|---|---|
| `email-blast.md` | FUB email/text blast generator from any listing input format |
| `tenant-rep-blast.md` | TRPA/TRO blast generator (Margules, Village Dwellings, off-SE units) |
| `bond-lead-matcher.md` | Ranked apartment send list from a lead note |
| `bentley-pull.md` / `bentley-import.skill` | Bentley (bentley.realtymx.com) listing extraction |
| `draft-fub-sequence.md` | 4-email FUB action-plan sequence |
| `fub-inbox.md` | Inbox priority review + automation audit |
| `fub-intel.skill` | FUB triage/segment/track modes |
| `fub-lead-import.md` | Lead import handling |
| `fub-building-email.skill` | Building-specific email formatting |
| `pull-media.md` | Media URL backfill for listings |
| `rental-app-analysis.skill` | 40x rule / guarantor rental app review |
| `real-estate-drip-workflows.md` | Drip stage architecture (Immediate → Post-Tour) |
| `sheet-listings.skill` | Spreadsheet-sourced listing ingestion |
| `triage.md` | Fast FUB inbox scan (URGENT/SHOWING/APP/QUESTION/SKIP) |
| `ric_listings_snapshot.md`, `rics-listings.md` | Live listing snapshots — always pull live, never trust as static |
| `data/fub_setup_status.json` | Per-listing setup/automation status |
| `dashboard/ric-listings-dashboard.html` | Status dashboard artifact |

## Live Artifacts (qualified-bank / rics-listings)

Exactly ONE live artifact per dataset. Before patching, list candidate files with timestamps and confirm you're editing the live snapshot, not an older/duplicate file. After any patch: dedupe, verify media/image URLs survived, report before/after record count, then republish.

Git-tracked at `~/Claude/scratchpad/` (repo initialized 2026-08-03) — auto-commits on session end, so a bad patch can be diffed/reverted instead of re-run through a backfill script.

For "which file is actually live" archaeology across multiple candidate versions (qualified-bank*, Harlington scrapes, etc.), delegate the exploration to a subagent that reports back a table (file, timestamp, entry count) — don't burn main-session context on it, and don't let it edit anything.

## Shared FUB Account

The FUB account belongs to Ric Salinas. Three users share it:
- **Ric Salinas** — broker/co-owner
- **Jessie Huaman** — agent collaborator
- **Lucia Johansson** — Lucia (the user)

Treat all leads in the account as shared pipeline regardless of assigned agent.
