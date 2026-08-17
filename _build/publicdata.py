"""public/data/*.v1.json — the datasets, published as a contract.

WHAT THIS IS
------------
Nobody in this community publishes consumable data. Every tool re-transcribes
the same wiki pages and inherits the same classic-era errors doing it. The
position worth holding is not the fifth tracker; it is the layer underneath —
clean, versioned, per-claim-sourced data that other tools read instead of
retyping.

That is only worth anything if it can be relied on, so this is written as a
contract and the contract is stated on the files themselves.

THE VERSION IN THE FILENAME IS THE PROMISE
------------------------------------------
`sky.v1.json` will not change shape. Fields are never removed and never change
type. New optional fields may appear — a consumer that ignores unknown keys
keeps working. Anything that would break a reader gets a new number at a new
URL, and v1 stays up.

**Values change. That is the point, not a violation.** This site corrects
itself; a figure that improves is the product working. `hash` changes when the
data does, so a consumer can cache on it.

INTERNAL SHAPES ARE NOT THE CONTRACT
------------------------------------
These files are generated FROM assets/, never symlinked to it. The internal
files change shape whenever a generator needs them to — sky.json gained a whole
provenance model in a day. Publishing them directly would turn every internal
refactor into a broken promise, so there is a mapping layer here, and it is the
only thing that has to stay still.

WHAT IS NOT PUBLISHED
---------------------
Raw combat logs and inventory dumps. They are a named person's play records and
carry private chat. Everything derived from them is here; the source is not,
and never will be.
"""
import os, sys, json, hashlib, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
OUT = 'public/data'
SITE = json.load(open('site.config.json', encoding='utf-8')).get(
    'site_url', 'https://eqlsource.com').rstrip('/')

TERMS = {
    "summary": "Use it, credit EQL Source, and read the provenance before you "
               "trust a value.",
    "attribution": f"EQL Source, {SITE}",
    "measured": "The measured data — drop sightings, damage figures, spell "
                "lists — is parsed from this project's own combat logs. Freely "
                "usable with attribution.",
    "inherited": "Fields sourced from community wikis carry their tier and "
                 "source. Those values are not ours to license; respect the "
                 "original source and do not present a tier 5 figure as fact.",
    "warranty": "None. This is a fan project and the game is actively patched. "
                "Every dataset here states what it does not know.",
    "unofficial": "Not affiliated with or endorsed by Daybreak Game Company, "
                  "Game Jawn or Darkpaw Studios.",
}

STABILITY = [
    "Fields in a vN file are never removed and never change type.",
    "New optional fields may be added; ignore keys you do not recognise.",
    "A breaking change gets a new version at a new URL. The old one stays up.",
    "Values change as evidence improves. That is the product working, not a "
    "breach — watch `hash` if you cache.",
]


def wrap(name, version, title, description, payload, notes=None):
    body = dict(
        name=name, version=version, title=title, description=description,
        source=SITE, schema=f"{SITE}/data/{name}.v{version.split('.')[0]}.json",
        terms=TERMS, stability=STABILITY,
        notes=notes or [],
        data=payload)
    # A content hash rather than a build timestamp: a timestamp would rewrite
    # every file on every build, make the diffs meaningless and trip the stale
    # tree check. This changes only when the data does, which is also the thing
    # a consumer actually wants to cache on.
    body['hash'] = hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False).encode('utf-8')
    ).hexdigest()[:16]
    return body


# ---------------------------------------------------------------- sky --------
def build_sky():
    s = json.load(open('assets/sky.json', encoding='utf-8'))
    src = s['sources']

    def facet(f):
        meta = src.get(f['src'], {})
        return dict(source=f['src'], tier=meta.get('tier'),
                    status=f.get('status', 'ok'),
                    note=f.get('note'))

    classes = {}
    for code, c in s['classes'].items():
        quests = []
        for q in c['quests']:
            quests.append(dict(
                name=q['n'], giver=q['g'], say=q['say'],
                reward=dict(name=q['r'], slot=q['s'], stats=q['st'] or None),
                turnins=[dict(name=i['n'], islands=i['i'], source=i['m'],
                              rune=bool(i.get('rune'))) for i in q['it']],
                provenance={k: facet(v) for k, v in q['p'].items()}))
        verified = all(
            src.get(f['src'], {}).get('tier') is not None
            and src[f['src']]['tier'] <= 2 and f['status'] == 'ok'
            for q in c['quests'] for f in q['p'].values())
        classes[code] = dict(label=c['label'], hub=c['hub'], armor=c['armor'],
                             verified=verified, quests=quests)
    return wrap(
        'sky', '1.0.0', 'Plane of Sky class unlock quests',
        'Every Plane of Sky test for all sixteen classes, with the turn-ins, '
        'the island each component drops on, and a source recorded per claim.',
        dict(sources=src, islands=s['islands'], ladder=s['ladder'],
             order=s['order'], efreeti=s['efreeti'], classes=classes),
        notes=[
            "`verified` is DERIVED, never hand-set: every claim of every quest "
            "must name a source of tier 2 or better with nothing marked "
            "against it. Five of sixteen classes qualify.",
            "Tier 1 is a developer statement, 2 a structured wiki record that "
            "passed a provenance check, 3 a named community guide, 4 an "
            "aggregator, 5 inherited Project 1999 prose.",
            "Six reward stat blocks carry classic percentage haste and are "
            "marked suspect in place. Legends uses a flat attack-speed value.",
        ])


