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

# "<name> has asked you to join the instance: The Plane of Sky 0 (Normal).
#  Would you like to join? ..." - the sentence ends at the first ". ", and
# reading to the end of the line instead carries the question into the zone
# name so that it matches nothing. That mistake made an early pass of this work
# conclude that no invite ever names a tier, which is the opposite of the truth.
INVITE = re.compile(r'asked you to join the instance:\s*(.+?)\.\s')
TIER_RE = re.compile(r'\s(\d) \(([A-Za-z]+)\)\s*$')

# The game's own word for each tier, learned from the invites rather than typed.
# "Normal" is in here because the invites say "0 (Normal)"; the site's own word
# for an INFERRED tier 0 stays "Base", so the label itself records whether the
# number was read or reasoned to.
TIER_LABEL = {}
# zone base -> set of tiers it has ever been entered at, and how many entries.
# Filled by note_invite() during the scan, read by resolve_tier() afterwards.
INSTANCED = collections.defaultdict(set)
INSTANCED_N = collections.Counter()


def note_invite(name):
    base, num, label = split_tier(name)
    if base is None or num is None:
        return
    INSTANCED[base].add(num)
    INSTANCED_N[base] += 1
    TIER_LABEL.setdefault(num, label)


def split_tier(name):
    """("The Plane of Sky", 0, "Normal") or ("The Plane of Sky", None, None)."""
    if not name:
        return None, None, None
    m = TIER_RE.search(name)
    if not m:
        return name.strip(), None, None
    return TIER_RE.sub('', name).strip(), int(m.group(1)), m.group(2)


# WHY THIS IS NOT A ONE-LINE FALLBACK ANY MORE
# --------------------------------------------
# It used to be. An unsuffixed zone name returned `0, "Base"`, which reads as a
# measurement and is not one, and 98 of 213 fights were published on the back of
# it. Measured across the 13 staged logs on 26 August 2026:
#
#   * A ZONE line prints "0 (Normal)" exactly 0 times, in 514 zone lines.
#     (This read 385 until 1 Sep 2026. The corpus grew and the figure was
#     re-measured to 514 in CLAUDE.md, docs/SOURCES.md, logstats.py and at
#     line 207 OF THIS FILE - four places out of five. The fifth was here.)
#   * An INVITE line prints it 16 times.
#
# So tier 0 IS named in the game - on the instance invite, never on the zone
# line. CLAUDE.md said flatly that D0 is not named and that was wrong; the true
# claim is narrower and is now recorded there.
#
# Pairing each invite with the zone line that followed it: 73 agree exactly,
# 16 are the zone line dropping a tier the invite had named, and **0 disagree**.
# The invite never contradicts the zone line, so there is no winner to choose -
# there is a gap to fill, and filling it silently with 0 was the fault.
#
# The two populations behind those 98 rows are not alike:
#
#   * The Plane of Sky, 90 fights. Every Sky invite in the corpus says 0, and
#     no Sky invite says anything else. Those rows are corroborated.
#   * Eight "- Group" fights in three zones entered at {0,2,3,4}, {0,1,2,3} and
#     {0,1,2,3,4}. A bare "The Plane of Fear - Group" cannot mean 0 when that
#     instance was entered at four different tiers. Those are unresolved, and
#     saying so is the whole point.
#
# The invite is evidence and is kept whether or not it is the field's source.

