"""Raid boss fights out of combat logs, one row per kill.

    python3 _build/raidstats.py <dir-of-logs>    # writes assets/raids-measured.json

WHY THIS IS NOT logstats.py
---------------------------
logstats.py measures a grinding session: many mobs, many kills, rates across a
window. A raid boss is the opposite shape - one mob, one fight, and the thing
worth knowing is how that single fight differs when you run it again at a higher
difficulty. Same log, different question.

WHAT IT ANSWERS
---------------
CLAUDE.md has carried this as the biggest gap on the site since it was written:
"which class kits attach to which raid boss at D3+ is still unpublished", and
"D3 and D4 are not pinned, by anyone". A log of the same boss killed at every
tier answers both at once.

THE BUG THIS SCRIPT WAS WRITTEN AROUND
--------------------------------------
The first pass at this did not reset the current fight when the character zoned,
so a boss killed in one instance and killed again in the next were summed into
one fight. It reported 304,164 damage for a D2 kill that actually took 139,117,
and made D4 look *cheaper* than D2. Zoning ends a fight. Every total below was
checked a second time by a separate pass that finds the zone line and the death
line by raw line number and sums between them, with no state machine at all.

DAMAGE TO KILL IS NOT HIT POINTS
--------------------------------
It is the damage that had to be dealt, which is what a raid actually cares
about, and it is an upper bound on hit points rather than a measurement of them.
Bosses heal: Master Yael healed itself ten times at D4. Self-healing is counted
and reported separately so the two are never confused, and neither number is
labelled "HP" anywhere.
"""
import os, re, sys, json, glob, collections, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

TS = re.compile(r'^\[(.*?)\]\s*(.*)$')
ZONE = re.compile(r'^You have entered (.+?)\.$')
# "You have entered an area where levitation effects do not function" uses the
# same wording and is not a zone. It cost an entire fight the first time.
NOT_A_ZONE = ('an area where',)

# The bosses worth tracking. Anything else in a log is a grinding session and
# belongs to logstats.py.
BOSSES = ["Master Yael", "Lord Nagafen", "Lady Vox", "Phinigel Autropos",
          "Cazic Thule", "Innoruuk", "Maestro of Rancor", "Fright", "Dread",
          "Terror", "a dracoliche"]

TIER_NAME = {"1": "Awakened", "2": "Adaptive", "3": "Fused", "4": "Refined"}


def tier_of(zone):
    """D-tier from the zone line. The game prints it on entry, which is the
    only unambiguous source: loot +N is modal and can disagree."""
    if not zone:
        return None, None
    m = re.search(r'\s(\d) \(([A-Za-z]+)\)\s*$', zone)
    if not m:
        return 0, "Base"
    return int(m.group(1)), m.group(2)


def parse_log(path):
    boss_re = {b: dict(
        dmg=re.compile(rf'\b{re.escape(b)} for (\d+) points? of damage\.$'),
        spell=re.compile(rf'^{re.escape(b)} has taken (\d+) damage from (.+?)\.$'),
        slain=re.compile(rf'^(?:{re.escape(b)} has been slain by|You have slain {re.escape(b)})'),
        cast=re.compile(rf'^{re.escape(b)} begins casting (.+?)\.$'),
        heal=re.compile(rf'^{re.escape(b)} healed itself for (\d+) hit points by (.+?)\.$'),
        melee=re.compile(rf'^{re.escape(b)} (\w+) .+? for (\d+) points? of damage\.$'),
    ) for b in BOSSES}

    char = re.search(r'eqlog_([^_]+)_', os.path.basename(path))
    char = char.group(1) if char else "unknown"
    zone = None
    open_fights = {}
    done = []
    for line in open(path, encoding='utf-8', errors='replace'):
        m = TS.match(line.rstrip('\n'))
        if not m:
            continue
        ts, b = m.group(1), m.group(2)
        z = ZONE.match(b)
        if z:
            if not z.group(1).startswith(NOT_A_ZONE):
                open_fights.clear()          # zoning ends every fight in progress
                zone = z.group(1)
            continue
        for boss, rx in boss_re.items():
            if boss not in b:
                continue
            d = rx['dmg'].search(b) or rx['spell'].match(b)
            if d:
                f = open_fights.setdefault(boss, dict(
                    boss=boss, zone=zone, character=char, start=ts, damage=0,
                    healed=0, heal_count=0, casts=collections.Counter(),
                    melee_verbs=collections.Counter(), melee_hits=[]))
                f['damage'] += int(d.group(1))
                break
            f = open_fights.get(boss)
            if f is None:
                break
            c = rx['cast'].match(b)
            if c:
                f['casts'][c.group(1)] += 1
                break
            h = rx['heal'].match(b)
            if h:
                f['healed'] += int(h.group(1)); f['heal_count'] += 1
                break
            mv = rx['melee'].match(b)
            if mv:
                f['melee_verbs'][mv.group(1)] += 1
                f['melee_hits'].append(int(mv.group(2)))
            if rx['slain'].match(b):
                f['end'] = ts
                done.append(f)
                open_fights.pop(boss, None)
            break
    return done


def fmt(f):
    t = datetime.datetime.strptime
    secs = int((t(f['end'], '%a %b %d %H:%M:%S %Y')
                - t(f['start'], '%a %b %d %H:%M:%S %Y')).total_seconds())
    num, label = tier_of(f['zone'])
    hits = f['melee_hits']
    return {
        "boss": f['boss'], "zone": f['zone'], "character": f['character'],
        "date": t(f['end'], '%a %b %d %H:%M:%S %Y').strftime('%d %b %Y'),
        "difficulty": num, "difficulty_label": label,
        "group_instance": " - Group" in (f['zone'] or ""),
        "seconds": secs,
        "damage_to_kill": f['damage'],
        "self_healed": f['healed'], "self_heal_count": f['heal_count'],
        "spells": dict(sorted(f['casts'].items(), key=lambda kv: -kv[1])),
        "spells_distinct": len(f['casts']),
        "melee_verbs": dict(f['melee_verbs']),
        "melee_hits": len(hits),
        "melee_min": min(hits) if hits else None,
        "melee_max": max(hits) if hits else None,
    }


def main(src):
    logs = sorted(glob.glob(os.path.join(src, '*eqlog*.txt')))
    if not logs:
        print(f"no logs under {src}")
        return
    out = []
    for p in logs:
        out += [fmt(f) for f in parse_log(p)]
    out.sort(key=lambda r: (r['boss'], r['difficulty'] if r['difficulty'] is not None else -1))
    json.dump(out, open('assets/raids-measured.json', 'w', encoding='utf-8',
                        newline='\n'), indent=1)
    print(f"raids-measured.json: {len(out)} boss kills from {len(logs)} log(s)")
    for r in out:
        print(f"   D{r['difficulty']} {r['boss']:<18} {r['damage_to_kill']:>9,} dmg  "
              f"{r['seconds']:>4}s  {r['spells_distinct']:>2} spells  "
              f"heal {r['self_healed']}")


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'state/logs')
