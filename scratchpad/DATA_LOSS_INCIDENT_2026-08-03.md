# Data Loss Incident — Aug 3, 2026

**Status:** Resolved ✓

## What Happened
- **Aug 1 15:29**: qualified-bank-interactive-clean.html created with 1,010 entries (baseline)
- **Aug 3 01:51**: qualified-bank-LIVE.html edited outside Claude Code → corrupted to 850 entries (160 lost)
- **Aug 3 10:07+**: Claude sessions began; pre-tool-use hook backups captured the corrupted state 8 times
- **Aug 3 10:18**: SessionEnd hook auto-committed the corrupted state to git

## Root Cause
File was edited outside Claude Code harness (no hook protection). Likely manual edit, script, or external tool that truncated the data array.

## Resolution
- Restored qualified-bank-LIVE.html from Aug 1 clean backup: 1,010 entries recovered
- Committed restore at commit 8ba6187
- All 160 missing entries now restored

## Going Forward
**Workflow locked as of Aug 3:**
1. Only edit `qualified-bank-LIVE.html` via Claude Code
2. PreToolUse hook creates timestamped backup before each Write/Edit
3. SessionEnd hook auto-commits to git with timestamp
4. Never edit this file outside Claude Code CLI/IDE/web app
5. If manual edit needed: use git worktree isolation instead

**Backup locations:**
- Real-time: `~/Claude/scratchpad/backups/qualified-bank-*.html` (hook-created)
- Git history: `git log --oneline -- qualified-bank-LIVE.html`
- Reference clean state: interactive-clean.html (keep as read-only reference)

**Verification command:**
```bash
cd ~/Claude/scratchpad && grep -c '"address":' qualified-bank-LIVE.html
# Should always be 1010 or higher
```
