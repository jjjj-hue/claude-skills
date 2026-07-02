---
name: rics-listings-check
description: "Check Ric's LIVE StreetEasy active listings and flag what changed since the last check — new ads, dropped ads, price/unit changes, in-contract units. ONLY run when Lucia explicitly asks (e.g. 'check Ric's listings') — never run automatically or as a side effect of another task. Use before recommending any apartment, building a drip, or sending a blast that might touch Ric's inventory. Never trust a static/cached list — always pull live when asked."
---

# Ric's Listings — Live Check & Change Detection

**Trigger:** Only run this when Lucia explicitly asks for it. Do not run proactively, on a
schedule, or as a prerequisite step buried inside another task without asking first — it costs
credits (browser pull + possible per-listing drill-in) and Lucia wants to control when it fires.

**StreetEasy profile:** https://streeteasy.com/profile/845901-ric-salinas?tab_profile=active_listings

## Core rule
StreetEasy's "Active" tab (profile card view) only means the ad is still posted — it does NOT
mean the unit is truly available. Ric leaves ads up after a unit is rented or has an application
in progress, because inquiries still come in and get redirected. The profile card view has no
"In Contract" indicator — that only shows on the individual listing page. Keep this check light:
pull the card grid, diff it, and flag anything new/changed to Lucia. Only open an individual
listing page if Lucia specifically asks to confirm In Contract status on a particular unit —
don't drill into all listings by default, that's unnecessary overhead for a quick time-saver check.

## Status categories (Lucia/Ric define these — StreetEasy can't)
- **AVAILABLE** — truly open, safe to send/flip to leads
- **HAS AN APPLICATION** — ad still live, inquiries KEEP COMING IN → needs active FLIP/redirect messaging
- **RENTED (ad still live)** — ad still live, inquiries KEEP COMING IN → needs active FLIP/redirect messaging
- **FLIP** — never truly available even when first listed, ad still live → needs active FLIP/redirect messaging
- **IN CONTRACT** — ad is DOWN, no live leads coming in at all → just EXCLUDE from everything (blasts, automations, flip pools). No redirect messaging needed since there's no inbound to redirect.

Practically: everything that isn't confirmed AVAILABLE gets excluded from send-out blasts, but
only HAS APP / RENTED-still-live / FLIP need active flip/redirect handling in automations —
IN CONTRACT units generate zero live leads and should just be dropped from consideration entirely,
not treated as a flip target.

## Workflow

1. **Pull live** — browse the StreetEasy profile URL above, extract every active listing:
   address, unit, beds/baths, price, neighborhood. (Availability date and amenities aren't
   on the profile card — only pull those from the individual listing page if specifically needed.)

2. **Diff against the last saved snapshot** (`ric_listings_snapshot.md` in this skill folder):
   - **NEW** — address/unit combo appears now but wasn't in the last snapshot → flag as new ad, ask Lucia for status (available / has app / rented)
   - **DROPPED** — was in last snapshot, no longer active → flag as likely rented, in contract, or pulled — ask Lucia to confirm, don't just assume rented
   - **CHANGED** — same address/unit, different price → flag the old vs new price
   - **UNCHANGED** — carry forward its last known status (available/app/rented/flip) from the snapshot

3. **Output a change report first**, before anything else:
   ```
   RIC'S LISTINGS — CHECKED [date]

   NEW ADS (confirm status):
   - [address/unit] — [beds] — $[price] — ?

   DROPPED (confirm — rented / in contract / pulled?):
   - [address/unit] — was $[price]

   PRICE CHANGES:
   - [address/unit]: $[old] → $[new]

   UNCHANGED — carried forward status:
   - [count] available, [count] flip/app/rented
   ```

4. **Ask Lucia to tag any NEW or ambiguous listing** as Available / Has App / Rented / Flip.
   Never guess — if unconfirmed, default-treat as FLIP (safer than accidentally sending a
   dead unit to a lead).

5. **Update the snapshot file** with the new full list + confirmed statuses so next check
   has an accurate baseline to diff against.

## Output for downstream use (email-blast, tenant-rep-blast, draft-fub-sequence)
- **AVAILABLE** → send-out pool
- **HAS APP / RENTED-still-live / FLIP** → "redirect inquiries here" pool (active flip messaging needed — leads are still coming in on these)
- **IN CONTRACT** → excluded entirely, not part of any pool — ad is down, no live leads, nothing to redirect
