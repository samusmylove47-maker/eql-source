"""Inventory dumps in, an item-ID map out.

    python3 _build/inventory.py [dir]     # default state/inventory

WHY THIS EXISTS
---------------
`/outputfile inventory` writes what the game itself believes about every item a
character is carrying. For item *names* and *IDs* that is not a reading of a
document, it is the game's own record — the strongest source we have, and it
settles questions that no amount of wiki-reading could.

WHAT IT IS EVIDENCE OF, AND WHAT IT IS NOT
------------------------------------------
It is direct evidence that an item exists, spelled exactly so, with that ID.

It is evidence of **nothing else**. The dump carries no stats, no drop source,
no zone. An item appearing here says a character owns one, and says nothing
about where it came from. So items found here that our catalogue does not
already name are **not** added to it: a page with a name and an ID and no
provenance is a worse page than no page.

WHAT IS COMMITTED, AND WHAT IS NOT
----------------------------------
A dump is a named person's account contents. It carries no chat, but nobody
asked for their holdings to be public. `state/inventory/` is gitignored and the
only thing committed is the impersonal half — name to numeric ID. No counts, no
locations, no character names, nothing about who has what.

Like `geometry.py` and `logstats.py`, this is hand-run and its output is
committed, so `./build.sh` works on a machine with no dumps on it.

THE FORMAT
----------
Tab-separated, two sections. First `Location Name ID Count Slots`:

    Feet                    Golden Efreeti Boots +4              4407  1  10
    Feet-Slot7              Golden Efreeti Boots (Exaltation)    4407  1  10
    General 1               Spacious Rucksack                  177751  1  24
    General 1-Slot3         Bone Chips                          13073  390 10
    General 1-Slot20        Chipped Bone Rod +4                 14510  1  10
    General 1-Slot20-Slot7  Empty                                   0  0   0

A `-SlotN` suffix is containment: a slot in a bag, or an augment socket in an
item. Depth reaches two — an augment inside an item inside a bag. `Empty` rows
carry ID 0 and are skipped.

Then a `KeyRing Name ID` section, typed Augmentation / Equipment / Activated.

THREE THINGS THE FORMAT ESTABLISHES
-----------------------------------
1. **The ID is the canonical key.** Across the two dumps we hold, 257 base names
   map to 257 IDs with no collision either way, and the ID does not change with
   the `+N` upgrade tier or the `(Exaltation)` form. Our name key had to strip
   articles and guess at apostrophes; this does not.

2. **`(Exaltation)` is an augment form.** All 95 of them sit in a `-SlotN` of
   another item or on the Augmentation keyring, never loose and never equipped
   directly. It shares the parent item's ID.

3. **`+N` runs past the drop cap.** Drops top out at +4 (the D4 floor), and
   inventory holds +5 through +10. So the tier above +4 is made, not dropped,
   which is what the log lines showing `... to create a Keg Mallet +4` describe.
"""
import os, re, sys, json, glob, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

PLUS = re.compile(r'\s*\+(\d+)\s*$')
EXALT = re.compile(r'\s*\(Exaltation\)\s*$')
HEAD_INV = 'Location'
HEAD_KEY = 'KeyRing'


def base(name):
    """The item without its upgrade tier or its augment form."""
    return PLUS.sub('', EXALT.sub('', name)).strip()


def norm(s):
    """The catalogue's own join key, so a comparison here means what it means
    everywhere else on the site."""
    s = re.sub(r'^(a|an|the)\s+', '', (s or '').strip(), flags=re.I)
    return re.sub(r'[^a-z0-9]+', '', s.lower())


def read(path):
    """Every non-empty row, as (location, name, id, count)."""
    out, section = [], 'inv'
    for line in open(path, encoding='utf-8', errors='replace'):
        f = line.rstrip('\n').split('\t')
        if not f or not f[0].strip():
            continue
        if f[0] == HEAD_INV:
            continue
        if f[0] == HEAD_KEY:
            section = 'key'
            continue
        if section == 'inv':
            if len(f) < 5:
                continue
            loc, name, iid, count = f[0], f[1], f[2], f[3]
        else:
            if len(f) < 3:
                continue
            loc, name, iid, count = 'KeyRing:' + f[0], f[1], f[2], '1'
        # An empty socket is a row, not an item.
        if name == 'Empty' or iid in ('0', ''):
            continue
        try:
            iid = int(iid)
        except ValueError:
            continue
        out.append((loc, name, iid, int(count or 1)))
    return out


