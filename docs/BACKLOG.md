# Backlog

Ordered by value per unit of effort. Each item has acceptance criteria, because
"done" needs to mean something specific.

**Rule for all of it:** if a task needs a number we do not have, the answer is to
flag the gap, not to invent the number.

---

## Recovered from the exchange, 1 Sep 2026

Five findings that existed only inside `HANDOFF.md`'s "To the Director" section
and would have been lost when it was pruned. Each is real, each was verified
against the tree on the day, and none has an owner yet.

**`assets/gap-engine.json` has no upstream identity.** Nothing checks that the
vendored fixture still matches what it was vendored from, and the file carries no
sha to compare against — its metadata keys are `_fixture`, `_why`, `_never` and
`_regenerate`, and none of them names an upstream. Contrast the served apps,
which `scripts/check.py` verifies byte-for-byte against a recorded hash for
exactly this reason. *Acceptance: an upstream sha recorded in the vendored file's
own metadata, and a check that compares it.*

**Teach `logstats.py` to read the instance invite.** `raidstats.py` reads it and
`logstats.py` does not, so 61 of its 172 sessions rest on something other than a
numbered zone line — 50 unsuffixed, 10 loot-tier, 1 with nothing at all. This was
called the highest-value follow-up available and was held back because it moves
`measured.json` and the public `sightings` contract. *Acceptance: the 61 resolve
or are stated as unresolved with a reason, and the published contract is versioned
rather than changed in place.*

**`check.py`'s own assertions are almost entirely unexercised.** A coverage pass
found 22 of 106 assertions proven alive — `gate.py` 19 of 42, `check.py` 3 of 64 —
and every one of `gate.py`'s seven unreachable `warn(` calls has the same shape:
"X is missing, so Y is unchecked". `gate_selftest.py` records the blind spot and
the seven, not the coverage. *Acceptance: the figure regenerates from a command
rather than being typed here, per HANDOFF.md's own rule.*

**`melee_verbs` is measured and rendered nowhere.** `raidstats.py` parses and
stores it; no page reads it. The boss table on `learn/difficulty.html` has a
Spells column and no melee column, so every backstabbing raid boss in the corpus
reads there as a caster — including Phinigel Autropos, whose three kits are now
recorded in CLAUDE.md section 9. *Acceptance: either published, or moved to the
"do not build" table with a reason. An unread field with no note beside it is what
a later session deletes as dead.*

**A correction can sit merged on `main` and unserved to readers indefinitely.**
It happened for weeks once, and nothing in the toolchain watches for it.
`scripts/freshness.py` does not cover this: it compares committed output against a
fresh build, not the tree against the live site. *Acceptance: a command that
fingerprints a live page against the same page on `main`. Lower priority — the
deploy path is now understood and documented in CLAUDE.md.*

---

## A display heading exceeds its 16ch measure on five pages — a design question

**Reported by the content-vs-box probe in `scripts/conformance.js`, and left open
deliberately rather than tuned out of the report.** Ten findings, desktop only,
on `named/cauldronbubble`, `named/the-thaumaturgist`, `named/arisen-thaumaturgist`
and two item pages. `CAULDRONBUBBLE` needs 799px in the 713px box that
`h1.display{max-width:16ch}` gives it.

**Measured, and nothing is lost:** at 1440 the heading's ink stops at 932px while
its shell runs to 1333, so no text leaves the page and nothing sits in the
overhang. `16ch` is a measure for line length, not a boundary, and a single
unbreakable word cannot honour it.

The mobile half of this WAS a defect and is fixed: at 390px the same heading
painted to 407px against a 390px viewport with `document.scrollWidth` still
reading 390, so 17px of the name was off-screen and unreachable — the layout
clipped instead of scrolling, which is the one shape the old document-level
check could not report. `h1.display{overflow-wrap:anywhere}` now applies under
760px only.

