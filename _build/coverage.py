"""assets/coverage.json — how much of what a player needs each zone carries.

WHY THIS REPLACES THE HEADLINE GRADE
------------------------------------
The old headline was `verify_level`, and its third gate asks whether plotted
coordinates land on drawn floor. Plane of Fear and Plane of Hate have no plotted
coordinates, so that gate could never pass there however much we played — and
both zones scored the same zero as Kedge Keep, where we have never logged a
session at all. A grade that cannot tell "no coordinates" from "no evidence"
is not measuring the thing.

Coordinates are how WE draw the floor plans. They are a build input. What a
player wants, in the collaborator's own order: bosses, loot, what the difficulty
tier changes, which inherited advice is now wrong, and — for the zones people
grind — whether it is worth farming.

`verify_level` is kept exactly as it was. It is sourcing hygiene, it is real,
and it is no longer the headline. See docs/WHAT-COUNTS.md.

EVERY FACET IS COMPUTED, NOT TYPED
----------------------------------
The one rule this project keeps relearning is that a number typed beside data
drifts from it. So each facet is derived here from measured.json, sightings.json,
raids-measured.json and zones-index.json, and the page prints what this file
says. A zone improves its grade by being played, not by being edited.

    measured   our own parsed logs say so
    sourced    documented from a named source, no play of our own
    none       we have nothing
"""
import os, re, sys, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

Z = json.load(open('assets/zones-index.json', encoding='utf-8'))
M = json.load(open('assets/measured.json', encoding='utf-8'))
S = json.load(open('assets/sightings.json', encoding='utf-8'))
R = json.load(open('assets/raids-measured.json', encoding='utf-8'))
IX = json.load(open('assets/index-data.json', encoding='utf-8'))

# The same zone-name mapping build9.py uses: the game writes "The Ruins of Old
# Paineel" where the survey says "The Hole", and a public group instance appends
# " - Group".
ALIASES = {'ruinsoldguk': 'lowerguk', 'cityguk': 'upperguk',
           'ruinsoldpaineel': 'hole'}
GROUP = re.compile(r'\s*-\s*group\s*$', re.I)


def zkey(name):
    # ORDER MATTERS. The game writes "The Plane of Fear - Group 3 (Fused)", so
    # " - Group" sits in the MIDDLE, not at the end. Stripping the group suffix
    # first leaves it untouched, and Plane of Fear read as a zone we had never
    # fought a boss in - with sixteen parsed boss fights in the file.
    s = re.sub(r'\s+\d+\s*\(.*?\)\s*$', '', name or '')   # drop " 3 (Fused)"
    s = GROUP.sub('', s)                                  # then " - Group"
    s = re.sub(r'\b(the|of|a|an)\b', ' ', s.lower())
    s = re.sub(r'[^a-z0-9]', '', s)
    return ALIASES.get(s, s)


BY_KEY = {zkey(z['title']): z['slug'] for z in Z}


def zone_of(name):
    return BY_KEY.get(zkey(name))


def facet(level, detail):
    return dict(level=level, detail=detail)


# ---- what our logs say, per zone -------------------------------------------
kills = collections.Counter()
tiers = collections.defaultdict(set)
mobtypes = collections.defaultdict(set)
for s in M:
    slug = zone_of(s.get('zone') or '')
    if not slug:
        continue
    kills[slug] += s.get('kills', 0)
    if s.get('difficulty') is not None:
        tiers[slug].add(s['difficulty'])
    mobtypes[slug] |= set(s.get('mobs') or {})

bossfights = collections.defaultdict(list)
for f in R:
    slug = zone_of(f.get('zone') or '')
    if slug:
        bossfights[slug].append(f)

# measured drops, attributed to a zone through the session that saw them
drops = collections.defaultdict(set)
for item, rows in S.get('by_item', {}).items():
    for r in rows:
        for sess in r.get('sessions', []):
            slug = zone_of(sess.get('zone') or '')
            if slug:
                drops[slug].add(item)

# what the surveys themselves record
named_in_roster = collections.Counter(n.get('z') for n in IX['named'])
loot_in_roster = collections.Counter(i.get('z') for i in IX['items']
                                     if i.get('kind') == 'item')

