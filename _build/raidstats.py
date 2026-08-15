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

WHO WAS ACTUALLY THERE
----------------------
The damage line names its attacker, and for a month nothing read it. Every
figure in this file was published as the work of our own trio - the difficulty
page said Master Yael was "killed once at every difficulty by one trio in one
session" - and every one of those kills was a **public pick-up raid**. Five or
six players landed hits on each; our character dealt 13-19% of the damage.

The damage totals were never wrong. They sum every attacker, which is what
damage-to-kill means, and the D4 arithmetic was re-checked line by line and
comes to 242,060 exactly. What was wrong was the sentence beside them, and it
was wrong in the direction that misleads hardest: a reader planning to take a
duo into The Hole at D4 would have read "one trio did this" and believed it.

So every fight now records how many attackers there were and what share was
ours. Names are counted and thrown away - other players are not named on this
site outside the credits - but the count and the share go in the record, where
a page cannot restate them wrongly.

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
# EXACTLY as the game writes them. "Cazic Thule" and "Innoruuk" were guesses
# and neither ever matched a line: the game writes "Cazic-Thule" with a hyphen
# and "Innoruuk, the Prince of Hate" in full. Both gods were killed on 12 and 13
# August and this file recorded nothing, because a boss whose name is wrong is
# indistinguishable from a boss nobody fought.
BOSSES = ["Master Yael", "Lord Nagafen", "Lady Vox", "Phinigel Autropos",
          "a dracoliche",
          # Plane of Fear
          "Cazic-Thule", "Dread", "Fright", "Terror",
          # Plane of Hate
          "Innoruuk, the Prince of Hate", "Avatar of Abhorrence",
          "Maestro of Rancor", "Lord of Ire", "Lord of Loathing",
          "Master of Spite", "Mistress of Scorn", "High Priest M`kari",
          "Magi P`tasa", "Grandmaster R`tal", "Coercer T`vala",
          "Ashenbone Broodmaster",
          # Plane of Sky. All six loop bosses plus the efreeti line, killed
          # 14-15 Aug 2026. The bee island runs several named variants rather
          # than one, which no source we hold mentions.
          "Bazzt Zzzt", "Gorgalosk", "Protector of Sky", "Keeper of Souls",
          "Sister of the Spire", "Eye of Veeshan", "Noble Dojorn",
          "Overseer of Air", "The Spiroc Lord", "Thunder Spirit Princess",
          "Bazzzazzt", "Bzzazzt", "Bzzzt", "Bizazzzt", "Bzizzzt",
          # Its article is part of the name and is lowercase, unlike "The
          # Spiroc Lord" two lines up. It was left out of this list until 15
          # Aug 2026, so the zone's own island-8 wanderer had a full loot table
          # in measured.json - the whole efreeti line - and no fight at all.
          "the Hand of Veeshan"]

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


# The verb sits between the attacker and the boss, and the game inflects it per
# weapon and class. Stripping it is what turns "<name> cleaves" and "<name>"
# into one attacker instead of two. A real name is not used even in a comment:
# the whole point of counting attackers rather than listing them is that other
# players are not named by this project outside the credits.
OURS = set()   # every character we hold a log for; filled by main()

MELEE_VERB = re.compile(
    r'\s+(?:hits?|slashe?s?|bashe?s?|crushe?s?|pierces?|bites?|kicks?|punches|'
    r'gores?|mauls?|slices?|backstabs?|frenzies on|strikes?|claws?|slams?|'
    r'cleaves?|smites?|shoots?|rends?|stings?|lashes?)$', re.I)


def attacker_name(prefix):
    """The attacker from a damage line's prefix, verb removed."""
    return MELEE_VERB.sub('', prefix.strip()).strip() or '(unnamed)'


def boss_pat(b):
    """The boss name as a pattern, tolerating sentence capitalisation.

    A name whose own article is lowercase gets capitalised when it opens a
    line, so the game writes "hits the Hand of Veeshan for 409 points" mid-line
    and "The Hand of Veeshan has been slain by" at the start of one. Matching
    either spelling literally loses half the fight, and losing the slain line
    loses the fight entirely. Every other boss here begins with a capital
    already - "The Spiroc Lord" is written that way in both positions - so this
    returns the plain escape for them and changes nothing.
    """
    e = re.escape(b)
    return f'[{b[0].upper()}{b[0]}]{e[1:]}' if b[:1].islower() else e


