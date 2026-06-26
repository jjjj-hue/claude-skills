---
name: triage
description: "FUB Inbox Triage — Minimal. Scan FUB inbox fast via JavaScript, flag threads by urgency (URGENT/SHOWING/APP/QUESTION/SKIP), max 3 click-ins. Use when Lucia wants a quick scan of who needs a reply."
---

# FUB Inbox Triage — Minimal

Scan FUB inbox in one call. No screenshots. No navigation. No clicking unless a preview is ambiguous and truly worth it.

## RULES
- One JavaScript call reads the entire inbox thread list as text
- Flag threads from preview text only — no clicking unless essential
- Max 3 click-ins, only if the preview is a direct question or scheduling ask that needs context
- Output immediately. Done.

## STEP 1 — Read Inbox via JavaScript (one call)

The FUB inbox tab is always open. Find it in `mcp__kapture__list_tabs` — look for `spacesalsa.followupboss.com/2/inbox`.

Run this single JS call on that tab:

```javascript
const body = document.body.innerText;
const start = body.indexOf('Unread Messages');
body.slice(start, start + 4000)
```

This returns the full thread list: name, channel, preview, time. Read it all at once.

If the tab isn't open, navigate to `https://spacesalsa.followupboss.com/2/inbox-new` first, wait, then run the JS.

## STEP 2 — Flag from Preview Text

From the JS output, mark each thread as one of:
- ⚠️ URGENT — unsubscribe / STOP / wire issue / deal problem
- 📅 SHOWING — "what time", "when can", "schedule", "can we see"
- 📋 APP — "application", "apply", "send the app"
- ❓ QUESTION — direct question needing a real answer
- ✅ SKIP — "thank you", "sounds good", no reply needed

## STEP 3 — Click-in Only If Needed (max 3)

Only click a thread if the preview cuts off mid-question.

## OUTPUT — One Table

| Lead | Type | What they need | Action | When |
|---|---|---|---|---|

Skip list (one line): "Skipped: Name, Name — no action needed."

## $ARGUMENTS$
