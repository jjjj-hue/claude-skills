---
name: email-blast
description: >
  Lucia's apartment email and text blast generator for Bond New York / Follow Up Boss.
  Use whenever Lucia provides apartment listings in ANY format — pasted notes, Bentley PDF,
  Excel sheet, Bond listing report, URL list, or raw scratchpad text — and needs a FUB-ready
  email or text blast. Trigger on: "blast this", "make the email", "generate the FUB email",
  "email for [building/criteria]", "pull studios and 1-beds", "filter for [criteria] and make
  the email", "write the HTML email", "draft a text for these", "turn this listing report into
  an email", "PDF availability email", or any time listings appear and output goes into FUB.
  Always use this skill when output goes into FUB's HTML template editor or text template editor.
---

# Email & Text Blast — Bond New York / Lucia

Two-step workflow: plain text first → HTML after approval. Never skip to HTML on the first response.

## Media mode flag

- Default (no flag): **skip media pull entirely** — output listings fast, no YouTube/Matterport/SE photo search
- `/email-blast media` or "blast with media": **run full media pull** (Steps 3a–3c: Jessie YouTube → Matterport → SE photos)
- If Lucia says "no media", "skip media", "just listings", or "fast" → default mode
- If Lucia says "with media", "pull media", "include tours", "add photos" → media mode

In default mode: omit Tour/Photo lines entirely from output. Do not note their absence per listing.

---

## Step 1 — Parse the input

### A. Pasted notes / scratchpad (most common)
- Extract: address, unit, beds/baths, sq ft (if listed), price, avail date, amenities, media link
- Strip from client output: lockbox codes, key instructions, "NOT ON SE", "MGM Master", "Key plus", agent-only access notes
- Never fabricate missing fields. Note in summary if price or address is missing.

### B. Bentley / RealtyMX PDF export
- Columns: listing ID, DOM, OP%, type, neighborhood, address, unit, beds, baths, price, avail date, mgmt company, access instructions
- Access instructions = internal only, strip from client output

### C. Excel sheet (MASTER UPDATE, GPG, BLDG, SOLIL, Village Dwellings, etc.)
- Use openpyxl for hyperlink extraction (pandas misses .hyperlink.target)
- See sheet-by-sheet guide at bottom

### D. Bond-generated Listing Report PDF
- Header: "Listing Report Prepared Especially For: [Agent]"
- Parse: address, apt, beds/baths, sqft, price, doorman, DOM
- No tour links in these — check BOND Matterport Library for matches

### E. Website / management URL list
- Use web_fetch on each URL
- If JS-heavy or login-required, note "check directly" — never fabricate units

---

## Step 2 — Filter

- **Include**: available, blank status, status = A
- **Exclude silently**: HOLD (any case), rented, OOS, no access flagged — note in summary
- **Exclude always**: 51 Leroy St #1D · 3 W 103rd St · 40 Ave B #3W · 166 Second Ave
- **Centennial**: non-Centennial options first — include Centennial only if no other viable match
- Show gross rent always. Concession inline (e.g. "1 month free"). Never NE price.
- Preserve original order unless Lucia asks to re-sort.

---

## Step 3 — Pull media for each listing *(media mode only — skip entirely in default mode)*

**Priority order — stop at first hit:**

### 1. Jessie's YouTube (check FIRST)
`https://www.youtube.com/@jessieoriolhuaman/search?query=[street+number+keywords]`

```javascript
Array.from(document.querySelectorAll('a[href*="/watch"]')).map(a => ({
  href: 'https://www.youtube.com' + a.getAttribute('href').split('&')[0],
  title: (a.querySelector('#video-title') || a).getAttribute('title') || a.textContent.trim().slice(0,80)
})).filter(v => v.title)
```

Confirm match by address/unit in title. If confident → use as Video Tour. Try multiple search terms if 0 results (street number, unit, neighborhood).

### 2. Matterport
StreetEasy: `https://streeteasy.com/building/[address-slug-new_york]/[unit]`

