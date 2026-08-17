"""What a zone is worth to farm, read out of the measured sessions.

Imported by the generators that cite it. Writes no file of its own.

WHY THIS EXISTS
---------------
The site could say what a kill was worth and never how often that kill
happened, because `exp_by_mob` carried a mean and `logstats.py` discarded the
count it was taken over. So every question a player actually arrives with —
is this zone worth my evening, what should I kill, what should I walk past —
could only be answered by typing a number beside the data. That is the one
fault this project keeps finding in other people's work.

`_build/backstab.py` is the pattern and the precedent: a figure that cites a
dataset is read out of that dataset at build time, so a re-parse moves the
prose on the next build. This module does the same for the farming picture,
and for every zone rather than one claim in one of them.

WHAT IT REFUSES TO DO
---------------------
**Experience is level-dependent and does not generalise.** The client prints
`You gain experience! (0.144%)` — a percentage of the level being worked on,
so the same mob pays a different percentage to a level 26 character than to a
level 45 one. Every experience figure here is returned with the character,
their level where the log states it, their trio, the difficulty and the date,
and a page that prints the figure without that scope is publishing a rate for
a character nobody has.

**Per-type kill counts are absent for older sessions and stay absent.** The
seven Castle Mistmoore sessions of 8 August 2026 were parsed before
`kills_by_mob` existed and their raw logs have since rotated away, so the
dataset holds a mean per mob type and no count. `has_kill_counts` says which
way round a zone is, and callers must branch on it rather than estimate.

**A mean over one kill is not a rate.** `exp_samples` travels with every
figure so a page can print the sample size beside it, or decline to print the
figure at all.
"""
import json
import os

_CACHE = {}

_MEASURED = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'assets', 'measured.json')


def _load():
    if 'm' in _CACHE:
        return _CACHE['m']
    try:
        _CACHE['m'] = json.load(open(_MEASURED, encoding='utf-8'))
    except (OSError, ValueError):
        _CACHE['m'] = []
    return _CACHE['m']


def sessions(zone, date=None, difficulty=None):
    """Every measured session in a zone, newest ordering left to the caller.

    `zone` is matched as a substring so 'Mistmoore' finds 'The Castle of
    Mistmoore' and its numbered instance forms. Optional date and difficulty
    narrow it, because a zone farmed at two tiers is two different zones and
    averaging across them would be the difficulty error this project has
    already made once.
    """
    out = []
    for s in _load():
        if zone.lower() not in (s.get('zone') or '').lower():
            continue
        if date is not None and s.get('date') != date:
            continue
        if difficulty is not None and s.get('difficulty') != difficulty:
            continue
        out.append(s)
    return out


