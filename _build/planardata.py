"""assets/planar.json — the 116 planar armour pieces, as data.

WHY THIS IS ITS OWN FILE
------------------------
It was the first half of _build/build19.py, which rendered the planar gear tool
and wrote this dataset in the same breath. Four things read the dataset and none
of them render that page:

    _build/build24.py      /sets/, every planar set piece by piece
    _build/build25.py      the inventory reader
    _build/sightings.py    the measured-drop match table
    scripts/contamination.py

**sightings.py is the one that makes this load-bearing.** index-data.json is
mined from the dungeon surveys and contains no planar armour at all, so without
these names every planar set drop matches nothing and is discarded as trash —
86 of them, the only evidence anyone holds of which boss drops which set. That
feeds public/data/sightings.v1.json, which is a published contract.

So a page generator was, unannounced, the only producer of a dataset that a
published contract depends on. Deleting the page would have taken the data with
it and the build would have gone green: check.py failed a dataset that emptied,
and this one would not have emptied — it would have lost the hundred items the
two catalogues share and kept the rest.

Split out so the page can be withdrawn without the data going with it. Runs in
build.sh before every one of its readers.
"""
import os, sys, json, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))

FIELDS = ["slot", "ac", "str", "sta", "agi", "dex", "wis", "int", "cha", "hp",
          "mana", "svmagic", "svfire", "svcold", "svdisease", "svpoison",
          "effect", "weight", "classes"]

# Set name -> the class it belongs to. The two shared sets carry no single
# class; their own class lists on the items decide who may wear them.
SETS = [
    ("Lustrous Russet", None, "Chain and plate. Drops from haunted chests in Hate."),
    ("Midnight Clad", None, "Cloth and leather. Drops from phoboplasms in Fear."),
    ("Ethereal Mist", "CLR", None), ("Vermiculated", "DRU", None),
    ("Rune Etched", "SHM", None), ("Anthemion", "BST", None),
    ("Thorny Vine", "RNG", None), ("Valorium", "PAL", None),
    ("Shadow Rage", "BER", None), ("Shiverback-hide", "MNK", None),
    ("Insidious", "ENC", None), ("Apothic", "MAG", None),
    ("Blighted", "NEC", None), ("Carmine", "WIZ", None),
    ("Imbrued Platemail", "BRD", None), ("Umbral Platemail", "SHD", None),
    ("Woven Shadow", "ROG", None), ("Indicolite", "WAR", None),
]
CLASSES = ["WAR", "CLR", "PAL", "RNG", "SHD", "DRU", "MNK", "BRD",
           "ROG", "SHM", "NEC", "WIZ", "MAG", "ENC", "BST", "BER"]
CLASS_NAME = {"WAR": "Warrior", "CLR": "Cleric", "PAL": "Paladin", "RNG": "Ranger",
              "SHD": "Shadow Knight", "DRU": "Druid", "MNK": "Monk", "BRD": "Bard",
              "ROG": "Rogue", "SHM": "Shaman", "NEC": "Necromancer", "WIZ": "Wizard",
              "MAG": "Magician", "ENC": "Enchanter", "BST": "Beastlord",
              "BER": "Berserker"}
SLOTS = ["HEAD", "CHEST", "ARMS", "WRIST", "HANDS", "LEGS", "FEET"]
# Wrist is the only planar slot a character wears two of. The sets carry no
# rings or earrings, so those are not offered rather than invented.
DOUBLE = {"WRIST": 2}


def parse():
    items, missing = [], 0
    for line in open('_build/planar_raw.txt', encoding='utf-8'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = [p.strip() for p in line.split('|')]
        name, vals = parts[0], parts[1:]
        row = dict(zip(FIELDS, vals))
        it = {"n": name, "s": row["slot"]}
        for f in FIELDS:
            if f in ("slot", "classes", "effect", "weight"):
                continue
            v = row[f]
            if v != "NR":
                it[f] = int(re.sub(r'[^0-9-]', '', v) or 0)
            else:
                missing += 1
        # An effect has to have a letter in it. One row arrived with "5" in the
        # effect column, which is a save value that slipped a field, and a
        # numeric effect name would have been published as a clicky.
        if row["effect"] != "NR" and re.search(r'[A-Za-z]', row["effect"]):
            it["fx"] = row["effect"]
        if row["weight"] != "NR":
            it["w"] = float(row["weight"])
        it["c"] = row["classes"].split()
        for prefix, cls, note in SETS:
            if name.startswith(prefix):
                it["set"] = prefix
                it["cls"] = cls
                break
        else:
            raise SystemExit(f"no set matches {name!r}")
        items.append(it)
    return items, missing


ITEMS, N_MISSING = parse()
SHARED = [s for s, c, n in SETS if c is None]
BY_SET = {}
for it in ITEMS:
    BY_SET.setdefault(it["set"], []).append(it)
THIN = {s: len(v) for s, v in BY_SET.items() if len(v) < 7}

DATA = {
    "items": ITEMS,
    "slots": SLOTS,
    "double": DOUBLE,
    "classes": CLASSES,
    "classNames": CLASS_NAME,
    "shared": SHARED,
    "setClass": {s: c for s, c, n in SETS},
    "thin": THIN,
}

# Guarded, because build19.py imports this module for DATA and an unguarded
# write would rewrite the file and print the same line a second time on every
# build. Importing it gives you the pieces; running it writes the dataset.
if __name__ == '__main__':
    json.dump(DATA, open('assets/planar.json', 'w', encoding='utf-8', newline='\n'),
              separators=(',', ':'))
    print(f"assets/planar.json: {len(ITEMS)} pieces across {len(BY_SET)} sets, "
          f"{N_MISSING} unrecorded fields kept blank")
