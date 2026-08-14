"""Build assets/sky.json — the Plane of Sky dataset, with provenance per claim.

    python3 _build/skydata.py --from-html    # one-time extraction, already done
    python3 _build/skydata.py                # validate the committed file

WHY THIS EXISTS
---------------
An outside audit on 14 August 2026 found six reward tooltips carrying classic
percentage haste inside classes the tracker flagged **verified**. The values
were wrong-ish; the reason they could be wrong was structural.

`v` was one boolean per class. It covered a class's turn-ins, its reward names,
its slots, its stat blocks and its drop sources — thirty-odd separate claims
read from different pages on different days — and it was set by hand. The
turn-ins had been checked. The stat blocks had not. One flag cannot say that,
so it rounded up, and a stat block inherited a badge its neighbours had earned.

PROVENANCE IS PER FACET, NOT PER CLASS
--------------------------------------
A quest makes four claims that can independently be right or wrong, and this
file records a source for each:

    turnins   what you hand in, and what drops it where
    giver     which NPC gives the test and what you say
    reward    the item you get and the slot it fills
    stats     the tooltip on that item

Each names a source id from `sources`, and may carry `status` and `note`.
`sources` holds the tier, the URL, the revision and the date it was read.

**`verified` is now derived and cannot be typed.** A facet counts as verified
when its source is tier 2 or better and its status is ok. A class is verified
only if every facet of every one of its quests is. Under that rule Warrior
stops being verified immediately — its stat blocks were cross-read from
eqlwiki's Warrior_Plane_of_Sky_Tests, a page whose own turn-ins this site
already rejected as classic. Same page, same day, two opposite decisions, and
before today nothing recorded that.

NOTHING HERE IS INVENTED
------------------------
Every source assignment below is what the tracker's own sourcing note already
said in prose. This moves those sentences into the data so the renderer can act
on them; it does not add a single new claim about the game.
"""
import os, re, sys, json, subprocess, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

OUT = 'assets/sky.json'
HTML = '_build/source/eql-sky-tracker.html'

# ---------------------------------------------------------------------------
# The sources, exactly as the tracker's sourcing note describes them.
SOURCES = {
    "wiki-sky-151528": dict(
        tier=2, name="eqlwiki, Plane of Sky", rev="151528",
        url="https://eqlwiki.com/Plane_of_Sky", read="2026-06-28",
        note="Revision post-dates the 28 July 2026 launch check; used for "
             "turn-ins, givers and reward names throughout."),
    "wiki-warrior-tests": dict(
        tier=5, name="eqlwiki, Warrior Plane of Sky Tests",
        url="https://eqlwiki.com/Warrior_Plane_of_Sky_Tests", read="2026-06-28",
        note="Warrior stat blocks were cross-read from here. The SAME page's "
             "turn-ins were rejected as classic and are not used, which is the "
             "reason this source is tier 5 and not tier 2."),
    "forge-2026-08-02": dict(
        tier=4, name="EQL Build Forge item snapshot", read="2026-08-02",
        note="Community aggregator, snapshot-dated. Supplies a few partial "
             "stat lines."),
    "unsourced": dict(
        tier=None, name="No confirmed Legends-era source",
        note="The turn-ins for these classes are Legends-current; the reward "
             "tooltip has no source we are willing to stand behind."),
}

# Which source each facet comes from. Read off the tracker's own note.
STATS_SOURCE = collections.defaultdict(lambda: "wiki-sky-151528", {
    "WAR": "wiki-warrior-tests",
    "RNG": "unsourced", "ROG": "unsourced", "SHD": "unsourced",
    "SHM": "unsourced", "WIZ": "unsourced",
})
FLAT = "wiki-sky-151528"          # turn-ins, givers and reward names


def facet(src, status="ok", note=None):
    f = dict(src=src, status=status)
    if note:
        f['note'] = note
    return f


def extract_from_html():
    """Evaluate the tracker's own constants with node. Faithful by
    construction: the file's literals are executed, never retyped."""
    js = r'''
const fs=require('fs');
const src=fs.readFileSync(process.argv[2],'utf8');
const start=src.indexOf('const ISLANDS=');
const marker='\n/* ==================== ';
let end=src.indexOf(marker, src.indexOf('const CLASSES='));
if(end<0) end=src.length;
const fn=new Function(src.slice(start,end)+'\nreturn {ISLANDS,LADDER,EF,EFM,CLASSES};');
process.stdout.write(JSON.stringify(fn()));
'''
    tmp = os.path.join(ROOT, '_skyx.js')
    open(tmp, 'w', encoding='utf-8', newline='\n').write(js)
    try:
        raw = subprocess.run(['node', tmp, HTML], capture_output=True,
                             text=True, encoding='utf-8', check=True).stdout
    finally:
        os.remove(tmp)
    return json.loads(raw)


