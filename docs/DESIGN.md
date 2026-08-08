# Design brief

**Goal: a professional reference site with its own identity.** Modern, clean,
crisp, impressive. Not bloated, not gaudy. Desktop is the primary target.

**The site must be good to look at. That is a requirement, not a finishing
touch.** It sits alongside being functional, verifiable and transparent — not
beneath them. A reference nobody enjoys opening does not get opened, and a
standard of evidence nobody reads persuades nobody. Beauty and rigour are not in
tension here; the rigour is the subject matter, and the design is how it earns
attention.

## The rejected direction

This brief replaces one written in a Claude Code session, which asserted a
specific flat aesthetic as law: no radii, no shadows, no gradients, hairlines
only, "a technical document, not a SaaS dashboard", and a final test asking
whether the result still looked like a technical instrument — with instructions
to *pull back* if it had become too visually appealing.

**That direction is rejected outright, not merely relaxed.** It was never the
owner's requirement, and it produced exactly what it promised: flat, barren,
spartan. Every surface on one plane, every element the same weight, nothing
drawing the eye anywhere.

Restraint is not the same thing as absence. A disciplined palette, a tight type
scale and generous space are restraint. Refusing depth, contrast and focal
weight is just an unfinished page. **Where this brief and the old one disagree,
this one wins, and the old instinct to strip things back should be actively
resisted.**

---

## 1. The problem to solve

The site currently looks like it was generated, because it was. The tells are
specific and each one is fixable.

1. **It explains itself before it shows you anything.** The home page opens with
   a mission statement, then "What we are trying to do", then four numbered
   commitments, then a tier scale — four screens of epistemology before a single
   piece of reference. A reference site earns trust by being useful first.
2. **Numbered section headings** — `01`, `02`, `03`, `04`, `05` down the page.
3. **A row of stat tiles** near the top: four tools, 452 items, 208 named, ten
   plates, eight gaps. Generic landing-page furniture.
4. **Every band is the same shape.** Heading, lede, row of equal-weight cards,
   five times. Nothing is more important than anything else.
5. **Every card is the same card**: kicker, title, paragraph, footer row with a
   right-aligned arrow.
6. **The prose declares.** "This site exists to be the version you can trust."
   Show it instead.
7. **No depth at all.** Every surface is on one plane, so the eye has nothing to
   follow.

**Test for the whole job:** someone who has never seen the site should not be
able to tell it was built with an AI assistant.

---

## 2. The identity

The site's identity is already in its material, and nothing else has it:

- **The ten zone accents**, used as fields rather than as trim.
- **The survey plate** — coordinates, `/loc` readings, room lists, measured
  drawings. The hand-drawn SVG maps are 1,461 lines of bespoke geometry and are
  the most valuable thing on the site.
- **The tier badges** — a published, visible standard of evidence.
- **The 3D encounter viewer.**

**So: a survey, not a fansite.** The reference for a world, drawn precisely —
instruments, plates, measured colour.

Read that as a *subject*, not as a licence to be austere. The old brief made
exactly that mistake: it took "technical" to mean stripped, and produced
something that looks unfinished rather than exacting. A surveyor's chart, a
well-set atlas and a good instrument panel are all beautiful objects, and they
are beautiful *because* of their precision, not in spite of it.

The target is a well-made data product: dense, confident, deliberate, with real
hierarchy and real depth — something a visitor notices is well built before they
have read a single figure.

---

## 3. What is load-bearing

Do not change these. They are the identity.

- **Monochrome frame, colour from content.** All colour comes from the material:
  ten zone accents, instrument blue for tools, ember for raids.
- **Each zone owns its accent permanently.** `check.py` fails on duplicates.
- **The plate cards** — one per zone, accent-washed, plate number cropped by the
  card edge, contour rings anchored to a different corner on each. This is the
  home page's signature and the visual language the rest of the page extends.
- **The tier badges**, `.tier` with `.t1`–`.t5`.
- **Three typefaces**, no more: Saira Condensed (display), IBM Plex Mono (data
  and labels), Public Sans (prose).
- **WCAG AA on all text.** The site now measures clean across 11,942 text nodes
  on 25 pages. Do not regress it. Accents that fail as text get a lifted variant;
  the accent itself is never reassigned.

