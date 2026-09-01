"""assets/sky-loot.json — what the Plane of Sky actually dropped, and what its
bosses actually cost.

    python3 _build/skyloot.py     # run from build.sh, before build8.py

WHY THIS FILE HAS TO EXIST
--------------------------
The Sky logs of 14-15 August 2026 are the best evidence anyone in this community
holds about the zone: 43 boss fights, 16 named bosses, 148 loot lines. All of it
was parsed and committed to assets/measured.json and assets/raids-measured.json.

**None of it reached a page**, and the reason is worth writing down because it
will happen again. sightings.py joins measured drops to the item catalogue, and
that catalogue is mined from the dungeon surveys plus the planar sets. The Plane
of Sky is neither. So every one of the 148 Sky loot lines - 74 distinct items,
every key in the chain, the whole efreeti line - was silently discarded as
vendor trash, and assets/sightings.json contains not one Sky drop. No Sky mob is
on a survey roster either.

docs/SKY-MEASURED.md said "full per-boss drop tables are in sightings.json".
They were not there at all. A generator that drops evidence on the floor without
counting what it dropped looks exactly like a generator that found nothing.

The general fix belongs in sightings.py and is a migration across a dataset five
builders and the public contract read. This file is the narrow one: it derives
the Sky numbers straight from the two measured datasets, so the page renders
committed data rather than figures typed beside it. That is the specific fault
CLAUDE.md records as having cost two retractions in one day.

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
No rates. A drop seen once is seen once, and 43 fights over two nights is a
sample, not a drop table. Every count here is "how many we watched fall".

No island labels. Which boss stands on which island is structure and lives in
build8.py, which has carried it since the page was written from two independent
post-launch accounts. This file measures; the page joins. Keeping the join in
the page is what lets it say "the chain predicted this and the log confirmed
it" without either half quietly deriving from the other.
"""
import os, re, json, statistics, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

ZONE = 'The Plane of Sky'

# Items whose name is the evidence: the key chain, and the efreeti line that the
# 14 Aug audit flagged as an unresolved source conflict with eqlegendstools.
KEY_RE = re.compile(r'\b(?:Key|Keys)\b', re.I)
EFREETI_RE = re.compile(r'\bEfreeti\b', re.I)
RUNE_RE = re.compile(r'^Wind Rune (\w+)$')


def base(item):
    """"Belt of Contention +1" and "Belt of Contention" are one item.

    +N is an upgrade tier rolled on the drop, not part of the name - CLAUDE.md
    sets this out with the 43/11/1 Fine Steel Rapier split. Counting the tiers
    as separate items would invent nine belts out of four.
    """
    return re.sub(r'\s*\+\d+\s*$', '', item or '').strip()


def merge_case(mobs):
    """The log sentence-capitalises a mob at the start of a line, so "an essence
    carrier" and "An essence carrier" arrive as two entries - and in this zone
    the capitalised one is always the empty one. Nine mobs split that way here,
    including the Hand of Veeshan, whose entire efreeti drop table sits under
    the lowercase spelling."""
    out = {}
    for name, rec in mobs.items():
        first = None
        for seen in out:
            if seen.lower() == name.lower():
                first = seen
                break
        # Prefer whichever spelling actually carries the data.
        if first is None:
            out[name] = dict(rec)
            continue
        keep = out.pop(first)
        richer = rec if (rec.get('loot') or rec.get('swings')) else keep
        poorer = keep if richer is rec else rec
        name_kept = name if richer is rec else first
        loot = collections.Counter(richer.get('loot') or {})
        loot.update(poorer.get('loot') or {})
        merged = dict(richer)
        merged['loot'] = dict(loot)
        out[name_kept] = merged
    return out


