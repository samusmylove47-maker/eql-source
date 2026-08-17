"""The Castle Mistmoore backstab evidence, derived rather than remembered.

Imported by the generators that cite it. No output file of its own.

WHY THIS EXISTS
---------------
CLAUDE.md, learn/still-true.html, learn/difficulty.html and
learn/reading-the-plans.html all carried the same sentence: *two ordinary trash
types backstabbed 39 times between them - An initiate familiar 22, A pledge
familiar 17* - and *melee 1-38, backstab 100-143*.

**None of those six numbers is in assets/measured.json.** The parse holds 113
backstabs across the seven Mistmoore sessions of 8 August 2026 (A pledge
familiar 62, An initiate familiar 51), and 101 across the four logged by
Avenrae alone. No session and no combination of sessions produces 22 and 17.

The damage range was worse than stale, it was impossible: one session's
backstabs average 38.8, which cannot happen if the lowest is 100, and the
recorded maxima run to 168 rather than stopping at 143. A range whose floor
sits above a recorded mean is not a measurement of anything.

The figures were almost certainly right when first written, against a smaller
parse, and the data grew while four copies of the prose did not. That is the
fault this project keeps finding in other people's work, published in its own
rules file - the one that says never invent a number.

So nobody types them again. Every caller reads this module, this module reads
the dataset, and a re-parse moves the pages on the next build.
"""
import json
import os

_CACHE = {}

ZONE = 'Mistmoore'
DATE = '08 Aug 2026'
# The two trash types the claim is about. Named exactly as the log writes them.
TYPES = ('An initiate familiar', 'A pledge familiar')


def evidence():
    """Backstab counts and damage, per mob type, across the Mistmoore sessions.

    Returns a dict carrying the totals, the per-type figures, and the session
    and character counts, so a page can state its own scope instead of leaving
    a reader to guess which sessions a figure came from. Naming no scope is how
    the old figure drifted for a week without anyone noticing.
    """
    if 'e' in _CACHE:
        return _CACHE['e']
    try:
        M = json.load(open('assets/measured.json', encoding='utf-8'))
    except (OSError, ValueError):
        return None

    per = {t: dict(backstabs=0, bs_max=0, bs_avg_lo=None, bs_avg_hi=None,
                   melee_max=0, melee_avg_lo=None, melee_avg_hi=None) for t in TYPES}
    sessions, chars = 0, set()
    for s in M:
        if ZONE not in (s.get('zone') or '') or s.get('date') != DATE:
            continue
        hit = False
        for name, rec in (s.get('mobs') or {}).items():
            if name not in per or not (rec.get('backstabs') or 0):
                continue
            hit = True
            p = per[name]
            p['backstabs'] += rec['backstabs']
            p['bs_max'] = max(p['bs_max'], rec.get('backstab_max') or 0)
            for key, val in (('bs_avg', rec.get('backstab_avg')),
                             ('melee_avg', rec.get('avg'))):
                if val is None:
                    continue
                lo, hi = p[key + '_lo'], p[key + '_hi']
                p[key + '_lo'] = val if lo is None else min(lo, val)
                p[key + '_hi'] = val if hi is None else max(hi, val)
            p['melee_max'] = max(p['melee_max'], rec.get('max') or 0)
        if hit:
            sessions += 1
            chars.add(s.get('character'))

    total = sum(p['backstabs'] for p in per.values())
    if not total:
        return None
    out = dict(
        total=total, sessions=sessions, characters=len(chars), date=DATE,
        per=per,
        # The honest damage statement: a maximum and the range the per-session
        # averages actually span. Never a floor we did not record.
        bs_max=max(p['bs_max'] for p in per.values()),
        melee_max=max(p['melee_max'] for p in per.values()),
        bs_avg_lo=min(p['bs_avg_lo'] for p in per.values() if p['bs_avg_lo'] is not None),
        bs_avg_hi=max(p['bs_avg_hi'] for p in per.values() if p['bs_avg_hi'] is not None),
    )
    _CACHE['e'] = out
    return out


def counts_phrase():
    """"113 times between them - A pledge familiar 62, An initiate familiar 51"."""
    e = evidence()
    if not e:
        return ''
    parts = sorted(((t, p['backstabs']) for t, p in e['per'].items()), key=lambda x: -x[1])
    return (f"{e['total']} times between them &mdash; "
            + ", ".join(f"{t} {n}" for t, n in parts))


def damage_phrase():
    """A damage statement with no invented floor."""
    e = evidence()
    if not e:
        return ''
    return (f"melee up to {e['melee_max']}, backstab up to {e['bs_max']} "
            f"with per-session averages from {e['bs_avg_lo']:.0f} to {e['bs_avg_hi']:.0f}")


def scope_phrase():
    e = evidence()
    if not e:
        return ''
    return (f"{e['sessions']} sessions on {e['date']}"
            + (f", {e['characters']} characters" if e['characters'] > 1 else ""))