def build(raw):
    classes = {}
    for code, c in raw['CLASSES'].items():
        quests = []
        for q in c['q']:
            st = (q.get('st') or '').strip()
            ssrc = STATS_SOURCE[code]
            if not st:
                stats = facet("unsourced", "unsourced",
                              "no Legends tooltip recorded")
            elif q.get('sus'):
                stats = facet(ssrc, "suspect", q['sus'])
            else:
                stats = facet(ssrc)
            quests.append(dict(
                n=q['n'], g=q.get('g', ''), say=q.get('say', ''),
                r=q.get('r', ''), s=q.get('s', ''), st=st,
                it=q['it'],
                p=dict(turnins=facet(FLAT), giver=facet(FLAT),
                       reward=facet(FLAT), stats=stats)))
        classes[code] = dict(label=c['label'], abbr=c['abbr'], hub=c['hub'],
                             armor=c['armor'], quests=quests)
    # The order the class picker lists them in. This was a separate top-level
    # constant sitting just past CLASSES, it went out with the block that was
    # replaced, and the picker rendered nothing for a day because ORDER.map on
    # an undefined ORDER throws before a single button is built. It belongs
    # with the data it orders.
    order = sorted(raw['CLASSES'], key=lambda k: raw['CLASSES'][k]['label'])
    return dict(
        _comment=[
            "The Plane of Sky dataset, with a source recorded per claim.",
            "Generated once from the tracker's own constants and hand-maintained",
            "here since. _build/skydata.py validates it; the tracker page is",
            "rendered FROM it, so the page cannot disagree with the data.",
            "",
            "'verified' is derived, never typed. See skydata.py for why.",
        ],
        sources=SOURCES,
        islands=raw['ISLANDS'], ladder=raw['LADDER'], order=order,
        efreeti=dict(islands=raw['EF'], mobs=raw['EFM']),
        classes=classes)


# ---------------------------------------------------------------------------
def verified_facets(sky):
    """A facet is verified when its source is tier 2 or better and nothing is
    wrong with it. Derived here and nowhere else."""
    def ok(f):
        t = sky['sources'][f['src']].get('tier')
        return f['status'] == 'ok' and t is not None and t <= 2
    return ok


def summarise(sky):
    ok = verified_facets(sky)
    rows = []
    for code, c in sky['classes'].items():
        facets = [f for q in c['quests'] for f in q['p'].values()]
        good = sum(1 for f in facets if ok(f))
        rows.append((code, c['label'], good, len(facets),
                     all(ok(f) for f in facets)))
    return rows


# DATASET INVARIANTS.
# Three independent projects - eqlegendstools, loadoutlegends and EQBuddy -
# land on these same counts, which is the strongest validation available
# without client access. An outside audit listed them on 14 August 2026 and I
# first reported they did not reproduce; that was my error, from counting with
# a regex that missed the efreeti-set helper instead of evaluating the data.
# Evaluated, they match exactly. A correction that changes one of these is a
# finding that needs a deliberate note, not a silent edit.
INVARIANTS = dict(classes=16, quests=95, turnin_slots=222,
                  unique_turnins=128, contested=29, islands=10)


