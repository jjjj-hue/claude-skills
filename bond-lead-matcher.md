---
name: bond-lead-matcher
description: "Use when Ric or Lucia provides a renter lead note, CRM/FUB message, client criteria, or apartment inventory and needs a ranked Bond New York apartment send list. Extract budget, move date, neighborhood, beds, must-haves, and tenant rep status; search only active/current units; require OP unless tagged #tenantrep; exclude rented, expired, or unavailable units; and return a clean copy-ready format for Ric."
metadata:
  author: Lucia
  version: '1.0'
---

# Bond Lead Matcher

## When to Use This Skill

Use this skill whenever Lucia or Ric needs to turn renter lead information into a ranked list of apartments to send or pursue at Bond New York.

Trigger this skill for requests such as:

- "Match this lead to apartments"
- "What should I send this lead?"
- "Find good fits from this inventory"
- "Rank these listings for this client"
- "Make a send list for Ric"
- "Here is a FUB lead/message/note"
- "This person wants a 1 bed under $4,000 downtown"
- Any pasted CRM note, text message, email, lead criteria, listing sheet, availability list, or apartment inventory where the goal is to identify suitable rental matches

This skill is especially important when the user provides both:

1. Lead criteria, such as budget, move date, neighborhood, beds, amenities, timing, guarantor/pet needs, or tenant rep status
2. Current apartment inventory, a listing sheet, or permission to use available Bond/NYC rental inventory

## Core Objective

Turn a lead note, message, or criteria summary into a ranked apartment send list for Ric at Bond New York.

The output must answer:

- What does the lead want?
- Which apartments are the best available matches?
- Why does each match work?
- Which units should be excluded and why?
- What should Ric send or do next?

Return the result in a clean, copy-ready format for Ric.

## Matching Rules

### Extract Lead Criteria First

Before matching apartments, extract and summarize the lead's criteria.

Look for:

- Budget or max rent
- Move date, lease start timing, or urgency
- Neighborhoods, boroughs, commute needs, or location preferences
- Bedroom count and bathroom needs
- Must-have amenities or deal breakers
- Pets, guarantors, roommates, income requirements, elevator/laundry/doorman preferences, outdoor space, light, floor level, or work-from-home needs
- Tenant rep status
- Any `#tenantrep` tag
- Whether the lead is flexible on price, location, move date, or apartment type

If criteria are missing, state what is unknown and make conservative assumptions.

Do not invent hard facts about the lead.

### Use Only Active Inventory

Only recommend apartments that are active or currently available.

Exclude:

- Rented units
- Expired listings
- Unavailable units
- Units with unclear availability that cannot be reasonably treated as current
- Duplicate versions of the same apartment unless there is a meaningful difference

If a unit appears in the user's current instructions as rented, treat it as unavailable even if it appears elsewhere in older notes.

Important standing note: 19 South William St should be treated as rented unless the user gives newer contrary information.

### OP Requirement

Unless the lead is tagged `#tenantrep`, require an OP.

Rules:

- If the lead is not tagged `#tenantrep`, exclude units with no OP.
- If OP strength differs among similar matches, prefer stronger OPs.
- If OP data is missing, flag the uncertainty and do not treat the unit as a strong match unless the user explicitly allows it.
- If the lead is tagged `#tenantrep`, OP is not required, but still mention whether OP exists if known.

### Fit and Ranking Logic

Rank matches by overall fit, not just price.

Prioritize:

1. Must-have requirements
2. Budget fit
3. Neighborhood or commute fit
4. Move date and availability fit
5. Bedroom/bathroom fit
6. Amenity fit
7. OP strength, unless `#tenantrep`
8. Quality of listing/media, if relevant
9. Ease of showing or next action

Use common-sense rental judgment. A slightly more expensive apartment may rank above a cheaper one if it better matches the lead's must-haves, timing, or location.

When the match is uncertain, clearly label it as a backup, stretch, or conditional fit.

## Output Format

Use a concise, copy-ready structure Ric can act on quickly.

Default format:

```markdown
Lead Summary:
- Budget:
- Move Date:
- Neighborhoods:
- Beds/Baths:
- Must-Haves:
- Tenant Rep Status:
- Notes:

Best Matches:

1. Address #Apt — Price — Beds/Baths — OP
Why it works: [brief fit explanation]
Watch-out: [missing criteria, price stretch, availability issue, or tradeoff if any]
Action: [send, verify, tour, ask manager, hold as backup, etc.]

2. Address #Apt — Price — Beds/Baths — OP
Why it works:
Watch-out:
Action:

Backups / Conditional Fits:
- Address #Apt — [why it is a backup or conditional fit]

Exclude / Do Not Send:
- Address #Apt — [rented, expired, no OP, wrong budget, wrong neighborhood, unavailable, etc.]

Ric Copy:
[A short copy-ready note Ric can use internally or adapt for client follow-up.]
```

If the user asks specifically for a client-facing message, draft it separately after the match list and label it clearly.

## Ric Copy Style

Keep the Ric-facing summary practical, direct, and easy to paste.

Use:

- Short paragraphs
- Clear ranking
- Specific reasons
- Plain English
- No overexplaining
- No fake certainty

Avoid:

- Long market commentary unless requested
- Overly polished marketing language for internal notes
- Recommending unavailable units
- Treating missing OP as acceptable unless `#tenantrep`
- Saying "perfect" unless the unit clearly satisfies the lead's stated criteria

## Verification Standards

When using web or external inventory:

- Prefer Bond New York, current inventory sheets, StreetEasy, landlord sites, or user-provided availability
- Treat user-provided fresh inventory as higher priority than old conversation memory
- If facts conflict, explain the conflict and recommend verification before sending
- For high-stakes details like availability, concessions, OP, fees, and exact move-in date, say "verify before sending" if not directly confirmed

When no current inventory is provided, ask for inventory or permission to search current listings. Do not fabricate available apartments.

## Final Checks Before Responding

Before giving the final answer, confirm:

- The lead criteria were extracted
- Only active/current apartments are recommended
- Rented, expired, and unavailable units are excluded
- OP is required unless `#tenantrep`
- Similar units are ranked with stronger OPs favored
- Each recommended match has a brief reason
- The result is clean and copy-ready for Ric
