# Plane of Sky, measured — 14–15 August 2026

**Status:** published 15 August 2026. `raids/plane-of-sky.html` was rewritten
from this, and the figures now render from `assets/sky-loot.json` rather than
from anything typed here.
**Source:** `state/logs/eqlog_Avenrae_rivervale_2026-08-15.txt`, 110,058 lines
inside the zone. The log is gitignored and the collaborator deletes it after
each scan; everything below is derived and committed.

---

## Four things this file got wrong, corrected 15 August 2026

Written from a first pass and not re-checked against the data before it was
handed on. Each error is left in place below with the correction beside it,
because deleting them would hide that a findings doc can be as wrong as a page.

1. **Thunder Spirit Princess was never killed.** It is listed under "every loop
   boss killed" below. The string appears **zero times** in the log — not
   killed, not seen, not named. It is island 1's boss and the one link in the
   key chain still unconfirmed.
2. **Six keys were measured, not five.** The table below omits **Key of the
   Swarm ×2 from The Spiroc Lord**. Six of the seven predicted drops landed,
   each from exactly the boss the chain names.
3. **Three mobs drop the efreeti line, not two.** `the Hand of Veeshan` drops
   it as well — Efreeti Mace, Magi Staff, War Staff, Wind Staff, Battle Axe and
   Golden Efreeti Vambraces. It was invisible because `raidstats.py` matched
   boss names case-sensitively and its article is lowercase.
4. **"Full per-boss drop tables are in `assets/sightings.json`" was false.**
   There were no Sky drops in that file at all. `sightings.py` joins measured
   drops to a catalogue mined from the dungeon surveys plus the planar sets,
   and Sky is neither, so **all 148 Sky loot lines across 74 distinct items
   were discarded as vendor trash**. `_build/skyloot.py` now derives them
   directly. The general fault in `sightings.py` is still open — see
   `docs/BACKLOG.md`.

---

## The headline: Sky is not a raid zone any more

The Sky pages on every reference in this community, ours included, describe a
zone that needs a full raid. **It does not.**

| Boss | Attackers seen | Damage to kill | Fight |
|---|---|---|---|
| Sister of the Spire | 3 | 10,016 | 38s |
| Noble Dojorn | 3 | 17,516 | 82s |
| Bazzt Zzzt | 3 | 26,158 | 431s |
| Bazzzazzt | 4 | 13,023 | 60s |

For scale, from the same parser: **Cazic-Thule at Refined costs 382,035** and
**Innoruuk 345,385**. A Sky boss is one to three per cent of a plane god.

41 Sky boss fights are recorded. Median attacker count **4**; minimum **2**.
Four fights had three attackers or fewer.

The collaborator states plainly that everything in the zone can be soloed and
is easy with two or three. **The log does not prove "soloed"** — the thinnest
fight we have is two attackers — but it does show three-attacker kills of the
loop bosses in under ninety seconds, which is the same practical claim. Publish
the measured figures; attribute the solo claim to the collaborator as tier C
until a one-attacker kill appears in a log.

## Every loop boss killed

~~Thunder Spirit Princess~~ (**see correction 1 — never killed**), Protector of
Sky, Gorgalosk, Keeper of Souls, The Spiroc Lord, Sister of the Spire, Eye of
Veeshan — plus **Noble Dojorn**, the **Overseer of Air** and **the Hand of
Veeshan**, the three the site's own page could not label.

## The bee island runs several named, not one

No source we hold mentions this. Killed as separate named mobs:
**Bazzt Zzzt, Bazzzazzt, Bzzazzt, Bzzzt, Bizazzzt, Bzizzzt** — six variants.
The site's island table names only Bazzt Zzzt.

## The key chain, measured

Each key dropped from the boss the tracker predicts, which is the first
independent confirmation of that chain:

| Key | Dropped by |
|---|---|
| Key of Scale | Bazzt Zzzt ×3 |
| Key of Beasts | Gorgalosk ×2 |
| Key of Misfortune | Protector of Sky ×2 |
| Avian Key | Keeper of Souls ×2 |
| Veeshan's Key | Sister of the Spire ×3 |
| Key of the Swarm | The Spiroc Lord ×2 — **omitted from the first pass, see correction 2** |

Key of Swords, island 1's, is the seventh and has no measurement either way.

## Boss loot, measured

Notable: **Noble Dojorn** drops the efreeti line — Efreeti Standard ×2, Efreeti
Wind Staff, Efreeti Battle Axe, Efreeti War Axe, Golden Efreeti Vambraces. The
**Overseer of Air** drops Efreeti War Axe ×2, Golden Efreeti Bracers, Efreeti
War Spear, Efreeti Magi Staff. **And so does the Hand of Veeshan** — Efreeti
Mace, Magi Staff, War Staff, Wind Staff, Battle Axe, Golden Efreeti Vambraces
(see correction 3). Three sources, all on the back half of the circuit. That is
direct evidence on the **Efreeti Great Staff / Efreeti Statuette source
conflict** the 14 Aug audit flagged as unresolved between us and
eqlegendstools.

Full per-boss drop tables are in `assets/sky-loot.json`, written by
`_build/skyloot.py`. They are **not** in `assets/sightings.json` and never
were — see correction 4.

## What to do with this — done 15 August 2026

1. ~~Rewrite the Sky page's difficulty framing.~~ Done. The measured cost is now
   the page's first section and its headline.
2. ~~Add the five bee-island named to the island table.~~ Done, as a table of
   all six with fights and damage to kill.
3. ~~Publish the key chain as measured rather than sourced.~~ Done, six of seven
   marked confirmed in place with the count.
4. ~~Revisit the efreeti-item conflict.~~ Published as three measured sources.
   **The conflict itself is not resolved** — we have where the gear dropped for
   us, not the full list of what drops it.
5. The strategy brief from the video transcript is sound and stays.

**Still open:** everything here is base difficulty. One logged Sky session at
Awakened would say whether the tiers change this zone at all.

## Deaths

Three, across the whole period: `Bazzzazzt`, `an essence tamer`,
`Sarkis Ebonblade`. For a zone described as a raid target, that is the point.
