import json, re, copy

FN = "/Users/luciaj/Claude/scratchpad/qualified-bank-LIVE.html"

text = open(FN).read()
start_marker = "const SEED = ["
start = text.index(start_marker) + len("const SEED = ")
end = text.index("\nconst STORE_KEY")
arr_text = text[start:end].strip()
assert arr_text.endswith(";")
arr_text = arr_text[:-1]
cleaned = re.sub(r",(\s*[\]}])", r"\1", arr_text)
data = json.loads(cleaned)
print("total entries:", len(data))

def norm(addr):
    a = addr.lower()
    a = re.sub(r'\(.*?\)', '', a)
    a = re.sub(r'#', '', a)
    a = re.sub(r'\bstreet\b|\bst\b', '', a)
    a = re.sub(r'\bavenue\b|\bave\b', 'ave', a)
    a = re.sub(r'(\d+)(st|nd|rd|th)\b', r'\1', a)
    a = re.sub(r'[^a-z0-9]', '', a)
    return a

def normapt(apt):
    a = apt.lower()
    a = re.sub(r'[^a-z0-9]', '', a)
    a = re.sub(r'^0+', '', a)
    return a

def is_solil(d):
    s = (d.get('source','') or '') + (d.get('note','') or '')
    return 'solil' in s.lower()

solil = [d for d in data if is_solil(d)]
print("solil entries:", len(solil))

def find(addr, apt):
    na, nap = norm(addr), normapt(apt)
    matches = [d for d in solil if norm(d['address'])==na and normapt(d['apt'])==nap]
    return matches

def set_status(d, status):
    status_l = status.lower()
    b = d['badges']
    b['app'] = False
    b['rented'] = False
    if 'rented' in status_l:
        b['rented'] = True
        b['op'] = False if 'op' in b else b.get('op', False)
    elif 'app' in status_l:
        b['app'] = True
    d['note'] = status if status else d.get('note','')

MISSES = []

# ---------------- CHANGED ----------------
changed = [
    ("71 West 12th St","4H", dict(note="app approved but might back out")),
    ("20 Fifth Ave","1E", dict(note="app approved")),
    ("20 Fifth Ave","2B", dict(priceNum=8600, priceDisp="$8,600/mo", note="price drop")),
    ("96 Fifth Ave","3H", dict(avail="vacant")),
    ("96 Fifth Ave","5N", dict(avail="vacant")),
    ("96 Fifth Ave","8P", dict(avail="vacant")),
    ("96 Fifth Ave","11L", dict(note="rented", status="rented")),
    ("145 East 16th St","15H", dict(note="RENTED", status="rented", avail="")),
    ("235 West 22nd St","2Y", dict(note="now 1+1")),
    ("165 East 35th St","3C", dict(note="now 1+1")),
    ("165 East 35th St","5H", dict(note="now 1+1")),
    ("140 East 46th St","4A", dict(note="", avail="09/01/26 still occupied")),
    ("140 East 46th St","6M", dict(note="rented", status="rented")),
    ("140 East 46th St","7K", dict(note="rented", status="rented")),
    ("140 East 46th St","7R", dict(note="rented", status="rented")),
    ("140 East 46th St","9H", dict(note="APP APPROVED", status="app")),
    ("140 East 46th St","11K", dict(note="APP", status="app")),
    ("300 East 49th St","1B", dict(note="rented", status="rented")),
    ("145 West 55th St","6E", dict(note="app approved", status="app")),
    ("145 West 55th St","7A", dict(note="app approved", status="app")),
    ("145 West 55th St","14C", dict(avail="vacant")),
    ("405 East 56th St","9L", dict(note="alcove studio? (size unconfirmed)")),
    ("405 East 56th St","10M", dict(note="APP", status="app")),
    ("401 East 58th St","B8", dict(avail="vacant")),
    ("157 East 57th St","16A", dict(note="")),
    ("219 East 69th St","9F", dict(note="app approved but might back out")),
    ("219 East 69th St","10D", dict(note="app approved but might back out", avail="vacant")),
    ("219 East 69th St","10HJ", dict(note="app approved but might back out")),
    ("147 East 72nd St","5F", dict(avail="vacant")),
    ("166 West 72nd St","3C", dict(note="APP", status="app", avail="vacant")),
    ("166 West 72nd St","8D", dict(note="RENTED", status="rented", avail="")),
    ("160 West 73rd St","6E", dict(avail="vacant")),
    ("160 West 73rd St","7K", dict(note="")),
    ("1043 Lexington Ave","4R", dict(note="rented", status="rented")),
    ("1427 York Ave","2B", dict(note="very negotiable")),
    ("1427 York Ave","0E", dict(avail="vacant")),
    ("240 East 82nd St","2K", dict(priceNum=5600, priceDisp="$5,600/mo", note="price drop")),
    ("240 East 82nd St","20F", dict(note="tenant not responding")),
    ("401 East 88th St","15D", dict(avail="vacant")),
    ("222 East 89th St","3", dict(priceNum=4000, priceDisp="$4,000 very negotiable", note="with PATIO!")),
    ("150 Remsen St","22", dict(note="RENTED", status="rented", avail="")),
    ("80 Cranberry St","6G", dict(avail="")),
    ("161 East 55th St","2C", dict(avail="vacant")),
    ("151 East 71st St","304", dict()),  # no real change, just addr format
]