def profile(zone, date=None, difficulty=None, min_kills=1):
    """The farming picture for a zone: rate, roster, hazards, loot.

    `min_kills` drops sessions below a threshold so a character who stood in
    the zone as support does not pull the kill rate down. It defaults to 1,
    which keeps every session that killed anything; the Mistmoore pages pass a
    higher figure because Shara logged 10 kills across three sessions while
    playing support and Avenrae logged 1,008.
    """
    key = ('p', zone, date, difficulty, min_kills)
    if key in _CACHE:
        return _CACHE[key]

    ss = sessions(zone, date, difficulty)
    if not ss:
        return None

    # TWO SESSION SETS, because two different questions are being asked.
    #
    # A kill rate and an experience figure belong to the character that earned
    # them. Experience is printed by the client as a percentage of the level
    # being worked on, so averaging Avenrae's gains at level 26 with Shara's at
    # her own level produces a rate for a character who does not exist. Both
    # are therefore taken from the sessions that did the killing.
    #
    # What a mob DID, on the other hand, it did in front of whoever was
    # standing there. Backstabs, spells, stuns and drops are counts of events,
    # and dropping the sessions where a support character watched would throw
    # away real observations. Those aggregate over everything.
    earning = [s for s in ss if (s.get('kills') or 0) >= min_kills]
    timed = [s for s in earning if s.get('minutes')]
    minutes = sum(s['minutes'] for s in timed)
    kills = sum(s.get('kills') or 0 for s in timed)

    mobs = {}
    for s in ss:
        counts = s.get('kills_by_mob') or {}
        # Experience only from the sessions that earned it — see above.
        exps = (s.get('exp_by_mob') or {}) if s in earning else {}
        samples = s.get('exp_samples_by_mob') or {}
        for name, rec in (s.get('mobs') or {}).items():
            m = mobs.setdefault(name.lower(), dict(
                name=name, swings=0, landed=0, melee_max=0, backstabs=0,
                backstab_max=0, bs_avg_lo=None, bs_avg_hi=None,
                casts={}, loot={}, kills=0, exp_weighted=0.0, exp_samples=0))
            m['swings'] += rec.get('swings') or 0
            m['landed'] += rec.get('landed') or 0
            m['melee_max'] = max(m['melee_max'], rec.get('max') or 0)
            m['backstabs'] += rec.get('backstabs') or 0
            m['backstab_max'] = max(m['backstab_max'], rec.get('backstab_max') or 0)
            bs = rec.get('backstab_avg')
            if bs is not None:
                m['bs_avg_lo'] = bs if m['bs_avg_lo'] is None else min(m['bs_avg_lo'], bs)
                m['bs_avg_hi'] = bs if m['bs_avg_hi'] is None else max(m['bs_avg_hi'], bs)
            for k, v in (rec.get('casts') or {}).items():
                m['casts'][k] = m['casts'].get(k, 0) + v
            for k, v in (rec.get('loot') or {}).items():
                m['loot'][k] = m['loot'].get(k, 0) + v
        # Experience and kill counts key on the log's own lower-case mob name,
        # while the damage tables key on the capitalised form the combat lines
        # use. Same mob, two spellings, and joining them wrongly is how a
        # roster ends up with every mob listed twice.
        for name, per in exps.items():
            m = mobs.setdefault(name.lower(), dict(
                name=name, swings=0, landed=0, melee_max=0, backstabs=0,
                backstab_max=0, bs_avg_lo=None, bs_avg_hi=None,
                casts={}, loot={}, kills=0, exp_weighted=0.0, exp_samples=0))
            n = samples.get(name) or 0
            if n:
                m['exp_weighted'] += per * n
                m['exp_samples'] += n
            elif m['exp_samples'] == 0:
                # Older sessions carry the mean and no count. Record it as a
                # single sample so the figure survives, and let has_kill_counts
                # tell the page it may not weight these.
                m['exp_weighted'] += per
                m['exp_samples'] += 1
        for name, n in counts.items():
            mobs.setdefault(name.lower(), dict(
                name=name, swings=0, landed=0, melee_max=0, backstabs=0,
                backstab_max=0, bs_avg_lo=None, bs_avg_hi=None,
                casts={}, loot={}, kills=0, exp_weighted=0.0,
                exp_samples=0))['kills'] += n

    for m in mobs.values():
        m['exp_per_kill'] = (round(m['exp_weighted'] / m['exp_samples'], 3)
                             if m['exp_samples'] else None)

    stuns, casters, unread = {}, {}, 0
    loot = {}
    ctl = dict(melee_stuns_avoided=0, lockout_lines=0, fear_lines=0,
               screams=0, scream_seconds=0)
    for s in ss:
        c = s.get('control') or {}
        for k in ctl:
            ctl[k] += c.get(k) or 0
        unread += c.get('stuns_cause_unread') or 0
        for sp, rec in (c.get('stuns') or {}).items():
            stuns[sp] = stuns.get(sp, 0) + (rec.get('landed') or 0)
            for who, n in (rec.get('casters') or {}).items():
                casters.setdefault(sp, {})
                casters[sp][who] = casters[sp].get(who, 0) + n
        for name, rec in (s.get('mobs') or {}).items():
            for it, n in (rec.get('loot') or {}).items():
                loot[it] = loot.get(it, 0) + n

    out = dict(
        zone=ss[0].get('zone'),
        sessions=len(ss),
        characters=sorted({s.get('character') for s in ss if s.get('character')}),
        dates=sorted({s.get('date') for s in ss if s.get('date')}),
        difficulty=ss[0].get('difficulty'),
        difficulty_label=ss[0].get('difficulty_label'),
        minutes=minutes,
        hours=round(minutes / 60, 2) if minutes else None,
        kills=kills,
        kills_per_hour=round(kills / minutes * 60) if minutes else None,
        # True only where every session carries per-type counts. Where it is
        # False the roster's exp_per_kill figures are unweighted means and the
        # page must not multiply them out into a rate.
        has_kill_counts=all('kills_by_mob' in s for s in ss),
        mobs=sorted(mobs.values(), key=lambda m: -(m['exp_per_kill'] or 0)),
        stuns=sorted(((sp, n, casters.get(sp, {})) for sp, n in stuns.items()),
                     key=lambda t: -t[1]),
        stuns_cause_unread=unread,
        control=ctl,
        loot=sorted(loot.items(), key=lambda t: -t[1]),
        context=[c for s in ss for c in (s.get('context') or [])],
    )
    _CACHE[key] = out
    return out


def backstabbers(prof):
    """Every mob type recorded backstabbing, not only the ones we wrote about.

    `_build/backstab.py` answers a narrower question — it exists to hold one
    published claim about two familiars to its data — and is deliberately
    scoped to those two names. Asking the zone instead of the claim gives a
    different and larger answer, and the difference is the point: in Castle
    Mistmoore seven mob types backstab, and the hardest recorded hit belongs to
    none of the two.
    """
    return [m for m in sorted(prof['mobs'], key=lambda m: -m['backstabs'])
            if m['backstabs']]


def two_kit_mobs(prof):
    """Mobs that both backstab and cast: two class kits on one mob type.

    Backstab is a rogue ability and a spell list is not, so a type doing both
    is carrying two kits. The log cannot tell whether one individual does both
    or whether the type spawns with either, and no caller may claim it does.
    """
    return [m for m in backstabbers(prof) if m['casts']]
