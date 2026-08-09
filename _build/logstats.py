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

The parenthesised word is the tier name: D0 Base/Normal, D1 Awakened, D2
Adaptive, D3 Fused, D4 Refined. Loot is read separately — items drop at +N and
the modal N is the difficulty — and the two are reported apart rather than
collapsed, because they are independent and their agreement is evidence. They
agreed on the 8 Aug Mistmoore session. Where they disagree, the page says the
difficulty is unresolved instead of choosing.

BACKSTAB
--------
Kept apart from ordinary swings. Mistmoore's familiars hit for 1-38 in melee and
100-143 from behind, so a combined average of "10.5, max 143" describes neither.
It is also the clearest class evidence in a log: a spell list can belong to one
broad caster kit, but backstab is a rogue ability, and a mob type doing both is
running two kits.
"""
import os, sys, re, json, collections, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

TS = re.compile(r'^\[(\w{3}) (\w{3}) (\d{2}) (\d{2}):(\d{2}):(\d{2}) (\d{4})\]\s*(.*)$')
VERBS = (r'(?:hit|slash|bash|crush|pierce|bite|claw|kick|punch|gore|maul|slice|'
         r'backstab|frenzy|strike)')
ARTICLE = re.compile(r'^(?:a|an|the)\s+', re.I)

# The difficulty tier names used by personal and public instancing, supplied by
# the collaborator on 8 Aug 2026. Independently corroborated for D1 by our own
# log: the zone line read "(Awakened)" and 22 of 27 drops were +1, so the label
# and the loot-tier rule agree without being derived from each other.
DIFFICULTY = {'base': 0, 'normal': 0, 'base / normal': 0,
              'awakened': 1, 'adaptive': 2, 'fused': 3, 'refined': 4}

ZONE = re.compile(r'You have entered (.+?)\.\s*$')
STAMP = re.compile(r'ATTN Claude:\s*(.+?)\'?\s*$')
SLAIN_BY_YOU = re.compile(r'^You have slain (.+?)!')
SLAIN = re.compile(r'^(.+?) has been slain')
HIT_YOU = re.compile(rf'^(.{{1,44}}?) ({VERBS}(?:es|s)?) YOU for (\d+)')
MISS_YOU = re.compile(rf'^(.{{1,44}}?) tries to {VERBS} YOU, but')
YOU_HIT = re.compile(rf'^You {VERBS}(?:es|s)? (.+?) for (\d+)')
YOU_MISS = re.compile(rf'^You try to {VERBS} (.+?), but')
CAST = re.compile(r'^(.{1,44}?) begins (?:to cast a spell|casting) ?(.*?)\.?$')
LOOT = re.compile(r"looted an? (.+?) from (.+?)'s corpse")
PLUS = re.compile(r'\+(\d)\b')
FACTION = re.compile(r'Your faction standing with (.+?) (?:has|could)')
FACTION_D = re.compile(r'Your faction standing with (.+?) has been adjusted by (-?\d+)')

# THE MESSAGE THAT IS NOT A MISSING NUMBER
# Blackburrow logged 2,631 faction lines across 42 kills and not one was
# attributable, which read as a parser gap and was published as "direction
# unknown". It is not a gap. EverQuest reports a faction that has hit its floor
# or ceiling in words instead of numbers:
#
#   Your faction standing with Undead Frogloks of Guk could not possibly get any worse.
#   Your faction standing with Frogloks of Guk could not possibly get any better.
#
# The direction is right there. "worse" is a kill that would have lowered the
# faction and could not; "better" is one that would have raised it. Only the
# magnitude is unknowable, because nothing moved. Reading these as noise threw
# away the direction for every capped faction we have ever logged - in the
# 9 Aug Lower Guk run they are 337 of the 355 faction lines.
FACTION_CAP = re.compile(
    r'Your faction standing with (.+?) could not possibly get any (better|worse)')
EXP = re.compile(r'You gain (?:party )?experience! \(([\d.]+)%\)')

# Faction arrives in the same second as the kill that caused it, just before the
# "You have slain" line, so it can be attributed per mob rather than only summed.
# It is worth doing: killing Xicotl moved Mayong Mistmoore by -300 where a trash
# kill moves it by -5, so a named is 60x a trash kill on that faction. No wiki
# carries that, and it is the whole basis of a faction planner.

# Escapes. Succor and Evacuate teleport the group out, so a cast of one is a
# decision that the fight was lost — the single most useful judgement a log
# records, and one no wiki carries. What was being fought and what it had just
# done are captured with it, because "we ran" is only useful with the reason.
ESCAPE = re.compile(r'\b(\w+ )?(Succor|Evacuate|Evacuation)\b', re.I)
ENGAGE = re.compile(r'^(.{1,44}?) (?:says|shouts), ')
ESCAPE_WINDOW = datetime.timedelta(seconds=45)

# A stamp reporting the group changing is flagged, not split on. Every measured
# figure is conditional on who was present, and at 11:57:34 on 8 Aug the healer
# lost connection — but she was back at 11:58:07, 33 seconds later. Cutting the
# session there would have halved the sample to record a gap shorter than one
# fight. So the change is marked in place and shown on the page, and the reader
# is told conditions varied rather than being handed two thin sessions.
CONDITION_CHANGE = re.compile(
    r'(?:lost connection|disconnected|linkdead|logged off|logging off|'
    r'left the group|swapped|switching to|changed (?:trio|difficulty|class))',
    re.I)
LEVEL_SELF = re.compile(r'You have (?:gained|reached) level (\d+)')

# CONTROL EFFECTS — what stops you playing, and what it came from.
#
# This is the most actionable thing a log holds and it took a death to notice.
# The collaborator carries a 100% immunity to stunning MELEE attacks, and it
# works: 206 melee stuns avoided in one session. Every stun that actually landed
# came from a spell, which that immunity does not cover — 29 of 35 from Lightning
# Bolt alone. Meanwhile Screaming Terror, assumed to be fear, produced no fear
# behaviour at all: no fleeing, no "afraid", just a scream and a lockout.
#
# So control is counted by what the log says happened, not by what a spell is
# assumed to be, and the spell that caused each stun is captured with it. That
# is what turns "this mob is dangerous" into a kill order.
STUN_LANDED = re.compile(r'^You are stunned!')
STUN_AVOIDED = re.compile(r'^You avoid the stunning blow')
STUN_LOCKOUT = re.compile(r"^You can't attack while stunned")
SCREAM_START = re.compile(r'^You begin to scream')
SCREAM_END = re.compile(r'^You stop screaming')
BY_SPELL = re.compile(r'\bby ([A-Z][^.]*?)\.?\s*$')
RESISTED = re.compile(r'^You resist (.+?)\'s (.+?)!')
FEAR_WORDS = re.compile(r'You (?:flee|are afraid|are terrified|run in terror)')

# Signals that a name belongs to a person rather than a mob. Nothing hostile
# heals us and nothing hostile speaks in a chat channel, so these are safe one
# way: they never mistake a mob for a player.
HEALED_YOU = re.compile(r'^(.{1,24}?) healed you(?: over time)? for \d+')
YOU_HEALED = re.compile(r'^You healed (.{1,24}?) for \d+')
CHATTER = re.compile(r'^(\w[\w`\'-]{2,23}) (?:tells|says) (?:the |your )?'
                     r'(?:guild|group|party|raid|fellowship|General|OOC|auction)')
GROUP_CAST = re.compile(r'^(\w[\w`\'-]{2,23})(?:\'s)? (?:image shimmers|begins to cast a spell on you)')


# Filenames carry a date stamp so a rotated log cannot overwrite an earlier
# one, and a trailing digit so two logs from the same character can coexist:
#   eqlog_Avenrae_rivervale_2026-08-08-pm.txt  ->  Avenrae
CHAR = re.compile(r'eqlog_([A-Za-z]+?)\d*_', re.I)


def character_of(path):
    """Whose log this is. Damage taken, hit rates and control effects are all
    from the logger's point of view, so two characters' figures must never be
    averaged together — the healer's log and the tank's describe different
    fights."""
    m = CHAR.search(os.path.basename(path))
    return m.group(1) if m else None


# ZONE STATED BY THE COLLABORATOR, NOT INFERRED
#
# A log that begins mid-zone has no "You have entered" line, so its zone is
# unknown however obvious it looks. The 8 August afternoon logs start at 14:22
# and 14:34, after a client restart, and carried 411 and 5 kills against a null
# zone — the largest single sample the project has, reaching no plate.
#
# Rather than guess from context, the zone is recorded here as a statement:
# "The entire log took place inside Mistmoore", 8 Aug 2026. That is a person
# telling us where they were, which is evidence, and it is written down as such
# so a later reader can see it was asserted rather than parsed.
# CONDITIONS STATED BY THE COLLABORATOR
#
# A log records what happened, not why. On the afternoon of 8 August the
# healer's client froze and crashed repeatedly, and the collaborator reports
# that every death that day but one fell during or just after a crash. Those
# deaths, and any escape called because the group had suddenly lost its healer,
# measure a technical fault rather than the encounter — and the plate presents
# escapes as a judgement the group made about a fight.
#
# Recorded here so the affected sessions carry the caveat in public rather than
# reading as evidence about the zone. Stated by a person, like ZONE_STATED,
# not inferred from the log.
SESSION_CAVEAT = {
    ('Avenrae', '08 Aug 2026', '14:34-16:43'):
        "The healer's client was freezing and crashing through this session. The "
        "collaborator reports that every death this day but one fell during or just "
        "after a crash, so deaths and any escape here may record a technical failure "
        "rather than the fight going badly.",
    ('Avenrae', '08 Aug 2026', '17:15-18:14'):
        "The healer's client was freezing and crashing through this session. The "
        "collaborator reports that every death this day but one fell during or just "
        "after a crash, so deaths and any escape here may record a technical failure "
        "rather than the fight going badly.",
    ('Shara', '08 Aug 2026', '14:22-15:33'):
        "Client freezing and crashing repeatedly through this session; the low kill "
        "count reflects that rather than the zone.",
    ('Shara', '08 Aug 2026', '15:33-18:14'):
        "Client freezing and crashing repeatedly through this session; the low kill "
        "count reflects that rather than the zone.",
}

ZONE_STATED = {
    # Avenrae's 9 Aug log opens mid-zone with no "You have entered" line.
    # Shara's log covers the same clock window and carries
    # "The Ruins of Old Guk 1 (Awakened)", and both characters stamped the
    # party channel with "D1 Awakened Lower Guk starting run" at 11:11.
    ('Avenrae', '09 Aug 2026', '11:10-13:16'): 'The Ruins of Old Guk',
    ('Avenrae', '08 Aug 2026', '14:34-16:43'): 'The Castle of Mistmoore',
    ('Shara',   '08 Aug 2026', '14:22-15:33'): 'The Castle of Mistmoore',
}


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


def collect(rows, character=None):
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

    # Subtract the people. "<name> has been slain" is evidence something died,
    # not evidence it was a mob: Shara was killed by Lasna Cheroon and duly
    # appeared in the named-mob table of a published plate. That is the Azuria
    # error arriving from the other direction, and the same rule applies —
    # positive evidence only, and people leave plenty of it. Nothing hostile
    # heals us, and nothing hostile talks in a chat channel.
    players = set()
    for _w, x in rows:
        for rx in (HEALED_YOU, YOU_HEALED, CHATTER, GROUP_CAST):
            m = rx.match(x)
            if m:
                players.add(m.group(1).strip())
    mobs -= players

    # Character context is usually stamped before zoning in — the trio and level
    # were noted at 11:07:53 and the zone was entered at 11:08:57, which put them
    # in different sessions. Every stamp in the file is therefore offered to
    # every session as context; session-scoped stamps stay separate.
    all_stamps = [{'at': w.strftime('%H:%M'), 'date': w.strftime('%d %b %Y'),
                   'text': m.group(1).strip().rstrip("'")}
                  for w, x in rows for m in [STAMP.search(x)] if m]

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
                    you_hit=0, you_miss=0, context=all_stamps, escapes=[],
                    difficulty_num=None, character=character,
                    ctl=dict(melee_avoided=0, lockout_lines=0, fear_lines=0,
                             stuns=collections.Counter(),
                             stun_casters=collections.defaultdict(collections.Counter),
                             resists=collections.defaultdict(collections.Counter),
                             screams=0, scream_seconds=0),
                    fac_by_mob=collections.defaultdict(dict),
                    cap_by_mob=collections.defaultdict(dict),
                    exp_by_mob=collections.defaultdict(list))

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
            diff = dnum = None
            # "The Castle of Mistmoore 1 (Awakened)". The number was read as an
            # instance id and discarded. It is the difficulty: Shara's log has
            # Befallen 1 (Awakened), Blackburrow 2 (Adaptive), Befallen 3
            # (Fused) and The City of Guk 4 (Refined), matching the published
            # tier names exactly. So every zone line states the difficulty twice
            # and the two are checked against each other.
            dm = re.search(r'\s+(\d+)\s*\((.+?)\)\s*$', raw)
            if dm:
                dnum, diff = int(dm.group(1)), dm.group(2)
                raw = raw[:dm.start()].strip()
            else:
                dm = re.search(r'\s*\((.+?)\)\s*$', raw)
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
            cur['difficulty_num'] = dnum
            sessions.append(cur)
            continue
        cur['end'] = when.strftime('%H:%M')

        m = STAMP.search(x)
        if m:
            note = m.group(1).strip().rstrip("'")
            cur['stamps'].append({'at': when.strftime('%H:%M'), 'text': note,
                                  'conditions': bool(CONDITION_CHANGE.search(note))})
        ctl = cur['ctl']
        if STUN_AVOIDED.match(x):
            ctl['melee_avoided'] += 1
        if STUN_LOCKOUT.match(x):
            ctl['lockout_lines'] += 1
        if FEAR_WORDS.search(x):
            ctl['fear_lines'] += 1
        if STUN_LANDED.match(x):
            cur['_stun_at'] = when
        elif cur.get('_stun_at') and (when - cur['_stun_at']).total_seconds() <= 2:
            # the line after "You are stunned!" names what did it
            sp = BY_SPELL.search(x)
            if sp:
                spell = sp.group(1).strip()
                ctl['stuns'][spell] += 1
                who = re.match(r'^(.{1,44}?) hit you for', x)
                if who:
                    ctl['stun_casters'][spell][who.group(1).strip()] += 1
                cur['_stun_at'] = None
        if SCREAM_START.match(x):
            ctl['screams'] += 1
            cur['_scream_at'] = when
        if SCREAM_END.match(x) and cur.get('_scream_at'):
            ctl['scream_seconds'] += int((when - cur['_scream_at']).total_seconds())
            cur['_scream_at'] = None
        m = RESISTED.match(x)
        if m:
            ctl['resists'][m.group(2).strip()][m.group(1).strip()] += 1

        m = FACTION_D.search(x)
        if m:
            cur.setdefault('_fac_buf', []).append((when, m.group(1).strip(), int(m.group(2))))
        m = FACTION_CAP.search(x)
        if m:
            # Direction known, magnitude nil. Kept apart from the numeric buffer
            # so a capped faction can never be averaged in as if it moved.
            cur.setdefault('_cap_buf', []).append(
                (when, m.group(1).strip(), 'up' if m.group(2) == 'better' else 'down'))
        m = EXP.search(x)
        if m:
            cur['_exp_buf'] = (when, float(m.group(1)))

        m = SLAIN_BY_YOU.match(x)
        if m and m.group(1).strip() in mobs:
            name = m.group(1).strip()
            cur['kills'][name] += 1
            # attribute anything from the same second to this kill
            for w, fac, delta in cur.get('_fac_buf', []):
                if (when - w).total_seconds() <= 1:
                    cur['fac_by_mob'][name].setdefault(fac, delta)
            cur['_fac_buf'] = []
            for w, fac, direction in cur.get('_cap_buf', []):
                if (when - w).total_seconds() <= 1:
                    cur['cap_by_mob'][name].setdefault(fac, direction)
            cur['_cap_buf'] = []
            eb = cur.get('_exp_buf')
            if eb and (when - eb[0]).total_seconds() <= 1:
                cur['exp_by_mob'][name].append(eb[1])
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
            cur['dmg'][m.group(1).strip()].append((m.group(2), int(m.group(3))))
            cur['mob_hit'][m.group(1).strip()] += 1
        m = MISS_YOU.match(x)
        if m and m.group(1).strip() in mobs:
            cur['mob_miss'][m.group(1).strip()] += 1
        # Everything that engaged us recently, not just whichever mob swung last.
        # Naming only the last one said the group fled "a jeering gargoyle" when
        # Princess Cherista was the actual threat; in a multi-mob fight the last
        # swing is arbitrary.
        recent = cur.setdefault('_recent', [])
        for rx in (HIT_YOU, MISS_YOU):
            mm2 = rx.match(x)
            if mm2 and mm2.group(1).strip() in mobs:
                recent.append((mm2.group(1).strip(), when, None))
                break
        mm2 = CAST.match(x)
        if mm2 and mm2.group(1).strip() in mobs:
            recent.append((mm2.group(1).strip(), when, (mm2.group(2) or '').strip()))

        if ESCAPE.search(x) and 'begins casting' in x:
            who = x.split(' begins casting')[0].strip()
            window = [r for r in recent if (when - r[1]) <= ESCAPE_WINDOW]
            engaged, seen = [], set()
            for nm, _w, _sp in reversed(window):
                if nm not in seen:
                    seen.add(nm)
                    engaged.append(nm)
            last_spell = next(((nm, sp) for nm, _w, sp in reversed(window) if sp), None)
            cur['escapes'].append(dict(
                at=when.strftime('%H:%M:%S'), by=who,
                engaged=engaged[:6],
                after=f'{last_spell[0]} cast {last_spell[1]}' if last_spell else None))
            cur['_recent'] = []

        if YOU_HIT.match(x):
            cur['you_hit'] += 1
        if YOU_MISS.match(x):
            cur['you_miss'] += 1
    return sessions


def summarise(s):
    mh, mm = sum(s['mob_hit'].values()), sum(s['mob_miss'].values())

    # Difficulty two ways, kept separate so they can disagree in the open.
    # The zone line names the tier; the loot tier is the collaborator's own rule,
    # that the modal +N of what drops is the difficulty. Where a log has no zone
    # line at all — one that started mid-zone — only the loot reading survives.
    label = (s['difficulty_label'] or '').strip().lower()
    d_named = DIFFICULTY.get(label)
    d_num = s.get('difficulty_num')
    # An unnumbered, unlabelled zone line is the open world, which is D0.
    if d_named is None and d_num is None and s['zone']:
        d_named = 0
    d_loot = None
    if s['drop_tiers']:
        d_loot = int(max(s['drop_tiers'].items(), key=lambda kv: kv[1])[0])
    agree = None if (d_named is None or d_loot is None) else (d_named == d_loot)

    out = dict(zone=s['zone'], character=s.get('character'),
               difficulty_label=s['difficulty_label'],
               difficulty_num=d_num,
               difficulty=d_num if d_num is not None else
                          (d_named if d_named is not None else d_loot),
               difficulty_from=('zone line, numbered' if d_num is not None else
                                ('zone line' if d_named is not None else
                                 ('loot tier' if d_loot is not None else None))),
               difficulty_label_agrees=(None if (d_num is None or d_named is None)
                                        else d_num == d_named),
               difficulty_agrees=agree, date=s['date'],
               window=f"{s['start']}-{s['end']}", stamps=s['stamps'],
               kills=sum(s['kills'].values()), distinct=len(s['kills']),
               kinds=sorted(s['kills']),
               drop_tiers=dict(sorted(s['drop_tiers'].items())),
               faction=dict(s['faction'].most_common()),
               # Context is offered from the whole file so a trio stamped before
               # zoning in is not lost, but only from the same day. Shara's log
               # spans four days, and an 8 August stamp reading "Level 26" was
               # being printed against Befallen runs from 4 August.
               context=[c for c in s.get('context', [])
                        if c.get('date') in (None, s['date'])],
               escapes=s.get('escapes', []),
               control=dict(
                   melee_stuns_avoided=s['ctl']['melee_avoided'],
                   lockout_lines=s['ctl']['lockout_lines'],
                   fear_lines=s['ctl']['fear_lines'],
                   screams=s['ctl']['screams'],
                   scream_seconds=s['ctl']['scream_seconds'],
                   stuns={k: dict(landed=v,
                                  casters=dict(s['ctl']['stun_casters'][k].most_common()))
                          for k, v in s['ctl']['stuns'].most_common()},
                   resists={k: dict(v.most_common())
                            for k, v in s['ctl']['resists'].items()}),
               faction_by_mob={k: v for k, v in s.get('fac_by_mob', {}).items()},
               faction_capped_by_mob={k: v for k, v in s.get('cap_by_mob', {}).items()},
               exp_by_mob={k: round(sum(v)/len(v), 3) for k, v in s.get('exp_by_mob', {}).items() if v},
               you_hit=s['you_hit'], you_miss=s['you_miss'],
               mob_hit=mh, mob_miss=mm, mobs={})
    for name, v in s['dmg'].items():
        h, ms = s['mob_hit'].get(name, 0), s['mob_miss'].get(name, 0)
        # Backstab is kept apart from ordinary swings. Mistmoore's familiars hit
        # for 1-38 in melee and 100-143 from behind; averaging the two together
        # reports "10.5 average, 143 maximum", which describes neither and hides
        # the thing a reader actually needs to know.
        plain = [d for verb, d in v if verb != 'backstabs']
        backs = [d for verb, d in v if verb == 'backstabs']
        out['mobs'][name] = dict(
            swings=h + ms, landed=h,
            avg=round(sum(plain) / len(plain), 1) if plain else None,
            max=max(plain) if plain else None,
            backstabs=len(backs),
            backstab_avg=round(sum(backs) / len(backs), 1) if backs else None,
            backstab_max=max(backs) if backs else None,
            casts=dict(s['casts'][name].most_common()) if name in s['casts'] else {},
            loot=dict(s['loot'][name].most_common()) if name in s['loot'] else {})
    for name in s['casts']:
        out['mobs'].setdefault(name, dict(swings=0, landed=0, avg=None, max=None,
                                          backstabs=0, backstab_avg=None, backstab_max=None,
                                          casts=dict(s['casts'][name].most_common()),
                                          loot=dict(s['loot'][name].most_common()) if name in s['loot'] else {}))
    for name in s['loot']:
        out['mobs'].setdefault(name, dict(swings=0, landed=0, avg=None, max=None,
                                          backstabs=0, backstab_avg=None, backstab_max=None,
                                          casts={}, loot=dict(s['loot'][name].most_common())))
    return out


def build(src):
    files = ([src] if os.path.isfile(src)
             else [os.path.join(src, f) for f in sorted(os.listdir(src)) if f.endswith('.txt')])
    sessions = []
    for f in files:
        for s in collect(parse(f), character_of(f)):
            if sum(s['kills'].values()) or s['dmg']:
                sessions.append(summarise(s))
    # ACCUMULATE, NEVER REPLACE.
    #
    # This used to write whatever the current log folder produced, which is fine
    # until a log rotates. EverQuest was restarted mid-afternoon on 8 August and
    # began a fresh file at 14:34. Re-running against that alone silently
    # deleted the morning's two Mistmoore sessions — 300 kills — because the
    # output is a wholesale replacement. The raw log was recoverable that time;
    # it will not always be.
    #
    # Sessions are keyed by character, date, window and zone. A re-parse of the
    # same stretch replaces its own entry and nothing else is touched, so the
    # committed record only ever grows.
    existing = []
    try:
        existing = json.load(open('assets/measured.json', encoding='utf-8'))
    except (OSError, ValueError):
        pass

    def keyof(sess):
        # Deliberately NOT keyed on zone. A session's zone can be corrected —
        # the 8 August afternoon runs went from null to Mistmoore once the
        # collaborator said where they were — and keying on it meant the
        # corrected session was added alongside the stale one rather than
        # replacing it. Character, date and window identify a stretch of play
        # uniquely and do not change under correction.
        return (sess.get('character'), sess.get('date'), sess.get('window'))

    for s in sessions:
        if s.get('zone') is None:
            stated = ZONE_STATED.get((s.get('character'), s.get('date'), s.get('window')))
            if stated:
                s['zone'] = stated
                s['zone_from'] = 'stated by the collaborator, not read from the log'
    for s in sessions:
        caveat = SESSION_CAVEAT.get((s.get('character'), s.get('date'), s.get('window')))
        if caveat:
            s['caveat'] = caveat

    merged = {keyof(s): s for s in existing}
    fresh = {keyof(s): s for s in sessions}
    kept = len([k for k in merged if k not in fresh])
    merged.update(fresh)
    out = sorted(merged.values(),
                 key=lambda s: (s.get('date') or '', s.get('window') or ''))

    json.dump(out, open('assets/measured.json', 'w', encoding='utf-8', newline='\n'),
              indent=1)
    print(f"{len(files)} log file(s) -> {len(sessions)} parsed, "
          f"{kept} earlier session(s) preserved, {len(out)} total")
    for s in sessions:
        th, tm_ = s['you_hit'], s['you_miss']
        print(f"  {s.get('character') or '?'} | {s['zone']} D{s['difficulty']} "
              f"({s['difficulty_label']}) {s['date']} {s['window']}: "
              f"{s['kills']} kills / {s['distinct']} distinct, {len(s['mobs'])} mobs measured, "
              f"your hit rate {100*th/max(1,th+tm_):.1f}%, drops {s['drop_tiers']}")
        for line in s['stamps']:
            print(f"      stamp {line['at']}: {line['text'][:100]}")


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else 'state/logs')