for addr, apt, fields in changed:
    m = find(addr, apt)
    if not m:
        MISSES.append(("CHANGED", addr, apt))
        continue
    for d in m:
        status = fields.pop('status', None)
        for k,v in fields.items():
            d[k] = v
        if status:
            set_status(d, fields.get('note', d.get('note','')))
        d['confirmed'] = '8/1'
        if 'SOLIL_UPDATE_7:24' in (d.get('source') or ''):
            d['source'] = '8-1_Solil_UPDATE.pdf'
        elif d.get('source') == 'Solil':
            d['source'] = 'Solil'  # generic tag, leave as-is

# ---------------- REMOVED (mark deleted) ----------------
removed = [
    ("151 Mott St","18"),
    ("71 West 12th St","2F"),
    ("20 Fifth Ave","8E"),
    ("20 Fifth Ave","10D"),
    ("20 Fifth Ave","12A"),
    ("145 East 16th St","4G"),
    ("145 East 16th St","17H"),
    ("235 West 22nd St","7C"),
    ("517 Third Ave","8"),
    ("140 East 46th St","3D"),
    ("20 Beekman Place","3A"),
    ("20 Beekman Place","3F"),
    ("405 East 56th St","3D"),
    ("405 East 56th St","10B"),
    ("219 East 69th St","PHA"),
    ("1427 York Ave","2E"),
    ("106 East 81st St","5C"),
    ("150 Remsen St","6"),
    ("150 Remsen St","66"),
]
for addr, apt in removed:
    m = find(addr, apt)
    if not m:
        MISSES.append(("REMOVED", addr, apt))
        continue
    for d in m:
        d['deleted'] = True
        d['note'] = (d.get('note') or '')
        d['confirmed'] = '8/1'

# ---------------- ADDED (new units) ----------------
template = solil[0]
def new_entry(address, apt, beds, priceNum, priceDisp, avail, note, status=None):
    d = copy.deepcopy(template)
    d['id'] = f"solil_{norm(address)}_{normapt(apt)}"
    d['address'] = address
    d['apt'] = apt
    d['beds'] = beds
    d['priceNum'] = priceNum
    d['priceDisp'] = priceDisp
    d['avail'] = avail
    d['source'] = '8-1_Solil_UPDATE.pdf'
    d['confirmed'] = '8/1'
    d['note'] = note
    for k in d['badges']:
        d['badges'][k] = False
    d['badges']['op'] = True
    if status:
        set_status(d, status)
    d['deleted'] = False
    d['starred'] = False
    d['picked'] = False
    d['highlights'] = ""
    d['media'] = []
    d['video'] = ""
    d['floorplan'] = ""
    d['bath'] = ""
    d['pick1'] = False
    d['pick2'] = False
    d['pick3'] = False
    d['videoTour'] = ""
    return d

