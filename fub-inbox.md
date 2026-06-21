---
name: fub-inbox
description: "FUB Inbox Priority Review + Automation Audit. Use when Lucia wants to see who needs a reply today (especially anyone wanting to see a property), plus an audit of active automations and template gaps."
---

# FUB Inbox Priority Review + Automation Audit

## Part 1 — Priority Reply List

### Parallel data pull
1. `mcp__followupboss__listTextMessages` limit:50
2. `mcp__followupboss__listEvents` limit:75
3. `mcp__followupboss__listTasks` limit:30

### Score each inbound contact

| Signal | Pts |
|---|--:|
| Wants to see / schedule showing / "tour" / "walk-through" | +5 |
| Mentions specific address or listing | +3 |
| "pre-approved" / "cash buyer" / "ready" / "have financing" | +4 |
| "today" / "tomorrow" / "this weekend" / "ASAP" / "urgent" | +3 |
| No agent reply yet (inbound with no outbound follow-up) | +3 |
| Multiple messages in last 48h | +2 |
| Overdue task for this person | +2 |
| Portal inquiry (Zillow/Realtor.com/website) | +2 |
| Cold/generic/auto-response signal | −3 |

≥5 = **HOT** · 3–4 = **WARM** · Show only HOT and WARM

For each HOT/WARM: call `mcp__followupboss__getPerson` once to get name, stage, assigned agent, last activity, phone/email.

### Output

```
## 🔴 Reply NOW (HOT)
**[Name]** — Score: X
- Last message: "[quote, max 2 sentences]"
- Channel: Text / Email · Stage: [stage]
- Why urgent: [1 line]
- Suggested reply: [1–2 sentence draft]

## 🟡 Follow Up Today (WARM)
[same, briefer]
```

Zero HOT = say so in one line, proceed to Part 2.

---

## Part 2 — Automation & Template Audit

### Parallel data pull
1. `mcp__followupboss__listAutomations` limit:50
2. `mcp__followupboss__listAutomationsPeople` limit:100
3. `mcp__followupboss__listTemplates` limit:50
4. `mcp__followupboss__listTextMessageTemplates` limit:50
5. `mcp__followupboss__listActionPlans` limit:50

### Gap analysis
- Which lead sources from Part 1 have NO automation?
- Which stages appear in active leads but have no automation step?
- HOT/WARM contacts from Part 1 not enrolled in any automation?
- Automations with zero enrolled (stale/unused)?

### Output

```
## Automations Running
| Name | Enrolled | Status |
(top 10 by enrollment; skip paused with 0 enrolled)

## Templates
Email: N — [top 3 names]
Text: N — [top 3 names]
Action Plans: N — [all names]

## Gaps (act on these)
1. [specific gap with lead count]
2. ...

## Suggested Additions (ranked by impact)
1. [e.g. "Showing Requested action plan: immediate text + follow-up for showing requests"]
2. ...
```

---

**Token rules:** never call `listPeople` unfiltered · `limit:50` or less on all calls · don't re-fetch data already retrieved · stop after Part 2
