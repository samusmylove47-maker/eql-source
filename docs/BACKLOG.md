# Backlog

Ordered by value per unit of effort. Each item has acceptance criteria, because
"done" needs to mean something specific.

**Rule for all of it:** if a task needs a number we do not have, the answer is to
flag the gap, not to invent the number.

---

## P0 — `sightings.py` is discarding every drop from an unsurveyed zone

**Found 15 August 2026, while rewriting the Plane of Sky page.**

`sightings.py` keeps a measured drop only where the item matches a catalogue
mined from the dungeon surveys plus `planar.json`. **The Plane of Sky is
neither**, so all **148 Sky loot lines across 74 distinct items** — the whole
key chain, the whole efreeti line — were discarded as vendor trash, and
`assets/sightings.json` contained not one Sky drop. `docs/SKY-MEASURED.md` said
the per-boss drop tables were in that file. They were never in it.

This is the same fault the file already documents and fixed **on the mob side**
in August: measured evidence could only ever confirm what we had already typed,
never add to it. It was fixed for mobs and left standing for items.

`_build/skyloot.py` works around it for Sky only. Every other zone we have not
surveyed is still losing its drops silently, and **a generator that discards
evidence without counting what it discarded looks exactly like one that found
nothing**.

**Acceptance:**

- `sightings.py` reports how many drops it discarded and from which zones, so
  the loss is visible in the build output rather than inferred a month later.
- An item dropped by a named mob is kept even where no catalogue lists it,
  marked so a page can say the name came from the log — mirroring `off_roster`
  on the mob side.
- Vendor trash stays excluded. That filter is doing real work and removing it
  wholesale would bury the signal.
- `scripts/toolrender.js` run before and after, and diffed: `sightings.json`
  feeds five builders and the public data contract, so this is a migration and
  the handoff's "slow down at data migrations" applies.
- `_build/skyloot.py` reassessed once this lands — it may become redundant.

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

## P1 — Difficulty primer  — BUILT 8 Aug 2026

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

## P1.5 - The Level 11 Lock: a deity and permanent-choice guide

**Proposed 8 Aug 2026 after surveying the sibling sites. Needs the owner's
approval before building - it is a new section, not an extension.**

**Why this one.** Primary class and race lock permanently at level 11. The site
already ships a race-and-primary calculator for two legs of that decision. Deity
is the third, and it is the largest genuinely uncovered decision in the game.

What the rest of the ecosystem has:

| Source | Deity coverage |
|---|---|
| eqlwiki `Deity` | **A redirect stub. No text at all.** |
| eqlwiki `Category:Deity` | 17 names, "There is currently no text in this page" |
| eqlwiki `Starting_Faction_Standings` | Carries its own cleanup banner admitting inaccuracies specific to Legends; TBA across Rivervale, Kelethin, Kaladim |
| eqlbase `/deities/` | Alignment and compatibility cards. No faction effects, no quests, no dates |
| eqltools, eqlegendstools | Nothing |

**The advice that exists is incomplete rather than contradictory — checked
8 Aug 2026, and the earlier framing of this entry was wrong.** Both sources were
read in full:

- eqlwiki Newbie Guide, last edited 7 Aug 2026 14:31, carries a WIP banner:
  *"If your class allows, choosing Agnostic is always a safe bet."*
- everquestguides.com New Player FAQ, 3 Jul 2026, updated 24 Jul 2026:
  *"It dodges the enemies a deity makes and locks you out of every
  deity-specific item and faction perk."*

This entry previously said "both cannot be right". **They can.** The first is a
claim about risk; the second names a benefit *and* a cost in the same sentence.
Nothing in the second says agnostic is unsafe — it says it is safe and that the
safety is paid for. Writing them up as a contradiction would have published a
false claim about two sources that agree.

The real editorial point is better than the invented one: **the wiki gives
advice with the cost omitted, on a choice that locks permanently at level 11.**
"Always a safe bet" is true and incomplete, and incomplete is what matters when
the decision cannot be taken back. That is worth saying, with both quotes and
both dates, and without pretending anyone is wrong.

Two things the FAQ supplies that the wiki does not:
- It corroborates the token: *"the devs have confirmed a Deity Token that
  changes it afterward"*, which matches the Producer's Letter price below.
- *"The best-value picks players land on are Bristlebane and Solusek Ro."*
  Explicitly player consensus, single source — **T4, badge it**.

**The fact almost nobody publishes:** the lock is reversible. The official
Producer's Letter (8 Jul 2026, everquestlegends.com) prices a Deity Unlock Token
at 500 IR, Race at 1,000, Class at 1,500. That is tier 1 and it changes the
decision materially.

