#!/usr/bin/env python3
"""Mine the survey plates into one searchable dataset for The Index.
Run from build.sh. Output: assets/index-data.json"""
import os, re, json, html as H
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
Z=json.load(open('assets/zones-index.json',encoding='utf-8'))

BADGE=re.compile(r'<span[^>]*class="[^"]*\b(?:tag|pill|badge|new)\b[^"]*"[^>]*>.*?</span>',re.S|re.I)
def txt(x):
    x=BADGE.sub('',x)                      # drop "new" style badges
    x=re.sub(r'<br\s*/?>',' · ',x,flags=re.I)   # a line break separates entries
    x=re.sub(r'</(li|p|div)>',' · ',x,flags=re.I)
    t=re.sub(r'\s+',' ',H.unescape(re.sub(r'<[^>]+>','',x))).strip()
    t=re.sub(r'(\s*·\s*)+',' · ',t).strip(' ·')
    return t
def cells(row): return [txt(c) for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>',row,re.S)]

SLOTS=["Head","Face","Ear","Neck","Shoulders","Arms","Back","Wrist","Hands",
       "Fingers","Finger","Chest","Waist","Legs","Feet","Primary","Secondary",
       "Range","Ammo","Charm","Shield"]
TYPES=["1H Slash","1H Blunt","1H Pierce","2H Slash","2H Blunt","2H Pierce",
       "Hand to Hand","Bow","Instrument","Bag","Container","Food","Drink","Quest","Misc"]
CLS=["WAR","CLR","PAL","RNG","SHD","DRU","MNK","BRD","ROG","SHM","NEC","WIZ",
     "MAG","ENC","BST","BER"]
def norm_slot(raw):
    r=raw or ""
    for s in SLOTS:
        if re.search(r"\b"+s+r"\b", r, re.I): return "Fingers" if s=="Finger" else s
    for t in TYPES:
        if re.search(re.escape(t), r, re.I): return t
    if re.search(r"\bno drop\b|\blore\b", r, re.I): return "Other"
    return "Other"
def norm_cls(raw):
    """Classes an item allows, from a cell that usually also carries races.

    Two rules earned the hard way:

    - The races clause is dropped first. "WAR PAL RNG SHD | all races" contains
      ALL, and reading that as "every class" is exactly backwards.
    - A cell we cannot parse returns [], never ["ALL"]. The old default claimed
      every class could use an item whenever the parse failed, which invents a
      permission and is the worst direction to be wrong in.
    """
    r = (raw or "").upper()
    if not r:
        return []
    r = r.split("|")[0]                      # classes sit before the races clause
    r = re.sub(r"\bALL RACES\b", " ", r)
    if re.search(r"\bALL EXCEPT\b|\bEXCEPT\b", r):
        tail = r.split("EXCEPT", 1)[1]
        excl = [c for c in CLS if re.search(r"\b" + c + r"\b", tail)]
        return [c for c in CLS if c not in excl] if excl else []
    if re.match(r"^\s*ALL\b", r) or re.search(r"\bALL SIXTEEN\b|\bALL CLASSES\b", r):
        return ["ALL"]
    return [c for c in CLS if re.search(r"\b" + c + r"\b", r)]

def slug(s):
    """The address a name gets.

    Computed once, here, and carried in the data. The Index renders its result
    rows in the browser and build17 writes the files those rows link to; if each
    derived the slug itself, one in JavaScript and one in Python, they would
    agree until the first name with a character the two regard differently, and
    then link to a 404 with nothing to catch it. One field, one answer.
    """
    s = re.sub(r'&[a-z]+;', ' ', s)
    s = re.sub(r"[^A-Za-z0-9\s-]", '', s.lower())
    return re.sub(r'[\s_]+', '-', s).strip('-')[:60]


items, named = [], []
for z in Z:
    src=f"_build/source/{z['slug']}.html"
    if not os.path.exists(src): continue
    h=open(src,encoding='utf-8').read()
    for t in re.findall(r'<table[^>]*>(.*?)</table>',h,re.S):
        rows=re.findall(r'<tr[^>]*>(.*?)</tr>',t,re.S)
        if len(rows)<2: continue
        hd=[c.lower() for c in cells(rows[0])]
        if not hd: continue
        # ---- loot tables: Item | Slot | Stats | Classes | Dropped by
        if hd[0]=='item' and 'dropped by' in ' '.join(hd):
            ix={k:i for i,k in enumerate(hd)}
            for r in rows[1:]:
                c=cells(r)
                if len(c)<3: continue
                g=lambda k,d='': c[ix[k]] if k in ix and ix[k]<len(c) else d
                # Headers are not uniform across the surveys: some say "Classes",
                # others "Classes & races", and an exact lookup silently returned
                # nothing for 160 of 452 items - every item in Mistmoore and The
                # Hole. The Index's class filter was dropping a third of the
                # catalogue without saying so. Match the column, not its wording.
                def col(*words, default=''):
                    for k, i in ix.items():
                        if all(w in k for w in words) and i < len(c):
                            return c[i]
                    return default
                slot=col('slot') or g('slot')
                cls=col('class')
                names=[x.strip() for x in c[0].split(' · ') if x.strip()]
                slots_l=[x.strip() for x in slot.split(' · ')] if slot else []
                # 27 of 389 loot rows list several items in one cell and share a
                # single stats cell between them. Splitting the names is right;
                # copying the stats onto each is not, because "Red Dragon Scales"
                # then carries a line describing a Tooth and a book of Prayers.
                # Flagged so a page can show the row rather than assert the stats.
                for k,nm in enumerate(names):
                  sl=slots_l[k] if k<len(slots_l) else (slots_l[0] if slots_l else '')
                  items.append({"n":nm,"s":norm_slot(sl),"sr":sl,"st":g('stats')[:140],
                              "shared":len(names)>1,
                              "c":norm_cls(cls),
                              "d":g('dropped by')[:110],"z":z['slug'],"zt":z['title'],
                              "a":z['accent'],"p":z['plate'],"lv":z['levels']})
        # ---- named rosters: Named | ... | Lvl | ...
        elif 'named' in ' '.join(hd[:2]):
            ix={k:i for i,k in enumerate(hd)}
            nk='named' if 'named' in ix else hd[1]
            for r in rows[1:]:
                c=cells(r)
                if len(c)<2: continue
                g=lambda k,d='': c[ix[k]] if k in ix and ix[k]<len(c) else d
                nm=g(nk)
                if not nm or nm in ('#',''): continue
                named.append({"n":nm,"lv":g('lvl'),"loc":g('loc (y, x)'),
                              "fl":g('flr'),"rc":g('race / class'),
                              "no":(g('notes') or g('spawn & notes'))[:190],
                              "z":z['slug'],"zt":z['title'],"a":z['accent'],"p":z['plate']})

for r in items: r["u"] = slug(r["n"])
for r in named: r["u"] = slug(r["n"])

# A slug collision would point two different names at one page, so it is a build
# failure rather than a warning. Names that differ only in punctuation collide.
for label, rows in (("item", items), ("named", named)):
    bad = {}
    for r in rows:
        bad.setdefault(r["u"], set()).add(r["n"])
    clash = {k: v for k, v in bad.items() if len(v) > 1}
    if clash:
        raise SystemExit(f"{label} slug collision: {clash}")

# de-duplicate identical item rows within a zone
seen=set(); clean=[]
for it in items:
    k=(it['n'],it['z'])
    if k in seen: continue
    seen.add(k); clean.append(it)

order=SLOTS[:-1]+TYPES+["Other"]
slots=[s for s in order if any(i['s']==s for i in clean)]
classes=[c for c in ["ALL"]+CLS if any(c in i['c'] for i in clean)]
json.dump({"items":clean,"named":named,"slots":slots,"classes":classes},
          open('assets/index-data.json','w',encoding='utf-8',newline='\n'), separators=(',',':'))
print(f"index-data.json: {len(clean)} items, {len(named)} named, "
      f"{len(slots)} slots, {len(classes)} class tags")
