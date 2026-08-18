# EQL Source — project rules

A reference site for EverQuest Legends: dungeon surveys, 3D raid
encounter guides, and progression tools. Static HTML, no server, no database.
**Cloudflare** publishes on every merge to `main` — the host is a Worker with
static assets, configured by `wrangler.jsonc`. This file said *Netlify* until
14 August 2026 and it was wrong: `curl -I https://eqlsource.com` answers
`Server: cloudflare`. `netlify.toml` is still in the repo and its headers and
redirects are **inert**; treat it as history until it is removed deliberately.

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

### Provenance attaches to a claim, not to a page

`assets/sky.json` is the model, built 14 Aug 2026 after an audit found six
classic haste figures inside a badge that said **verified**.

**A boolean per page or per class will always lie eventually.** The Sky
tracker's `v` covered a class's turn-ins, givers, reward names, slots and stat
blocks at once — thirty-odd claims read from different pages on different days —
so a stat block nobody had checked inherited a badge the turn-ins had earned.

Each claim now names a source id, and `sources` carries that source's tier, URL,
revision and read-date. **Verified is derived and cannot be typed**: a claim
counts when its source is tier 2 or better and nothing is marked against it.
Applying that rule dropped the verified class count from eleven to five, and
Warrior fell out immediately — its stat blocks came from a page whose own
turn-ins we had already rejected as classic.

Do this for any dataset where one flag would otherwise cover several
independently-checkable claims.

### Badge everything below tier 2

Tiers 1 and 2 print plain. **Tiers 3, 4 and 5 carry a visible badge wherever the
claim appears** — `<span class="tier t3">T3</span>` and so on. A T3 claim printed
bare is a bug, and a worse one than a broken link.

**Exception, deliberate:** the survey plates carry no tier badges yet. They
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
  **D1**, 8 Aug 2026, two ordinary trash types backstabbed **113 times** between
  them across seven sessions — `A pledge familiar` 62, `An initiate familiar` 51
  — while the same types were
  logged casting Root, Screaming Terror, Shadow Vortex, Shock of Poison and
  Engulfing Darkness. Backstab is a rogue ability and a spell list is not, so
  that mob type carries two kits at D1, on trash, not on a named. The log cannot
  tell whether one individual does both.

  **Replicated in a second zone, 10 Aug 2026.** `An imp protector` in Nagafen's
  Lair at D1 backstabbed 103 times while casting Dry Bone Fire Burst 379 times,
  plus Greater Healing, Allure and Tashania. Same shape as Mistmoore, nearly
  three times the sample. `A lava beetle` there does it too, 15 backstabs
  alongside heals and roots.

  **At D0, trash runs one kit each, not two.** In The Ruins of Old Paineel at
  base difficulty, 11 Aug 2026, `An elemental capturer` backstabbed and never
  cast; `An elemental channeler` cast Superior Healing and never backstabbed;
  `An elemental wizard` cast Lightning Bolt and never backstabbed. So the class
  *kits* reach trash at D0 — but a mob carrying two of them is a D1 observation,
  and the distinction is worth keeping.

  Damage separates the same way: those familiars hit up to 39 in melee and up to
  168 from behind, with per-session backstab averages from 18 to 143 — and the
  imp protector 45 on average in melee against 175
  from behind, max 405. Never publish a combined average for a mob that
  backstabs.

  The tiers are named in game, and the zone line prints the name on entry —
  `You have entered The Castle of Mistmoore 1 (Awakened).`

  | | Name |
  |---|---|
  | **D0** | Base / Normal — the default. The open world, and any instance run at base |
  | **D1** | Awakened |
  | **D2** | Adaptive |
  | **D3** | Fused |
  | **D4** | Refined |

  Loot gives the same answer independently, and **the difficulty is the *lowest*
  tier that drops, not the commonest.** Measured 11 Aug 2026 across the 52
  sessions whose difficulty a numbered zone line states on its own: the minimum
  matched every one, the mode matched 50. In 1,742 upgradeable drops carrying an
  independent difficulty, **not one landed below the zone's tier.** Above it,
  about 19% at D1 and under 1% at D2 and D3.

  It is a roll, not a property of the item — `Fine Steel Rapier` dropped +1
  forty-three times, +2 eleven times and +3 once, all in D1 zones. Named mobs do
  not roll higher than trash. Befallen rolls above tier 19.5% of the time at D1
  and zero times in 115 drops at D3, so it is not a zone effect either.

  **A bare item is the tier-0 form**, so it has to be counted as `+0`, or every
  open-world session reads as D1. Read the *dropped* value, not the created one
  — `looted a Keg Mallet +2 … to create a Keg Mallet +4` is a `+2` drop.

  Both readings stay in `measured.json` as `drop_tier_floor` and
  `drop_tier_modal`, reported separately rather than collapsed: when the loot
  and the zone line disagree, the difficulty is unresolved and the page must say
  so. Where a session has no zone line at all, the floor is what names its
  difficulty.

  **Not every "You have entered" line names a zone.** `an area where levitation
  effects do not function` is an effect boundary, and parsing it as a zone
  invented one.