**Build:** extend the existing calculator rather than starting a codebase. Same
URL-state pattern. Data is eqlwiki starting faction standings (T2, holes and all
- naming the TBA holes is a feature here), deity quest lists (T2), token prices
(T1). No mined data required.

**Acceptance:** the page quotes both published positions on agnostic with their
dates, and states accurately how they relate — the wiki's advice omits a cost the
FAQ names, which is not the same as the two disagreeing. It does not manufacture
a contradiction, and does not pretend to resolve what the evidence cannot. The
Bristlebane and Solusek Ro "best value" ranking is explicitly player consensus
from a single source and must be badged T4.

---

## P2 - Faction Impact Checker  — BUILT 8 Aug 2026

**Why:** nobody has built one, it is a real and constant EverQuest problem, and
we already hold the faction data from the race-unlock work.

**Built.** `tools/faction-impact.html`, from `_build/extract_faction.py` and
`_build/build10.py`. Search across 65 factions, 25 quest steps and 16 races.

What the entry did not anticipate: the movement half is **measured from our own
combat logs**, not read, so it covers only zones we have played — one so far.
Coverage is stated at the top and every uncovered zone is named, because a
faction tool that stays silent about a zone reads as "this zone is safe".

Also: checking only the factions a race *requires* finds almost nothing. The
steps that unlock a race move far more factions than the race lists, and a
step's side gain costs as much to undo as a requirement. Both are traced.

The data exists in `_build/source/eql-race-unlocks.html` (`STEPS` and `RACES`
objects). It needs extracting to `assets/faction-data.json` the same way
`_build/extract.py` mines the plates.

**Acceptance:** answers "I am about to farm Deathfist orcs for 2000 kills — what
does that cost me?" with named factions and named consequences. Shares the URL
state pattern used by the other tools.

**Confirmed uncontested, 8 Aug 2026.** eqltools has no faction content. Neither
does eqlegendstools. eqlbase's faction pages carry three columns - members,
raised by killing, lowered by killing - raw counts with no quest requirements, no
gated unlocks, no reverse lookup. eqlwiki has 258 faction pages but organised
faction-first: faction to its mobs, not mob to its consequences. Its Crushbone
page warns that killing slaves hurts their home city, and never says which race
unlock that damages.

**Nobody joins the chain mob -> faction -> consequence.** That join is human
knowledge rather than mined data, and it is already written out in prose inside
`_build/source/eql-race-unlocks.html` - thresholds, the +5 maximum gain mechanic,
the kobold and Deepwater Knights conflict, the cross-race collisions. The hard
part is done; what remains is extraction and interface.

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

## ~~P4 — Five missing navigation maps~~ · struck 10 Aug 2026

Superseded. `_build/geometry.py` reads the floor plans from the game's own
meshes and covers all ten zones, so the five it named have had a map since the
plates were retired. What the plans lack now is room names, which is a different
piece of work and is recorded as a gap on Accuracy rather than a backlog item.

---

## ~~P5 — Close the verification gates~~ · struck 10 Aug 2026

Done. All ten cleared all three gates on 9 Aug 2026 and `verify_gate` in
`assets/zones-index.json` records the evidence for each. Gate 3 was rewritten
that day — it had asked for a collision check against a room list that does not
exist, and now asks that every coordinate land within 120 units of drawn floor.
`docs/SOURCES.md` carries the reasoning and what the new gate is weaker at.

Still true, and worth keeping in view: do not upgrade a `verify_level` without
doing the work, and "verified" means checked against source, not finished.

---

## P4.5 - Inventory import for the Sky tracker

**Proposed 8 Aug 2026.** eqlegendstools accepts a plain-text inventory export and
auto-ticks Plane of Sky quest progress from it. Our tracker makes the player tick
by hand across 560 trios.

**This is not a data pipeline and does not breach the exclusion below.** The file
is supplied by the player from their own client. It needs no item database, only
matching against the turn-in names our 95-quest tracker already lists. Nothing is
uploaded anywhere; the parse happens in the browser like everything else here.

Worth copying honestly: their implementation warns that Wind Runes live in the
currency tab and will not appear in the export. Ours should say the same. Record
it in the change log as an idea taken from a sibling site rather than an original.

---

## P5 - The =logo family, and settling the sibling tool names

**Recorded 18 Aug 2026, not started. `docs/DESIGN.md`'s call, with the owner.**

The product is **EQLS Auras**, which reads aloud as "Equals Auras". That is not
an abbreviation that happened to fit; it is the anchor for a planned logo family
written as **=Auras**, **=50Upgrades**, **=SkyLedger**.

Which means the decision is larger than one heading. It touches the site
wordmark and the names of two tools that already ship under other names — the
50 Upgrades description page and the Sky Ledger. Renaming either is a change to
a published page's title, its `og:title`, its share card under
`public/assets/og/`, and every footer that links it, so it is not a CSS job with
a naming side effect.

