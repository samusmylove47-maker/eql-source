"""The Castle Mistmoore chart — every line and every mark read from the data.

    python _build/mistmoorecarto.py        # run by hand, then commit the result

WHY THIS EXISTS AT ALL
----------------------
_build/source/mistmoore-map.html is a hand-authored page: build3.py imports it
verbatim and injects chrome, and it takes no substitutions. So anything drawn on
it has to be *in* it. Until 17 Aug 2026 that meant a hand-drawn SVG of 33 paths
and 48 invented dots, sitting on a site whose whole argument is that it measures
things — while assets/zone-geometry.json held the zone's real walkable floor,
read out of the game's own .s3d meshes.

This closes that. It reads the geometry, the recorded /loc values and the plan
bounds, renders the chart, and writes it back into the source page between
sentinel comments. **No coordinate on that page is typed by a person.** Re-run it
after any change to zone-geometry.json or the survey's coordinates and diff; if
the page moves, the page was stale.

It is deliberately outside build.sh, for _build/geometry.py's reason: the
authored page is the thing a human edits, and a build step that rewrote it every
run would fight the author. Same category as geometry.py, ogcards.py and
palette.py — hand-run, output committed.

THE TRANSFORM, WHICH IS THE ONLY PART THAT IS EASY TO GET WRONG
---------------------------------------------------------------
`/loc` returns **Y, X, Z**. North is +Y and west is +X, and the site draws north
up and west left, so BOTH axes invert into page space: page_x = -X, page_y = -Y.
_build/geometry.py already stores the floor lines in that inverted space, which
is the only reason a mesh line and a recorded /loc can share one viewBox. The
graticule below therefore prints -page as the game's own axis value, so a reader
can read a /loc straight off the chart.

Imported from plans.py rather than restated: `locate()` also refuses a range
("718-800, 212-236" is a span, not a position) and handles U+2212 MINUS SIGN,
which 141 of the site's recorded coordinates use.

WHAT IS DELIBERATELY NOT DRAWN
------------------------------
The train funnel band, the one-way tomb-to-jail path and 48 "population spawn
point" dots were on the old drawing and are not here. None of them has a
recorded position. A drawing is an assertion, and those were assertions the data
does not make. They are named as unrecorded in the page's caveats instead.
"""
import json, math, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from plans import locate, NUM, RANGE

SLUG = 'mistmoore'
PAGE = '_build/source/mistmoore-map.html'

# The zone's permanent accent, read from the index rather than typed. Content
# colour only: the chrome of the chart stays monochrome, per docs/DESIGN.md.
Z = {z['slug']: z for z in json.load(open('assets/zones-index.json', encoding='utf-8'))}
ACCENT = Z[SLUG]['accent']

GEO = json.load(open('assets/zone-geometry.json', encoding='utf-8'))[SLUG]
BOUNDS = json.load(open('assets/zone-plan-bounds.json', encoding='utf-8'))['zones'][SLUG]
NAMED = [n for n in json.load(open('assets/index-data.json', encoding='utf-8'))['named']
         if n.get('z') == SLUG]

# The zone line, from the survey's own Succor row. A recorded /loc like any
# other; it gets a mark because it is measured, not because it is important.
SUCCOR = '−295, 123'

# Ink. Every one of these already ships on this page and the site measures AA
# across all of them; nothing new is introduced here.
INK      = '#DCD9D6'   # chart line work at full weight
MARG     = '#A59E98'   # graticule and marginalia          6.6:1 on #1E1914
FAINT    = '#9C958E'   # secondary marginalia              5.9:1 on #1E1914
FIELD    = '#1E1914'   # the chart field
RULE     = '#40372D'
ACCENT_T = '#C3828E'   # the accent lifted to pass as text 5.7:1 on #1E1914

X0, Y0 = BOUNDS['x0'], BOUNDS['y0']
W, H = BOUNDS['w'], BOUNDS['h']

# Margins in game units. The chart is drawn in the game's own coordinate space,
# so a margin is a distance in that space too; at the rendered width one unit is
# roughly 0.79px.
ML, MR, MT, MB = 100, 78, 46, 196
VB = (X0 - ML, Y0 - MT, W + ML + MR, H + MT + MB)