*Acceptance: either the desktop cap is relaxed for single-word headings, or the
finding is accepted as a measure being exceeded harmlessly and the probe learns
to say so. `docs/DESIGN.md` is binding — this is a typographic decision and not
a bug to be silenced. Do not simply raise the probe's threshold past it: 86px is
far above every real fault it has found.*

## `coverage.py` reads a file that `build.sh` writes forty-nine lines later

**Found 4 September 2026, by `freshness.py`, after the sightings change moved a
dataset far enough to make it visible.**

    build.sh:33   extract.py      writes index-data.json
    build.sh:37   coverage.py     READS sightings.json, writes coverage.json
    build.sh:41   build1.py       reads coverage.json
    build.sh:73   planardata.py   writes planar.json
    build.sh:86   sightings.py    READS planar.json, WRITES sightings.json

**So `coverage.json` is always computed from the PREVIOUS build's sightings, and
the plate cards `build1.py` prints it on are one build behind.** Invisible while
`sightings.json` is stable, which it normally is. When it moved on 4 Sep the
error was not small: *"40 items recorded dropping here"* against a true 86, 28
against 43, 33 against 45, 41 against 99 — eleven zones, every one understated.

**It is NOT a simple reorder, which is why it is filed rather than fixed.**
`coverage` cannot move later because `build1` reads it at 41; `sightings` cannot
move earlier because it reads `planar.json`, written at 73. The chain
`extract → planardata → sightings → coverage → build1` is not the order
`build.sh` runs, and straightening it means moving `planardata` too and
re-deriving what IT depends on.

**A single build is not a fixed point on this tree.** Two consecutive builds
after the change were identical, so the state is reachable — it just takes two.
`freshness.py` rebuilds ONCE, so it correctly fails a tree committed after one.

*Acceptance: `build.sh` ordered so one build is a fixed point, with the
dependency stated in comments at each moved line; or a documented second pass
with `freshness.py` taught to expect it. Do not fix it by committing a
twice-built tree and calling the order correct.*

## P0 — `sightings.py` is discarding every drop from an unsurveyed zone

> **CLOSED 4 SEPTEMBER 2026, AND THE SKY HALF CLOSED BY A JOIN RATHER THAN BY
> NEW DATA — WHICH IS NOT WHAT THIS SESSION FIRST CONCLUDED.**
>
> Two faults, one on each side of the same join. **The item side** discarded a
> drop whose item was not in our catalogue, so measured evidence could only
> confirm the catalogue and never extend it — 452 pairs covering 930 drops from
> mobs our roster names, now kept and marked `off_catalogue`. **The mob side**
> had no roster for any zone that is not a surveyed dungeon, which is why Sky
> failed both tests at once.
>
> **I reported that Sky needed new data. It did not.** The Director pointed at
> `assets/raids-measured.json` — already in this repo, already read by two
> generators — and asked whether its bosses match the mob names on the excluded
> drops. Measured: **15 of 15 Sky bosses match, 0 roster names unused, 382 of the
> 543 excluded Sky drops theirs.** So the raid bosses are admitted as a second
> roster, exactly as `planar.json` is a second catalogue.
>
>     pairs 704 -> 1,521    items 308 -> 762    mobs 255 -> 291
>     excluded 5,360 -> 3,895      Sky discards 543 -> 161
>     pairs carrying a Sky session: 0 -> 266, all 15 bosses present
>
> **27 of 36 raid bosses were on no survey roster**, so this also recovers
> Innoruuk's court — the case `sightings.py`'s own mob-side comment says was
> "discarded on the way past". Every one of the 1,156 previously-kept pairs
> survives; 0 lost.
>
> **What remains excluded is what should be.** 161 Sky drops from 25 unnamed
> trash mobs — An essence carrier, An azarack, A heartsbane drake — which is the
> vendor-trash case the exclusion exists for.
>
> **`_build/skyloot.py` can now be re-derived against real data.** Its docstring
> says "the general fix belongs in sightings.py"; that is done. It is NOT
> retired here — it should be re-derived against the recovered drops and
> withdrawn only if it agrees, which is a separate change with its own diff.
>
> *Remaining acceptance: skyloot.py re-derived against the recovered Sky drops
> and withdrawn or kept on the evidence.*


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

