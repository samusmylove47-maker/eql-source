"""Survey plots — recorded coordinates, made readable.

THE PROBLEM THIS SOLVES
-----------------------
The first version of this page was numbered dots against a grid, with a lookup
table underneath. Readers reported it as "just dots on the screen" — accurate,
and useless, because nothing on the drawing told you what you were looking at.

WHAT IS DRAWN, AND ON WHAT AUTHORITY
------------------------------------
Every mark traces to a `/loc` recorded in assets/index-data.json.

- THE FLOOR PLAN is derived from the game's own zone mesh by _build/geometry.py
  and read from assets/zone-geometry.json. It is our own computation of where the
  walkable floor ends, not a copy of any published map. Where a zone stacks, each
  storey is a separate group so the height control can isolate it.
- POINTS are named in place rather than numbered, and coloured by level band, so
  the danger gradient is visible without reading anything.
- REGIONS are convex hulls around mobs that are close together. A hull says
  "these recorded positions sit together". It is NOT a room shape and the legend
  says so.
- A REGION IS ONLY NAMED when at least two of its members' notes independently
  mention the same place. One note agreeing with itself is not evidence, so those
  regions stay unnamed and are labelled by their contents instead.
- SCALE AND COMPASS are drawn because a coordinate means nothing without them.

ORIENTATION
-----------
EverQuest's /loc returns Y, X, Z. The navigation maps in _build/source state the
convention: north up the page, west to the left. +Y is north and +X is west, so
both axes invert to page coordinates.

THE MINUS SIGN
--------------
141 of the recorded coordinates use U+2212 MINUS SIGN, not ASCII hyphen. A plain
`-?\\d+` regex reads every one as positive. Parse with NUM below.
"""
import os, sys, json, re, math, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

Z = json.load(open('assets/zones-index.json', encoding='utf-8'))
IX = json.load(open('assets/index-data.json', encoding='utf-8'))

# Floor plans derived from the game meshes by _build/geometry.py. Committed data
# rather than a build step, because a rebuild must work without the game
# installed. Missing or empty is fine: the plot falls back to points alone.
try:
    GEO = json.load(open('assets/zone-geometry.json', encoding='utf-8'))
except (OSError, ValueError):
    GEO = {}

# Which named drops what. The item records carry their source in `d` as
# "Drelzna · L25", so the mob name is everything before the middle dot. This is
# a join we have always held and never surfaced on the map: a reader looking at
# a marker wants to know what it drops, and until now had to scroll to a table.
DROPS = collections.defaultdict(list)
for _it in IX['items']:
    _src = (_it.get('d') or '').split('·')[0].strip()
    if _src:
        DROPS[(_it['z'], _src)].append(_it['n'])

NUM = re.compile(r'[-−]?\d+(?:\.\d+)?')
def nums(s):
    return [float(t.replace('−', '-')) for t in NUM.findall(s or '')]

# A range is not a coordinate. "718–800, 212–236" is a span the mob appears
# across, and reading its two ends as a Y,X pair put A hiding gnoll 464 units
# outside Lair of the Splitpaw. Ranges join the unplotted list, which already
# exists for mobs that vary by spawn point. Note the en dash, not a hyphen.
RANGE = re.compile(r'\d\s*[–—]\s*\d')

# COORDINATES WITHHELD FROM THE PLOT
# ----------------------------------
# These six are recorded on eqlwiki (read 8 Aug 2026) and are transcribed
# faithfully on the Najena survey — the survey is not wrong about what the source
# says. They are withheld because the position itself cannot be right.
#
# Najena's geometry spans worldY −168..546. Every one of these sits south of
# that, by between 57 and 513 units, which places them outside the dungeon.
#
# The authority is the game's own map file: EverQuest Legends installs najena.txt
# under maps/ in the game directory, 4,144 line segments of first-party geometry
# describing the live zone. Two community map sets drawn independently by
# different cartographers, Brewall and Goodurden, agree with it to within two
# units (−166..544 and −167..546), which is corroboration rather than the source.
#
# The client's label layer, najena_1.txt, carries exactly one label — the zone
# exit. Official maps ship geometry and zone connections, no mob positions. So
# they can show a recorded position is impossible but cannot supply the right one.
#
# What makes it a column problem rather than noise: the X value matches in every
# case, and only Y is out. Brewall's own markers for four of them put them
# inside the zone at the same X — Rathyl −154 against our −670, Ekeros −162
# against −681, BoneCracker +250 against −262, Officer Grush +91 against −385.
#
# No replacement value is published here. Brewall is a tier 4 aggregator of
# classic data and is not authority for a Legends coordinate; it is used only to
# show the recorded figure is impossible, which does not require it to be right.
# One /loc reading per mob closes this.
WITHHELD = {
    ('najena', 'Rathyl'), ('najena', 'Ekeros'), ('najena', 'BoneCracker'),
    ('najena', 'Officer Grush'), ('najena', 'Trazdon'),
    ('najena', 'A Visiting Priestess'),
}

def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&quot;'))

# Region naming. Ordered most specific first; a name is only used when two or
# more member notes agree on it.
PATS = [
    re.compile(r'\bRoom\s+\d+\b', re.I),
    re.compile(r'\b(?:the\s+)?((?:Dead|Live|Secret|Ratman|Frenzy|Undead|Golem|Jail|Throne|Bone)\s+'
               r'(?:Tower|Keep|Vault|Jail|Room|Hall|Yard|Chamber|Wing))\b', re.I),
    re.compile(r'\b(bottom|middle|top|upper|lower)\s+floor\b', re.I),
]

def region_name(notes):
    for p in PATS:
        hits = [m.group(0).strip() for n in notes for m in [p.search(n or '')] if m]
        if len(hits) >= 2:
            best, cnt = collections.Counter(h.lower() for h in hits).most_common(1)[0]
            if cnt >= 2:
                for h in hits:
                    if h.lower() == best:
                        return h[0].upper() + h[1:]
    return None

def lvl_of(s):
    v = nums(s)
    return sum(v[:2]) / len(v[:2]) if v else None

def cluster(pts, eps):
    par = list(range(len(pts)))
    def f(a):
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if math.dist(pts[i][:2], pts[j][:2]) <= eps:
                ra, rb = f(i), f(j)
                if ra != rb: par[rb] = ra
    g = collections.defaultdict(list)
    for i in range(len(pts)): g[f(i)].append(i)
    return list(g.values())