Inherited lines like "you need a full group of level 50s" came from a game where
neither was true. Unreliable in both directions. Mark them.

---

## 3. Hard rules

- **Never invent a number.** No drop rate, spawn timer, coordinate, stat or plat
  cost that you did not read in a named source. If it is not sourced, write
  "not recorded".

  **And a measured number goes stale.** This file carried "backstabbed 39 times
  between them — `An initiate familiar` 22, `A pledge familiar` 17" and
  "1–38 in melee and 100–143 from behind" until 17 Aug 2026. The parse holds
  113, 51 and 62, and a backstab maximum of 168; no session or combination of
  sessions produces 22 and 17, and one session's backstabs *average* 38.8, which
  cannot happen if the floor is 100. The figures were probably right against a
  smaller parse and four copies of the prose did not move when the data grew.
  **A figure that cites a dataset must be read out of that dataset at build
  time** — `_build/backstab.py` is the pattern. A number typed beside the data
  it claims to come from is the fault this project keeps finding in other
  people's work.
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
- **Do not ship a worse copy of something that already exists.** Where another
  tool holds client-mined data or geometry we cannot match, link to it rather
  than half-rebuilding it. `docs/BACKLOG.md` lists what not to build.

  The test is whether ours would be worse. Where we hold something nobody else
  does &mdash; the Sky Ledger knowing a turn-in piece can only be spent once, and
  refusing a drop rate it cannot measure &mdash; we ship it.

---

## 4. File map

