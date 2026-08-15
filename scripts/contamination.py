"""Find classic EverQuest fingerprints in our own published content.

    python3 scripts/contamination.py            # report
    python3 scripts/contamination.py --write    # report and write the data file

WHY THIS POINTS AT US FIRST
---------------------------
Large parts of every EverQuest Legends reference — ours included — are Project
1999 text describing a game that stopped existing in 2001. This site's whole
claim is that it can tell the difference. On 14 August 2026 an outside audit
found six classic haste figures sitting inside our own *verified* tier, which
is the strongest possible argument that the claim needs a tool behind it rather
than a habit.

**The order matters and is not negotiable.** A scanner that only finds other
people's contamination is an attack ad. This one runs against eqlsource and
publishes what it finds here. If it is ever pointed outward, it is pointed here
first and the results go up either way.

WHAT A FINGERPRINT IS, AND WHAT IT IS NOT
-----------------------------------------
A hit is **not** proof of an error. Legends kept a great deal of classic
EverQuest intact, and several of these patterns are perfectly current. A hit
means *this figure carries a convention from a game whose numbers we know
changed, and nobody has checked this one*. That is a question, not a verdict,
and the report says so on every line.

The useful distinction is not right against wrong. It is **marked against
unmarked**. A classic figure that carries a T5 badge and a note is doing its
job. The same figure printed bare is the fault this site exists to prevent, and
that is what the `unmarked` count at the end of the report counts.
"""
import os, re, sys, json, glob, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

OUT = 'assets/contamination.json'

# ---------------------------------------------------------------------------
# Each signature: what it matches, what classic did, what Legends does, and how
# sure we are that a hit is actually wrong. `certainty` is about the MECHANIC,
# not about any individual hit.
#   changed     the mechanic itself demonstrably differs in Legends, so a hit
#               is very likely a wrong number and is worth acting on
#   convention   a classic FORMAT. Usually harmless and often still current;
#               useful only in aggregate, as a measure of how much of a page
#               was transcribed from a classic-era record
#
# Keeping these apart is the difference between a report and a pile. The first
# run mixed them and produced 315 findings, 296 of which were the word "SV".
SIGNATURES = [
    dict(id='haste-pct', certainty='changed',
         pattern=r'\bHaste\s*\+\s*\d+\s*%',
         classic='Haste was a percentage that divided weapon delay.',
         legends='Legends uses a flat value on an attack-speed stat. EQL Tools '
                 'documents it; eqlwiki still carries the classic formula, so '
                 'the two best sources in the field disagree.',
         settle='One screenshot of a Legends haste tooltip.'),
    dict(id='charges', certainty='convention',
         pattern=r'\(\s*\d+\s*charges?\s*\)',
         classic='Classic printed a charge count in brackets on clickable items.',
         legends='Nobody has published whether Legends keeps charge counts or '
                 'the same numbers.',
         settle='One screenshot of a clickable item tooltip.'),
    dict(id='sv-resist', certainty='convention',
         pattern=r'\bSV\s+(?:MAGIC|FIRE|COLD|DISEASE|POISON|ALL)\b',
         classic='Classic stat blocks abbreviated resists as SV MAGIC +N.',
         legends='The abbreviation may well be current. Its presence marks a '
                 'block transcribed from a classic-era record, which is worth '
                 'knowing even when the number is right.',
         settle='Compare one block against the item in game.'),
    dict(id='nodrop', certainty='convention',
         pattern=r'\bNO\s*DROP\b|\bLore\s+Equipped\b',
         classic='Classic flag wording on item records.',
         legends='Legends may use different wording. Unchecked.',
         settle='One screenshot of an item tooltip carrying the flag.'),
    # A tell CLAUDE.md already names as diagnostic of classic text. Written
    # first as "any small number followed by 'players'", which matched "Three
    # player-made Najena maps were consulted" - sourcing prose about map
    # credits. A raid word has to be present and the number has to exceed the
    # cap, or this finds ordinary English.
    dict(id='raid-size', certainty='changed',
         pattern=r'\b(?:dozens?\s+of\s+(?:players?|people)'
                 r'|(?:9|\d{2,})\s+(?:players?|people|raiders?)'
                 r'|(?:full\s+)?raid\s+of\s+(?:\d{2,}|dozens?))\b',
         classic='Classic raids ran to dozens of players, and advice was sized '
                 'for them.',
         legends='Legends caps a raid at 8. Anything sized larger is inherited '
                 'and describes nothing about this game.',
         settle='Nothing — the cap is published.'),
    # A `plat-cost` signature was here and has been removed. It matched any
    # three-digit platinum figure, which is not a classic fingerprint: it hit
    # "over 1600 plat of ore" for the Iksar unlock and "around 100 to 120
    # platinum" for a key in The Hole, both sourced, both hedged, both fine.
    # A signature that cannot distinguish a classic import from an ordinary
    # sourced price is not measuring contamination.
]

# Where our claims live. The archive is excluded deliberately: it republishes
# retired plates verbatim and is marked, noindexed and explained as history.
SURFACES = [
    ('_build/source/*.html', 'survey and tool sources'),
    ('assets/sky.json', 'Plane of Sky dataset'),
    ('assets/planar.json', 'planar armour sets'),
    ('assets/index-data.json', 'mined item and mob catalogue'),
    ('assets/motes.json', 'mote values'),
]
SKIP = ('assets/archive-plates.json',)

