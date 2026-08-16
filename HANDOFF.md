# Handoff — 15 August 2026 (evening)

Read `CLAUDE.md` first. This file is the current state and the open work.

---

## The one thing to understand before you touch anything

The collaborator corrected the project's direction on 14 August and it matters
more than any task below:

> *Few people playing EQ Legends care about plot coordinates… trash monsters are
> irrelevant. Players only care about bosses, unless it's for farming
> experience… What our site needs to carry is only data that players care
> about.*

`docs/WHAT-COUNTS.md` records the correction. Zones are graded on **bosses,
loot, difficulty behaviour, inherited-advice marking and farming value**,
computed by `_build/coverage.py`. A zone improves by being played, not edited.

**When proposing work, say who it is for.**

---

## Open pull requests

- **Plane of Sky, rewritten.** Branch `feat/sky-rewrite-measured`. Pushed,
  awaiting review and merge.

## What that branch did, and the one thing to check first

`raids/plane-of-sky.html` said the zone needs a full raid. It does not, and the
page now leads with the measurement: 43 fights, 15 bosses, median 4 attackers,
biggest boss 26,158 damage against Cazic-Thule's 382,035.

**Check this before anything else:** the branch also changed
`_build/raidstats.py`, which **moves published figures in Plane of Fear**.
The parser matched boss names case-sensitively, so a name whose article is
lowercase lost its slain line and the fight never closed. `a dracoliche` was
published at **1,287** damage at Adaptive and **14,483** at Fused. It is
actually **85,671** and **285,202**, plus a Refined kill at **362,687** we held
no record of at all. Same fault hid `the Hand of Veeshan` entirely. Both are in
the change log as a Correction. If you disagree with that call, it is one commit
to revert — but the old figures are wrong.

## Immediate work, in the collaborator's order

1. **Castle Mistmoore is revamped on Tuesday 18 August.** Three days. We hold
   1,008 pre-revamp kills across 65 mob types. The "before" data is already
   parsed and committed; **what is missing is a frozen, labelled baseline** an
   after-patch parse can be diffed against rather than silently averaged into.
   Do that before Tuesday. More pre-patch play is the collaborator's call, not
   ours.

2. **Kedge Keep.** Still blocked, and the previous handoff was optimistic:
   **no Kedge logs have arrived.** The newest log
   (`eqlog_Avenrae_rivervale_2026-08-15.txt`, scanned this morning) has no Kedge
   or Siren zone line anywhere in it, and `measured.json`'s latest session is
   14 August. It remains the only zone at 3/10 with zero measured sessions.

3. **Age-stamp the outgrown zones.** Najena, Splitpaw, Crushbone, The Warrens at
   4/10 — fully verified under the old standard, never played with logging on.
   Wording: *"updated as of XX/XX — any new information since has not been
   verified."* **Generate it from the last measured session date** so it cannot
   go stale by hand.

4. **`sightings.py` is losing evidence.** Now `docs/BACKLOG.md` P0, with
   acceptance criteria. It discards every measured drop whose item is not in a
   catalogue mined from the dungeon surveys plus the planar sets, so **all 148
   Plane of Sky loot lines were thrown away** and `sightings.json` held no Sky
   drop at all. `_build/skyloot.py` works around it for Sky only; every other
   unsurveyed zone is still losing drops silently. This is a migration across a
   dataset five builders and the public contract read — run
   `scripts/toolrender.js` before and after.

## Standing rules learned the hard way

- **Never publish a drop rate.** A drop seen once is seen once.
- **Read who was in the fight.** Every raid-boss kill in every log we hold is a
  public pick-up raid, not our trio.
- **Other players are never named** outside the credits. Counted, then discarded.
- **A log records what its own character witnessed.** Where the attacker count
  is thin, the damage is a floor, not a measurement.
- **Never let a hand-typed sentence sit beside a generated figure.** Two
  retractions came from that. The Sky page renders every figure from
  `assets/sky-loot.json`.
- **A findings doc can be as wrong as a page.** `docs/SKY-MEASURED.md` carried
  four errors into this session — a boss listed as killed that appears **zero**
  times in the log, a missing key drop, a missing efreeti source, and a pointer
  to drop tables that were not in the file it named. All four are corrected in
  place rather than deleted. Re-check a findings doc against the data before
  building on it.
- **Run `node scripts/toolsmoke.js`** after touching anything a tool reads, and
  `scripts/toolrender.js` before and after any data migration.
- **Do not write regex escapes through a bash heredoc.** Use the Write tool.

## Health

723 pages pass `check.py`. **19** gate self-test cases, up from 17. 8 tools run
under the smoke test. Public data contract live at `/data/`.

**Two new gate cases, because this one nearly shipped.** The withdrawn `build4.py`'s `BODY` was
a plain triple-quoted string — it carries the 3D engine's JavaScript, so it can
never be an f-string — and f-string syntax written into it renders as itself.
`raids/eye-of-veeshan.html` published the literal text `{EYE_FULL:,}` in its
stat block **and passed all 723 checks**, because every check reads what a page
says and none asked whether it had finished rendering. `gate.py` check 5d now
refuses both `{...}` and `@@TOKEN@@` leaks, and the self-test proves it for each.
Caught by opening the page, which remains the only way.

## Logs

`state/logs/` is gitignored and holds copies through 15 Aug. The collaborator
deletes the game-side logs after each scan, so **secure and parse before
confirming**. Everything derived is committed; the raw logs are never published.
