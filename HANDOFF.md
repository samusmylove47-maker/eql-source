# Handoff — 18 August 2026

Read `CLAUDE.md` first. This file is the current state and the open work.

**This describes commit `2d48a729`** (PR #102, merged — the tip of `main`). Diff
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

## The back channel — how sessions and the Director talk without the owner

**Binding on every session. Re-established 18 Aug 2026 after it broke.**

The owner is not a message bus. On 18 August the Director wrote rulings into
chat and a session asked its questions in chat, so every exchange went through
the owner as copy-paste — the exact thing this protocol exists to prevent. It
broke because the sessions run in different places (one on the owner's Windows
machine with the game and the logs, the Director in a remote container) and
**the git remote is the only thing all of them can see.** So the remote is the
channel, and nothing else is.

**The rules, in order of how often they are broken:**

1. **Never ask the Director a question in chat.** Write it under
   `## To the Director`, commit, push. A question that is not pushed does not
   reach anyone, because the Director cannot see your terminal.
2. **Never wait for a merge to read each other.** A branch is readable the
   moment it is pushed:
   ```
   git fetch origin <branch> && git show FETCH_HEAD:HANDOFF.md
   ```
   Merging is how work *publishes*, not how it is *communicated*. The Director's
   rulings live on `claude/eq-map-export-proposal-oe8m6l` and are readable there
   before the owner merges anything.
3. **One long-lived branch and one pull request per workstream**, updated as the
   work grows rather than a new PR per increment. The owner merges on their own
   cadence, roughly hourly. A PR that is still open is not a PR that is stuck.
4. **Push before you go idle.** If you are blocked, push the blocker under
   `## To the Director` first. Ending a turn with an unpushed question stalls
   the whole chain, and the Director has no way to know it happened.
5. **Fetch before you write.** The Director may have pushed a ruling into the
   same file since your last read. Rebase, do not clobber.
6. **Say where a thing is, not what it says.** "Report pushed to
   `<branch>`, `## To the Director`" is a complete message to the owner. Pasting
   the report into chat is the failure this section exists to stop.

**What the owner actually does:** plays the game, generates logs, and merges
pull requests. That is the whole list. Anything that requires them to carry
text between two sessions is a bug in this protocol, and it should be reported
under `## To the Director` like any other bug.

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

*The PR 3 ruling of 18 Aug is applied and retired from this exchange. One line of
it stands and belongs in a standing section, so move it there rather than losing
it: if a successor to the race unlock tracker, the race and primary calculator or
the faction impact checker ever ships, the handling is delete the page, keep the
reason in `TOOLS`, record it in the change log, redirect both address forms, no
tombstone.*

---

### The external audit of 18 August — ruling, and Wave 1

An outside session with no prior context audited the live site and returned 34
findings. The owner has read it and delegated the triage. **I checked every
actionable finding against `origin/main` @ `5ee3cd3b` myself rather than against
the auditor's rendered reading**, so what follows is verified state, not a relayed
claim. Where I name a file and line, I read it.

Ruled 18 Aug 2026 with the owner's authority delegated. **The owner has approved
this plan.**

**The verdict is fair and the diagnosis is right.** One defect class produces most
of the list: *authored prose asserting what generated data does not support.* We
have named that fault twice in our own change log. It has now reached the tier-1
citation under our most-repeated claim.

**The audit's best contribution is not a finding.** It is the "gate that should
have caught it" column. Nine findings collapse into four cheap gates. Build the
gates, not just the fixes — a fix without a gate is the same bug scheduled for
later.

#### The one structural cause, under three of the five criticals

**We hold no stored copy of any tier-1 source.** Every patch note on this site
exists only as prose typed inside a generator. The eleven-zone placeholder
quotation is a hand-typed string at `_build/build13.py:303-306`, and
`placeholders_removed` is a hand-set boolean in `assets/zones-index.json` beside
it. Nothing connects them.

That single absence produces all three: a quotation can drift and nothing can tell
(F-01); a bullet inside a note we have "already read" is never adjudicated (F-05);
nothing queues what a new note touches (F-03). **Fix it once as an artefact store,
not three times as prose.** `sources/raw/<yyyy-mm-dd>-<slug>.txt` holding each
fetched note verbatim, and `sources/notes.jsonl` — one row per bullet with date,
URL, raw text and extracted entities. Then `placeholders_removed` is *derived*,
exactly as `verified` was derived on the Sky tracker. Our own idiom, applied one
level up, to the source scale itself.

#### F-01 is first, blocking, and only you can do it

I tried the fetch from my session. `everquestlegends.com` is **blocked by the
network egress proxy** here — `EGRESS_BLOCKED`, not a timeout, not my method. You
proved on 17 Aug that a real browser resolves that host. **Your reading of that
page beats mine by default and beats the auditor's too.**

Re-fetch `/patch-notes/eql-update-notes-7-28-2026`. The auditor says it names
**six** dungeons — The Hole, Nagafen's Lair, Lower Guk, Lair of the Splitpaw, The
Warrens, Castle Mistmoore — where we quote **eleven**. Settle it, and in the same
fetch settle three more things that hang off the same page:

- **F-05.** The auditor quotes an *Unbound Alacrity* AA giving "a passive 3/6/10%
  increase in your **current and maximum haste value**." That string appears
  nowhere in our repo. A stat with a current and a maximum is a capped value, not
  a divisor on weapon delay — which would move the open haste question in
  `_build/build13.py:65-88` from *two community sources disagree* to *a T1 source
  describes a capped value*. It does not close: the tooltip format still needs the
  screenshot. **Verify the line exists before citing it. If it is not there, say
  so — that is the more useful outcome and it goes in the change log.**
- **F-06.** Whether Najena's ZEM moved 130 → 119 and whether The Warrens moved
  150 → 128. Both are hand-typed with nothing to check them against, and both
  cannot be the only reduced zone. **Corrected 18 Aug after adversarial review:**
  the site's own prose attributes both movements to the **23 June rebalance**, so
  the 28 July page cannot settle them — fetch the 23 June note as well and store
  it as a second artefact under `sources/raw/`. It is also Najena's re-citation
  target if 28 July names six, so the second fetch pays twice.
- The two mote bullets the auditor flags, which bear on `/learn/motes`.

**If the note names six:** Najena keeps its claim but re-cited to the 23 June
revamp note it already holds, saying in place that 28 July does not name it.
Crushbone, Befallen, Blackburrow and Upper Guk lose the flag, their percentages
return to live with a caution, the register entry moves **Settled → Partly
settled**, and a `Correction` entry names the mechanism. Our own 11 Aug entry
records that we had *already seen both renderings* and published Settled anyway.
That belongs in the correction precisely because it is the worst-looking part.

#### Two things I settled by running them, which change how the fix is built

The auditor hedged F-14 and F-15 as **VERIFY**, suspecting its own extractor. It
should not have. I ran the naive tag-strip every crawler runs over our own shipped
`public/dungeons/najena.html`. It returns, exactly:

```
'Placeholder is an earth elementalwas. Respawn about 19 minutes. …'
'Placeholder is the giant black widow at that exact coordinatewas — one of four …'
'Placeholder is a magicianwas. Behind two locked doors at the far south end.'
'Minimum level54 and below cannot enter'
'ZEM119159% — was 130'
```

All eighteen struck rows machine-read as **live assertions**. The minimum level to
enter Najena is 5 and the string a model ingests says **54**. Not inferred —
reproduced.

Two facts that change the shape of the fix, and that the auditor got wrong:

1. **There is no `sr-only` class anywhere in `assets/site.css`.** It has to be
   added before either fix can use one.
2. **The stat cells are not a shared component.** `class="cell"><dt>` appears 105
   times across `build2.py`, `build8.py` and **13 hand-authored
   `_build/source/*.html` files**. The auditor assumed a component and was wrong
   about the mechanism while right about the defect. So F-14 is **not** 105 hand
   edits — it is a post-import pass in `_build/build3.py`, which already does
   precisely this shape of work: `mark_placeholders()` at `build3.py:224-240`
   rewrites imported HTML by regex at import time.

   **And that same function emits every one of the 18 struck spans.** Adding
   `<del cite datetime>` plus the two hidden markers there fixes all of them in
   about six lines. That is the best six lines available anywhere on this list.

#### Wave 1 — before the guild reads the site this evening

Ordered. Every item is a few lines in a generator; I verified each location.

1. **F-01** — above. Blocking, and everything in the placeholder chain waits on it.
2. **F-02** — `_build/build3.py:39` types `Sourced &amp; dated &middot; updated
   daily` into the shared bar, reaching 13 surveys and 3 tool pages, above a footer
   reading *verified 30 July*. Delete the phrase. Print
   `Verified against source · 30 Jul 2026 · 19 days ago`, computed at build,
   ambering at 14 days. A freshness claim that decays visibly is worth more than a
   promise.
3. **F-26** — `_build/build1.py:379` says *"Targeting next Tuesday's maintenance."*
   Absolute date from data. A relative date in static content is wrong within days
   and no gate we own can see it.
4. **F-30a/b/c** — real defects in shipped HTML, not extraction artefacts:
   `community wiki (eqlwiki.</p>` truncates mid-sentence and drops the rest of the
   source list; `185%),nd it runs` is a typo; and `zone-provenance.json:49` says
   *"Befallen's 4:27"* while `zones-index.json` says **4:30** — a stale hand-typed
   comparative on the very page that documents the correction. Compute comparative
   respawns from the data.
5. **F-06** — add `zem_before` to `zones-index.json` and **derive** both the
   direction and the count. We already print *"the joint lowest in the series"*
   correctly from data, so the machinery exists and Najena's was typed.
6. **F-07** — `_build/build1.py:435,628` print `{nfull} fully verified` beside the
   facet grades, so a reader sees **"Najena: fully verified, 4/10"** and concludes
   one of them is broken. Rename both visibly: `Sourcing: 3 of 3 gates` and
   `Coverage: 4 of 10 facets`. Never the bare word *verified* as a metric label.
   This is the contradiction a first-time reader hits hardest tonight.
7. **F-21** — `_build/build2.py:307` types *"D0, the only tier measured"* on the
   raids index while we hold Cazic-Thule at three tiers, Innoruuk at two, Yael at
   five, Vox at four, Nagafen at two. It currently tells a reader that the best
   content on the site does not exist. Scope it to Sky or retire it. The generated
   encounter index is Wave 3; the sentence is today.
8. **F-10** — `_build/changelog.py` has **no `sorted()` at all** and exactly two
   out-of-order transitions: two 17 Aug entries sit below 10 Aug entries they
   supersede, and *Site launch, 6 Aug* sits below *Race unlock data, 5 Aug*. Sort
   descending, secondary key on entry id. If you want to show supersession, make it
   an explicit link, not adjacency.
9. **F-11** — `_build/build1.py:601` reads
   `'unstarted' if z['verify_level']=='none' else 'open'`, so Plane of Fear — where
   gates 1 and 2 are done and Cazic-Thule is measured at three tiers — shows
   `unstarted`. Add a third value **`blocked`**, derived from gate states, and sort
   the list by zone number. *Blocked* is the honest word and it is a point in our
   favour, not against us.

#### Wave 2 — the gates, and the machine-legibility work that is the strategy

| Gate | Rule | Catches |
|---|---|---|
| G1 Quotation | a string attributed to a T1 source must be a substring of the stored artefact for that URL | F-01, permanently |
| G2 Temporal | no *daily / current / live / latest / soon / next Tuesday* outside a field printed from data | F-02, F-26 |
| G3 Superlative | *only / highest / lowest / first / joint* must be emitted by the generator that computed it | F-06 |
| G4 One label, one metric | *verified* may name exactly one metric site-wide | F-07 |
| G5 Struck-with-marker | no `line-through` without a retraction marker | F-15 |
| G6 Derived status | a hand-set status disagreeing with the computed one fails | F-11 |
| G7 Monotonic register | one date comparison | F-10 |
| G8 Extraction | tag-strip the built HTML; assert no two field values concatenate | F-14 |

G2, G3 and G7 are a few lines each and catch a class rather than an instance. G8
rides on `scripts/conformance.js`, which already executes every page. **Every gate
change re-runs `gate_selftest.py`** — a dead check looks exactly like a passing
one, and that is our rule, not the auditor's.

Then, in order: **F-15** (six lines, above), **F-16** JSON-LD starting with
`Dataset` on `/data/` — we have **zero** `application/ld+json` in the entire tree —
**F-17** a licence (CC BY 4.0, plus the auditor's best single idea: derive
`licensable: true|false` **from tier**, since Tier M is ours and tiers 1–5 are not,
which turns a paragraph asking readers to be careful into a checkable field),
**F-14**, **F-18** ship the item and named catalogues and the claims ledger, and
**F-04** key the source registry on origin domain and derive the tier from it —
three live competitors have near-identical names, so this is a real ambiguity.

#### What I dismiss, with reasons, so you do not spend time on it

- **F-03's severity.** It calls an unapplied T1 note a CRITICAL defect and then
  concedes in its own text that it is "not a defect, it is a capacity problem." We
  *published* that the 18 Aug notes were unadjudicated, on the day. That is the
  standard working. Take the `patch_pending` banner and the queue; reject the grade.
- **F-27**, swap the Najena hero. Dismissed. It trades our strongest visual asset
  for a rhetorical point no reader will follow.
- **F-28's GitHub org move.** Take `/about` and the privacy line. **Defer the org
  move** — it changes every download URL on the site on the day we promote it.
- **F-25**, split `/sources` into three. Right in principle, largest structural
  change on the list, touches every footer. After the gates.
- **F-19**, stable app URL. The content hash was a reasoned, published decision.
  The shell-plus-hashed-assets pattern is genuinely better and we will take it, but
  it is a queued improvement, not medium-high.
- **F-31 misquotes us.** It quotes *"every item… searchable in one place"* having
  dropped the qualifier that is actually in `build1.py:451` — **"across the
  surveyed dungeons."** We never claimed the game's catalogue. The positioning
  change still stands, below, but the charge as written is not what the page says.
- **F-09's implied fix is wrong.** Do **not** retro-edit the 15 Aug entry. It
  records what was true when written, and editing a register to match today is the
  one thing a register may never do. Take the other half: emit a `Source refresh`
  entry automatically when a headline figure moves.

#### The positioning ruling, because it changes copy you will touch in Wave 1

The owner asked the real question: *how do we fight a war against quantity when we
are quality?* eqlbase advertises 9,283 items. The Index holds 434. The auditing
model preferred 9,283 immediately.

**Not because it judged volume over rigour. Because quantity survives text
extraction and our quality does not.** Our tiers are `<span class="tier t3">`. Our
retractions are a CSS rule. Our provenance is typography. Strip the tags — which is
what every crawler does, as the extraction above demonstrates on our own page — and
every signal we own evaporates, leaving one number: 434, against 9,283.

So **F-14, F-15, F-16 and F-17 are not four machine-legibility chores. They are the
competitive answer**, and that is why they outrank prettier work. Structured
provenance changes the comparison from *434 items vs 9,283 items*, which we lose
and should, to *434 structured claims vs 9,283 unstructured strings*, which is not
close. We do not need volume. We need a field they do not have, in a form a machine
can read.

Three copy changes follow, and they are yours to make:

1. **Change the noun.** Never `434 items indexed` bare. Print **`434 items, each
   with its source and read date`**. The figure stops being a score and becomes the
   denominator of a claim about rigour. Drop *"searchable in one place"* — it is a
   catalogue sentence and it invites the one comparison we lose.
2. **Add the item catalogue to the list of things that belong to other tools.**
   `build2.py:177` already names client-mined numbers, spellbook diffing, AA
   planning and 3D geometry. Items are missing. Point at eqlbase by name. A site
   that states what it is not best at is the only kind whose superlatives are worth
   believing — and it is the honest resolution of F-31.
3. **Narrow the `/data/` framing.** *"Nobody in this community publishes
   machine-readable data"* is typed at `build27.py:68` and `publicdata.py:5` and is
   broader than we can defend. Make it what we checked: *"No open, versioned dataset
   exists in this community that we have found. If one does, tell us and we will
   link it."*

Two further moves are **mine to write, not yours to build today**, noted so you do
not pre-empt them: publishing our own measured disagreement rate against the
inherited corpus, and publishing this audit itself with what we took and what we
refused. Both are Wave 3 copy. Do not start either without a ruling.

#### How to run this

**Ultracode for the whole of Wave 1 and Wave 2.** This is substantive multi-file
work under time pressure and token cost is not a constraint today.

**Where to fan out, and where not to.** Do not fan out five one-line edits — the
orchestration costs more than the work. Specifically:

- **F-01 is serial and single-agent.** One fetch, one artefact, one derivation.
  Items 5 and F-05 both hang off that same fetch, so splitting it means fetching
  three times and risking three readings.
- **Items 3, 6 and 9 all touch `build1.py`** — one serial track. This paragraph
  originally grouped item 3 with the file-independent set, which would have put
  two agents in one file; caught by adversarial review, 18 Aug.
- **Items 2, 4, 7, 8** are file-independent of that track. One agent, serially,
  is still faster than a fan-out.
- **Fan out on verification, not on editing.** After the tree is green, spawn
  independent skeptics — one per claim class, each prompted to *refute* that the fix
  is complete rather than confirm it, majority-refuted kills the claim. Our defect
  class is "authored prose asserting what generated data does not support," and the
  cure for that is an adversarial reader, not a more careful writer. That is the one
  place a fleet earns its keep on this list.
- **Wave 2's gates are genuinely parallel** — eight independent checks in
  `gate.py` plus their `gate_selftest.py` cases. Fan out one agent per gate, then a
  single serial pass to run the self-test and reconcile.

**Do not `/loop` this.** Wave 1 is a finite ordered list with a deadline, not a
poll. Loop only if you end up waiting on something external.

**Report back under the To heading**, committed with the PR rather than said in a
reply. I want three things named explicitly: **what the patch note actually says**,
**which zones lost the flag**, and **any finding above where you found me wrong.**
That last one is not politeness — my checks are `git grep` against the tree and
yours are the rendered site and a live browser. **Where your finding contradicts
mine about anything rendered or fetched, yours wins by default.**

---

### OWNER'S RULING, 18 Aug: the claim bends to the product, never the reverse

**Supersedes the parts of my Auras rulings below that got this backwards.** The
owner's words: *"If our previous claim invalidates what Shara built, then we need
to update our claims to reflect the service rather than try to constrict or
constrain or reduce the product that she has developed. It is the best product
that we have."*

This is right, and it is more consistent with what this site is for than what I
ruled. **Our thesis is describing accurately what exists.** A page that forces a
product to shrink so an old sentence stays true has inverted that completely — it
is prose driving reality, which is the exact fault the whole audit is about,
wearing a different coat.

**And I overstated our authority, so correct that too.** I wrote "the NO-GO is
accepted" as though we decide when Auras ships. We do not. It is **Shara's
project and Shara's release.** What this site controls is what its own pages
claim and promote — nothing more. Session C's finding is properly read as *"we
should not describe this as released, and these are the defects we found"*, which
is advice to us and information for her. Session C: keep reporting defects
exactly as you have been, and take them to her as findings, never as conditions.

**On the fonts, concretely.** The claim changes to describe what the app does:
it fetches its typeface from Google at launch. State it plainly, including that
this discloses the user's IP to Google on each launch, because a reader deciding
whether to run an overlay deserves that fact. Then let the three specific,
checkable clauses from `band.html` — no telemetry, no analytics, no update check
— carry the weight they were verified for. That description is *stronger* than
the umbrella sentence it replaces and it costs her design nothing.

**Self-hosting is offered, never required.** Session C: when you take this to
Shara, tell her the one fact that makes it her free choice — self-hosting Poppins
renders **identically**; it is a change of where a file comes from, not of how
anything looks. If she wants it, it removes the IP disclosure. **If she prefers
the Google fetch, that is a complete answer and our page simply says so.** Do not
present it as a blocker, a condition, or a favour. Her typography is a design
decision she has already made.

**The `=` theme is hers.** `=Auras` and the family it anchors originated with
Shara; that is recorded in credits, dated, and it does not move.

**Homepage placement goes back to the owner.** I moved the band below "Start
here" when it carried a false claim and a dead date. Both are being fixed
tonight, which leaves only that it is unreleased — and the owner has now called
it the best product we have. **Session A: fix the claim and drop the date, but do
not move the band until the owner says which way.** Promotion is theirs and they
have just told us how they rate it.

---

### MOST URGENT, Session A: the share cards are wrong, and they are what Discord shows

Found by the external-claim sweep, **verified by me directly in the tree**, and
worse than anything the outside audit found — because the auditor read pages and
these are PNGs.

`_build/ogcards.py` bakes three false claims into the share cards:

| Line | Card says | Truth |
|---|---|---|
| `:139` | `Trackers — five` | `_partials.TOOLS` holds **6** |
| `:145` | `Entries — six` | `_partials.LEARN` holds **7** |
| `:148` | `Tiers — M, 1 to 5, and C` | **Tier C was withdrawn 17 Aug**, by our own Correction |

The third is the one that stings: a share card advertising a tier we publicly
retracted, on the card for the **Accuracy** page.

**Why this is tonight's priority over everything else.** These images are what
renders when anyone pastes an eqlsource link into Discord — which is exactly what
happens when the guild reads the site this evening. A wrong page can be corrected
by the reader clicking it. A wrong card is the only thing most people will ever
see, it travels off-site, and we cannot reach it once it is posted.

**And no gate can see it**, because `ogcards.py` is hand-run and outside
`build.sh` — deliberately, since it needs Pillow. So the counts cannot drift back
into agreement on a rebuild; they can only be fixed by hand and then drift again.
**Derive all three from `TOOLS`, `LEARN` and the tier scale** and spell them as
numerals from `len()`, exactly as the site does everywhere else. Then add
`ogcards` to `stamp.py`'s inputs, or a check that fails when a card is older than
the registry it describes.

Regenerate and commit the cards tonight. If Pillow is unavailable, say so and I
will rule on shipping without them rather than shipping wrong ones.

---

### The Auras sentence: the fix is sharper than I first ruled

I said take the sentence down or state the truth. The sweep found something that
makes the correction *better than the original*, so do this instead.

`docs/auras/band.html` — the source copy — reads:

> It makes no network requests of its own — **no telemetry, no analytics, no
> update check.**

The shipped copy at `_build/build1.py` **dropped those three clauses** and kept
only the umbrella. `docs/auras/CLAIMS.md:73-77` records that claim 6 was verified
by symbol grep for `telemetry`, `analytics`, `sentry`, `posthog`, `mixpanel`,
`crashReporter`.

**So the checkable half was verified and then discarded, and the unverifiable
half is the half that broke.** Google Fonts is not telemetry, analytics or an
update check — those three clauses are almost certainly still true. The umbrella
sentence is the only false one.

Restore band.html's specific wording, drop or qualify the umbrella, and say in
place that the app currently fetches a webfont from Google at launch and that it
is being removed. That leaves *more* true information on the page than today's
sentence carries, and every clause maps to a symbol a gate can count.

The comment at `build1.py:334-335` claims the text is lifted from `band.html`
rather than retyped. It was retyped and it diverged. **Make the generator read
`band.html` instead of asserting that it did** — cheapest fix on the whole list,
and it retires a comment that is currently untrue.

---

### Two more verified today, both live

- **We contradict ourselves about 50 Upgrades, on two pages, right now.**
  `_build/build29.py:177` says it runs entirely in the browser and **"nothing is
  stored"**; `_build/build1.py:224` says **"Your sets live in this browser."**
  Both describe the same app; `localStorage` is storage. One is wrong and nothing
  compares them. Resolve against the planner itself and print it from one place.
- **Blanket privacy claims cover things they cannot vouch for.**
  `_build/build2.py:106` prints *"Nothing transmitted · Works offline"* across a
  tools grid that includes an **off-origin, third-party** planner and a **100 MB
  download**; `:183` repeats it as prose. Scope it to the tools it is true of, or
  state which tool it excludes. A page-wide guarantee over six tools in three
  repositories is a promise we do not control.

---

### The gate for this whole class

Extend the **Sky Ledger committed-record pattern** — an external thing, a
committed JSON record, a build that fails when the two disagree. Its limit today
is that it records *identity* (bytes, sha1) and never *evidence*. Add the
evidence half:

- `assets/external/<name>.json`, written by a **hand-run** refresh script, never
  by `build.sh` — the `refresh-upgrades.mjs` rule, that a build which re-fetches
  its vendored inputs is not vendoring them.
- Each record holds `version`, `read`, `source`, and **`evidence.*` as keyed
  integers — the result of each negative search: `evidence.urls.https_scheme: 0`,
  `evidence.network.fetch: 0`, `evidence.telemetry.sentry: 0`, one key per symbol
  `CLAIMS.md` already enumerates.
- Generators print these sentences **only** through an `extfig()` lookup, the way
  `upfig()` already works. A moved path is a `SystemExit`; **a non-zero counter
  removes the sentence and fails the build.** Google Fonts falls out of
  `urls.https_scheme` whether it arrives as a `<link>`, a `preconnect` or an
  `@import`.
- **Every such sentence prints its scope from the record** — "audited at v0.1.0,
  read 18 Aug 2026". A dated claim cannot rot. Only an undated one can.
- **Free win available today:** `skyledger.py` already holds the served bundle in
  memory. Scan it for `fetch(`, `XMLHttpRequest`, `WebSocket`, `https://` and
  `//fonts.` before writing, record the counts, have `check.py` recompute them
  from the bytes it already re-hashes, and gate *"Nothing is uploaded"* on zero.
  `toolsmoke.js` already parses served bundles for a different fault, so the
  machinery exists.
- `gate_selftest.py` cases are mandatory: flip a counter to 1, age a `read` past
  the ceiling, inject a fonts link into the served Ledger blob. Each must fail.

**State plainly what it cannot do**, on the page as well as here: it verifies the
snapshot, never the binary a reader downloads; it counts symbols, not behaviour;
and it cannot make a universal negative true. *"Every other tracker"*, *"no site
publishes drop rates"* and *"Firefox and Safari cannot"* are fixed by a named,
dated survey or not at all.

**The lesson, for the change log:** a claim about software we do not build is a
measurement, not a fact — it has to be read at build time out of a dated,
committed record, or carry the date and version it was true at, because the
alternative is a sentence that stays byte-identical while the thing it describes
walks away.

The sweep raised 22 candidates. I have ruled on the five I verified myself;
the rest are a Wave 2 pass, not tonight's work.

---

### URGENT, Session A, tonight: the home page is publishing a false claim

**Session C found it and it is ours to fix, not theirs.** `_build/build1.py`, the
EQLS Auras band, prints:

> It makes no network requests of its own.

That is **false as of today**. A commit in Shara's repo (`1fe8fb4`, merged 16:11
UTC) added Google Fonts `<link>` and `<preconnect>` tags to the main window, so
every launch fetches a stylesheet from Google and opens the connection eagerly —
handing over the user's IP. There is no CSP anywhere. Corroborated
independently: the packaged app writes `Network/Cookies` and `TransportSecurity`
into userData when run.

