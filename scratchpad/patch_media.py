import json, re

FN = "/Users/luciaj/Claude/scratchpad/qualified-bank-LIVE.html"
text = open(FN).read()
s = text.index("const SEED = ") + len("const SEED = ")
start = text.index("[", s)
end = text.index("];const STORE_KEY")
data = json.loads(text[start:end+1])
print("total:", len(data))

def norm(addr):
    a = addr.lower()
    a = re.sub(r'\(.*?\)', '', a)
    a = re.sub(r'\bstreet\b|\bst\b', '', a)
    a = re.sub(r'\bavenue\b|\bave\b', '', a)
    a = re.sub(r'(\d+)(st|nd|rd|th)\b', r'\1', a)
    a = re.sub(r'[^a-z0-9]', '', a)
    return a
def normapt(apt):
    a = apt.lower(); a = re.sub(r'[^a-z0-9]','',a); return a

def find_all(addr, apt):
    na, nap = norm(addr), normapt(apt)
    return [d for d in data if norm(d['address'])==na and normapt(d['apt'])==nap]

media_updates = [
    ("491 Columbus Ave", "4R", {"floorplan": "https://my.matterport.com/show/?m=vP6y2jQtkTP"}),
    ("162 West 80th St", "5G", {
        "videoTour": "https://www.youtube.com/watch?v=LRHt80YXRbk&t=2s",
        "floorplan": "https://my.matterport.com/show/?m=uVL8am8UwXk",
    }),
    ("96 Fifth Ave", "3H", {"floorplan": "https://my.matterport.com/show/?m=KUZRR2TcXBV"}),
    ("294 West 92nd St", "5E", {"videoTour": "https://www.youtube.com/watch?v=YMMvjJ_O8Ao"}),
    ("67 West 73rd St", "4B", {"floorplan": "https://my.matterport.com/show/?m=GBVP4ZciM6H"}),
]

MISSES = []
touched = 0
for addr, apt, fields in media_updates:
    m = find_all(addr, apt)
    if not m:
        MISSES.append((addr, apt))
        continue
    for d in m:
        for k, v in fields.items():
            d[k] = v
        touched += 1

print("MISSES:", MISSES)
print("touched entries:", touched)

new_arr_text = json.dumps(data, indent=2)
new_text = text[:start] + "\n" + new_arr_text + ";" + text[end+len("];"):]
open(FN, "w").write(new_text)
print("WRITTEN.")
