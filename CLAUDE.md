# EQL Source — project rules

A reference site for EverQuest Legends: dungeon survey plates, 3D raid
encounter guides, and progression tools. Static HTML, no server, no database.
Netlify publishes on every merge to `main`.

Read this before your first edit in a session. For what to do, read `HANDOFF.md`
then `docs/BACKLOG.md`. For design work, `docs/DESIGN.md` is binding.

---

## 1. The standing agreement

**The human directs.** Priorities, scope, what publishes and when. They supply
in-game observation, screenshots and logs.

**You own accuracy.** Which claims enter the site, how each is sourced, what is
flagged uncertain, and what is refused for lack of evidence. Where sources
conflict, you adjudicate and record the reasoning.

That authority has a limit: you are the authority on *what the sources say* and
on *how confident the pages should sound*, not on ground truth in a live,
actively-patched game you cannot play.

**The standard: every claim traceable to a named source with a date, and every
gap stated rather than smoothed over.** Flag uncertainty even when it makes a
page look less finished.

---

## 2. Source hierarchy

Higher tiers override lower ones. Always.

0. **Measured combat logs — tier M.** First-hand instrument data from our own
   play: what happened, in the live game, on a dated session, to a named
   character. Parsed by `_build/logstats.py` into `assets/measured.json`.
   **Outranks every read source for what it directly measures, and generalises
   to nothing beyond its stated conditions.** Always publish trio, level, zone,
   difficulty label, date and sample size beside the figure. One session is a
   sample, not a rate: a drop seen once is "seen once". Full handling, including
   how mobs are told from players, is in `docs/SOURCES.md`.
1. **Official patch notes** — everquestlegends.com/news. Dated and authoritative.
   Anything published after a wiki page's last edit supersedes that page.
2. **Structured wiki data** — eqlwiki.com infoboxes, NPC tables, item tables,
   coordinate records — **but only once the page passes the provenance test below.**

### The provenance test — apply before trusting any eqlwiki page as tier 2

Tier 2 prints **bare, with no badge**, so misclassifying a page here is the most
expensive mistake available. Large parts of eqlwiki were bulk-imported from the
Project 1999 wiki *before EverQuest Legends existed*, and imported infoboxes look
identical to measured ones.

**EverQuest Legends launched 28 July 2026.** Check the page's oldest revision:

- **Oldest revision predates 2026, or the author is `imported>…` or `P99Wiki>…`**
  → the page is a Project 1999 import. **Tier 5, badge it,** no matter how
  structured it looks. Every Plane of Sky, Hate and Fear boss page fails this
  test: Spiroc Lord created Jan 2025, Bazzt Zzzt Nov 2025 and never edited since.
- **A named editor changed the field after launch with a comment describing
  measurement** → tier 2, and cite the revision id, date and editor.
- **Page carries `{{Classic Era}}`** → its prose is import until proven otherwise.
  Nine of the ten surveyed zone pages carry it. Note the wiki uses that template
  to mean the current level-50 era, not classic EverQuest, but in practice the
  tagged prose is P99 text.

Two tells that a stat block is classic rather than Legends: a boss listed with a
**single class** (Legends raid bosses run triple-class from D3), and raid sizing
advice measured in dozens of players (Legends caps raids at 8).

**A page can be tier 2 in its infobox and tier 5 in its prose at the same time.**
Najena is exactly that today — infobox 4:50, prose "19 minutes", same page.
3. **eqprogression.com / eqlwiki user guides** — Alanna's Race Unlock Guide and
   similar. Named authors, actively maintained, generally reliable.
4. **Community aggregators** — EQL Build Forge, EQ Legends Tools. Useful for
   cross-checking, snapshot-dated.
5. **Wiki prose** — treat as Project 1999 import until proven otherwise. Large
   parts are classic EverQuest text, word for word, describing a single-class
   game at fixed difficulty. Quote it only when marked as classic.

