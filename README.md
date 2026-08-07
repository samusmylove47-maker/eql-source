# EQL Source

**New here? Read `START-HERE.md` first.** It walks through setup from nothing.
**Handing this to Claude Code? Point it at `HANDOFF.md`.**
**Working with Claude Code? `CLAUDE.md` is the project's rules** — it loads
automatically every session.

A comprehensive, sourced, daily-updated reference site for EverQuest Legends:
survey plates for every revamped dungeon, interactive 3D raid encounter guides,
and progression tools that hold your place.

Site identity lives in **one file**: `site.config.json`. Name, tagline and URL.
Change it there, run `./build.sh`, and every page, the wordmark, the sitemap and
robots.txt update together.

---

## Deploying

The site is fully static. No build step is required to serve it; the Python
scripts only regenerate HTML.

**Netlify, drag and drop the zip.** Go to app.netlify.com, open the Sites tab,
and drag `norrath-survey.zip` straight onto the drop area. Netlify unpacks it
and publishes. `netlify.toml` is already configured, so nothing to set up.
This works from a phone browser too.

**After it is live, set your domain once.** The sitemap ships with a
placeholder. From a terminal:

```bash
SITE_URL="https://your-site.netlify.app" python3 _build/sitemap.py
```

Or just edit `sitemap.xml` and `robots.txt` by hand and replace
`REPLACE-ME.netlify.app`. Nothing breaks if you skip it — only search engines
care.

**Netlify, from Git (recommended, because you are updating daily).**

```bash
git init && git add -A && git commit -m "EQL Source"
git remote add origin <your repo>
git push -u origin main
```

Then in Netlify: New site from Git, pick the repo, leave the build command
empty, set publish directory to `.`. Every push deploys.

`netlify.toml` already sets `must-revalidate` on `/dungeons/*` and `/raids/*`
so a corrected guide is never served stale, and keeps `/assets/*` cached for
an hour. It also adds three short URLs: `/sky`, `/races`, `/calculator`.

---

## Structure

```
index.html              home — the spectrum, section entries
sources.html            sourcing standard, known gaps, change log
netlify.toml            headers, cache policy, redirects
build.sh                full rebuild
site.config.json        name, tagline, URL — the only place these live
HANDOFF.md              current state and the three jobs — for Claude Code
START-HERE.md           first-time setup, step by step
CLAUDE.md               project rules, loaded by Claude Code every session
docs/BACKLOG.md         the work, prioritised, with acceptance criteria
docs/DESIGN.md          the aesthetic brief, binding for design work
docs/SOURCES.md         source hierarchy and the automation watchlist
docs/AUTOMATION.md      how the twice-daily refresh works
scripts/check.py        pre-commit validation. Run before every commit
state/                  automation memory. Do not hand-edit
.claude/                Claude Code settings and custom slash commands
.github/workflows/      the scheduled refresh
favicon.svg             the spectrum, in miniature
robots.txt              generated
sitemap.xml             generated - carries your domain
.gitignore

assets/
  site.css              the whole design system, one file
  site.js               nav only, deliberately tiny
  zones-index.json      generated from zones.json — drives all navigation
  vendor/three.min.js   r128, vendored so the 3D has no CDN dependency

dungeons/
  index.html            the ten plates and the five maps
  <slug>.html           survey plates (imported)
  <slug>-map.html       navigation maps (imported)

raids/
  index.html            encounter index
  eye-of-veeshan.html   first full 3D encounter guide

_build/                 NOT served - blocked in netlify.toml
  _partials.py          shared header, nav, footer. Site name lives here
  build1-4.py           page generators
  sitemap.py            sitemap + robots
  source/               the original plates and tools, unmodified

tools/
  index.html
  plane-of-sky.html     Sky class-unlock tracker
  race-unlocks.html     race unlock tracker
  combo-calculator.html same app, boots on the calculator tab, shares one save
```

---

## Updating

**A plate changed.** Edit the file in `_build/source/`, then run `./build.sh`.
It re-imports and re-injects the site chrome and the favicon. Never edit the
copy in `dungeons/` directly — a rebuild overwrites it.

**Zone facts changed** (ZEM, respawn, verification date). Edit
`assets/zones-index.json`,
edit `assets/zones-index.json` to match, then `./build.sh`. The home page, the
spectrum and the dungeon index all read from it, so one edit updates
everything.

**A new zone.** Add it to `assets/zones-index.json` with a plate number and a
unique accent, drop `<slug>.html` into `_build/source/`, run `./build.sh`. The spectrum grows
on its own — change `grid-template-columns:repeat(10,1fr)` in `site.css` to
match the new count.

**A new raid encounter.** Copy `_build/build4.py`, change the data and the phase
array. The viewer engine is self-contained in that file: islands, markers,
radius rings, dashed paths, phases, and a hand-rolled orbit control so there
is no dependency beyond Three.js.

**The change log** on `sources.html` is hand-edited and typed — Addition,
Correction, Source refresh — so a fix is never mistaken for new content.

---

## What is honest about this build, and what is not

Solid: the ten plates, their coordinates, the tools, the race and Sky data.
All of it traces to a named source with a date.

**The Eye of Veeshan model is schematic, not surveyed.** Island proportions
and the vertical offset communicate the relationship between islands 7 and 8;
they are not scaled from game coordinates, because Plane of Sky has not been
surveyed. A handful of `/loc` readings from each island would turn it into a
measured model, and the page says so in place.

**D4 encounter behaviour is the biggest gap on the site.** Difficulty tiers
change mob *kits*, not mob levels, and no published source records which kits
attach to which raid boss at D3 and above. Only combat logs close that.

Five Plane of Sky class reward tooltips (Ranger, Rogue, Shadow Knight, Shaman,
Wizard) are still unverified for Legends and are flagged red in the tool.

---

## Validating

```bash
./build.sh
python3 scripts/check.py
```

`check.py` verifies every internal link resolves, every page carries the site
chrome and a favicon, `zones-index.json` matches what is on disk, zone accents
and plate numbers are unique, the spectrum column count matches the zone count,
and no page loads a script from a CDN. A failure is a blocker, not a warning.

## Automation

A scheduled GitHub Action checks the sources twice a day and opens a pull
request when something changes. It never publishes on its own — merging the
pull request is what publishes. See `docs/AUTOMATION.md`.
