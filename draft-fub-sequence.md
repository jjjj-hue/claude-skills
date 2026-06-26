---
name: draft-fub-sequence
description: "Draft FUB Email Sequence. Use when Lucia needs a complete 4-email Follow Up Boss action plan sequence for a rental unit — initial reply, flip options, alternatives, and evergreen check-in. Follows Bond NY / SpaceSalsa playbook."
---

# Draft FUB Email Sequence

Draft a complete 4-email Follow Up Boss automation sequence for a rental building unit, following the SpaceSalsa / Bond New York playbook exactly.

## HOW TO START

Ask the user for (if not already provided):
1. **Unit(s)** — address + unit number(s) being advertised
2. **Status** — Leased/Approved, Available-Occupied, or Available-Vacant
3. **Profile** — beds, price range, neighborhood
4. **Media** — 3D Tour links, video links, or photo set (one per listing)
5. **Inventory pool** — up to 5 listings per email (address, beds, rent, availability, concession, media link)
6. **Shared automation?** — if two+ units share same profile, one automation can cover both (see Flip Logic)
7. **PS Line Library** — ask user to paste the PS Line Library v2 content, OR use the placeholder format below

---

## VOICE & TONE (NON-NEGOTIABLE)

- Direct, personal, 1-to-1. Always reads like Ric writing to one specific person.
- Never sounds like a marketing email or blast.
- Short paragraphs. Natural language. No fluff. No corporate filler.
- Sign-off: always **"Ric."**
- Greeting: always **"Hi %contact_first_name%,"**

---

## SUBJECT LINE (EVERY EMAIL)

```
%inquiry_address% StreetEasy Inquiry From %contact_first_name%
```

Makes it look like a direct reply to their StreetEasy inquiry, not a blast.

---

## MERGE TAGS

- `%inquiry_address%` — the address/unit the lead inquired on (used in subject + body of Email 1)
- `%contact_first_name%` — lead's first name

---

## SEQUENCE CADENCE

| Email | Delay | Content |
|-------|-------|---------|
| 1 | 5 min | First touch — unit status + first 5 listings |
| 2 | 20 min | 5 more listings |
| 3 | 6 hrs | More options + introduce end-of-June pipeline |
| 4 | Day 7 | Evergreen check-in / soft close — no listings, re-engage |

Rules:
- 5 listings per email, MAX (Emails 1–3 only; Email 4 is evergreen, no listings)
- Old templates stay in FUB inactive — never deleted

---

## EMAIL 1 — FLIP LOGIC (pick based on unit status)

**(A) Unit Leased / Approved (most common)**
> "Thanks for reaching out on %inquiry_address%. That one just got leased — but I have a few similar 2BRs available right now. Here's what I'm working with:"

**(B) Unit Available but Occupied**
> "Thanks for reaching out on %inquiry_address%. Good news — it's available. It's currently occupied, so I set showings up around the current tenant. Send me a couple of times that work this week and I'll coordinate with them and confirm.
>
> In the meantime, here are a few others in the same range that are open right now:"

**(C) Unit Available / Vacant**
> "Thanks for reaching out on %inquiry_address%. It's still available — I can get you in to see it. Here are a few others in the same range while we're at it:"

Flip inventory (Emails 1–9): always IMM / Apt Open first. Pipeline (end-of-June) units introduced Email 3+, framed as "get on the radar now."

---

## LISTING FORMAT

```
[Address] #[Unit] – [Beds] BR – $[rent]/mo | [availability] | [concession] | [media link]
```

**Examples:**
```
118 West 83rd #3C – 2 BR / Open Kitchen, DW – $4,075/mo | IMM | Apt Open | [3D Tour](Link)
693 Ninth Ave #2FN – 2 BR – $3,750/mo | IMM | 1 month free | [3D Tour](Link)
411 East 70th #5C – 2 BR – $4,000/mo | Avail end of June | [3D Tour](Link)
```

Availability tags: `IMM`, `Apt Open`, `Avail [date]`, `Avail end of June`, `TBD`
Concessions when applicable: `1 month free`, `2 months free`
Media: one link per listing — 3D Tour (default for UES 2BR), video, or photo set. State media rule at top of sequence doc.

---

## SHARED AUTOMATION (multiple units, one build)

When two+ units share the same profile (same beds, same price band, same area):
- Trigger = Tag Added, include ALL tag variants for all units + StreetEasy variants
- `%inquiry_address%` makes Email 1 auto-read correctly for whichever unit the lead came in on
- The flip inventory is identical (same profile, same pool)

**3D Tour trade-off:** One automation can't merge two different tour URLs.
- Default: remove hardcoded tour link from Email 1, offer on reply: *"I'll get you the 3D tour so you can take a look before we go."
- Alternative: split back into two separate automations. Ric's call per build.

---

## P.S. SYSTEM

Every email ends with a P.S. driving to welcomehomenyc.net — **EXCEPT** Piece of Cake emails (automation #65, movers — no P.S., booking link is the only CTA).

**Format (strict):**
- ONE hyperlinked anchor per P.S.
- Hook sentence(s) = plain text only
- Anchor text = blue hyperlinked text only
- Destination: always `https://welcomehomenyc.net`
- FUB auto-wraps as `fub.direct/...` tracked redirect on paste

**Example:**
> P.S. Most people furnish their first NYC apartment wrong. [Here's how to do it right.](https://welcomehomenyc.net)

**Tone rotation across a 9-email sequence:**
| Email | Tone |
|-------|------|
| 1 | Warm but Sharp |
| 2 | Dry NYC Humor |
| 3 | Brand-Forward |
| 4 | Confident & Slightly Smug |
| 5+ | Direct & No Apology |
| 6, 9 (evergreen) | Warm (don't read pushy) |

Every P.S. in a sequence is a DISTINCT line — no lead sees the same P.S. twice.

If PS Line Library v2 is not available, generate original P.S. lines matching the tone rotation above, routing to `https://welcomehomenyc.net`. Reference brands: Fellow, Yamazaki, Brightech, Nathan James, AquaTeak, Adesso.

---

## TEMPLATE NAMING CONVENTION

```
[Date] #[Step] [Description] [Building/Address]
```
Example: `5/10/26 #1 Initial 52 Barrow 3 Bed`

---

## INVENTORY SOURCING NOTE

Inventory is pulled from Google Sheets (Margules, BLDG, SOLIL, Brusco, GPG, Centennial, West Side Mgmt, etc.) — all feed one management-agnostic pool. Lead profile (beds + price + neighborhood) decides what gets served, not the landlord. IMM / Apt Open first. Pipeline in Email 3+.

---

## OUTPUT FORMAT

For each email, output:
1. **Template name** (using naming convention above)
2. **Subject line**
3. **Body** (ready to paste into FUB)

After all 9 emails, output a **trigger tag list** — all address variants to add to the automation trigger.

---

## $ARGUMENTS$
