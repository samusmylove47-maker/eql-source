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

**Branch `claude/placeholder-recitation`. F-01 fetched and stored, F-05 settled,
the placeholder correction shipped. Protocol read; this is where my questions
live from now on.**

### What the 28 July note actually says

Fetched in a real browser, stored verbatim at
`sources/raw/2026-07-28-eql-update-notes.txt` — the first artefact of the store.
It is JS-rendered, so a plain fetch returns navigation and nothing else, which is
most of why nobody had checked it.

> Removed placeholders from and lowered maximum respawn times in several
> dungeons: **The Hole · Nagafen's Lair · Lower Guk · Lair of the Splitpaw ·
> The Warrens · Castle Mistmoore**. More dungeon treatments will take place over
> time.

**Six.** Not eleven, not ten-and-Upper-Guk. Upper Guk is not mentioned anywhere
in the note.

**The haste string exists verbatim**, which is the more useful of the two
outcomes you named: *"Added the Unbound Alacrity AA, a new autogranted class AA
for Monk Gives a passive 3/6/10% increase in your current and maximum haste
value."*

**Both mote bullets, verbatim:** *"Players will no longer receive motes while at
the class lock cap."* and *"Motes will no longer drop for players unless they
were eligible to gain exp from the kill."*

### Which zones lost the flag: one, not four

Your per-zone ruling is why, and applying it changed the answer:

| zone | disposition | basis now |
|---|---|---|
| the six named | keep | `patch-2026-07-28`, tier 1, quoted and stored |
| Najena | keep, re-cited | `patch-2026-06-23`, tier 1 — **but see below** |
| Befallen, Blackburrow | keep, downgraded | `eqlwiki-cat-named-155553`, tier 2, rev + editor + read-date visible |
| **Crushbone** | **loses it outright** | none |

Crushbone's rows carried `title="Historical. The 28 July 2026 patch note removed
placeholders from this zone."` — a tooltip citing a note that never named it.
They are live text again.

**The boolean is gone as the carrier.** `assets/placeholder-sources.json` holds
one entry per basis with tier, url, read-date and the quote; each zone names one
by `placeholders_source_id`; the confidence a page shows derives from that. Same
remedy `skydata.py` already applies.

**The evidence is propagated.** The eqlwiki revision lived only in Najena's
provenance block while supporting three zones. Copied to Befallen's and
Blackburrow's.

---

### Where the directive and the prompt are wrong

**1. There is no 23 June patch note to cite, and Najena's basis is now the
weakest thing on the page.** `everquestlegends.com/patch-notes` lists six notes;
the oldest is **7 July 2026 (Beta)**. Probes for 6-16, 6-23 and 6-30 fall through
to the site's Home view, which is how that single-page app answers a path that
does not exist. F-06's plan to fetch it and use it as Najena's re-citation target
**cannot be executed**. I have recorded it as `fetchable: false` with the
reasoning rather than quietly citing an unreachable source. Najena's claim now
rests on a tier-1 note a reader cannot check, plus the tier-2 wiki revision that
also names it. **That is worth your ruling: I would rather demote Najena to the
wiki revision alongside Befallen and Blackburrow than keep a tier-1 badge on
something unverifiable.**

**2. `measured.json` does not establish tier M for Befallen or Blackburrow, and
I have not badged them.** The counts are right — 7 and 3 sessions — but the parse
records kills, loot and casts per mob and **no spawn-cycle structure at all**. It
cannot distinguish *named on every spawn* from *named killed often*. What it
shows is suggestive: in one Befallen session `Knight V'Tal` dropped 9 items and
`Soldier of V'Zher` 7, which is repeated kills of the same named in one sitting.
That is consistent with no placeholders and does not demonstrate it — a zone
*with* placeholders also yields repeated named kills, just less often. Najena's
own standard is the one to beat: *"a combat log across several cycles at one
camp, showing the named on every spawn."* Settling it means a camp-cycle analysis
of the raw 04–07 Aug Shara logs, which are in `state/logs`. **That is real work
and I did not fake it under deadline.** Left at tier 2.

**3. The survey prose already had it right; the error was confined to
`zones-index.json`, and the site contradicted itself.** `zone-provenance.json`
already names the six correctly on The Hole, Nagafen's Lair, The Warrens and
Mistmoore — `thehole[2]` quotes all six verbatim — and `blackburrow[0]` says in
as many words *"Blackburrow was not named in the 28 July launch-day dungeon
pass."* So one file said six and excluded Blackburrow while another flagged it
and claimed eleven. Worth knowing for the audit's model of how this defect
spreads: it was not a uniform belief, it was two files disagreeing.

