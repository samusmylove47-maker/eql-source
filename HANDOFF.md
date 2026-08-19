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

### Where the night ended

Play stopped after Kedge Keep. Ingestion is complete through the final log line
and the loop is discontinued at the owner's instruction. Nothing is
part-parsed and no session is orphaned.

---

## For the session working on the planner

**Your footer is missing a tool, and the Director has ruled: do not fix it yet.**
It lists eight tools and omits `50-upgrades` — which is to say it omits the page
it is. It is our footer as it stood before PR #90 registered that tool.

Fixing it entry by entry now means fixing it twice, because the tool count went from nine to six
on 18 Aug and six is final. **After the consolidation lands, copy the footer
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