**Never** cite Project 1999 or Allakhazam as current Legends fact. Historical
context only.

### Badge everything below tier 2

Tiers 1 and 2 print plain. **Tiers 3, 4 and 5 carry a visible badge wherever the
claim appears** — `<span class="tier t3">T3</span>` and so on. A T3 claim printed
bare is a bug, and a worse one than a broken link.

**Exception, deliberate:** the ten survey plates carry no tier badges yet. They
are incomplete and ungraded on purpose, pending a later phase that verifies and
grades them in full. Do not add badges to them as part of other work, and do not
log their absence as a defect.

### Two systems that invalidate most inherited advice

- **Multiclass.** Characters run three classes at once. Two at creation, third
  at level 10, primary and race lock permanently at 11. The active trio uses the
  level of the *lowest* class in it.
- **Difficulty D0–D4 does not raise mob levels.** It makes mobs run player-style
  class kits, widens aggro ranges and pre-upgrades loot. Named mobs are often
  multiclass from D2; raid bosses start appearing triple-class at D3.

  **Measured, and it starts earlier than that on trash.** In Castle Mistmoore at
  **D1**, 8 Aug 2026, two ordinary trash types backstabbed 39 times between them
  — `An initiate familiar` 22, `A pledge familiar` 17 — while the same types were
  logged casting Root, Screaming Terror, Shadow Vortex, Shock of Poison and
  Engulfing Darkness. Backstab is a rogue ability and a spell list is not, so
  that mob type carries two kits at D1, on trash, not on a named. The log cannot
  tell whether one individual does both.

  Damage separates the same way: those familiars hit for 1–38 in melee and
  100–143 from behind. Never publish a combined average for a mob that
  backstabs.

  The tiers are named in game, and the zone line prints the name on entry —
  `You have entered The Castle of Mistmoore 1 (Awakened).`

  | | Name |
  |---|---|
  | **D0** | Base / Normal — the default open world |
  | **D1** | Awakened |
  | **D2** | Adaptive |
  | **D3** | Fused |
  | **D4** | Refined |

  Loot gives the same answer independently: items drop at `+N` and the modal `N`
  is the difficulty. Read the *dropped* value, not the created one — `looted a
  Keg Mallet +2 … to create a Keg Mallet +4` is a `+2` drop. The two readings
  agreed on our 8 Aug Mistmoore session, which is why both are kept and reported
  separately rather than collapsed: when they disagree, the difficulty is
  unresolved and the page must say so.

Inherited lines like "you need a full group of level 50s" came from a game where
neither was true. Unreliable in both directions. Mark them.

---

## 3. Hard rules

- **Never invent a number.** No drop rate, spawn timer, coordinate, stat or plat
  cost that you did not read in a named source. If it is not sourced, write
  "not recorded".
- **Never present classic EverQuest as Legends.** Where a page carries inherited
  prose, say so in place.
- **Never delete a flagged gap to make a page look complete.** Gaps close with
  evidence, not tidying.
- **Never edit files in `dungeons/` or `tools/` directly.** They are generated.
  Edit the originals in `_build/source/` and run `./build.sh`.
- **Never push straight to `main` for content changes.** Branch, open a pull
  request, let the human merge. Merging is what publishes.
- **Never merge your own pull request.**
- **New Sebilis / New Sebilisian Expedition content is out of scope** for the
  dungeon plates. The one exception is the Iksar race unlock, which requires
  that faction and is part of the race tracker.
- **Do not clone eqltools.com.** Client-mined data, log parsing and 3D zone
  geometry we cannot match. Our layer is quests, factions, routes and tactics.
  Link to them rather than shipping worse copies. `docs/BACKLOG.md` lists what
  not to build.

---

## 4. File map

