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

**Four tools.** Plane of Sky class-unlock tracker (95 quests, all 560 trios),
race unlock tracker (16 races, merged faction routes), race-and-primary
calculator, and The Index (452 items and 208 named mobs searchable across the
ten survey plates). All client-side. Progress packs into the URL fragment and
mirrors to browser storage — no account, no server.

**Ten dungeon survey plates** plus five navigation maps. Hand-written HTML,
imported from `_build/source/` with site chrome injected at build time.

**One 3D raid encounter guide** — Eye of Veeshan, on vendored Three.js with a
hand-rolled orbit control.

**A published accuracy standard** — a five-tier source scale, with tiers 3 to 5
carrying visible badges. This is the reason the site exists.

---

## The three jobs, in priority order

### Job 1 — Aesthetic uplift
The design is disciplined but monotonous: every section is a heading followed by
a row of equal-weight cards, and the page reads grey. `docs/DESIGN.md` is a full
brief with testable direction, and it says which parts are load-bearing and
which are open. Do not freestyle it.

### Job 2 — New sections and tools
`docs/BACKLOG.md`, prioritised with acceptance criteria. The top two are a
**Difficulty primer** (closes the biggest gap, and there is a good external
source to cite) and a **Faction Impact Checker** (nobody has one, and we already
hold the data).

### Job 3 — Close verification gaps
Five of ten plates have not cleared the full three-gate standard, and which gate
is open is recorded per zone. `/verify <zone>` walks it.

---

## How to work here

**Build, then check, then commit.** `check.py` is a blocker, never a warning. It
catches broken links, missing chrome, duplicate zone accents, CDN dependencies,
and any page claiming more verified plates than the data supports.

**Never edit generated files.** `dungeons/`, `tools/`, `raids/index.html`,
`index.html` and `sources.html` are output. Edit `_build/source/` and the
generators in `_build/`. A rebuild silently discards work done in the wrong
place, and `check.py` will not catch it.

**Branch for content, push freely for fixes.** Anything that changes a published
claim goes through a pull request. Build fixes and design work can go straight
to `main` once `check.py` passes.

**One task per conversation.**

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

**Windows build.** `build.sh` calls `python3`, which Windows does not ship. Any
new `open()` in a generator must name `encoding='utf-8'` and, for writes,
`newline='\n'`, or the output is corrupted silently.
