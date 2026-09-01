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
    # THE TWO LARGEST FAMILIES, AND THE SCANNER HAD NO SIGNATURE FOR EITHER.
    #
    # Until now it defined five, and reported "0 unmarked" — a true statement
    # about those five and SILENT about the two that account for most of the
    # inherited data on this site. A number that cannot come back non-zero for a
    # family is not a measurement of that family.
    #
    # Neither can be reached by carrying badge markup through extraction, which
    # is why they need their own signatures: the 15 graded cells carry a span,
    # and these carry their provenance as a SENTENCE in the parent survey. A
    # sentence does not survive extraction into a catalogue page.
    #
    # Patterns use character classes rather than backslash escapes throughout,
    # because this file is edited through shells that eat them.
    # A `spawn-pct` signature was written here and WITHDRAWN before shipping,
    # and the reason is recorded so nobody writes it again the same way.
    #
    # The family is real: roughly 90 inherited per-kill spawn percentages sit in
    # named-mob Notes cells, carried from classic wikis, describing nothing about
    # this game. They are the largest inherited family on the site and they are
    # NOT reachable by carrying badge markup through extraction, because their
    # provenance is a sentence in the parent survey and a sentence does not
    # survive into a catalogue page.
    #
    # WHAT DEFEATED THE SIGNATURE: a bare percentage pattern matches layout.
    # Stripping <style> and <script> is not enough, because the percentages that
    # ruin it live in ATTRIBUTES - `style="left:63.48%;top:39.85%"` on every
    # locator mark, `width="100%"` on every rule. Measured: 233 named pages
    # against a true family of about 90, and the extra 143 are stylesheet
    # arithmetic. Session 0 got the identical 233 independently.
    #
    # The scope that would work is the audit's - percentages in Notes that are
    # inherited - and expressing it needs a TEXT-ONLY scan. That conflicts with
    # marker detection, which reads `class="tier t5"` out of the markup: strip
    # the tags and the markers go with them. Resolving that is a real change to
    # how this file reads a page, not a pattern tweak.
    #
    # So the family is NAMED AND UNMEASURED rather than badly measured. A wrong
    # number in a published report is worse than a stated gap, which is the whole
    # argument of /learn/contamination.
    dict(id='rarity-word', certainty='convention',
         pattern=r'[(](?:rare|common|uncommon)[)]',
         classic='Classic loot tables graded every drop rare, common or '
                 'uncommon.',
         legends='These are the wiki word, not a measurement. Nothing here has '
                 'counted a drop against the kills that produced it.',
         settle='The same thing the percentages need: a count and a '
                'denominator.'),
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
    # THE BUILT TREE, WHICH THIS SCANNER NEVER LOOKED AT.
    #
    # Every surface below is a build INPUT. So this measured the layer
    # BEFORE the damage: extract.py stripped a tier badge's markup and left
    # its letters, 'Haste +10% T5' shipped to 675 catalogue pages and into
    # the meta descriptions Google shows, and a scanner whose whole purpose
    # is finding classic conventions in our own published content could not
    # see it, because our own published content was not on the list.
    #
    # A self-audit that reads the sources and not the output is checking
    # what we meant rather than what we said.
    ('public/**/*.html', 'every published page'),
    ('_build/source/*.html', 'survey and tool sources'),
    ('assets/sky.json', 'Plane of Sky dataset'),
    ('assets/planar.json', 'planar armour sets'),
    ('assets/index-data.json', 'mined item and mob catalogue'),
    ('assets/motes.json', 'mote values'),
]
# public/app/ holds applications built in OTHER repositories and copied in
# verbatim under a content hash. Their contents are not ours to write and not
# ours to fix, so reporting their figures as our contamination would be
# misattribution AND unactionable - and this file exists because a scanner
# that finds other people's rot is an attack ad. They are published by us and
# a reader does see them; that is a question for their own repositories, and
# the Sky Ledger's is where it has to be asked.
SKIP = ('assets/archive-plates.json',)
SKIP_PREFIX = ('public/app/',)

# A hit inside one of these is already declared below tier 2 at the point of
# use, so it is marked rather than bare.
MARKERS = (r'class="tier t[345]"', r'class="tier tC"', r'\bsus\s*:', r'"status"\s*:\s*"suspect"',
           r'classic-era', r'Suspect figure', r'not confirmed for Legends',
           r'inherited', r'Project 1999', r'\bT5\b', r'\bT4\b', r'\bT3\b')
# A HEADING THAT DECLARES THE CONTENT CLASSIC IS A MARKER, and a stronger one
# than a badge. /learn/still-true is built as two columns, "What classic did"
# against "What Legends does", so a classic haste percentage under that
# heading is the page doing its job rather than the site asserting a stale
# figure. Without this the scanner reported its own explainer as
# contamination - a false positive inside a report we publish.
MARKERS = MARKERS + ('What classic did',)

MARKER_RE = re.compile('|'.join(MARKERS), re.I)
WINDOW = 400          # chars either side of a hit to look for a marker


CODE = re.compile(r'<(script|style)\b.*?</\1>', re.S | re.I)


def scan_text(text, sig):
    """Hits in a signature's pattern, each with whether it is declared nearby.

    STYLE AND SCRIPT ARE REMOVED FIRST, and that is not tidiness. A percentage
    signature run over a page's raw bytes matches `width:100%` and
    `color-mix(in srgb, var(--c) 58%, ...)` in the inline stylesheet - a
    thousand hits of stylesheet arithmetic reported as inherited game data. The
    five older signatures escaped it by luck rather than design: none of their
    patterns happen to occur in CSS.

    `exclude` lets a signature reject a hit by its CONTEXT rather than by a
    lookbehind. The bare-rate pattern has to match a percentage anywhere, and
    the site prints two of its own - a zone ZEM and item haste - which are not
    inherited and must not be counted as such.
    """
    rx = re.compile(sig['pattern'], re.I)
    ex = re.compile(sig['exclude'], re.I) if sig.get('exclude') else None
    body = CODE.sub(' ', text)
    for m in rx.finditer(body):
        a, b = max(0, m.start() - WINDOW), min(len(body), m.end() + WINDOW)
        if ex and ex.search(body[max(0, m.start() - 70):m.end() + 25]):
            continue
        yield m.group(0).strip(), bool(MARKER_RE.search(body[a:b]))


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
        for path in sorted(glob.glob(pattern, recursive=True)):
            _p = path.replace(os.sep, '/')
            if _p in SKIP or _p.startswith(SKIP_PREFIX):
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