**Do not begin any of it from a heading change.** `DESIGN.md` is binding for
design work and this is design work: the mark comes first, the tool names follow
it, and the home page follows them. Whoever picks this up should read
`docs/DESIGN.md` and get the owner's decision on the mark before touching a
single generator.

The one thing already settled: **the band heading is "EQLS Auras" and stays
there** until the family lands. `_build/build1.py` carries the reasoning above
the band so a tidying pass cannot expand it back.

**What the mark means, set by the owner 18 Aug 2026.** The canonical reading of
`=` is **"this is measured"**. That is not decoration attached afterwards; it is
the same proposition the site already leads with, and the home page headline
states it in words: *Norrath, measured.*

Which makes the mark and the headline one idea in two forms, and it sets the
order of work when the family lands. **The masthead tagline — `Survey` in
`site.config.json` — is the third thing to reconsider**, and deliberately not
the first. The hero eyebrow was cut on 18 August for saying the same thing a
third time; once the mark exists, the tagline becomes the only element still
competing with it.

It is last for a practical reason as well as an editorial one: the tagline
renders on all 716 pages through `_partials.py`, so changing it re-renders the
whole site. That is a decision to take once, with the mark settled and the tool
names settled, rather than a string to adjust while the family is still being
drawn.

---

## P5 - The home page's prose ceiling is coupled to the change log

**Recorded 18 Aug 2026, not started. Nobody designed this and it will bite again.**

`index.html` renders `ENTRIES[:4]` from `_build/changelog.py`, and those four
entries are counted by `page_words` like any other prose. So **writing a verbose
correction silently spends the front page's headroom**, and the page that trips
its ceiling is whichever one happens to be nearest it rather than the one that
grew.

It has already happened. Two change-log entries landed on 18 August and moved
`index.html` from 649 to 657 with nothing on the home page having been written
or edited. A session then planned a band against 649, and the arithmetic was
wrong before it started.

That is the same shape as the fault `page_words` already strips `<svg>` labels
and ledger rows to avoid — a ceiling that bites on recording rather than on
writing — but it is **not** simply another `LEDGERS` entry, and it should not be
fixed by adding one without thought. `ENTRIES[:4]` is a rolling window, not an
append-only list: it does not grow without bound, it *fluctuates* with the
length of whatever was written most recently. Exempting it outright would stop
the home page's own prose being governed at all, because the four entries are a
large share of the page.

Options worth weighing, none chosen:

- exempt the four rendered entries the way ledger rows are exempt, and accept
  that the rest of the home page is what the ceiling then governs;
- render a fixed-length summary on the home page rather than entry bodies, so
  the window's weight cannot vary;
- leave it and document it, so the next session budgeting the home page knows
  to measure rather than to trust a number written down earlier.

The third is what is in place today, via the derivation table in `HANDOFF.md`.
It is the weakest of the three and it is honest about being weak.

---

## Deliberately not doing

**Do not clone EQL Tools.** Their layer is client-mined numbers, log parsing and
3D zone geometry: Log Parser, Gotta Kill 'Em All, Gear Upgrade Finder,
Spellmaster, Zone Atlas, AA Planner, Starting Attributes, the Learn primers. All
need a data pipeline we do not have. Shipping worse copies would waste our effort
and make the community worse off.

**The same exclusion now covers eqlbase.com**, found 8 Aug 2026 - a second mined
database: 2,038 spells, 568 zones, a bestiary with loot tables and faction
affiliations, and a Build Planner. Self-described "VERY early alpha", so any
figure taken from it needs a snapshot date.

**Do not enter these either**, each surveyed 8 Aug 2026 and each already served
well:

- **Items, weapons, procs, focus effects, clickies, worn effects, exaltations** -
  eqlegendstools.com owns this thoroughly. Version 4.6.7, audited bi-weekly, 43
  items changed in the week to 6 Aug, three-class filtering throughout, and item
  comparison. Link to it.
- **Travel, ports, boats, bind points** - eqlwiki's Travel Guide is strong and
  genuinely Legends-aware. The one thing worth publishing is our own druid and
  wizard port-level contradiction, as a sourced correction rather than a tool.
- **Levelling routes** - everquestguides.com's 1-50 guide is Legends-native and
  already warns that grinding frogs costs the Froglok unlock.
- **Class epic quests** - eqlwiki's list admits its walkthroughs are "1.0 from
  allakhazam", which is tempting under our rules, but it is a very large content
  project against an incumbent that at least has text on the page.

**Our layer is quests, factions, routes and tactics** — the human-knowledge
layer. That is where every new tool should sit. When a player needs something we
deliberately do not build, link to whoever does it well.