def build(src):
    files = sorted(glob.glob(os.path.join(src, '*.txt')))
    if not files:
        print(f'inventory: no dumps in {src}/, nothing to do '
              f'(the committed assets/item-ids.json is left alone)')
        return

    ids = {}            # base name -> id
    clash = collections.defaultdict(set)
    tiers = collections.Counter()
    exalt_rows = exalt_socketed = 0
    for p in files:
        for loc, name, iid, _count in read(p):
            b = base(name)
            ids.setdefault(b, iid)
            clash[b].add(iid)
            m = PLUS.search(name)
            if m:
                tiers[int(m.group(1))] += 1
            if EXALT.search(name):
                exalt_rows += 1
                # containment is the '-SlotN' chain; the keyring counts too
                if '-Slot' in loc or loc.startswith('KeyRing'):
                    exalt_socketed += 1

    # A name mapping to two IDs would mean the key is not canonical after all,
    # so it is checked rather than assumed. Same in reverse.
    bad_name = {k: sorted(v) for k, v in clash.items() if len(v) > 1}
    byid = collections.defaultdict(set)
    for k, v in ids.items():
        byid[v].add(k)
    bad_id = {k: sorted(v) for k, v in byid.items() if len(v) > 1}

    # Merge with what is already committed. Dumps come and go; the map only
    # grows, exactly as measured.json does.
    prior = {}
    try:
        prior = json.load(open('assets/item-ids.json', encoding='utf-8')).get('items', {})
    except (OSError, ValueError):
        pass
    merged = dict(prior)
    merged.update(ids)

    out = dict(
        _comment=[
            "Item name to the game's own numeric item ID, read from",
            "/outputfile inventory dumps. Generated by _build/inventory.py and",
            "hand-run, like geometry.py - the dumps themselves are gitignored",
            "because they are a named person's account contents.",
            "",
            "This file says an item exists and is spelled exactly so. It says",
            "nothing about stats, or about where the item drops.",
        ],
        items=dict(sorted(merged.items())),
        max_upgrade_seen=(max(tiers) if tiers else None),
        upgrade_tiers_seen={str(k): v for k, v in sorted(tiers.items())},
        exaltation_rows=exalt_rows,
        exaltation_always_socketed=(exalt_rows == exalt_socketed),
    )
    json.dump(out, open('assets/item-ids.json', 'w', encoding='utf-8', newline='\n'),
              indent=1, ensure_ascii=False)

    print(f'item-ids.json: {len(merged)} items ({len(merged) - len(prior)} new) '
          f'from {len(files)} dump(s)')
    print(f'   upgrade tiers seen: {dict(sorted(tiers.items()))}, max +{max(tiers) if tiers else 0}')
    print(f'   (Exaltation) rows: {exalt_rows}, all socketed: {exalt_rows == exalt_socketed}')
    if bad_name:
        print(f'   WARNING one name, several IDs: {bad_name}')
    if bad_id:
        print(f'   WARNING one ID, several names: {bad_id}')

    # ---- what the dump says about the catalogue -----------------------------
    # Reported, never applied. A name correction is a decision for a person to
    # make and record on the change log, not something a parser does quietly on
    # its way past.
    try:
        cat = json.load(open('assets/index-data.json', encoding='utf-8'))['items']
    except (OSError, ValueError, KeyError):
        return
    ours = {norm(i['n']): i['n'] for i in cat}
    theirs = {norm(k): k for k in merged}
    differ = [(ours[k], theirs[k]) for k in sorted(set(ours) & set(theirs))
              if ours[k] != theirs[k]]
    if differ:
        print(f'\n   {len(differ)} item(s) we spell differently from the game:')
        for a, b in differ:
            print(f'      ours {a!r} -> game {b!r}')
    missing = sorted(set(theirs) - set(ours))
    print(f'\n   {len(missing)} item(s) held but not in our catalogue. NOT added: '
          f'the dump gives no drop source, and a page with no provenance is '
          f'worse than no page.')


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else 'state/inventory')
