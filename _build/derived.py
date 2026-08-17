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
    out = [
        ('@@ZEM_RANK@@', zem_rank(slug)),
        ('@@ZEM_LEADER@@', zem_leaders()),
        ('@@FEAR_MEASURED@@', measured_of(FEAR_TARGETS)),
        ('@@HATE_MEASURED@@', measured_of(HATE_TARGETS)),
        ('@@RAID_FIGHTS@@', f'{raid_fight_count():,}'),
    ]
    if slug == 'mistmoore':
        out += mist_tokens()
    return out


# ---------------------------------------------------------------------------
# Castle Mistmoore's measured half.
#
# The survey carried 2,828 words and not one measured figure, on a zone we have
# 4.68 hours of parsed log for. These tokens are what the page prints instead of
# a wiki summary, and every one is read from assets/measured.json at build time.
# ---------------------------------------------------------------------------
import re

import zonestats

MIST = dict(zone='Mistmoore', min_kills=50)

# The party stamp the log carries at the head of a session:
# "Avenrae BRD WAR BER. Level 26. Mistmoore Castle." A level is only read out of
# a stamp that names a character and a trio, because the same session's chat
# also says "these are level 4 we are level 26" and a loose /level \d+/ picks up
# the mob's level as readily as ours. Where two stamps disagree the level is
# unresolved and nothing is printed.
_LEVEL_STAMP = re.compile(r'\b[A-Z][a-z]+(?:\s+[A-Z]{3}){2,3}\.\s*Level\s+(\d+)\b')


def _mist():
    if 'mist' not in _CACHE:
        _CACHE['mist'] = zonestats.profile(MIST['zone'], min_kills=MIST['min_kills'])
    return _CACHE['mist']


def _fmt(v, places=3):
    """Fixed places, never trimmed.

    Trailing zeros were being stripped, so one experience figure printed 0.200
    in the ranked table and 0.2 in the sentence introducing it. A reader
    checking one against the other sees two numbers.
    """
    return f'{v:.{places}f}'


def _mist_level(p):
    """The level the experience figures were earned at, read from the log."""
    seen = {int(m.group(1))
            for c in (p.get('context') or [])
            for m in _LEVEL_STAMP.finditer(c.get('text') or '')}
    return str(seen.pop()) if len(seen) == 1 else 'not recorded'


WORDS_CAP = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six',
             7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten'}


def _exp_rows(mobs):
    """A ledger column: mob type, experience a kill. Rows, not a sentence.

    The survey used to type these twelve figures beside the dataset they came
    from, which is the fault CLAUDE.md section 3 records and _build/backstab.py
    exists to prevent. A re-parse now moves the table on the next build.
    """
    return ''.join(f'<tr><td class="nmob">{m["name"]}</td>'
                   f'<td class="lv">{_fmt(m["exp_per_kill"])}</td></tr>'
                   for m in mobs)


def _bs_rows(bs):
    """The backstab ledger, including the spell list that makes it two kits."""
    out = []
    for m in bs:
        casts = ', '.join(w for w, _n in
                          sorted(m['casts'].items(), key=lambda t: -t[1])[:4])
        out.append(f'<tr><td class="nmob">{m["name"]}</td>'
                   f'<td class="lv">{m["backstabs"]}</td>'
                   f'<td class="lv">{m["backstab_max"]}</td>'
                   f'<td class="lv">{m["melee_max"]}</td>'
                   f'<td class="st">{casts or "&mdash;"}</td></tr>')
    return ''.join(out)


def _haste_clause(by_name):
    """Mynthi Davissi's two hastes, counted rather than remembered.

    A shaman haste and an enchanter haste in one fight is the page's evidence
    that a named ran two class kits at D1. The counts were typed beside the log
    they came from; they are read out of it now.
    """
    casts = (by_name.get('Mynthi Davissi') or {}).get('casts') or {}
    a, q = casts.get('Alacrity'), casts.get('Quickness')
    if a and q:
        return f'cast Alacrity {a} times and Quickness {q} times'
    return 'is logged casting neither haste in the sessions we hold'


def mist_tokens():
    p = _mist()
    if not p:
        return []
    ranked = [m for m in p['mobs'] if m['exp_per_kill']]
    best, worst = ranked[0], ranked[-1]
    bs = zonestats.backstabbers(p)
    hardest = max(bs, key=lambda m: m['backstab_max'])
    stun, stun_n, casters = p['stuns'][0]
    top_casters = ', '.join(f'{w} ({n})' for w, n in
                            sorted(casters.items(), key=lambda t: -t[1])[:3])
    caitiff = next((i for i, m in enumerate(ranked, 1)
                    if m['name'].lower() == 'an avenging caitiff'), None)
    return [
        ('@@M_KILLS@@', f"{p['kills']:,}"),
        ('@@M_HOURS@@', _fmt(p['hours'], 2)),
        ('@@M_RATE@@', f"{p['kills_per_hour']:,}"),
        ('@@M_SESSIONS@@', str(p['sessions'])),
        ('@@M_TIER@@', f"D{p['difficulty']} {p['difficulty_label']}"),
        ('@@M_DATE@@', p['dates'][0] if p['dates'] else 'not recorded'),
        ('@@M_TYPES@@', str(len(ranked))),
        ('@@M_BEST@@', best['name'].lower()),
        ('@@M_BEST_XP@@', _fmt(best['exp_per_kill'])),
        ('@@M_WORST@@', worst['name'].lower()),
        ('@@M_WORST_XP@@', _fmt(worst['exp_per_kill'])),
        ('@@M_SPREAD@@', str(round(best['exp_per_kill'] / worst['exp_per_kill']))),
        ('@@M_BS_TYPES@@', str(len(bs))),
        ('@@M_BS_TOTAL@@', str(sum(m['backstabs'] for m in bs))),
        ('@@M_BS_HARDEST@@', hardest['name'].lower()),
        ('@@M_BS_MAX@@', str(hardest['backstab_max'])),
        ('@@M_BS_MELEE@@', str(hardest['melee_max'])),
        ('@@M_STUN@@', stun),
        ('@@M_STUN_N@@', str(stun_n)),
        ('@@M_STUN_WHO@@', top_casters),
        ('@@M_ITEMS@@', str(len(p['loot']))),
        ('@@M_CAITIFF_RANK@@', str(caitiff) if caitiff else 'not recorded'),
        ('@@M_CAITIFF_XP@@', _fmt(next(m['exp_per_kill'] for m in ranked
                                       if m['name'].lower() == 'an avenging caitiff'))),
        ('@@M_LEVEL@@', _mist_level(p)),
        # The ranked ledgers and the backstab ledger, read out of the dataset
        # rather than typed under it.
        ('@@M_WORTH_ROWS@@', _exp_rows(ranked[:6])),
        ('@@M_SKIP_ROWS@@', _exp_rows(ranked[:-7:-1])),
        # A backstabbing type that also casts is running two class kits. Counted
        # from the same records the table prints, so the sentence and the table
        # cannot disagree.
        ('@@M_BS_DUAL@@', WORDS_CAP.get(sum(1 for m in bs if m['casts']),
                                        str(sum(1 for m in bs if m['casts'])))),
        ('@@M_BS_ROWS@@', _bs_rows(bs)),
        ('@@M_MYNTHI_HASTE@@', _haste_clause({m['name']: m for m in p['mobs']})),
    ]