def hull(points):
    """Convex hull, monotone chain. Returns [] for fewer than 3 points."""
    p = sorted(set(points))
    if len(p) < 3: return []
    def half(ps):
        out = []
        for q in ps:
            while len(out) >= 2 and ((out[-1][0]-out[-2][0])*(q[1]-out[-2][1]) -
                                     (out[-1][1]-out[-2][1])*(q[0]-out[-2][0])) <= 0:
                out.pop()
            out.append(q)
        return out
    return half(p)[:-1] + half(p[::-1])[:-1]

def expand(poly, pad):
    cx = sum(x for x, _ in poly) / len(poly)
    cy = sum(y for _, y in poly) / len(poly)
    out = []
    for x, y in poly:
        d = math.hypot(x - cx, y - cy) or 1
        out.append((x + (x - cx) / d * pad, y + (y - cy) / d * pad))
    return out

def lift(hexc, pct=0.56):
    """Accent blended toward bone, for text on the plot's dark field. The raw
    accents are chosen as chrome; two of the ten fall below AA as small text."""
    a=[int(hexc[i:i+2],16) for i in (1,3,5)]; b=[0xE6,0xE9,0xE4]
    return '#%02X%02X%02X' % tuple(round(a[i]*pct+b[i]*(1-pct)) for i in range(3))

ON_FLOOR = 120          # world units; a mob this close to drawn floor is on the map