def validate(sky):
    """What the old shape made impossible. Every one of these is a fault the
    dataset could previously carry with nothing to catch it."""
    bad = []
    names = [i['n'] for c in sky['classes'].values() for q in c['quests']
             for i in q['it']]
    got = dict(classes=len(sky['classes']),
               quests=sum(len(c['quests']) for c in sky['classes'].values()),
               turnin_slots=len(names), unique_turnins=len(set(names)),
               contested=sum(1 for v in collections.Counter(names).values() if v > 1),
               islands=len(sky['islands']))
    for k, want in INVARIANTS.items():
        if got[k] != want:
            bad.append(f"invariant {k}: {got[k]}, expected {want}. If this is a "
                       f"deliberate correction, update INVARIANTS and say why.")
    # The page reads these keys off the top of the dataset. A missing one is
    # not a data problem, it is a blank tool - which is exactly how the class
    # picker shipped empty.
    for k in ('sources', 'islands', 'ladder', 'order', 'efreeti', 'classes'):
        if k not in sky:
            bad.append(f"sky.json has no {k!r}; the tracker reads it at load")
    if set(sky.get('order', [])) != set(sky['classes']):
        bad.append("order and classes disagree: "
                   f"{sorted(set(sky['classes']) - set(sky.get('order', [])))} missing "
                   f"from order")
    slots = collections.Counter()
    for code, c in sky['classes'].items():
        for q in c['quests']:
            where = f"{code} / {q['n']}"
            if not q['it']:
                bad.append(f"{where}: no turn-in items")
            for f_name, f in q['p'].items():
                if f['src'] not in sky['sources']:
                    bad.append(f"{where}: {f_name} names unknown source {f['src']!r}")
                if f['status'] not in ('ok', 'suspect', 'unsourced'):
                    bad.append(f"{where}: {f_name} has status {f['status']!r}")
            if q['s']:
                slots[q['s']] += 1
            for it in q['it']:
                for isl in it['i']:
                    if isl not in sky['islands']:
                        bad.append(f"{where}: item {it['n']!r} names island {isl!r}")
            # a stat block with a source but no text, or text but no source
            if q['st'] and q['p']['stats']['status'] == 'unsourced':
                bad.append(f"{where}: has a stat block but stats are marked unsourced")
    # SLOT SANITY.
    # A name that says bracelet should not sit in a waist slot. Matched on whole
    # words against the slot vocabulary the data actually uses, because the
    # first version read "ring" inside "Earring" and reported seven items that
    # were perfectly fine. A validator that cries wolf gets switched off.
    EXPECT = {'bracelet': {'Wrist', 'Back / Wrist'},
              'bracer': {'Wrist', 'Back / Wrist'},
              'ring': {'Finger'}, 'earring': {'Ear'}, 'boots': {'Feet'},
              'helm': {'Head'}, 'cloak': {'Back', 'Back / Wrist'},
              'mask': {'Face'}, 'necklace': {'Neck'}, 'girdle': {'Waist'},
              'sash': {'Waist'}, 'belt': {'Waist'}}
    for code, c in sky['classes'].items():
        for q in c['quests']:
            if not q['s']:
                continue
            words = set(re.findall(r"[a-z]+", q['r'].lower()))
            for word, allowed in EXPECT.items():
                if word in words and q['s'] not in allowed:
                    # A fault we have already marked is not a build failure.
                    # We do not know the right slot and will not guess one, so
                    # the honest handling is the same as the haste figures:
                    # keep the value, mark it, and say what would settle it.
                    if q['p']['reward']['status'] != 'ok':
                        continue
                    bad.append(f"{code} / {q['n']}: {q['r']!r} sits in slot "
                               f"{q['s']!r} — a {word} belongs in "
                               f"{' or '.join(sorted(allowed))}. Mark the "
                               f"reward facet suspect if this is known.")
    return bad


def main():
    if '--from-html' in sys.argv:
        sky = build(extract_from_html())
        json.dump(sky, open(OUT, 'w', encoding='utf-8', newline='\n'),
                  indent=1, ensure_ascii=False)
        print(f"{OUT} written from {HTML}")
    else:
        sky = json.load(open(OUT, encoding='utf-8'))

    nq = sum(len(c['quests']) for c in sky['classes'].values())
    ni = sum(len(q['it']) for c in sky['classes'].values() for q in c['quests'])
    names = [i['n'] for c in sky['classes'].values() for q in c['quests']
             for i in q['it']]
    cnt = collections.Counter(names)
    print(f"  {len(sky['classes'])} classes, {nq} quests, {ni} turn-in slots, "
          f"{len(set(names))} unique, {sum(1 for v in cnt.values() if v > 1)} contested")

    print("\n  verified facets per class (derived, not typed):")
    for code, label, good, tot, allok in sorted(summarise(sky),
                                                key=lambda r: (-r[2] / r[3], r[0])):
        mark = 'verified' if allok else ''
        print(f"    {code}  {label:14} {good:>3}/{tot:<3} {mark}")

    bad = validate(sky)
    if bad:
        print(f"\n  {len(bad)} validation failure(s):")
        for b in bad:
            print("    -", b)
        return 1
    print("\n  validation: clean")
    return 0


if __name__ == '__main__':
    sys.exit(main())
