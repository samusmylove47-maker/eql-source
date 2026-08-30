# Handoff — 18 August 2026

Read `CLAUDE.md` first. This file is the current state and the open work.

**This describes commit `5ee3cd3b`** (PR #103, merged — the tip of `main`). Diff
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

**PR 3 is not being done, and this is the reasoning rather than a deferral.**

The consolidation was going to take nine tools to three. It took nine to six and
stops there. Ruled 18 Aug 2026 with the owner's authority delegated.

PR 2 removed the character sheet, the planar gear tool and the inventory reader,
and it was right for one reason: **50 Upgrades already did all three jobs,
better, against a bigger catalogue.** Keeping a worse copy of something already
available is the rule this site applies to other people's tools, so it has to
apply to ours.

**That reason does not exist for the remaining three.** Nothing supersedes the
race unlock tracker, the race and primary calculator, or the faction impact
checker. Deleting three working, unduplicated tools to reach a number would
invert the standard the consolidation was justified by — it would be removing
things *because* they are ours, which is the opposite of the rule.

Three items were carried to PR 3 and are now moot in the right direction:

- **The undefined-constant check stays.** It was to be retired because no
  surviving tool page would declare a capitalised constant. Three still do —
  `combo-calculator` and `race-unlocks` nine each, `faction-impact` two — and
  `gate_selftest` case 1 still points at a live target.
- **The tools-index prose stays true.** "What you tick is packed into the page
  URL" describes race unlocks and the calculator, which survive; so does "the
  race tracker and the calculator share one save".
- **The hub grid is fixed rather than deferred.** The reason to wait was that
  PR 3 would remove two more cards. It will not.

If a successor to any of those three ever ships, the precedent is set and the
handling is written down: delete the page, keep the reason in `TOOLS`, record it
in the change log, redirect both address forms, no tombstone.

---

## To the Director

### 30 Aug 01:30 — STANDBY. Fonts done and pushed; five lines for the restore

**Relayed the standby block to C, D, B and E before touching my own tree**, as
ordered. All four sent.

1. **What I was doing: the Google Fonts fix, and it is DONE, not in progress.**
   All four faces are self-hosted from `public/assets/fonts/`, 26 files, 318 KB,
   fetched once by a new hand-run `_build/fetchfonts.py`. **Zero of 715 pages
   fetch another origin.** Verified as a matched pair on one page: `index.html`
   reads self-contained **NO** before and **YES** after, with no-transmit-path
   YES both times, so the verdict turns on exactly the change.

   **The sha to use is `523fac0` or later, NOT the `df49a58` this entry named
   when it was written.** D fixed the auditor's exit status at `fe14728`: at
   `df49a58` it exits 0 on a self-contained NO, so a CI check reading only the
   exit code would go green beside a page fetching from three origins — the exact
   failure this whole thread is about. The measurement above stands unchanged,
   because `df49a58`'s *verdicts* are right and only its exit status was wrong;
   it is automation, not conclusions, that would be misled.
2. **The next concrete step is to open the PR.** The branch is
   `claude/self-host-fonts-and-split-the-claim`, pushed. It was never opened as a
   pull request because standby arrived first. Everything is committed; nothing
   is half-applied.
3. **The directive's "three lines in one file" was wrong and the correction is
   the thing most worth not re-deriving.** `_partials.py:202-204` fixed **700**
   pages. The other **15** — the thirteen surveys and two imported tools — never
   call `head()`, carry their own `<head>`, and were the most-read pages on the
   site. They are rewritten in `build3.py`'s `inject()` so a sixteenth imported
   page cannot arrive with a Google link nobody notices.
4. **Two new checks, both mutation-proven, both passing.** `check.py` now fails
   any page fetching another origin on load, and fails if a declared face does
   not resolve from the stylesheet's own directory — B's trap, where a missing
   font silently falls back and "looks like a design choice rather than a bug".
   36 self-test cases, up from 35.
5. **Held in my head and in no file: `learn/difficulty.html` overflows 390px by
   4 pixels**, in both grounds, found by the conformance run I did immediately
   before standby. It is unrelated to the fonts, it is not fixed, and it is the
   only finding in 717 pages. Second unfiled thing: E's carried note says the
   BACKLOG arithmetic is **three** unaccounted, not two — `procs-per-minute` is a
   mechanic, not one of their fifteen — and their nine/six split closes it. #150
   merged with my wording and wants amending to theirs.

**Not done, deliberately, because standby says start nothing:** the PR, the
`sources.html` correction is written and committed but unreviewed, and the
`learn/difficulty.html` overflow.

**One correction arriving after the above was written, from D at standby.** The
auditor's exit-status fault — exits 0 on a self-contained NO — **is fixed**, at
`fe14728`. **If anyone wires this into CI, use `523fac0` or later, not
`df49a58`**: against `df49a58` a green tick would sit beside a page fetching from
three origins, which is the exact failure this whole thread is about. The
matched-pair measurement above stands unchanged — `df49a58`'s verdicts are
correct and only its exit code was wrong, so nothing I concluded moves. D is at
`22ce477`, 106 green; the Director's standby snapshot has them at `df49a58` / 104
and is two commits stale.

**CARRIED FROM C AT STANDBY, and it changes what tomorrow starts on.** Recorded
here because I am the only session that can reach the Director and the Director
cannot reply.

- **Shara has merged the lockout work and built on it.** PR #14 into `master` at
  01:22Z, PR #15 at 05:25Z; her master is **8 commits beyond** head `6834d78`,
  which is an ancestor of it. Every document saying "unpushed" was stale within
  hours.
- **Her shipped master carries C's retracted paragraph verbatim**, at
  `src/main/logRotation.js` lines 24, 28 and 42 — *"THE RESET, MEASURED RATHER
  THAN TYPED … a measurement, not a constant somebody typed"*. C withdrew that
  today, and she has built an Eastern reset setting on top of it. The number may
  be right; **the claim that anyone measured it is not**, because those two Alt+Z
  readings are object 2, the six-day rolling instance lockout.
  `proposed/FOR-SHARA-2026-08-30-reset-provenance.md` is written and pushed, and
  it leads with her design being better than C's — she gated the hour on
  `hourKnown` with `RESET_RULE` as fallback and left `RESET_RULE.hour` null,
  which closes the gap C had reported open without breaking D's anti-constant
  rule. **Somebody has to make sure she sees it.**
- **C is NOT mid ratchet-port.** The standby snapshot says so and it is wrong;
  the port is finished, committed and verified — injecting `hour:11` into the
  vendored `RESET_RULE` now fails the ported test where before the port it
  produced zero failures. C is at `fd198c7c` (docs) and `session-c/feat-lockouts-wip`
  at `28feac2` (app), both pushed to the EQLSAuras repo so a session without this
  disk can still read them.
- **Four of five `=Auras` renderers are self-contained, overlay included**,
  measured with `df49a58`. That turns our band's scoping sentence — *"the overlay
  drawn over the game requests nothing at all"* — from an assertion into a
  measurement. Commands in their HANDOFF section 19.

### 30 Aug — 16d4edad published (not 9ad53415), the count corrected to six, and the Auras answer

**Item 1. Published, both conditions met — and the build moved under me while I
worked, which is worth more than the publish.** You named `9ad53415`. I verified
that build, ran `./build.sh` before amending a commit, and `lockouts.py` did
exactly what it is designed to do: it found a NEWER build in D's repo,
`16d4edad`, copied it and swept the old one. So the commit, the PR title and my
report to you all said `9ad53415` while the tree shipped `16d4edad`.

Caught before merge, by an unrelated grep that listed the served file. **It is
280,212 bytes**, read off disk, and I have now verified it the same two ways:
zero external references statically, and zero network requests observed in a
browser, rendering the grid. `9ad53415` was 275,459 bytes; `eb2a1195`, which both
replace, was 265,191, read 27 Aug, matching your figure exactly.

**The lesson is about the design, not the accident.** "Every D release needs an A
commit" makes a rebuild a publish decision — so any `./build.sh` between
verification and commit can silently change what ships. The audible no-op I added
on 27 Aug printed the swap plainly and I did not read it, because I ran the build
for an unrelated reason. Verify immediately before committing, or not at all.

**Zero external references, verified two independent ways.** Statically: no
absolute `src`/`href`, no protocol-relative URL, no `@import`, no remote `url()`,
no `fetch`/`XHR`/`WebSocket`/`sendBeacon`/`importScripts`, no preconnect, no
`fonts.googleapis.com`, no CDN, and no `http(s)://` literal anywhere — against a
deliberately over-broad pattern set, on both the old build and the new. Seven
embedded `data:` URIs, all fonts. At runtime: opened in a browser,
**no network requests recorded at all**, no console errors, and it renders the
grid rather than an empty shell.

**Item 2. You are right, it is six — one per mob, and the way I got four is the
part worth keeping.** Measured against the pre-fix artefact at `8604ef43`:

| mob | loc field in the pre-fix bundle |
|---|---|
| A Visiting Priestess | `−493, 170` |
| BoneCracker | `−262, 167` |
| Ekeros | `−681, −49` |
| Officer Grush | `~−385, 230` |
| Rathyl | `−670, −119` |
| Trazdon | `−225, 150` |

The bundle is JSON, so the minus is stored as the **six-character escape**
`−` — **245 of them, and zero literal minus signs in the file.** The scan
that produced "four" matched on the character class `[-−]`, which cannot match an
escape sequence; it counted the mobs whose digits happened to parse anyway. Fixed
in `gate.py`, `gate_selftest.py` and above, each with the reason rather than just
the number.

**Item 3. Yes — two sentences become false, and one of them is on the home page.**

The site's claims about the app are these, verbatim:

- home band: *"It reads your combat log in the browser, and **nothing leaves the
  machine**."*
- tools page: *"**Nothing is uploaded**; there is no server to upload to."*,
  hero-sig *"**Nothing transmitted**"*, and *"nothing installed · **nothing
  sent**"*

**"Nothing leaves the machine" is the one that breaks outright.** A Google Fonts
fetch leaves the machine. It does not carry the log, but the sentence is broader
than the log. *"Nothing transmitted"* and *"nothing sent"* are unqualified and
break the same way.

**And the site would then contradict itself on one page.** Your Auras disclosure
— which I have not touched — already says the fetch *"is the main window only:
the overlay drawn over the game requests nothing at all."* The tracker is being
integrated into `src/renderer/main-window/index.html`, which **is** that window.
So the home page would simultaneously say the main window fetches from Google and
that the tracker sends nothing, about the same running code.

**The fix is to scope the claim to the artefact, not to the tool.** Every one of
those sentences sits beside *"Run it in your browser"* and *"served from this
site"*, so they were always about the copy we serve — the copy I verified today.
They just do not say so.

**D has proposed better wording than mine and I would take it**: the engine has
no transmit path, so your log cannot leave regardless of where it is embedded.
That is true of the standalone build and of the integrated one, which is exactly
the property a sentence on a landing page should have. I have not applied it —
this PR publishes a build and fixes a count, and rewording the band is a separate
decision. Say the word and it is two sentences.

**And the verification fan-out found the part I had missed: the tension is not in
the future, it is live now, on our own pages.**

`public/tools/lockouts.html` — the page that prints *"Nothing transmitted"* and
*"there is no server to upload to"* — **itself preconnects to
`fonts.googleapis.com` and `fonts.gstatic.com` and loads a stylesheet from
Google, on load, before a reader has clicked anything.** So does every other
page: **715 of them**, from the shared head in `_partials.py:202-204`. It
predates this branch and is nothing to do with the lockout tool.

Both things are true at once, and that is the whole problem: the **app** is
genuinely clean — I verified zero external references statically and zero network
requests at runtime — while the **page making that promise** discloses the
reader's IP to Google to render its own headings.

**The sharpest form of it is an asymmetry in our own disclosure.** We tell a
reader, in the Auras band, that Auras *"fetches its typeface from Google each
time it launches, which discloses your IP address to Google"*. We say nothing of
the kind about the page they are reading that sentence on, which has already done
it. Holding a third party to a standard we do not state for ourselves is the
shape this project calls an attack ad, and `scripts/contamination.py` exists
because of exactly that reasoning.

The tools hub is where it reads worst: its signature line says **"Works
offline"** above all seven cards, on a page that needs Google to finish drawing.

**Three things follow, and none of them is mine to decide alone:**

1. Scope the tool claims to the artefact ("the copy on this page"), or take D's
   egress wording, which is true in every host.
2. Consider a site-level font disclosure equivalent to the one we give Auras.
   Your instruction protects the Auras sentence; it says nothing about our
   silence regarding ourselves, and I am raising that rather than acting on it.
3. `conformance.js` aborts every non-file request, which is why nothing here ever
   surfaced from a sweep: it has measured a site whose webfonts never load since
   the day it was written. That is documented and deliberate, and it is also why
   this went unseen — the fourth instrument this month whose stated limitation
   hid something real.

**What I could not verify:** the Auras repository is **not checked out on this
machine** — only `EQLS-Auras-2026-08-23.zip`, dated a week ago. I cannot confirm
the three Google Fonts fetches or commit `1fe8fb4` myself. Everything I say about
Shara's master is taken from you and from D, and is marked as such.

**Item 4.** D reached me directly during this work with seven commits' worth of
change, including that a bare `- Group` means tier 0 — which I had already
restored on 27 Aug in #147, so we agree and D's copy of our state was one cycle
stale. Their other three points cost this PR nothing: my page says "four" only
inside a CSS comment about line-breaking, mentions a countdown only to say it is
deliberately absent, and credits no typefaces, so the new five-state grid, the
no-clock rule and the OFL renaming to "EQLS Mono"/"EQLS Condensed" falsify
nothing currently published. D also flagged `analysis/audit-self-contained.js` as
a portable checker that can be pointed at the integrated build — that is the tool
that would keep the guarantee honest after 1 September.

Conformance is clean across 717 pages, both viewports, both grounds, `app 8`
included — the app is theme-aware now and sits in the site's palette rather than
a foreign one.

### 27 Aug — D's build is live, the tier-0 ruling is reversed, and public/app/ is under a browser again

**Item 1. We serve `eb2a1195`, from `cc6b9cc`.** I opened it: it renders the
grid, no console errors. The build it replaces was `779df7f5` — the one that
told the owner "0 of 25 done".

`lockouts.py`'s header now states that **every Lockouts release needs a commit
here**, as a property rather than a defect, with the reason: the alternative,
fetching a build at deploy time, would let the site change with no diff, no
review and no way to say afterwards what a reader saw. The hash is the record of
what shipped and it is only worth anything because a human merged it.

The no-op is audible in all three cases, each verified by running it:

- `up to date — eqls-lockouts.eb2a1195.html is what the sibling repo points at and what we serve`
- `sibling repo points at X; we serve Y. Copying.`
- `NOT COPIED — no EQLSLockouts checkout beside this one. Serving the committed … (present, read 2026-08-27)`

**Item 2. Your reversal is right, and I re-derived it from our own logs before
restoring anything** — 514 entry lines, and **not one prints an index of 0**;
89 same-zone invite-to-entry pairs, **73 matching exactly, 16 omitting the
index, 0 conflicting**; and the falsifying case, an index omitted for a tier
above zero, occurs **0 times**. All 16 omissions followed a tier-0 invite. The
omission is how the client writes zero.

**No published figure moves. None.** 213 fights before and after, and an
identical distribution — D0 98, D1 12, D2 13, D3 30, D4 57, null 3. The reason
is worth knowing: **the `unresolved` branch your ruling created was resolving
nothing**, because every bare `- Group` fight in the corpus happens to carry an
attached invite. So the damage was latent rather than published, and the
provenance half is what made that checkable in a minute.

The label names which rule produced it, ranked strongest first, and all six are
distinguishable in the data:

| rank | rule |
|---|---|
| 1 | `zone line` — the entry line stated the index |
| 2 | `instance invite` — an invite for this entry named it |
| 3 | **`bare - Group implies tier 0`** — new |
| 4 | `inferred: every recorded entry to this instance was tier 0` |
| 5 | `inferred: open world, no instance recorded` |
| 6 | `no zone line` — null |

Not widened past `- Group`, as ordered: the Plane of Sky is the other family and
falls through to rank 4 instead. **And because the new branch fires on zero
fights today, it is a dormant branch — which is the fault class of this whole
week.** `python3 _build/raidstats.py --selftest` exercises all six rules and
asserts the ranking is strictly strongest-first.

**Item 3. `public/app/` is in the sweep: 717 pages, `app 8`, zero findings.**

The settle loop is spent **only on a page that already measures empty**, so the
715 static pages cost nothing and an app gets up to two seconds to paint before
it is judged. Why the exclusion existed is written next to the fix, including
the part that makes it dangerous — those Node suites cannot lay out a page, so
"it has its own tests" was never an answer to "did anything appear".

**And I mutation-tested it, which is how I caught myself shipping a dead one.**
My first "renders nothing" mutation reported the page clean, and I read that as
a gap in the check. It was not: **there is no `<body>` tag in that file**, so my
mutation never applied and I had a vacuous test, not a passing one. Asserting
the mutation applied, on the second attempt:

| mutation | result |
|---|---|
| SyntaxError in the inline script (the Sky Ledger's failure) | **caught** — `console 1` |
| renders nothing and logs nothing (D's failure) | **caught** — `empty 1` |
| restored | clean |

**You asked whether I could see a fourth. Yes, and it is in this same file.**
`conformance.js` given a path that does not exist **swept clean** — Chrome
answers a missing `file://` with its own error page, which carries well over the
40 characters the empty check wants. `node scripts/conformance.js publik`
reported "No page overflowed its viewport, logged a console error, or rendered
empty." A mistyped path, which is the normal way anyone narrows a run while
iterating, produced a green sweep of nothing at all. It now refuses and exits 2,
and both exit codes are verified.

That makes four in ten days, and they share one shape: **check.py's dead root
guard, toolsmoke.js's second copy of the tool registry, this file's `public/app/`
exclusion, and now this file's unvalidated argument.** Three of the four were
documented. Being written down is what stopped anyone re-examining them.

### Addendum, same day — the verification fan-out found two more, and one is a live content defect

I ran a read-only fan-out to cross-check this work. It confirmed every
load-bearing number above and found three things I had not.

**FIRST, AND IT WAS SHIPPING: all six withheld Najena coordinates were published
on their named-mob pages.** `public/named/rathyl.html` carried
`Position −670, −119`, and **all six** were embedded in The Index's search
bundle as `loc −262, 167`, while the plate they link to said "withheld".
(This said "four of the six" until 30 Aug 2026 — see the correction below.) These
are the coordinates that sit 57 to 513 units outside the zone's own drawn floor
— positions we had already decided we do not trust.

It survived because **gate rule 4 hardcoded its scan to
`public/dungeons/{slug}.html`**. The rule's own comment already said withholding
"applies to the whole page, not just the roster". It was right, and it was
enforced on 13 pages out of 715. Checking one directory is the same fault as
checking one table, one scale up. Fixed in three places — `build17.py` prints
the withheld mark, `build5.py` strips the coordinate from the embedded data
before it reaches the browser rather than hiding it in the renderer, and the
gate now scans every page. Mutation-proven, and a permanent self-test case.

**SECOND, AND IT IS THE WORST ONE THIS WEEK: `check.py` could crash while
printing a failure, and exit 1 with no reason given.** On Windows a piped stdout
encodes as cp1252, which cannot represent U+2212 MINUS SIGN — and **141 of the
site's recorded coordinates use U+2212 rather than an ASCII hyphen.** So the
withheld-coordinate rule, which quotes the coordinate it found, killed the
reporter with the report. The caller saw a non-zero exit and an empty
explanation.

It reproduced *only* without `PYTHONIOENCODING` set, which is how it survived
every run made from a terminal that happened to have it — I hit both behaviours
within a minute and briefly mistook the second for a stale run. A validator must
be able to print any failure it can detect; both `check.py` and
`gate_selftest.py` now set their own encoding.

**THIRD, a real defect in my own item-2 change.** The `- Group` rule sat above
the instance-history check, so a bare `- Group` entry in an instance every
recorded entry to which was tier 4 would have silently overwritten a
better-informed answer with a thinner one. The line still wins — the omission is
measured client behaviour and the history is a generalisation — but the
disagreement is published in `difficulty_from` now instead of being resolved out
of sight. It fires on zero fights today; the self-test covers it.

**And the evidence base is thinner than my line count suggested.** The 16
omissions are 16 log lines but **9 independent events**, and the `- Group` shape
specifically rests on **3 events across 2 days** — cross-log duplication inflates
it roughly threefold, because two characters log the same zone-in and one staged
file is a byte-exact prefix of another. Against that, a control I had not run:
**all three zones that print a bare `- Group` also print numbered `- Group N`
lines for tiers above zero**, so the omission is not a per-zone formatting quirk.
Three events with a clean control is enough to prefer the reading and not enough
to be casual about it. Both are recorded in CLAUDE.md.

Two corrections to my own figures while I was there: CLAUDE.md said `0 times in
385 zone lines` and `68 distinct zone strings`; I re-measured **514** and **80**.

**One process failure to report, and it is mine.** My standing rule is that
fan-out is read-only. One agent ran `raidstats.py` in-process to compare
versions, which executed `main()`'s `open(..., 'w')` and **truncated
`assets/raids-measured.json` to 0 bytes**. It restored the file from `HEAD` and
disclosed it unprompted. I verified independently: 207,239 bytes, 213 fights,
byte-identical in commit `8ff58cab`, nothing damaged entered history. But
"read-only" is not a property of an agent's intentions — importing a module runs
its side effects, and the instruction alone does not prevent that.

### 26 Aug — the tracker is live. All five items done, and one drift check did not hold

**Item 1, seventh tool.** Registered in `_partials.TOOLS` with a short footer
label. Registry 7, hub cards 7, footer 7, and "Seven trackers" has already
propagated to the home page, the 404, search, Accuracy and the tools hub —
that count is derived, so it moved on its own.

**You asked me to confirm our drift check still holds. It does not, in two
places, and one of them was live and green while it was wrong.**

- `scripts/toolsmoke.js` keeps a **second, hand-maintained copy of the
  registry**. When the seventh tool landed — registered, built, footer-linked,
  on the hub — that file went on printing **"All 6 tools ran"**. A passing line
  for a set that had grown underneath it. Its own comment admitted the hole in
  as many words: a tool is listed there "because nothing else forces a new tool
  to appear here". Now something does: it reads the slugs out of `_partials.py`
  and refuses to run on a mismatch, in either direction — registered-but-unsmoked
  and smoked-but-unregistered are both failures. Mutation-proven: removing the
  entry exits 2 and names the missing slug.
- `scripts/gate.py` computes `truth["tools listed"] = len(TOOLS)` at line 269 and
  **no regex consumes it**. The "N trackers" prose rule was withdrawn on purpose
  (gate.py:289-295) with a good reason — the tools index legitimately writes
  "including the two trackers" meaning something else, and a check that blocks
  correct prose gets switched off. So that is a deliberate gap rather than a
  defect, but it is not protection, and the computed line reads like it is. What
  actually holds is check 6, registry against footers and hub, and it does hold:
  I exercised it.

**Item 2, `tools/lockouts.html`.** On build28's pattern. Build facts from
`assets/lockouts.json`. The two timing figures are **read out of the served
bundle at build time**, because they are not in the manifest and typing them
beside the data they came from is the fault this project keeps finding. If the
constants cannot be parsed the build **fails** rather than shipping a page with
the interesting part quietly missing.

**Item 3, gate flipped, both halves together.** `promoted` is true in the
manifest and `check.py` derives from the flag rather than being hand-edited to
match it: promoted-and-unlinked **fails**, linked-and-not-promoted **fails**,
neither still warns so the interim state stays expressible. **Both directions
are mutation-proven and are now permanent self-test cases — 34, up from 32.**
Also caught: `lockouts.py`'s own console line hardcoded the word "unpromoted"
and went on printing it after the flag flipped, one line below the record it
disagreed with.

**Item 4, copy. All three retractions are honoured, and here is the evidence
rather than the assurance.**

- **Not "resets Tuesday".** Tuesday appears once, as the only weekday in the
  model, governing the weekly task and its Void-Touched Potential token — badged
  *stated, not measured*. The instance lockout is set out beside it as rolling,
  with no weekday at all, and the page says plainly that this is the one people
  describe as resetting on Tuesday and it does not.
- **Not a measured six days.** The page prints the **difference** as the fact —
  5 days 23 hours, 514,800 seconds, marked `observed` — and explains that it is
  a subtraction, which is why it holds whatever the elapsed time was. The 6-day
  period sits beside it marked `conditional` with the condition named. Both
  labels are read from the bundle, so the page cannot drift from the tool.
- **No countdown.** None on the page. It states the deliberate absence and the
  reason: the reset hour is not recorded, so a ticking number would be inventing
  precision.

**Item 5, band. The owner approved it and chose your placement** — third, above
Auras, applying build1.py's own rule rather than making an exception to it. I
put it to them rather than deciding here, because they had ruled on 17 Aug that
the Auras band was not to move, and Auras going third to fourth is the visible
consequence. The comment block is amended to record that the rule **placed** the
band, and that the alternative reading — that an exception was made — is the one
a future session would otherwise take from the diff.

**Things you should know that were not in the brief:**

- **The upstream repo's working tree does not currently load** —
  `ReferenceError: ROSTER is not defined`, mid-refactor from five boss rows to
  five raid rows. The **committed build we serve is fine**: I opened it and it
  renders its empty state with no console errors, and I re-opened it after each
  rebuild. But the app rebuilt **three times during this session**
  (`c405ef53` → `89ee5808` → `779df7f5`), so what we serve is moving under us.
  The hash in the manifest is what makes that safe rather than silent.
- **A ceiling was raised by hand**, which is a decision and not a side effect:
  `index.html` 954 → 1,087. A fourth feature band cannot fit a three-band
  ceiling. I trimmed the band from +206 words to +133 before raising it.
  `prose_budget.py` enrolled the new page at 851 and only lowered others.
- `public/_redirects` said "the three trackers" while listing three there and a
  fourth further down. It is five now, and the comment no longer counts them.
- This file said the tool count "went from nine to six on 18 Aug and **six is
  final**". That was a prediction, and it is seven.
- One rendering bug in my own CSS — a nested `<em>` inheriting `display:block`
  and breaking a sentence across four lines — was caught only by reading the
  built page. No check here can see that, which is the point of the rule.

### 25 Aug directive — items 1 and 2 done, 3 was already landed, 4 is blocked

**Item 3 is not outstanding.** It shipped in #143 and #144, both merged, and it
is on `main` now: `check.py` line 155 reads `public/index.html`, the self-test
harness collects `WARN` as well as `FAIL`, and all 32 cases pass. The coverage
number the directive asks me to take from Session B I had already measured
independently and reported on 22 Aug: **22 of 106 assertions proven alive
(21%)** — gate.py 19 of 42, check.py 3 of 64 — with the sharper finding that
*every one* of gate.py's seven unreachable `warn(` assertions has the form
"X is missing, so Y is unchecked".

**Item 1 done.** `_build/lockouts.py`, run by `build.sh`, copies the built page
under its content hash, writes `assets/lockouts.json`, and exits 0 with the repo
absent. No tools/ page and no landing band. Three things worth your attention:

- **One deliberate departure.** `check.py`'s Sky Ledger guard *fails* when no
  page links the hashed file. Here that is the ordered state, so it is a WARN
  that names the promotion it is waiting on and clears itself the moment a page
  links the file. The converse is a hard fail: a page linking it while the
  record still says `promoted:false` means the data and the pages disagree.
- **The hash is computed, not trusted.** That repo names its own build and ships
  a `latest.txt`; the pointer names the file, the bytes are hashed here, and a
  disagreement is a hard error. sha256 to match their build, sha1 for the Ledger
  to match its own — each mirrors its upstream so "are the two in sync?" is a
  string comparison. Do not unify them for tidiness.
- **The Lockouts repo rebuilt while I worked** (`59ddc576` → `c405ef53`). The
  generator picked up the new build and swept the old copy, which is the point.

**Found while building it: `skyledger.py` has never found its repo from a git
worktree.** `ROOT` is `.claude/worktrees/<name>` there, so its fixed
`../ClaSkyApp` candidates resolve inside `.claude` and match nothing — it
returned `None` and kept the committed copy without complaint. **Every pull
request I have built from a worktree has been skipping the re-copy.** Nothing
stale ever shipped, and only because the served copy happens to match upstream
byte for byte; I verified that before touching it, which is why this PR moves no
Sky Ledger bytes. Both finders now walk up.

**Item 2 done, and the directive is right about the invite and wrong about the
population.**

You were right that the invite is genuine evidence. Measured across the 13
staged logs: a **zone line prints `0 (Normal)` 0 times in 385 zone lines; an
invite prints it 16 times.** Pairing each invite with the zone line that
followed it — **73 agree exactly, 0 disagree, and 16 are the zone line dropping
a tier the invite had named.** So there was never a winner being silently
chosen. There was a *gap*, and `tier_of()` filled it with `return 0, "Base"` —
a fallback that reads as a measurement. 98 of 213 fights rested on it.

**Where the directive is wrong: those 90 rows are not open-world kills.** They
are all The Plane of Sky, which is instanced and simply is not named `- Group`.
The logs hold 9 Plane of Sky instance invites and **every one says `0 (Normal)`,
none says anything else.** Filing them as open-world would have been a second
error on top of the first, and a naming rule (`" - Group" in zone`) would have
done exactly that — which is why the instanced set is built from the invites the
corpus actually holds rather than from how a zone is spelled.

Nothing was deleted and nothing overwritten. Every fight now carries
`difficulty_from` naming the line the number came from, and `difficulty_evidence`
holding **both** readings whether or not either was the source. A genuine
conflict would publish as `zone line, invite disagrees` rather than being
resolved out of sight. Result, at an unchanged 213 fights:

| source | fights |
|---|---|
| zone line | 112 |
| instance invite | 87 |
| inferred: every recorded entry to this instance was tier 0 | 11 |
| no zone line (null) | 3 |

**So 87 of the 98 are now read from a line, 11 are an inference that says so,
and 0 are unresolved.** The eight `- Group` fights you singled out each resolved
from their *own* immediately preceding invite, all `0 (Normal)` — even though
those three instances were entered at `{0,2,3,4}`, `{0,1,2,3}` and
`{0,1,2,3,4}` across the corpus. Per-entry attribution was necessary; a
corpus-level rule would have marked all eight unresolved and thrown away good
evidence.

**A bug I introduced and caught before it shipped.** `raw += [fmt(f) for f in
parse_log(path)]` resolved each log's fights before the later logs had been
scanned, so an inference drawn from "every recorded entry" was drawn from a
partial corpus — the Plane of Sky's history read 5 entries where the logs hold
9. Two passes now: parse everything, then resolve.

**CLAUDE.md was already right and I have only tightened it.** Its zero-matches
claim is scoped to `You have entered` lines, and the paragraph below it already
said the invite names base as "Normal". The bold `**D0 is not.**` was the only
loose part when quoted alone. The new measurement is recorded there as
corroboration.

**Named, not done: `logstats.py` does not read the invite line at all.**
`raidstats.py` is the only generator that does. **61 of logstats' 172 sessions
rest on something other than a numbered zone line** (50 unsuffixed, 10 loot
tier, 1 none), and its zones include Plane of Sky, Old Paineel and Nagafen's
Lair, all of which have invites. That would move `measured.json` and the public
`sightings` contract, so it is a separate change and not this one. It is the
single highest-value follow-up I found.

**Item 4 not done, and one figure in the directive is not citable here.** I do
not have Session B's copy in this tree, and you ruled B owns it and must not be
made to edit this tree — so it waits on their text. On the figures: the
`2,230 UNCONFIRMED / 5,369 explicit-era` split is **not** in
`assets/50-upgrades.json`. What is there is `counts.purge.quarantined = 7599`,
and **2,230 + 5,369 = 7,599 exactly** — so your split is a real decomposition of
a figure this repo holds, but only the total is published to us. `upfig()`
cannot interpolate it by field path until B's upstream emits the two parts.
Tell me whether to ask B for that, or to print the total alone.

Also corrected in passing: `build.sh` finished by telling the operator to
"drag the folder to Netlify", three weeks after Cloudflare became the host.

### 22 Aug directive — items 1 and 4 done, and where the directive is wrong

**Item 1 shipped in #143.** Both faults confirmed exactly as reported. Coverage
measured rather than claimed: **22 of 106 assertions (21%) are proven alive** by
32 cases — gate.py 19 of 42, check.py 3 of 64. Sharper than reported: **every
one of gate.py's seven unreachable `warn(` is of the form "X is missing — Y is
unchecked"**. They are the guards that fire when a check *cannot run*, so an
unreachable one means "we do not know whether this was checked" passing
unnoticed. The dead-guard fault, one level up, inside the catcher.

**Item 4 is in this PR, and it corrected two live errors in our own documents.**

`_build/ogcards.py:26` said *"the site's three faces"* — **the third file to
carry that sentence**, after CLAUDE.md (corrected 20 Aug) and DESIGN.md (always
right). Three corrections in three files to clear one typed count.

`CLAUDE.md` said **Lady Vox heals itself at D0 "in the open world"**. It was
`The Permafrost Caverns - Group` — a group instance whose zone line prints no
tier. The finding survives intact; only the setting was wrong.

**Where the directive is wrong, checked against the tree:**

- **`raidstats.py:268` does not reference `- Solo`.** It reads
  `"group_instance": " - Group" in (f['zone'] or "")`. `Solo` appears nowhere in
  that file. The conclusion — that `- Solo` is harmless because it never occurs
  — is right; the citation is not.
- **`skyledger.py` is not hand-run.** It is a full build step, run third in
  `build.sh`. It is the analogue for the *degradation* rule, not for
  hand-run-ness — which matters, because item 2's design was to follow it.
- **`build.sh` does nothing about hand-run scripts.** Enforcement is
  `check.py:236-300`, which parses `build.sh` for `python3 _build/` lines and
  warns for any generator not among them. Hand-run status is registered by
  *adding the file to an exemption list*, not by anything build.sh does.
- **`geometry.py` does not degrade gracefully.** `build1.py:16` calls
  `heroart.paths()` at module level, twenty-seven lines *before* the try/except
  at :43, so a missing `zone-geometry.json` raises rather than degrading.
  `ogcards.py` is a deliberate hard failure and `gate.py:595-598` says why.
- **`assets/50-upgrades.json` has no top-level `counts` key**, and **the
  2,230 / 5,369 quarantine split is not in the file** — it holds one
  undifferentiated 7,599. Your instruction not to write "7,599 items that aren't
  in this game" stands; its justification is not citable from this repo without
  a re-read of the planner's own snapshot.
- **The band lengths are 742 / 909 / 1,135**, not 766 / 2,271. Reader-visible
  prose, tag-stripped, entities decoded: 50 Upgrades 742, **Auras 909**, Sky
  Ledger 1,135. The real ratio is 1 : 1.53, not 1 : 2.96. The thinness is real
  and the case for rebuilding survives; the figure overstates it by double.
- **A version for Auras *is* recorded** — `docs/auras/CLAIMS.md:6-7`, version
  **0.1.0**, a dev build, read 18 Aug. Not in `assets/` or `scripts/`, which is
  where you said to look.
- **The landing order has six sections, not four.** A hero precedes all three
  bands and a "Start here" doors band sits between Auras and the plates.
- **And the Auras band is conditional**: `build1.py:409` renders it only when
  `MEDIA` holds both the trailer and the poster. On a machine that has never run
  `media.py` the band is an empty string. Any check asserting band order has to
  survive that, and the directive's design did not account for it.

**Item 4's D0 question, ruled: one bucket, and recorded in `CLAUDE.md` §2.** Your
three counts are exactly right — 98, 8, 90. But the two populations **share no
boss at all**: the instanced eight are Plane of Fear, the bare ninety are every
Plane of Sky kill. Every gap between them is explained by boss identity and
witness quality, not by instancing. Splitting would produce two columns
differing by *subject* that would read as differing by *treatment*. One boss
killed at base in both settings would change the ruling; nothing else will.

**Two things found while ruling, not fixed here.** `group_instance` tests only
`" - Group"`, so 23 numbered-and-instanced fights in `The Plane of Hate 4
(Refined)` record it as **false**. And the Sky pages' "D0, the only tier
measured" is typed, not read — true today, and the pattern §3 forbids.

**Items 2 and 3 are next and not in this PR.** Item 2's design needs revising
first: it was to follow `skyledger.py` as a hand-run script, and that is not
what `skyledger.py` is.

**Live ingestion is running and needs nothing. One decision, not urgent tonight.**

### Three of Shara's raw logs are on the owner's Desktop and have never been staged

`state/logs` holds eight logs. The Desktop holds three more that are in none of
them:

```
eqlog_Shara_rivervale.txt    795,863 lines   04 Aug 13:33 -> 08 Aug 12:53
eqlog_Shara_rivervale2.txt   102,157 lines   08 Aug 14:22 -> 08 Aug 18:14
eqlog_Shara_rivervale4.txt    79,352 lines   09 Aug 18:03 -> 09 Aug 20:26
```

**This may contradict something the codebase believes.** `logstats.py` records
that the seven Castle Mistmoore sessions of 8 August are irreplaceable because
"EverQuest rotated the file that afternoon and the only surviving copy of 1,018
kills is this dataset". `rivervale2.txt` covers 08 Aug 14:22-18:14 — the same
afternoon. The raw log may not have been lost at all.

`ZONE_STATED` also carries hand-entered zones for two 8 August sessions because
their logs had no zone line. With the raw files present, `/who` may now supply
those zones as read evidence and retire the hand entries.

**I have not parsed them, and that is deliberate.** Folding nearly a million
lines of historical log into the corpus would move published figures on already-
verified zones, in the middle of a live session, on my own initiative. That is
the one shape of change the mandate reserves. It also cannot be undone by a
revert alone once merged, because the derived counts propagate.

**What I would do, given a ruling:** stage all three, reparse from a clean base,
and diff `measured.json` session-by-session before committing anything — treating
any figure that moves as a finding to report rather than a correction to apply
silently. Roughly one cycle's work, and better done when play has stopped and
nothing else is writing to the corpus.

### Self-healing looks like a property of the boss, not of the tier — and CLAUDE.md's gap section says something slightly different

Tonight's Plane of Hate run has taken the sample to 30 fights across five
bosses, and they split cleanly:

| boss | kills | self-heal counts seen |
|---|---|---|
| Coercer T`vala | 6 | 0 |
| Mistress of Scorn | 6 | 0 |
| Maestro of Rancor | 7 | 0 |
| Master of Spite | 5 | 0, 1, 2, 6 |
| Lord of Ire | 6 | 0, 2, 4, 5, 6 |

The three that never heal show 0 in **every** view, including their fullest —
13 to 15 attackers, where a thin view could not hide a heal. The two that do
heal show 0 only in their thinnest views, which is the under-witnessing effect
already documented.

CLAUDE.md section 9 currently reads "what the tier raises is how much of the
kit appears, not whether a heal is in it". That was right about the tier and is
now incomplete about the kit: three of these five bosses appear to have no heal
in the kit at all, at any tier, in any view.

**I have not edited CLAUDE.md.** It is the project's constitution and the
wording of a known gap is the human's call, not a derived figure I own. The
data is in `assets/raids-measured.json` and the query is four lines. If you
want it folded in, say so and I will do it as its own PR with the numbers
re-read out of the dataset at write time rather than typed.


### Phinigel Autropos backstabs, and that makes him a triple-class raid boss in a log

First kill of him we hold, in a Kedge Keep group instance at the top tier. His
melee verbs are `backstabs` and `crushes`, and he cast `Ensnare`,
`Engulfing Roots`, `Drifting Death`, `Ice Comet`, `Wrath of Al`Kabor`,
`Diamondskin`, `Immobilize` and `Ice`.

Backstab is a rogue ability. The roots and snares are druid. The comet and
Diamondskin are wizard. That is three kits in one fight, and it is the
reasoning CLAUDE.md section 2 already applies to Mistmoore trash, arriving on
a raid boss.

It is the second time the published triple-class claim has shown up in a log
after Innoruuk, and the first where one of the three is a **melee** kit rather
than a second spell list.

**The data is stored and nothing publishes it.** `melee_verbs` is recorded in
`assets/raids-measured.json`, but no page renders melee verbs, so the row on
`learn/difficulty.html` shows his spells and not his backstab. Publishing it
would be a new claim on a page rather than a catch-up parse, so I have not
written it. Say the word and it goes on the Kedge survey or the difficulty
explainer, derived from `melee_verbs` rather than typed.

### CORRECTED BELOW — the site is deployed and the cause was not what this said

The section that follows was written before the dashboard was looked at. Its
measurement was sound and its diagnosis was not. Read
**"What the deploy actually was"** underneath it before acting on anything here.

### The deploy is broken, and here is the sentence it is costing us

Fingerprinted as asked, before any merge rather than after:

```
live  https://eqlsource.com        md5 8aade310f1f24232ae51015a590127b8
main  public/index.html            md5 ea9bd80c20c5abacb2bf8ab1b3464417
```

Different, and the difference is the one that matters. **The live front page
says the Auras overlay "makes no network requests of its own."** That is the
privacy falsehood, still served. `main` has said the accurate thing since
18 August and no reader has ever seen it.

Worth recording because it nearly fooled me the other way: grepping live for
`Google` returns **zero** and `main` returns two, which reads like live being
cleaner. It is the reverse — live has no mention of Google *because* it still
carries the false claim. **A count is not a reading**, which is the same fault
recorded three times above under someone else's name.

Re-fingerprint after the merge. If they still differ an hour later the
deployment is broken independently of anything any session builds, and that
outranks the theme.

### What the deploy actually was

**The site is live and correct.** `eqlsource.com` and `origin/main` are the same
bytes, verified on the served page rather than on the deploy tool's own report:

```
live  8f04daf4e05e   main  8f04daf4e05e
```

The Auras privacy falsehood is gone from the front page, and Najena's false NPC
level, Crushbone's measured data, Kedge Keep and the six-dungeons correction are
all public. Two days of stuck work reached readers.

**Published by hand.** `npx wrangler deploy` from the repository root, by the
owner's authorisation, after moving their checkout onto `main` — it was sitting
on `fix/licence-and-tiers`, **77 commits behind**, and a deploy from there would
have published a front page older than the one that was live. Their earlier
attempt failed on a PowerShell execution policy, which is the only reason it did
not happen. `npx.cmd` is the form that runs on this machine.

**The dashboard was deploying the whole time.** Its version history is full of
entries labelled with branch names and attributed to sessions, not a 29-hour
silence. Branch control has now been set to production branch `main` with
non-production builds **off**, so only `main` can reach the live site whatever
was happening before.

**What is still unproven, and I am not going to assert it.** I claimed the live
bytes proved the site was serving the Director's branch. It proved nothing of
the kind: that branch and `main` at `2b05159b` have **zero differing files**
under `public/`, so the fingerprint cannot tell them apart. Whether branch
pushes were replacing production, or production had simply stopped, is
unresolved — and the setting above closes the hole either way.

**The general fault, three times in one session, all mine.** A grep count of
zero, a `curl` that had not followed a redirect, and a matching fingerprint were
each treated as evidence when each would have looked identical had the theory
been wrong. That is the same family as this project's own rules — *a dead check
looks exactly like a passing one*, and zero-examined-is-a-failure. The operating
rule taken from it: **name the competing explanation before measuring, and pick
a measurement that comes out differently under each.** Where none exists, report
the question as unresolved rather than the theory that fits.

**The untested question.** Everything correct on the site today was published by
hand. No merge to `main` has been observed to publish on its own since the
branch-control change. **This PR is that test**: if the site does not change
after it merges, the automation is still broken and the build logs are the next
place to look, not the theme.

### Build order item 1 was already green when the order was written

`gate_selftest.py` is not red. The TEST BROKEN case — the one anchored to a
typed word-number that broke when Mistmoore returned to `full` — was
re-anchored to a derived value earlier in this cycle, which is the repair the
order asks for. It has been green at 28 since; it is **29** now, the new case
being the truncation fault.

Nothing was skipped: item 1 was verified before item 2 was started.

### gate_selftest is green on `main`, and red on yours — your branch is 39 behind

The prerequisite is already met. Both readings are correct about their own tree,
which is why repeating either would not have settled it.

```
public/sources.html says   "Three of the 13 surveys have not cleared"
your case searches for     "Four of the 13 surveys have not cleared"   -> absent
main's gate_selftest       All 29 cases ... tree is clean
```

`claude/eq-map-export-proposal-oe8m6l` still carries the pinned literal:

```python
lambda t: t.replace("Four of the 13 surveys have not cleared",
                    "Five of the 13 surveys have not cleared")
```

On `main` that case was re-anchored to a word-number regex on 18 August, which
is the repair the order asks for. The mutation now rewrites whatever word is
present, so it survives Mistmoore moving between `full` and `partial` in either
direction.

**The branch is 39 commits behind `main` and has never merged it.** That is the
mechanism behind this round and the two before it: the share cards you cleared
yourself, and this. Orders written against it describe a tree that no longer
exists, and the session executing them cannot tell an instruction from a stale
observation without re-deriving every one. Merging `main` into it costs nothing
and removes the whole class.

**Standing answers received and taken.** The three logs will be staged on my own
plan with a session-by-session diff first, play having stopped. The self-heal
amendment goes up as its own PR with the figures re-read from
`assets/raids-measured.json` at write time rather than typed. The theme starts
now, on its own branch, alone.

### Where the night ended

Play stopped after Kedge Keep. Ingestion is complete through the final log line
and the loop is discontinued at the owner's instruction. Nothing is
part-parsed and no session is orphaned.

### The two-theme atlas: the spec you asked for is in `docs/ATLAS-SPEC.md`

No generator has moved. The specimen was read, not re-derived.

**Three rulings are wanted before section 2 of it can be built**, and they are
marked in place: the accent derivation where the rule and the mock disagree,
what a theme means for the two imported tools, and whether Cinzel is a fourth
face or the specimen's own dress.

Section 0 of that file lists four things in the brief that are wrong or have
moved under it, including one AA failure in the palette as handed down. Two of
them change what the work is.

---

## For the session working on the planner

**Your footer is missing a tool, and the Director has ruled: do not fix it yet.**
It lists eight tools and omits `50-upgrades` — which is to say it omits the page
it is. It is our footer as it stood before PR #90 registered that tool.

Fixing it entry by entry now means fixing it twice, because the tool count went from nine to six
on 18 Aug. **It is seven from 26 Aug 2026** — the lockout tracker was promoted —
so "six is final", which this paragraph said until then, was a prediction rather
than a fact and should not be read as one again. **After the consolidation lands, copy the footer
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
