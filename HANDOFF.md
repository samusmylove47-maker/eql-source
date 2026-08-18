# Handoff — 18 August 2026

Read `CLAUDE.md` first. This file is the current state and the open work.

**This describes commit `348e6559`** (PR #91, merged — the tip of `main`). Diff
against it rather than trusting anything below — a later session should
re-derive, not remember. Name a commit `main` actually pointed at: the licence
fix `37d12f50` is a branch commit that only ever reached `main` inside that
merge, so diffing against it walks through a state `main` never had.

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
| `.html` → extensionless 307 | Real, post-launch. It touches every internal link and the sitemap. |
| Self-hosting the site's fonts | Real, post-launch. |
| The map export | Post-launch. |
| Editing `public/assets/site.css` casually | It re-hashes `CSS_V` and rewrites the stylesheet line on every page. Fine when the CSS genuinely changed; never as a side effect. |
| Running `scripts/prose_budget.py` to fix a page that is over | It only lowers ceilings. A page over its cap is trimmed, or the ceiling is raised **by hand with the reason in the commit** — `CLAUDE.md` §5, precedent in PR #89. |

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

---

## To the Director

**From Session C, 18 August 2026, branch `claude/eql-auras-promo-band-9e76de`.**
The Auras band is ready as material and a spec. Nothing was built or rebuilt
here and `public/` was not touched — Session A lands it.

### What is on this branch

| File | What it is |
|---|---|
| `_media/auras-trailer.mp4` | 839 KB, 1600x900, 8.9s, 24fps, **no audio stream at all** |
| `_media/auras-poster.jpg` | 174 KB, 1600x900 |
| `docs/auras/BAND-COPY.md` | the copy, the word count, the markup shape, the gate rules it avoids |
| `docs/auras/band.html` | the exact markup the count was measured from — lift the text from here, do not retype |
| `docs/auras/CLAIMS.md` | the claim set, for you to adjudicate |

`_build/media.py` hashes both files on the next build and writes them into
`assets/media.json`. **No build change is needed** — the band reads the manifest
exactly as the Sky Ledger band already does.

### The video

Cut from `EQ AURAS BURST.mp4` (35.8s, 1920x1080, 42.8 MB) and encoded once by
hand at **CRF 28, no audio**, which is the Sky Ledger recipe unchanged. The one
departure is 24fps rather than 30: at 30 the particle burst came out at 1112 KB,
heavier than the trailer precedent despite being shorter. At 24 it is 839 KB,
under the 949 KB the Sky Ledger trailer ships at, with the documented CRF intact.

**It is 8.9 seconds because the source constrains it, not because I trimmed for
weight.** The clip runs 2.0s to 10.9s: the Quick Buff cast, then fourteen buff
tiles filling the top of the screen each counting down. At **t=11.25 the Windows
Start menu opens** in the capture, showing the desktop — Discord, Outlook,
Battle.net, "Update and shut down" — and at t=13 the application window opens
over the game. I verified frame by frame that the onset is between t=11.0
(clean) and t=11.25 (open), and cut at 10.9. The encoded file's first and last
frames were both checked after encoding, not just the source.

The poster is a frame from inside the clip, at t=10.8, with the full buff row up.
It is what shows below 700px and under `prefers-reduced-motion`, so it had to
carry the message alone.

The band's video **never shows the application window**, which incidentally
sidesteps a naming problem noted below.

### The copy — 136 words, and the ceiling

Measured with `gate.py`'s own `page_words`, not by eye. `index.html` is at
**649 of 649** — no headroom at all. With the band it is **785**, so
`assets/prose-budget.json` needs a hand edit to 785 with the reason in the commit
message. `prose_budget.py` only ever lowers, so this is a decision, as intended.

`BAND-COPY.md` carries three shorter variants measured the same way — 129, 124
and 118 — in the order I would cut them. **I recommend the full 136.** The first
thing to go is the clause naming the three things it does not do, and that clause
is the one buying the return visit you described.

### Three things need your decision

1. **"The idea is WeakAuras'" is the one claim I cannot source.** The word
   `weakaura` — and `wow`, `lua`, `addon`, and the bare word `aura` — appears
   nowhere in the project, in code, comments, docs or file formats. Modelled-on
   is a claim about design intent and only the author can source it. Your brief
   states it, and I have taken your instruction as the author's statement rather
   than inventing a citation, but you asked to be told. **One line from the
   author settles it.** The rest of that paragraph — from scratch, no shared code
   or trigger format, not affiliated or endorsed — is strongly evidenced.
2. **"Reads the log and nothing else" would have been false**, and it was my
   first draft. It also reads the character's spellbook file and the game's spell
   icon art. The shipped sentence names all three. Separately, there is one
   Windows-API call: every two seconds it asks the OS the *name* of the focused
   window's process so the overlay can hide on alt-tab. It never opens the game
   process or reads its memory, so the copy stays true, but "it touches no
   Windows API" would be false and I have not written it. The band omits that
   nuance for space; **the tool page should state it plainly.**
3. **The release date has no source but you.** The project's own handoff says
   "Status: dev build only, nothing shipped", the version is 0.1.0, and a
   main-window redesign is marked "planning only, nothing implemented yet". That
   is the argument for the qualifier, not against the band: **"targeting" is
   load-bearing and must not become "releasing".**

### Two findings for the author, unrelated to the band

- **The app calls itself "EQ Buff Tracker"** — window title, taskbar,
  `package.json` — while we are announcing "EQL Auras". Invisible in this band,
  obvious on any page showing a screenshot. Worth settling before the tool page.
- **Its About page understates its own work threefold.** It says roughly 3,300
  buffs; the bundled data file holds **11,337**, 11,190 with landing text. A good
  promotional figure, deliberately kept out of the band because a number like
  that should print from the data at build time rather than be typed beside it.

**And one to watch:** the project has no LICENSE file, no `license` field, and is
marked private. The first-party code is unlicensed — all rights reserved by
default. Nothing may describe it as open source or redistributable. Given the
eqlwiki licence claim withdrawn this week, it is the same shape of mistake.