# A hit inside one of these is already declared below tier 2 at the point of
# use, so it is marked rather than bare.
MARKERS = (r'class="tier t[345]"', r'class="tier tC"', r'\bsus\s*:', r'"status"\s*:\s*"suspect"',
           r'classic-era', r'Suspect figure', r'not confirmed for Legends',
           r'inherited', r'Project 1999', r'\bT5\b', r'\bT4\b', r'\bT3\b')
MARKER_RE = re.compile('|'.join(MARKERS), re.I)
WINDOW = 400          # chars either side of a hit to look for a marker


def scan_text(text, sig):
    rx = re.compile(sig['pattern'], re.I)
    for m in rx.finditer(text):
        a, b = max(0, m.start() - WINDOW), min(len(text), m.end() + WINDOW)
        yield m.group(0).strip(), bool(MARKER_RE.search(text[a:b]))


def scan_json(data, sig):
    """Structural scan for a JSON surface.

    Proximity is the wrong test in structured data. In sky.json a stat block
    and the provenance that marks it are 589 characters apart, because the
    quest's turn-in list sits between them - so a text window either misses the
    marker or has to be widened until it starts crediting unrelated ones. All
    six suspect haste figures read as unmarked.

    So: walk the tree, and judge a hit by the object that CONTAINS it.
    """
    rx = re.compile(sig['pattern'], re.I)

    def marked(obj):
        return bool(MARKER_RE.search(json.dumps(obj, ensure_ascii=False)))

    def walk(node, holder):
        if isinstance(node, dict):
            for v in node.values():
                yield from walk(v, node)
        elif isinstance(node, list):
            for v in node:
                yield from walk(v, holder)
        elif isinstance(node, str):
            for m in rx.finditer(node):
                yield m.group(0).strip(), marked(holder)

    yield from walk(data, data if isinstance(data, dict) else {})


def main():
    findings = collections.defaultdict(lambda: dict(marked=0, unmarked=0,
                                                    files=collections.Counter(),
                                                    samples=[]))
    scanned = []
    for pattern, label in SURFACES:
        for path in sorted(glob.glob(pattern)):
            if path.replace(os.sep, '/') in SKIP:
                continue
            try:
                text = open(path, encoding='utf-8').read()
            except OSError:
                continue
            scanned.append(path)
            data = None
            if path.endswith('.json'):
                try:
                    data = json.loads(text)
                except ValueError:
                    data = None
            for sig in SIGNATURES:
                hits = (scan_json(data, sig) if data is not None
                        else scan_text(text, sig))
                for hit, marked in hits:
                    f = findings[sig['id']]
                    f['marked' if marked else 'unmarked'] += 1
                    f['files'][path] += 1
                    if len(f['samples']) < 6 and not marked:
                        f['samples'].append(dict(file=path, text=hit))

    by_id = {s['id']: s for s in SIGNATURES}
    total_u = sum(f['unmarked'] for f in findings.values())
    total_m = sum(f['marked'] for f in findings.values())

    print(f"scanned {len(scanned)} files across {len(SURFACES)} surfaces")
    rows = []
    for level, heading in (
            ('changed', 'MECHANICS WE KNOW CHANGED — a hit here is probably a '
                        'wrong number'),
            ('convention', 'CLASSIC FORMATS — usually harmless, useful as a '
                           'measure of how much was transcribed')):
        print(f"\n  {heading}")
        print(f"  {'signature':14}{'unmarked':>9}{'marked':>8}   where")
        for sig in (s for s in SIGNATURES if s['certainty'] == level):
            f = findings.get(sig['id'])
            if not f:
                print(f"    {sig['id']:12}{0:9}{0:8}   none")
                continue
            where = ', '.join(os.path.basename(p) for p, _ in f['files'].most_common(3))
            print(f"    {sig['id']:12}{f['unmarked']:9}{f['marked']:8}   {where}")
            rows.append(dict(
                id=sig['id'], certainty=sig['certainty'],
                classic=sig['classic'], legends=sig['legends'], settle=sig['settle'],
                unmarked=f['unmarked'], marked=f['marked'],
                files={p: n for p, n in f['files'].most_common()},
                samples=f['samples']))

    act = sum(f['unmarked'] for i, f in findings.items()
              if next(s for s in SIGNATURES if s['id'] == i)['certainty'] == 'changed')
    print(f"\n  {act} unmarked hits on mechanics we know changed. "
          f"{total_u - act} more are formats.")
    print(f"  {total_m} carry a badge already and are doing their job.")

    for sig in SIGNATURES:
        f = findings.get(sig['id'])
        if not f or not f['samples'] or sig['certainty'] != 'changed':
            continue
        print(f"\n  {sig['id']} — every unmarked hit:")
        for s in f['samples']:
            print(f"     {s['file']}: {s['text'][:70]}")

    if '--write' in sys.argv:
        json.dump(dict(
            _comment=[
                "What our own published content looks like when scanned for",
                "classic EverQuest conventions. Generated by",
                "scripts/contamination.py, hand-run.",
                "",
                "A hit is a question, not a verdict: Legends kept much of",
                "classic intact. What matters is marked against unmarked.",
            ],
            scanned=len(scanned), unmarked=total_u, marked=total_m,
            signatures=rows),
            open(OUT, 'w', encoding='utf-8', newline='\n'), indent=1,
            ensure_ascii=False)
        print(f"\n  wrote {OUT}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