def seg_dist(px, py, a, b):
    """Distance from a point to a line segment."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = dx * dx + dy * dy
    t = 0.0 if L == 0 else max(0.0, min(1.0, ((px - a[0]) * dx + (py - a[1]) * dy) / L))
    return math.hypot(px - (a[0] + t * dx), py - (a[1] + t * dy))

def nice_step(span):
    for s in (25, 50, 100, 250, 500, 1000):
        if span / s <= 10: return s
    return 2000

# level band -> colour. Cool where it is safe, hot where it is not.
def band_colour(lv, lo, hi):
    if lv is None or hi == lo: return '#7FB2C7'
    t = max(0.0, min(1.0, (lv - lo) / (hi - lo)))
    stops = [(0.0, (95,163,126)), (0.5, (217,162,39)), (1.0, (201,69,58))]
    for i in range(len(stops) - 1):
        a, b = stops[i], stops[i+1]
        if a[0] <= t <= b[0]:
            k = (t - a[0]) / (b[0] - a[0] or 1)
            c = [round(a[1][j] + (b[1][j] - a[1][j]) * k) for j in range(3)]
            return '#%02X%02X%02X' % tuple(c)
    return '#C9453A'

def layer_of(px, py, layers):
    """Which storey a plan position belongs to.

    Most recorded coordinates are two-value with no Z, so the storey cannot be
    read off the coordinate — it is inferred from which drawn floor the position
    sits nearest. Where storeys overlap in plan view this can only be a best
    guess, and the survey says so rather than implying we know.

    Returns (index of nearest layer, distance to it).
    """
    best, best_d = None, None
    for i, L in enumerate(layers):
        segs = [sg for c in L['lines'] for sg in zip(c, c[1:])]
        if not segs:
            continue
        d = min(seg_dist(px, py, a, b) for a, b in segs)
        if best_d is None or d < best_d:
            best, best_d = i, d
    return best, best_d



# MOBS THE SURVEY TELLS YOU NOT TO KILL.
#
# The farming route is nearest-neighbour from the LOWEST-LEVEL mob, and in
# Najena that is Moosh at 18 — so the route opened on the one named the same
# page forbids: "Do not kill Moosh. Attacking him pulls an injured halfling out
# of the cell, and killing that halfling tanks every Rivervale faction."
#
# They stay ON THE PLOT. A reader needs to know where Moosh is precisely so
# they can avoid him; removing the marker would hide the hazard along with the
# mistake. They are excluded from the ROUTE only, and the page says why.
#
# Explicit rather than parsed out of the prose, following WITHHELD: a warning
# reworded should not silently put a mob back in the route.
NO_ROUTE = {
    ('najena', 'Moosh'),
}

def route_order(dots, levels):
    """An order to walk the named in, and how far that walk is.

    Nearest neighbour from the lowest-level mob — a rough stand-in for starting
    near the entrance, since the zone line is not recorded for every zone —
    then 2-opt until it stops improving. With eighteen points that is instant
    and lands within a few per cent of optimal.

    THIS IS NOT A PATH. It is an order, drawn as straight lines between spawn
    points. It does not know about walls, doors, locks or drops, and the survey
    must say so wherever the overlay appears. A route that looks like it walks
    through a wall is the drawing being honest about what it is, not an error.
    """
    n = len(dots)
    if n < 3:
        return list(range(n)), 0.0

    def dist(a, b):
        return math.hypot(dots[a][0] - dots[b][0], dots[a][1] - dots[b][1])

    start = min(range(n), key=lambda i: (levels[i] if levels[i] is not None else 999))
    unvisited = set(range(n)) - {start}
    tour = [start]
    while unvisited:
        last = tour[-1]
        nxt = min(unvisited, key=lambda j: dist(last, j))
        tour.append(nxt)
        unvisited.discard(nxt)

    improved = True
    while improved:
        improved = False
        for i in range(1, n - 1):
            for k in range(i + 1, n):
                a, b = tour[i - 1], tour[i]
                c = tour[k]
                d = tour[k + 1] if k + 1 < n else None
                delta = dist(a, c) - dist(a, b)
                if d is not None:
                    delta += dist(b, d) - dist(c, d)
                if delta < -1e-9:
                    tour[i:k + 1] = reversed(tour[i:k + 1])
                    improved = True
    total = sum(dist(tour[i], tour[i + 1]) for i in range(n - 1))
    return tour, total


def build_plot(zone, pts, layers):
    ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
    pxs = [-v for v in xs]; pys = [-v for v in ys]
    gx = [x for L in layers for c in L['lines'] for x, _y in c]
    gy = [y for L in layers for c in L['lines'] for _x, y in c]
    # The zone's own footprint sets the scale once there is geometry; the points
    # alone used to, which zoomed in on wherever the named mobs happened to be.
    span = max(max(pxs + gx) - min(pxs + gx), max(pys + gy) - min(pys + gy)) or 100
    lv = [p[4] for p in pts if p[4] is not None]
    lo, hi = (min(lv), max(lv)) if lv else (0, 1)

    fs = span * 0.024
    r_dot = span * 0.010

    def box(cx, cy, text, anchor, size=None):
        """Collision box for a label, measured rather than guessed.

        IBM Plex Mono advances exactly 0.60em per character, confirmed against
        the rendered text. Height was the error: text occupies 1.26em, not the
        1.04em assumed here, and every label also carries a halo stroke of
        0.42em painted under it. Underestimating both is why labels kept
        overlapping after the placer said they did not."""
        s = fs if size is None else size
        w = len(text) * s * 0.60
        pad = s * 0.30
        x = cx if anchor == 'start' else (cx - w if anchor == 'end' else cx - w / 2)
        return (x - pad, cy - s * 0.98 - pad, x + w + pad, cy + s * 0.30 + pad)

    def hits(a, b):
        return not (a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1])

    # Everything that will be drawn gets its bounding box collected here, and
    # the frame is derived from the union at the end. Sizing the frame from the
    # points alone clipped labels off the right edge — 327 units of "The
    # Warrens", 268 of Lower Guk — because a label extends well past the marker
    # it belongs to, and further still once placement pushes it sideways.
    extents = []

    # ---- the floor plan, drawn under everything else -----------------------
    # One group per storey so the height control can isolate them. Without it a
    # stacked zone draws every level on top of every other and reads as noise.
    geo = []
    for i, L in enumerate(layers):
        paths = ''.join(
            '<polyline points="' + ' '.join(f'{x},{y}' for x, y in c) + '"/>'
            for c in L['lines'])
        geo.append(f'<g class="lyr" data-lyr="{i}" data-z0="{L["z"][0]}" '
                   f'data-z1="{L["z"][1]}" fill="none" stroke="{zone["accent"]}" '
                   f'stroke-opacity=".45" stroke-width="2" stroke-linejoin="round" '
                   f'stroke-linecap="round" vector-effect="non-scaling-stroke">{paths}</g>')
        for c in L['lines']:
            for x, y in c:
                extents.append((x, y, x, y))

    regions, rlabels, rboxes = [], [], []
    for c in cluster(pts, span * 0.14):
        pp = [(-pts[i][1], -pts[i][0]) for i in c]
        nm = region_name([pts[i][3] for i in c]) if len(c) >= 2 else None
        # hull() returns nothing for points that are collinear or coincident, and
        # expand() divides by the vertex count. Three points in a line is a real
        # case, so check the hull rather than the input.
        h = hull(pp) if len(pp) >= 3 else []
        hp = expand(h, span * 0.035) if h else []
        if hp:
            d = 'M' + 'L'.join(f'{x:.0f},{y:.0f}' for x, y in hp) + 'Z'
            regions.append(f'<path d="{d}" fill="{zone["accent"]}" fill-opacity=".07" '
                           f'stroke="{zone["accent"]}" stroke-opacity=".34" stroke-width="1.5" '
                           f'stroke-dasharray="7 5" vector-effect="non-scaling-stroke"/>')
            extents += [(x, y, x, y) for x, y in hp]
        elif len(pp) == 2:
            (ax, ay), (bx, by) = pp
            regions.append(f'<line x1="{ax:.0f}" y1="{ay:.0f}" x2="{bx:.0f}" y2="{by:.0f}" '
                           f'stroke="{zone["accent"]}" stroke-opacity=".3" stroke-width="1.5" '
                           f'stroke-dasharray="7 5" vector-effect="non-scaling-stroke"/>')
        if nm:
            cx = sum(x for x, _ in pp) / len(pp)
            cy = min(y for _, y in pp) - span * 0.055
            rlabels.append(f'<text x="{cx:.0f}" y="{cy:.0f}" text-anchor="middle" '
                           f'font-family="Saira Condensed, sans-serif" font-size="{span*0.033:.0f}" '
                           f'font-weight="700" letter-spacing="1" fill="{lift(zone["accent"])}" '
                           f'style="text-transform:uppercase">{esc(nm)}</text>')
            rboxes.append(box(cx, cy, nm, 'middle', span * 0.033))
            extents.append(rboxes[-1])

    # ---- labels, placed so they do not sit on top of one another ----------
    # Naive placement put every label directly above its point, which collided
    # constantly — "The Tenderizer" landed on "Lost Crusader" and both became
    # unreadable. Each label now tries a ring of candidate offsets and takes the
    # first that clears every label already placed, plus every plotted point. A
    # leader line is drawn whenever the label ends up away from its marker.
    CAND = [(0,-1,'middle'), (0,1.35,'middle'),
            (1,-0.35,'start'), (-1,-0.35,'end'),
            (1,0.9,'start'),  (-1,0.9,'end'),
            (1,-1.3,'start'), (-1,-1.3,'end'),
            (0,-2.3,'middle'), (0,2.6,'middle'),
            (1.8,-0.35,'start'), (-1.8,-0.35,'end')]

    # Seeded with the region names, which are drawn first and must not be
    # written through — "THE DEAD TOWER" printed straight over "a ghoul
    # ritualist" while they were absent from this set.
    placed = list(rboxes)
    dots = [(-p[1], -p[0]) for p in pts]
    marks, leaders = [], []
    order = sorted(range(len(pts)), key=lambda i: (-pts[i][1], -pts[i][0]))
    for i in order:
        yv, xv, name, note, lev, lev_raw = pts[i]
        px, py = -xv, -yv
        short = name if len(name) <= 24 else name[:22] + '…'
        chosen = None
        for dx, dy, anchor in CAND:
            lx = px + dx * (r_dot * 1.9 + len(short) * fs * 0.30 * abs(dx) * 0.18)
            ly = py + dy * (r_dot * 1.9 + fs * 0.9)
            bb = box(lx, ly, short, anchor)
            if any(hits(bb, q) for q in placed):
                continue
            if any(bb[0] - r_dot < dx2 < bb[2] + r_dot and bb[1] - r_dot < dy2 < bb[3] + r_dot
                   for j, (dx2, dy2) in enumerate(dots) if j != i):
                continue
            chosen = (lx, ly, anchor, bb)
            break
        if chosen is None:
            # The candidate ring is exhausted, which happens wherever the zone is
            # crowded — Mistmoore's library corner puts six names in one room.
            # Falling back to the default position knowingly draws one label over
            # another, so push outward in rings until something is free instead.
            # A name further from its marker still has a leader line; a name
            # written through another name is simply lost.
            for mult in (2.6, 3.6, 4.8, 6.2, 8.0):
                for k in range(12):
                    a = k * math.pi / 6.0
                    lx = px + math.cos(a) * r_dot * 2.0 * mult
                    ly = py + math.sin(a) * (r_dot * 2.0 + fs) * mult * 0.55
                    anchor = 'start' if math.cos(a) > 0.4 else ('end' if math.cos(a) < -0.4 else 'middle')
                    bb = box(lx, ly, short, anchor)
                    if not any(hits(bb, q) for q in placed):
                        chosen = (lx, ly, anchor, bb)
                        break
                if chosen:
                    break
        if chosen is None:
            lx, ly, anchor = px, py - r_dot * 1.9 - fs * 0.9, 'middle'
            chosen = (lx, ly, anchor, box(lx, ly, short, anchor))
        lx, ly, anchor, bb = chosen
        placed.append(bb)
        if abs(lx - px) > r_dot * 2.2 or abs(ly - py) > r_dot * 3.4:
            ex = lx if anchor == 'middle' else (lx - fs * 0.2 if anchor == 'start' else lx + fs * 0.2)
            leaders.append(f'<line class="mklead" x1="{px:.0f}" y1="{py:.0f}" x2="{ex:.0f}" '
                           f'y2="{ly + fs*0.28:.0f}" '
                           f'stroke="#71675D" stroke-width="1" vector-effect="non-scaling-stroke"/>')
        col = band_colour(lev, lo, hi)
        # Everything the reader might want to filter or read on click travels
        # with the marker, so the page needs no second data structure and the
        # SVG stays the single record of what was drawn.
        lyr, lyr_d = layer_of(px, py, layers)
        drops = DROPS.get((zone['slug'], name), [])
        # The band maths averages a range to pick a colour. Printing that average
        # invents a level: "24-25" became "Level 24.5". Print the source text.
        lev_txt = lev_raw or (f'{lev:g}' if lev is not None else '')
        lyr_attr = f' data-lyr="{lyr}"' if lyr is not None else ''
        marks.append(
            f'<g class="mk" data-name="{esc(name)}" data-lv="{lev_txt}"{lyr_attr}'
            f' data-drops="{esc(" · ".join(drops))}" tabindex="0" role="button"'
            f' aria-label="{esc(name)}{f", level {lev_txt}" if lev_txt else ""}'
            f'{f". Drops {len(drops)} recorded items." if drops else ". No drops recorded."}">'
            f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r_dot:.1f}" fill="{col}" '
            f'fill-opacity=".95" stroke="#0B0704" stroke-width="1.5" vector-effect="non-scaling-stroke"/>'
            f'<text class="mklbl" x="{lx:.0f}" y="{ly:.0f}" text-anchor="{anchor}" '
            f'font-family="IBM Plex Mono, monospace" font-size="{fs:.0f}" fill="#F2EADA" '
            f'style="paint-order:stroke" stroke="#191410" stroke-width="{fs*0.42:.1f}" '
            f'stroke-linejoin="round">{esc(short)}</text></g>')
    # ---- the farming route -------------------------------------------------
    # An order to take the named in, not a path through the zone. Drawn hidden;
    # the survey's control reveals it.
    # Drop the do-not-kill mobs before ordering, and keep enough to say so.
    keep = [k for k, p in enumerate(pts) if (zone['slug'], p[2]) not in NO_ROUTE]
    skipped = [p[2] for k, p in enumerate(pts) if k not in keep]
    rdots = [dots[k] for k in keep]
    rlev = [pts[k][4] for k in keep]
    rtour, tour_len = route_order(rdots, rlev)
    tour = [keep[i] for i in rtour]
    route = ''
    if len(tour) > 2:
        pl = ' '.join(f'{dots[i][0]:.0f},{dots[i][1]:.0f}' for i in tour)
        stops = ''.join(
            f'<circle class="rstop" cx="{dots[i][0]:.0f}" cy="{dots[i][1]:.0f}" '
            f'r="{r_dot*1.9:.1f}" fill="none" stroke="#E8B04B" stroke-width="1.6" '
            f'vector-effect="non-scaling-stroke"/>'
            f'<text class="rnum" x="{dots[i][0]:.0f}" y="{dots[i][1] - r_dot*2.6:.0f}" '
            f'text-anchor="middle" font-family="IBM Plex Mono, monospace" '
            f'font-size="{fs*0.86:.0f}" fill="#E8B04B" style="paint-order:stroke" '
            f'stroke="#191410" stroke-width="{fs*0.36:.1f}">{k+1}</text>'
            for k, i in enumerate(tour))
        route = (f'<g class="route" hidden><polyline points="{pl}" fill="none" '
                 f'stroke="#E8B04B" stroke-width="2" stroke-opacity=".75" '
                 f'stroke-dasharray="7 5" stroke-linejoin="round" '
                 f'vector-effect="non-scaling-stroke"/>{stops}</g>')

    marks = leaders + marks
    extents += placed

    # ---- frame, derived from what is actually drawn ------------------------
    # The scale bar and compass get a reserved strip along the bottom instead of
    # sitting inside the plot area. With the frame now fitted tightly to the
    # content there is no slack left for them to occupy safely.
    pad = max(34, span * 0.05)
    strip = max(90, span * 0.15)
    ex0 = min(min(b[0] for b in extents), min(pxs))
    ex1 = max(max(b[2] for b in extents), max(pxs))
    ey0 = min(min(b[1] for b in extents), min(pys))
    ey1 = max(max(b[3] for b in extents), max(pys))
    x0, x1 = ex0 - pad, ex1 + pad
    y0, y1 = ey0 - pad, ey1 + pad + strip
    w, h = x1 - x0, y1 - y0
    step = nice_step(max(w, h))

    g = []
    gx = (int(x0 // step) + 1) * step
    while gx < x1:
        g.append(f'<line x1="{gx:.0f}" y1="{y0:.0f}" x2="{gx:.0f}" y2="{y1:.0f}" '
                 f'stroke="#322A23" stroke-width="1" vector-effect="non-scaling-stroke"/>')
        gx += step
    gy = (int(y0 // step) + 1) * step
    while gy < y1:
        g.append(f'<line x1="{x0:.0f}" y1="{gy:.0f}" x2="{x1:.0f}" y2="{gy:.0f}" '
                 f'stroke="#322A23" stroke-width="1" vector-effect="non-scaling-stroke"/>')
        gy += step

    # scale bar bottom-left, north arrow bottom-right, both inside the strip
    sbx, sby = x0 + pad * 0.7, y1 - strip * 0.30
    scale = (f'<g><line x1="{sbx:.0f}" y1="{sby:.0f}" x2="{sbx+step:.0f}" y2="{sby:.0f}" '
             f'stroke="#B5AA95" stroke-width="2" vector-effect="non-scaling-stroke"/>'
             f'<line x1="{sbx:.0f}" y1="{sby-span*0.012:.0f}" x2="{sbx:.0f}" y2="{sby+span*0.012:.0f}" '
             f'stroke="#B5AA95" stroke-width="2" vector-effect="non-scaling-stroke"/>'
             f'<line x1="{sbx+step:.0f}" y1="{sby-span*0.012:.0f}" x2="{sbx+step:.0f}" y2="{sby+span*0.012:.0f}" '
             f'stroke="#B5AA95" stroke-width="2" vector-effect="non-scaling-stroke"/>'
             f'<text x="{sbx+step/2:.0f}" y="{sby-span*0.024:.0f}" text-anchor="middle" '
             f'font-family="IBM Plex Mono, monospace" font-size="{fs:.0f}" fill="#B5AA95">'
             f'{step} units</text></g>')
    ncx = x1 - pad * 0.7 - span * 0.02
    nb = y1 - strip * 0.16
    ntop = y1 - strip * 0.88
    compass = (f'<g><line x1="{ncx:.0f}" y1="{nb-fs*1.5:.0f}" x2="{ncx:.0f}" y2="{ntop+span*0.018:.0f}" '
               f'stroke="#B5AA95" stroke-width="2" vector-effect="non-scaling-stroke"/>'
               f'<path d="M{ncx:.0f},{ntop:.0f} L{ncx-span*0.014:.0f},{ntop+span*0.026:.0f} '
               f'L{ncx+span*0.014:.0f},{ntop+span*0.026:.0f} Z" fill="#B5AA95"/>'
               f'<text x="{ncx:.0f}" y="{nb:.0f}" text-anchor="middle" '
               f'font-family="IBM Plex Mono, monospace" font-size="{fs:.0f}" fill="#B5AA95">N</text></g>')

    svg = (f'<svg class="plotsvg" viewBox="{x0:.0f} {y0:.0f} {w:.0f} {h:.0f}" role="img" '
           f'aria-label="Survey plot of {esc(zone["title"])}. {len(pts)} recorded named-mob positions, '
           f'labelled in place and coloured by level. Dashed outlines group positions that sit close '
           f'together; they are not room shapes. North is up, west is left. Every position is also '
           f'listed as text beneath the plot.">'
           f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{w:.0f}" height="{h:.0f}" fill="#191410"/>'
           + ''.join(g) + ''.join(geo) + ''.join(regions) + ''.join(rlabels) + route
           + ''.join(marks)
           + scale + compass + '</svg>')
    return svg, step, (lo, hi), sum(1 for r in rlabels), tour, tour_len

sections = []
tot_plot = tot_named = tot_regions = tot_withheld = tot_geo = 0
tot_measured = tot_on_floor = 0
PLATE_QUEUE = []
for z in Z:
    pts, unplotted, withheld = [], [], []
    for n in IX['named']:
        if n['z'] != z['slug']: continue
        raw = (n.get('loc') or '').strip()
        v = nums(raw)
        if (z['slug'], n['n']) in WITHHELD:
            withheld.append((n['n'], raw or 'not recorded'))
        elif RANGE.search(raw) or len(v) < 2:
            unplotted.append((n['n'], raw or 'not recorded'))
        else:
            pts.append((v[0], v[1], n['n'], n.get('no') or '', lvl_of(n.get('lv')),
                        (n.get('lv') or '').strip()))
    if not pts: continue
    zone_total = len(pts) + len(unplotted) + len(withheld)
    tot_plot += len(pts); tot_named += zone_total
    tot_withheld += len(withheld)
    layers = GEO.get(z['slug'], {}).get('layers', [])

    # How many recorded positions actually land on the floor we drew. Two
    # independent things have to be right for a point to land close — the
    # coordinate and the geometry — so this is a real check on both, and it is
    # counted here rather than typed, so it cannot drift from the data.
    segs = [s for L in layers for c in L['lines'] for s in zip(c, c[1:])]
    zone_on_floor = 0
    if segs:
        for yv, xv, *_ in pts:
            px, py = -xv, -yv
            best = min(seg_dist(px, py, a, b) for a, b in segs)
            tot_measured += 1
            if best <= ON_FLOOR:
                tot_on_floor += 1
                zone_on_floor += 1

    svg, step, (lo, hi), nregions, tour, tour_len = build_plot(z, pts, layers)
    tot_regions += nregions
    if layers:
        tot_geo += 1

    # Height control. Only worth showing where the zone actually stacks; a flat
    # zone gets no control rather than a dead one. Ordered top storey first,
    # which is how a reader thinks about a building.
    height = ''
    if len(layers) > 1:
        opts = ''.join(
            f'<button type="button" class="lvbtn" data-lyr="{i}" '
            f'aria-pressed="false">{i+1}<span>{L["z"][0]} to {L["z"][1]}</span></button>'
            for i, L in reversed(list(enumerate(layers))))
        height = (f'<div class="levels" data-zone="{z["slug"]}">'
                  f'<span class="lvlab">Height</span>'
                  f'<button type="button" class="lvbtn on" data-lyr="all" '
                  f'aria-pressed="true">All<span>{len(layers)} levels</span></button>{opts}</div>')

    rows = '\n'.join(
        f'<li><span class="pn2">{esc(nm)}</span>'
        f'<span class="pl">{"level " + lvr if lvr else "level not recorded"}</span>'
        f'<span class="pc">{yv:.0f}, {xv:.0f}</span></li>'
        for yv, xv, nm, _, lv, lvr in sorted(pts, key=lambda p: (p[4] is None, p[4] or 0)))

    missing = ''
    if unplotted:
        items = ''.join(f'<li><span class="pn2">{esc(a)}</span><span class="pc">{esc(b)}</span></li>'
                        for a, b in unplotted)
        missing = (f'<div class="note warn"><strong>{len(unplotted)} of {zone_total} named '
                   f'mobs in this zone are not on the plot.</strong> They wander, vary by spawn point, '
                   f'or have no coordinate on record. Listed here rather than placed somewhere '
                   f'plausible.</div><ul class="plotmissing">{items}</ul>')

    if withheld:
        items = ''.join(f'<li><span class="pn2">{esc(a)}</span><span class="pc">{esc(b)}</span></li>'
                        for a, b in withheld)
        missing += (
            f'<div class="note warn"><strong>A further {len(withheld)} coordinates are recorded but '
            f'cannot be right, and are withheld rather than drawn.</strong> Each sits south of this '
            f'zone&rsquo;s own extent &mdash; outside the dungeon &mdash; by between 57 and 513 units. '
            f'The figures below are transcribed correctly from '
            f'<a href="https://eqlwiki.com/Najena">the eqlwiki Najena page</a> '
            f'<span class="tier t5">T5</span>, read 8 August 2026; it is the recorded position that is '
            f'wrong, not the transcription. The extent is measured from the map file EverQuest Legends '
            f'installs with the game, 4,144 segments of first-party geometry for this zone, and two '
            f'community map sets drawn independently agree with it to within two units. In every case '
            f'the east&ndash;west value is consistent and only the north&ndash;south one is out, which '
            f'points at a single column rather than at noise. The official map carries geometry and '
            f'zone exits but no mob positions, so it can show a figure is impossible without supplying '
            f'the right one. No replacement is published here, because none is sourced. <strong>One '
            f'<code>/loc</code> reading per mob closes this.</strong></div>'
            f'<ul class="plotmissing">{items}</ul>')

    sections.append(f'''
<section class="band plotband" id="{z['slug']}" style="--c:{z['accent']}">
  <div class="shell">
    <div class="sechead">
      <div><h2 class="sec">{esc(z['title'])}</h2>
        <p class="lede" style="margin:0">{len(pts)} of {zone_total} named mobs plotted
          &middot; {step}-unit grid &middot; levels {int(lo)}&ndash;{int(hi)} shown green through red.
          Dashed outlines group positions that sit near each other; they are not room shapes.</p></div>
      <a class="link" href="{z['slug']}.html">Survey {z['plate']:02d} &rarr;</a></div>
    {height}
  </div>
  <div class="plotwrap">{svg}</div>
  <div class="shell">
    <ol class="plotkey">
{rows}
    </ol>
    {missing}
  </div>
</section>''')
    if layers:
        PLATE_QUEUE.append((z, svg, layers, len(pts), zone_on_floor, tour, tour_len, pts))

# ---- the same drawing, put on each survey ---------------------------------
# The plates are standalone pages with their own inline CSS and no link to
# site.css, so the block carries its own styling rather than borrowing any.
# build3.py has already written them by the time this runs, and regenerates
# them from _build/source on every build, so injecting here is not cumulative.
PLATE_CSS = """
<style>
.fplan{margin:38px 0 10px}
.fplan h2{font-family:"Saira Condensed",sans-serif;font-weight:600;text-transform:uppercase;
  letter-spacing:.02em;font-size:clamp(21px,3.4vw,28px);margin:0 0 8px}