## The decorative alphabet: two of five shipped, three dropped for good

Ruled 20 Aug 2026, after the two-theme atlas landed. The brief named five marks —
dividers, compass rose, scale bar, lantern, hachures. **Two have a home and three
should not exist here.** Written down because a session arriving with energy and
no context will build all five enthusiastically.

**Shipped.** The **lantern**, on the theme switch and nowhere else. The
**divider**, in the footer only, in flow. The masthead half is unbuilt: the bar's
free space collapses to nothing between roughly 760px and 1040px, above the
700px escape hatch and a width nothing in the repo tests.

**Do not build the compass rose.** Two reasons and the second is the one that
settles it. All thirteen surveys already draw a north arrow from the mesh
(`_build/build6.py`), so a decorative rose is the *second* compass on the page
and a reader cannot tell which one is the measurement. And this site publishes,
live at `learn/reading-the-plans.html`: *"An image model will draw a convincing
dungeon map, with a legend and a scale bar and a compass rose, and every spatial
relationship in it will be invented."* **Two of the five marks are named there as
the tells of a fabrication.** Shipping house versions of both while that sentence
stands is a contradiction a reader finds in one search.

**Do not build the scale bar.** The floor plans already carry one, measured,
labelled in game units at full opacity (`_build/build6.py`). A faded ornamental
twin beside a real instrument is worse than none. On a plate card it is worse
still: the card art is letterboxed and path-capped, so its units-per-pixel is
unknowable — a bar there asserts a scale it cannot state.

**Do not build hachures.** The objection is semantic, so no placement fixes it.
**Hachures encode slope**, and using them as a storey separator asserts a
gradient nobody measured — on a site whose rule is that a drawing is an
assertion. The plate art also flattens every storey into one point cloud before
drawing, so a divider across it divides the card rather than the zone, and it
would look right, which is the dangerous part.

**The real gap the survey found is not a motif.** 680 pages carry an oriented
floor plan in `<figure class="locator">` and none of them says which way is up;
"North is up" appears on the thirteen surveys and nowhere else. The orientation
is a verified derived fact. That is an instrument, not ornament, and it belongs
in a content change against `_build/build17.py`.

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

## P1.75 — `lastmod` is a build date wearing a modification date's name

**Found 1 Sep 2026, 05:00, while checking the scope of an unrelated commit.**
Not started deliberately: it touches `public/`, it carries a design decision, and
it turned up an hour before a shutdown. Reverted out of that branch rather than
left half-done.

`_build/sitemap.py:9` computes `today = datetime.date.today().isoformat()` and
line 34 writes it into the `<lastmod>` of **every** URL. So all 715 entries in
`public/sitemap.xml` carry one date: the day of the last build.

**Two separate problems, and the second bites daily.**

1. It asserts every page on the site was modified on the build date. That is not
   true of any of them &mdash; a figure claiming something the data does not
   support, on 715 pages, which is the largest live instance of this project's
   oldest rule.
2. **Any rebuild on a new day rewrites all 715 lines.** A pull request opened
   after one carries a 715-line diff nobody made, and a real one-line sitemap
   change would be invisible inside it. That is how a change hides.

**The decision, which is why this is not a five-minute fix.** Either give each
URL the real modification date of the page it points at, or drop `lastmod`
entirely. Both are defensible: an absent `lastmod` is honest and costs a crawler
hint; a per-page date is more useful and needs a source that is not "when the
generator last ran". **A filesystem mtime is not that source** &mdash; every
build rewrites every page, so the mtime is the build date again with extra steps.
An honest per-page date probably has to come from git history, and that is the
part to settle before writing any code.

**Acceptance criteria**

