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
    if slug == 'thehole':
        out += hole_tokens()
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


# ---------------------------------------------------------------------------
# THE EXPERIENCE LADDER, AND WHY IT IS NOT AN AVERAGE.
#
# `zonestats.profile` keeps the FIRST session in which a mob appears and drops
# the rest, because these sessions carry a mean per type and no count, so there
# is nothing to weight by. The survey then ranked on that number and crowned
# "a deathly usher, best experience in the zone at 3.196" — which is session
# 19's figure. The same mob pays 1.327, 1.100 and 0.777 in the next three, and
# an ancille cook that session never killed beats it in all three sessions
# where both died. The ladder was ranking mobs by which session they first
# appeared in.
#
# The cause is not the join. Experience per kill falls all day across the whole
# roster: of the 26 types killed in every session, all 26 paid less by the last
# than the first. So an absolute percentage from 11:08 is not comparable with
# one from 17:15, and no aggregate over the four can be.
#
# What IS comparable is a mob's standing INSIDE its own session. Each type is
# scored against the median of the session it was killed in, and a type's place
# is the mean of those scores. A type killed in one session only cannot be
# placed at all and is excluded rather than ranked on a single reading — which
# is what put an undead knight second on a sample of one.
# ---------------------------------------------------------------------------
_MIN_SESSIONS = 2


def _median(vals):
    v = sorted(vals)
    n = len(v)
    if not n:
        return None
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2


def _exp_sessions():
    """The sessions whose experience the page may rank: one character's own.

    Experience belongs to whoever earned it. `min_kills` drops the support
    character's sessions for the same reason `zonestats.profile` does.
    """
    ss = [s for s in zonestats.sessions(MIST['zone'])
          if (s.get('kills') or 0) >= MIST['min_kills'] and s.get('exp_by_mob')]
    return sorted(ss, key=lambda s: (s.get('date') or '', s.get('window') or ''))


def _exp_scores():
    """{name: [(session, ratio-to-that-session's-median, absolute per cent)]}."""
    if 'mist_xp' in _CACHE:
        return _CACHE['mist_xp']
    out = {}
    for s in _exp_sessions():
        e = s['exp_by_mob']
        med = _median(e.values())
        if not med:
            continue
        for name, v in e.items():
            out.setdefault(name, []).append((s, v / med, v))
    _CACHE['mist_xp'] = out
    return out


def _ladder():
    """Every type placeable across sessions, best first."""
    if 'mist_ladder' in _CACHE:
        return _CACHE['mist_ladder']
    rows = [dict(name=n, score=sum(r for _s, r, _v in v) / len(v), n=len(v),
                 hi=max(a for _s, _r, a in v), lo=min(a for _s, _r, a in v))
            for n, v in _exp_scores().items() if len(v) >= _MIN_SESSIONS]
    rows.sort(key=lambda r: (-r['score'], r['name']))
    _CACHE['mist_ladder'] = rows
    return rows


