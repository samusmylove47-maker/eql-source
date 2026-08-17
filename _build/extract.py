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
    # "range 40" on a thrown weapon is a distance, not the Range equipment slot.
    # The whole descriptor is fed in here now, so the word arrives where it
    # never used to: Dagger of Marnek reads "Pierce 3 / 30 · range 40 · lore"
    # and was filed under Range in The Index's slot filter, on a cell that names
    # no equipment slot at all. The number is already captured separately as the
    # item's range, so the measurement is not lost by ignoring it here.
    r = re.sub(r"\brange\s+\d+", " ", r, flags=re.I)
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

# ---------------------------------------------------------------------------
# THE SLOT CELL CARRIES MORE THAN A SLOT, AND IT USED TO BE THROWN AWAY.
#
# A survey's "Slot / type" cell is the only place the guides record whether an
# item can be handed to a guildmate. It reads
# "Primary · 1H Slash · 15 / 46 · lore · no drop" and this file kept the first
# token. So 159 "no drop" markings in the surveys reached 0 of 442 item pages,
# every weapon's damage and delay went the same way, and two weapons could not
# be compared anywhere on the site.
#
# Parsed here, once, into named fields. The rule that matters most is the
# negative one: **a flag absent from the cell is not evidence the restriction is
# absent.** There is no "tradeable" value anywhere in this file. An item whose
# cell names no restriction gets an empty list, and the page says "not recorded".

TRADE_FLAGS = [                      # order matters, see the two suppressions
    (r"\bno[\s-]?drop\b",     "No Drop"),
    (r"\bno[\s-]?trade\b",    "No Trade"),
    (r"\bno[\s-]?rent\b",     "No Rent"),
    (r"\blore\s+equipped\b",  "Lore Equipped"),
    (r"\blore\b",             "Lore"),
    (r"\battun(?:able|ed)\b", "Attunable"),
    (r"\btemporary\b",        "Temporary"),
    # "magic item" only. A bare "Magic" in these cells is nearly always
    # "SV Magic +3", and reading a saving throw as an item flag invents one.
    (r"\bmagic\s+item\b",     "Magic"),
]
# What a survey writes immediately after a flag when it is saying the flag went
# away. Anchored at the match, so "No Rent removed 24 June" is a removal and
# "No Rent, removed from the vendor list" is not caught by accident - the comma
# form would need a cue word first.
NEGATED = re.compile(r'\s*(?:was\s+)?(?:removed|lifted|dropped)\b'
                     r'|\s*no\s+longer\b', re.I)

HANDLING_FLAGS = [
    (r"\bfocus\b",            "Focus effect"),
    (r"\bclick(?:able|y)?\b", "Clickable"),
    (r"\bproc\b",             "Proc"),
    (r"\bexpendable\b",       "Expendable"),
    (r"\btradeskill\b",       "Tradeskill"),
    (r"\bultra[\s-]rare\b",   "Ultra rare"),
    (r"\brare\b",             "Rare"),
    (r"\bquest\s+turn-?in\b", "Quest turn-in"),
    (r"\bquest\s+starter\b",  "Quest starter"),
    (r"\bquest\s+reward\b",   "Quest reward"),
    (r"\bquest\b",            "Quest"),
]
WTYPES = ["Hand to Hand", "1H Slash", "1H Blunt", "1H Pierce", "2H Slash",
          "2H Blunt", "2H Pierce", "Archery", "Throwing", "Piercing", "Pierce",
          "Slashing", "Slash", "Blunt", "Bow", "Instrument"]
WTYPE_RE = re.compile(r"\b(" + "|".join(re.escape(t) for t in WTYPES) + r")\b", re.I)
# "15 / 46" is damage over delay. Guarded against the stat shorthands that also
# carry a slash: never after a word character, a sign or a decimal point, so
# "HP +15/+10" and "pg. 1/3" cannot be read as a weapon.
DMGDLY_RE = re.compile(r"(?<![\w+.\-])(\d{1,3})\s*/\s*(\d{1,3})(?![\w.])")
BACKSTAB_RE = re.compile(r"\bbackstab\s+(\d{1,3})\b", re.I)
RANGE_RE = re.compile(r"\brange\s+(\d{1,4})\b", re.I)
CHARGES_RE = re.compile(r"\b(unlimited|single|\d{1,3})\s+charges?\b", re.I)
SLOT_WORDS = {s.lower() for s in SLOTS}


def is_slot_tok(t):
    """True where every word of the token is a slot name — "Primary / Secondary",
    "Range Ammo", "Wrist". Used to decide slot phrases and per-item alignment."""
    parts = [p for p in re.split(r"[\s/]+", t.strip()) if p]
    return bool(parts) and all(p.lower() in SLOT_WORDS for p in parts)


