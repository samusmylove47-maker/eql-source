# Handoff — 18 August 2026

Read `CLAUDE.md` first. This file is the current state and the open work.

**This describes commit `fddcb2ed`** (PR #92, merged — the tip of `main`). Diff
against it rather than trusting anything below — a later session should
re-derive, not remember. Name a commit `main` actually pointed at: a branch
commit that only ever reached `main` inside a merge is not one, so diffing
against it walks through a state `main` never had.

**The Director and this session exchange through this file.** Rulings arrive
under `## From the Director`; work is reported back under `## To the Director`,
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
| The planner's catalogue counts | `assets/50-upgrades.json` — `counts`, `standing`, `purge` |
| When the planner snapshot was read | `assets/50-upgrades.json` → `read` |
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
| `.html` → extensionless 307 | Real, post-launch, and **held by a cross-repo dependency as of 18 Aug 2026: do not remove the `.html` form.** The 50 Upgrades planner's masthead and footer link the `.html` URLs for all 32 of their outbound links, so dropping the rule breaks that footer at once. The Director has asked that repository to link extensionless and will release this hold when it has. Until then this is not merely deferred — it would break a live page in another repository. |
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

**The `assets/50-upgrades.json` refresh is deliberately not being done yet.**
The snapshot is stale — 3,653 items vendored against 3,663 live — but the
planner's own session is mid-turn and the snapshot would be stale again before
a refresh here finished. The Director will schedule it once that turn lands and
has been verified. **Do not refresh it opportunistically**; a vendored snapshot
whose read-date is newer than its verification is worse than a stale one.

---

## To the Director

**PR: A1, A2 and A4. A3 is a second pull request against the workflow.**

**A1 — Mistmoore is `partial`.** `verify_gate` names what changed, that gates 1
and 2 stand on sourcing, that gate 3 is open because nobody has checked whether
the mesh moved, and that one logged session in the revamped zone closes it.
Every downstream count re-rendered itself: the home page reads **9 fully
verified**, the dungeon index reads **9 of 13 … 1 is partial and 3 are not
verified at all**, and `sources.html` moved from *Three* to **Four of the 13
surveys have not cleared**. Nobody typed any of those.

**Three second-order effects beyond the two you flagged.**

*`gate.py` check 2's second assertion was dead, and also wrong.* Its regex read
`(\w+) of the ten plates have not cleared`. The plates became surveys on 10
August and that sentence renders its count from `len(Z)`, so the page has said
"of the 13 surveys" ever since — it had matched nothing for eight days and
reported clean. It also compared against `npart`, while the sentence counts
every survey short of the full standard, `partial` and `none` together. So on
the day it started matching it would have failed a correct page: `npart` was 0
and the page said three. **Fixing the regex alone would have converted a silent
check into a false one**, so both are fixed together, and `gate_selftest.py`
grows a 25th case that proves the revived check reaches the sentence that
actually ships.

*A plural agreement bug that only existed at `npart == 1`.* The verdict sentence
would have shipped "1 are partial". `npart` had been 0 since the sentence was
written, so it had never rendered. Now derived.

*The prose ratchet fired, correctly, and the first fix I reached for was the
wrong one.* `dungeons/index.html` grew 374 → 450 words, because the "Open gates"
list prints `verify_gate` in full for every zone short of `full` and Mistmoore
became a fourth entry. I raised the ceiling by hand to 450 — the sanctioned
path — and was about to send it to you that way, on the reasoning that `LEDGERS`
carries an argument that widening it should be hard.

**That reasoning was out of date and I had not checked it.** `LEDGERS` already
holds five entries of exactly this shape, each with the same comment in
different words: one card per zone forbids adding a zone, one card per tool
forbids shipping a tool, one row per boss kill forbids measuring another. The
open-gates list is the sixth instance of a pattern this file has settled five
times, and it carries the sharpest edge of any of them — a ceiling over those
rows puts budget pressure on the description of an open gap, and *"never delete
a flagged gap to make a page look complete"* is a hard rule. A check whose
cheapest remedy is to say less about an unsolved problem is worse than no check.

So the rows are exempt and the hand-raise is reverted. The page measures **181**
words of actual prose, the ratchet lowered its ceiling from 374 to 181 on its
own, and **193 words of slack that had been hiding behind the gate rows are
gone**. Opening or closing a gate now moves this ceiling by nothing.

I mention the wrong turn because it is the failure mode this project keeps
finding: I quoted a rule from memory instead of reading it, and the memory was
a version of the file that no longer exists.

**A2 — the change log entry** is a `Source refresh` dated 18 Aug 2026. It
records the Mistmoore revamp, records the Kedge Keep respawn fix separately
against §9's open respawn gap and notes that no figure was published this time
either, and states plainly that survey prose has **not** been adjudicated
against these notes. Ledger rows are exempt from the ceilings, so it cost no
words anywhere.

**A4 — answered above**, in *Why conformance.js is hand-run*, with the WARN path
verified by execution rather than by reading it.

**Not done, as instructed:** no ingestion of the notes into survey prose, and no
50 Upgrades refresh.

---

## For the session working on the planner

Two facts you cannot see from that repository:

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
