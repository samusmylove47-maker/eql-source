# Handoff — 18 August 2026

Read `CLAUDE.md` first. This file is the current state and the open work.

**This describes commit `3d0c9073`** (PR #101, merged — the tip of `main`). Diff
against it rather than trusting anything below — a later session should
re-derive, not remember. Name a commit `main` actually pointed at: a branch
commit that only ever reached `main` inside a merge is not one, so diffing
against it walks through a state `main` never had.

**The Director and this session exchange through this file.** Rulings arrive
under the From heading; work is reported back under the To heading,
written and committed with the pull request rather than said in a reply. When a
ruling has been applied it moves into whichever standing section it belongs in
and is deleted from the exchange. **The exchange holds only what is still live**
— if a heading below is empty, that is the correct state, not a lost note.

---

## Every figure here is a command, not a number

A remembered figure survives a session boundary as a fact. A command survives as
a fact-checker. Nothing in this file states a count that you cannot regenerate,
because the counts move and this file will not.

```bash
./build.sh                      # must exit 0
python3 scripts/check.py        # page count, and every link/chrome/ceiling rule
python3 scripts/gate_selftest.py  # the propagation gate still catches its faults
node scripts/toolsmoke.js       # every tool runs; every served bundle parses
```

| What you want to know | How to get it |
|---|---|
| How many pages ship | `python3 scripts/check.py` prints `checked N pages` |
| How many tools are registered | `python3 -c "import sys;sys.path.insert(0,'_build');from _partials import TOOLS;print(len(TOOLS))"` |
| Which tools | same import, `[t['slug'] for t in TOOLS]` |
| Every prose ceiling | `assets/prose-budget.json` — and `scripts/gate.py`'s `page_words` is the only correct way to measure against it |
| A page's current weight | `python3 -c "import sys;sys.path.insert(0,'scripts');from gate import page_words;print(page_words('public/index.html','index.html'))"` |
| The planner's catalogue counts | `assets/50-upgrades.json` → `figures`, **keyed by the dotted path each figure was read from** in the planner's `meta.json`. `counts.items` is the catalogue; `counts.purge.shipped` is what survived the era purge. They are not the same quantity and were equal until 18 Aug 2026 |
| When the planner snapshot was read | `assets/50-upgrades.json` → `read` — the day a person stood behind it, not the day a script ran |
| How to refresh that snapshot | `node scripts/refresh-upgrades.mjs <YYYY-MM-DD>`. Hand-run, needs network, never in `build.sh`. Never hand-edit a figure |
| Which zones are revamped | `assets/zones-index.json` → any zone with `revamped` |
| How many zones have cleared every gate | `python3 -c "import json,collections;print(collections.Counter(z['verify_level'] for z in json.load(open('assets/zones-index.json',encoding='utf-8'))))"` |
| Which pages lack the shared footer | `grep -rL site-foot --include='*.html' --exclude-dir=app public/` — the imported pages, and nothing else. Do **not** use `public/**/*.html`: with globstar off it silently skips the five root pages |
| What the Sky Ledger serves | `assets/sky-ledger.json` → `app.file`, `app.hash` |
| Measured sessions, zones, raid fights | `assets/measured.json`, `assets/raids-measured.json` |

**The rule behind the table:** where a decision can live in a data file or a
check, put it there. `zones-index.json` carrying the revamp date rather than two
generators is why that fact will outlive every session that reads this. It is
`gate.py`'s argument applied to sessions instead of pages.

---

## Do not build these

Every one has been considered and declined. A session arriving with energy and
no context will do them enthusiastically. Written down they are decisions;
unwritten they read as omissions.

| Not this | Why |
|---|---|
| Hosting the 50 Upgrades planner under `public/app/` | It is built, tested and refreshed in its own repository. We carry a description page and a link. Same-origin hosting makes us responsible for a release cadence we do not control. |
| A home-page feature band for 50 Upgrades | `index.html` has no room. The ceiling is in `prose-budget.json`, the gate fails at cap + 40, and the Sky Ledger band alone is ~190 words. The tools door already reads its count from `len(TOOLS)`, so the tool is announced at zero word cost. |
| Withdrawing any existing tool | Nothing currently duplicates anything. The Sky Ledger withdrawal on 17 Aug was justified by a correctness property ours lacked; absent that, two tools are two tools. |
| A shared `.btn` class | The imported pages carry their own stylesheets and never load `site.css`. A shared button would have to be injected into every one of them, and each already styles its own. Count them, never quote a number: `grep -rL site-foot --include='*.html' --exclude-dir=app public/`. Real, and post-launch. |
| The doubled `cache-control` header | Real, harmless, post-launch. |
| Migrating every internal href to the extensionless form | **The redirect is already live** — `/x.html` 307s to `/x`, measured 18 Aug 2026 — and this row was wrong for a day in saying otherwise. What is unbuilt is changing the ~61 hrefs per page that still say `.html`; each costs a reader one redirect hop. The cross-repo hold on it is **released**: the planner now links extensionless for all 42 of its outbound URLs, so the dependency is discharged. Released, not scheduled — it touches every internal link on 716 pages. **The redirect itself stays regardless**: it costs nothing and protects links already in the wild. |
| Self-hosting the site's fonts | Real, post-launch. |
| The map export | Post-launch. |
| Editing `public/assets/site.css` casually | It re-hashes `CSS_V` and rewrites the stylesheet line on every page. Fine when the CSS genuinely changed; never as a side effect. |
| Running `scripts/prose_budget.py` to fix a page that is over | It only lowers ceilings. A page over its cap is trimmed, or the ceiling is raised **by hand with the reason in the commit** — `CLAUDE.md` §5, precedent in PR #89. |

---

## Why conformance.js is hand-run, and what its silence means

Settled 18 Aug 2026. Recorded here rather than decided again by the next session
that notices it is not wired into anything.

**It stays hand-run. It does not go inside `check.py`.** Three reasons, in order
of weight:

1. **86 seconds against 2.3.** `check.py` runs before every commit and is
   currently fast enough that nobody weighs whether to run it. Folding in the
   sweep makes it roughly forty times slower, and the first thing that happens
   to a slow pre-commit check is that people stop running it. A check that is
   skipped catches nothing, so this would trade a live fast check for a
   thorough one nobody runs.
2. **It needs a browser, and a rebuild may not assume one.** Same rule that
   keeps `geometry.py` out of `build.sh` because it needs the game install, and
   `ogcards.py` out because it needs Pillow. A machine with a clean checkout and
   no Chrome must still be able to build and validate this site.
3. **It measures something that changes rarely.** Layout breaks when the chrome,
   the stylesheet or a template changes — not when a survey gains a paragraph.
   Wiring it to every commit spends 86 seconds re-proving an unchanged layout
   hundreds of times over.

The counter-argument is real and worth stating: `toolsmoke.js` **is** called by
`check.py`, and it is also a node script that can be absent. The difference is
0.08 seconds against 85.7 — two orders of magnitude, not a difference of
principle. If it ever gets fast enough, this reasoning is what to re-open.

`CLAUDE.md` §5 names it as the thing to run **after a layout, chrome or
stylesheet change**, which is the trigger this reasoning implies.

**Yes, it warns and continues where Chrome is absent** — verified by execution
on 18 Aug 2026, not by reading the code, by pointing its candidate list at
nothing:

```
WARN  no Chrome or Edge binary found — conformance sweep skipped.
      This is not a build failure. check.py and toolsmoke.js still
      cover the markup and the tools; nothing lays a page out.
exit=0
```

**And that is the sharp edge on it.** A WARN that exits 0 reads, in a log,
exactly like a clean sweep — the same equivalence between a dead check and a
passing one that `gate_selftest.py` exists to break. Two things guard it: every
successful run prints its page count and elapsed time, so a real sweep is
visibly a real sweep, and `--show` prints every measurement. **If you see no
output about pages, it did not look at any.**

---

## From the Director

**The tool consolidation is being mapped, and nothing should pre-empt it.**
Nine tools become three. The mapping was still running on 18 Aug 2026; the
Director will produce an ordered, independently-revertible PR sequence when it
lands, and will queue the planner subdomain behind it.

Until that sequence arrives:

- **Do not add, remove, rename or restructure a tool.** `_partials.TOOLS` is
  about to change shape, and `gate.py` rule 6 will follow it automatically —
  anything hand-aligned to the current nine gets aligned twice.
- **Do not fix the planner's footer**, which omits `50-upgrades`. It is about to
  be wrong in six new ways. Recorded in full under *For the session working on
  the planner*.
- **The subdomain is not started**, and it is first after the consolidation, not
  before. `docs/BACKLOG.md` P5 carries it, including the one trap worth knowing
  in advance: the DNS record goes in DNS-only until GitHub Pages has issued the
  certificate, because Cloudflare's proxy conflicts with that provisioning.

---

## To the Director

**PR 2: three tools withdrawn.** Six remain. Every accept criterion met, and
three things in the brief did not hold against the tree.

### Two of the PR 2 items are actually PR 3 items

**The undefined-constant check does not die here.** The brief says no surviving
tool page declares a capitalised data constant after these removals. Measured:

```
combo-calculator.html   9 declared   CLASSNAMES, CORDER, KINDS, RACES, RORDER, SKEY
race-unlocks.html       9 declared   CLASSNAMES, CORDER, KINDS, RACES, RORDER, SKEY
faction-impact.html     2 declared   FAC, RACES
```

Those are exactly the three pages PR 3 removes. `gate_selftest.py` case 1 still
points at `race-unlocks.html`'s `RORDER`, which is still there. **Retiring the
check now would have deleted live protection and a working self-test case**, so
it is untouched and carried to PR 3.

**None of the flagged prose became false either.** `build2.py:91` names Sky
Ledger, race unlocks and the calculator — all three survive PR 2. `:97` and
`build404.py:44` derive from `len(TOOLS)` and self-updated to *Six trackers*.
`:101-104`'s "what you tick is packed into the page URL" is still true of race
unlocks and the calculator, and `:190`'s "the race tracker and the calculator
share one save" is still true of both. **Every one of them goes false in PR 3**,
when those two are removed — which is the state the brief was describing.

`build1.py:396` is inside the Auras video script, not prose; the line numbers
there moved when the 50 Upgrades band landed.

### The inbound links were eight, and not the eight listed

`public/_redirects:13-14` is `/races` and `/calculator`, which point at tools
that survive. Nothing in that file referenced the three. The real set:

```
_build/build2.py        three hub cards (109, 158, 176) — not in the brief
_build/build24.py:162   /sets/ crumb          -> tools/index
_build/build24.py:166   "the gear tool"       -> 50 Upgrades
_build/changelog.py:56  <a> unwired to plain text, per the :18 precedent
_build/source/planeoffear.html:395  -> /sets/
_build/source/planeofhate.html:405  -> /sets/
```

Both surveys carry their own footers, as the brief said, so those two were the
ones no footer sweep would have caught.

### Raised, not decided

**`_build/build20.py:41` credits BarakDur for the idea behind the planar gear
tool.** Left exactly as written. Removing a credit is yours, and `CLAUDE.md` §7
is explicit that an outside contributor keeps their name — stripping one to tidy
after a withdrawal happened once before and was caught. The tool is gone; the
person still had the idea.

**The tools hub grid has drifted and I did not fix it.** Six tools registered,
five cards, and the one with no card is **50 Upgrades** — the tool being posted.
This predates PR 2: it was nine tools and eight cards before I touched it. PR 3
removes two more cards, so fixing it now means fixing it twice, which is your
own reasoning about B's footer. It wants generating from `TOOLS` rather than
hand-writing, once the count has stopped moving. Not urgent: the tool is in
every footer by `gate.py` rule 6, and the home page now leads with its band.

### Carried to PR 3

Retire the undefined-constant check and its self-test case; correct
`build2.py:91`, `:101-104`, `:190` and `build404.py:44`; regenerate the hub grid
from `TOOLS`. All four are only correct to do once race unlocks, the calculator
and the faction checker are actually gone.

---

## For the session working on the planner

**Your footer is missing a tool, and the Director has ruled: do not fix it yet.**
It lists eight tools and omits `50-upgrades` — which is to say it omits the page
it is. It is our footer as it stood before PR #90 registered that tool.

Fixing it entry by entry now means fixing it twice, because the tool count is
about to go from nine to three. **After the consolidation lands, copy the footer
once from the final state and add the drift check** — the same shape you already
built for the nav. A hand-copied footer drifts silently, which is the argument
that put `len(TOOLS)` behind ours and `gate.py` rule 6 in front of it; rule 6
cannot see your copy.

**Your outbound links are already correct** and this closed a hold on our side:
all 42 are absolute and extensionless, none end `.html`. Both forms resolve —
`/x.html` 307s to `/x` — so nothing was ever broken, and the prohibition on our
touching that redirect is now lifted.

Two more facts you cannot see from that repository:

**The Mistmoore revamp date is data, not code.** It lives in
`assets/zones-index.json` as `revamped` and `revamped_note` on the mistmoore
entry, and both `_build/build9.py` (the survey's measured section) and
`_build/build11.py` (the difficulty explainer) read it. When post-revamp logs
land, the ingestion path is a data edit and a rebuild — no generator changes.

**The licence correction is ours too.** `eqlwiki.com` publishes no content
licence: `siteinfo` `rightsinfo` is empty and `Project:Copyrights` is absent,
checked 18 August 2026. Any Sources screen carrying `used under CC BY-SA 4.0`
for eqlwiki-derived data is repeating an unsourced claim. Keep the attribution,
drop the terms, say the source states none.

---

## Recent shape of the work

The site was made **generic rather than personal** on 17 August: no character
names, kill counts, play dates or experience-per-kill anywhere a reader sees.
`CLAUDE.md` §7 is the rule and carries its three deliberate exemptions. A tier M
badge means "verified in play" — a page never has to publish the log to earn it.

**Tier C was withdrawn** the same day. It was generalised from a single event,
and one event is not a rank on a scale. The change log records both its
introduction and its withdrawal, because a ledger records what was true when it
was written.

The Castle Mistmoore survey is the house format; the other twelve and the raid
pages follow it. If you reformat anything, **diff for lost facts before you
commit** — a reformat deleted evidence on 17 August and a green build did not
notice. `scripts/check.py` validates that pages are well-formed, and `gate.py`
validates that figures agree with their data. Neither notices a sentence
describing a thing that no longer exists.