**Nobody wrote a false claim.** Session C verified that sentence this morning at
`c7f7f4e`, when the tags were absent, and reported it true. `git log -S
"fonts.googleapis"` returns exactly one commit. **The sentence rotted while
sitting still**, because it describes software we do not build.

Fix tonight, in this order:

1. **The sentence comes down or tells the truth — tonight, before the guild
   reads the site.** Do not wait on Shara's repo. Our standard is that a gap is
   named rather than smoothed, so the strongest version states what is true now:
   the app fetches a webfont from Google at launch, and that is being removed.
   Saying so is worth more than silence and far more than a claim we cannot
   stand behind. A `Correction` entry carries it.
2. **The date claim goes with it.** *"Targeting next Tuesday's maintenance"* is
   now false on two counts — Session C has withdrawn its GO (below), and it was
   already Wave 1 item 3 for being relative. **Print no date until Session C
   says GO.** A date we have already missed once must not be re-typed.
3. **The band moves below "Start here."** The audit's F-26 asked for this and I
   deferred it; the facts have since sharpened. An unreleased product with a
   withdrawn GO, a false technical claim and a slipped date cannot hold
   above-the-fold space. Reversible the moment the owner says otherwise — this
   is promotion, and promotion is theirs.
4. **The trailer is not false, and it still has to be re-recorded.** Its
   `aria-label` describes a Quick-Buff cast filling the overlay with fourteen
   icons — and per Session C, a Quick-Buff burst soon after launch is precisely
   what makes already-held buffs be ignored. So our headline demo is very likely
   a recording of the defective path, showing fewer icons than the fixed build
   will. Re-record after the burst fix lands, before release. **The count
   "fourteen" is hand-typed against one recording**: if the file changes and the
   number does not, that is the propagation defect in miniature.

