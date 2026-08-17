"""Phrases the surveys must not type for themselves.

Imported by `_build/build3.py`, which substitutes these tokens into every
survey as it imports it. Writes no file of its own.

WHY THIS EXISTS
---------------
On 17 August 2026 a cold reader found that The Ruins of Old Paineel called
itself "the highest zone experience modifier in the game" in its H1, its meta
description, its Open Graph card and its Twitter card. Kedge Keep is 139. The
Hole is 128, level with Lair of the Splitpaw and The Warrens. The wrong claim
was the one travelling off-site on a share card.

The first repair replaced one typed superlative with four typed ordinals, which
is the same fault with better arithmetic: nothing in `check.py` or `gate.py`
notices when a fourteenth survey lands above 128, and the pages go stale in
silence exactly as they did before.

So a page asks for `@@ZEM_RANK@@` and gets a sentence computed from
`assets/zones-index.json` at build time. A re-ranked zone moves every page that
mentions the ranking on the next build, which is the property the site claims to
have and did not.

WHAT IT WILL NOT SAY
--------------------
**Never "in the game".** We have surveyed 13 zones. Ranking what we have not
measured is the invented number this project's first rule forbids, and it is how
the original claim came to be wrong. Every phrase here is bounded to our own
surveys and says so.
"""
import json
import os

_CACHE = {}
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _zones():
    if 'z' in _CACHE:
        return _CACHE['z']
    try:
        raw = json.load(open(os.path.join(_ROOT, 'assets', 'zones-index.json'),
                             encoding='utf-8'))
    except (OSError, ValueError):
        return []
    _CACHE['z'] = raw['zones'] if isinstance(raw, dict) else raw
    return _CACHE['z']


def _title(slug):
    for z in _zones():
        if z.get('slug') == slug:
            return z.get('title') or slug
    return slug


def _listed(titles):
    """"A, B and C" — the site writes lists out rather than using an ampersand."""
    titles = list(titles)
    if not titles:
        return ''
    if len(titles) == 1:
        return titles[0]
    return ', '.join(titles[:-1]) + ' and ' + titles[-1]


def zem_rank(slug):
    """Where a zone's experience modifier sits among the ones we have surveyed.

    Returns a bare clause, no leading capital and no full stop, so a page can
    set it inside a sentence of its own. Ties are named rather than broken:
    three zones share 128 and a page that called one of them "second" without
    saying so would be technically true and practically misleading.
    """
    key = ('zem', slug)
    if key in _CACHE:
        return _CACHE[key]

    zs = [z for z in _zones() if isinstance(z.get('zem'), (int, float))]
    if not zs:
        return 'not recorded'
    me = next((z for z in zs if z.get('slug') == slug), None)
    if me is None:
        return 'not recorded'

    # Rank over DISTINCT values, so three zones tied on 128 all sit at the same
    # place and the zone below them is third rather than fifth.
    values = sorted({z['zem'] for z in zs}, reverse=True)
    place = values.index(me['zem']) + 1
    peers = [_title(z['slug']) for z in zs
             if z['zem'] == me['zem'] and z.get('slug') != slug]
    ordinal = {1: 'highest', 2: 'second-highest', 3: 'third-highest',
               4: 'fourth-highest', 5: 'fifth-highest', 6: 'sixth-highest',
               7: 'seventh-highest', 8: 'eighth-highest', 9: 'ninth-highest',
               10: 'tenth-highest'}.get(place, f'number {place} of')

    # KEPT SHORT ON PURPOSE. The phrase this replaced ran to nineteen words and
    # named every tied zone and the leader, on a site whose brief is that a page
    # should carry "only the most pure, most refined information". "Joint" says
    # a tie exists; a reader who wants the whole ranking has the dungeon index.
    n = len(zs)
    if place == 1:
        out = (f'joint {ordinal} of our {n} surveys' if peers
               else f'the {ordinal} of our {n} surveys')
    else:
        top = max(z['zem'] for z in zs)
        leader = _listed(sorted(_title(z['slug']) for z in zs if z['zem'] == top))
        joint = 'joint ' if peers else 'the '
        out = f'{joint}{ordinal} of our {n} surveys, behind {leader}'
    _CACHE[key] = out
    return out


def zem_leaders():
    """"Kedge Keep" or "A, B and C" — whoever currently holds the top figure."""
    zs = [z for z in _zones() if isinstance(z.get('zem'), (int, float))]
    if not zs:
        return 'not recorded'
    top = max(z['zem'] for z in zs)
    return _listed(sorted(_title(z['slug']) for z in zs if z['zem'] == top))


def _raids():
    if 'r' in _CACHE:
        return _CACHE['r']
    try:
        _CACHE['r'] = json.load(open(os.path.join(_ROOT, 'assets',
                                                  'raids-measured.json'),
                                     encoding='utf-8'))
    except (OSError, ValueError):
        _CACHE['r'] = []
    return _CACHE['r']


WORDS = {0: 'none', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
         6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten'}


def measured_of(names):
    """"five of the seven" — how many named bosses we have actually parsed.

    The Plane of Fear page said "the raid targets named above have been killed
    and parsed" over a table of seven, two of which appear in no log we hold.
    A page may name what it has measured; it may not imply it measured a table.
    """
    have = {r['boss'] for r in _raids()}
    hit = sum(1 for n in names if n in have)
    total = len(names)
    if hit == total:
        return 'both' if total == 2 else f'all {WORDS.get(total, total)}'
    return f'{WORDS.get(hit, hit)} of the {WORDS.get(total, total)}'


def raid_fight_count():
    return len(_raids())


FEAR_TARGETS = ('Cazic-Thule', 'Dread', 'Fright', 'Terror', 'a dracoliche',
                'Wraith of a Shissir', 'Irak Altil')
HATE_TARGETS = ('Innoruuk, the Prince of Hate', 'Maestro of Rancor')


def tokens(slug):
    """Every substitution offered to a survey, whether or not it uses them."""
    return [
        ('@@ZEM_RANK@@', zem_rank(slug)),
        ('@@ZEM_LEADER@@', zem_leaders()),
        ('@@FEAR_MEASURED@@', measured_of(FEAR_TARGETS)),
        ('@@HATE_MEASURED@@', measured_of(HATE_TARGETS)),
        ('@@RAID_FIGHTS@@', f'{raid_fight_count():,}'),
    ]
