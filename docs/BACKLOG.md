# Backlog

Ordered by value per unit of effort. Each item has acceptance criteria, because
"done" needs to mean something specific.

**Rule for all of it:** if a task needs a number we do not have, the answer is to
flag the gap, not to invent the number.

---

## P0 — Aesthetic uplift

See `docs/DESIGN.md` for the full brief. Break it into these commits:

1. **Hero and atmosphere layer** — one atmospheric device, hero restructured.
2. **Commitments and tier scale** — asymmetric layout, the scale reading as a
   scale.
3. **Tools band** — hero card for The Index, three supporting.
4. **Raids band** — full-bleed ember treatment.
5. **Dungeons and gaps** — spectrum-led, gaps understated.
6. **Motion pass** — staggered reveals, hover states, reduced-motion respected.
7. **Interior pages** — the same rhythm applied to `tools/index.html`,
   `raids/index.html`, `dungeons/index.html`, `sources.html`.

**Acceptance:** `check.py` passes; zero horizontal overflow at 390px; screenshots
before and after at both widths; the four verification questions at the end of
`docs/DESIGN.md` answered in writing.

---

## P1 — Difficulty primer

**Why:** D4 behaviour is the biggest documented gap on the site, and our raid
guides currently say "nobody has published this". That is no longer entirely
true — https://eqltools.com/learn/difficulty has measured figures.

**Build:** a new page `learn/difficulty.html`, and a `learn/` section.

What is known and citable:
- Difficulty does not raise mob levels. It scales HP, damage, resists, AC, mana,
  movement speed and aggro radius, roughly linearly per tier.
- Measured HP multipliers, D1 and D2: ×1.15 / ×1.30 multiplayer tuning,
  ×1.10 / ×1.20 solo. **D3 and D4 run well above these and are not pinned.**
- XP multipliers: ×1.15 / ×1.30 / ×1.45 / ×1.60 multiplayer,
  ×1.10 / ×1.20 / ×1.30 / ×1.40 solo.
- Multiclass frequency rises with tier. Named often multiclass from D2, raid
  bosses triple-class from D3. **Which kits attach to which boss is unpublished.**
- Loot table is identical at every tier; what changes is the upgrade level on
  arrival. A +4 item is worth 16 base copies of upgrade progress. **Player-derived,
  no dev statement.**
- Each difficulty is its own weekly loot-lockout track.

**Sourcing discipline:** these are another site's measurements, not ours. Cite
EQL Tools by name with a link, badge the derived claims `T3`, and badge anything
they mark as player consensus `T4`. Do not restate their numbers as if we
measured them. Where they say something is unpinned, we say it is unpinned.

**Acceptance:** page live; every claim badged or plain per the tier rules; the
raid pages link to it; `sources.html` gap for D4 rewritten to say what is now
known and what is still open.

---

## P2 — Faction Impact Checker

**Why:** nobody has built one, it is a real and constant EverQuest problem, and
we already hold the faction data from the race-unlock work.

**Build:** `tools/faction-impact.html`. Input: a zone, or a mob type, or a
planned grind. Output: which factions rise, which fall, and — the valuable part —
**which race unlocks or quest lines that damages.**

The data exists in `_build/source/eql-race-unlocks.html` (`STEPS` and `RACES`
objects). It needs extracting to `assets/faction-data.json` the same way
`_build/extract.py` mines the plates.

**Acceptance:** answers "I am about to farm Deathfist orcs for 2000 kills — what
does that cost me?" with named factions and named consequences. Shares the URL
state pattern used by the other tools.

---

## P2.5 — Raid access and instance types primer

**Status: writable today, entirely tier 1.** Researched 8 Aug 2026.

Open-world raid bosses no longer spawn in EverQuest Legends. Raid instances are
created by NPCs called **voidlings** — hail one for a list of raid options with
lockout timers. There are three distinct instance types and they are easy to
confuse: **public**, **personal** (zone-level, 2 charges, 1 per hour), and
**raid** (voidling-created). Raids cap at 8 players, groups at 4, and D0–D4 is
selectable in raid instances.

