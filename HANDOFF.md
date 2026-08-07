# HANDOFF — read this first

You are picking up **EQL Source**, a reference site for EverQuest Legends. It is
live at https://eqlsource.netlify.app and it works. Your job is to make it
better, not to rebuild it.

Read this file, then `CLAUDE.md` (the rules), then `docs/BACKLOG.md` (the work).
Everything else is reference you can read when you need it.

---

## 1. Orient yourself first

Before proposing anything, run these and read the output:

```bash
./build.sh                  # regenerates every page from source
python3 scripts/check.py    # validates. Must pass before any commit
```

Then look at `index.html`, `tools/index-search.html` and
`raids/eye-of-veeshan.html` in that order. Those three show the range: a
generated marketing page, a data tool, and a 3D interactive.

**Then tell the human what you found and what you propose to do first.** Do not
start editing on your first turn.

---

## 2. What exists

**Four tools.** Plane of Sky class-unlock tracker (95 quests, all 560 trios),
race unlock tracker (16 races, merged faction routes), race-and-primary
calculator, and The Index (452 items and 208 named mobs searchable across the
ten survey plates). All client-side. Progress is packed into the URL fragment
and mirrored to browser storage — no account, no server.

**Ten dungeon survey plates** plus five navigation maps and a campaign plate.
These are hand-written HTML, imported from `_build/source/` with site chrome
injected at build time.

**One 3D raid encounter guide** — Eye of Veeshan, built on vendored Three.js
with a hand-rolled orbit control.

**A published accuracy standard** — a five-tier source scale, with tiers 3 to 5
carrying visible badges. This is the reason the site exists. Protect it.

---

## 3. The three jobs, in priority order

### Job 1 — Aesthetic uplift
The design is competent and disciplined but monotonous: every section is a
heading followed by a row of equal-weight cards, and the page reads grey.
`docs/DESIGN.md` is a full brief with specific, testable direction. **Do not
freestyle this** — the existing system is deliberate and the brief tells you
which parts are load-bearing and which are yours to change.

### Job 2 — New sections and tools
`docs/BACKLOG.md` has them prioritised with acceptance criteria. The top two are
a **Difficulty primer** (closes our biggest gap, and there is a good external
source to cite) and a **Faction Impact Checker** (nobody has one, and we already
hold the data).

### Job 3 — Close verification gaps
Five of ten plates have not cleared the full three-gate standard, and which gate
is open is recorded per zone. `/verify <zone>` is a slash command that walks it.

---

## 4. How to work here

**Build, then check, then commit.** `check.py` is a blocker, never a warning. It
catches broken links, missing chrome, duplicate zone accents, CDN dependencies,
and — importantly — any page claiming more verified plates than the data
supports. That last check exists because the site once published "8 of 10
verified" when the real number was 5.

**Never edit generated files.** `dungeons/`, `tools/`, `raids/index.html`,
`index.html` and `sources.html` are all output. Edit `_build/source/` and the
generators in `_build/`. `check.py` will not catch this; a rebuild will silently
throw your work away.

**Branch for content, push freely for fixes.** Anything that changes a published
claim goes through a pull request. Build fixes and design work can go straight to
`main` once `check.py` passes — the human will tell you if they want that
tightened.

**One task per conversation.** Finish, commit, `/clear`, start the next.

---

## 5. Slash commands already built

| Command | Does |
|---|---|
| `/newzone <zone>` | Adds a survey plate correctly — accents, spectrum count, change log |
| `/verify <zone>` | Walks the three-gate verification standard |
| `/gaps` | Reviews every open gap and what evidence would close it |
| `/ship` | Build, check, commit, push, with a correction log entry if needed |

---

## 6. Things that will bite you

**The stale-revision trap.** A wiki fetch can silently return an old revision, or
an empty page reported as success. Both have happened here. The Hole's plate was
once built from an empty fetch and had to be thrown away. Always compare the
`oldid` in the fetched footer against the API's current revision.

**Three sources of truth once disagreed about verification counts** and the site
published the highest. `verify_level` in `assets/zones-index.json` is now
explicit and `check.py` guards it. Do not derive a count from "has a date in the
field".

**Do not clone EQL Tools.** https://eqltools.com is an excellent sibling site
with client-mined data, log parsing and 3D zone geometry. We cannot match their
data pipeline and should not try. We link to them. Our layer is quests,
factions, routes and tactics — the human-knowledge layer. `docs/BACKLOG.md`
explains the split.

**The tools are single-file apps** with inline CSS and JS, imported wholesale.
They do not use `assets/site.css`. If you restyle the site, they need a separate
pass — and their internal palettes should stay recognisably theirs.

---

## 7. First session, suggested

1. Run the build and the checker. Report state.
2. Read `docs/DESIGN.md` and `docs/BACKLOG.md`.
3. Propose an ordered plan for the aesthetic uplift, with the specific files you
   would touch and what you would change in each. Wait for approval.
4. Implement one section end to end — the hero and the first band — so the human
   can react to something real before you do the rest.

Do not do all of Job 1 in one commit. Small, reviewable steps.
