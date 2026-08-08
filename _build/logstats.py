"""Combat logs in, measured figures out.

WHY THIS EXISTS
---------------
Almost everything on this site is read from somewhere. A combat log is the one
source that is measured rather than read: it records what actually happened, in
the live game, on a known date, to a known character. It is the only way to
close the gaps CLAUDE.md lists as the biggest ones — which class kits attach to
which mob, what a fight actually costs, and what a named mob really drops.

It is also the one source that can be over-read, so this is deliberately narrow:
it counts what the log states and attaches the conditions to every figure. A hit
rate measured by a level 26 trio against level 40 mobs is a fact about that
matchup and nothing else, and the output carries the level gap so the page can
say so.

    python3 _build/logstats.py <dir-of-logs>     # writes assets/measured.json

TELLING MOBS FROM PLAYERS
-------------------------
This is the part that goes wrong quietly. A first pass here recorded "Azuria" as
a named mob missing from the Mistmoore plate. Azuria is a player: they dodge,
riposte, parry and carry a thorns shield, and they were fighting the same mobs
we were. Published, that would have invented a mob.

So a name counts as a mob only on positive evidence, never by default:
  - the log says "You have slain <name>", or
  - the log says "<name> has been slain", or
  - it attacked us, or
  - it is written with an article, as trash always is.
Anything else is left out. A named mob that was fought but not killed and never
landed a blow will be missed, which is the right way round to be wrong.

ZONE AND DIFFICULTY
-------------------
The zone line carries both:

    You have entered The Castle of Mistmoore 1 (Awakened).

The parenthesised word is recorded as the zone's stated difficulty label but is
NOT mapped to a D-number here, because that mapping is not yet confirmed. Loot
tier is recorded separately: items drop at +N, and the modal N is the
difficulty by the collaborator's own rule.
"""
import os, sys, re, json, collections, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

TS = re.compile(r'^\[(\w{3}) (\w{3}) (\d{2}) (\d{2}):(\d{2}):(\d{2}) (\d{4})\]\s*(.*)$')
VERBS = (r'(?:hit|slash|bash|crush|pierce|bite|claw|kick|punch|gore|maul|slice|'
         r'backstab|frenzy|strike)')
ARTICLE = re.compile(r'^(?:a|an|the)\s+', re.I)

ZONE = re.compile(r'You have entered (.+?)\.\s*$')
STAMP = re.compile(r'ATTN Claude:\s*(.+?)\'?\s*$')
SLAIN_BY_YOU = re.compile(r'^You have slain (.+?)!')
SLAIN = re.compile(r'^(.+?) has been slain')
HIT_YOU = re.compile(rf'^(.{{1,44}}?) {VERBS}(?:es|s)? YOU for (\d+)')
MISS_YOU = re.compile(rf'^(.{{1,44}}?) tries to {VERBS} YOU, but')
YOU_HIT = re.compile(rf'^You {VERBS}(?:es|s)? (.+?) for (\d+)')
YOU_MISS = re.compile(rf'^You try to {VERBS} (.+?), but')
CAST = re.compile(r'^(.{1,44}?) begins (?:to cast a spell|casting) ?(.*?)\.?$')
LOOT = re.compile(r"looted an? (.+?) from (.+?)'s corpse")
PLUS = re.compile(r'\+(\d)\b')
FACTION = re.compile(r'Your faction standing with (.+?) (?:has|could)')
LEVEL_SELF = re.compile(r'You have (?:gained|reached) level (\d+)')


def parse(path):
    rows = []
    for line in open(path, encoding='utf-8', errors='replace'):
        m = TS.match(line.rstrip('\n'))
        if m:
            when = datetime.datetime.strptime(
                f'{m.group(2)} {m.group(3)} {m.group(7)} {m.group(4)}:{m.group(5)}:{m.group(6)}',
                '%b %d %Y %H:%M:%S')
            rows.append((when, m.group(8)))
    return rows