TICK = 100          # graticule interval, game units
LABEL_EVERY = 200
SCALE_BAR = 200     # game units


def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


# vector-effect is NOT an inherited property, so putting it on a <g> does
# nothing to the paths inside — the computed value on every child stays "none"
# and the hairlines quietly scale with the drawing. It goes on each stroked
# element, and stroke widths below are therefore real pixels at any size.
VE = ' vector-effect="non-scaling-stroke"'


def path_d(line):
    """One polyline to a path, closed where the mesh closed it."""
    pts = []
    for p in line:
        xy = (p[0], p[1])
        if not pts or xy != pts[-1]:
            pts.append(xy)
    if len(pts) < 2:
        return None
    closed = len(pts) > 2 and line[0] == line[-1]
    d = 'M' + ' L'.join(f'{x} {y}' for x, y in pts)
    return d + 'Z' if closed else d


# Storeys, deepest first. geometry.py sorts them by their lower z already; the
# weights below run light-to-heavy with depth so the composite reads as one
# building rather than as three drawings on top of each other.
STOREY_STYLE = [
    dict(sw=1.10, op=1.00, dash=''),
    dict(sw=0.85, op=0.62, dash=''),
    dict(sw=0.75, op=0.42, dash=' stroke-dasharray="6 4"'),
]


def storey_paths(layer, style):
    ds = [d for d in (path_d(ln) for ln in layer['lines']) if d]
    return (f'<g fill="none" stroke="currentColor" stroke-width="{style["sw"]}" '
            f'stroke-linejoin="round" stroke-linecap="round" '
            f'opacity="{style["op"]:.2f}"{style["dash"]}>'
            + ''.join(f'<path d="{d}"{VE}/>' for d in ds) + '</g>'), len(ds)