**The misconception worth correcting:** a personal instance is *not* a solo raid.
Someone entering a personal instance of Plane of Hate expecting Innoruuk will
find an empty zone and will have spent a charge doing it.

Sourced: patch note 16 Jun 2026 confirms *"Personal instances for Plane of Hate
and Plane of Fear are now available!"* and *"Balance changes to Solo Raid
versions of Innoruuk, Cazic-Thule, Maestro of Rancor, and Lord of Loathing"* —
so solo raid versions demonstrably exist. `eqlwiki.com/Personal_Instance`
(4 Jul 2026) documents the mechanism.

**Unresolved, do not publish either side:** a 6 May 2026 dev stream reported solo
and multiplayer raid lockouts are decoupled; current community summaries describe
a shared Tuesday-resetting weekly lockout. The patch notes do not settle it.

---

## P3 — More raid encounters

Order set by which fights a diagram actually helps with:

1. **The Spiroc Lord** (Island 5) — vanquisher squad-respawn logic determines
   kill order and is nearly impossible to hold in your head from prose.
2. **Bazzt Zzzt** (Island 6) — the bee split tree is a decision graph.
3. **Sister of the Spire** (Island 7).

Copy `_build/build4.py`. The 3D engine is self-contained in it. **Every model
must state in place whether it is surveyed from `/loc` data or schematic.**

### Sourcing verdict, 8 Aug 2026 — read before writing any of these

**Plane of Sky: YES, with hard limits.** On 19 July 2026 editor *Sadres* made a
deliberate de-classicing pass on `eqlwiki.com/Plane_of_Sky`, summarised as
"Cut out large swaths of the raid strategy fluff from classic... replaced it with
my own experiences on EQLegends Beta". The page lost 28% of its bytes. Islands
3–7 have surviving Legends-authored strategy prose. Route, spawn logic and phase
structure are writable, **badged T3**, attributed to Sadres and dated, reinforced
by the 16 Jun patch note that restructured Sky spawns.

**Do not publish any boss HP, AC, level or damage figure.** The only ones
available come from pages created in 2025, before the game existed. Confirmed
Legends facts worth having: keys now bind permanently to the keyring, and **boss
NPCs no longer have a death touch**.

**Plane of Hate: NO. Plane of Fear: NO.** Both zones are implemented and solo
raid versions of their bosses demonstrably exist — but *nobody has written down
what happens inside them*. The Hate zone page's only 2026 strategy edit deleted a
heading and substituted nothing. Every boss page predates the game: Cazic Thule's
450,000 HP and "several dozen melee and a dozen healers" is classic EverQuest,
unaltered. A guide written today would be classic tactics wearing a Legends
banner — precisely what this project exists to prevent.

**What unblocks Hate and Fear:** one person entering a voidling solo raid
instance at a stated difficulty and recording what the boss actually does —
ability names, whether it runs multiclass kits, roughly how long it survives.
That is a few hours of play. Searching harder will not produce it, because it has
not been written down by anyone yet.

---

## P4 — Five missing navigation maps

Crushbone, Befallen, Blackburrow, The Hole, The Warrens have plates but no map.
Blackburrow first: it has an explicit three-floor structure, which makes it the
strongest candidate for a 3D treatment rather than a flat plan.

---

## P5 — Close the verification gates

Five plates are short of the full three-gate standard. `verify_gate` in
`assets/zones-index.json` names the open gate for each. Use `/verify <zone>`.

Do not upgrade a `verify_level` without doing all three gates. `check.py` will
catch a count that outruns the data, but it cannot catch a lie in the field
itself.

---

## Deliberately not doing

**Do not clone EQL Tools.** Their layer is client-mined numbers, log parsing and
3D zone geometry: Log Parser, Gotta Kill 'Em All, Gear Upgrade Finder,
Spellmaster, Zone Atlas, AA Planner, Starting Attributes, the Learn primers. All
need a data pipeline we do not have. Shipping worse copies would waste our effort
and make the community worse off.

**Our layer is quests, factions, routes and tactics** — the human-knowledge
layer. That is where every new tool should sit. When a player needs something we
deliberately do not build, link to whoever does it well.