- `public/sitemap.xml` does not change when a rebuild changes no page.
- Whatever date is published, a reader can say what it means without reading
  `sitemap.py`.
- If `lastmod` is kept: one page whose content changed and one that did not carry
  different dates. Without that pair the fix is unproven.
- `scripts/check.py` stays green and the sitemap still lists every published page.

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

**Do not build these as 3D models, and `_build/build4.py` is gone.** This said
to copy that file until 20 August 2026; it was deleted with the Eye of Veeshan
on 17 August, so the instruction pointed at nothing. The withdrawal rule is in
`CLAUDE.md` section 8: a drawing is an assertion, so it needs *more* evidence
behind it, not less, and no encounter model may be built of a fight nobody
here has fought. `docs/PLANES.md` section 6b already declined the same idea
for Plane of Hate: *a downgrade dressed as an upgrade*.

A 20 August investigation added the arithmetic reason. `assets/zone-geometry.json`
holds `lines`, `n` and `z` per storey and nothing else — flat outlines, two
height numbers per band, and no walls anywhere in the file. A 3D view would have
to invent a height for every floor, every wall, and the gaps between storeys —
gaps `_build/geometry.py` states do not exist, because stairs and ramps fill
them. **If these fights are ever worth a diagram, it is a floor plan or a
section, drawn from what the mesh actually holds.**

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

## P5 - Serve the planner from a subdomain

**Recorded 18 Aug 2026, not started. Queued by the Director behind the tool
consolidation; the subdomain is the first thing after it.**

The planner lives at `samusmylove47-maker.github.io/EQL50ups/`. The home page
band links out to it, which works and reads as a link to somebody else's site.

**A subdomain answers the objection that ruled out same-origin hosting.** The
entry above says hosting it under `public/app/` "makes us responsible for a
release cadence we do not control", and that is still true and still decisive.
A subdomain sidesteps it entirely: the planner ships when its own repository
ships, and the URL still says ours. Nothing about our build or our deploy takes
on their cadence.

**One implementation trap, known in advance.** `eqlsource.com` is on Cloudflare,
and Cloudflare's proxy conflicts with GitHub Pages' certificate provisioning.
**The DNS record goes in DNS-only — grey cloud — until Pages has issued the
certificate.** Only then is proxying it a decision worth taking. Getting that
order wrong produces a certificate error on a public URL, which is the most
alarming possible failure for a page whose whole pitch is that it is safe to
use.

Three things move together and none is ours alone: the DNS record, a `VITE_BASE`
change in the planner's build, and every link pointing at the planner — the home
page band, `tools/50-upgrades.html`, and `assets/50-upgrades.json`'s `url`
field, which `refresh-upgrades.mjs` writes from a constant.

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

### The exception for Session E's gap engine, ruled 30 August 2026

Read plainly, the rule above forbids Session E's tool twice over: it parses a log
and it recommends gear, and **Log Parser** and **Gear Upgrade Finder** are named
in the first paragraph as EQL Tools' layer. The Director has ruled the exception
applies. It is written here because **a rule with a silent exception is worse
than no rule** — an unwritten carve-out reads to the next session as either a
dead rule or a broken one, and both readings are wrong.

**The exception is per finding, not per tool.** Nothing is exempt because of
whose repository it lives in. Each finding is admitted or refused on its own, and
a tool may ship nine findings and be refused the tenth.

**THE TEST, and it is deliberately one sentence you can apply without judgement:**

> **If a recommendation survives with the log removed, it belongs to
> eqlegendstools.com and we link to it.**

A finding ships only if it is **uncomputable from a catalogue**. An item database
plus a character sheet is the thing that already exists and is maintained better
than we would maintain it; anything reachable from those two inputs is theirs.

**What that admits.** Nine of E's fifteen need a log *and* measured mechanics,
and no item database can produce them: stance, lane uptime, position, pet uptime,
engaged time, resist rate, mana ceiling, procs-per-minute, and haste-against-cap.
Each is a fact about what a character actually did, not about what a character
could theoretically hold.