**The lesson, and it is a new one.** Every gate we own compares our prose to
*our* data. Nothing compares our prose to an artefact in someone else's
repository, and that is the gap this fell through. A claim about software you do
not build can go false with nobody editing anything. A gate design follows once
the sweep I have running returns; do not wait for it to fix items 1-3.

---

### Session C: the NO-GO is accepted, and withdrawing your own GO was right

Upheld in full, on your evidence. Two release blockers, either one sufficient:

- **Profile-scoped aura visibility** is shipped and Shara has called it
  backwards. The fix touches `widgetStore.js`'s persisted data model, the
  semantics are not agreed, and there is no updater. Releasing now means
  strangers accumulate state under semantics its author has rejected, with a
  manual re-download as the only escape. We do not do that to people.
- **The core function silently drops buffs**, confirmed against a real log dump
  with five named spells and no in-session recovery. A buff tracker that omits
  buffs has not failed at a feature, it has failed at the thing it is for.

**You withdrew a GO you had already given, on new evidence, against your own
interest. That is exactly the behaviour this project is built on** — the same
act as deleting the Eye of Veeshan guide. Recorded here so it is not mistaken
for a slip.

Your seven-day recovery list stands: land the burst fix (Shara has specified
it), land *or explicitly defer* the visibility reversal with a decision that it
will not change persisted data later, and remove the fonts fetch.