---

## 4. What the design must do

These are requirements, not permissions. A stage that ships without them has not
met the brief.

**Build depth.** The page must have a visible hierarchy of surfaces — the reader
should be able to tell what sits on top of what without reading a word. Express
it as a change of background value plus a hairline, and a large soft shadow at
low opacity where a surface genuinely floats. Cap it at three levels. What is
banned is the *hard* drop shadow of a 2010s card, not depth itself.

**Soften the geometry.** One small radius, chosen once in the 3–6px range, used
everywhere. Not pills, not circles, not mixed values. Sharp corners everywhere
is a style, and it is the style being replaced.

**Give the eye somewhere to go.** Every screen needs a clear first thing. That
means real contrast in size and weight — a 2:1 visual difference between a
primary card and a supporting one, not the current 1:1. Some numbers should be
genuinely large.

**Use the colour you already own.** Ten good accents currently appear in one
element on one page. They should tint rows on hover, mark plate numbers, carry
accent hairlines in zone context. The frame stays monochrome; the material is
where colour lives.

**Modulate large surfaces.** A one-or-two-step gradient across a big panel to
keep it from reading as dead flat. Never a coloured gradient as decoration,
never on text, never a hero gradient.

**Move with purpose.** Motion where it explains something — a state change, a
reveal, a hover affordance. Never decorative, never looping, always disabled
under `prefers-reduced-motion`.

**Tighten.** The current cards are mostly empty space at desktop width.

### The failure mode to watch for

If a stage lands and the page still reads as flat, grey and evenly weighted, the
work has not been done — regardless of how disciplined the CSS looks. That is the
old brief reasserting itself. The correct response is to add hierarchy, not to
justify its absence as restraint.

---

## 5. What stays out

- No fourth typeface.
- No colour outside the system.
- No illustration, stock art, or generated imagery.
- No icon set. The site has no need for icons and they date badly.
- Nothing that shouts: no oversized hero gradient, no glow, no glass, no
  animated background.
- No framework. Hand-written CSS in `assets/site.css`. No CDN — `check.py`
  fails the build on one.

---

## 6. Direction

**Lead with the material.** The ten plates are the strongest thing the site has.
They belong at the top, not in section 04. A visitor should
reach the reference before they reach the philosophy.

**Move the epistemology.** The four commitments and the tier scale are important
and should stay on the site — but as a page of their own, linked prominently,
not as the first thing between a visitor and the data. The tier badges do the
explaining in place, which is the point of having them.

**Break the rhythm.** No two consecutive bands should share a layout. Give the
the plate grid room to breathe. Let the tools band lead with one large card. Let raids run
dark and full-bleed in ember.

**Establish a scale.** The site currently uses 21 distinct font sizes, including
9, 9.5, 10, 10.5, 11 and 11.5 — differences nobody can see, multiplying
maintenance. Reduce to a single scale of 7–9 steps and use only those. Same for
spacing: one scale, used everywhere.

**Unify the plates with the site.** The ten plates and five maps do not load
`assets/site.css`. They carry their own 65-line stylesheet — verified
byte-identical across all fifteen files apart from line 11, which sets the zone
accent. **This is the largest structural problem on the site.**

**It is not a matter of deleting that block.** An inventory established that
`site.css` styles no bare `h1`, `h2`, `section`, `table`, `th`, `td` or
`footer` — it only ever styles `h1.display`, `h2.sec` and `section.band`. The
plates contain 4,224 `<td>`, 104 `<section>`, 104 `<h2>`, 66 `<table>` and 15
`<footer>` elements that would lose every rule they have. Removing the block
first would strip the plates bare.

The order is the reverse:

1. **Absorb before linking.** Move the plate block's element rules — tables,
   bare headings, sections, footer — into `site.css`, expressed in tokens.
2. **Reconcile the greys.** Five structural colours in the plates sit *between*
   the shared ramp's rungs rather than on one: `#12171A`, `#1A2126`, `#232C32`,
   `#2E3A41` and `#8A9998`. Each needs a deliberate decision, not a nearest-match.
