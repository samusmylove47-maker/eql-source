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

**Cloudflare** serves the site — a Worker with static assets, configured by
`wrangler.jsonc`. **Anything merged to `main` publishes automatically**, in about
a minute or two. There is no build step on the host's side: the generated HTML is
committed, so the Worker only serves files.

This section said *Netlify* until 4 September 2026. `curl -I https://eqlsource.com`
answers `Server: cloudflare`, and CLAUDE.md has recorded the switch since 14
August — the README simply did not move with it.

`public/_headers` sets the cache policy: **every** page revalidates, after a
reader was served a pre-redesign home page from their own cache, and `/assets/*`
is cached for an hour. It also adds the three short URLs `/sky`, `/races` and
`/calculator`.

**Nothing outside `public/` is published, and that is structural rather than a
rule.** `wrangler.jsonc` points the served folder at `./public`, so `_build/`,
`docs/`, `CLAUDE.md` and the rest are not reachable at any address. Verified 4
September against the live site: those all answer 404 while `/assets/site.css`
answers 200.

`netlify.toml` is still in the repository and **nothing reads it**. Its headers
and redirects are inert; the force-404 rules it once carried are gone, because
they only existed when the whole repository was the publish directory. Treat it
as history until it is removed deliberately.

To undo a bad deploy, `git revert` the merge on `main` and open that as a pull
request — merging it publishes the fix, by the same one route as everything else.

---

## Structure

**Everything served lives under `public/`.** This block placed `index.html`,
`sources.html`, `assets/`, `dungeons/`, `raids/` and `tools/` at the repository
root until 6 September 2026. None of them has ever been there — `wrangler.jsonc`
serves `./public` as the assets directory, and that is what the paths below
reflect. It also listed `tools/plane-of-sky.html`, withdrawn on 17 Aug 2026 when
the Sky Ledger superseded it, and omitted five tools that ship.

```
build.sh                full rebuild
site.config.json        name, tagline, URL — the only place these live
wrangler.jsonc          the host: a Worker serving ./public
netlify.toml            INERT. Nothing reads it; kept as history
CLAUDE.md               the project rules. Read before your first edit
HANDOFF.md              current state and open work
START-HERE.md           the door for a cold session
_build/                 the generators. Outside public/, so never published
_media/                 source media. media.py hashes it into public/assets/media
assets/                 the INTERNAL datasets and the stylesheet source
docs/                   BACKLOG, DESIGN, SOURCES, AUTOMATION
scripts/                check.py, gate.py, conformance.js and the rest
sources/raw/            fetched patch notes, kept verbatim
state/                  automation memory and the build stamp. Do not hand-edit
.claude/                Claude Code settings and custom slash commands
.github/workflows/      the scheduled refresh

public/                 EVERYTHING SERVED. All GENERATED unless said otherwise
  index.html            home — the plate cards
  sources.html          sourcing standard, gaps, change log
  search.html           site search index
  404.html
  favicon.svg  robots.txt  sitemap.xml
  _headers              headers, cache policy, redirects — the file actually read
  assets/
    site.css            the whole design system, one file
    fonts/              26 self-hosted .woff2 since 30 Aug 2026, plus fonts.css
    media/  og/         hashed media and the share cards
  data/                 public/data/*.vN.json — the datasets as a PUBLIC CONTRACT
  dungeons/             the surveys, their floor plans and navigation maps
  raids/                index and the Plane of Sky page
  items/  named/        one page each, plus two A–Z hubs
  learn/                the explainers
  archive/              the ten original plates, verbatim
  app/                  the Sky Ledger and Lockouts browser builds, hash-named
  tools/                index.html plus one page per entry in _partials.TOOLS —
                        50-upgrades, combo-calculator, faction-impact,
                        gap-engine, index-search, lockouts, race-unlocks,
                        sky-ledger

assets/                 (internal, NOT served)
  zones-index.json      hand-edited. DRIVES ALL NAVIGATION
  index-data.json       GENERATED — mined from the surveys by extract.py
  zone-geometry.json    floor plans from the game meshes. Committed, not built
  vendor/three.min.js   r128, vendored. Loaded by no page since the encounter
                        viewer was withdrawn on 17 Aug 2026
```

Counts are deliberately not repeated here: the two that were (452 and 208) had
drifted to 435 and 232 before anyone noticed. `_partials.TOOLS` is the count of
tools; `assets/zones-index.json` is the count of zones.

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
and an unused accent, drop `<slug>.html` into `_build/source/`, and run
`./build.sh`. **That is the whole procedure.**

This used to end "and change `grid-template-columns:repeat(10,1fr)` in
`site.css` to the new zone count". There is no such rule in `site.css` and there
has not been since the fixed-column spectrum was withdrawn on 8 Aug 2026 and
replaced by the plate cards, which reflow. CLAUDE.md section 8 says so in as
many words — *"The plate grid reflows on its own; nothing in `site.css` needs a
count updated"* — so the README was telling a reader to hand-edit a layout
constant that no longer exists, in the one document a newcomer reads first.
`check.py` fails if the home page stops linking a zone, which is the real
backstop.

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