def resolve_tier(zone, invite):
    """(number, label, source, evidence) for one zone entry.

    `invite` is the instance invite immediately preceding this entry, for this
    same zone, or None. Nothing is overwritten: both readings go into the
    evidence, and `source` names the one the number came from.
    """
    ev = {}
    if zone is None:
        return None, None, "no zone line", ev

    zbase, znum, zlabel = split_tier(zone)
    if znum is not None:
        ev['zone_line'] = dict(text=zone, tier=znum, label=zlabel)
    if invite:
        ibase, inum, ilabel = split_tier(invite)
        if inum is not None:
            ev['invite_line'] = dict(text=invite, tier=inum, label=ilabel)

    zl, il = ev.get('zone_line'), ev.get('invite_line')
    if zl and il and zl['tier'] != il['tier']:
        # Never seen in the corpus. If it ever happens the zone line wins -
        # it records where the character actually stood, where the invite
        # records what was offered - but the disagreement is published rather
        # than resolved out of sight.
        return zl['tier'], zl['label'], "zone line, invite disagrees", ev
    if zl:
        return zl['tier'], zl['label'], "zone line", ev
    if il:
        return il['tier'], il['label'], "instance invite", ev

    # NEITHER LINE NAMED A TIER, so whatever comes back is an inference and is
    # labelled as one - and the label names WHICH rule produced it, because the
    # rules are not equally strong and a reader is entitled to tell them apart.

    # THE CLIENT OMITS THE INSTANCE INDEX EXACTLY WHEN IT IS ZERO.
    #
    # This file said the opposite for two days. #145 was told to "stop inferring
    # tier 0", so a bare "Zone - Group" resolved to `unresolved`; the ruling was
    # reversed on 27 Aug 2026 after Session D measured the client's behaviour,
    # and re-derived here from our own 13 staged logs before restoring it:
    #
    #   * 514 entry lines. Not one prints an index of 0.
    #   * 89 invite-to-entry pairs for the same zone: 73 match the index
    #     exactly, 16 omit it, 0 conflict.
    #   * THE FALSIFYING CASE - an index omitted for a tier above zero - occurs
    #     0 times. All 16 omissions followed an invite naming tier 0.
    #
    # So the omission is not missing information. It is how the client writes
    # zero, and a bare "- Group" is evidence OF tier 0 rather than absence of
    # evidence. Weaker than the line stating it, stronger than not knowing, and
    # the label says which.
    #
    # DELIBERATELY NOT WIDENED PAST "- Group". A second instanced family exists
    # whose entry lines carry no mode word, and at tier 0 it drops the suffix
    # entirely and is indistinguishable from an ordinary open-world zone-in.
    # " - Group" marks a line as instanced independently of the index, so the
    # absence of an index is informative there and nowhere else. The Plane of
    # Sky is that other family, which is why it falls through to the history
    # rule below rather than being caught here.
    # WHERE THIS RULE CONTRADICTS THE ZONE'S OWN HISTORY, SAY SO.
    #
    # The rule sits above the history check below because it reads THIS entry's
    # line, where the history reasons from other entries. But the two can
    # genuinely disagree: a bare "Kedge Keep - Group" in an instance every
    # recorded entry to which was tier 4. Preferring the line silently would
    # overwrite a better-informed answer with a thinner one and leave no trace,
    # which is the fault the whole provenance exercise exists to stop.
    #
    # So the line still wins - the omission is measured behaviour of the client,
    # and the history is a generalisation - but the disagreement is published in
    # the source string and the history goes into the evidence. It occurs zero
    # times today. It is written down because the sample behind this rule is
    # THREE independent events, and a rule that thin should not quietly beat
    # anything without leaving a record that it did.
    if " - Group" in zone:
        seen_g = INSTANCED.get(zbase)
        if seen_g and 0 not in seen_g:
            ev['instance_history'] = dict(tiers=sorted(seen_g),
                                          entries=INSTANCED_N[zbase])
            return 0, "Normal", (
                "bare - Group implies tier 0, instance history disagrees"), ev
        return 0, "Normal", "bare - Group implies tier 0", ev

    # What kind of inference depends on the zone. INSTANCED is built from the
    # invites the corpus actually holds, rather than from how a zone is spelled.
    seen = INSTANCED.get(zbase)
    if not seen:
        # No invite for this zone anywhere in the corpus. It is open world as
        # far as anything we hold can say, and 0 follows from the absence of an
        # instance rather than from a line naming it.
        return 0, "Base", "inferred: open world, no instance recorded", ev
    if len(seen) == 1:
        # Every recorded entry to this instance was at the same tier. That is
        # weaker than reading the line for THIS entry and stronger than a bare
        # default, so it is published with the reasoning attached rather than
        # rounded to either.
        only = next(iter(seen))
        ev['instance_history'] = dict(tiers=[only], entries=INSTANCED_N[zbase])
        return only, TIER_LABEL.get(only), (
            f"inferred: every recorded entry to this instance was tier {only}"), ev
    # Entered at more than one tier, and nothing says which one this was. This
    # is the honest answer and the one the site was not giving.
    ev['instance_history'] = dict(tiers=sorted(seen), entries=INSTANCED_N[zbase])
    return None, None, "unresolved", ev