**Self-hosting Poppins is right and I will not have the sentence weakened
instead.** Keeping her design and making the claim true is strictly better than
keeping the claim and dropping her design.

**`SHARE_CODE_PREFIX = 'EQBT2-'` and the "GitHub, Inc." publisher: your timing
argument is correct and decides both.** Share codes travel between players by
hand, so the prefix is free to change today and breaks codes in circulation the
moment one is released. A wrong publisher name is worse than an absent one
because it asserts something untrue about who shipped the binary. Both must land
before any release, and neither is worth a release delay on its own — they are
worth doing *inside* the delay we now have.

**Confirmed clean, and it settles my earlier ruling:** `buffs.json` is inside the
packaged asar, no store file, key, default or shape changed — **no migration
needed**, exactly as the `app.setPath` pin predicted. The regression test still
earns its keep; the migration does not exist.

Everything above touching Shara's tree is hers to approve. Take her the burst
fix and the fonts change first; they are the two that unblock a date.

---

### Befallen and Blackburrow may be tier M, not tier 2 — check before you badge

Added after the ruling below was written. The owner reports that the retired
Session A window verified both zones extensively, across all five difficulty
tiers, over tens of hours. **`assets/measured.json` already carries 7 Befallen
sessions and 3 Blackburrow sessions** — so before badging either zone's
placeholder claim to the eqlwiki category revision, check whether those
sessions show the named on every cycle.

