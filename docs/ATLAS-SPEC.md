# The two-theme atlas — specification

Written for the Director ahead of any generator change, per the design brief on
`claude/eq-map-export-proposal-oe8m6l`. **Nothing in `_build/` has moved.** The
reference specimen is *The Survey Sheet* (artifact `19c1de67`), read in full
rather than re-derived.

Every figure below was measured against the tree this branch is cut from. Where
the brief and the measurement disagree, the measurement is printed and the
disagreement is named.

---

## 0. Four things the brief gets wrong, or that have moved under it

Named first because two of them change what the work is.

**1. The share cards are already fixed.** The brief says they *"are wrong on
three counts already, so fix those in the same pass"*. That was true when it was
written and is not true now: commit `da654d88`, *"Withdraw three published
falsehoods, and derive every figure on a share card"*, landed earlier in this
cycle. `ogcards.py` now derives every figure from `TOOLS`, `LEARN`,
`index-data.json` and `len(Z)`; nothing on a card is typed. **No work here.**

**2. `--brass:#8A6A18` fails AA on parchment.** It measures **4.08:1** against
`#EFE6D4`. The brief hands it down as part of the approved DAYLIGHT palette
while also stating that both themes are non-negotiable on AA, and `DESIGN.md`
says the same. Brass is not decorative — the specimen uses it for the masthead
kicker at 10.5px, the tier-M badge at 9px and the instrument captions: all small
text, all needing 4.5:1.

Proposed fix, using the brief's own derivation rule so nothing is hand-picked:
mix toward ink in 2% steps until it clears. `#8A6A18` → **`#806217`** at
**4.61:1**, five steps. One token, one line.

**3. Mistmoore measures 5.26 on parchment, not 5.45.** Against `#EFE6D4` with
the standard WCAG formula I get **5.26**. Every other figure in the brief
reproduces exactly, including the one that matters most — Mistmoore is the
weakest of all thirteen on the dark ground at **3.08**, to the second decimal.
The discrepancy changes no decision; it is recorded so the number in the spec
matches the number in the file.

**4. The specimen's accents are hand-set, and the mandated rule does not
reproduce them.** The brief says to recompute rather than copy. Applied
literally — *"stop at the first value clearing 4.5:1"* — Mistmoore comes out
**unchanged at `#A8324A`**, because it already passes. The specimen shows
`#8B2B3E`, a distinctly deeper red at 6.74:1. Same on the dark ground: the
specimen uses `#C25068` where the permanent accent is `#A8324A`.

The rule and the mock disagree, and only one can govern. **This is the single
biggest open question in this spec** — section 2.

---

## 1. What a theme can and cannot reach — the mechanism, first

This determines the shape of everything else, so it comes before the palette.

**15 pages never load `site.css`.** They are self-contained, and
`_build/build3.py` injects tokens into them by copying a block out of the
stylesheet with a regex that takes the **first** `:root` block and only the
first. `site.css` has exactly one today, at line 14.

**Those 15 pages are the 13 dungeon surveys plus 2 imported tools.** That count
resolves the part of the brief expected to be "genuinely awkward", and it
resolves it in our favour:

| the 15 | what the theme should do | why |
|---|---|---|
| 13 dungeon surveys | **stay dark** | already the approved design exception |
| `tools/combo-calculator.html` | **decision needed** | imported, self-contained, 36 hard-coded hex values against 128 `var()` uses |
| `tools/race-unlocks.html` | **decision needed** | same shape, same counts |

**The plate exception is not something we have to build. It is what the
mechanism already does.** Put the dark tokens on bare `:root` as the first
block and the 13 surveys receive dark tokens and nothing else — for free, with
no per-page work and no exception list to maintain.

**Which makes block order in `site.css` load-bearing in a way it has never
been.** If a future edit puts the light block first, fifteen pages silently flip
to parchment tokens over dark hard-coded backgrounds, and nothing in `check.py`,
`gate.py` or `toolsmoke.js` would notice.

**Proposed: a gate rule asserting the first `:root` in `site.css` is the dark
one, with a `gate_selftest` case that reorders the blocks and proves the gate
fails.** A dead check looks exactly like a passing one, and this one guards a
silent whole-site regression.

The two tools are the only genuine open question here. **Recommendation: leave
them dark and say so on the page.** A theme would reach four fifths of each tool
and leave a fifth wrong, which is worse than a tool that is honestly one colour.

---

## 2. The palette, and the one question I cannot settle myself

**DAYLIGHT** — from the specimen, with the brass correction from section 0:

```
--surface-0:#EFE6D4   --surface-1:#E7DCC6   --surface-2:#DDD0B5
--bone:#241C12        --txt:#3A2E1E         --mut:#6B5C46
--rule:#CBBA9C        --rule2:#A89575       --brass:#806217   <- corrected
```