def is_type_tok(t):
    """True where the token is a weapon type, with or without its damage/delay."""
    r = t.strip()
    m = WTYPE_RE.match(r)
    if not m:
        return False
    return not re.sub(r"[\d\s/]+", "", r[m.end():])


WORDS_OK = SLOT_WORDS | {w.lower() for t in WTYPES for w in t.split()}


def read_dmgdly(toks, has_type):
    """Damage and delay, but only from a token that is about a weapon.

    "50 / 50" is a valid-looking pair and Najena's Dark Cauldron cell reads
    "Component · no drop · roughly 50/50" — a drop chance. So the pair is only
    read where the rest of its own token is slot and weapon-type words
    ("Secondary 8 / 31", "2H Slash 15 / 38"), or where the pair stands alone in
    its token and the cell names a weapon type elsewhere ("Primary · 2H Slash ·
    15 / 46"). Anything else is a number we cannot vouch for, so we do not
    publish it.
    """
    for t in toks:
        m = DMGDLY_RE.search(t)
        if not m:
            continue
        rest = [w for w in re.split(r"[\s/]+", DMGDLY_RE.sub(" ", t)) if w]
        if not rest:
            if has_type:
                return int(m.group(1)), int(m.group(2))
            continue
        if all(w.lower() in WORDS_OK for w in rest):
            return int(m.group(1)), int(m.group(2))
    return None


def read_cell(cell):
    """Every fact a survey's slot/type cell records, as named fields.

    Returns a dict carrying only what the cell actually says. Keys are absent
    where the cell is silent — never filled with a default, because a default is
    a claim we did not read anywhere.
    """
    out = {}
    if not cell:
        return out
    toks = [t.strip() for t in cell.split(' · ') if t.strip()]

    trade, lifted = [], []
    for pat, label in TRADE_FLAGS:
        m = re.search(pat, cell, re.I)
        if not m:
            continue
        # A SURVEY THAT RECORDS A FLAG BEING REMOVED IS NOT RECORDING THE FLAG.
        #
        # Najena writes "Key 3 - Drelzna's room - No Rent removed 24 June", and
        # matching the words alone published a restriction the same sentence
        # says was lifted. Both No Rent flags on the site read that way, so the
        # flag was wrong twice out of twice.
        #
        # The removal is itself worth publishing - a reader who remembers the
        # old behaviour needs to be told it changed - so it is recorded rather
        # than merely suppressed.
        after = cell[m.end():m.end() + 40]
        if NEGATED.match(after):
            lifted.append(label)
        else:
            trade.append(label)
    if "Lore Equipped" in trade and "Lore" in trade:
        trade.remove("Lore")           # one flag written two ways, not two flags
    if lifted:
        out['trade_lifted'] = lifted
    hand = []
    for pat, label in HANDLING_FLAGS:
        if re.search(pat, cell, re.I):
            hand.append(label)
    for broad, narrow in (("Rare", "Ultra rare"),
                          ("Quest", "Quest turn-in"), ("Quest", "Quest starter"),
                          ("Quest", "Quest reward")):
        if narrow in hand and broad in hand:
            hand.remove(broad)
    if trade:
        out["tf"] = trade
    if hand:
        out["hf"] = hand

    m = WTYPE_RE.search(cell)
    if m:
        out["wt"] = next(t for t in WTYPES if t.lower() == m.group(1).lower())
    dd = read_dmgdly(toks, "wt" in out)
    if dd:
        out["dmg"], out["dly"] = dd
    m = BACKSTAB_RE.search(cell)
    if m:
        out["bs"] = int(m.group(1))
    m = RANGE_RE.search(cell)
    if m:
        out["rng"] = int(m.group(1))
    m = CHARGES_RE.search(cell)
    if m:
        out["ch"] = m.group(0)

    slots = [t for t in toks if is_slot_tok(t)]
    if slots:
        out["sl"] = ' · '.join(slots)
    return out


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


