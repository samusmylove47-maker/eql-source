# Design brief — the aesthetic uplift

The current design is disciplined and correct. It is also monotonous. This brief
says what is load-bearing, what is wrong, and what to do about it.

**Read the whole thing before changing a pixel.** Several of the things that look
like defaults are deliberate.

---

## What is load-bearing — do not change these

**Monochrome chrome, polychrome content.** The frame is bone and graphite. All
colour comes from the material: the ten zone accents, instrument blue for tools,
ember for raids. This is the single decision that keeps the site off the
near-black-plus-one-neon-accent look every fansite lands on. Keep it.

**The ten zone accents are permanent identity.** Each zone owns its colour
forever. `check.py` fails on duplicates. Never reassign one.

**Three faces, no more.** Saira Condensed (display, uppercase, tight tracking),
IBM Plex Mono (data, labels, anything numeric), Public Sans (prose). Adding a
fourth is the classic way to make a considered site look amateur.

**The spectrum.** Ten bars, plate order, zone accents, height keyed to the top of
each level band. Ornament, chart and navigation at once. It is the site's
signature. Improve it; do not replace it.

**Hairlines, no rounded corners, no drop shadows, no gradients on chrome.** The
plate aesthetic is a technical document, not a SaaS dashboard.

**The tier badges.** `.tier` with `.t1`–`.t5`. Tiers 1 and 2 print plain;
3 to 5 always show. This is the site's whole reason for existing made visible.

---

## What is actually wrong

Diagnose it honestly before fixing it:

1. **Every section has the same rhythm.** Section number, heading, lede, row of
   equal-weight cards. Five times down the page. Nothing earns attention because
   everything asks for the same amount.
2. **No hierarchy inside card rows.** Four cards of identical size, so the reader
   has no idea which one matters. The Index is our best tool and it looks exactly
   like the third-best one.
3. **The page reads grey.** Colour discipline has become colour absence. Between
   the spectrum and the tier scale there are long stretches with no colour at all.
4. **Cards are mostly empty space** at desktop width. The type sits small in a
   large box.
5. **No texture, no atmosphere.** This is a fantasy game. The site is a cold
   instrument panel with nothing that says *Norrath*. That is not an argument for
   dragons and parchment — it is an argument for one restrained atmospheric layer.
6. **Almost no motion.** Only the spectrum animates, once, on load.

---

## Direction

### 1. Break the rhythm
Give each band its own shape. Suggested, not prescribed:

- **Hero** — full-bleed, taller, the only place the display face runs above 100px.
- **Commitments** — asymmetric two-column: a large statement left, the four
  numbered items in a narrow right rail. Not a four-across grid.
- **Tier scale** — horizontal, full width, reading as a *scale* rather than five
  boxes. Consider a continuous bar with five stops, where the colour ramp itself
  carries the meaning.
- **Tools** — one hero card at double width (The Index), three smaller beneath.
- **Raids** — let the ember carry a dark full-bleed band. This is the one section
  that should feel like a boss fight.
- **Dungeons** — spectrum-led, minimal text.
- **Gaps** — quiet, small, deliberately understated. Honesty does not shout.

### 2. Introduce one atmospheric layer, and only one
Options, pick one and commit:

- A very low-opacity **contour/topographic line motif**, derived from the shapes
  already in the navigation maps. Justified because the site is a survey.
- A subtle **grain overlay** at 2–4% opacity, which warms flat dark fields
  considerably and costs nothing.
- A **coordinate grid** wash behind the hero only, echoing `/loc` readings.

Requirements: under 8 KB, no images if it can be SVG or CSS, must not reduce text
contrast below WCAG AA, must respect `prefers-reduced-motion`.

### 3. Use the zone accents more
Ten good colours sit unused outside the spectrum. Ideas: tint the dungeon rows on
hover with their own accent; let the plate number take the accent; use accent
hairlines rather than grey ones in zone contexts.

### 4. Earn some motion
Restrained and orchestrated, never decorative:

- Section headings and first cards fade-rise on scroll, staggered, once.
- Card hover: a 2px accent bar grows from left, not a lift-and-shadow.
- The spectrum bars respond to hover with a readout of that zone's level band.

Everything must be disabled under `prefers-reduced-motion: reduce`.

### 5. Density and hierarchy
Tighten card padding at desktop. Increase the size gap between a hero card and a
supporting one — a 2:1 visual weight difference, not the current 1:1. Let some
numbers be genuinely large; the index strip figures could be twice their size.

---

## Constraints

- **No framework.** No React, no Tailwind, no build step beyond the Python
  generators. Hand-written CSS in `assets/site.css`.
- **No web fonts beyond the three already loaded.**
- **No CDN.** `check.py` fails the build on one. Vendor anything new.
- **Every page must still pass `check.py`.**
- **Mobile first-class.** Test at 390px. Zero horizontal overflow is a hard
  requirement, currently met everywhere.
- **The four tools are single-file apps** with their own inline styling. They are
  *not* restyled by `assets/site.css`. Treat them as a separate, later pass, and
  keep their internal palettes recognisably theirs.

---

## How to verify you improved it

Take a full-page screenshot before and after at 1440px and at 390px. Then answer,
in writing:

1. Can you tell at a glance which tool is the most important one?
2. Does any two consecutive bands share the same layout shape?
3. Is there colour in the top third of the page other than the hero text?
4. Does it still look like a technical instrument rather than a fantasy fansite?

If the answer to 4 is no, you have gone too far. Pull back.