.fp-lede{color:#B0A9A2;margin:0 0 16px;max-width:66ch}
.fp-wrap{border:1px solid #40372D;background:#191410;overflow:hidden;border-radius:4px}
.fp-wrap svg{display:block;height:min(96vh,1000px);width:auto;max-width:100%;margin:0 auto}
@media(max-width:900px){.fp-wrap svg{height:auto;width:100%}}
.fp-levels{display:flex;flex-wrap:wrap;gap:8px;align-items:stretch;margin:0 0 14px}
.fp-levels .lab{align-self:center;font-family:"IBM Plex Mono",monospace;font-size:10px;
  letter-spacing:.14em;text-transform:uppercase;color:var(--faint);margin-right:4px}
.fp-levels button{display:flex;flex-direction:column;gap:2px;padding:8px 12px;cursor:pointer;
  background:#251F19;border:1px solid #40372D;border-radius:4px;color:var(--mut);
  font-family:"IBM Plex Mono",monospace;font-size:13.5px;line-height:1}
.fp-levels button span{font-size:10px;color:#B6ABA1}
.fp-levels button:hover{color:var(--bone);border-color:var(--accd)}
.fp-levels button:focus-visible{outline:2px solid var(--acct);outline-offset:2px}
.fp-levels button.on{background:color-mix(in srgb, var(--acc) 16%, #251F19);
  border-color:var(--accd);color:var(--bone)}
.fp-note{color:var(--faint);font-size:13.5px;margin:12px 0 0;max-width:78ch}
.lyr{transition:stroke-opacity .18s}
.lyr.mute{stroke-opacity:.07}
@media(prefers-reduced-motion:reduce){.lyr{transition:none}}
.fp-toggles{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 10px}
.fp-t{padding:7px 13px;cursor:pointer;background:#251F19;border:1px solid #40372D;
  border-radius:4px;color:var(--mut);font-family:"IBM Plex Mono",monospace;font-size:12.5px;
  letter-spacing:.04em}
.fp-t:hover{color:var(--bone);border-color:var(--accd)}
.fp-t:focus-visible{outline:2px solid var(--acct);outline-offset:2px}
.fp-t.on{background:color-mix(in srgb, var(--acc) 16%, #251F19);border-color:var(--accd);
  color:var(--bone)}
.fp-t[data-t="route"].on{background:rgba(232,176,75,.16);border-color:#E8B04B;color:#F2DDAE}
.plotsvg.nonames .mklbl,.plotsvg.nonames .mklead{display:none}
.mk{cursor:pointer}
.mk:focus-visible circle{stroke:var(--bone);stroke-width:3}
.mk.dim{opacity:.14}
.mk.sel circle{stroke:var(--bone);stroke-width:3}
.fp-detail{margin:12px 0 0;padding:13px 15px;border:1px solid #40372D;border-radius:4px;
  background:#1E1914}
.fp-detail h3{margin:0 0 3px;font-family:"Saira Condensed",sans-serif;font-weight:600;
  text-transform:uppercase;letter-spacing:.02em;font-size:17px;color:var(--bone)}
.fp-detail .dmeta{font-family:"IBM Plex Mono",monospace;font-size:11.5px;color:var(--faint);
  letter-spacing:.06em;text-transform:uppercase}
.fp-detail ul{margin:9px 0 0;padding:0;list-style:none;display:flex;flex-wrap:wrap;gap:6px}
.fp-detail li{font-family:"IBM Plex Mono",monospace;font-size:12px;color:#D2CDC8;
  background:#251F19;border:1px solid #40372D;border-radius:3px;padding:3px 8px}
.fp-detail .dnone{color:#B0A9A2;font-size:13.5px;margin:8px 0 0}
.fp-route{margin:12px 0 0;padding:12px 14px;border-left:3px solid #E8B04B;
  background:rgba(232,176,75,.06);color:#B0A9A2;font-size:13.5px;line-height:1.6}
.fp-route strong,.fp-route .rlen{color:var(--bone)}
.fp-route em{color:#F2DDAE;font-style:normal}
</style>"""

PLATE_JS = """
<script>
(function(){
  var wrap=document.querySelector('.fp-wrap'); if(!wrap) return;
  var svg=wrap.querySelector('svg'); if(!svg) return;
  var layers=svg.querySelectorAll('.lyr');
  var marks=svg.querySelectorAll('.mk');
  var route=svg.querySelector('.route');
  var rnote=document.querySelector('.fp-route');
  var detail=document.querySelector('.fp-detail');
  var bar=document.querySelector('.fp-levels');
  var togs=document.querySelector('.fp-toggles');
  var pick='all';

  // Height. Storeys mute rather than vanish so the zone keeps its shape, and
  // the named filter with them - a mob on floor 3 is noise while you read
  // floor 1.
  function applyLayer(){
    layers.forEach(function(g){
      g.classList.toggle('mute', pick!=='all' && g.dataset.lyr!==pick);
    });
    marks.forEach(function(m){
      var on = pick==='all' || m.dataset.lyr===pick;
      m.classList.toggle('dim', !on);
    });
  }
  if(bar){
    bar.addEventListener('click', function(e){
      var b=e.target.closest('button'); if(!b) return;
      bar.querySelectorAll('button').forEach(function(o){
        o.classList.toggle('on', o===b); o.setAttribute('aria-pressed', o===b?'true':'false');});
      pick=b.dataset.lyr; applyLayer();
    });
  }

  if(togs){
    togs.addEventListener('click', function(e){
      var b=e.target.closest('button'); if(!b) return;
      var on=b.getAttribute('aria-pressed')!=='true';
      b.setAttribute('aria-pressed', on?'true':'false');
      b.classList.toggle('on', on);
      if(b.dataset.t==='names'){ svg.classList.toggle('nonames', !on); }
      if(b.dataset.t==='route'){
        if(route) route.hidden=!on;
        if(rnote) rnote.hidden=!on;
      }
    });
  }

  function show(m){
    marks.forEach(function(o){ o.classList.toggle('sel', o===m); });
    var drops=(m.dataset.drops||'').split(' · ').filter(Boolean);
    var lv=m.dataset.lv? '<span class="dmeta">Level '+m.dataset.lv+'</span>' : '';
    var body = drops.length
      ? '<ul>'+drops.map(function(d){return '<li>'+d+'</li>';}).join('')+'</ul>'
      : '<p class="dnone">No drops recorded for this mob on this survey. That means we '
        +'have not recorded any, not that it carries nothing.</p>';
    detail.innerHTML='<h3>'+m.dataset.name+'</h3>'+lv+body;
    detail.hidden=false;
  }
  marks.forEach(function(m){
    m.addEventListener('click', function(){ show(m); });
    m.addEventListener('keydown', function(e){
      if(e.key==='Enter'||e.key===' '){ e.preventDefault(); show(m); }
    });
  });
})();
</script>"""


def write_plate_plan(z, svg, layers, npts, on_floor, tour, tour_len, pts):
    """Put the floor plan on the survey itself, above its first section."""
    path = f"public/dungeons/{z['slug']}.html"
    if not os.path.exists(path):
        return False
    h = open(path, encoding='utf-8').read()
    if '<section>' not in h:
        return False

    # Three controls, one row. Names off is the one a reader reaches for first:
    # a dense zone puts eighteen labels on the plan and orienting is easier
    # without them.
    toggles = ('<div class="fp-toggles">'
               '<button type="button" class="fp-t on" data-t="names" aria-pressed="true">Names</button>'
               + ('<button type="button" class="fp-t" data-t="route" aria-pressed="false">'
                  'Farming route</button>' if len(tour) > 2 else '')
               + '</div>')

    # The route's honesty clause. It appears with the drawing, not in a footnote,
    # because the drawing is what gets screenshotted into Discord.
    route_note = ''
    if len(tour) > 2:
        order = ' &rarr; '.join(pts[i][2] for i in tour)
        # Anything plotted but not in the tour was excluded on purpose — see
        # NO_ROUTE. Derived here rather than passed in, so the caption cannot
        # disagree with the line that was actually drawn.
        skipped = [p[2] for k, p in enumerate(pts) if k not in set(tour)]
        route_note = (
            f'<p class="fp-route" hidden><strong>Order, not a path.</strong> {order}. '
            f'<span class="rlen">{tour_len:,.0f} units straight-line.</span> '
            + (f'<strong>{" and ".join(skipped)} left off deliberately</strong> '
               f'&mdash; this survey says do not kill '
               f'{"it" if len(skipped) == 1 else "them"}. '
               if skipped else '')
            + '<a href="../learn/reading-the-plans.html">Why the line crosses walls '
              '&rarr;</a></p>')

    lv = ''
    if len(layers) > 1:
        opts = ''.join(
            f'<button type="button" data-lyr="{i}" aria-pressed="false">{i+1}'
            f'<span>{L["z"][0]} to {L["z"][1]}</span></button>'
            for i, L in reversed(list(enumerate(layers))))
        lv = (f'<div class="fp-levels"><span class="lab">Height</span>'
              f'<button type="button" data-lyr="all" class="on" aria-pressed="true">All'
              f'<span>{len(layers)} levels</span></button>{opts}</div>')
        levels_line = (f' This zone has {len(layers)} levels and they overlap when flattened, so the '
                       f'control above isolates one at a time.')
    else:
        levels_line = ' This zone is a single level, so there is nothing to separate.'

    block = (f'<section class="fplan">'
             f'<h2>Floor plan</h2>'
             f'<p class="fp-lede">Where the walkable floor ends, computed from the zone&rsquo;s own '
             f'geometry in the game files, with the {npts} named mob{"" if npts == 1 else "s"} whose '
             f'position{"" if npts == 1 else "s"} {"is" if npts == 1 else "are"} on record '
             f'plotted on it.{levels_line}</p>'
             f'{toggles}{lv}<div class="fp-wrap">{svg}</div>'
             f'<div class="fp-detail" hidden aria-live="polite"></div>'
             f'{route_note}'
             f'<p class="fp-note">Lines are floor edges &mdash; a wall or a drop. '
             f'<b>{on_floor} of {npts} recorded positions land on drawn floor.</b> '
             f'<a href="../learn/reading-the-plans.html">What this plan does not '
             f'mark &rarr;</a></p></section>')

    h = h.replace('</head>', PLATE_CSS + '</head>', 1)
    h = h.replace('<section>', block + '<section>', 1)
    h = h.replace('</body>', PLATE_JS + '</body>', 1)
    open(path, 'w', encoding='utf-8', newline='\n').write(h)
    return True


plated = 0
for z, svg, layers, npts, onf, tour, tlen, pts in PLATE_QUEUE:
    if write_plate_plan(z, svg, layers, npts, onf, tour, tlen, pts):
        plated += 1

page = head("Survey plots",
  "Every recorded named-mob coordinate in the ten surveyed EverQuest Legends dungeons, plotted to "
  "scale, labelled in place and coloured by level.", rel="../") + bar("../") + f'''
<main>

<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp;
      <a href="index.html">Dungeons</a> &nbsp;/&nbsp; Plots</p>
    <h1 class="display">Where everything<br><em>actually is.</em></h1>
    <p class="hero-lede">{tot_plot} named mobs plotted from their recorded <code>/loc</code>, labelled
      where they stand and coloured by level. The other {tot_named - tot_plot} wander, have no
      coordinate on record, or &mdash; in {tot_withheld} cases &mdash; carry a recorded coordinate that
      places them outside the zone itself. All are listed rather than placed.</p>
    <p class="hero-sig"><span>{tot_plot} positions</span><span>{len(sections)} zones</span><span>North up, west left</span><span>To scale</span></p>
  </div>
</section>

<div class="shell">
  <div class="note"><strong>How to read these.</strong> The floor plan is the outline of the walkable
    floor, computed from the zone&rsquo;s own geometry in the game files &mdash; where the line runs is
    where the floor stops, at a wall or a drop. {tot_geo} of the {len(Z)} zones carry one. It is our own
    derivation and not a copy of any published map, so it shows where the floor ends and nothing else:
    <strong>doors, locks and one-way drops are not marked</strong>, and a gap in a line is as likely to
    be a ledge as a doorway.
    <br><br><strong>{tot_on_floor} of {tot_measured} plotted mobs land on that floor</strong>, within
    {ON_FLOOR} units of it. That is worth stating because two independent things have to be right for a
    point to land close &mdash; the recorded coordinate and our reading of the geometry &mdash; so
    agreement is evidence for both. It is counted at build time from the same data the drawing uses,
    not typed in. A position that fell well outside would be visible as a dot in open space, and the
    six withheld from Najena are exactly that case.
    <br><br>Where a zone stacks, <strong>the height control isolates one storey at a time</strong>.
    Storeys are found from the geometry itself, by looking for the heights where floor area piles up,
    so they are the building&rsquo;s real levels rather than slices at fixed intervals. Flat zones get
    no control.
    <br><br>A dashed outline groups named mobs whose recorded positions sit close together &mdash; it
    means &ldquo;these are near each other&rdquo;, not &ldquo;this is a room&rdquo;. An outline is named
    only when at least two of its members&rsquo; notes independently mention the same place;
    {tot_regions} groups across the {len(Z)} zones cleared that bar, and the rest stay unnamed rather than
    guessed at. <strong>Mob positions are not tied to a storey</strong>, because most recorded
    coordinates carry no height &mdash; every point stays visible whichever level you select.</div>
</div>
{''.join(sections)}

</main>
<script>
/* Height control. Progressive enhancement: with no JS every storey stays
   visible, which is the same drawing the page shipped before the control
   existed. Selecting a level fades the others rather than hiding them, so you
   keep the sense of what sits above and below. */
(function(){{
  document.querySelectorAll('.levels').forEach(function(bar){{
    var svg = bar.closest('section').querySelector('.plotsvg');
    if (!svg) return;
    var layers = svg.querySelectorAll('.lyr');
    bar.addEventListener('click', function(e){{
      var b = e.target.closest('.lvbtn');
      if (!b) return;
      bar.querySelectorAll('.lvbtn').forEach(function(o){{
        o.classList.toggle('on', o === b);
        o.setAttribute('aria-pressed', o === b ? 'true' : 'false');
      }});
      var pick = b.dataset.lyr;
      layers.forEach(function(g){{
        g.classList.toggle('mute', pick !== 'all' && g.dataset.lyr !== pick);
      }});
    }});
  }});
}})();
</script>
''' + foot("../")

# dungeons/plots.html was retired on 10 Aug 2026. It collected all ten drawings
# on one page because that is what the plates needed. Every survey now carries its
# own plan, with the height control and the drop panel, so the collection was a
# second copy of ten drawings with no route to it. The page is still assembled
# above because the same code computes the per-survey blocks; it is simply not
# written out.
print(f"floor plans: {plated} surveys carry one, {tot_on_floor} of {tot_measured} positions on drawn floor")
