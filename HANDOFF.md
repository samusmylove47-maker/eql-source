# Handoff — 15 August 2026

Read `CLAUDE.md` first. This file is the current state and the open work.

---

## The one thing to understand before you touch anything

The collaborator corrected the project's direction on 14 August and it matters
more than any task below:

> *Few people playing EQ Legends care about plot coordinates… trash monsters are
> irrelevant. Players only care about bosses, unless it's for farming
> experience… What our site needs to carry is only data that players care
> about.*

The previous session had drifted into verifying things nobody needed. The
verification grade literally measured whether plotted coordinates landed on
drawn floor, so Plane of Fear scored **zero** while holding Cazic-Thule parsed
at three difficulties.

`docs/WHAT-COUNTS.md` records the correction. Zones are now graded on
**bosses, loot, difficulty behaviour, inherited-advice marking and farming
value**, computed by `_build/coverage.py`. A zone improves by being played, not
by being edited.

**When proposing work, say who it is for.** "This helps a player pick a camp
tonight" is a reason. "This makes the data more defensible" is one too — but
only when a player would feel the difference.

---

## Open pull requests

- **#78 — Plane of Sky, measured.** Committed, pushed, awaiting merge.

## Immediate work, in the collaborator's order

1. **Kedge Keep.** Logs arriving. It is the only zone at 3/10 and the only one
   with zero measured sessions. `verify_gate` says "nothing here is ours yet"
   and that is currently accurate.

2. **Castle Mistmoore is being revamped on Tuesday 18 August.** We hold 1,008
   pre-revamp kills across 65 mob types there. **Capture the before/after** —
   nobody else in this community can make that comparison, and the window
   closes when the patch lands.

3. **Rewrite the Plane of Sky page.** `docs/SKY-MEASURED.md` has the findings.
   The page describes a full-raid zone; three attackers kill its bosses in
   under 90 seconds. This is a rewrite, not an edit. The strategy brief from the
   video transcript is sound and stays; the rest is old.

4. **Age-stamp the outgrown zones.** Najena, Splitpaw, Crushbone, The Warrens
   sit at 4/10 — fully verified under the old standard, never played with
   logging on. The collaborator's wording: *"updated as of XX/XX — any new
   information since has not been verified."* **Generate it from the last
   measured session date** so it cannot go stale by hand.

## Standing rules learned the hard way this week

- **Never publish a drop rate.** A drop seen once is seen once.
- **Read who was in the fight.** Every raid-boss kill in every log we hold is a
  public pick-up raid of 5–15 players, not our trio. `raidstats.py` records
  `attackers` and `our_damage_share_pct` for this reason.
- **Other players are never named** outside the credits. Counted, then discarded.
- **A log records what its own character witnessed.** Where the attacker count
  is thin, the damage is a floor, not a measurement.
- **Run `node scripts/toolsmoke.js` after touching anything a tool reads**, and
  `scripts/toolrender.js` before and after any data migration. A tool shipped
  dead for a day with 721 green checks because nothing ran its JavaScript.
- **Do not write regex escapes through a bash heredoc.** It ate `\b` five times.
  Use the Write tool or a file.

## Health

723 pages pass `check.py`. 17 gate self-test cases. 8 tools run under the smoke
test. Public data contract live at `/data/` with a shape guard.

Four material errors were made and corrected this week — a dead tool shipped, a
committed asset emptied on a false premise, a wrong invariant claim from a bad
regex, and a drop figure using the wrong denominator. Three were caught after
committing. Slow down at data migrations specifically.

## Logs

`state/logs/` is gitignored and holds copies through 15 Aug. The collaborator
deletes the game-side logs after each scan, so **secure and parse before
confirming**. Everything derived is committed; the raw logs are never published.