def tier_of(zone):
    """Back-compat for callers that have only a zone string."""
    num, label, _src, _ev = resolve_tier(zone, None)
    return num, label


# WAS THIS FIGHT INSTANCED. Two of CLAUDE.md section 2's four zone shapes are:
#
#     Zone - Group            a group instance at tier 0
#     Zone - Group N (Label)  a group instance at a named tier
#     Zone N (Label)          a RAID instance at a named tier
#     Zone                    open world
#
# The third is the one `group_instance` cannot see, and it is 23 fights. A
# trailing " N (Label)" is what marks it; an open-world line carries no number.
_INSTANCED = re.compile(r'(?: - Group(?:\s|$)| \d+ \([^)]+\)$)')


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
        # A BOSS'S PET IS NOT THE BOSS, AND THE MELEE PATTERN COULD NOT TELL.
        #
        # The game writes "Terror pet bashes YOU for 15 points of damage." - the
        # owner's name, the bare word "pet", then the pet's own verb. `melee`
        # below matches the boss name and then takes the NEXT WORD as the verb,
        # so every one of those lines recorded the boss swinging with a verb
        # called "pet". Measured 4 Sep 2026: 4,573 such lines across 46 owners,
        # and `pet` duly appears in melee_verbs for 17 of 213 fights.
        #
        # It never reached a reader, because no page rendered melee_verbs. It was
        # about to: the field exists to say which class kit a boss runs, and a
        # made-up verb in that list is exactly the kind of thing that gets read
        # as evidence. Fixing it before publication rather than after is the
        # whole reason to look at a field before rendering it.
        #
        # THE PET LINES ARE NOT DISCARDED, because owning a pet is itself a class
        # tell - the same kind of evidence backstab is. They set `has_pet`.
        # Matched BEFORE `melee` below, because `melee` matches them too.
        pet=re.compile(rf'^{boss_pat(b)} pet (\w+) .+? for (\d+) points? of damage\.$'),
        melee=re.compile(rf'^{boss_pat(b)} (\w+) .+? for (\d+) points? of damage\.$'),
    ) for b in BOSSES}
    # The cheap prefilter below is a case-sensitive substring test, so it has to
    # know the same thing boss_pat does or it discards the lines before any
    # pattern sees them.
    boss_sub = {b: (b if not b[:1].islower() else b[1:]) for b in BOSSES}

    char = re.search(r'eqlog_([^_]+)_', os.path.basename(path))
    char = char.group(1) if char else "unknown"
    zone = None
    pending_invite = None      # seen, not yet attached to a zone entry
    zone_invite = None         # the invite that named the zone we are in
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
        inv = INVITE.search(b)
        if inv:
            # Held until the next zone line, then attached to it. An invite is
            # evidence about the entry that follows it, not about the zone the
            # character is standing in when it arrives.
            pending_invite = inv.group(1)
            note_invite(pending_invite)
            continue
        z = ZONE.match(b)
        if z:
            if not z.group(1).startswith(NOT_A_ZONE):
                open_fights.clear()          # zoning ends every fight in progress
                first_active.clear()
                zone = z.group(1)
                # Only where it is an invite for THIS zone. Declining an invite
                # and going somewhere else would otherwise stamp the wrong
                # instance's tier onto the zone actually entered.
                zone_invite = (pending_invite
                               if pending_invite
                               and split_tier(pending_invite)[0] == split_tier(zone)[0]
                               else None)
                pending_invite = None
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
                    boss=boss, zone=zone, zone_invite=zone_invite,
                    character=char, start=ts, damage=0,
                    healed=0, heal_count=0, casts=collections.Counter(),
                    melee_verbs=collections.Counter(), melee_hits=[],
                    pet_verbs=collections.Counter(), has_pet=False,
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
            # ORDER IS LOAD-BEARING: `melee` matches a pet line too, and would
            # record the boss swinging with a verb called "pet". See the pattern
            # definitions above.
            pv = rx['pet'].match(b)
            if pv:
                f['has_pet'] = True
                f['pet_verbs'][pv.group(1)] += 1
            else:
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
    num, label, dsrc, dev = resolve_tier(f['zone'], f.get('zone_invite'))
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
        # WHICH LINE THIS CAME FROM. A number with no provenance beside it is
        # how 98 fights came to be published as tier 0 on the strength of a
        # fallback. Both readings are kept in difficulty_evidence whether or not
        # they were the source, so nothing is chosen out of sight, and
        # difficulty is null where the logs genuinely do not say.
        "difficulty_from": dsrc,
        "difficulty_evidence": dev,
        # `group_instance` answers what its name says and nothing more: was this
        # fought in a "- Group" instance. It is NOT the answer to "was this
        # instanced", and reading it that way is wrong for 23 fights.
        #
        # CLAUDE.md section 2 gives the grammar four shapes, and two of them are
        # instanced: "Zone - Group N (Label)" AND "Zone N (Label)", the second
        # being a RAID instance. The 23 fights in "The Plane of Hate 4 (Refined)"
        # are in a numbered raid instance and record group_instance false, which
        # is correct about the group and silent about the instancing - exactly
        # the gap CLAUDE.md section 9 flags.
        #
        # So the honest field is added rather than the existing one retyped. A
        # numbered suffix is what marks a raid instance; an open-world zone line
        # carries no number at all.
        "group_instance": " - Group" in (f['zone'] or ""),
        "instanced": bool(_INSTANCED.search(f['zone'] or "")),
        "seconds": secs,
        "damage_to_kill": f['damage'],
        "self_healed": f['healed'], "self_heal_count": f['heal_count'],
        "spells": dict(sorted(f['casts'].items(), key=lambda kv: -kv[1])),
        "spells_distinct": len(f['casts']),
        # SWING COUNTS ARE NOT PUBLISHED (CLAUDE.md section 7), so what leaves
        # here is the SET of verbs. Which kit a boss runs is the fact; how many
        # times it swung is a record of somebody's play.
        "melee_verbs": dict(f['melee_verbs']),
        # Owning a pet is a class tell, so it is kept as a fact rather than
        # discarded with the lines that produced it.
        "has_pet": bool(f.get('has_pet')),
        "pet_verbs": dict(f['pet_verbs']),
        "melee_hits": len(hits),
        "melee_min": min(hits) if hits else None,
        "melee_max": max(hits) if hits else None,
    }