```
HANDOFF.md          current state and the open work
site.config.json    site name, tagline and URL. The ONLY place these live
index.html          GENERATED by _build/build1.py
sources.html        GENERATED by _build/build2.py
dungeons/           GENERATED — plates and maps, chrome injected
raids/              index generated; encounter guides by _build/build4.py
tools/              GENERATED — four tools, imported or built
assets/
  site.css          the entire design system, one file
  zones-index.json  DRIVES ALL NAVIGATION. Edit this, rebuild, everything updates
  index-data.json   GENERATED — mined from the plates by _build/extract.py
  zone-geometry.json  floor plans derived from the game meshes. Committed data,
                    NOT a build step — see _build/geometry.py
  vendor/three.min.js   r128, vendored. Do not switch to a CDN
_build/
  _partials.py      head, nav and footer
  build1.py         home and dungeon index
  build2.py         tools, raids and sources indexes
  build3.py         imports plates and tools, injects chrome
  build4.py         raid encounter guides, contains the 3D engine
  build5.py         The Index tool
  geometry.py       zone floor plans from the game's own meshes. Reads .s3d
                    archives from the EverQuest Legends install, writes
                    assets/zone-geometry.json. Run by hand, not by build.sh: a
                    rebuild must work on a machine without the game. The .s3d
                    files are Daybreak's and are never committed
  extract.py        mines the plates into index-data.json
  sitemap.py        sitemap + robots
  source/           the real originals. Edit these
docs/
  BACKLOG.md        the work, prioritised, with acceptance criteria
  DESIGN.md         the aesthetic brief. Binding for design work
  SOURCES.md        source hierarchy and the automation watchlist
  AUTOMATION.md     how the twice-daily refresh works
scripts/check.py    validation. Run before every commit
state/              automation memory. Do not hand-edit
```

**`assets/zones-index.json` is the single source of navigation truth.** Home
page, plate cards and dungeon index all read from it.

Generated files are overwritten by `./build.sh`. A rebuild silently throws away
anything edited in place; `check.py` will not catch it.

---

## 5. Build and verify

```bash
./build.sh
python3 scripts/check.py
```

After changing `scripts/gate.py`, also run:

```bash
python3 scripts/gate_selftest.py
```

`scripts/gate.py` is the propagation gate, run by `check.py`. It exists because
every fault an external audit found on 9 Aug 2026 was the same fault: a
correction applied in one place instead of all of them. It refuses a build where
a count disagrees with the data it came from, a withheld coordinate reaches a
table, a page metadata asserts a figure the body hedges, a zone marked `full`
still names an open gate, or a tool is missing from the footer. **A dead check
looks exactly like a passing one**, so `gate_selftest.py` mutates the tree with
each real fault and proves the gate still catches it.

`check.py` also verifies that every internal link resolves, every page has the site
chrome and a favicon, `zones-index.json` matches the files on disk, no page has
lost its stylesheet, and **no page claims more verified plates than the data
supports.** Run it before every commit. A red check is a blocker, not a warning.

**The counting invariant.** `verify_level` is `full`, `partial` or `none`, and
anything not `full` must name its open gate in `verify_gate`. The home page and
the plates page render the count from that field. The site once published "8 of
10 verified" while the ledger said 5, because three sources of truth disagreed
and the highest number reached the front page. Never derive a count from "has a
date in the field".

**On Windows**, `build.sh` needs a `python3` on PATH; Windows ships only
`python`. Any new `open()` in a generator must specify `encoding='utf-8'` and,
for writes, `newline='\n'` — the platform defaults corrupt the output.

---

## 6. Design system

`docs/DESIGN.md` is the full brief and is binding. The non-negotiables, repeated
because they are easy to break by accident:

- **Monochrome chrome, polychrome content.** The frame is bone and graphite. All
  colour comes from the material — the ten zone accents, instrument blue for
  tools, ember for raids.
- **Three faces.** Saira Condensed (display, uppercase, tight), IBM Plex Mono
  (data, labels, anything numeric), Public Sans (prose).
