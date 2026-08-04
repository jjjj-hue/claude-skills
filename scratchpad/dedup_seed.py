import json, re
from datetime import datetime

FN = "/Users/luciaj/Claude/scratchpad/qualified-bank-LIVE.html"
text = open(FN).read()
s = text.index("const SEED = ") + len("const SEED = ")
start = text.index("[", s)
end = text.index("];const STORE_KEY")
data = json.loads(text[start:end+1])
print("total before:", len(data))

def norm_addr(addr):
    a = addr.lower()
    a = re.sub(r'\(.*?\)', '', a)
    a = re.sub(r'\*', '', a)
    a = re.sub(r'\bstreet\b|\bst\b', '', a)
    a = re.sub(r'\bavenue\b|\bave\b', '', a)
    a = re.sub(r'(\d+)(st|nd|rd|th)\b', r'\1', a)
    a = re.sub(r'[^a-z0-9]', '', a)
    return a
def norm_apt(apt):
    a = (apt or '').lower()
    a = re.sub(r'[^a-z0-9]', '', a)
    a = re.sub(r'^0+', '', a)
    return a

def confirmed_key(d):
    c = (d.get('confirmed') or '').strip()
    m = re.match(r'(\d+)/(\d+)', c)
    if m:
        mo, day = int(m.group(1)), int(m.group(2))
        return (mo, day)
    return (0, 0)

groups = {}
for i, d in enumerate(data):
    key = (norm_addr(d.get('address','')), norm_apt(d.get('apt','')))
    groups.setdefault(key, []).append((i, d))

MERGE_FIELDS = ['media','video','videoTour','floorplan','highlights','note','starred','picked']

survivors = []
merged_count = 0
sort_addr_map = {}

for key, items in groups.items():
    if len(items) == 1:
        idx, d = items[0]
        d['_sortAddr'] = norm_addr(d.get('address',''))
        survivors.append(d)
        continue
    # pick survivor: most recent confirmed date, prefer not-deleted, prefer non-empty priceNum
    items_sorted = sorted(items, key=lambda x: (
        confirmed_key(x[1]),
        0 if x[1].get('deleted') else 1,
        1 if x[1].get('priceNum') else 0,
    ), reverse=True)
    winner_idx, winner = items_sorted[0]
    for idx, d in items_sorted[1:]:
        for f in MERGE_FIELDS:
            wv = winner.get(f)
            dv = d.get(f)
            if not wv and dv:
                winner[f] = dv
            elif f == 'media' and isinstance(dv, list) and dv:
                existing = winner.get('media') or []
                winner['media'] = list({*existing, *dv}) if all(isinstance(x,str) for x in existing+dv) else existing
        merged_count += 1
    winner['_sortAddr'] = norm_addr(winner.get('address',''))
    survivors.append(winner)

print("merged away:", merged_count)
print("total after:", len(survivors))

# sort survivors by normalized address then apt so true dupes/near-dupes cluster, then strip helper key
survivors.sort(key=lambda d: (d['_sortAddr'], norm_apt(d.get('apt',''))))
for d in survivors:
    del d['_sortAddr']

new_arr_text = json.dumps(survivors, indent=2)
new_text = text[:start] + "\n" + new_arr_text + ";" + text[end+len("];"):]
open(FN, "w").write(new_text)
print("WRITTEN.")