```
HANDOFF.md          current state and the open work
site.config.json    site name, tagline and URL. The ONLY place these live
index.html          GENERATED by _build/build1.py
sources.html        GENERATED by _build/build2.py
dungeons/           GENERATED — surveys and floor plans, chrome injected
raids/              index and the Plane of Sky page (build8.py). No encounter
                    guides: the one that existed was withdrawn, see section 8
tools/              GENERATED — imported or built, one page per entry in
                    `_partials.TOOLS`, which is the count. Our own Plane
                    of Sky tracker was withdrawn 17 Aug 2026: the Sky Ledger
                    supersedes it, and two Sky trackers is the "which do I use"
                    problem with ours as the wrong answer
app/                GENERATED — the Sky Ledger's browser build, served under a
                    content hash. Written by _build/skyledger.py
items/              GENERATED — one page per item, plus an A–Z hub
named/              GENERATED — one page per named mob, plus an A–Z hub
archive/            GENERATED — the ten original plates, verbatim
learn/              GENERATED — the explainers
assets/
  site.css          the entire design system, one file
  zones-index.json  DRIVES ALL NAVIGATION. Edit this, rebuild, everything updates
  index-data.json   GENERATED — mined from the plates by _build/extract.py
  faction-data.json GENERATED — mined by _build/extract_faction.py OUT OF
                    _build/source/eql-race-unlocks.html, plus the measured half
                    from the logs. The tool source is the truth and this file
                    is downstream of it. Read as a second hand-maintained copy
                    on 14 Aug 2026 and "de-duplicated" the wrong way round,
                    which emptied it: the extractor had nothing left to mine
  zone-geometry.json  floor plans derived from the game meshes. Committed data,
                    NOT a build step — see _build/geometry.py
  vendor/three.min.js   r128, vendored. Do not switch to a CDN
_build/
  _partials.py      head, nav and footer
  build1.py         home and dungeon index
  build2.py         tools, raids and sources indexes
  build3.py         imports plates and tools, injects chrome
  build5.py         The Index tool
  ogcards.py        Open Graph share cards, 1200x630 PNG, from zones-index.json.
                    Run by hand like geometry.py: it needs Pillow, and a rebuild
                    must work without it. Output committed under public/assets/og/
  geometry.py       zone floor plans from the game's own meshes. Reads .s3d
                    archives from the EverQuest Legends install, writes
                    assets/zone-geometry.json. Run by hand, not by build.sh: a
                    rebuild must work on a machine without the game. The .s3d
                    files are Daybreak's and are never committed
  skydata.py        validates assets/sky.json and DERIVES which Sky claims are
                    verified. Run by build.sh before anything renders it, so a
                    malformed dataset, a claim naming a source that does not
                    exist, or a moved invariant fails the build. `--from-html`
                    re-extracts from the tracker source; a one-time escape
                    hatch, not part of the build
  extract.py        mines the surveys into index-data.json. Also assigns every
                    item and named mob its slug, so The Index (which links in
                    the browser) and build17.py cannot disagree about addresses
  build17.py        the item and named-mob pages, and their two A–Z hubs
  publicdata.py     public/data/*.vN.json — the datasets as a PUBLIC CONTRACT.
                    Generated FROM assets/, never symlinked to it: the internal
                    shapes change whenever a generator needs them to, and the
                    published ones may not. Fields are never removed and never
                    retyped; a breaking change gets a new version at a new URL
                    and the old one stays up. check.py declares the v1 shape and
                    fails the build if a field goes missing or a dataset empties
  build27.py        data/index.html — the human half of that contract
  skyledger.py      copies the Sky Ledger's browser build out of its own repo
                    into public/app/sky-ledger.<sha1>.html and writes
                    assets/sky-ledger.json. The hash is load-bearing: an
                    unhashed copy goes stale in readers' caches exactly as the
                    stylesheet did. Exits cleanly when the Ledger repo is
                    absent, so a machine without it still builds
  build28.py        tools/sky-ledger.html
  sitemap.py        sitemap + robots
  source/           the real originals. Edit these
docs/
  BACKLOG.md        the work, prioritised, with acceptance criteria
  DESIGN.md         the aesthetic brief. Binding for design work
  SOURCES.md        source hierarchy and the automation watchlist
  AUTOMATION.md     how the twice-daily refresh works
scripts/
  check.py          validation. Run before every commit
  toolsmoke.js      runs each tool's JavaScript under a stub DOM and asserts it
                    neither throws nor renders nothing. Called by check.py;
                    skipped with a WARN where node is absent. Every other check
                    reads the HTML a page ships, which is how a tool with a dead
                    class picker passed 721 green checks on 14 Aug 2026
  contamination.py  scans OUR OWN published content for classic EverQuest
                    conventions and writes assets/contamination.json, rendered
                    at learn/contamination.html. Hand-run. Points at eqlsource
                    and nowhere else: a scanner that only finds other people's
                    rot is an attack ad. If it is ever pointed outward it comes
                    here first and the result publishes either way
  conformance.js    loads every built page in headless Chrome over file:// and
                    reports console errors, viewport overflow and an empty body,
                    at 1440x900 and 390x844. Hand-run, ~86s for the site, no
                    dependencies — it drives Chrome over the DevTools Protocol
                    with node's built-in WebSocket. WARNs and exits 0 where no
                    browser is installed. It aborts every non-file: request, so
                    the webfonts fall back and it must NEVER be extended to
                    judge type or spacing: that would be measuring a page which
                    does not ship. `--show` prints every measurement, because a
                    silent pass and a dead check read the same
  toolrender.js     dumps what a tool actually renders, so a refactor can be
                    proved to change nothing. Run it before and after any change
                    that moves data a tool reads, and diff. toolsmoke says the
                    pane is full; only this says it is full of the same thing
  gate.py           the propagation gate, run by check.py
  gate_selftest.py  proves the gate still catches each fault it was built for
  prose_budget.py   lowers the prose ceilings after a trim. Run by hand
  stamp.py          fingerprints the build inputs so a stale tree cannot pass
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

**After touching anything a tool's JavaScript reads — a data file, a constant,
an injected blob — run the tools:**

```bash
node scripts/toolsmoke.js
```

`check.py` calls it, so a normal run covers you. Run it directly when you want
the per-tool detail. It executes each tool under a stub DOM and asserts it
neither throws nor renders nothing. **It cannot tell you a tool looks right or
that a click does the right thing** — only that the script runs and the page
fills. That is the exact gap that let a tracker ship with an empty class picker
and every other check green, and it is all this closes. Opening the page is
still the only way to know it works.

**After a layout, chrome or stylesheet change, load the site in a real browser:**

```bash
node scripts/conformance.js
```

Hand-run and not part of `build.sh` — it takes about 86 seconds against the
whole site and needs a browser installed, and a rebuild must work without one.
It loads every built page over `file://` at 1440x900 and 390x844 and reports
console errors, `scrollWidth` against `innerWidth`, and an empty body. That is
the layer `check.py` and `toolsmoke.js` both miss: neither of them lays a page
out, so neither can see a page that overflows 390px or throws on load.