# How much a difficulty reading is worth, best first. A line naming the tier
# beats an inference from the zone's history, which beats an inference from the
# absence of an instance, which beats nothing at all.
# Strongest first. The order is the argument: a line stating the index beats an
# invite naming it, which beats the client's own convention of omitting a zero,
# which beats a generalisation over the corpus, which beats knowing nothing.
# "bare - Group implies tier 0" sits third because it reads THIS entry's own
# line, where the two rules below it reason about other entries instead.
SRC_RANK = ("zone line, invite disagrees", "zone line", "instance invite",
            "bare - Group implies tier 0",
            "bare - Group implies tier 0, instance history disagrees")


def src_rank(src):
    src = src or ""
    if src in SRC_RANK:
        return SRC_RANK.index(src)
    if src.startswith("inferred: every recorded entry"):
        return len(SRC_RANK)
    if src.startswith("inferred:"):
        return len(SRC_RANK) + 1
    return len(SRC_RANK) + 2          # unresolved, or no zone line


def best_src(obs):
    return min(obs, key=lambda o: src_rank(o.get('difficulty_from')))


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
            "difficulty_label": best_src(obs)['difficulty_label'],
            # THE BEST-SOURCED CLIENT DESCRIBES THE FIGHT, not the first one in
            # the list. Two characters in one group log the same kill, and one
            # may have accepted the instance invite while the other zoned in
            # without it - so one client can read the tier from a line while the
            # other can only infer it. obs[0] was whichever log was parsed first,
            # which is not a reason to prefer its provenance.
            "difficulty_from": best_src(obs)['difficulty_from'],
            "difficulty_evidence": best_src(obs)['difficulty_evidence'],
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
            # Union across clients, exactly as spells are: a swing one client
            # was out of position for still happened. The SET, never the count -
            # CLAUDE.md section 7 does not publish swing counts.
            "melee_verbs": sorted({v for o in obs for v in o['melee_verbs']}),
            # A pet seen by any client was there. See the `pet` pattern for why
            # these are not melee_verbs: until 4 Sep 2026 they were, under a
            # verb called "pet".
            "has_pet": any(o.get('has_pet') for o in obs),
            "pet_verbs": sorted({v for o in obs for v in o.get('pet_verbs', {})}),
            "instanced": obs[0]['instanced'],
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
    # TWO PASSES, AND THE ORDER IS LOAD-BEARING.
    # fmt() resolves a fight's difficulty, and one of the readings it can fall
    # back on is the set of tiers this instance has EVER been entered at, which
    # is a fact about the whole corpus. Parsing and formatting in one loop -
    # `raw += [fmt(f) for f in parse_log(path)]` - resolved log 1's fights
    # against a registry holding only log 1, so the Plane of Sky's history read
    # 5 entries where the logs hold 9, and an inference drawn from a partial
    # corpus is not the inference it claims to be. Parse everything, then
    # resolve.
    parsed = []
    for path in logs:
        parsed += list(parse_log(path))
    raw = [fmt(f) for f in parsed]
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