def parse_log(path):
    boss_re = {b: dict(
        dmg=re.compile(rf'\b{boss_pat(b)} for (\d+) points? of damage\.$'),
        # Who swung. The damage line names its attacker before the verb, and
        # until 11 Aug 2026 nothing read it - so five-player pick-up raids were
        # recorded and published as "one trio in one session". See WHO WAS
        # ACTUALLY THERE in the module docstring.
        attacker=re.compile(rf'^(.*?) \b{boss_pat(b)} for \d+ points? of damage\.$'),
        spell=re.compile(rf'^{boss_pat(b)} has taken (\d+) damage from (.+?)\.$'),
        slain=re.compile(rf'^(?:{boss_pat(b)} has been slain by|You have slain {boss_pat(b)})'),
        cast=re.compile(rf'^{boss_pat(b)} begins casting (.+?)\.$'),
        heal=re.compile(rf'^{boss_pat(b)} healed itself for (\d+) hit points by (.+?)\.$'),
        melee=re.compile(rf'^{boss_pat(b)} (\w+) .+? for (\d+) points? of damage\.$'),
    ) for b in BOSSES}
    # The cheap prefilter below is a case-sensitive substring test, so it has to
    # know the same thing boss_pat does or it discards the lines before any
    # pattern sees them.
    boss_sub = {b: (b if not b[:1].islower() else b[1:]) for b in BOSSES}

    char = re.search(r'eqlog_([^_]+)_', os.path.basename(path))
    char = char.group(1) if char else "unknown"
    zone = None
    open_fights = {}
    # When the boss was first seen doing anything in this zone. A fight opens on
    # the first damage dealt TO the boss, so if the boss was already swinging or
    # casting well before that, we arrived after it had been engaged and the
    # damage total is a floor rather than the cost of the fight.
    first_active = {}
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
                first_active.clear()
                zone = z.group(1)
            continue
        for boss, rx in boss_re.items():
            if boss_sub[boss] not in b:
                continue
            if boss not in open_fights and boss not in first_active and (
                    rx['melee'].match(b) or rx['cast'].match(b)):
                first_active[boss] = ts
            d = rx['dmg'].search(b) or rx['spell'].match(b)
            if d:
                f = open_fights.setdefault(boss, dict(
                    boss=boss, zone=zone, character=char, start=ts, damage=0,
                    healed=0, heal_count=0, casts=collections.Counter(),
                    melee_verbs=collections.Counter(), melee_hits=[],
                    by=collections.Counter(),
                    active_since=first_active.get(boss)))
                f['damage'] += int(d.group(1))
                a = rx['attacker'].match(b)
                if a:
                    f['by'][attacker_name(a.group(1))] += int(d.group(1))
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
    # WHO WAS ACTUALLY THERE.
    # Names are counted and thrown away. Other players do not get named on this
    # site outside the credits, so the record carries how many there were and
    # what share was ours, which is all a reader needs to judge the figure.
    # A mob or a pet is written with an article, exactly as in logstats.py; a
    # player name is not.
    # OURS is every character we hold a log for. A log calls its own character
    # "You" and names the rest, so without that set the share came out as one
    # character's contribution and the partner read as a stranger.
    late = None
    if f.get('active_since'):
        late = int((t(f['start'], '%a %b %d %H:%M:%S %Y')
                    - t(f['active_since'], '%a %b %d %H:%M:%S %Y')).total_seconds())
        late = late if late > 0 else None
    by = f.get('by') or {}
    total = sum(by.values()) or 1
    mine = {'You', 'YOUR', f['character']} | set(OURS)
    ours = sum(v for k, v in by.items() if k in mine)
    others = [k for k in by
              if k not in mine and not re.match(r'^(a|an|the)\s', k, re.I)]
    return {
        "boss": f['boss'], "zone": f['zone'], "character": f['character'],
        # Needed to tell one fight logged twice from the same boss killed twice.
        "start_ts": f['start'],
        "attackers": 1 + len(others),
        "other_players": len(others),
        "our_damage_share_pct": round(100 * ours / total, 1),
        # Late RELATIVE TO THE FIGHT, not in absolute seconds. A flat 20s
        # threshold marked a 273-second kill as partial because the boss was
        # already swinging at somebody when we arrived, which is simply what
        # walking into a fifteen-player raid looks like. Missing a quarter of
        # the fight is what makes a total a floor.
        "joined_late_seconds": late,
        "damage_is_floor": late is not None and secs and late > max(20, 0.25 * secs),
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


def merge(rows):
    """One fight, however many clients logged it.

    Two characters in the same group produce two logs of the same kill, and
    publishing both as separate kills would double the sample and claim a
    precision we do not have. Merged instead - and the disagreement between
    clients is kept, because it turns out to be the most useful number here. A
    client records only what it was in range to see, so two parses of one fight
    differ by however much each missed. That difference is this method's error
    bar, measured rather than assumed.
    """
    # SAME FIGHT, NOT SAME DAY.
    # This keyed on (boss, difficulty, date) alone, which was right while we
    # killed each boss once per tier per night. In the planes the raid killed
    # the same lieutenant several times in an evening, and two separate kills
    # merged into one "fight" with a fabricated range - Lord of Ire published
    # as "61,014-401,708, two clients 84.8% apart" on a night when only one
    # character was logging at all.
    #
    # Two clients of ONE fight start within seconds of each other and are
    # different characters. The same character killing a boss twice is always
    # two fights, however close together.
    def same_fight(a, b):
        if a['character'] == b['character']:
            return False
        try:
            ta = datetime.datetime.strptime(a['start_ts'], '%a %b %d %H:%M:%S %Y')
            tb = datetime.datetime.strptime(b['start_ts'], '%a %b %d %H:%M:%S %Y')
        except (KeyError, ValueError):
            return True          # no timestamps: fall back to the old behaviour
        return abs((ta - tb).total_seconds()) <= 120

    buckets = collections.defaultdict(list)
    for r in rows:
        bucket = buckets[(r['boss'], r['difficulty'], r['date'])]
        for grp in bucket:
            if any(same_fight(r, o) for o in grp):
                grp.append(r)
                break
        else:
            bucket.append([r])
    # flatten to one entry per fight, so the loop below is unchanged
    g = []
    for (boss, diff, date), groups in buckets.items():
        for obs in groups:
            g.append((boss, diff, date, obs))
    out = []
    for boss, diff, date, obs in g:
        dmg = [o['damage_to_kill'] for o in obs]
        spells = {}
        for o in obs:
            for k, v in o['spells'].items():
                spells[k] = max(spells.get(k, 0), v)
        heals = [o['self_heal_count'] for o in obs]
        out.append({
            "boss": boss, "difficulty": diff,
            "difficulty_label": obs[0]['difficulty_label'],
            "date": date, "zone": obs[0]['zone'],
            "group_instance": obs[0]['group_instance'],
            "observers": sorted(o['character'] for o in obs),
            # The largest attacker count any client saw, and the smallest share
            # of the damage ours turned out to be. Both are the cautious
            # direction: a client that was out of position undercounts both.
            "attackers": max(o.get('attackers', 1) for o in obs),
            "other_players": max(o.get('other_players', 0) for o in obs),
            "our_damage_share_pct": max(o.get('our_damage_share_pct', 0.0)
                                        for o in obs),
            # A floor only if EVERY client that saw the fight joined it late.
            # One client in position from the start saw the whole thing.
            "damage_is_floor": all(o.get('damage_is_floor') for o in obs),
            "joined_late_seconds": min((o.get('joined_late_seconds') or 0)
                                       for o in obs) or None,
            "damage_low": min(dmg), "damage_high": max(dmg),
            "damage_spread_pct": round((max(dmg) - min(dmg)) / max(dmg) * 100, 1),
            "seconds": max(o['seconds'] for o in obs),
            # union across clients: a spell one client missed still happened
            "spells": dict(sorted(spells.items(), key=lambda kv: -kv[1])),
            "spells_distinct": len(spells),
            "self_heal_low": min(heals), "self_heal_high": max(heals),
            "melee_verbs": sorted({v for o in obs for v in o['melee_verbs']}),
        })
    # A CLIENT THAT SAW FEW ATTACKERS SAW LITTLE OF THE FIGHT.
    #
    # Joining late is not the only way to under-witness a raid. In a fifteen
    # player raid spread across a plane, a client in the wrong place logs a
    # fraction of the damage without ever being late.
    #
    # The evidence is in the file itself. Where two kills of one boss at one
    # tier were both witnessed with a similar attacker count, the totals agree:
    # Master Yael at D1, six attackers both times, 1.1x apart. Where one kill
    # saw two attackers and the other twelve, they are 60x apart. So the
    # attacker count is the tell, and the fullest view of a boss at a tier is
    # the one to trust.
    best = {}
    for r in out:
        k = (r['boss'], r['difficulty'])
        if r['attackers'] > best.get(k, (0,))[0]:
            best[k] = (r['attackers'], r['damage_low'])
    for r in out:
        k = (r['boss'], r['difficulty'])
        fuller = best.get(k, (0, 0))[0]
        if r['attackers'] < fuller:
            r['damage_is_floor'] = True
            r['partial_reason'] = (
                f"saw {r['attackers']} attackers where another kill of this boss "
                f"at this tier saw {fuller}")
        elif r.get('damage_is_floor'):
            r['partial_reason'] = (
                f"joined {r.get('joined_late_seconds')}s after the boss was engaged")
    out.sort(key=lambda r: (r['boss'],
                            r['difficulty'] if r['difficulty'] is not None else -1))
    return out


def main(src):
    logs = sorted(glob.glob(os.path.join(src, '*eqlog*.txt')))
    if not logs:
        print("no logs under " + src)
        return
    for p in logs:
        m = re.search(r'eqlog_([^_]+)_', os.path.basename(p))
        if m:
            OURS.add(m.group(1))
    raw = []
    for path in logs:
        raw += [fmt(f) for f in parse_log(path)]
    out = merge(raw)
    json.dump(out, open('assets/raids-measured.json', 'w', encoding='utf-8',
                        newline=chr(10)), indent=1)
    print(f"raids-measured.json: {len(out)} fights from {len(raw)} client "
          f"observations across {len(logs)} log(s)")
    for r in out:
        rng = (f"{r['damage_low']:,}" if r['damage_low'] == r['damage_high']
               else f"{r['damage_low']:,}-{r['damage_high']:,}")
        print(f"   D{r['difficulty']} {r['boss']:<16} {rng:>19}  {r['seconds']:>4}s  "
              f"{r['spells_distinct']:>2} spells  heals "
              f"{r['self_heal_low']}-{r['self_heal_high']}  "
              f"{r['attackers']} attackers, ours {r['our_damage_share_pct']}%  "
              f"({len(r['observers'])} clients, {r['damage_spread_pct']}% apart)")


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'state/logs')