**It aborts every non-file request, so the three Google-hosted faces fall back
to system fonts.** Nothing it reports is a statement about type, rhythm or
whether a label fits its box — it is measuring a page that does not ship. Do not
extend it to make that judgement.

Two traps are recorded in its header and both cost a wrong answer while it was
being written: `mobile:true` makes the layout viewport elastic, so the overflow
check can never fire; and a clean sweep is indistinguishable from a broken
measurement, which is what `--show` is for.

After a deliberate trim, lower the prose ceilings to match and commit them with
the trim:

```bash
python3 scripts/prose_budget.py
```

Ceilings only ever fall. Raising one means editing `assets/prose-budget.json` by
hand and saying why in the commit — a decision, not a side effect. The script is
deliberately outside `build.sh`, because a build that re-baselined its own
ceilings would never fail the prose check at all.

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

**A shell heredoc eats backslash escapes.** Any file whose content contains
`\n`, `\t`, `\x89`, or a regex escape like `\b` or `\d` is written through the
editor, never through `python - <<'PY'` or `cat <<'EOF'`. This has cost three
incidents:

- `src-app.js` — an escaped `\n\n` became two real line breaks inside a
  JavaScript string literal. The bundle raised `SyntaxError`, the Sky Ledger
  rendered nothing, and **196 dataset assertions still passed**, because they
  exercise the engine and the data rather than the built page. It shipped to a
  public release for six minutes.
- `media.py` — `b'\x89PNG\r\n\x1a\n'` arrived as a literal newline and the file
  would not parse.
- `gate.py` — `\b` arrived as a backspace character, and `check.py` caught it
  only because it happens to scan for control characters.

The tell is that the damage is invisible in a diff summary and obvious in
`cat -A`. `node scripts/toolsmoke.js` now parses every served bundle for exactly
this fault, which closes the worst case and none of the others.

---

## 6. Design system

`docs/DESIGN.md` is the full brief and is binding. The non-negotiables, repeated
because they are easy to break by accident:

- **Monochrome chrome, polychrome content.** The frame is bone and graphite. All
  colour comes from the material — the zone accents, instrument blue for
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
- **WCAG AA on all text.** Do not regress it.
- Elevation, small consistent radii, imperceptible surface gradients and
  purposeful motion are all permitted in service of hierarchy. `docs/DESIGN.md`
  sets the limits. An earlier brief banned them outright; that ban is withdrawn.

**Desktop PC is the primary target.** Other devices must stay functional and
390px must not overflow, but where a trade-off exists, the desktop reading wins.

---

## 7. Writing voice

**The site is generic, never personal.** This is the rule that governs every
other one in this section, set 17 August 2026 after a sweep found 322 places
where the site read as one player's diary rather than a reference.

Nothing is tied to a character. No kill counts, swing counts, hit rates,
"seen x12" tallies, session windows, play dates, hours farmed, attacker counts,
or damage shares. **No experience per kill at all** &mdash; experience is a
function of the reader's level, so a figure measured at 26 tells a stranger at
35 nothing true. Zone ZEM is the one sanctioned experience figure.

**A tier M badge already means "we verified this in play".** The page does not
have to publish the log to earn it. Wherever a sentence exists to prove the
measurement happened, delete it and let the badge do the work.

