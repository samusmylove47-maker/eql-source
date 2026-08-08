"""Survey plots — one per zone, drawn from recorded coordinates only.

WHAT THIS DOES AND DELIBERATELY DOES NOT DO
-------------------------------------------
It plots the 208 named-mob positions the project has actually recorded, to
scale, on a measured grid. Every mark on the output traces to a `/loc` in
assets/index-data.json, which extract.py mines from the plates.

It draws NO walls, rooms, corridors or terrain. That information is not in the
data, and a floor plan invented around real coordinates would look authoritative
while being wrong — the exact failure CLAUDE.md exists to prevent. These are
survey plots, not maps, and they are labelled as such.

ORIENTATION
-----------
EverQuest's /loc returns Y, X, Z. The navigation maps in _build/source state the
convention this project draws to: north is up the page, west is to the left.
+Y is north and +X is west, so both axes inverting gives page coordinates.

A NOTE ON THE MINUS SIGN
------------------------
141 of the 208 recorded coordinates use U+2212 MINUS SIGN, not ASCII hyphen.
A plain `-?\\d+` regex reads every one of those as positive. Parse with NUM below.
"""
import os, sys, json, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

Z = json.load(open('assets/zones-index.json', encoding='utf-8'))
IX = json.load(open('assets/index-data.json', encoding='utf-8'))

NUM = re.compile(r'[-−]?\d+(?:\.\d+)?')
def nums(s):
    return [float(t.replace('−', '-')) for t in NUM.findall(s or '')]

def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&quot;'))

def nice_step(span):
    """A round grid interval giving roughly 6-12 lines across the span."""
    for s in (25, 50, 100, 250, 500, 1000, 2000):
        if span / s <= 12:
            return s
    return 5000