```javascript
Array.from(document.querySelectorAll('a[href*="matterport"], iframe[src*="matterport"]')).map(e => e.href || e.src)
```

### 3. StreetEasy Photos (up to 6)
```javascript
Array.from(document.querySelectorAll('img[src*="zillowstatic"]'))
  .map(i => i.src.replace(/-p_[a-z]\.webp$/, '-se_large_800_400.webp'))
  .filter((v,i,a) => a.indexOf(v) === i).slice(0,6)
```

If none found: "Photos available upon request" in grey text.

---

## Step 4 — Plain text output (ALWAYS FIRST)

Format per line:
```
Address Apt X – X BR / Y BA – $Price/mo | Avail Date | highlight1, highlight2, highlight3 — [Tour label]: URL
```

Rules:
- `Apt X` not `#X`
- En dash between major fields, pipe before highlights
- 2–3 lowercase highlights only — no caps, no neighborhood label per line. Pick standout features: dishwasher, elevator, doorman, W/D in unit, central A/C, fireplace, outdoor space, renovated kitchen, 2 baths. Never use "hardwood floors" (too standard) or "stainless steel appliances" (expected) as highlights.
- Gross rent only. Concession inline.
- Tour: raw URL after label. Omit entirely if no media found.
- No section headers, no sign-off, no greeting

Summary line below listings:
```
X listings included. Excluded: [unit] — [reason]. Internal notes: [stripped access info].
```

End with: "Let me know if anything needs to change and I'll generate the HTML."

---

## Step 5 — HTML output (after approval only)

**Rules:**
- All CSS inline — FUB strips `<style>` blocks
- No `<img>` tags — photos as `Photo 1 · Photo 2 · ...` clickable text links only
- No `<hr>` dividers, no tables, no buttons
- `&ndash;` for en dashes — never literal –
- `&middot;` between photo links
- `&rsquo;` for apostrophes in CTA
- Max-width 600px, Arial 14px #000
- `<meta charset="UTF-8">` in head
- Sort by price ascending unless Lucia says otherwise

**Listing block:**
```html
<p style="margin:0 0 6px 0;"><strong><span style="color:#000000;text-decoration:none;">[Address] Apt [Unit]</span></strong> &ndash; [X BR / Y BA] &ndash; $[price]/mo | [Avail] | [highlight1, highlight2, highlight3]</p>
<p style="margin:0 0 16px 0;font-size:13px;">[media]</p>
```

**HTML scaffold:**
```html
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#ffffff;font-family:Arial,sans-serif;font-size:14px;color:#000000;">

<p style="margin:0 0 16px 0;">Hi %contact_first_name%,</p>

<p style="margin:0 0 16px 0;">[intro]</p>

[listing blocks]

<p style="margin:24px 0 16px 0;">[CTA]</p>

<p style="margin:0;">Ric<br>%agent_phone%</p>

</body>
</html>
```

**NEVER include in footer:**
- "Reply or call/text to schedule a showing."
- "Approval based on gross rent, not net effective."

---

## Step 6 — Text version (after HTML, unless Lucia says skip)

Cap at 5 listings. Raw URLs on their own line. ≤320 chars per message block.

---

## Step 7 — Channel routing

- FUB blast (StreetEasy/Zillow leads) → signed as Ric
- Direct text to 917-923-7380 → signed as Lucia
- Default to Ric unless told otherwise

---

## Never do these

1. Output HTML before plain text review
2. `<style>` blocks — FUB strips them
3. Literal en dashes in HTML — always `&ndash;`
4. Raw URLs in HTML body — always wrapped as linked text
5. Include HOLD/no-access units in client output
6. Show NE rent instead of gross
7. Re-sort when not asked
8. Add sign-off / agent block — FUB handles it
9. "Tour coming soon" — if no link, omit
10. Section date headers — avail date goes inline
11. Include lockbox codes or access instructions in client output
12. `<img>` tags — text links only
13. `<hr>` dividers
14. Unit as #X — always Apt X
15. Footer lines: "Reply or call/text..." or "Approval based on gross rent..."