**Keep the fact, drop the count.** "882 stunning melee attacks were shrugged off
and 296 stuns landed anyway" becomes "stuns here arrive as spells, not as melee".
Same knowledge, no diary. Never delete a finding to satisfy this rule; restate it.

Three exemptions, all deliberate:

- **Sample inputs on tools** may show a character name, because a reader needs
  to see the shape of what to type.
- **`credits.html` names the site's own characters, once.** Decided by the
  collaborator on 17 August 2026: credits is where a site is entitled to say who
  it is. It is the only page that does, and a future sweep should not read it as
  a violation.
- **Named third parties keep their names everywhere.** Annalise (AnnaWulf),
  sowoky and any other outside contributor are credited by name with a date,
  because CLAUDE.md's own standard is that every claim traces to a named source.
  The rule protects the collaborator's characters, not other people's. Stripping
  an outsider's credit to satisfy it is misattribution, and it happened once
  during that sweep before being caught.

- **`public/data/*.vN.json` keeps its fields**, including sighting counts and
  session dates. It is a published contract and fields are never removed.
  Decided 17 August 2026: reword the human-facing descriptions, leave the shape
  alone. The counts are gone from every page a reader sees.

Plain, specific, confident where the evidence is and openly uncertain where it
is not. Short sentences. No hype, no "ultimate guide", no exclamation marks.
British spelling. Numerals for game figures. Address the reader as "you" only in
instructional passages.

Do not write around a gap. Name it instead.

---

## 8. Adding things

**A new dungeon survey.** Add to `assets/zones-index.json` with the next plate
number and an unused accent. Put `<slug>.html` in `_build/source/`. Run
`./build.sh`. The plate grid reflows on its own; nothing in `site.css` needs a
count updated. `check.py` fails if the home page stops linking a zone.

**A new raid encounter.** There is no template any more, and that is
deliberate. `_build/build4.py` held a self-contained 3D engine and rendered the
Eye of Veeshan; both were withdrawn on 17 August 2026 because the tactic the
model illustrated — pulling the boss down to island 7 — was inherited Project
1999 text. The collaborator has killed that boss about ten times and has always
killed it where it spawns.

**The lesson is a rule now: a drawing is an assertion.** A 3D model, a plotted
route or a phase diagram carries more conviction than the same claim in prose,
so it needs *more* evidence behind it, not less. Do not build an encounter model
of a fight nobody here has fought. Measured figures — damage to kill, attacker
counts, what a boss cast — belong on the zone page, where they already are.

**A correction.** Update the change log on `sources.html`, typed as
Addition / Correction / Source refresh. A fix must never read as new content.

---

## 8b. The plates were retired on 10 Aug 2026

The site began as ten hand-drawn coordinate plots and the guides were named for
them. `_build/geometry.py` replaced them: the floor plans read the game's own
`.s3d` meshes, separate the storeys, filter the named by storey, and check every
coordinate against walkable floor at build time. That check caught six
impossible Najena positions; the hand plots had nothing to check against.

The guides are **Dungeon surveys** now. The ten originals live whole in
`assets/archive-plates.json`, rendered by `_build/build14.py` at
`/archive/index.html`, stored exactly as they last shipped. **Do not restore
them to the guides and do not restyle them in the archive** — a restyled archive
is not an archive.

`plate` survives as a numeric field in `zones-index.json`. It is an identifier,
not a label.

## 9. Current known gaps

These close with evidence, not tidying.

