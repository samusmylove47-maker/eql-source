# Atlas field guide

Binding brief: `docs/DESIGN.md`. This page is the implementer’s do/don’t so the
cartography system does not drift.

## Two readings of one chart

The **atlas** (default) is daylight vellum: cream paper, iron-gall ink, leather
chrome. The **dungeon** reading (`html[data-theme="dungeon"]`, or a stored
preference, or `prefers-color-scheme: dark` when the reader has not chosen) is
the measured umber-black ground from Norrath’s textures. Same tokens, inverted
roles. Zone accents are never reassigned; on paper they become inks, and where
they fail as text they are mixed toward `--bone`.

Toggle lives in the masthead. Preference is `localStorage` key `eql-theme`.
Audio is not shipped — a parchment rustle or page-turn would be optional and
must stay behind an explicit control if it is ever added.

## Faces (four, no more)

| Role | Face |
|---|---|
| Display, illuminated initials, plate numerals | Cinzel |
| Dense UI, card titles, table names | Saira Condensed |
| Nav, badges, coordinates | IBM Plex Mono |
| Body prose | Source Serif 4 |

## Surfaces

`--surface-0/1/2` are the page, a panel, a lifted panel. `--bind*` is the
leather chrome and is **the same in both themes**. Floor plans keep a dark
`--plot-bg` inset on the sheet so mesh line-work drawn for a dark ground stays
readable.

## Components

- `.sheet` / `.wrap` — the paper leaf (surveys, raids index, Sky)
- `.mast` / `.plateno` / `.strip` — cartouche title block
- `.plate` — zone card: accent wash, cropped number, real mesh thumbnail
- `.site-bar` / `.ns-bar` — leather index
- `.cm` / `.note` / `.kick` — marginalia
- `.fplan` — dungeon plan; JS selectors are load-bearing (`data-lyr`, `.mk`, `.fp-*`)

## Honesty

Compass roses, neatlines, scale bars and rhumb-like rules belong in **chrome**.
They must not sit on a floor plan in a way that could be read as rooms, secret
doors, or unmeasured geography. Do not generate coastlines of Norrath. The art
is `assets/zone-geometry.json`. Files under `public/assets/ornament/` are the
marks: a compass rose, a neatline frame, a cartouche corner. They are never
evidence.

## Motion

`--speed` is the only duration for hovers. The hero mesh may draw itself in.
`prefers-reduced-motion` kills animation globally and must leave the drawing
visible (stroke already drawn). Theme changes do not require a view transition.

## Checks

After touching `site.css` or chrome: `./build.sh` then `python3 scripts/check.py`.
After touching a tool’s CSS/JS: `node scripts/toolsmoke.js`. Zero horizontal
overflow at 390px. WCAG AA on both themes.
