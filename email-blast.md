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

## Step 3 — Pull media for each listing

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

**Media link formats:**
- Video: `<a href="URL" target="_blank" style="color:#0066cc;text-decoration:underline;">Video Tour</a>`
- 3D Tour: `<a href="URL" target="_blank" style="color:#0066cc;text-decoration:underline;">3D Tour</a>`
- Photos: `<a href="URL" target="_blank" style="color:#0066cc;text-decoration:underline;">Photo 1</a> &middot; <a ...>Photo 2</a> ...`
- None: `<span style="color:#666666;">Photos available upon request</span>`

**HTML scaffold:**
```html
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#ffffff;font-family:Arial,sans-serif;font-size:14px;color:#000000;">

<p style="margin:0 0 16px 0;">Hi %contact_first_name%,</p>

<p style="margin:0 0 16px 0;">[intro — rotate each blast, never reuse the same line. Examples: "Here are some no-fee options in [area] that are available now." / "Pulled a few no-fee places in [area] that just hit." / "Got some good no-fee options in [area] — all available soon." / "Here's what's available no-fee in [area] right now." / "A few no-fee spots in [area] worth a look."]</p>

[listing blocks]

<p style="margin:24px 0 16px 0;">[CTA — rotate each blast, never reuse the same line. Examples: "Anything jump out? Just reply and I&rsquo;ll get the showing on the calendar." / "See something you like? I can usually get you in same or next day." / "Any of these feel right? Drop me a reply and I&rsquo;ll lock it in." / "Like what you see? A quick reply is all it takes &mdash; I&rsquo;ll handle the rest." / "Something catch your eye? Reply and I&rsquo;ll get you in." / "Interested in any of these? I can usually schedule a showing same or next day."]</p>

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

```
Hi %contact_first_name%! [1-line hook]:

68 East 1st St, Apt 6C – 2 BR / 1 BA – $5,895 | Avail Now | elevator, FD
https://my.matterport.com/show/?m=UoToGZRiSxx

Interested in any?
%agent_first_name% | Bond NY | %agent_phone%
```

---

## Step 7 — Channel routing

- FUB blast (StreetEasy/Zillow leads) → signed as Ric
- Direct text to 917-923-7380 → signed as Lucia
- Default to Ric unless told otherwise

---

## Step 8 — File naming (only if Lucia asks to save)

HTML: `FUB Email – [Criteria] – [MM-DD-YY].html`
Text: `FUB Text – [Criteria] – [MM-DD-YY].txt`
Save to `/Users/luciaj/Claude/Projects/FUB & Tools/` by default.

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

---

## Excel Sheet-by-Sheet Guide

### GPG / GPG Occupied
Columns: STATUS, APP DATE, BROKER, DATE ADDED, MATTERPORT, ADDRESS, APT, SIZE, LIST RENT, CONCESSION, NET RENT, LEASE TYPE, COMMENTS, STREETEASY AGENT, OLD RENT
- Show LIST RENT (gross); note concession inline. Include COMMENTS if non-empty.

### BLDG (~60 buildings)
Structure: building header rows + unit rows. Columns: Unit#, Matterport, 1yr rent, 2yr rent, Size, Available, Access
- Show both 1-yr and 2-yr pricing.

### SOLIL
Columns: ADDRESS, APT, STATUS, SIZE, RENT, VAC DATE, ACCESS

### Village Dwellings
Columns: STATUS, APP DATE, BROKER, DATE ADDED, ADDRESS, APT, SIZE, LIST RENT, CONCESSION, TENANT REP TERMS, NER, MOVE IN DATE, MATTERPORT, FD CODE
- Show LIST RENT; include concession + move-in date.

### CENTENNIAL
Organized by neighborhood. Use only if no non-Centennial options match.

### Margules
Show ASKING RENT (not NER).

### Brusco
Always include DESCRIPTION column.

### Mango (301 E 38th St)
Show GROSS RENT.

### Penmark
Columns: ADDRESS, APT, LOCATION, SIZE, STATUS, PETS, TYPE, RENT, AVAIL, ACCESS

---

## Technical notes

- openpyxl for Excel hyperlinks; pandas for filtering
- openpyxl rows 1-indexed; pandas 0-indexed
- pdfplumber first for PDFs; pypdf as fallback
- web_fetch for URL list inputs
- Master Update cross-reference: 1uVwSvajr1ISm7aonriUa3nGWc_gb6dTtgmx9y-ryvGg
