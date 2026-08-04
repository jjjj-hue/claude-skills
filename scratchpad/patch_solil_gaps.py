import json, re, copy

FN = "/Users/luciaj/Claude/scratchpad/qualified-bank-LIVE.html"
text = open(FN).read()
s = text.index("const SEED = ") + len("const SEED = ")
start = text.index("[", s)
end = text.index("];const STORE_KEY")
data = json.loads(text[start:end+1])
print("total before:", len(data))

template = None
for d in data:
    if 'solil' in ((d.get('source','') or '')+(d.get('note','') or '')).lower():
        template = d
        break

def norm(addr):
    a = addr.lower()
    a = re.sub(r'\(.*?\)', '', a)
    a = re.sub(r'#', '', a)
    a = re.sub(r'\bstreet\b|\bst\b', '', a)
    a = re.sub(r'(\d+)(st|nd|rd|th)\b', r'\1', a)
    a = re.sub(r'[^a-z0-9]', '', a)
    return a
def normapt(apt):
    a = apt.lower(); a = re.sub(r'[^a-z0-9]','',a); a = re.sub(r'^0+','',a); return a

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
    if status == 'rented':
        d['badges']['rented'] = True
        d['badges']['op'] = False
    elif status == 'app':
        d['badges']['app'] = True
        d['badges']['op'] = True
    else:
        d['badges']['op'] = True
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

gaps = [
    new_entry("20 Fifth Ave","1E","2","8255","$8,255/mo","8/7/26","2BR/2BTH with W/D, rent stab, app approved", status="app"),
    new_entry("145 East 16th St","15H","studio","5800","$5,800/mo","","RENTED — alcove studio", status="rented"),
    new_entry("140 East 46th St","4A","1","4300","$4,300/mo","09/01/26 still occupied","app fell through, back available"),
    new_entry("157 East 57th St","16A","2","8100","$8,100/mo","vacant","2BR/2BTH with Terrace and W/D"),
    new_entry("219 East 69th St","9F","jr4","6100","$6,100/mo","vacant","app approved but might back out", status="app"),
    new_entry("219 East 69th St","10D","2","8700","$8,700/mo","vacant","app approved but might back out", status="app"),
    new_entry("219 East 69th St","10HJ","4","17500","$17,500/mo","vacant","app approved but might back out", status="app"),
    new_entry("166 West 72nd St","8D","1","5900","$5,900/mo","","RENTED", status="rented"),
    new_entry("150 Remsen St","22","1","5000","$5,000/mo","","RENTED", status="rented"),
    new_entry("80 Cranberry St, Brooklyn","6G","1","5800","$5,800/mo","","RENTED", status="rented"),
]
data.extend(gaps)
print("added gap entries:", len(gaps))
print("total after:", len(data))

new_arr_text = json.dumps(data, indent=2)
new_text = text[:start] + "\n" + new_arr_text + ";" + text[end+len("];"):]
open(FN, "w").write(new_text)
print("WRITTEN.")
