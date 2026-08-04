import json, re, copy

FN = "/Users/luciaj/Claude/scratchpad/qualified-bank-LIVE.html"
text = open(FN).read()
s = text.index("const SEED = ") + len("const SEED = ")
start = text.index("[", s)
end = text.index("];const STORE_KEY")
data = json.loads(text[start:end+1])
print("total before:", len(data))

def norm(addr):
    a = addr.lower()
    a = re.sub(r'\*', '', a)
    a = re.sub(r'\(.*?\)', '', a)
    a = re.sub(r'\bstreet\b|\bst\b', '', a)
    a = re.sub(r'\bavenue\b|\bave\b', '', a)
    a = re.sub(r'(\d+)(st|nd|rd|th)\b', r'\1', a)
    a = re.sub(r'[^a-z0-9]', '', a)
    return a
def normapt(apt):
    a = apt.lower(); a = re.sub(r'[^a-z0-9]','',a); return a

def is_brusco(d):
    s = (d.get('source','') or '') + ' ' + (d.get('mgmt','') or '')
    return 'brusco' in s.lower()

brusco = [d for d in data if is_brusco(d)]
print("brusco entries found:", len(brusco))

def find(addr, apt):
    na, nap = norm(addr), normapt(apt)
    return [d for d in brusco if norm(d['address'])==na and normapt(d['apt'])==nap]

# price/date updates confirmed by 8/1 Brusco sheet (all still active OP units)
changed = [
    ("107 West 69th St","1B", 3790, "$3,790/mo"),
    ("491 Columbus Ave","4R", 5350, "$5,350/mo"),
    ("308 West 73rd St","1B", 5295, "$5,295/mo"),
    ("162 West 80th St","5G", 5775, "$5,775/mo"),
    ("39 West 68th St","PHB", 5700, "$5,700/mo"),
]
MISSES = []
for addr, apt, priceNum, priceDisp in changed:
    m = find(addr, apt)
    if not m:
        MISSES.append((addr, apt))
        continue
    for d in m:
        d['priceNum'] = priceNum
        d['priceDisp'] = priceDisp
        d['confirmed'] = '8/1'
        d['avail'] = 'IMM'
print("MISSES:", MISSES)

# genuinely new units on 8/1 sheet, never tracked before
template = brusco[0]
def new_entry(address, apt, beds, priceNum, priceDisp, note):
    d = copy.deepcopy(template)
    d['id'] = f"brusco_{norm(address)}_{normapt(apt)}"
    d['address'] = address
    d['apt'] = apt
    d['beds'] = beds
    d['priceNum'] = priceNum
    d['priceDisp'] = priceDisp
    d['avail'] = 'IMM'
    d['source'] = '8-1_Brusco_UPDATE.xls'
    d['confirmed'] = '8/1'
    d['flag'] = 'good'
    d['note'] = note
    for k in d['badges']:
        d['badges'][k] = False
    d['badges']['op'] = True
    if 'confirmedop' in d['badges']:
        d['badges']['confirmedop'] = True
    d['deleted'] = False
    d['starred'] = False
    d['picked'] = False
    d['highlights'] = note
    d['media'] = []
    d['video'] = ""
    d['floorplan'] = ""
    d['bath'] = "1"
    d['mgmt'] = "The Brusco Group"
    d['pick1'] = False
    d['pick2'] = False
    d['pick3'] = False
    d['videoTour'] = ""
    return d

added = [
    new_entry("329 West 76th St","2A","Studio",3475,"$3,475/mo","1/2 mo OP, huge studio with bay windows, deco fireplace, SS appliances"),
    new_entry("303 West 76th St","3A","1",4190,"$4,190/mo","1/2 mo OP, spacious 1BR, oversized windows, deco fireplace, SS appliances"),
    new_entry("294 West 92nd St","5E","1",3850,"$3,850/mo","1/2 mo OP, newly renovated, hardwood floors, white cabinets, SS appliances"),
]
data.extend(added)
print("added:", len(added))
print("total after:", len(data))

new_arr_text = json.dumps(data, indent=2)
new_text = text[:start] + "\n" + new_arr_text + ";" + text[end+len("];"):]
open(FN, "w").write(new_text)
print("WRITTEN.")
