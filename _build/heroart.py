"""Zone geometry as drawable SVG — the site's own art, from the game's meshes.

Imported by the page generators. No output file of its own.

WHY THIS IS THE ART
-------------------
The site had no imagery at all, and read as documentation rather than as a
reference for a game people love. The obvious fixes are all bad: screenshots are
Daybreak's, stock fantasy art is nobody's, and generated art would be exactly
the "AI slop" the collaborator's guildmates called it.

We already hold something better and nobody else has it. `assets/zone-geometry.json`
is the walkable floor of thirteen zones, derived from the game's own `.s3d`
meshes by `_build/geometry.py`. Drawn as line work it is genuinely beautiful,
it is unmistakably Norrath because it IS Norrath, and it is ours: a measurement
of the world, in exactly the way every number on this site is a measurement.

It also says what the site is for without a sentence of copy. The hero is a
dungeon being surveyed, drawn in as you watch.
"""
import json, os

_CACHE = {}


def load():
    if 'g' not in _CACHE:
        _CACHE['g'] = json.load(open('assets/zone-geometry.json', encoding='utf-8'))
    return _CACHE['g']


def paths(slug, box=1000, layer=None, max_paths=None, precision=1):
    """SVG path data for one zone, normalised into a `box`-sized square.

    Returns (list_of_d_strings, width, height). The zone keeps its aspect ratio
    and is centred, so a caller can drop the paths straight into a viewBox of
    the returned size without distorting the floor plan - a stretched map of a
    real place is worse than no map.

    `precision` is decimal places. Zone coordinates are already integers in game
    units, so 1 is plenty and 0 is usually indistinguishable; the default keeps
    the file small because this is inlined into every page that uses it.
    """
    g = load()
    if slug not in g:
        return [], box, box
    layers = g[slug]['layers']
    if layer is not None:
        layers = [layers[layer]] if layer < len(layers) else []

    pts = [p for l in layers for line in l['lines'] for p in line]
    if not pts:
        return [], box, box
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x0, x1 = min(xs), max(xs)
    y0, y1 = min(ys), max(ys)
    span = max(x1 - x0, y1 - y0) or 1
    scale = box / span
    w = (x1 - x0) * scale
    h = (y1 - y0) * scale
    # centre the smaller dimension inside the square
    ox = (box - w) / 2
    oy = (box - h) / 2

    def fx(v):
        return round((v - x0) * scale + ox, precision)

    def fy(v):
        return round((v - y0) * scale + oy, precision)

    out = []
    for l in layers:
        for line in l['lines']:
            if len(line) < 2:
                continue
            d = 'M' + ' L'.join(f'{fx(p[0])},{fy(p[1])}' for p in line)
            out.append(d)
    if max_paths:
        # Keep the longest paths: they carry the zone's silhouette, and dropping
        # the short ones thins the clutter without changing what it looks like.
        out.sort(key=len, reverse=True)
        out = out[:max_paths]
    return out, box, box


def stats(slug):
    g = load()
    if slug not in g:
        return None
    L = g[slug]['layers']
    return dict(layers=len(L),
                paths=sum(len(l['lines']) for l in L),
                points=sum(len(p) for l in L for p in l['lines']))