- **D4 encounter behaviour** — **partly closed, and partly retracted 11 Aug 2026.**
  Master Yael was killed at all five tiers in one session in the group instance
  of The Hole, parsed by `_build/raidstats.py` into `assets/raids-measured.json`.
  Damage to kill runs 75,369 / 85,415 / 139,117 / 227,690 / 242,060, and those
  figures are sound — the D4 total was re-checked line by line.

  **Two things published beside them were not, and the same fault caused both:
  a figure printed from data with a sentence typed next to it.**

  **These were not trio kills.** Every raid-boss fight in every log we hold is a
  **public pick-up raid of 5–7 players**, and our own characters dealt 13–44% of
  the damage. "Killed by one trio" was never true of any of them. `raidstats.py`
  now records `attackers` and `our_damage_share_pct` per fight so no page can
  restate it wrongly. **Other players are never named on the site outside the
  credits**, so the count and the share are recorded and the names discarded.

  **Self-healing is not gated at D3.** "He healed himself never at D0–D2" was
  read off one session. A later D2 kill of the same boss shows one self-heal
  (`Superior Healing`, 210 hp), and **Lady Vox heals itself at D0**, in the open
  world. What the tier raises is how much of the kit appears, not whether a
  heal is in it. **And "ten times at D4" is ten log lines of one effect ticking
  every six seconds for the same 22 hit points** — a recurring drain, not ten
  decisions. The same shape appears on Vox at her top tier.

  **The plane-boss half closed 14 Aug 2026.** Cazic-Thule was killed at D2, D3
  and D4 and Innoruuk at D3 and D4, along with ten of Innoruuk's court, and
  every spell each cast is in `assets/raids-measured.json`. Cazic-Thule runs a
  shadow-knight-flavoured kit — `Harm Touch`, `Life Leech`, `Dooming Darkness`,
  `Shadow Vortex` — and **heals itself sixteen times at D2**, which is the
  strongest evidence yet that self-healing is not tier-gated. Innoruuk mixes
  wizard (`Ice Comet`, `Wrath of Al`Kabor`), shaman (`Malosi`, `Plague`,
  `Gale of Poison`) and priest (`Superior Healing`) in one fight, which is the
  published triple-class claim showing up in a log for the first time.

  D3/D4 hit points are still not pinned by anyone: damage to kill is an upper
  bound, not HP.

  **A single client under-witnesses a large raid, and the attacker count is how
  you tell.** Where two kills of one boss at one tier were both logged with a
  similar attacker count the totals agree — Master Yael at D1, six attackers
  both times, 1.1x apart. Where one client saw two attackers and the other
  twelve, the same boss at the same tier came out **60x apart**. `raidstats.py`
  marks the thinner view `damage_is_floor` and records why. Trust the fullest
  view of a boss at a tier and treat the rest as lower bounds.

  **The general lesson, because it has now cost two retractions in one day:**
  a log records what its own character witnessed and who else was present. Read
  both before describing a fight, and never let a hand-typed sentence sit beside
  a generated figure without checking it against the same data.
- **Plane of Sky geometry** — **half closed, 11 Aug 2026.** `_build/skyislands.py`
  reads `airplane.s3d` and measures 21 separate bodies of walkable floor across
  2,878 units of height, committed to `assets/sky-islands.json` and drawn as a
  side elevation on the Sky page. What it cannot do is say which measured body is
  which island: that lives in the teleporter network, not the mesh. **Ten `/loc`
  readings, one per island, label the chart permanently.** The side elevation
  now prints its own vertical exaggeration (0.38, so the zone reads 2.6x
  flatter than it is), which it had not since 11 August.
- **Five Sky class tooltips** — Ranger, Rogue, Shadow Knight, Shaman, Wizard
  reward stat blocks unconfirmed for Legends. Turn-ins are current.
- **Respawn ceilings** — the 28 July patch lowered maximums without publishing
  figures. Affected surveys state pre-patch timers as ceilings.
- **Druid and wizard port levels** — two wiki pages disagree, 25/27 against
  19/29.
- **Verification gates** — **not every zone has cleared them, and this section
  asserted that they had until 18 Aug 2026.** Some zones carry
  `verify_level: "none"`, and a cold session reading the old sentence would have
  been told the opposite of what the data says. `verify_level` in
  `assets/zones-index.json` is the only answer, and `verify_gate` carries either
  the evidence for a cleared zone or the name of the gate still open. Count it
  rather than remembering it:
  `python3 -c "import json,collections;print(collections.Counter(z['verify_level'] for z in json.load(open('assets/zones-index.json',encoding='utf-8'))))"`

  A zone marked `none` has had no gate attempted, not a gate failed. Gate 3
  changed on 9 Aug 2026: it asked for a collision check against a room list that
  does not exist, and now asks that every coordinate land within 120 units of
  drawn floor. `docs/SOURCES.md` carries the reasoning and what the new gate is
  weaker at. Do not upgrade a level without doing the work, and do not read
  "verified" as "complete" — it means checked against source, not finished.

---

## 10. When you are unsure

Say so, in the page and to the human, and say exactly what would resolve it —
usually one screenshot, one log line, or one `/loc`. Naming the missing evidence
is more useful than hedging the prose.