def _ord(n):
    """1st, 2nd, 3rd, 11th. The page used to append a literal "th" to a token
    and printed "2th" the first time a rank below four came out of the data."""
    if n is None:
        return 'not recorded'
    if 11 <= n % 100 <= 13:
        return f'{n}th'
    return f'{n}' + {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')


def _place(name):
    for i, r in enumerate(_ladder(), 1):
        if r['name'].lower() == name.lower():
            return i, r
    return None, None


def _beats(winner, loser):
    """How often one type outpaid another in the sessions that killed both."""
    sc = _exp_scores()
    a = {s.get('window'): v for s, _r, v in sc.get(winner, [])}
    b = {s.get('window'): v for s, _r, v in sc.get(loser, [])}
    both = [k for k in a if k in b]
    return sum(1 for k in both if a[k] > b[k]), len(both)


def _exp_rows(mobs):
    """A ledger row: type, its score, and how many sessions stand behind it.

    The survey used to type these figures beside the dataset they came from,
    which is the fault CLAUDE.md section 3 records and _build/backstab.py exists
    to prevent. The sample size travels with the score because a place built on
    two sessions is not the same claim as one built on four.
    """
    return ''.join(f'<tr><td class="nmob">{m["name"]}</td>'
                   f'<td class="lv">{m["score"]:.2f}&times;</td>'
                   f'<td class="lv">{m["n"]}</td></tr>'
                   for m in mobs)


def _drift():
    """How far the experience figures move across one day, read out of them."""
    runs = [[v for _s, _r, v in rec]
            for rec in _exp_scores().values()
            if len(rec) == len(_exp_sessions())]
    fell = [r for r in runs if r[0] > r[-1]]
    mono = [r for r in runs if all(r[i] > r[i + 1] for i in range(len(r) - 1))]
    ratios = _median([r[0] / r[-1] for r in runs]) if runs else None
    return len(runs), len(fell), len(mono), ratios


def _level_scope():
    """Which sessions actually carry the level stamp the figures are quoted at.

    Two of the four do. The page said "these figures hold at level 26" over a
    sample whose second half stamps no level at all, which is the same shape of
    claim as a ranking typed beside the data it ranks.
    """
    ss = _exp_sessions()
    with_stamp = [s for s in ss
                  if any(_LEVEL_STAMP.search(c.get('text') or '')
                         for c in (s.get('context') or []))]
    return len(with_stamp), len(ss), with_stamp


def _zone_line_scope():
    """Sessions whose difficulty the numbered zone line states on its own.

    CLAUDE.md: where a session carries no zone line, the loot floor names its
    difficulty and the page must say so. One of the four here does not.
    """
    ss = _exp_sessions()
    read = [s for s in ss if 'zone line' in (s.get('difficulty_from') or '')]
    guessed = [s for s in ss if s not in read]
    if not guessed:
        return (f'All {WORDS.get(len(ss), len(ss))} print the numbered zone line.')
    g = guessed[0]
    return (f'{WORDS_CAP.get(len(read), len(read))} of the '
            f'{WORDS.get(len(ss), len(ss))} print the numbered zone line; '
            f'{g.get("window")} ({g.get("kills"):,} kills) does not, so its zone is '
            f'the collaborator&rsquo;s word and its tier a loot floor of '
            f'+{g.get("drop_tier_floor")}.')


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

    They are read over every session in the zone, which is the same scope as the
    backstab table this sentence sits beside — and the page prints that scope,
    because the counts over one character's four sessions are 68 and 13 rather
    than 109 and 42, and a sentence beside a table has to say which it is.
    """
    casts = (by_name.get('Mynthi Davissi') or {}).get('casts') or {}
    a, q = casts.get('Alacrity'), casts.get('Quickness')
    if a and q:
        return f'cast Alacrity {a} times and Quickness {q} times'
    return 'is logged casting neither haste in the sessions we hold'


# A tier suffix is a roll on the drop, not a different item — CLAUDE.md section
# 2. The bard table counted "Lute of the Gypsy Princess +1" and printed 9 while
# the named page summed the suffixes and printed 11.
_TIER_SUFFIX = re.compile(r'\s*\+\d+$')


def _seen(mob, item):
    """How many of one item one mob type dropped, summed across tier suffixes."""
    n = 0
    for s in zonestats.sessions(MIST['zone']):
        for name, rec in (s.get('mobs') or {}).items():
            if name.lower() != mob.lower():
                continue
            for it, c in (rec.get('loot') or {}).items():
                if _TIER_SUFFIX.sub('', it).lower() == item.lower():
                    n += c
    return n


def _droppers(item):
    """Every mob type measured dropping an item, commonest first."""
    tot = {}
    for s in zonestats.sessions(MIST['zone']):
        for name, rec in (s.get('mobs') or {}).items():
            for it, c in (rec.get('loot') or {}).items():
                if _TIER_SUFFIX.sub('', it).lower() == item.lower():
                    tot[name] = tot.get(name, 0) + c
    return sorted(tot.items(), key=lambda t: -t[1])


def _swings(mob):
    """Swings a type took at us — a denominator the dataset actually holds.

    The page said a deathly usher "casts nothing across 1,008 kills". 1,008 is
    every kill of every type; zonestats' own docstring records that per-type
    kill counts are absent for these sessions and stay absent. Swings are not.
    """
    n = 0
    for s in _exp_sessions():
        for name, rec in (s.get('mobs') or {}).items():
            if name.lower() == mob.lower():
                n += rec.get('swings') or 0
    return n


USHER, COOK, CAITIFF = 'a deathly usher', 'an ancille cook', 'an avenging caitiff'


def mist_tokens():
    p = _mist()
    if not p:
        return []
    lad = _ladder()
    best, worst = lad[0], lad[-1]
    bs = zonestats.backstabbers(p)
    hardest = max(bs, key=lambda m: m['backstab_max'])
    stun, stun_n, casters = p['stuns'][0]
    top_casters = ', '.join(f'{w} ({n})' for w, n in
                            sorted(casters.items(), key=lambda t: -t[1])[:3])

    # THE CAITIFF IS NOT ON THE LADDER, AND THAT IS THE POINT.
    # It was killed in one session, so it has no cross-session standing. The
    # page prints the single reading with the window it belongs to rather than
    # ranking it against three sessions it was never in.
    cait = _exp_scores().get(CAITIFF) or []
    cs, _cr, cv = cait[0] if cait else (None, None, None)
    cwin = cs.get('window') if cs else 'not recorded'
    corder = sorted((cs.get('exp_by_mob') or {}).items(), key=lambda t: -t[1]) if cs else []
    cplace = next((i for i, (n, _v) in enumerate(corder, 1) if n == CAITIFF), None)

    usher_place, _u = _place(USHER)
    cook_place, _c = _place(COOK)
    cook_wins, cook_both = _beats(COOK, USHER)
    runs, fell, mono, med = _drift()
    lvl_n, lvl_of, lvl_ss = _level_scope()
    lvl_when = ' and '.join(s.get('window') or '' for s in lvl_ss)

    # Every session in the zone, both characters — the scope of the backstab
    # ledger and of the haste sentence beside it. The experience half above is
    # one character's four sessions, and both now say which they are.
    allss = zonestats.sessions(MIST['zone'])
    nchar = len({s.get('character') for s in allss})
    bs_scope = (f"{WORDS_CAP.get(len(allss), len(allss))} sessions, "
                f"{WORDS.get(nchar, nchar)} characters, "
                f"{sum(s.get('kills') or 0 for s in allss):,} kills")

    bracers = [n for n, _c in _droppers('Bronze Bracers')]
    return [
        ('@@M_KILLS@@', f"{p['kills']:,}"),
        ('@@M_HOURS@@', _fmt(p['hours'], 2)),
        ('@@M_RATE@@', f"{p['kills_per_hour']:,}"),
        ('@@M_SESSIONS@@', str(len(_exp_sessions()))),
        ('@@M_TIER@@', f"D{p['difficulty']} {p['difficulty_label']}"),
        ('@@M_DATE@@', p['dates'][0] if p['dates'] else 'not recorded'),
        ('@@M_WINDOW@@', f"{_exp_sessions()[0].get('window','').split('-')[0]}"
                         f"&ndash;{_exp_sessions()[-1].get('window','').split('-')[-1]}"),
        # ---- the ladder, scored inside each session -------------------------
        ('@@M_TYPES@@', str(len(lad))),
        ('@@M_BEST@@', best['name']),
        ('@@M_BEST_R@@', f"{best['score']:.2f}"),
        ('@@M_WORST@@', worst['name']),
        ('@@M_WORST_R@@', f"{worst['score']:.2f}"),
        ('@@M_SPREAD@@', str(round(best['score'] / worst['score']))),
        ('@@M_WORTH_ROWS@@', _exp_rows(lad[:6])),
        ('@@M_SKIP_ROWS@@', _exp_rows(lad[:-7:-1])),
        ('@@M_USHER_RANK@@', _ord(usher_place)),
        ('@@M_COOK_RANK@@', _ord(cook_place)),
        ('@@M_COOK_WINS@@',
         (f'all {WORDS.get(cook_both, cook_both)}' if cook_wins == cook_both
          else f'{WORDS.get(cook_wins, cook_wins)} of the '
               f'{WORDS.get(cook_both, cook_both)}')),
        ('@@M_CAITIFF_XP@@', _fmt(cv) if cv is not None else 'not recorded'),
        ('@@M_CAITIFF_RANK@@', _ord(cplace)),
        ('@@M_CAITIFF_OF@@', str(len(corder))),
        ('@@M_CAITIFF_WIN@@', cwin),
        # ---- what the figures are, and what they are scoped to --------------
        ('@@M_DRIFT_ALL@@', str(runs)),
        ('@@M_DRIFT_FELL@@', str(fell)),
        ('@@M_DRIFT_MONO@@', str(mono)),
        ('@@M_DRIFT_MED@@', _fmt(med, 1) if med else 'not recorded'),
        ('@@M_LEVEL@@', _mist_level(p)),
        ('@@M_LEVEL_N@@', WORDS.get(lvl_n, str(lvl_n))),
        ('@@M_LEVEL_OF@@', WORDS.get(lvl_of, str(lvl_of))),
        ('@@M_LEVEL_WHEN@@', lvl_when),
        ('@@M_ZONELINE@@', _zone_line_scope()),
        ('@@M_USHER_SWINGS@@', f'{_swings(USHER):,}'),
        # ---- the backstab ledger, and its own scope -------------------------
        ('@@M_BS_SCOPE@@', bs_scope),
        ('@@M_BS_TYPES@@', str(len(bs))),
        ('@@M_BS_TOTAL@@', str(sum(m['backstabs'] for m in bs))),
        ('@@M_BS_HARDEST@@', hardest['name'].lower()),
        ('@@M_BS_MAX@@', str(hardest['backstab_max'])),
        ('@@M_BS_MELEE@@', str(hardest['melee_max'])),
        ('@@M_STUN@@', stun),
        ('@@M_STUN_N@@', str(stun_n)),
        ('@@M_STUN_WHO@@', top_casters),
        ('@@M_ITEMS@@', str(len(p['loot']))),
        # A backstabbing type that also casts is running two class kits. Counted
        # from the same records the table prints, so the sentence and the table
        # cannot disagree.
        ('@@M_BS_DUAL@@', WORDS_CAP.get(sum(1 for m in bs if m['casts']),
                                        str(sum(1 for m in bs if m['casts'])))),
        ('@@M_BS_ROWS@@', _bs_rows(bs)),
        ('@@M_MYNTHI_HASTE@@', _haste_clause({m['name']: m for m in p['mobs']})),
        # ---- drop counts, summed across tier suffixes -----------------------
        ('@@M_LUTE_MYNTHI@@', str(_seen('Mynthi Davissi', 'Lute of the Gypsy Princess'))),
        ('@@M_LUTE_WOLF@@', str(_seen('A werewolf gypsy', 'Lute of the Gypsy Princess'))),
        ('@@M_DRUMS@@', str(_seen('Mynthi Davissi', 'Mistmoore Battle Drums'))),
        ('@@M_BRACERS_MORE@@', WORDS.get(max(len(bracers) - 1, 0),
                                         str(max(len(bracers) - 1, 0)))),
    ]


# ---------------------------------------------------------------------------
# The Hole's backstabbing trash.
#
# The survey carried: "Backstabs land for 348. Elemental capturers hit that
# figure; the weaker deceivers run around 248 with a maximum near 300."
#
# NONE OF THOSE THREE FIGURES IS IN assets/measured.json, and the ranking is
# backwards. Across the Paineel sessions the deceiver's hardest recorded
# backstab is the LARGER of the two, so "the weaker deceivers" describes an
# order the data does not hold. Same fault as the Mistmoore familiars in
# _build/backstab.py, and the same fix: the page asks for a token, the token
# reads the dataset, and a re-parse moves the sentence on the next build.
#
# The two names are the claim's own scope. The zone's hardest backstab belongs
# to a muck covered elemental, which is a named and a different claim.
# ---------------------------------------------------------------------------
HOLE_ROGUES = ('An elemental capturer', 'An elemental deceiver')


def _hole_backstab():
    """Melee and backstab maxima for the two rogue trash types, from the parse."""
    p = zonestats.profile('Paineel')
    if not p:
        return None
    rec = {m['name']: m for m in zonestats.backstabbers(p)}
    got = [rec[n] for n in HOLE_ROGUES if n in rec]
    if not got:
        return None
    melee = max(m['melee_max'] for m in got)
    back = max(m['backstab_max'] for m in got)
    if not melee or not back:
        return None
    return dict(melee=melee, backstab=back, ratio=back / melee)


def hole_tokens():
    b = _hole_backstab()
    if not b:
        # Never a typed fallback figure. A missing parse says so and the
        # sentence reads as a gap, which is the house rule for every other
        # number on the site.
        return [('@@H_BACKSTAB@@', 'Their damage from behind is not recorded'),
                ('@@H_BS_RATIO@@', 'an unrecorded multiple of')]
    return [
        ('@@H_BACKSTAB@@',
         f"They melee up to {b['melee']} and backstab up to {b['backstab']}"),
        ('@@H_BS_RATIO@@',
         f"about {WORDS.get(round(b['ratio']), round(b['ratio']))} times"),
    ]


def clip(s, n):
    """Shorten to at most n characters without inventing a fact.

    A hard slice published "the NPC record says 3" on named/najena.html where
    the source says 35: extract.py's 190-character cut landed between the two
    digits, and the site asserted a level for a named mob that no source
    states. A severed number does not look severed - it looks like a whole,
    smaller one. That is the single truncation that turns into a falsehood
    rather than a rough edge, which is why it is guarded specifically.

    So: break on a word boundary, drop trailing words until the last does not
    end in a digit, and mark the cut with an ellipsis so a reader can see that
    something was removed.

    Lives here rather than in extract.py because build17.py truncates the same
    field again for its meta description, and two truncations with one rule
    beats two rules. extract.py cannot be imported for it - it has no __main__
    guard and rewrites index-data.json on import.
    """
    s = (s or '').strip()
    if len(s) <= n:
        return s
    cut = s[:n]
    sp = cut.rfind(' ')
    if sp > 0:
        cut = cut[:sp]
    cut = cut.rstrip()
    while cut and cut[-1].isdigit():
        sp = cut.rfind(' ')
        cut = cut[:sp].rstrip() if sp > 0 else ''
    cut = cut.rstrip(' ,;:.&-')
    return (cut + '…') if cut else ''