def graticule():
    """Ticks and edge labels in the GAME's axes, not the page's.

    page_x = -X and page_y = -Y, so the label printed beside a page coordinate
    is its negation. Getting this backwards would put a plausible-looking wrong
    number on every edge of the chart.
    """
    out = ['<g fill="none" stroke="currentColor" stroke-width="0.8" opacity="0.5">']
    labels = []
    lo = int((X0 // TICK) * TICK)
    px = lo
    while px <= X0 + W:
        if px >= X0:
            long_ = (-px) % LABEL_EVERY == 0
            out.append(f'<path d="M{px} {Y0 + H} L{px} {Y0 + H + (20 if long_ else 11)}"{VE}/>')
            if long_:
                labels.append(f'<text x="{px}" y="{Y0 + H + 45}" text-anchor="middle">'
                              f'{fmt(-px)}</text>')
        px += TICK
    lo = int((Y0 // TICK) * TICK)
    py = lo
    while py <= Y0 + H:
        if py >= Y0:
            long_ = (-py) % LABEL_EVERY == 0
            out.append(f'<path d="M{X0} {py} L{X0 - (20 if long_ else 11)} {py}"{VE}/>')
            if long_:
                labels.append(f'<text x="{X0 - 27}" y="{py + 6}" text-anchor="end">'
                              f'{fmt(-py)}</text>')
        py += TICK
    out.append('</g>')
    out.append(f'<g font-family="IBM Plex Mono, monospace" font-size="17" fill="{MARG}">'
               + ''.join(labels) + '</g>')
    return ''.join(out)


def fmt(v):
    v = int(round(v))
    return ('−' + str(-v)) if v < 0 else str(v)


# ---- marks -----------------------------------------------------------------
# Number labels are placed by trying offsets outward from the station and
# keeping the first whose TEXT BOX clears every station and every label already
# down. Xicotl and Lasna Cheroon stand 18 game units apart and Ssynthi stands 25
# from the undead knight, so a fixed offset overprints one label on the other —
# and a centre-to-centre distance test still does, because "21" is twice as wide
# as "2". The boxes are measured, not guessed at.
LABEL_SIZE = 19          # font-size in game units, matching the <text> below
CHAR_W = 11.4            # IBM Plex Mono advance at that size
RINGS = (11, 19)         # station disc, and the outer ring a Level 2 mark adds

OFFSETS = [(17, -13), (17, 21), (-17, -13), (-17, 21),
           (24, 5), (-24, 5), (0, -25), (0, 33),
           (32, -22), (-32, -22), (32, 30), (-32, 30),
           (0, -42), (0, 50), (44, 5), (-44, 5)]


def _box(x, y, dx):
    """The rect a number label occupies, in game units, for a given anchor."""
    def rect(n):
        w = CHAR_W * len(str(n))
        left = x if dx > 0 else x - w if dx < 0 else x - w / 2
        return (left, y - LABEL_SIZE * 0.78, w, LABEL_SIZE * 1.02)
    return rect


def _hits(r, boxes, discs):
    x, y, w, h = r
    for bx, by, bw, bh in boxes:
        if x < bx + bw and x + w > bx and y < by + bh and y + h > by:
            return True
    # nearest point on the rect to the disc centre
    for cx, cy, cr in discs:
        nx = min(max(cx, x), x + w)
        ny = min(max(cy, y), y + h)
        if (cx - nx) ** 2 + (cy - ny) ** 2 < cr ** 2:
            return True
    return False


def place_labels(marks):
    discs = [(x, y, RINGS[1] + 3 if m['lvl2'] else RINGS[0] + 3)
             for _, x, y, m in marks]
    boxes, out = [], []
    for n, x, y, _ in marks:
        chosen = None
        for dx, dy in OFFSETS:
            r = _box(x + dx, y + dy, dx)(n)
            if not _hits(r, boxes, discs):
                chosen = (dx, dy, r)
                break
        if chosen is None:                      # nowhere clear: keep the default
            dx, dy = OFFSETS[0]
            chosen = (dx, dy, _box(x + dx, y + dy, dx)(n))
        dx, dy, r = chosen
        boxes.append(r)
        out.append((n, x + dx, y + dy,
                    'end' if dx < 0 else 'start' if dx > 0 else 'middle'))
    return out


# GATE 3, APPLIED TO THIS DRAWING.
#
# docs/SOURCES.md's third verification gate asks that every recorded coordinate
# land within 120 game units of drawn floor. It is the check the hand plots had
# nothing to check against, and it is the one that catches the mistake this
# drawing is most exposed to: page_x = -X and page_y = -Y, and getting either
# sign wrong puts a mark in the diagonally opposite corner, looking perfectly
# plausible. A sign error moves a mark by hundreds of units, so the gate finds
# it. This runs the gate at draw time and refuses to write a chart that fails.
GATE = 120


def _segments():
    return [(a[0], a[1], b[0], b[1])
            for L in GEO['layers'] for ln in L['lines']
            for a, b in zip(ln, ln[1:])]


def floor_distance(px, py, segs):
    """Distance from a plotted position to the nearest drawn floor edge."""
    best = float('inf')
    for x1, y1, x2, y2 in segs:
        dx, dy = x2 - x1, y2 - y1
        t = 0.0 if dx == dy == 0 else max(0.0, min(
            1.0, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
        best = min(best, math.hypot(px - (x1 + t * dx), py - (y1 + t * dy)))
    return best


def collect():
    """Every named the survey records, split into plotted and unrecorded."""
    plotted, missing = [], []
    for m in NAMED:
        loc = (m.get('loc') or '').strip()
        pos = locate(BOUNDS, loc) if loc else None
        if pos:
            v = [t.replace('−', '-') for t in NUM.findall(loc)]
            plotted.append(dict(
                name=m['n'], lv=m.get('lv') or '', slug=m.get('u') or '',
                loc=loc,
                px=-float(v[1]), py=-float(v[0]),
                # "Level 2" is the survey's own storey label. It is a label, not
                # a Z reading, and it is never matched to a measured storey.
                lvl2=bool(re.search(r'Level\s*2', loc)),
                # A third number is only a Z where the string is a bare triple.
                z=(float(v[2]) if len(v) > 2 and not re.search(r'Level', loc) else None),
            ))
        else:
            missing.append(dict(name=m['n'], lv=m.get('lv') or '',
                                loc=loc or 'not recorded'))
    return plotted, missing


def main():
    plotted, missing = collect()
    layers = GEO['layers']
    zlo = min(L['z'][0] for L in layers)
    zhi = max(L['z'][1] for L in layers)

    segs = _segments()
    for m in plotted:
        m['off'] = floor_distance(m['px'], m['py'], segs)
    worst = max((m['off'] for m in plotted), default=0.0)
    bad = [m for m in plotted if m['off'] > GATE]
    if bad:
        for m in bad:
            print(f'  ! {m["name"]} /loc {m["loc"]} is {m["off"]:.0f} units from '
                  f'any drawn floor, past the {GATE}-unit gate')
        raise SystemExit('refusing to draw: a mark the mesh does not support')

    # ---- the composite chart ------------------------------------------------
    body = []
    body.append(f'<rect x="{X0:.0f}" y="{Y0:.0f}" width="{W:.0f}" height="{H:.0f}" '
                f'fill="{FIELD}" stroke="none"/>')
    npaths = 0
    for L, st in zip(layers, STOREY_STYLE):
        g, n = storey_paths(L, st)
        body.append(g)
        npaths += n
    body.append(graticule())
    # neatline, then the plate border outside it
    body.append(f'<rect x="{X0:.0f}" y="{Y0:.0f}" width="{W:.0f}" height="{H:.0f}" '
                f'fill="none" stroke="{MARG}" stroke-width="1.5" '
                f'vector-effect="non-scaling-stroke"/>')
    bx, by = VB[0] + 7, VB[1] + 7
    bw, bh = VB[2] - 14, VB[3] - 14
    body.append(f'<rect x="{bx:.0f}" y="{by:.0f}" width="{bw:.0f}" height="{bh:.0f}" '
                f'fill="none" stroke="{RULE}" stroke-width="3" '
                f'vector-effect="non-scaling-stroke"/>')
    body.append(f'<rect x="{bx + 9:.0f}" y="{by + 9:.0f}" width="{bw - 18:.0f}" '
                f'height="{bh - 18:.0f}" fill="none" stroke="{RULE}" stroke-width="1" '
                f'vector-effect="non-scaling-stroke"/>')

    # north mark. +Y is north and page_y = -Y, so north is up the page.
    nx, ny = X0 + W - 52, Y0 + 52
    body.append(
        f'<g fill="none" stroke="{MARG}" stroke-width="1.2">'
        f'<path d="M{nx} {ny + 44} L{nx} {ny - 30}"{VE}/>'
        f'<path d="M{nx - 11} {ny - 14} L{nx} {ny - 30} L{nx + 11} {ny - 14}"{VE}/>'
        f'<circle cx="{nx}" cy="{ny + 44}" r="5"{VE}/></g>'
        f'<text x="{nx}" y="{ny + 74}" text-anchor="middle" '
        f'font-family="IBM Plex Mono, monospace" font-size="18" fill="{MARG}" '
        f'letter-spacing="2">N</text>')

    # scale bar, in the game's own units
    sx, sy = X0, Y0 + H + 74
    body.append(
        f'<g fill="none" stroke="{MARG}" stroke-width="1.2">'
        f'<path d="M{sx} {sy - 9} L{sx} {sy + 9} M{sx + SCALE_BAR} {sy - 9} '
        f'L{sx + SCALE_BAR} {sy + 9} M{sx} {sy} L{sx + SCALE_BAR} {sy}"{VE}/></g>'
        f'<rect x="{sx}" y="{sy - 5}" width="{SCALE_BAR // 2}" height="10" '
        f'fill="{MARG}" opacity="0.55"/>'
        f'<text x="{sx + SCALE_BAR + 14}" y="{sy + 6}" '
        f'font-family="IBM Plex Mono, monospace" font-size="17" fill="{MARG}">'
        f'{SCALE_BAR} game units</text>')

    # marginalia, bottom left under the scale bar
    marg = [
        (f'Floor from the game mesh &#183; {len(layers)} storeys, {npaths} outlines', MARG),
        (f'Height &#8722;{-zlo} to &#8722;{-zhi}, {zhi - zlo} units of relief '
         f'&#183; axes are the game&#8217;s own, +Y north, +X west', FAINT),
        (f'Every mark falls within {worst:.0f} units of drawn floor '
         f'&#183; the survey gate allows {GATE}', FAINT),
    ]
    for i, (t, c) in enumerate(marg):
        body.append(f'<text x="{X0:.0f}" y="{Y0 + H + 112 + i * 26:.0f}" '
                    f'font-family="IBM Plex Mono, monospace" font-size="16" fill="{c}">'
                    f'{t}</text>')

    # ---- the marks ----------------------------------------------------------
    marks, key = [], []
    for i, m in enumerate(plotted, 1):
        marks.append((i, m['px'], m['py'], m))
    body.append(f'<g stroke="{ACCENT}" fill="none" stroke-width="1.2">')
    for i, x, y, m in marks:
        body.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="11"{VE}/>')
        if m['lvl2']:
            body.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="19"{VE}/>')
    body.append('</g>')
    body.append(f'<g fill="{ACCENT}" stroke="none">')
    for i, x, y, m in marks:
        body.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4.5"><title>'
                    f'{esc(m["name"])} &#183; /loc {esc(m["loc"])}</title></circle>')
    body.append('</g>')
    body.append(f'<g font-family="IBM Plex Mono, monospace" font-size="19" '
                f'font-weight="600" fill="{ACCENT_T}">')
    for n, lx, ly, anch in place_labels(marks):
        body.append(f'<text x="{lx:.0f}" y="{ly:.0f}" text-anchor="{anch}">{n}</text>')
    body.append('</g>')

    # the zone line
    sp = locate(BOUNDS, SUCCOR)
    zin = ''
    if sp:
        v = [t.replace('−', '-') for t in NUM.findall(SUCCOR)]
        zx, zy = -float(v[1]), -float(v[0])
        body.append(
            f'<g fill="none" stroke="{MARG}" stroke-width="1.4">'
            f'<path d="M{zx - 14} {zy} L{zx} {zy - 14} L{zx + 14} {zy} L{zx} {zy + 14}Z"{VE}>'
            f'<title>Zone line to Lesser Faydark &#183; /loc {esc(SUCCOR)}</title></path>'
            f'<path d="M{zx - 5} {zy} L{zx + 5} {zy} M{zx} {zy - 5} L{zx} {zy + 5}"{VE}/></g>'
            f'<text x="{zx}" y="{zy + 40}" text-anchor="middle" '
            f'font-family="IBM Plex Mono, monospace" font-size="17" fill="{MARG}">'
            f'ZONE LINE</text>')
        zin = SUCCOR

    main_svg = (
        f'<svg class="chart" viewBox="{VB[0]:.0f} {VB[1]:.0f} {VB[2]:.0f} {VB[3]:.0f}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="Measured plan of Castle Mistmoore. Walkable floor from the '
        f'game mesh in {len(layers)} storeys, with {len(plotted)} recorded named '
        f'positions numbered to the key." '
        # `color` as a PRESENTATION ATTRIBUTE, never a stylesheet rule. The
        # chart paints its own dark field, so a currentColor falling back to the
        # initial black would draw black lines on near-black ground. A drawing
        # that has to survive a missing stylesheet carries its own ink.
        f'color="{INK}">' + ''.join(body) + '</svg>')

    # ---- the three storey sheets -------------------------------------------
    sheets = []
    m2 = 26
    svb = (X0 - m2, Y0 - m2, W + m2 * 2, H + m2 * 2 + 4)
    # only these two named carry a Z, so only these two can be put on a storey
    zmobs = [(i, m) for i, m in enumerate(plotted, 1) if m['z'] is not None]
    for idx, L in enumerate(layers):
        ds = [d for d in (path_d(ln) for ln in L['lines']) if d]
        here = [(i, m) for i, m in zmobs if L['z'][0] <= m['z'] <= L['z'][1]]
        g = (f'<rect x="{X0:.0f}" y="{Y0:.0f}" width="{W:.0f}" height="{H:.0f}" '
             f'fill="{FIELD}"/>'
             f'<g fill="none" stroke="currentColor" stroke-width="0.8" '
             f'stroke-linejoin="round">'
             + ''.join(f'<path d="{d}"{VE}/>' for d in ds) + '</g>'
             + ''.join(f'<circle cx="{m["px"]:.0f}" cy="{m["py"]:.0f}" r="16" '
                       f'fill="none" stroke="{ACCENT}" stroke-width="1.4" '
                       f'vector-effect="non-scaling-stroke"/>'
                       f'<circle cx="{m["px"]:.0f}" cy="{m["py"]:.0f}" r="6" '
                       f'fill="{ACCENT}"><title>{esc(m["name"])}</title></circle>'
                       for _, m in here)
             + f'<rect x="{X0:.0f}" y="{Y0:.0f}" width="{W:.0f}" height="{H:.0f}" '
               f'fill="none" stroke="{MARG}" stroke-width="1.2" '
               f'vector-effect="non-scaling-stroke"/>')
        marked = (' &middot; ' + ', '.join(esc(m['name']) for _, m in here)) if here else ''
        sheets.append(
            f'<figure class="sheet">'
            f'<svg viewBox="{svb[0]:.0f} {svb[1]:.0f} {svb[2]:.0f} {svb[3]:.0f}" '
            f'xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="Storey {idx + 1} of Castle Mistmoore, {len(ds)} floor '
            f'outlines between height {L["z"][0]} and {L["z"][1]}." '
            f'color="{INK}">{g}</svg>'
            f'<figcaption><b>Storey {idx + 1}</b>'
            f'<span>Z &#8722;{-L["z"][0]} &rarr; &#8722;{-L["z"][1]} '
            f'&middot; {len(ds)} outlines{marked}</span></figcaption>'
            f'</figure>')

    # ---- the key ------------------------------------------------------------
    key_html = '<ol class="key">' + ''.join(
        f'<li><span class="n">{i}</span>'
        f'<a href="../named/{esc(m["slug"])}.html">{esc(m["name"])}</a>'
        f'{" <span class=\"l2\">L2</span>" if m["lvl2"] else ""}'
        f'<span class="lv">{esc(m["lv"])}</span>'
        f'<span class="lc">{esc(m["loc"])}</span></li>'
        for i, m in enumerate(plotted, 1)) + '</ol>'

    miss_html = '<ul class="unrec">' + ''.join(
        f'<li><b>{esc(m["name"])}</b> <span>level {esc(m["lv"])}</span> '
        f'&mdash; recorded as <em>{esc(m["loc"])}</em>, so it is not on the chart</li>'
        for m in missing) + '</ul>'

    l2n = sum(1 for m in plotted if m['lvl2'])
    facts = (
        f'<div class="cell"><dt>Zone line</dt><dd>{esc(zin) if zin else "not recorded"}</dd></div>'
        f'<div class="cell"><dt>Storeys</dt><dd>{len(layers)}<small>from the mesh</small></dd></div>'
        f'<div class="cell"><dt>Floor outlines</dt><dd>{npaths}</dd></div>'
        f'<div class="cell"><dt>Relief</dt><dd>{zhi - zlo}<small>game units</small></dd></div>'
        f'<div class="cell"><dt>Named plotted</dt><dd>{len(plotted)}<small>of '
        f'{len(plotted) + len(missing)} recorded</small></dd></div>'
        f'<div class="cell"><dt>Marked Level 2</dt><dd>{l2n}<small>survey label</small></dd></div>')

    blocks = {
        'FACTS': facts,
        'MAIN': main_svg,
        'STOREYS': ''.join(sheets),
        'KEY': key_html,
        'UNRECORDED': miss_html,
    }

    h = open(PAGE, encoding='utf-8').read()
    written = 0
    for k, v in blocks.items():
        pat = re.compile(f'(<!--CARTO:{k}-->).*?(<!--/CARTO:{k}-->)', re.S)
        h, n = pat.subn(lambda m: m.group(1) + v + m.group(2), h)
        if not n:
            print(f'  ! no sentinel for {k}')
        written += n
    open(PAGE, 'w', encoding='utf-8', newline='\n').write(h)
    print(f'mistmoorecarto: {written} blocks written into {PAGE}')
    print(f'  storeys {len(layers)}  outlines {npaths}  '
          f'relief {zhi - zlo} units ({zlo} to {zhi})')
    print(f'  named plotted {len(plotted)}, unrecorded {len(missing)}, '
          f'survey Level 2 {l2n}, carrying a Z reading {len(zmobs)}')
    print(f'  gate 3: worst mark {worst:.1f} units from drawn floor, '
          f'limit {GATE}, all {len(plotted)} pass')
    print(f'  main chart {len(main_svg) // 1024} KB, '
          f'{len(sheets)} storey sheets {sum(len(s) for s in sheets) // 1024} KB')
    return 0


if __name__ == '__main__':
    sys.exit(main())