**4. A gap closed that this site had already scoped precisely.** Blackburrow's
`respawn_note` has said since 11 August that eqlwiki's rendering named six
without it, a fuller quotation supplied to us named eleven with it, and **"one
reading of the developers' own page settles it."** That reading is done. Six,
without Blackburrow; the eleven-zone quotation was wrong. Recorded as a gap
closing, not as new content, and 22:00 is not a pre-patch ceiling for that zone
because the pass never touched it.

**5. Stream 2's premise was false when written, and the owner has since fixed
it.** The live `eqlog_Avenrae_rivervale.txt` held **17 Aug 15:51–17:17 only** —
17,806 lines, every one `Mon Aug 17`, zero 18 August lines. One zone entry, `The
Plane of Fear 1 (Awakened)`. **74 slain lines and zero bosses** — no Cazic-Thule,
Dread, Fright or Terror. Not two clears; 86 minutes of trash. Its only two
"mistmoore" strings are other players' chat, one of them saying *"i think
mistmoore is getting a revamp tomorrow"*. `dbg.txt` was written today at 14:30,
so the client ran and the chat log did not — logging was off.

The owner then supplied Shara's logs, and those are the real thing. See below.

**6. Attack Speed is 163, not 161.** Single screenshot, dated today, sent into
this session. Recorded as yours per your own instruction — but note it is one
image, so the "did it move during the session" reading does not arise from this
evidence.

---

### The haste question has a third answer, and the screenshots settle it

Not a bare number and not a percent. On items, haste is a **named effect with a
rank**:

- `Cape of Midnight Mist +4` — **Focus Effect: Enhancement Haste I**
- `Nightshade Wreath +2` — **Focus Effect: Reanimation Haste I**

On the character sheet it is a **%-labelled stat carrying a bare number**:
`Attack Speed % 163`. The register asked whether a tooltip prints a bare number
or a percent; on these fifteen items it prints **neither** — it prints a name and
a roman numeral, and the number lives on the sheet. That is consistent with the
patch note's *"3/6/10% increase in your current and maximum haste value"*: a
percentage applied to a stat, with the stat shown on the sheet and the source
shown on the item.

Two items corroborate the 18 Aug notes independently: `Wine Thief +4` carries
*Improved Vampirism II* (the note gives Bloodmoon *III*), and `Cherista's Fangs
+2` carries *Combat Effect: Lifebite* (the note adds Lifebite). Per your ruling
the Vampirism pair is a finding, not a footnote, and both readings publish.

### Shara's logs — the first post-revamp Mistmoore data exists

`eqlog_Shara_rivervale_2026-08-18.txt`, 60,756 lines, 00:00:02–15:47:37 today.
Copied into `state/logs` beside all eight existing logs (10 total; `.gitignore`
covers `state/logs/` and `*eqlog*.txt`, verified — `git status` cannot see them).

**Mistmoore at three tiers, all post-patch by timestamp** (servers down 06:00
PDT; these are afternoon):

```
12:55:32  The Castle of Mistmoore              (D0)
12:56:35  The Castle of Mistmoore 1 (Awakened) (D1)
13:58:47  The Castle of Mistmoore              (D0)
13:59:39  The Castle of Mistmoore 2 (Adaptive) (D2)
```

Named killed: **Xicotl ×4, Butler Syncall ×4, Maid Issis ×3** — repeated named
kills inside three hours, which bears directly on the revamp's *"named NPCs being
guaranteed spawns"*. `eqlog_Shara_rivervale_2026-08-17.txt` carries the Plane of
Fear day, including `The Plane of Fear - Group` and an unnumbered entry, so D0
and D1 both.

**I have not parsed them into `measured.json` yet.** That is the Mistmoore
ingestion PR, and per the directive it rebases onto Wave 1's Mistmoore touches
and needs the `build9.py` date-split before eras can be kept distinct. Doing it
in the same PR as this correction would have delayed the correction, and Q1 said
fix first.

### Questions

1. **Najena's tier.** Demote to the wiki revision, or keep a tier-1 citation a
   reader cannot reach? I lean demote.
2. **The tier-M analysis for Befallen and Blackburrow** — worth doing? It is a
   camp-cycle pass over the raw logs, and it would make this the strongest
   version of the claim the site has held. Not tonight.
3. **`/outputfile inventory`** — requested per your ruling. `_build/inventory.py`
   survives and still writes `assets/item-ids.json`, so the parser is intact.

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
