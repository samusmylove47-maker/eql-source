# Handoff — 18 August 2026

Read `CLAUDE.md` first. This file is the current state and the open work.

**This describes commit `5f50d1b4`** (PR #95, merged — the tip of `main`). Diff
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

*Empty. Every ruling received has been applied and moved into the standing
section it belongs in — that is the correct state for this heading, not a lost
note.*

---

## To the Director

**PR: the EQL Source Auras band, from Session C's material.**

**The ceiling is 787, not 768, and 768 was not reachable.** This is the one
number in the brief I could not honour, so here is the derivation rather than
the conclusion.

`index.html` was **657** when I started, not 649. Session C measured against
`fddcb2ed`; two change-log entries have landed since, and the home page renders
`ENTRIES[:4]`, so the rolling window got heavier. Their band measurement was
exact — I reproduce their 136 words to the word — but the base under it moved.

| variant | band | index becomes |
|---|---|---|
| A, as C wrote it, + the naming edit | 137 | 794 |
| **B — cut #1 applied (approved)** | **130** | **787** |
| C — + cut #2 (you overrode this) | 125 | 782 |
| D — + cut #3 (you refused this) | 119 | 776 |

**Even taking all three cuts lands at 776.** 768 cannot be reached without
cutting copy you explicitly protected, so I applied the approved cut #1, kept
the eyebrow and the caption, and raised the ceiling to the measured 787. If you
want a number closer to 768 it has to come out of the second paragraph, which C
argued hardest to keep and which I would not cut without you saying so.

**It is a genuine raise, not a `LEDGERS` case — confirmed by reading it, not
recalling it.** Every one of the eight `LEDGERS` entries matches a *repeating
row*: `<div class="zrow">`, `<article class="st-entry">`, `<a class="plate">`,
`<a class="card">`, `<li class="gaterow">`, `<tr>`, `<article class="fzone">`.
Each exists because a set grows when something is recorded. The Auras band is
one fixed `<section>` of fixed prose that grows when nothing. Exempting it would
be exempting writing, which is the only thing the ratchet is for. You were right
and my reversal yesterday was in the other direction for the right reason.

### The video

Leads, above the prose. `.featgrid` is a single column at every width — there is
no two-column rule in `site.css` at all — so DOM order is reading order and
putting the `<figure>` first is what "above" means here. **No CSS change**, so
`CSS_V` does not re-hash.

`_build/media.py` needed no change either: it globs `_media/`, so committing the
two files was enough. They ship as `auras-trailer.5fc3fbbc.mp4` (839 KB) and
`auras-poster.5c861299.jpg` (175 KB).

Verified in a real browser at both viewports and under reduced motion:

| | video box | `autoplay` | shows |
|---|---|---|---|
| 1440x900 | 601x339, 1.77 | present | video |
| 390x844 | 273x154, 1.77 | **removed** | poster |
| 1440x900, reduce | 601x339, 1.77 | **removed** | poster |

No `<iframe>` on the page. No `controls` attribute, so no control implying sound
— Pause is the only one, and the caption says "silent". The encode carries no
audio stream at all.

### C's copy, untouched except as instructed

The WeakAuras credit, the from-scratch clause, the non-affiliation clause and
the word "Targeting" are all as written, and `_build/build1.py` now carries a
comment above the band saying why each is load-bearing, so a later tidying pass
has to argue with a reason rather than a preference. Cut #1 removed the
telemetry list only; **"of its own" survives it**, which `CLAIMS.md` §6 flags as
the load-bearing half of that sentence.

Naming applied: **EQL Source Auras** at first mention. There is no second
mention in the band, so "Auras" does not appear alone anywhere yet.

### Three things I did, slightly beyond the brief

**`docs/auras/ENCODE.md` now exists.** You referred to it as the asset spec; it
did not. C's encoding reasoning — CRF 28, 24fps against 30, the 10.9s cut point
and what is at t=11.25 — was in their HANDOFF note, which is read once. It is a
spec, so it is filed as one.

**I did not take C's HANDOFF section.** It was written into a structure that
changed after they branched, and its substance is now in `ENCODE.md` and
`CLAIMS.md`. Their branch keeps the original.

**No change-log entry.** A band announcing a tool that has not shipped is not a
correction, a source refresh, or an addition of a claim. When Auras actually
ships, that is the Addition. Saying so here because it also keeps the ceiling
arithmetic above honest — an entry would have moved `ENTRIES[:4]` again.

### Recorded, not solved

`tools/50-upgrades.html`'s meta description says **"twenty-three slots"** while
the snapshot holds `slots.worn.length` = **18**. Left exactly as written.
Session B has the question.

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