def collect(rows):
    """Split into zone sessions and count within each."""
    mobs = set()
    for _when, x in rows:
        for rx in (SLAIN_BY_YOU, SLAIN, HIT_YOU, MISS_YOU):
            m = rx.match(x)
            if m:
                mobs.add(m.group(1).strip())
        m = CAST.match(x)
        if m and ARTICLE.match(m.group(1).strip()):
            mobs.add(m.group(1).strip())
    mobs = {m for m in mobs if m and not m.startswith('You')}

    # Character context is usually stamped before zoning in — the trio and level
    # were noted at 11:07:53 and the zone was entered at 11:08:57, which put them
    # in different sessions. Every stamp in the file is therefore offered to
    # every session as context; session-scoped stamps stay separate.
    all_stamps = [m.group(1).strip().rstrip("'")
                  for _w, x in rows for m in [STAMP.search(x)] if m]

    def new_session(zone, diff, when):
        return dict(zone=zone, difficulty_label=diff,
                    date=when.strftime('%d %b %Y'),
                    start=when.strftime('%H:%M'), end=when.strftime('%H:%M'),
                    stamps=[], kills=collections.Counter(),
                    casts=collections.defaultdict(collections.Counter),
                    loot=collections.defaultdict(collections.Counter),
                    drop_tiers=collections.Counter(), faction=collections.Counter(),
                    dmg=collections.defaultdict(list),
                    mob_hit=collections.Counter(), mob_miss=collections.Counter(),
                    you_hit=0, you_miss=0, context=all_stamps)

    # A log that starts mid-zone has no "You have entered" line at all — the
    # Blackburrow stress test is exactly that, and its combat is worth keeping.
    # Open an unnamed session so nothing before the first zone line is lost. The
    # zone stays null rather than being guessed from context.
    # Split on a zone change, and also on any gap longer than GAP: a log that
    # starts mid-zone has no zone line at all, and without this the 4 August
    # stress test and the 8 August Mistmoore run merged into one "session"
    # spanning four days.
    GAP = datetime.timedelta(minutes=30)
    sessions, cur, prev = [], None, None
    for when, x in rows:
        if cur is None or (prev is not None and when - prev > GAP):
            cur = new_session(cur['zone'] if cur else None,
                              cur['difficulty_label'] if cur else None, when)
            sessions.append(cur)
        prev = when
        m = ZONE.search(x)
        if m:
            raw = m.group(1).strip()
            diff = None
            dm = re.search(r'\((.+?)\)\s*$', raw)
            if dm:
                diff = dm.group(1)
                raw = raw[:dm.start()].strip()
            raw = re.sub(r'\s+\d+$', '', raw)
            # Re-entering the same zone is not a new session. Dying and
            # returning, or stepping out and back, emits another zone line and
            # was splitting one Mistmoore run into a 15-minute session and a
            # 2-minute one. A real break is caught by the gap rule above.
            if cur and cur['zone'] == raw and cur['difficulty_label'] == diff:
                continue
            cur = new_session(raw, diff, when)
            sessions.append(cur)
            continue
        cur['end'] = when.strftime('%H:%M')

        m = STAMP.search(x)
        if m:
            cur['stamps'].append(m.group(1).strip().rstrip("'"))
        m = SLAIN_BY_YOU.match(x)
        if m and m.group(1).strip() in mobs:
            cur['kills'][m.group(1).strip()] += 1
        m = CAST.match(x)
        if m:
            who = m.group(1).strip()
            if who in mobs:
                cur['casts'][who][(m.group(2) or '').strip() or '(unnamed)'] += 1
        m = LOOT.search(x)
        if m:
            item, src = m.group(1).strip(), m.group(2).strip()
            if src in mobs:
                cur['loot'][src][item] += 1
            first = PLUS.search(item)
            if first and 'to create' not in x:
                cur['drop_tiers'][first.group(1)] += 1
        m = FACTION.search(x)
        if m:
            cur['faction'][m.group(1).strip()] += 1
        m = HIT_YOU.match(x)
        if m and m.group(1).strip() in mobs:
            cur['dmg'][m.group(1).strip()].append(int(m.group(2)))
            cur['mob_hit'][m.group(1).strip()] += 1
        m = MISS_YOU.match(x)
        if m and m.group(1).strip() in mobs:
            cur['mob_miss'][m.group(1).strip()] += 1
        if YOU_HIT.match(x):
            cur['you_hit'] += 1
        if YOU_MISS.match(x):
            cur['you_miss'] += 1
    return sessions


def summarise(s):
    mh, mm = sum(s['mob_hit'].values()), sum(s['mob_miss'].values())
    out = dict(zone=s['zone'], difficulty_label=s['difficulty_label'], date=s['date'],
               window=f"{s['start']}-{s['end']}", stamps=s['stamps'],
               kills=sum(s['kills'].values()), distinct=len(s['kills']),
               drop_tiers=dict(sorted(s['drop_tiers'].items())),
               faction=dict(s['faction'].most_common()),
               context=s.get('context', []),
               you_hit=s['you_hit'], you_miss=s['you_miss'],
               mob_hit=mh, mob_miss=mm, mobs={})
    for name, v in s['dmg'].items():
        h, ms = s['mob_hit'].get(name, 0), s['mob_miss'].get(name, 0)
        out['mobs'][name] = dict(
            swings=h + ms, landed=h, avg=round(sum(v) / len(v), 1), max=max(v),
            casts=dict(s['casts'][name].most_common()) if name in s['casts'] else {},
            loot=dict(s['loot'][name].most_common()) if name in s['loot'] else {})
    for name in s['casts']:
        out['mobs'].setdefault(name, dict(swings=0, landed=0, avg=None, max=None,
                                          casts=dict(s['casts'][name].most_common()),
                                          loot=dict(s['loot'][name].most_common()) if name in s['loot'] else {}))
    for name in s['loot']:
        out['mobs'].setdefault(name, dict(swings=0, landed=0, avg=None, max=None,
                                          casts={}, loot=dict(s['loot'][name].most_common())))
    return out


def build(src):
    files = ([src] if os.path.isfile(src)
             else [os.path.join(src, f) for f in sorted(os.listdir(src)) if f.endswith('.txt')])
    sessions = []
    for f in files:
        for s in collect(parse(f)):
            if sum(s['kills'].values()) or s['dmg']:
                sessions.append(summarise(s))
    json.dump(sessions, open('assets/measured.json', 'w', encoding='utf-8', newline='\n'),
              indent=1)
    print(f"{len(files)} log file(s) -> {len(sessions)} session(s) with combat")
    for s in sessions:
        th, tm_ = s['you_hit'], s['you_miss']
        print(f"  {s['zone']} ({s['difficulty_label']}) {s['date']} {s['window']}: "
              f"{s['kills']} kills / {s['distinct']} distinct, {len(s['mobs'])} mobs measured, "
              f"your hit rate {100*th/max(1,th+tm_):.1f}%, drops {s['drop_tiers']}")
        for line in s['stamps']:
            print(f"      stamp: {line[:110]}")


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else 'state/logs')
