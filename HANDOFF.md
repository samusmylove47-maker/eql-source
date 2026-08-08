# Handoff — current state

**EQL Source** is a reference site for EverQuest Legends, live at
https://eqlsource.netlify.app.

Read this, then `CLAUDE.md` (the rules), then `docs/BACKLOG.md` (the work).

---

## Orient first

```bash
./build.sh
```

```bash
python3 scripts/check.py
```

Then look at `index.html`, `tools/index-search.html` and
`raids/eye-of-veeshan.html` — a generated marketing page, a data tool, and a 3D
interactive. That is the range.

Report what you found before editing anything.

---

## What exists

**Five tools.** Plane of Sky class-unlock tracker (95 quests, all 560 trios),
race unlock tracker (16 races, merged faction routes), race-and-primary
calculator, The Index (452 items and 208 named mobs across the ten plates), and
the **Faction Impact Checker** — what grinding a zone does to your standing and
which unlocks that helps or costs. All client-side, no account, no server.

**Ten dungeon survey plates**, each carrying a floor plan derived from the
game's own zone mesh, with a height control where the zone stacks. Plus five
hand-written navigation maps. Plates are hand-written HTML in `_build/source/`;
the floor plan and any measured sections are injected at build time.

**One 3D raid encounter guide** — Eye of Veeshan, on vendored Three.js with a
hand-rolled orbit control.

**Zone geometry, ours.** `_build/geometry.py` reads the `.s3d` archives from an
EverQuest Legends install, parses the `.wld` mesh, keeps up-facing triangles and
traces the floor boundary. Output is `assets/zone-geometry.json`, committed. The
archives are Daybreak's and are never committed, and the extraction is run by
hand so a rebuild works without the game installed. 174 of 174 recorded mob
positions land on the drawn floor — a real check, since coordinates and geometry
come from unrelated sources.

**Measured play.** `_build/logstats.py` turns combat logs into
`assets/measured.json`: per-mob damage, land rates, casts, loot with `+N` tiers,
faction and experience per kill, control effects, and fights the group broke off.
`build9.py` writes it onto the matching plate. Logs are gitignored; only the
derived counts are committed.

**A published accuracy standard** — a five-tier source scale plus **tier M** for
measured logs, with tiers 3 to 5 carrying visible badges. This is the reason the
site exists.

---

## The three jobs, in priority order

### Job 1 — Aesthetic uplift
The design is disciplined but monotonous: every section is a heading followed by
a row of equal-weight cards, and the page reads grey. `docs/DESIGN.md` is a full
brief with testable direction, and it says which parts are load-bearing and
which are open. Do not freestyle it.

### Job 2 — New sections and tools
`docs/BACKLOG.md`, prioritised with acceptance criteria. The Faction Impact
Checker is **built**. The **Difficulty primer** is now the top item and is much
better supplied than it was: the tier names are known (D0 Base/Normal, D1
Awakened, D2 Adaptive, D3 Fused, D4 Refined), every log self-identifies its
difficulty two independent ways, and there is measured evidence of multiclass
behaviour on trash at D1.

### Job 3 — Close verification gaps
Five of ten plates have not cleared the full three-gate standard, and which gate
is open is recorded per zone. `/verify <zone>` walks it.

---

## How to work here

**Build, then check, then commit.** `check.py` is a blocker, never a warning. It
catches broken links, missing chrome, duplicate zone accents, CDN dependencies,
and any page claiming more verified plates than the data supports.

**The published site is `public/`, and nothing else is deployed.** Generators
write into it; `assets/*.json`, `_build/`, `docs/`, `scripts/`, `state/` and the
project docs stay at the root and never reach a host. This replaced a list of
twelve blacklist rules that only worked while someone remembered to extend it —
on 8 August 2026 Cloudflare served `CLAUDE.md`, `build.sh` and `docs/BACKLOG.md`
publicly because those rules were Netlify-specific and did not travel. Host
settings: Cloudflare Pages build output directory `public`, Netlify
`publish = "public"`, build command empty on both.

**Never edit generated files.** `dungeons/`, `tools/`, `raids/index.html`,
`index.html` and `sources.html` are output. Edit `_build/source/` and the
generators in `_build/`. A rebuild silently discards work done in the wrong
place, and `check.py` will not catch it.

**Branch for content, push freely for fixes.** Anything that changes a published
claim goes through a pull request. Build fixes and design work can go straight
to `main` once `check.py` passes.

**One task per conversation.**

**Measured data is not rebuilt by `build.sh`.** `logstats.py` and `geometry.py`
read things that live outside the repository — combat logs and the game install
— so they are run by hand and their JSON output is committed. `build.sh` reads
that JSON and degrades cleanly when it is missing.

---

## Slash commands

| Command | Does |
|---|---|
| `/newzone <zone>` | Adds a survey plate — accents, spectrum count, change log |
| `/verify <zone>` | Walks the three-gate verification standard |
| `/gaps` | Reviews every open gap and what evidence would close it |
| `/ship` | Build, check, commit, push, with a correction log entry if needed |

---

## Things that will bite you

**The stale-revision trap.** A wiki fetch can silently return an old revision, or
an empty page reported as success. Both have happened here — The Hole's plate was
once built from an empty fetch and thrown away. Always compare the `oldid` in the
fetched footer against the API's current revision.

**Verification counts.** Three sources of truth once disagreed and the site
published the highest. `verify_level` in `assets/zones-index.json` is explicit
and `check.py` guards it. Do not derive a count from "has a date in the field".

**Do not clone EQL Tools.** https://eqltools.com is a sibling site with
client-mined data, log parsing and 3D zone geometry. We cannot match their data
pipeline. We link to them. Our layer is quests, factions, routes and tactics.

**The tools are single-file apps** with inline CSS and JS, imported wholesale.
They do not use `assets/site.css`. Restyling the site needs a separate pass for
them, and their internal palettes should stay recognisably theirs.

**Regex escapes written by tooling.** A `` word boundary was once written
into a generator as a literal backspace byte (U+0008). It is invisible in an
editor and in a diff, the regex compiles without complaint, and it silently
matches nothing. If a pattern that obviously should match does not, check the
bytes before you check your logic.

**Test the middle, not just the extremes.** The measured tables passed at 1920px
and at 390px and scrolled the whole page sideways at 700px, because the mobile
stack started below the width at which the table stopped fitting. Wide content
belongs in its own `overflow-x` container.

**Windows build.** `build.sh` calls `python3`, which Windows does not ship. Any
new `open()` in a generator must name `encoding='utf-8'` and, for writes,
`newline='\n'`, or the output is corrupted silently.
