# EQL Source

A sourced, daily-updated reference site for EverQuest Legends: survey plates for
every revamped dungeon, the Plane of Sky guide, and progression tools.

Static HTML. No server, no database. Python scripts regenerate the pages; the
output is committed and served as-is.

- `START-HERE.md` — how the project is wired, and day-to-day operation.
- `CLAUDE.md` — project rules. Loaded automatically in every Claude Code session.
- `HANDOFF.md` — current state and the open work.
- `docs/BACKLOG.md` — the work, prioritised, with acceptance criteria.
- `docs/DESIGN.md` — the aesthetic brief. Binding for design work.
- `docs/SOURCES.md` — source hierarchy and the automation watchlist.
- `docs/AUTOMATION.md` — how the twice-daily refresh works.

Site identity lives in one file: `site.config.json` — name, tagline and URL.
Change it there, run `./build.sh`, and every page, the wordmark, the sitemap and
`robots.txt` update together.

---

## Deploying

Netlify is connected to the GitHub repository. **Anything merged to `main`
publishes automatically**, in about a minute. There is no build step on
Netlify's side: the generated HTML is committed, so Netlify only serves files.
Publish directory is `.` and the build command is empty.

`netlify.toml` sets `must-revalidate` on `/dungeons/*` and `/raids/*` so a
corrected guide is never served stale, caches `/assets/*` for an hour, blocks
the internal files from the public site, and adds three short URLs: `/sky`,
`/races`, `/calculator`.

Netlify keeps every previous deploy, with one-click rollback under **Deploys**.

---

## Structure

```
index.html              home — the spectrum, section entries      GENERATED
sources.html            sourcing standard, gaps, change log       GENERATED
netlify.toml            headers, cache policy, redirects
build.sh                full rebuild
site.config.json        name, tagline, URL — the only place these live
scripts/check.py        pre-commit validation. Run before every commit
state/                  automation memory. Do not hand-edit
.claude/                Claude Code settings and custom slash commands
.github/workflows/      the scheduled refresh
favicon.svg             the spectrum, in miniature
robots.txt              GENERATED
sitemap.xml             GENERATED

assets/
  site.css              the whole design system, one file
  site.js               nav only, deliberately tiny
  zones-index.json      hand-edited. Drives all navigation
  index-data.json       GENERATED — mined from the plates by extract.py
  vendor/three.min.js   r128, vendored. Loaded by no page since the encounter
                        viewer was withdrawn on 17 Aug 2026

dungeons/               GENERATED
  index.html            the ten plates and the five maps
  <slug>.html           survey plates (imported from _build/source/)
  <slug>-map.html       navigation maps (imported)

raids/
  index.html            encounter index                            GENERATED
  plane-of-sky.html     the Sky page, side elevation from the mesh  GENERATED

tools/                  GENERATED
  index.html
  plane-of-sky.html     Sky class-unlock tracker
  race-unlocks.html     race unlock tracker
  combo-calculator.html same app, boots on the calculator tab, shares one save
  index-search.html     The Index — 452 items, 208 named mobs

_build/                 blocked from the public site in netlify.toml
  _partials.py          shared head, nav bar and footer
  build1.py             home and dungeon index
  build2.py             tools, raids and sources indexes
  build3.py             imports the plates and tools, injects chrome
  build5.py             The Index
  extract.py            mines the plates into assets/index-data.json
  sitemap.py            sitemap + robots
  source/               the original plates and tools. Edit these
```

Anything marked GENERATED is overwritten by `./build.sh`. Edit the originals in
`_build/source/` or the generators in `_build/`.

---

## Updating

**A plate changed.** Edit the file in `_build/source/`, then run `./build.sh`.
Never edit the copy in `dungeons/` — a rebuild overwrites it.

**Zone facts changed** (ZEM, respawn, verification level). Edit
`assets/zones-index.json`, then run `./build.sh`. The home page, the spectrum
and the dungeon index all read from it, so one edit updates everything.

**A new zone.** Add it to `assets/zones-index.json` with the next plate number
and an unused accent, drop `<slug>.html` into `_build/source/`, run
`./build.sh`, and change `grid-template-columns:repeat(10,1fr)` in `site.css`
to the new zone count.

**A new raid encounter.** There is no template, deliberately. `_build/build4.py`
and the Eye of Veeshan page it rendered were withdrawn on 17 Aug 2026 because
the tactic the model illustrated was inherited Project 1999 text. See
`CLAUDE.md` section 8: a drawing is an assertion, so it needs more evidence
behind it, not less. Measured figures belong on the zone page.

**The change log** on `sources.html` is hand-edited and typed — Addition,
Correction, Source refresh — so a fix is never mistaken for new content.

---

## Building and validating

```bash
./build.sh
python3 scripts/check.py
```

`check.py` verifies that every internal link resolves, every page carries the
site chrome and a favicon, `zones-index.json` matches what is on disk, zone
accents and plate numbers are unique, the spectrum column count matches the zone
count, no page loads a script from a CDN, the tier-badge system is intact, and
**no page claims more verified plates than the data supports**. A failure is a
blocker, not a warning.

On Windows, `build.sh` needs a `python3` on PATH; Windows ships only `python`.

---

## What is solid and what is not

Solid: the ten plates and their coordinates, the tools, the race and Sky data.
All of it traces to a named source with a date.

**The Plane of Sky side elevation is measured, not schematic.** `_build/skyislands.py`
reads `airplane.s3d` and measures 21 bodies of walkable floor across 2,878 units
of height, and ten `/loc` readings label them. It prints its own vertical
exaggeration. It replaced a schematic model that was withdrawn.

**D4 encounter behaviour is the biggest gap.** Difficulty tiers change mob kits,
not mob levels, and no published source records which kits attach to which raid
boss at D3 and above. Only combat logs close that.

Five Plane of Sky class reward tooltips — Ranger, Rogue, Shadow Knight, Shaman,
Wizard — are unverified for Legends and flagged in the tool.

The full list is in `CLAUDE.md`, section 9.

---

## Automation

A scheduled GitHub Action checks the sources twice a day and opens a pull
request when something changes. It never publishes on its own — merging is what
publishes. See `docs/AUTOMATION.md`.
