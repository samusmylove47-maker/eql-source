# Design brief

**Goal: a professional reference site with its own identity.** Modern, clean,
crisp, impressive. Not bloated, not gaudy. Desktop is the primary target.

This brief replaces the previous one, which was written in a Claude Code session
and asserted a specific flat aesthetic as law — no radii, no shadows, no
gradients, "a technical document, not a SaaS dashboard". Those were never the
owner's requirements. They are the direct cause of the site reading as barren
and utilitarian, and they are withdrawn.

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

- **The ten zone accents** and the spectrum built from them.
- **The survey plate** — coordinates, `/loc` readings, room lists, measured
  drawings. The hand-drawn SVG maps are 1,461 lines of bespoke geometry and are
  the most valuable thing on the site.
- **The tier badges** — a published, visible standard of evidence.
- **The 3D encounter viewer.**

**So: a survey, not a fansite.** The reference for a world, drawn precisely.
Instruments, plates, measured colour. What that must *not* mean is a flat
brutalist manifesto — that was the old brief's mistake. Aim for a well-made data
product: quiet, dense, confident, with real hierarchy.

---

## 3. What is load-bearing

Do not change these. They are the identity.

- **Monochrome frame, colour from content.** All colour comes from the material:
  ten zone accents, instrument blue for tools, ember for raids.
- **Each zone owns its accent permanently.** `check.py` fails on duplicates.
- **The spectrum** — one bar per zone, plate order, height keyed to the top of
  its level band. Improve it; do not replace it.
- **The tier badges**, `.tier` with `.t1`–`.t5`.
- **Three typefaces**, no more: Saira Condensed (display), IBM Plex Mono (data
  and labels), Public Sans (prose).
- **WCAG AA on all text.** The site now measures clean across 11,942 text nodes
  on 25 pages. Do not regress it. Accents that fail as text get a lifted variant;
  the accent itself is never reassigned.

---

## 4. What is now permitted

The old bans are lifted, replaced by taste rules. Each of these is allowed
*because* it builds hierarchy, and only in service of that.

**Elevation.** Surfaces may sit above one another, expressed as a change of
background value plus a hairline, and optionally a large soft shadow at very low
opacity. Never a hard drop shadow, never more than three levels.

**Radii.** A small consistent radius is permitted — pick one value in the 3–6px
range and use it everywhere. Not pills, not circles, not mixed radii.

**Gradients.** Permitted only as near-imperceptible surface modulation — a
one-or-two-step shift across a large panel. Never a coloured gradient as
decoration, never on text, never a "hero gradient".

**Motion.** Permitted where it explains something: a state change, a reveal, a
hover affordance. Never decorative, never looping, always disabled under
`prefers-reduced-motion`.

**Density.** Tighten. The current cards are mostly empty space at desktop width.

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

**Lead with the material.** The spectrum and the ten plates are the strongest
thing the site has. They belong at the top, not in section 04. A visitor should
reach the reference before they reach the philosophy.

**Move the epistemology.** The four commitments and the tier scale are important
and should stay on the site — but as a page of their own, linked prominently,
not as the first thing between a visitor and the data. The tier badges do the
explaining in place, which is the point of having them.

**Break the rhythm.** No two consecutive bands should share a layout. Give the
spectrum full width. Let the tools band lead with one large card. Let raids run
dark and full-bleed in ember.

**Establish a scale.** The site currently uses 21 distinct font sizes, including
9, 9.5, 10, 10.5, 11 and 11.5 — differences nobody can see, multiplying
maintenance. Reduce to a single scale of 7–9 steps and use only those. Same for
spacing: one scale, used everywhere.

**Unify the plates with the site.** The ten plates and five maps do not load
`assets/site.css` at all. They carry their own 65-line stylesheet, byte-identical
across all fifteen files, which re-declares its own greys, panels and type rules
— and collides with the shared system on `.eyebrow`, `.lede`, `.note`, `code`
and `:focus-visible`. **This is the largest structural problem on the site.**
Fixing it is a two-step change: link the stylesheet, then delete the page-local
block. Do it in that order, verify one plate, then roll it out.

Do not touch the SVG map geometry.

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

Six must be no. If four is no, the restructure has not happened yet.