out = {}
for z in Z:
    slug = z['slug']
    bf = bossfights.get(slug, [])
    distinct_bosses = sorted({f['boss'] for f in bf})
    btiers = sorted({f['difficulty'] for f in bf if f['difficulty'] is not None})

    # 1. BOSSES — what the player is actually here to kill
    if distinct_bosses:
        f_boss = facet('measured',
                       f"{len(distinct_bosses)} boss{'es' if len(distinct_bosses) > 1 else ''} "
                       f"fought and parsed across {len(bf)} kills"
                       + (f", tiers D{btiers[0]}–D{btiers[-1]}" if len(btiers) > 1 else
                          (f", D{btiers[0]}" if btiers else "")))
    elif named_in_roster.get(slug):
        f_boss = facet('sourced', f"{named_in_roster[slug]} named on the roster, "
                                  f"none fought by us")
    else:
        f_boss = facet('none', 'no named mobs recorded')

    # 2. LOOT — what drops, and whether we watched it
    if drops.get(slug):
        f_loot = facet('measured', f"{len(drops[slug])} items watched dropping here")
    elif loot_in_roster.get(slug):
        f_loot = facet('sourced', f"{loot_in_roster[slug]} items listed, none seen by us")
    else:
        f_loot = facet('none', 'no loot recorded')

    # 3. DIFFICULTY — the thing that has no classic equivalent at all
    t = sorted(tiers.get(slug, ()))
    if len(t) > 1:
        f_diff = facet('measured', "played and parsed at D" + ", D".join(str(x) for x in t))
    elif len(t) == 1:
        f_diff = facet('measured', f"played and parsed at D{t[0]} only")
    else:
        f_diff = facet('none', 'never played at a recorded difficulty')

    # 4. INHERITED — is the classic advice on this page marked as classic
    page = f"public/dungeons/{slug}.html"
    badges = 0
    if os.path.exists(page):
        badges = open(page, encoding='utf-8').read().count('class="tier t5"')
    if z.get('placeholders_removed') or badges:
        f_inh = facet('sourced',
                      f"{badges} inherited claim{'s' if badges != 1 else ''} badged"
                      + (", placeholder model retracted in place"
                         if z.get('placeholders_removed') else ""))
    else:
        f_inh = facet('none', 'nothing on this page is marked as inherited')

    # 5. FARMING — only meaningful for the grind zones, but cheap to state
    bits = []
    if z.get('zem'):
        bits.append(f"ZEM {z['zem']}")
    if z.get('respawn'):
        bits.append(f"respawn {z['respawn']}")
    if mobtypes.get(slug):
        bits.append(f"{len(mobtypes[slug])} mob types measured")
    f_farm = facet('measured' if mobtypes.get(slug) else
                   ('sourced' if bits else 'none'),
                   ', '.join(bits) or 'no farming figures recorded')

    facets = dict(bosses=f_boss, loot=f_loot, difficulty=f_diff,
                  inherited=f_inh, farming=f_farm)
    score = sum(2 if f['level'] == 'measured' else 1 if f['level'] == 'sourced' else 0
                for f in facets.values())
    out[slug] = dict(title=z['title'], facets=facets, score=score,
                     max_score=len(facets) * 2,
                     kills=kills.get(slug, 0),
                     bosses=distinct_bosses)

json.dump(dict(
    _comment=[
        "How much of what a player needs each zone carries, computed from the",
        "measured data rather than typed. See docs/WHAT-COUNTS.md.",
        "",
        "A zone improves this by being played, not by being edited.",
        "verify_level still exists and is sourcing hygiene, not the headline.",
    ],
    zones=out),
    open('assets/coverage.json', 'w', encoding='utf-8', newline='\n'),
    indent=1, ensure_ascii=False)

rank = sorted(out.items(), key=lambda kv: -kv[1]['score'])
print(f"coverage.json: {len(out)} zones graded on what a player needs")
for slug, d in rank:
    marks = ''.join({'measured': 'M', 'sourced': 's', 'none': '·'}[f['level']]
                    for f in d['facets'].values())
    print(f"   {d['score']:>2}/{d['max_score']}  {marks}  {d['title']}")