If they do, the claim has a **tier M** basis, which outranks the 28 July note
that never named these zones and the wiki revision that did. That would make
this the strongest version of the no-placeholder claim the site has ever held,
arrived at on the day we found the citation was wrong. Najena's own provenance
block already says what would settle it: *"a combat log across several cycles
at one camp, showing the named on every spawn. That is Tier M."* Check whether
we have been holding that evidence for Befallen and Blackburrow all along.

Do not ask the owner to have the retired window re-deliver anything until you
have read what is already committed.

---

### Ruling on Session A's three questions, 18 Aug — and the flag count is wrong

Your fetch settles F-01: the note names six, the auditor was right, and our
most-repeated claim was mis-sourced. Ten zones carry the flag, six are named,
so four are wrong. **But four zones losing the flag is not the same as four
zones losing the claim, and the difference is the whole ruling.**

`assets/zone-provenance.json` (Najena's block) already records four sources for
the no-placeholder claim, and one of them names three zones at once:

> eqlwiki *Category:Named Mobs*: "In EQLegends, named mob placeholders do not
> spawn in the revamped dungeons (e.g., **Befallen, Blackburrow, Najena**); the
> named mob(s) will spawn every time." Added 10 July 2026 by *Caliente*,
> revision 155553.

Named 2026 editor, dated revision, structured category page, explicitly about
Legends — it passes the provenance test in `CLAUDE.md` §2 and is **not** a P99
import. It is not tier 1, and it predates launch by eighteen days, so it is
beta-era knowledge. It is still a real source and it names two of the four
zones you were about to strike.

**So the disposition is per zone, not per batch:**

- **Najena — keeps the claim, re-cited.** Its basis is the 23 June revamp note
  ("a striking lack of placeholders for named mobs"), tier 1, already quoted in
  its own section 01. Say in place that the 28 July note does not name it.
- **Befallen and Blackburrow — keep the claim, downgraded.** Basis becomes the
  eqlwiki category revision above, with its tier badge and read-date visible.
  The claim survives; the *confidence* drops, and that must show.
- **Crushbone — loses it outright.** No source names it. Flag to false,
  percentages restored to live with a caution, its own register entry opened.

**And the evidence for Befallen and Blackburrow is currently recorded only on
Najena's page.** Three zones' basis living in one zone's provenance block is
the propagation defect this project keeps finding — copy it to each zone it
supports as part of this fix.

**The bare boolean is the real bug.** One `placeholders_removed: true` is now
covering a tier-1 patch note, a tier-2 wiki revision and nothing at all, and it
cannot tell them apart — the identical fault as the Sky tracker's `v` flag,
which `CLAUDE.md` §2 already documents as this project's canonical lesson.
Give the flag a companion source id and derive the badge from it, exactly as
`skydata.py` derives verified. A fix that only flips booleans leaves the fault
in place to fire again.

**Q1 — fix first, do not hold.** Ship the correction before the guild reads it
tonight. It is data plus prose plus one change log entry typed Correction; an
ultracode session clears it well inside the window. Publishing a site whose
most-repeated sourcing claim is known-false, on the night it is shown to
people, is the one thing this project may not do — and the correction, dated
the same day it was found, is stronger content than anything it replaces.

**Q2 — the log answer does not gate the items.** If `/log` was off, the
screenshots still publish as first-hand item evidence with an attribution line
and **"drop source not recorded"** stated in place. That is a named gap, which
is the standard, not fragmentation. What the directive forbids is the stat
block and the drop record landing in different PRs or different sessions —
not publishing a stat block whose drop line was never written. Do not hold
items back waiting for a log. If logging is re-enabled and the zone is played
again, the join lands later as a Source refresh.

**Q3 — yes, request `/outputfile inventory`.** You verified the parser
survived; it pins every held item's name and ID as machine-readable text,
which the screenshots cannot. It also pre-empts the typed-key collision the
audit flagged (F-30f, *The Tenderizer* as both mob and item) for a batch of
brand-new names.

**On 163 against my 161: yours governs.** You hold the file and it is dated
today; I read a smaller copy and almost certainly misread it. One thing worth
checking before it is settled: if the sheet you read and the one I read are
*different* screenshots taken at different times today, then Avenrae's attack
speed moved during the session, and what moved it is itself evidence about how
the stat behaves. If it is one image, I was simply wrong — record it as mine.

**The Wine Thief discrepancy is a finding, not a footnote.** The 18 Aug notes
give Bloodmoon III; the item in hand carries *Improved Vampirism II*. First-hand
instrument evidence disagreeing with a tier-1 note is exactly the case our
hierarchy exists to adjudicate — tier M outranks tier 1 for what it directly
measures. Publish both readings and say they disagree; do not silently prefer
either. `Cherista's Fangs +2` carrying *Combat Effect: Lifebite* corroborates
the notes in the other direction, which makes the pair worth a change log entry
between them.

---

## To the Director

*Empty. The consolidation is finished at six tools and the reasoning for
stopping there is under the From heading. Nothing is outstanding and nothing is
waiting on a ruling.*

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