# ---------------------------------------------------------- sightings --------
def build_sightings():
    s = json.load(open('assets/sightings.json', encoding='utf-8'))
    items = {}
    for item, rows in s.get('by_item', {}).items():
        items[item] = [dict(mob=r['mob'], seen=r['n'],
                            off_roster=bool(r.get('off_roster')),
                            sessions=[dict(date=x.get('date'), zone=x.get('zone'),
                                           difficulty=x.get('difficulty'))
                                      for x in r.get('sessions', [])])
                       for r in rows]
    return wrap(
        'sightings', '1.0.0', 'Measured drop sources',
        'Which mobs have been measured dropping which items, parsed from '
        'combat logs. Each row carries the sighting count behind it.',
        dict(items=items),
        notes=[
            "A COUNT, NEVER A RATE. A drop seen once is seen once. Nothing "
            "here supports a drop-rate claim and none is made.",
            "`seen` and `sessions` are the evidence behind a row, not a "
            "published finding. The pages on this site print which mob drops "
            "what and leave the tally here.",
            "`off_roster` means the mob was named by the log rather than by a "
            "survey we had already written.",
            "This is the one dataset in this community that is measured rather "
            "than transcribed. It is also the smallest sample. Both are true.",
        ])


# -------------------------------------------------------------- zones --------
def build_zones():
    z = json.load(open('assets/zones-index.json', encoding='utf-8'))
    # Adding an optional field to a v1 file is allowed by the contract on the
    # file itself: readers ignore keys they do not know. Removing one is not.
    try:
        cov = json.load(open('assets/coverage.json', encoding='utf-8'))['zones']
    except (OSError, ValueError, KeyError):
        cov = {}
    return wrap(
        'zones', '1.0.0', 'Surveyed dungeons',
        'The zones we have surveyed, with the level band, the experience '
        'modifier and how far verification has got.',
        dict(zones=[dict(slug=x['slug'], title=x['title'], levels=x.get('levels'),
                         zem=x.get('zem'), plate=x.get('plate'),
                         verify_level=x.get('verify_level'),
                         verify_gate=x.get('verify_gate'),
                         coverage=cov.get(x['slug'], {}).get('facets'),
                         coverage_score=cov.get(x['slug'], {}).get('score'),
                         url=f"{SITE}/dungeons/{x['slug']}") for x in z]),
        notes=["`coverage` is the useful one: how much of what a PLAYER needs "
               "we hold for the zone - bosses, loot, difficulty behaviour, "
               "which inherited advice is wrong, and farming value. Each facet "
               "is `measured` from our own logs, `sourced` from a document, or "
               "`none`. Computed, never typed.",
               "`verify_level` is sourcing hygiene and a coordinate check, not "
               "a measure of usefulness. Its third gate asks whether plotted "
               "coordinates land on drawn floor, so a zone with no plotted "
               "coordinates can never pass it however much play it gets.",
               "Verified means checked against source. It does not mean "
               "complete."])


# -------------------------------------------------------------- items --------
def build_items():
    try:
        ids = json.load(open('assets/item-ids.json', encoding='utf-8'))['items']
    except (OSError, ValueError, KeyError):
        ids = {}
    return wrap(
        'items', '1.0.0', 'Item names and game IDs',
        "Item name to the game's own numeric item ID, read from "
        "`/outputfile inventory` dumps.",
        dict(items=ids),
        notes=["The ID is stable across the +N upgrade tier and the "
               "(Exaltation) augment form, which makes it a better join key "
               "than a name.",
               "Says an item exists and is spelled exactly so. Says nothing "
               "about its stats or where it drops."])


BUILDERS = [('sky', build_sky), ('sightings', build_sightings),
            ('zones', build_zones), ('items', build_items)]


def main():
    os.makedirs(OUT, exist_ok=True)
    index = []
    for name, fn in BUILDERS:
        body = fn()
        major = body['version'].split('.')[0]
        fname = f"{name}.v{major}.json"
        path = os.path.join(OUT, fname)
        json.dump(body, open(path, 'w', encoding='utf-8', newline='\n'),
                  indent=1, ensure_ascii=False)
        size = os.path.getsize(path)
        index.append(dict(name=name, version=body['version'],
                          title=body['title'], description=body['description'],
                          url=f"{SITE}/data/{fname}", bytes=size,
                          hash=body['hash']))
        print(f"  {fname:22} {size//1024:>5} KB  {body['title']}")

    idx = dict(
        name='index', version='1.0.0',
        title='EQL Source public data',
        description='Versioned, per-claim-sourced EverQuest Legends data, free '
                    'to consume. Nobody else in this community publishes any, '
                    'so we do.',
        source=SITE, terms=TERMS, stability=STABILITY,
        contact=f"{SITE}/credits",
        datasets=index)
    json.dump(idx, open(os.path.join(OUT, 'index.json'), 'w',
                        encoding='utf-8', newline='\n'), indent=1,
              ensure_ascii=False)
    print(f"  {'index.json':22} {os.path.getsize(os.path.join(OUT,'index.json'))//1024:>5} KB"
          f"  {len(index)} datasets")
    return 0


if __name__ == '__main__':
    sys.exit(main())