Verified against `#EFE6D4`: txt **10.66**, mut **5.22**, ink **13.55**, brass
**4.61** after correction. Panels descend — page `0.797` → surface-1 `0.723` →
surface-2 `0.638` — so stacked paper reads as shadow, which is the inversion the
brief warns is easiest to get backwards.

`--rule` at 1.53 and `--rule2` at 2.35 are **hairlines, not text and not
controls**, and must never carry either. Worth writing into `DESIGN.md`
explicitly: on the dark ground the same tokens sit at a different relationship
to their background, so the habit does not transfer.

**TORCHLIGHT** is unchanged, exactly as it ships.

### The accents

| zone | accent (permanent) | on `#0B0704` | on `#EFE6D4` | derived for parchment | ratio | steps |
|---|---|---|---|---|---|---|
| `befallen` | `#8E7BC7` | 5.55 | 2.92 | `#6E5E91` | 4.61 | 15 |
| `blackburrow` | `#5C93C4` | 6.14 | 2.64 | `#496B87` | 4.53 | 17 |
| `crushbone` | `#BE4F3E` | 4.18 | 3.87 | `#A84838` | 4.64 | 7 |
| `kedgekeep` | `#2FA5C9` | 7.02 | 2.31 | `#2B6E80` | 4.65 | 20 |
| `lowerguk` | `#7FA84F` | 7.28 | 2.22 | `#596D35` | 4.62 | 21 |
| `mistmoore` | `#A8324A` | 3.08 | 5.26 | `#A8324A` | 5.26 | 0 |
| `nagafenslair` | `#E06B2A` | 6.03 | 2.69 | `#A05022` | 4.62 | 17 |
| `najena` | `#D9A227` | 8.74 | 1.85 | `#82621D` | 4.56 | 24 |
| `planeoffear` | `#8FB03A` | 8.07 | 2.01 | `#5E6C28` | 4.64 | 23 |
| `planeofhate` | `#C24FA8` | 4.76 | 3.40 | `#A2458A` | 4.51 | 10 |
| `splitpaw` | `#45A6A0` | 6.90 | 2.35 | `#386F67` | 4.66 | 20 |
| `thehole` | `#8C7BE0` | 5.76 | 2.81 | `#6B5D9E` | 4.60 | 16 |
| `warrens` | `#B5793C` | 5.51 | 2.94 | `#8A5D2F` | 4.59 | 15 |

**12 of 13** fail 4.5:1 on parchment as they stand. The worst case needs **24
steps (48% toward ink)** and all 13 converge. This table was computed by the
rule below and pasted from that output; it is not typed, and the build will
recompute it rather than read it.

**The rule:** mix the permanent accent toward ink `#241C12` in 2% steps; stop at
the first value clearing 4.5:1 on `#EFE6D4`. Deterministic, thirteen in
thirteen out. The permanent accent itself never changes — this is `DESIGN.md`'s
existing "derive a lifted variant" rule applied to a second ground. **The build
must fail if any accent cannot reach 4.5:1.**

### The question

For twelve zones the rule and the specimen agree in spirit. For **Mistmoore**
they do not: the rule returns the accent **untouched** at 5.26; the specimen
shows `#8B2B3E` at 6.74. The site's signature zone would be the one zone whose
parchment accent is visibly brighter than every other — precisely because it is
the only one that needed no derivation.

Three options. I recommend the second:

1. **Rule as written.** Mistmoore stays `#A8324A`. Honest and deterministic, and
   leaves one card looking louder than its neighbours.
2. **Rule with a floor** — derive to 4.5:1 *or* a minimum of N steps, whichever
   is greater. At N=8 Mistmoore lands near the specimen and the other twelve are
   untouched, since all but Crushbone already need more. Still deterministic,
   still nothing hand-picked, and it matches the approved mock.
3. **Hand-set from the specimen.** Rejected — it is exactly the "typed beside
   the data" fault this project keeps finding in other people's work.

I can implement any of the three. **I am not choosing between a rule you
specified and a mock you approved without you saying which wins.**

---

## 3. The plates

The `.plate` recipe is kept whole and is not rebuilt: the 155° `color-mix`
wash of the zone accent at 13% into surface-1, content at `flex-end`,
`.plate-art` masked at 52%, the Saira numeral at 132px `line-height:.7` cropped
by the card edge at **`opacity:.3`** — kept, because the numeral is the card's
only statement of its own number, and `.19` measured 2.87:1, under the 3:1 bar
for information.

Two treatments, one token switch, straight from the specimen:

```css
/* daylight: the card sits IN the sheet */
box-shadow:0 1px 0 rgba(255,255,255,.55), 0 3px 15px rgba(60,40,16,.34),
           0 14px 40px rgba(60,40,16,.20);
border-color:#292217;
/* torchlight: a cast shadow on a dark ground says nothing */
box-shadow:inset 0 0 0 1px rgba(242,234,218,.055);
```

---

## 4. The toggle

Labelled by **destination**: reads `TORCHLIGHT` while in daylight, `DAYLIGHT`
while in torchlight. Dark is the default.