- **The plate cards** are the home page's signature: one card per zone, washed
  with its own accent, carrying its plate number cropped by the card edge. They
  reflow, so adding a zone needs no layout change. A fixed-column spectrum of
  coloured bars preceded them and was withdrawn on 2026-08-08 — it cluttered the
  page and would not survive the zone count growing.
- Each zone owns its accent permanently. Never reuse or reassign one. Where an
  accent fails contrast as text, derive a lifted variant; never change the accent.
- **WCAG AA on all text.** Verified clean across 25 pages. Do not regress it.
- Elevation, small consistent radii, imperceptible surface gradients and
  purposeful motion are all permitted in service of hierarchy. `docs/DESIGN.md`
  sets the limits. An earlier brief banned them outright; that ban is withdrawn.

**Desktop PC is the primary target.** Other devices must stay functional and
390px must not overflow, but where a trade-off exists, the desktop reading wins.

---

## 7. Writing voice

Plain, specific, confident where the evidence is and openly uncertain where it
is not. Short sentences. No hype, no "ultimate guide", no exclamation marks.
British spelling. Numerals for game figures. Address the reader as "you" only in
instructional passages.

Do not write around a gap. Name it instead.

---

## 8. Adding things

**A new dungeon plate.** Add to `assets/zones-index.json` with the next plate
number and an unused accent. Put `<slug>.html` in `_build/source/`. Run
`./build.sh`. The plate grid reflows on its own; nothing in `site.css` needs a
count updated. `check.py` fails if the home page stops linking a zone.

**A new raid encounter.** Copy `_build/build4.py`. The 3D engine is
self-contained in it: islands, markers, radius rings, dashed paths, phases, and
a hand-rolled orbit control. Change the data and the phase array. Every model
must state in place whether it is surveyed from `/loc` data or schematic.

**A correction.** Update the change log on `sources.html`, typed as
Addition / Correction / Source refresh. A fix must never read as new content.

---

## 9. Current known gaps

These close with evidence, not tidying.

- **D4 encounter behaviour** — the tiers themselves are now documented in
  `learn/difficulty.html`: names, what scales, and what EQL Tools measured.
  D1 and D2 hit points are pinned; **D3 and D4 are not, by anyone**. And
  **which class kits attach to which raid boss at D3+ is still unpublished** —
  the biggest gap on the site. Needs combat logs from a raid at D3 or D4.
  Our own logs now show two kits on *trash* at D1, which is earlier and lower
  than the published claim about named mobs from D2.
- **Plane of Sky geometry** — never surveyed. The Eye of Veeshan model is
  schematic and says so. Needs `/loc` readings.
- **Five Sky class tooltips** — Ranger, Rogue, Shadow Knight, Shaman, Wizard
  reward stat blocks unconfirmed for Legends. Turn-ins are current.
- **Respawn ceilings** — the 28 July patch lowered maximums without publishing
  figures. Affected plates state pre-patch timers as ceilings.
- **Placeholder removals** — if placeholders are gone, published spawn
  percentages may be meaningless.
- **Druid and wizard port levels** — two wiki pages disagree, 25/27 against
  19/29.
- **Navigation maps** — five zones have plates but no map: Crushbone, Befallen,
  Blackburrow, The Hole, The Warrens.
- **Verification gates** — all 10 plates have cleared all three gates as of
  9 Aug 2026, and `verify_gate` in `assets/zones-index.json` records the evidence
  for each. Gate 3 changed that day: it asked for a collision check against a
  room list that does not exist, and now asks that every coordinate land within
  120 units of drawn floor. `docs/SOURCES.md` carries the reasoning and what the
  new gate is weaker at. Do not upgrade a level without doing the work, and do
  not read "verified" as "complete" — it means checked against source, not
  finished.

---

## 10. When you are unsure

Say so, in the page and to the human, and say exactly what would resolve it —
usually one screenshot, one log line, or one `/loc`. Naming the missing evidence
is more useful than hedging the prose.
