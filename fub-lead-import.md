---
name: fub-lead-import
description: "Use when Lucia wants to import, normalize, triage, score, or act on Follow Up Boss rental leads using Google Sheets, Drive exports, Notion, Drip, Gmail, or Google Calendar. Helps identify hot leads, target the right renters, and recommend the best email, SMS, Drip, or Notion next action. FUB is always read-only — draft only, never send/activate without confirmation."
---

# FUB Lead Import & Triage

## Import & Normalize
1. Identify source (Sheets, Drive CSV, Notion, screenshot, pasted data)
2. Normalize dates; map statuses to pipeline (see CLAUDE.md)
3. Extract preferences from notes: budget, neighborhood, beds, move date, pets, guarantor, tour windows
4. Deduplicate by email → phone → name+source+listing
5. Flag missing: budget, move date, beds, contact method

## Lead Scoring (0–100)

**Add:** +25 inbound reply <24h · +20 tour request/availability given · +18 toured or next-steps asked · +18 app started/requested · +15 move date ≤30 days · +12 budget fits · +10 clear beds+neighborhood · +10 has phone+email · +8 opened/clicked/replied campaign · +8 referral or strong source

**Subtract:** −25 no contact method · −20 dead/spam/unqualified · −15 no reply after 3+ outbound · −12 budget below listing · −10 move date >90 days · −10 missing budget+move date · −8 duplicate · −8 listing unavailable, no alt

**Bands:** 90–100 reply now · 75–89 hot, send today · 55–74 warm follow-up · 35–54 nurture · 0–34 suppress

## Segments
- **Hot tour lead** — inbound interest or tour request
- **Showing scheduled** — future tour date confirmed
- **Post-tour/app push** — toured, asked about applying
- **Flip candidate** — original unit gone or better alts exist
- **Qualification needed** — missing budget/move/beds/pets
- **No-response follow-up** — contacted, no inbound reply
- **Fresh inquiry** — new, no meaningful follow-up yet
- **Long-term nurture** — move date far out or unclear
- **Dead/unqualified** — spam, broker, impossible budget

## Best Send Per Segment

| Segment | Channel | CTA |
|---|---|---|
| Fresh inquiry | SMS first | "What move date? Free to tour today/tomorrow?" |
| Qualification needed | SMS | One question only: move date or budget |
| Hot tour lead | SMS | Specific windows: "Can you do [A] or [B]?" |
| Showing scheduled | Email | Confirm + access note |
| Post-tour | SMS | "Want next steps for applying, or see similar options?" |
| Flip | Email+SMS | 2–4 alts max, one CTA |
| No-response | SMS | "Still looking or should I close this out?" |
| Long-term nurture | Email | Market check-in or criteria refresh |

## Default Templates

**Fresh inquiry SMS:** `Hi {{first_name}}, saw your inquiry on {{listing}}. What move date are you targeting and are you free to tour {{today/tomorrow}}?`

**Flip SMS:** `Hi {{first_name}}, checking {{original}} but if unavailable I found similar options near {{area}}. Want me to send the best 2–3?`

**No-response SMS:** `Hi {{first_name}}, still looking for {{beds}} around {{area/budget}}, or should I close this out for now?`

**Post-tour SMS:** `Hi {{first_name}}, thanks for seeing {{listing}}. Want next steps on applying or a few similar options to compare?`

## Output Format
1. **Top priority leads** — ranked list: score, segment, reason, next action
2. **Segment counts**
3. **Recommended sends** — lead-specific SMS/email drafts for top leads
4. **Missing info** — what needs confirming before sending
5. **System updates** — suggested Notion/Sheet fields (never apply without confirmation)

Table when useful: `| Priority | Lead | Score | Segment | Why now | Best send | Verify |`

> Safety: FUB read-only. Confirm before sending, activating Drip, or updating live systems.