def main():
    M = json.load(open('assets/measured.json', encoding='utf-8'))
    R = json.load(open('assets/raids-measured.json', encoding='utf-8'))

    sessions = [s for s in M if (s.get('zone') or '') == ZONE]
    if not sessions:
        print('skyloot: no Plane of Sky session in measured.json, skipped')
        return
    fights = [f for f in R if ZONE in (f.get('zone') or '')]

    # ---------------------------------------------------------------- the loot
    mobs = {}
    for s in sessions:
        for name, rec in merge_case(s.get('mobs') or {}).items():
            cur = mobs.setdefault(name, dict(loot=collections.Counter(), casts=collections.Counter(),
                                             swings=0, landed=0, maxhit=None, avg=None))
            for item, n in (rec.get('loot') or {}).items():
                cur['loot'][base(item)] += n
            for spell, n in (rec.get('casts') or {}).items():
                cur['casts'][spell] += n
            cur['swings'] += rec.get('swings') or 0
            cur['landed'] += rec.get('landed') or 0
            if rec.get('max') is not None:
                cur['maxhit'] = max(cur['maxhit'] or 0, rec['max'])
            if rec.get('avg') is not None:
                cur['avg'] = rec['avg']

    exp = {}
    for s in sessions:
        for name, e in (s.get('exp_by_mob') or {}).items():
            exp.setdefault(name.lower(), e)

    # ------------------------------------------------------------- the fights
    byboss = collections.defaultdict(list)
    for f in fights:
        byboss[f['boss']].append(f)

    bosses = []
    for name in sorted(byboss, key=lambda b: b.lower()):
        fs = byboss[name]
        dmg = [f['damage_low'] for f in fs]
        # DAMAGE TO KILL IS NOT HIT POINTS and the biggest number here is not
        # automatically the best one. A fight the parser marked `damage_is_floor`
        # was joined after the boss was engaged, so its total is a lower bound.
        # The most defensible single figure is therefore the largest observed,
        # carrying whether that particular view was complete.
        best = max(fs, key=lambda f: f['damage_low'])
        complete = [f for f in fs if not f.get('damage_is_floor')]
        loot = mobs.get(name, {}).get('loot') or collections.Counter()
        m = mobs.get(name, {})
        bosses.append(dict(
            boss=name,
            fights=len(fs),
            dates=sorted({f['date'] for f in fs}),
            difficulties=sorted({f['difficulty'] for f in fs}),
            damage_max=best['damage_low'],
            damage_max_is_floor=bool(best.get('damage_is_floor')),
            damage_complete_max=(max(f['damage_low'] for f in complete) if complete else None),
            damage_min=min(dmg),
            seconds_min=min(f['seconds'] for f in fs),
            seconds_max=max(f['seconds'] for f in fs),
            attackers_min=min(f['attackers'] for f in fs),
            attackers_max=max(f['attackers'] for f in fs),
            our_share_max=max(f['our_damage_share_pct'] for f in fs),
            self_heals=max(f.get('self_heal_high') or 0 for f in fs),
            spells=sorted({sp for f in fs for sp in (f.get('spells') or {})}),
            casts=dict(m.get('casts') or {}),
            melee_avg=m.get('avg'),
            melee_max=m.get('maxhit'),
            # The sample behind the two figures above. A max hit means nothing
            # without it, and these are swings at ONE character - mitigation
            # differs per target, so this bounds what the boss did to us and
            # not what it does to a tank.
            melee_swings=m.get('swings') or 0,
            melee_landed=m.get('landed') or 0,
            exp_pct_per_kill=exp.get(name.lower()),
            # One fight is one observation. Bzizzzt's only record is 614 damage
            # over 3 seconds where its siblings take 10-20k, which is a kill we
            # arrived at the end of rather than a cheap boss - and the parser
            # cannot mark it a floor, because it never saw the boss act first.
            # Flagging the sample size is honest where guessing a threshold is
            # not, and the page prints the flag.
            single_observation=len(fs) == 1,
            loot=[dict(item=i, n=n) for i, n in loot.most_common()],
        ))

    # A NAMED we looted but hold no fight for is a gap worth printing rather
    # than hiding: it means the parser has no damage for something we
    # demonstrably killed. That is not hypothetical - the Hand of Veeshan sat
    # in exactly this state until 15 Aug 2026, with the full efreeti line in
    # its drop table and no fight record, because raidstats.py matched boss
    # names case-sensitively and its article is lowercase.
    #
    # Trash is not a gap: it is named by the log in lower case after its
    # article ("a soul harvester"), where a named capitalises ("the Hand of
    # Veeshan", "Bazzt Zzzt"). That is the only tell the log offers.
    def is_named(n):
        rest = re.sub(r'^(?:a|an|the)\s+', '', n.strip(), flags=re.I)
        return bool(rest[:1].isupper())

    looted_only = sorted(
        n for n, m in mobs.items()
        if m['loot'] and n not in byboss and is_named(n))

    # ------------------------------------------------------------- the chain
    keys = []
    for name, m in mobs.items():
        for item, n in m['loot'].items():
            if KEY_RE.search(item):
                keys.append(dict(key=item, boss=name, n=n))
    keys.sort(key=lambda k: (k['key']))

    efreeti = collections.defaultdict(collections.Counter)
    for name, m in mobs.items():
        for item, n in m['loot'].items():
            if EFREETI_RE.search(item):
                efreeti[name][item] += n

    runes = collections.Counter()
    rune_sources = collections.defaultdict(set)
    for name, m in mobs.items():
        for item, n in m['loot'].items():
            r = RUNE_RE.match(item)
            if r:
                runes[item] += n
                rune_sources[item].add(name)

    # ------------------------------------------------------- what we resisted
    # `resists` counts lines of the form "You resist <mob>'s <spell>!", so it is
    # what the zone threw at us and failed to land, not what it shrugged off.
    resisted = collections.defaultdict(collections.Counter)
    for s in sessions:
        for spell, casters in ((s.get('control') or {}).get('resists') or {}).items():
            for who, n in casters.items():
                resisted[spell][who] += n

    atk = sorted(f['attackers'] for f in fights)
    out = {
        '_comment': [
            'The Plane of Sky, measured. Generated by _build/skyloot.py - do not hand-edit.',
            'Counts are how many we watched drop. Nothing here is a rate.',
            'Damage to kill is an upper bound on hit points, never a measurement of them.',
            'Island numbers are NOT here: they are page structure and live in _build/build8.py.',
        ],
        'sessions': [dict(date=s.get('date'), window=s.get('window'),
                          character=s.get('character'), kills=s.get('kills'),
                          difficulty=s.get('difficulty'),
                          difficulty_label=s.get('difficulty_label') or 'Base',
                          difficulty_from=s.get('difficulty_from')) for s in sessions],
        'fights': dict(
            n=len(fights),
            bosses=len(byboss),
            dates=sorted({f['date'] for f in fights}),
            # Every Sky fight we hold is at base difficulty. Nothing on this page
            # generalises above D0 and the page has to say so.
            difficulties=sorted({f['difficulty'] for f in fights}),
            attackers_min=min(atk), attackers_max=max(atk),
            attackers_median=int(statistics.median(atk)),
            thin_fights=sum(1 for a in atk if a <= 3),
        ),
        'bosses': bosses,
        # THE DEAREST BOSS, DERIVED ONCE, BECAUSE TWO PAGES COMPARE AGAINST IT.
        #
        # Both the raids index and the Sky page state Sky's cost against
        # Cazic-Thule at Refined, and each computed its own max over the bosses
        # above. They agreed only because they made the same choice - and both
        # chose `damage_max`, which is the largest observed total INCLUDING
        # fights the parser marked a floor. So the pages published 35,946 "or
        # more" for Bazzt Zzzt while /learn/difficulty printed 23,321 for the
        # same boss at the same tier: a lower bound stated ABOVE the fullest
        # complete view, on six of eight bosses.
        #
        # CLAUDE.md's rule is to trust the fullest view of a boss at a tier and
        # treat the rest as lower bounds. `damage_complete_max` is that view and
        # it has been in this file all along with no readers. It is chosen here,
        # once, so the two pages cannot make the choice differently.
        #
        # `is_floor` stays true only if NO complete view exists for that boss -
        # today that is none of the fifteen, and a page must still be able to
        # say "or more" if it ever happens.
        'dearest': (lambda d: dict(
            boss=d['boss'],
            damage=d['damage_complete_max'] if d['damage_complete_max'] else d['damage_max'],
            is_floor=not d['damage_complete_max'],
        ))(max(bosses, key=lambda b: b['damage_complete_max'] or b['damage_max'])),
        'looted_but_unfought': looted_only,
        'keys': keys,
        'efreeti_sources': {k: dict(v.most_common()) for k, v in sorted(efreeti.items())},
        'wind_runes': dict(sorted(runes.items())),
        'wind_rune_sources': {k: sorted(v) for k, v in sorted(rune_sources.items())},
        'resisted': {k: dict(v.most_common()) for k, v in
                     sorted(resisted.items(), key=lambda kv: -sum(kv[1].values()))},
        'distinct_items': len({base(i) for m in mobs.values() for i in m['loot']}),
        'loot_lines': sum(sum(m['loot'].values()) for m in mobs.values()),
    }
    json.dump(out, open('assets/sky-loot.json', 'w', encoding='utf-8', newline='\n'), indent=1)
    print(f"sky-loot.json: {len(bosses)} bosses over {len(fights)} fights, "
          f"{out['distinct_items']} distinct items, {len(keys)} key drops, "
          f"{len(looted_only)} looted-but-unfought")


if __name__ == '__main__':
    main()