FIX = json.load(open("assets/catalogue-fixes.json", encoding="utf-8"))
FRAGMENTS, GROUPS = FIX["fragments"], set(FIX["groups"])
ALIASES, SPLITS = FIX["aliases"], FIX["split_named"]
# A fragment whose full name a dump has since confirmed is not a fragment any
# more - it is an ordinary item that we could not name. Renamed here, before
# anything downstream sees it, so the slug, the page, The Index and the share
# card all agree without any of them knowing this ever happened.
RESOLVED = {k: v["name"] for k, v in FIX.get("fragment_resolved", {}).items()}

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
                # Not every loot table names its descriptor column the same way.
                # Lower Guk heads one "Type", and four tables across Najena,
                # Mistmoore, The Hole and the Warrens head theirs "What it is
                # for" / "Used for". An exact lookup for "slot" found none of
                # them, so 82 of 389 rows carried no descriptor at all - and
                # those purpose columns are where Najena records that the
                # Magician epic components are no drop.
                slot = col('slot') or col('type') or g('slot')
                use = '' if slot else col('what it', 'for') or col('used for')
                # "Effect" is Mistmoore's word for the stats column.
                stats = col('stats') or col('effect')
                cls=col('class')
                names=[x.strip() for x in c[0].split(' · ') if x.strip()]
                desc = slot or use
                toks = [t.strip() for t in desc.split(' · ') if t.strip()]
                # Where a row lists several items AND the cell opens with one
                # slot or weapon type per item, they line up: "Shin Gauntlets ·
                # Shin Greaves" against "Hands · Legs · lore · no drop" gives
                # each its own slot and both the shared restrictions. Where they
                # do not line up - four names against "Various" - the whole cell
                # describes the row, and every name carries the whole cell rather
                # than one word torn out of it.
                lead = 0
                for t in toks:
                    if is_slot_tok(t) or is_type_tok(t):
                        lead += 1
                    else:
                        break
                aligned = len(names) > 1 and lead == len(names)
                tail = ' · '.join(toks[len(names):]) if aligned else ''
                # 27 of 389 loot rows list several items in one cell and share a
                # single stats cell between them. Splitting the names is right;
                # copying the stats onto each is not, because "Red Dragon Scales"
                # then carries a line describing a Tooth and a book of Prayers.
                # Flagged so a page can show the row rather than assert the stats.
                for k,nm in enumerate(names):
                  own = (' · '.join(x for x in (toks[k], tail) if x)
                         if aligned else desc)
                  nm = RESOLVED.get(nm, nm)
                  kind = ("fragment" if nm in FRAGMENTS else
                          "group" if nm in GROUPS else "item")
                  f = read_cell(own)
                  # A restriction written into the stats cell instead of the slot
                  # cell. One row does this today - Befallen's Smoked Glass Key,
                  # "Temporary removed 16 June · still flagged NO RENT" - and it
                  # is exactly the row a flag scanner would get backwards, since
                  # one of the two words is there to say the flag was taken away.
                  # So it is never parsed into a flag: the page is told to point
                  # the reader at the stats line and print it verbatim.
                  st = stats
                  if not f.get("tf") and re.search(
                          r"\bno[\s-]?(?:drop|trade|rent)\b|\blore\b|\btemporary\b",
                          st, re.I):
                      f["tfs"] = True
                  items.append({"n":nm,"s":norm_slot(f.get("sl") or own),
                              # The whole descriptor, never a torn-out token: it
                              # feeds The Index's free-text search as well as the
                              # item page, and a search for "no drop" that finds
                              # nothing is the same bug one layer up.
                              "sr":own,
                              # Uncapped. The old 140-character cap never bit -
                              # the longest stats cell in the ten surveys is 107 -
                              # but a cap that silently drops the tail of a fact
                              # is the shape of the bug this whole change fixes.
                              "st":st,
                              **({"use":use} if use else {}),
                              **f,
                              "kind":kind,
                              **({"parent":FRAGMENTS[nm]} if kind=="fragment" else {}),
                              "shared":len(names)>1,
                              # The cell describes the whole row rather than this
                              # item: several names, and no per-item slot to line
                              # them up against. The flags read out of it are the
                              # row's, and the page has to say so before it prints
                              # "no drop" against one of four names.
                              **({"rowdesc":True} if len(names)>1 and not aligned
                                 else {}),
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
                for nm in SPLITS.get(nm, [ALIASES.get(nm, nm)]):
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
# ONE DEFINITION OF "HOW MANY ITEMS", COUNTED HERE.
#
# Three generators counted this three ways and published two different figures:
# the home page counted every row including groups and fragments (451), The
# Index filtered fragments but not groups (441), and the A-Z counted the pages
# it had just written. An outside audit raised this on 11 August as 452 against
# 446; the numbers moved and the disagreement did not, because the fix was
# applied to the numbers rather than to the definition.
#
# `kind` already says what a thing is. These counts read it, and every page
# prints from here instead of counting for itself.
_items = [i for i in clean if i.get('kind') == 'item']
counts = {
    "item_pages":   len({i['n'] for i in _items}),   # one page per name
    "item_rows":    len(_items),                     # a name in two zones is two rows
    "item_groups":  len({i['n'] for i in clean if i.get('kind') == 'group'}),
    "item_fragments": len({i['n'] for i in clean if i.get('kind') == 'fragment'}),
    "named_pages":  len({n['n'] for n in named}),
    "named_rows":   len(named),
}
json.dump({"items":clean,"named":named,"slots":slots,"classes":classes,
           "counts":counts},
          open('assets/index-data.json','w',encoding='utf-8',newline='\n'), separators=(',',':'))
print(f"index-data.json: {counts['item_pages']} item pages "
      f"({counts['item_rows']} rows, {counts['item_groups']} groups, "
      f"{counts['item_fragments']} fragments), {counts['named_pages']} named, "
      f"{len(slots)} slots, {len(classes)} class tags")
