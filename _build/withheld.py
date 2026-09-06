"""Coordinates we hold but will not publish as positions, and why.

WHY THIS MODULE EXISTS
On 8 August 2026 six Najena coordinates were found sitting far outside the
zone's own drawn floor - 142 to 513 units, re-derived 6 Sep 2026, and see
REASON below for why no figure is typed here either.
They were withheld from the survey plot and
the reason was written up in the change log — and then they carried on printing
as bare coordinates in the named roster on the plate, which is the table a
reader actually navigates by. The withholding existed in the change log and in
the plot. It did not exist where the reader was.

So the set lives here, one place, and:

  - _build/build6.py skips these when plotting,
  - _build/build3.py rewrites their coordinate cells as the plate is built,
  - scripts/check.py fails the build if a withheld coordinate reaches a page.

A withheld coordinate is not deleted. The mob keeps its row, its level, its
class and its notes; only the position is replaced, by a statement that we do
not have one we trust. Deleting the row would be the dishonest version.
"""

# (zone slug, mob name as it appears on the plate)
WITHHELD = {
    ('najena', 'Rathyl'),
    ('najena', 'Ekeros'),
    ('najena', 'BoneCracker'),
    ('najena', 'Officer Grush'),
    ('najena', 'Trazdon'),
    ('najena', 'A Visiting Priestess'),
}

# TWO QUANTITIES, AND THE NOTE USED TO NAME ONE AND PRINT THE OTHER.
#
# "57 to 513" was the distance these sit outside the zone's north-south EXTENT.
# The sentence around it named the distance from the DRAWN FLOOR, which is the
# quantity the check actually uses, and that range is 142 to 513. Both numbers
# are true about something; the sentence was true about neither. Found by the
# pre-relaunch audit on 6 Sep 2026 and fixed by deriving rather than by
# swapping one literal for another - the count and both bounds now come out of
# the same data the plot is checked against.
#
# The names are read here too. "Six coordinates" was typed in four places
# against a set of six, and would have kept saying six.
def _measure(slug):
    """Distance from each withheld position to the nearest drawn floor edge.

    Deliberately NOT imported from build6: importing a generator runs it, and
    CLAUDE.md records that costing a truncated dataset. This is eight lines of
    geometry and a copy is cheaper than the coupling.
    """
    import json, math, re
    num = re.compile(r'[-−]?\d+(?:\.\d+)?')
    try:
        geo = json.load(open('assets/zone-geometry.json', encoding='utf-8'))
        ix = json.load(open('assets/index-data.json', encoding='utf-8'))
    except (OSError, ValueError):
        return []
    segs = [s for L in geo.get(slug, {}).get('layers', [])
            for c in L['lines'] for s in zip(c, c[1:])]
    if not segs:
        return []
    out = []
    for n in ix.get('named', []):
        if n.get('z') != slug or (slug, n.get('n')) not in WITHHELD:
            continue
        v = [float(t.replace('−', '-')) for t in num.findall(n.get('loc') or '')]
        if len(v) < 2:
            continue
        px, py = -v[1], -v[0]
        best = None
        for a, b in segs:
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = dx * dx + dy * dy
            t = 0.0 if L == 0 else max(0.0, min(1.0, ((px - a[0]) * dx + (py - a[1]) * dy) / L))
            d = math.hypot(px - (a[0] + t * dx), py - (a[1] + t * dy))
            best = d if best is None else min(best, d)
        out.append(best)
    return out


# _partials.wordnum already does this, with the same numeral fallback, and a
# second copy would be the fault this module is being edited to remove. Re-
# exported rather than re-implemented so build3 and build14 have one name to
# import alongside the set itself.
from _partials import wordnum as word


def count(slug):
    """How many coordinates this zone withholds. Four pages typed it."""
    return sum(1 for z, _ in WITHHELD if z == slug)


_NAJENA = _measure('najena')
_N = count('najena')
_WORD = word(_N)
_RANGE = (f'{min(_NAJENA):.0f} to {max(_NAJENA):.0f} units' if _NAJENA
          else 'a distance we could not measure on this build')

# One reason per zone, printed under the table it affects.
REASON = {
    'najena': (
        f'{_WORD} coordinates on this plate are withheld. Every recorded position on '
        f'the site is checked against the walkable floor extracted from the game’s own '
        f'mesh files, and these {_WORD.lower()} land {_RANGE} outside it — outside the '
        'zone, not merely off a walkway. The mobs are real and the rest of their '
        'records stand; the positions are not ones we are willing to send anyone to. '
        'A <code>/loc</code> reading taken standing on any of them would close this.'),
}

# What replaces the coordinate in a roster cell.
MARK = '<span class="wh">withheld</span>'
