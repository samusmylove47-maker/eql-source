"""Survey plots — recorded coordinates, made readable.

THE PROBLEM THIS SOLVES
-----------------------
The first version of this page was numbered dots against a grid, with a lookup
table underneath. Readers reported it as "just dots on the screen" — accurate,
and useless, because nothing on the drawing told you what you were looking at.

WHAT IS DRAWN, AND ON WHAT AUTHORITY
------------------------------------
Every mark traces to a `/loc` recorded in assets/index-data.json.

- POINTS are named in place rather than numbered, and coloured by level band, so
  the danger gradient is visible without reading anything.
- REGIONS are convex hulls around mobs that are close together. A hull says
  "these recorded positions sit together". It is NOT a room shape and the legend
  says so. No wall, corridor or door is drawn anywhere, because the project holds
  no survey of them.
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
# faithfully on the Najena plate — the plate is not wrong about what the source
# says. They are withheld because the position itself cannot be right.
#
# Najena's drawn geometry spans worldY −166..544. Every one of these sits south
# of that, by between 59 and 515 units, which places them outside the dungeon.
# That is checked against two map sets drawn independently by different
# cartographers, Brewall and Goodurden, which agree on the zone's extent to
# within two units (−166..544 against −167..546). The zone was not rebuilt for
# Legends, so the classic extent applies.
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

def build_plot(zone, pts):
    ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
    pxs = [-v for v in xs]; pys = [-v for v in ys]
    span = max(max(pxs) - min(pxs), max(pys) - min(pys)) or 100
    lv = [p[4] for p in pts if p[4] is not None]
    lo, hi = (min(lv), max(lv)) if lv else (0, 1)

    fs = span * 0.024
    r_dot = span * 0.010

    def box(cx, cy, text, anchor, size=None):
        s = fs if size is None else size
        w = len(text) * s * 0.60
        x = cx if anchor == 'start' else (cx - w if anchor == 'end' else cx - w / 2)
        return (x, cy - s * 0.82, x + w, cy + s * 0.22)

    def hits(a, b):
        return not (a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1])

    # Everything that will be drawn gets its bounding box collected here, and
    # the frame is derived from the union at the end. Sizing the frame from the
    # points alone clipped labels off the right edge — 327 units of "The
    # Warrens", 268 of Lower Guk — because a label extends well past the marker
    # it belongs to, and further still once placement pushes it sideways.
    extents = []

    regions, rlabels, rboxes = [], [], []
    for c in cluster(pts, span * 0.14):
        pp = [(-pts[i][1], -pts[i][0]) for i in c]
        nm = region_name([pts[i][3] for i in c]) if len(c) >= 2 else None
        hp = expand(hull(pp), span * 0.035) if len(pp) >= 3 else []
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
        yv, xv, name, note, lev = pts[i]
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
            lx, ly, anchor = px, py - r_dot * 1.9 - fs * 0.9, 'middle'
            chosen = (lx, ly, anchor, box(lx, ly, short, anchor))
        lx, ly, anchor, bb = chosen
        placed.append(bb)
        if abs(lx - px) > r_dot * 2.2 or abs(ly - py) > r_dot * 3.4:
            ex = lx if anchor == 'middle' else (lx - fs * 0.2 if anchor == 'start' else lx + fs * 0.2)
            leaders.append(f'<line x1="{px:.0f}" y1="{py:.0f}" x2="{ex:.0f}" y2="{ly + fs*0.28:.0f}" '
                           f'stroke="#5C6B70" stroke-width="1" vector-effect="non-scaling-stroke"/>')
        col = band_colour(lev, lo, hi)
        marks.append(
            f'<g><circle cx="{px:.0f}" cy="{py:.0f}" r="{r_dot:.1f}" fill="{col}" '
            f'fill-opacity=".95" stroke="#0E1315" stroke-width="1.5" vector-effect="non-scaling-stroke"/>'
            f'<text x="{lx:.0f}" y="{ly:.0f}" text-anchor="{anchor}" '
            f'font-family="IBM Plex Mono, monospace" font-size="{fs:.0f}" fill="#E6E9E4" '
            f'style="paint-order:stroke" stroke="#10161A" stroke-width="{fs*0.42:.1f}" '
            f'stroke-linejoin="round">{esc(short)}</text></g>')
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
                 f'stroke="#232D32" stroke-width="1" vector-effect="non-scaling-stroke"/>')
        gx += step
    gy = (int(y0 // step) + 1) * step
    while gy < y1:
        g.append(f'<line x1="{x0:.0f}" y1="{gy:.0f}" x2="{x1:.0f}" y2="{gy:.0f}" '
                 f'stroke="#232D32" stroke-width="1" vector-effect="non-scaling-stroke"/>')
        gy += step

    # scale bar bottom-left, north arrow bottom-right, both inside the strip
    sbx, sby = x0 + pad * 0.7, y1 - strip * 0.30
    scale = (f'<g><line x1="{sbx:.0f}" y1="{sby:.0f}" x2="{sbx+step:.0f}" y2="{sby:.0f}" '
             f'stroke="#AEB9B8" stroke-width="2" vector-effect="non-scaling-stroke"/>'
             f'<line x1="{sbx:.0f}" y1="{sby-span*0.012:.0f}" x2="{sbx:.0f}" y2="{sby+span*0.012:.0f}" '
             f'stroke="#AEB9B8" stroke-width="2" vector-effect="non-scaling-stroke"/>'
             f'<line x1="{sbx+step:.0f}" y1="{sby-span*0.012:.0f}" x2="{sbx+step:.0f}" y2="{sby+span*0.012:.0f}" '
             f'stroke="#AEB9B8" stroke-width="2" vector-effect="non-scaling-stroke"/>'
             f'<text x="{sbx+step/2:.0f}" y="{sby-span*0.024:.0f}" text-anchor="middle" '
             f'font-family="IBM Plex Mono, monospace" font-size="{fs:.0f}" fill="#AEB9B8">'
             f'{step} units</text></g>')
    ncx = x1 - pad * 0.7 - span * 0.02
    nb = y1 - strip * 0.16
    ntop = y1 - strip * 0.88
    compass = (f'<g><line x1="{ncx:.0f}" y1="{nb-fs*1.5:.0f}" x2="{ncx:.0f}" y2="{ntop+span*0.018:.0f}" '
               f'stroke="#AEB9B8" stroke-width="2" vector-effect="non-scaling-stroke"/>'
               f'<path d="M{ncx:.0f},{ntop:.0f} L{ncx-span*0.014:.0f},{ntop+span*0.026:.0f} '
               f'L{ncx+span*0.014:.0f},{ntop+span*0.026:.0f} Z" fill="#AEB9B8"/>'
               f'<text x="{ncx:.0f}" y="{nb:.0f}" text-anchor="middle" '
               f'font-family="IBM Plex Mono, monospace" font-size="{fs:.0f}" fill="#AEB9B8">N</text></g>')

    svg = (f'<svg class="plotsvg" viewBox="{x0:.0f} {y0:.0f} {w:.0f} {h:.0f}" role="img" '
           f'aria-label="Survey plot of {esc(zone["title"])}. {len(pts)} recorded named-mob positions, '
           f'labelled in place and coloured by level. Dashed outlines group positions that sit close '
           f'together; they are not room shapes. North is up, west is left. Every position is also '
           f'listed as text beneath the plot.">'
           f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{w:.0f}" height="{h:.0f}" fill="#10161A"/>'
           + ''.join(g) + ''.join(regions) + ''.join(rlabels) + ''.join(marks)
           + scale + compass + '</svg>')
    return svg, step, (lo, hi), sum(1 for r in rlabels)

sections = []
tot_plot = tot_named = tot_regions = tot_withheld = 0
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
            pts.append((v[0], v[1], n['n'], n.get('no') or '', lvl_of(n.get('lv'))))
    if not pts: continue
    zone_total = len(pts) + len(unplotted) + len(withheld)
    tot_plot += len(pts); tot_named += zone_total
    tot_withheld += len(withheld)
    svg, step, (lo, hi), nregions = build_plot(z, pts)
    tot_regions += nregions

    rows = '\n'.join(
        f'<li><span class="pn2">{esc(nm)}</span>'
        f'<span class="pl">{"level " + str(int(lv)) if lv else "level not recorded"}</span>'
        f'<span class="pc">{yv:.0f}, {xv:.0f}</span></li>'
        for yv, xv, nm, _, lv in sorted(pts, key=lambda p: (p[4] is None, p[4] or 0)))

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
            f'zone&rsquo;s own extent &mdash; outside the dungeon &mdash; by between 59 and 515 units. '
            f'The figures below are transcribed correctly from '
            f'<a href="https://eqlwiki.com/Najena">the eqlwiki Najena page</a> '
            f'<span class="tier t5">T5</span>, read 8 August 2026; it is the recorded position that is '
            f'wrong, not the transcription. The zone extent is checked against two map sets drawn '
            f'independently by different cartographers, which agree on it to within two units, and the '
            f'zone was not rebuilt for Legends. In every case the X value is consistent and only Y is '
            f'out, which points at one column rather than at noise. No replacement is published here, '
            f'because none is sourced. <strong>One <code>/loc</code> reading per mob closes '
            f'this.</strong></div><ul class="plotmissing">{items}</ul>')

    sections.append(f'''
<section class="band plotband" id="{z['slug']}" style="--c:{z['accent']}">
  <div class="shell">
    <div class="sechead">
      <div><h2 class="sec">{esc(z['title'])}</h2>
        <p class="lede" style="margin:0">{len(pts)} of {zone_total} named mobs plotted
          &middot; {step}-unit grid &middot; levels {int(lo)}&ndash;{int(hi)} shown green through red.
          Dashed outlines group positions that sit near each other; they are not room shapes.</p></div>
      <a class="link" href="{z['slug']}.html">Plate {z['plate']:02d} &rarr;</a></div>
  </div>
  <div class="plotwrap">{svg}</div>
  <div class="shell">
    <ol class="plotkey">
{rows}
    </ol>
    {missing}
  </div>
</section>''')

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
  <div class="note"><strong>How to read these, and what they are not.</strong> A dashed outline groups
    named mobs whose recorded positions sit close together &mdash; it means &ldquo;these are near each
    other&rdquo;, not &ldquo;this is a room&rdquo;. An outline is given a name only when at least two of
    its members&rsquo; notes independently mention the same place; {tot_regions} groups across the ten
    zones cleared that bar, and the rest stay unnamed rather than guessed at. <strong>No wall, door or
    corridor is drawn anywhere on this page</strong>, because the project holds coordinates and not a
    survey of the geometry between them.</div>
</div>
{''.join(sections)}

</main>
''' + foot("../")

open('dungeons/plots.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"survey plots: {len(sections)} zones, {tot_plot} positions, {tot_regions} named regions, {tot_withheld} withheld")
