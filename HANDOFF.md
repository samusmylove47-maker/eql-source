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