added = [
    new_entry("266 Bleecker St","20304","2","13000","$13,000/mo","8/3/26","2BR/2BTH with Terrace and W/D"),
    new_entry("307 Mott St","3A","1","4600","$4,600/mo","vacant","APP"),
    new_entry("20 Fifth Ave","9B","1","9200","$9,200/mo","vacant",""),
    new_entry("20 Fifth Ave","14A","1","9200","$9,200/mo","10/1/26","1BR with W/D"),
    new_entry("145 East 16th St","5F","studio","4800","$4,800/mo","09/01/26",""),
    new_entry("235 West 22nd St","7J","1","5500","$5,500/mo","vacant","app approved"),
    new_entry("165 East 35th St","10C","studio","4100","$4,100/mo","10/01/26","studio with balcony"),
    new_entry("165 East 35th St","11H","studio","4100","$4,100/mo","09/01/26","studio with balcony"),
    new_entry("156 East 37th St","1C","1","5000","$5,000/mo","8/3/26","APPS"),
    new_entry("137 East 38th St","2A","2","8000","$8,000/mo","vacant",""),
    new_entry("137 East 38th St","2D","studio","4300","$4,300/mo","vacant","alcove studio"),
    new_entry("987 First Ave (54th)","3R","1","4300","$4,300/mo","vacant","1BR with Terrace"),
    new_entry("159 East 55th St","4A","studio","4100","$4,100/mo","10/1/26","alcove studio"),
    new_entry("160 East 55th St","7F","studio","4100","$4,100/mo","10/1/26",""),
    new_entry("161 East 55th St","2C_new_dup","studio","4050","$4,050/mo","vacant","DUPLICATE_SKIP"),
    new_entry("162 East 55th St","5C","1","4200","$4,200/mo","8/3/26 (unconfirmed)",""),
    new_entry("405 East 56th St","2E","1","5000","$5,000/mo","9/1/26","1BR easy flex 2"),
    new_entry("405 East 56th St","9LA","studio","4400","$4,400/mo","10/1/26","alcove studio"),
    new_entry("1075 First Ave (58-59)","3A","1","4250","$4,250/mo","09/01/26","1BR easy flex 2"),
    new_entry("157 East 57th St","3A","2","8400","$8,400/mo","9/1/26","2BR/2BTH with D/A"),
    new_entry("157 East 57th St","12E","studio","4600","$4,600/mo","vacant","alcove studio"),
    new_entry("157 East 57th St","17C","1","6200","$6,200/mo","vacant",""),
    new_entry("25 West 68th St","3F","2","10100","$10,100/mo","8/28/26","2BR/2BTH with D/A and W/D"),
    new_entry("219 East 69th St","12L","1","5900","$5,900/mo","8/24/26",""),
    new_entry("166 West 72nd St","9D","1","5900","$5,900/mo","9/1/26","APP"),
    new_entry("160 West 73rd St","1F","1","5300","$5,300/mo","vacant",""),
    new_entry("160 West 73rd St","8K","studio","3850","$3,850/mo","10/01/26",""),
    new_entry("160 West 73rd St","10E","studio","4000","$4,000/mo","09/01/26",""),
    new_entry("1427 York Ave","2C","2","4650","$4,650/mo","vacant","RENTED", status="rented"),
    new_entry("24 East 80th St (elevator bldg)","5A","1","4800","$4,800/mo","09/01/26",""),
    new_entry("240 East 82nd St","10K","1","6000","$6,000/mo","09/01/26","1BR easy flex 2 with Balcony"),
    new_entry("167 East 87th St","2RW","1","4300","$4,300/mo","9/1/26",""),
    new_entry("222 East 89th St","16","1","4200","$4,200/mo","vacant",""),
]
# drop the deliberate duplicate placeholder (161 E55 2C already exists & handled in CHANGED)
added = [a for a in added if a['note'] != 'DUPLICATE_SKIP']

data.extend(added)

print("MISSES:", MISSES)
print("added count:", len(added))

# ---------------- serialize back ----------------
new_arr_text = json.dumps(data, indent=2)
new_text = text[:start] + "\n" + new_arr_text + ";" + text[end+1:]
# bump store key version
new_text = new_text.replace('const STORE_KEY = "qualifiedBankOP_v1"', 'const STORE_KEY = "qualifiedBankOP_v2"')

open(FN, "w").write(new_text)
print("WRITTEN. new size:", len(new_text))