def selftest():
    """Prove every difficulty rule still fires, and still ranks where it should.

    WHY THIS EXISTS. Restoring the "- Group" inference on 27 Aug 2026 changed no
    published figure at all - 213 fights, an identical distribution - because
    every bare "- Group" fight in the corpus happens to carry an attached
    invite, so the branch resolves nothing today. A branch the data never
    exercises is the dead-check class this project has now found four times, and
    it does not stop being that because it is new. So it is exercised here
    directly, with the ranking, which is the part a merge silently depends on.

        python3 _build/raidstats.py --selftest
    """
    INSTANCED['The Plane of Sky'].add(0)
    INSTANCED_N['The Plane of Sky'] = 9
    INSTANCED['Zone - Group'].update({0, 2, 3})
    INSTANCED['Solo - Group'].add(4)          # a single-tier instance, never 0
    INSTANCED_N['Solo - Group'] = 3
    TIER_LABEL.setdefault(0, 'Normal')

    cases = [
        ('Zone - Group 3 (Fused)', None, 'zone line', 3),
        ('Zone - Group', 'Zone - Group 0 (Normal)', 'instance invite', 0),
        # The rule the corpus does not reach. An instanced line whose index the
        # client omitted, with no invite to fall back on.
        ('Zone - Group', None, 'bare - Group implies tier 0', 0),
        # The same rule where the zone's own history contradicts it. The line
        # still wins and the disagreement is published rather than hidden.
        ('Solo - Group', None,
         'bare - Group implies tier 0, instance history disagrees', 0),
        # Deliberately NOT caught by that rule: no mode word, so the absence of
        # an index says nothing and the history rule has to answer instead.
        ('The Plane of Sky', None, 'inferred: every recorded entry', 0),
        ('The Feerrott', None, 'inferred: open world', 0),
        (None, None, 'no zone line', None),
    ]
    bad = 0
    for zone, invite, expect, tier in cases:
        num, label, src, _ev = resolve_tier(zone, invite)
        ok = src.startswith(expect) and num == tier
        bad += not ok
        print(f"  [{'ok ' if ok else 'BAD'}] {str(zone):<26} -> D{num} via {src}")

    order = [r for r in ('zone line', 'instance invite',
                         'bare - Group implies tier 0',
                         'bare - Group implies tier 0, instance history disagrees',
                         'inferred: every recorded entry to this instance was tier 0',
                         'inferred: open world, no instance recorded',
                         'unresolved')]
    ranks = [src_rank(r) for r in order]
    if ranks != sorted(ranks) or len(set(ranks)) != len(ranks):
        print(f"  [BAD] the rules do not rank strongest-first: {ranks}")
        bad += 1

    print('\nEvery rule fired and the ranking is strictly strongest-first.'
          if not bad else f'\n{bad} case(s) failed.')
    return 1 if bad else 0


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    main(sys.argv[1] if len(sys.argv) > 1 else 'state/logs')
