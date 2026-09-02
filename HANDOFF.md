# Handoff — 1 September 2026

Read `CLAUDE.md` first. This file is the current state and the open work.

**This describes commit `53fd3113`** (PR #181, merged — the tip of `main`). Diff
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

**An order written against a branch that has never merged `main` describes a tree
that no longer exists.** The session executing it cannot tell an instruction from
a stale observation without re-deriving every claim, which costs more than the
order saved. Merge `main` into the branch first: it costs nothing and removes the
whole class.

---

## Every figure here is a command, not a number

A remembered figure survives a session boundary as a fact. A command survives as
a fact-checker. Nothing in this file SHOULD state a count you cannot regenerate,
because the counts move and this file will not.

**Stated as a fact this was false, and an audit on 1 Sep 2026 measured how
false.** The file carried bare figures with no command beside them, and four had
already drifted: 717 pages referencing `assets/site.css` when it was 718,
`.nav-find` on 700 pages when it was 702, "36 self-test cases" when there are 48,
and `conformance.js` at "86 seconds" when it now takes 238. Every one was true
when it was typed, which is the whole problem: a figure is only as good as the
command beside it, and a figure without one has no way to announce that its
moment has passed.

So read the sentence as the intention it always was, and put the command beside
any number you add.

**And its companion, which cost more: A COUNT IS NOT A READING.** Grepping the
live site for `Google` returned zero and `main` returned two, which reads as live
being the cleaner of the pair. The truth was the reverse &mdash; live had no
mention of Google precisely *because* it still carried the false claim that the
overlay makes no network requests. A zero can be produced by the absent text
having been replaced by worse text, so a count in either direction is not a
reading of what a page says. Read the match.

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
| Whether the committed output is what a fresh build produces | `python3 scripts/freshness.py` &mdash; the one fault `check.py` structurally cannot see, because it runs after the build |
| Every prose ceiling | `assets/prose-budget.json` — and `scripts/gate.py`'s `page_words` is the only correct way to measure against it |
| A page's current weight | `python3 -c "import sys;sys.path.insert(0,'scripts');from gate import page_words;print(page_words('public/index.html','index.html'))"` |
| The planner's catalogue counts | `assets/50-upgrades.json` → `figures`, **keyed by the dotted path each figure was read from** in the planner's `meta.json`. `counts.items` is the catalogue; `counts.purge.shipped` is what survived the era purge. They are not the same quantity and were equal until 18 Aug 2026 |
| When the planner snapshot was read | `assets/50-upgrades.json` → `read` — the day a person stood behind it, not the day a script ran |
| How to refresh that snapshot | `node scripts/refresh-upgrades.mjs <YYYY-MM-DD>`. Hand-run, needs network, never in `build.sh`. Never hand-edit a figure |
| Which zones are revamped | `assets/zones-index.json` → any zone with `revamped` |
| How many zones have cleared every gate | `python3 -c "import json,collections;print(collections.Counter(z['verify_level'] for z in json.load(open('assets/zones-index.json',encoding='utf-8'))))"` |
| Which pages lack the shared footer | `grep -rL site-foot --include='*.html' --exclude-dir=app public/` — the imported pages, and nothing else. Do **not** use `public/**/*.html`: with globstar off it silently skips the six root pages |
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
| ~~A home-page feature band for 50 Upgrades~~ **THIS ROW WAS WRONG** | The band exists and has for some time — `_build/build1.py` renders it, and it reads **EQLS Upgrades** since 1 Sep 2026. A row in this table telling a session not to build a thing the site already ships is worse than no row: it reads as a decision and it is a stale note. Corrected rather than deleted, because the reasoning under it — that `index.html` has a prose ceiling and a band costs ~190 words — is still true and is why any *further* band needs the ceiling raised by hand. |
| Withdrawing any existing tool | Nothing currently duplicates anything. The Sky Ledger withdrawal on 17 Aug was justified by a correctness property ours lacked; absent that, two tools are two tools. |
| A shared `.btn` class | The imported pages carry their own stylesheets and never load `site.css`. A shared button would have to be injected into every one of them, and each already styles its own. Count them, never quote a number: `grep -rL site-foot --include='*.html' --exclude-dir=app public/`. Real, and post-launch. |
| The doubled `cache-control` header | Real, harmless, post-launch. |
| ~~Migrating every internal href to the extensionless form~~ **DONE 1 Sep 2026** | All internal page links are extensionless &mdash; 33,732 of 33,736 on 1 Sep 2026, the four being the hashed app bundles; the 4 that are not are the hashed app bundles, which have no extensionless form. The 29 `_redirects` targets went with them. **The `.html` files are untouched on disk and the 307 stays**, so every URL already in the wild still works &mdash; measured, 0 previously-published addresses lost, and an independent sweep of 35,848 links found 0 unserved. **The local cost, found and then fixed:** `python -m http.server` does no extension guessing, so 23,140 of 35,848 links (64%) 404ed on the configured preview server while every one worked in production. `scripts/serve.py` performs the same mapping the host does and `.claude/launch.json` runs it; measured after, every link shape resolves and an unknown path serves the site's own 404. **Raw `file://` browsing still cannot navigate** and nothing can fix that &mdash; `conformance.js` is unaffected, since it opens each page by path and never follows a link. |
| ~~Self-hosting the site's fonts~~ **THIS ROW WAS WRONG** | Done 30 Aug 2026: 26 committed `.woff2` files under `public/assets/fonts/` and zero `googleapis` references in any page. The third row in this table found telling sessions not to build a thing the site already ships. It also killed the stated reason for `conformance.js` never judging type &mdash; see CLAUDE.md section 5. |
| Removing `.nav-find`, or the other 39 undefined class names | 40 class names are used in built pages and defined in no stylesheet. `.nav-find` is the loudest: emitted once in `_build/_partials.py`, riding 702 pages, defined nowhere in `site.css`, read by no JavaScript. Dead and harmless, and removing it is a 700-file diff that re-hashes `CSS_V` for nothing. Left deliberately, and written down so the next sweep does not rediscover it as a defect. |
| The map export | Post-launch. |
| Editing `public/assets/site.css` casually | It re-hashes `CSS_V` and rewrites the stylesheet line on every page. Fine when the CSS genuinely changed; never as a side effect. |
| Running `scripts/prose_budget.py` to fix a page that is over | It only lowers ceilings. A page over its cap is trimmed, or the ceiling is raised **by hand with the reason in the commit** — `CLAUDE.md` §5, precedent in PR #89. |

---

## Why conformance.js is hand-run, and what its silence means

Settled 18 Aug 2026. Recorded here rather than decided again by the next session
that notices it is not wired into anything.

**It stays hand-run. It does not go inside `check.py`.** Three reasons, in order
of weight:

1. **238 seconds against 7.7** (86 against 2.3 when this was written). `check.py` runs before every commit and is
   currently fast enough that nobody weighs whether to run it. Folding in the
   sweep makes it roughly thirty times slower, and the first thing that happens
   to a slow pre-commit check is that people stop running it. A check that is
   skipped catches nothing, so this would trade a live fast check for a
   thorough one nobody runs.
2. **It needs a browser, and a rebuild may not assume one.** Same rule that
   keeps `geometry.py` out of `build.sh` because it needs the game install, and
   `ogcards.py` out because it needs Pillow. A machine with a clean checkout and
   no Chrome must still be able to build and validate this site.
3. **It measures something that changes rarely.** Layout breaks when the chrome,
   the stylesheet or a template changes — not when a survey gains a paragraph.
   Wiring it to every commit spends about four minutes re-proving an unchanged layout
   hundreds of times over.

The counter-argument is real and worth stating: `toolsmoke.js` **is** called by
`check.py`, and it is also a node script that can be absent. The difference is
0.09 seconds against 238 - nearly four orders of magnitude, not a difference of
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
stops there. Ruled 18 Aug 2026 with the owner's authority delegated. **(The registry holds eight today: `gap-engine` and `lockouts` were added afterwards, so the ruling was honoured - no further tool was deleted - and the count rose by addition.)**

PR 2 removed the character sheet, the planar gear tool and the inventory reader,
and it was right for one reason: **EQLS Upgrades already did all three jobs,
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
  `combo-calculator` and `race-unlocks` eleven each **(this said nine, and it was already eleven at the commit it was written against &mdash; the count missed two comma-continued declarations)**, `faction-impact` two — and
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

## Where the measured corpus stops

**The live-ingestion loop is not running, and it did not lapse — it was
discontinued at the owner's instruction.** Nothing else in the repo says so, and
a session finding no loop would reasonably assume it had broken.

`state/logs/` holds 13 staged logs and the last is dated **19 August 2026**, so
that is where every measured figure on this site terminates. Ingestion ran
through the final log line of that corpus: nothing is part-parsed and no session
is orphaned, which is the guarantee a future ingesting session needs before
adding to it. Re-derive rather than trusting this: `ls state/logs/` against
`assets/measured.json`.

Logs later than that exist and are unstaged. What is outstanding about them is
in the exchange below, because it is awaiting a ruling rather than settled.

---

## To the Director

> **PRUNED 1 September 2026, on the Director's ruling, per this file's own rule:
> an applied ruling moves into a standing section and is deleted from the
> exchange.** It had never once been executed &mdash; the section grew from 1
> entry to 20 across 24 commits and no commit ever removed one, so it had reached
> 1,118 lines, 83% of the file, almost all of it finished work written in the
> present tense.
>
> **17 entries went; 3 remain because they are genuinely open.** Nothing was
> discarded on the way: every entry was checked for facts recorded nowhere else,
> 25 were found, and each was relocated first &mdash; the deploy procedure and the
> read-only-import trap to `CLAUDE.md`, Phinigel's triple-class kit to section 9,
> the dead `truth["tools listed"]` to `gate.py`, the missing `<body>` to
> `conformance.js`, the unguarded `heroart` call to `build1.py`, and the rest to
> the standing sections above and `docs/BACKLOG.md`. One was not a relocation at
> all: `raidstats.py` still said 385 zone lines where four other files said 514.
>
> git holds every version regardless. What is below is what is still live.


### 31 Aug — Part 2: three proposals I would defend

Each carries what it costs, what would show it wrong, and whether it needs anyone
else. Ranked.

**1. Make `gate_selftest.py` round-trip bytes rather than text.**
*Cost:* small — read `rb`, write `wb`, and decode only for the mutation, which
means each case's lambda takes and returns `str` as now. Perhaps thirty lines.
*What would show it wrong:* if no case ever needs to touch a byte-sensitive
artifact, the change buys nothing and adds a decode step to forty cases. I think
that is already false — the served bundles are exactly what a bundle contract
needs proving against, and I had to delete a case tonight because of this.
*Needs anyone else:* no.

**2. A check that a class used by a `head()`-generated page is defined in
`site.css`.** Not all 40 — the specific, checkable subset: a class that appears
in a page loading the shared stylesheet and is defined only inside
`build3.py`'s injected block. That is the exact shape of both faults I shipped
this week, and it is mechanically detectable.
*Cost:* small, and it reuses the measurement I already wrote tonight.
*What would show it wrong:* if the false-positive rate is not near zero. Today
the intersection is two classes, both now fixed, so it would currently pass
clean — which is either evidence it is tight or evidence it is vacuous, and I
would want the matched pair before trusting it.
*Needs anyone else:* no.

**3. A check that a vendored file still matches its upstream, where the upstream
is reachable.** Finding 8 is currently uncovered: nothing tells us
`assets/gap-engine.json` has drifted from E's tree, and I found out because E
published a commit subject about it.
*Cost:* medium, and it is the one with a real objection: it needs the network, so
it belongs with `fetchfonts.py` and `geometry.py` as hand-run, and a hand-run
check is one nobody runs. A weaker version that costs nothing: record the
upstream sha in the vendored file's own metadata, so a human comparing takes ten
seconds rather than a diff.
*What would show it wrong:* if the weak version is enough, the strong version is
waste. I would ship the weak one first and see whether anyone ever uses it.
*Needs anyone else:* E, B and D would each have to keep a sha in a file I read.
**That is a request across a seam, so it is a proposal and not a decision.**


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


## For the session working on the planner

**Your footer is missing a tool, and the Director has ruled: do not fix it yet.**
It lists eight tools and omits `50-upgrades` — which is to say it omits the page
it is. It is our footer as it stood before PR #90 registered that tool.

Fixing it entry by entry now means fixing it twice, because the tool count went from nine to six
on 18 Aug. **It is eight from 30 Aug 2026** — the gap engine was registered — (it was seven from 26 Aug; this paragraph's count has now gone stale three times, which is the argument the paragraph is making) —
so "six is final", which this paragraph said until then, was a prediction rather
than a fact and should not be read as one again. **After the consolidation lands, copy the footer
once from the final state and add the drift check** — the same shape you already
built for the nav. A hand-copied footer drifts silently, which is the argument
that put `len(TOOLS)` behind ours and `gate.py` rule 6 in front of it; rule 6
cannot see your copy.

**Your outbound links are already correct** and this closed a hold on our side:
all 42 are absolute and extensionless, none end `.html`. Both forms resolve —
`/x.html` 307s to `/x` - so nothing was ever broken. **The prohibition is now STRONGER, not lifted:** the 307 is Cloudflare's default `html_handling`, the only lever would 404 all 716 sitemap URLs at once, and `wrangler.jsonc` carries that ruling in capitals beside the key. Internal links went extensionless on 1 Sep 2026 instead, so no internal click touches the redirect at all. What follows was written before that and is superseded: the prohibition on our
touching that redirect is now lifted.

Two more facts you cannot see from that repository:

**The Mistmoore revamp date is data, not code.** It lives in
`assets/zones-index.json` as `revamped` and `revamped_note` on the mistmoore
entry, and both `_build/build9.py` (the survey's measured section) and
`_build/build11.py` (the difficulty explainer) read it. When post-revamp logs
land, the ingestion path is a data edit and a rebuild — no generator changes.

**The licence correction is ours too. DONE 18 Aug 2026** &mdash; `sources.html` records the withdrawal, and the planner snapshot carries no `license` field at all. Kept for the reasoning, which still governs any future licence claim. `eqlwiki.com` publishes no content
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