def plot(zone, pts):
    """pts: list of (y, x, name, level). Returns (svg, legend_rows)."""
    ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
    # page axes: north up, west left  ->  px = -x, py = -y
    pxs = [-v for v in xs]; pys = [-v for v in ys]
    pad = max(90, (max(pxs) - min(pxs) + max(pys) - min(pys)) * 0.09)
    x0, x1 = min(pxs) - pad, max(pxs) + pad
    y0, y1 = min(pys) - pad, max(pys) + pad
    w, h = x1 - x0, y1 - y0
    step = nice_step(max(w, h))
    acc = zone['accent']

    g = []
    gx = (int(x0 // step) + 1) * step
    while gx < x1:
        major = abs(gx) < 1e-9
        g.append(f'<line x1="{gx:.0f}" y1="{y0:.0f}" x2="{gx:.0f}" y2="{y1:.0f}" '
                 f'stroke="{"#3A484F" if major else "#293439"}" stroke-width="{2 if major else 1}" '
                 f'vector-effect="non-scaling-stroke"/>')
        gx += step
    gy = (int(y0 // step) + 1) * step
    while gy < y1:
        major = abs(gy) < 1e-9
        g.append(f'<line x1="{x0:.0f}" y1="{gy:.0f}" x2="{x1:.0f}" y2="{gy:.0f}" '
                 f'stroke="{"#3A484F" if major else "#293439"}" stroke-width="{2 if major else 1}" '
                 f'vector-effect="non-scaling-stroke"/>')
        gy += step

    marks, rows = [], []
    for i, (yv, xv, name, lvl) in enumerate(pts, 1):
        px, py = -xv, -yv
        marks.append(
            f'<g><circle cx="{px:.0f}" cy="{py:.0f}" r="9" fill="{acc}" fill-opacity=".22" '
            f'stroke="{acc}" stroke-width="2" vector-effect="non-scaling-stroke"/>'
            f'<circle cx="{px:.0f}" cy="{py:.0f}" r="2.5" fill="{acc}"/>'
            f'<text x="{px:.0f}" y="{py - 15:.0f}" text-anchor="middle" '
            f'font-family="IBM Plex Mono, monospace" font-size="15" fill="#E6E9E4" '
            f'style="paint-order:stroke" stroke="#0E1315" stroke-width="4">{i}</text></g>')
        rows.append(f'<li><span class="pi">{i}</span><span class="pn2">{esc(name)}</span>'
                    f'<span class="pl">{esc(lvl) if lvl else "level not recorded"}</span>'
                    f'<span class="pc">{yv:.0f}, {xv:.0f}</span></li>')

    svg = (f'<svg class="plotsvg" viewBox="{x0:.0f} {y0:.0f} {w:.0f} {h:.0f}" role="img" '
           f'aria-label="Survey plot of {esc(zone["title"])}. {len(pts)} recorded named-mob '
           f'positions on a {step}-unit grid. North is up, west is left. Every position is '
           f'listed in the table beneath this plot.">'
           f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{w:.0f}" height="{h:.0f}" fill="#12171A"/>'
           + ''.join(g) + ''.join(marks) + '</svg>')
    return svg, '\n'.join(rows), step, len(pts)

sections = []
total_plotted = total_named = 0
for z in Z:
    pts, unplotted = [], []
    for n in IX['named']:
        if n['z'] != z['slug']:
            continue
        v = nums(n.get('loc'))
        if len(v) >= 2:
            pts.append((v[0], v[1], n['n'], n.get('lv', '')))
        else:
            # Deliberately unplottable: the project records "unrecorded",
            # "various", "any elemental point" and so on rather than inventing a
            # position. Those entries must still be visible, or the plot quietly
            # under-reports the zone.
            unplotted.append((n['n'], (n.get('loc') or 'not recorded').strip()))
    if not pts:
        continue
    total_plotted += len(pts); total_named += len(pts) + len(unplotted)
    svg, rows, step, count = plot(z, pts)
    missing = ''
    if unplotted:
        items = ''.join(f'<li><span class="pn2">{esc(a)}</span>'
                        f'<span class="pc">{esc(b)}</span></li>' for a, b in unplotted)
        missing = (f'<div class="note warn"><strong>{len(unplotted)} of '
                   f'{len(pts) + len(unplotted)} named mobs in this zone are not on the plot.</strong> '
                   f'Their positions are recorded as wandering, variable or simply not taken. They are '
                   f'listed here rather than placed somewhere plausible.</div>'
                   f'<ul class="plotmissing">{items}</ul>')
    sections.append(f'''
<section class="band plotband" id="{z['slug']}" style="--c:{z['accent']}">
  <div class="shell">
    <div class="sechead">
      <div><h2 class="sec">{esc(z['title'])}</h2>
        <p class="lede" style="margin:0">{count} of {count + len(unplotted)} named mobs plotted &middot; {step}-unit grid &middot;
          north up, west left. Marks are plotted from <code>/loc</code> records only; no walls or
          rooms are drawn, because the project holds no survey of them.</p></div>
      <a class="link" href="{z['slug']}.html">Plate {z['plate']:02d} &rarr;</a></div>
    <div class="plotwrap">{svg}</div>
    <ol class="plotkey">
{rows}
    </ol>
    {missing}
  </div>
</section>''')

page = head("Survey plots",
  "Every recorded named-mob coordinate in the ten surveyed EverQuest Legends dungeons, plotted to "
  "scale on a measured grid.", rel="../") + bar("../") + f'''
<main>

<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp;
      <a href="index.html">Dungeons</a> &nbsp;/&nbsp; Plots</p>
    <h1 class="display">Every position<br><em>we hold.</em></h1>
    <p class="hero-lede">{total_plotted} of {total_named} named mobs plotted from their recorded
      <code>/loc</code> on a measured grid. The other {total_named - total_plotted} wander, vary by
      spawn point, or have no coordinate on record &mdash; they are listed under each plot rather than
      placed somewhere plausible.</p>
    <p class="hero-sig"><span>{total_plotted} plotted</span><span>{total_named - total_plotted} unplottable</span><span>{len(sections)} zones</span><span>No geometry invented</span></p>
  </div>
</section>

<div class="shell">
  <div class="note"><strong>Why there are no walls on these.</strong> The project holds coordinates,
    not floor plans. A room drawn around a real coordinate would look authoritative and be a guess, so
    nothing here is drawn that was not measured. The five hand-drawn navigation maps under
    <a href="index.html">Dungeons</a> are a separate, deliberate piece of work.</div>
</div>
{''.join(sections)}

</main>
''' + foot("../")

open('dungeons/plots.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"survey plots: {len(sections)} zones, {sum(1 for n in IX['named'] if nums(n.get('loc')))} positions")