**What it constrains.** The four gear findings **never ship as a stat
comparison** — only as a ranked delta against the player's *own observed
baseline*. The distinction is the whole exception: "this sword has more DPS than
that one" is a catalogue answer and is theirs. "This sword closes the gap between
your measured haste and the cap you are already missing" cannot be computed
without the log, and is ours. Strip the log from the second sentence and it
collapses into the first, which is the test working.

**The open question in the ruling is closed, and it was three rather than two.**
This section recorded on 30 August that nine plus four is thirteen against
fifteen findings, and asked whoever landed the remainder to apply the test to it
in writing rather than guess. E did, the same day.

**Why it was three.** The Director's nine names **procs-per-minute**, which is a
*mechanic* from E's own table rather than one of the fifteen things the tool
reports. So eight of the nine land on the list, plus the four gear findings, is
twelve — leaving **spell/song rank**, **missing spells**, and **crit chance
against crit damage**. That is E's correction to a count this section took from
the ruling, and only E could have made it: the error was reading a mixed list as
a list of findings.

**The test applied to all three, which is what this section asked for:**

- **Missing spells entirely** — a lane the trio has access to and never casts.
  **Ours outright.** A catalogue can list what a trio *could* cast; only a log
  shows that it never did. **Absence is the one thing a catalogue structurally
  cannot hold.**
- **Spell and song rank.** **Conditional**, the same standing as the four gear
  findings. The catalogue holds every rank and what it does; the log holds which
  one you actually have, because the rank is printed in the line. Ships only as a
  ranked delta against the player's own observed output — a table of rank IX
  against rank X is a spell catalogue and is theirs.
- **Crit chance against crit damage.** **Conditional**, and it touches a second
  row in this file: **AA Planner** is already named as theirs, so the ladder and
  its costs are not ours to publish. What is ours is that the observed crit rate
  identifies which ranks a player holds, and at their observed damage the chain
  says which of the two is worth more — **and it is not always the same one.**
  That comparison cannot be computed from a ladder alone. Delta only.

**So the split is nine and six, and it closes:**

| ours outright — uncomputable from any catalogue | conditional — ranked delta only |
|---|---|
| haste against the cap · stance · ability-lane uptime · position · charm-pet uptime · engaged time · **missing spells** · resist rate · mana ceiling | weapon base damage · upgrade tier · exaltations · offhand legality · **spell/song rank** · **crit chance vs crit damage** |
| **9** | **6** |

**A SIXTEENTH FINDING INHERITS NOTHING.** The count above is load-bearing, not
descriptive. A new finding is **inadmissible until the test has been applied to
it in writing in this section** — which makes a rule of what was asked as a
favour, and is E's suggestion.

**A worked example, and it bit its author.** E's own gate ran against real claims
for the first time on 30 August and **rejected E's trio-DPS ceiling**: that
figure is computable from an item catalogue and a damage chain with no log at
all, so as a shipping finding it fails the test outright. It survives only as an
internal denominator that is never shown to a reader in any form. **The gap is
ours; the ceiling is not.**

**A tool reading your own log is not the site publishing a diary.** `CLAUDE.md`
§7 governs every page *about* a tool: no kill counts, no session windows, no
"seen x12". **It does not govern what a tool tells you about yourself.** The
whole value of a log-reading tool is that it says *your* haste, *your* uptime,
*your* missing lane — and someone applying the generic-voice rule to the output
rather than to the page would strip it of the only thing that makes it useful.
Written down here because that is a mistake a careful session makes while
following the rules, which is the kind worth pre-empting. E raised it; the
placement is this section's call.

**Ownership.** This section is the site's, not E's. E proposes wording; what a
page may claim about provenance is settled here, on the same footing as every
other row in this file. `sky-ledger` is E's repository name and is a legacy
label, not a description of its role.
