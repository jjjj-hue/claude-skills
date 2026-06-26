---
name: bentley-pull
description: >
  Light-token Bentley listing extractor for Bond New York / Lucia.
  Use when Lucia says "pull Bentley", "grab Bentley listings", "get Bentley for [criteria]",
  "refresh Bentley", "what's on Bentley for [beds/price/neighborhood]", or any time live
  Bentley inventory is needed without a full session. Navigates directly to the results page
  via a single GET URL, then extracts all listings in one JS pass. No screenshots, no form
  clicking, no page-by-page navigation.
---

# Bentley Pull — Light-Token Extractor

One navigate → one JS extract. No screenshots unless something breaks.

---

## How Bentley works (internal)

Bentley is a frameset ColdFusion app at `bondnewyork.com/admin2/`. The actual results page
is `listings_browser.cfm` and accepts ALL filters as GET parameters — no POST, no form
interaction needed. Navigate directly to a constructed URL and extract.

---

## Step 1 — Build the URL from Lucia's criteria

Base URL:
```
https://www.bondnewyork.com/admin2/listings_browser.cfm?page=listings&filterStatus=2&filterType=-1&filterContact=-1&filterBuilding=-1&filterDistribution1=-1&filterAmenities=-1&filterPets=-1&filterCategory=-1&filterBath=0,99&filterkeys=-1&filterparking=-1&filterWallsOK=-1&filterSharesOK=-1&filterViews=-1&filterCommercial=-1&filterEra=-1&filterCondition=-1&filterOffice=-1&filterGuarantor=-1&filterDown=0&filterMaint=0&filterCC=0&filterTax=0&filterPriceChange=0&filterSqft=0&filterPPSQFT=0&filterparkingFee=-1&searchStr=&sort=date_listed&order=-1&StartAt=1
```

Set these params based on Lucia's request:

| Criteria | Param | Format |
|----------|-------|--------|
| Status | `filterStatus` | `2` = For Rent (always use this) |
| Area | `filterArea` | See area codes below; `-1` = all |
| Min price | `filterPrice` | `0,999999999999` = no limit; `0,5500` = max $5,500 |
| Max price | (same param) | `filterPrice=3000,6000` for range |
| Fee type | `filterFee` | `OP` = owner pays; `All` = all; `FULL` = full fee |
| Available | `filterDate` | `-9999` = all; `NOW` = immediate; `occDate/7/1/2026` = Jul 1+ |
| Database | `filterDistribution` | `0,-2` = Internal (always use this) |
| Beds (server-side unreliable) | `filterSpace` | `2` = 2BR min — apply client-side filter too |

**Note:** `filterSpace` param does not reliably filter server-side. Always apply a client-side
bed count filter in the extraction JS (Step 3).

### Area codes (key neighborhoods):

| Neighborhood | Code | Neighborhood | Code |
|---|---|---|---|
| All | -1 | East Village | 9 |
| Upper East Side | 2 | Lower East Side | 25 |
| Upper West Side | 1 | SoHo | 10 |
| Midtown West | 3 | Tribeca | 16 |
| Midtown East | 4 | Chelsea | 6 |
| Hell's Kitchen | 180 | West Village / GV | 8 |
| Gramercy | 5 | Financial District | 17 |
| Murray Hill | 24 | Kips Bay | 194 |
| Flatiron | 7 | NoHo | 28 |
| East Side (parent) | 163 | Downtown (parent) | 166 |
| Midtown (parent) | 165 | West Side (parent) | 164 |

For multiple neighborhoods: run separate extractions and combine, or use the parent group code.

---

## Step 2 — Navigate

Use Kapture (or any available browser tool):

```
navigate → [constructed URL]
```

No screenshots needed — just confirm `domSize > 50000` to know results loaded.
If domSize is small (~2000), Bentley redirected to the frameset login page — tell Lucia to log in.

---

## Step 3 — Extract with one JS pass

Run this via `mcp__kapture__evaluate`:

```javascript
(function(minBeds, maxPrice, minPrice) {
  const results = [];
  
  // Each listing is a <tr> with 30+ cells and contains a price pattern
  const rows = Array.from(document.querySelectorAll('tr')).filter(r => {
    const cells = r.querySelectorAll('td');
    return cells.length > 20 && /\$[\d,]+/.test(r.textContent);
  });

  rows.forEach(row => {
    const c = row.querySelectorAll('td');
    const price = parseInt((c[15]?.textContent.trim() || '0').replace(/[\$,]/g, '')) || 0;
    const beds  = parseInt(c[13]?.textContent.trim()) || 0;

    // Client-side filters
    if (minBeds > 0 && beds < minBeds) return;
    if (maxPrice > 0 && price > maxPrice) return;
    if (minPrice > 0 && price < minPrice) return;

    const matterport = row.querySelector('a[href*="matterport"]');
    const video = row.querySelector('a[href*="youtube"], a[href*="youtu.be"], a[href*="vimeo"]');

    results.push({
      id:        c[1]?.textContent.trim(),
      landlord:  c[8]?.textContent.trim(),
      area:      c[9]?.textContent.trim(),
      address:   (c[10]?.textContent.trim()||'') + ' ' + (c[11]?.textContent.trim()||''),
      apt:       c[12]?.textContent.trim(),
      beds:      beds,
      baths:     c[14]?.textContent.trim(),
      price:     price,
      priceStr:  c[15]?.textContent.trim(),
      avail:     c[16]?.textContent.trim(),
      fee:       c[21]?.textContent.trim(),   // NONE / OP / FULL / COB / CYOF
      notes:     c[25]?.textContent.trim(),   // concessions, specials
      walls:     c[28]?.textContent.trim(),   // flex wall policy
      matterport: matterport?.href || null,
      video:     video?.href || null
    });
  });

  // Get total count from page header
  const countEl = document.querySelector('.listCount, [class*="count"]');
  const header  = document.body.innerText.match(/(\d[\d,]+)\s*Listings?/i);
  
  return JSON.stringify({
    count: results.length,
    total: header ? header[1] : '?',
    listings: results
  });
})(MIN_BEDS, MAX_PRICE, MIN_PRICE)
```

Replace `MIN_BEDS`, `MAX_PRICE`, `MIN_PRICE` with numeric values (0 = no filter):
- `(2, 6000, 0)` = 2BR+, max $6,000
- `(0, 5500, 3500)` = any beds, $3,500–$5,500
- `(1, 0, 0)` = 1BR+, no price filter

---

## Step 4 — Format output

From the JSON, produce a clean table. Default sort: by price ascending.

**Output format:**
```
BENTLEY — [criteria] — [date]
[N listings extracted] / [total on page]

Address Apt X · Beds/Bath · $Price/mo · Avail · Landlord · [Walls: X] · [Media]

...

OP: N units | TRPA/fee: N units
```

**Fee interpretation:**
- `NONE` or `OP` → owner pays (OP blast eligible)
- `FULL`, `COB`, `CYOF` → tenant pays fee (not OP)
- `TRPA`-named companies (Margules, Village Dwellings) → always TRPA regardless of fee field

**Walls field (flex indicator):**
- `Pressurized Walls OK` → true flex 2BR eligible
- `Bookcase Walls` → NOT true flex
- `Case by case` → confirm with landlord before listing as flex
- `Yes` / `Allowed` → flex eligible

Strip from client output: `id`, `fee` column (internal), `notes` if contains access codes.
Keep `notes` if it contains concessions (e.g. "1 month free", "$500 deposit special").

---

## Step 5 — Pagination (if needed)

The page shows 100 listings per page. If `total` > 100 and Lucia wants all:
1. Change `StartAt=101` in the URL, re-navigate, re-run extraction
2. Combine results, deduplicate by `id`
3. Repeat until `StartAt > total`

Cap at 300 listings (3 pages) without asking. More than that → confirm with Lucia.

---

## Segment routing (when asked)

After extracting, if Lucia says "segment these" or "which leads get these":
- Studio <$3.5k → OP blast
- 1BR $4k–$5.5k → OP blast
- 2BR $5k–$7k → OP blast
- 2BR $7k+ → targeted
- 3BR+ → targeted
- TRPA/fee landlords → never blast to OP lead pool

---

## Failure modes

| Problem | Fix |
|---------|-----|
| domSize ~2000 after navigate | Session expired — tell Lucia to log in at bondnewyork.com/admin2/ |
| `count: 0` from JS | filterPrice too tight or no 2BR+ available; loosen criteria and re-run |
| Beds showing 0 unexpectedly | Studio listed as 0 beds; adjust minBeds filter |
| Price = 0 for some rows | CF formatting issue — check `c[15]` raw text; may need different cell index |

---

## Token budget

Target: 1 navigate + 1 evaluate = ~500 tokens total.
No screenshots unless extraction fails after 2 attempts.
If broken after 2 tries → fall back to `/bentley-import` for full browser session.