3. **Rename the two modifiers.** The plates call them `.danger` and `.fresh`;
   `site.css` calls the same idea `.note.warn` and `.note.ok`, with *identical*
   colour values. Renaming 95 elements merges those rules at zero visual cost.
   `.note.key`, used 6 times, has no counterpart and needs one.
4. **Then** link `site.css` and remove what is now duplicated, one plate first.

Two findings that make this safer than it sounds. The plates contain **no `<a>`
elements at all**, so link styling cannot regress. And every one of the 670 SVG
`<text>` elements specifies its own family and size, so no stylesheet change can
reach the drawings — with one exception to check by eye rather than by
reasoning: the plates set `svg{width:100%}` and `site.css` sets
`max-width:100%`, and the drawings carry a `viewBox` with no width or height.

Do not touch the SVG map geometry.

**On generating maps.** The project holds 208 recorded named-mob coordinates and
`dungeons/plots.html` now draws all of them to scale on a measured grid. What it
deliberately does not draw is walls, rooms or corridors — that geometry is not in
the data, and a floor plan invented around real coordinates would look
authoritative while being a guess. Twenty-seven of the 208 are recorded as
wandering, variable or simply not taken; those are listed under each plot rather
than placed somewhere plausible, so the plot never silently under-reports a zone.

A hand-drawn map is a different artefact and needs a different input: either
in-game survey work, or an existing map used as reference. That is the owner's
call, not something to infer.

---

## 7. Order of work

Each stage is a pull request, reviewed against a local preview before the next
begins.

1. **Foundation.** Type scale, spacing scale, elevation levels, radius value.
   No layout change. The site should look almost identical and be far easier to
   change.
2. **Plate unification.** Link `site.css`, remove the page-local block, verify
   one plate end to end, then the rest.
3. **Home page.** Restructure to lead with the material; move the epistemology
   to its own page; drop the numbered sections and the stat tiles.
4. **Cards and hierarchy.** One card system with real size tiers.
5. **Raids and tools bands.**
6. **Motion pass.**
7. **Interior pages** — tools, raids, dungeons and sources indexes.

---

## 8. Constraints

- `check.py` must pass at every stage.
- **Zero horizontal overflow at 390px.** Currently met; it is a hard requirement.
- **Desktop leads.** Where a trade-off exists, the desktop reading wins, but
  mobile must not break.
- **The four tools are single-file apps** with their own inline styling and their
  own palettes. They are a separate pass, and their palettes should stay
  recognisably theirs.
- The plates are **deliberately ungraded** for source tier right now. A later
  phase will verify and grade them. Do not add tier badges to them as part of
  design work.

---

## 9. How to tell it worked

Answer in writing, with a local preview open at 1440px and 390px:

1. Can you tell at a glance which tool matters most?
2. Do any two consecutive bands share a layout?
3. Is there colour above the fold other than in the hero text?
4. Does a visitor reach reference material before philosophy?
5. Is there a visible hierarchy of surfaces, or is everything on one plane?
6. Could a stranger tell this was built with an AI assistant?
7. **Is it good to look at?** Would you send someone the link because the page
   itself is worth seeing, not only because the data is useful?

Six must be no. Seven must be yes — and it is the one that decides whether the
brief was met. If four is no, the restructure has not happened. If five or seven
is no, the old flat direction has crept back in; add hierarchy rather than
defending the absence of it.

**There is no "too visually appealing" failure state.** The old brief had one,
and it was wrong. The only aesthetic failures available here are gaudy, cluttered
and generic — none of which is the same as attractive.


---

## 10. Withdrawn: the spectrum

A row of ten coloured bars, one per zone, sized by level band, sat on the home
page until 2026-08-08. The previous brief called it "the signature" and said to
improve it rather than replace it.

It was withdrawn by the owner after seeing it in place, for a reason that is
worth recording because it applies to anything built next: **it did not scale.**
Ten bars read as a chart; thirty read as clutter, and every zone in the game is
eventually getting revamped and surveyed. A signature element that breaks when
the project succeeds is the wrong signature.

The zone accents themselves were never the problem and are more prominent now
than they were — as fields on the plate cards rather than as bars.