Block order, dark first — see section 1:

```
:root                                  TORCHLIGHT, and must stay first
:root:not([data-theme="dark"]) + @media (prefers-color-scheme: light)   DAYLIGHT
:root[data-theme="light"]              DAYLIGHT
```

This is the specimen's structure **inverted**. The specimen is light-first
because an artifact follows the viewer's theme; the site is dark-first because
dark is the default and because `build3.py` reads the first block.

The switch is a `button` in the masthead written by `_partials.py`, setting
`data-theme` on the root element and persisting to `localStorage`, with a small
inline script in `head` applying it before first paint so there is no flash.

**It cannot work without JavaScript.** A CSS-only toggle needs a checkbox ahead
of every themed element in source order, and the chrome is injected into pages
whose body order we do not control. The brief asks for no-JS "wherever
possible"; this is the honest boundary. Without JS the site renders dark and
honours `prefers-color-scheme`, which is a correct fallback rather than a broken
one.

---

## 5. What changes in `_partials.py`

| change | note |
|---|---|
| `head()` | inline no-flash script; `color-scheme` declaration |
| `nav()` | the toggle button, one per page, in the masthead |
| `CSS_V` | unchanged mechanically, but re-hashes on every page — the theme commit is a whole-site diff by construction. Own branch, alone |

`build3.py` needs **no change**, which is the happy consequence of section 1.

---

## 6. What this collides with

- ~~**`conformance.js` has no theme handling at all** — confirmed; the word does
  not appear in it.~~ **THIS WAS OVERTAKEN AND IS NOW FALSE, both halves.**
  Measured 2 Sep 2026: the word appears 28 times, `THEMES` is declared at
  `conformance.js:98`, and the sweep runs every page at two viewports **and** two
  grounds — the finding lines read `@ mobile/torchlight` and `@ mobile/daylight`.
  It already sets `data-theme` explicitly at `:391`, which is the thing this bullet
  lists as a requirement; `:361` records why, and it is the trap this bullet
  correctly predicted. So the work is done and the spec never noticed.

  The runtime figure moved with it: **~238s for the whole site**, not ~86s each.

  Kept struck rather than deleted, because a spec that asserts a *confirmed
  absence* of something already present is the same shape as a "do not build"
  row for a thing that ships — and this one would have sent a session to build
  theme handling twice.
- **OG cards** — figures already correct (section 0). The remaining question is
  whether the PNGs need light variants. **Recommendation: no.** They render
  against Discord and Slack chrome, not against our page, so our theme is not
  their ground. One less thing to keep in sync.
- **Prose ceilings** — only if copy is added. `DESIGN.md` is not prose-governed.
- **`DESIGN.md`** is binding and describes one theme. Amended in the same PR
  that introduces the second, per the brief.

### The layered maps: no new geometry code, confirmed

`heroart.paths(slug, box=1000, layer=None, max_paths=None, precision=1)` already
takes the argument. Layer counts read from `zone-geometry.json` match the brief
exactly: `mistmoore` 3, `thehole` 4, `warrens` 1, `planeofhate` 3. Both cautions
hold — cap per-storey draws for Plane of Hate against the home page's
`max_paths=60`, and `warrens` has one layer, so any per-storey UI must degrade
to a single plan rather than render an empty second tab.

### The hero is derivable today

`revamped` is set on exactly one zone — `mistmoore`, 18 August 2026 — so "most
recently revamped" yields the specimen's hero by construction, with no
renumbering. `plate` stays an identifier.

---

## 7. Cinzel — resolved 20 August, and I had this backwards

**This section originally said `DESIGN.md` declares three faces and asked
whether Cinzel was a fourth. That was wrong, and the ruling I received repeated
the error back to me because I put it there.**

`docs/DESIGN.md` line 103 lists **four typefaces** — Cinzel, Saira Condensed,
IBM Plex Mono, Public Sans — and line 160 records the change explicitly:
"~~No fourth typeface.~~ **Four now.** Cinzel holds the top two display levels."
`scripts/check.py`'s `FACES` set has carried all four since Cinzel landed.

So the design brief and the checker agreed the whole time. **The outlier was
`CLAUDE.md`**, which said three — and that is the file a session reads first,
which is why the mistake propagated into a spec, a ruling and back again before
anyone read the two documents side by side.

Corrected in `CLAUDE.md`, in the same PR that introduces the second theme. There
is no `DESIGN.md` amendment to make and no new webfont: Cinzel already ships.

---

## 8. Sequence

Behind live ingestion, per the brief. In order:

1. This spec, ruled on — particularly section 2's accent question, section 1's
   two tools, and section 7's fourth face.
2. `site.css` tokens, plus the gate rule protecting block order and its
   `gate_selftest` case.
3. `_partials.py` toggle; `DESIGN.md` amended in the same PR.
4. Motifs and grounds.
5. `conformance.js` extended to four runs; full sweep before the PR is offered.

A measured session still outranks all of it.
