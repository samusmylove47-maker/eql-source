"""Zone geometry: game meshes in, our own floor outlines out.

WHAT THIS IS FOR
----------------
The plates held coordinates and nothing to hang them on, which readers fairly
called "just dots on a screen". This derives the floor plan of each zone from
the game's own geometry so the dots sit in rooms.

WHY IT IS OURS TO PUBLISH
-------------------------
This reads the 3D mesh and computes where the walkable floor ends. It does not
copy anyone's map. Community map packs (Brewall, Goodurden) carry no licence at
all, and their author describes years of hand correction, so their line work is
his. The client's own map files are Daybreak's. Both are used here only as a
check on our output, never as a source for it. See docs/SOURCES.md.

WHAT IS NOT COMMITTED
---------------------
The .s3d archives. They are Daybreak's, they are large, and they are already on
any player's disk. This script reads them from the game install and writes
assets/zone-geometry.json, which is our derived data and is committed. That is
why build.sh does not run this: a rebuild must work without the game installed.

    python3 _build/geometry.py            # reads the default install path
    python3 _build/geometry.py <dir>      # or a directory of .s3d files

AXES, WHICH ARE THE EASY THING TO GET WRONG
-------------------------------------------
The .wld stores each vertex as (worldY, worldX, worldZ) — the same order /loc
prints, and NOT the order the field names suggest. Verified against the game's
own shipped map files for six zones and against two community sets for the four
the client does not ship; all ten agree on the extent.

Page coordinates follow the project's existing convention, north up, west left:

    page_x = -worldX = -mesh[1]
    page_y = -worldY = -mesh[0]
    elevation = worldZ = mesh[2]     true elevation, not negated
"""
import os, sys, json, struct, math, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

DEFAULT_EQ = r"C:/Users/Public/Daybreak Game Company/Installed Games/EverQuest Legends"

# zone slug -> the game's short name for the archive
SHORT = {'najena': 'najena', 'splitpaw': 'paw', 'crushbone': 'crushbone',
         'befallen': 'befallen', 'blackburrow': 'blackburrow', 'lowerguk': 'gukbottom',
         'nagafenslair': 'soldungb', 'thehole': 'hole', 'warrens': 'warrens',
         'mistmoore': 'mistmoore'}

FLOOR_N = 0.5      # normal z above this is floor rather than wall
SNAP = 1.0         # vertex snap, world units
SIMPLIFY = 2.0     # Douglas-Peucker tolerance, world units
MIN_CHAIN = 3      # drop boundary chains shorter than this
MAX_BANDS = 4
MIN_BAND_GAP = 24.0    # world units of vertical separation to call it a new level
MIN_BAND_SHARE = 0.04  # a band holding less than this share of floors is merged


# ---------------------------------------------------------------- PFS (.s3d)
FILENAME_CRC = 0x61580AC9


def _inflate(buf, off, size):
    import zlib
    out = bytearray()
    while len(out) < size:
        dl, _il = struct.unpack_from('<II', buf, off)
        off += 8
        out += zlib.decompress(buf[off:off + dl])
        off += dl
    return bytes(out)


def read_s3d(path):
    buf = open(path, 'rb').read()
    dir_off, magic, _v = struct.unpack_from('<I4sI', buf, 0)
    if magic != b'PFS ':
        raise ValueError(f'{path}: not a PFS archive')
    n = struct.unpack_from('<I', buf, dir_off)[0]
    entries = [struct.unpack_from('<III', buf, dir_off + 4 + i * 12) for i in range(n)]
    names, blobs = None, []
    for crc, off, size in sorted(entries, key=lambda e: e[1]):
        data = _inflate(buf, off, size)
        if crc == FILENAME_CRC:
            cnt = struct.unpack_from('<I', data, 0)[0]
            p, names = 4, []
            for _ in range(cnt):
                ln = struct.unpack_from('<I', data, p)[0]
                p += 4
                names.append(data[p:p + ln - 1].decode('latin-1'))
                p += ln
        else:
            blobs.append(data)
    return dict(zip(names or [], blobs))


# ---------------------------------------------------------------- WLD
WLD_MAGIC = 0x54503D02
XOR_KEY = bytes([0x95, 0x3A, 0xC5, 0x2A, 0x95, 0x7A, 0x95, 0x6A])


def wld_fragments(data, ftype):
    magic, version, count, _h3, _h4, hash_size, _h6 = struct.unpack_from('<7I', data, 0)
    if magic != WLD_MAGIC:
        raise ValueError('not a WLD file')
    off = 28 + hash_size
    out = []
    for _ in range(count):
        size, t = struct.unpack_from('<II', data, off)
        if t == ftype:
            out.append(data[off + 12: off + 8 + size])
        off += 8 + size
    return out, version == 0x00015500


# ---------------------------------------------------------------- mesh 0x36
PASSABLE = 0x0010


def decode_mesh(payload):
    """Solid triangles from one 0x36 fragment, in raw mesh order (Y, X, Z)."""
    o = 20                                   # flags + 4 fragment refs
    cx, cy, cz = struct.unpack_from('<3f', payload, o); o += 12
    o += 12 + 4 + 24                         # params2, max distance, bounds
    (nvert, ntex, nnorm, ncol, npoly, _nvp, _npt, _nvt, _s9, scale) = \
        struct.unpack_from('<10h', payload, o); o += 20
    div = float(1 << scale) if scale > 0 else 1.0
    verts = []
    for _ in range(nvert):
        a, b, c = struct.unpack_from('<3h', payload, o); o += 6
        verts.append((cx + a / div, cy + b / div, cz + c / div))
    o += ntex * 4 + nnorm * 3 + ncol * 4
    tris = []
    for _ in range(npoly):
        flags, i1, i2, i3 = struct.unpack_from('<4H', payload, o); o += 8
        if (flags & PASSABLE) == 0 and max(i1, i2, i3) < nvert:
            tris.append((verts[i1], verts[i2], verts[i3]))
    return tris


def zone_triangles(s3d_path):
    files = read_s3d(s3d_path)
    base = os.path.basename(s3d_path).replace('.s3d', '').lower()
    key = next((k for k in files if k.lower() == base + '.wld'), None)
    if key is None:
        raise ValueError(f'{s3d_path}: no {base}.wld inside')
    frags, _old = wld_fragments(files[key], 0x36)
    tris = []
    for p in frags:
        try:
            tris += decode_mesh(p)
        except (struct.error, IndexError):
            continue
    return tris


def normal_z(t):
    (ax, ay, az), (bx, by, bz), (cx, cy, cz) = t
    ux, uy, uz = bx - ax, by - ay, bz - az
    vx, vy, vz = cx - ax, cy - ay, cz - az
    nz = ux * vy - uy * vx
    m = math.sqrt((uy * vz - uz * vy) ** 2 + (uz * vx - ux * vz) ** 2 + nz * nz)
    return 0.0 if m == 0 else nz / m


# ---------------------------------------------------------------- outlines
def boundary_chains(floors):
    """Polylines where the floor stops, in page coordinates."""
    edges = collections.Counter()
    pos = {}
    for t in floors:
        pts = [(-p[1], -p[0]) for p in t]          # page x,y
        ks = [(round(x / SNAP), round(y / SNAP)) for x, y in pts]
        for k, q in zip(ks, pts):
            pos.setdefault(k, q)
        for a, b in ((ks[0], ks[1]), (ks[1], ks[2]), (ks[2], ks[0])):
            if a != b:
                edges[(a, b) if a < b else (b, a)] += 1

    adj = collections.defaultdict(list)
    unused = set()
    for e, n in edges.items():
        if n == 1:
            unused.add(e)
            adj[e[0]].append(e[1])
            adj[e[1]].append(e[0])

    lines = []
    while unused:
        a, b = next(iter(unused))
        unused.discard((a, b))
        chain = [a, b]
        for _ in range(2):
            while True:
                cur = chain[-1]
                nxt = next((v for v in adj[cur]
                            if ((cur, v) if cur < v else (v, cur)) in unused), None)
                if nxt is None:
                    break
                unused.discard((cur, nxt) if cur < nxt else (nxt, cur))
                chain.append(nxt)
            chain.reverse()
        if len(chain) >= MIN_CHAIN:
            lines.append([pos[k] for k in chain])
    return lines


def simplify(line, tol=SIMPLIFY):
    """Douglas-Peucker, iterative so deep chains cannot blow the stack."""
    if len(line) < 3:
        return line
    keep = [False] * len(line)
    keep[0] = keep[-1] = True
    stack = [(0, len(line) - 1)]
    while stack:
        i, j = stack.pop()
        ax, ay = line[i]
        bx, by = line[j]
        dx, dy = bx - ax, by - ay
        n = math.hypot(dx, dy)
        worst, wi = -1.0, i
        for k in range(i + 1, j):
            px, py = line[k]
            d = (abs(dy * px - dx * py + bx * ay - by * ax) / n) if n else math.hypot(px - ax, py - ay)
            if d > worst:
                worst, wi = d, k
        if worst > tol:
            keep[wi] = True
            stack += [(i, wi), (wi, j)]
    return [p for p, k in zip(line, keep) if k]


def elevation_bands(floors):
    """Split floors into storeys, cutting at the quiet heights between them.

    A zone like Najena is nearly flat and must stay one level; Mistmoore stacks
    three and The Hole drops 926 units, and drawing those on top of each other
    is exactly what makes a flat projection unreadable.

    Splitting on the largest vertical *gaps* does not work, because stairs and
    ramps fill every gap — the distribution is continuous from top to bottom.
    What actually marks a storey is density: floors pile up at the heights people
    stand on, and a ramp contributes a thin smear between them. So find the
    peaks, and cut at the emptiest height between consecutive peaks.
    """
    zs = sorted(sum(p[2] for p in t) / 3.0 for t in floors)
    if len(zs) < 120:
        return [(-1e9, 1e9)]
    lo, hi = zs[0], zs[-1]
    span = hi - lo
    if span < MIN_BAND_GAP * 2:
        return [(-1e9, 1e9)]

    nb = 60
    w = span / nb
    hist = [0] * nb
    for z in zs:
        hist[min(nb - 1, int((z - lo) / w))] += 1
    sm = [sum(hist[max(0, i - 1):i + 2]) / 3.0 for i in range(nb)]

    floor_h = max(sm) * 0.08
    peaks = [i for i in range(nb)
             if sm[i] >= floor_h
             and sm[i] >= sm[max(0, i - 1)] and sm[i] >= sm[min(nb - 1, i + 1)]]
    if len(peaks) < 2:
        return [(-1e9, 1e9)]

    # a storey has to be meaningfully above the one below it
    min_sep = max(MIN_BAND_GAP, span * 0.06)
    kept = [peaks[0]]
    for p in peaks[1:]:
        if (p - kept[-1]) * w >= min_sep:
            kept.append(p)
        elif sm[p] > sm[kept[-1]]:
            kept[-1] = p
    if len(kept) < 2:
        return [(-1e9, 1e9)]

    # cut at the emptiest bin between each pair, keeping the deepest valleys
    valleys = []
    for a, b in zip(kept, kept[1:]):
        i = min(range(a + 1, b + 1), key=lambda k: sm[k])
        valleys.append((sm[i], i))
    valleys.sort()
    cuts = sorted(i for _d, i in valleys[:MAX_BANDS - 1])

    edges, prev = [], lo - 1.0
    for i in cuts:
        edges.append((prev, lo + i * w))
        prev = lo + i * w
    edges.append((prev, hi + 1.0))

    total = len(zs)
    out = []
    for a, b in edges:
        if sum(1 for z in zs if a <= z < b) / total >= MIN_BAND_SHARE:
            out.append((a, b))
    if len(out) < 2:
        return [(-1e9, 1e9)]
    out[0] = (-1e9, out[0][1])
    out[-1] = (out[-1][0], 1e9)
    return out


# ---------------------------------------------------------------- driver
def build(src_dir):
    zones = json.load(open('assets/zones-index.json', encoding='utf-8'))
    out, report = {}, []
    for z in zones:
        short = SHORT.get(z['slug'])
        path = os.path.join(src_dir, short + '.s3d') if short else None
        if not path or not os.path.exists(path):
            report.append((z['slug'], 'no archive', 0, 0))
            continue
        tris = zone_triangles(path)
        floors = [t for t in tris if normal_z(t) > FLOOR_N]
        bands = elevation_bands(floors)
        layers = []
        for lo, hi in bands:
            sel = [t for t in floors if lo <= sum(p[2] for p in t) / 3.0 < hi]
            if not sel:
                continue
            chains = [simplify(c) for c in boundary_chains(sel)]
            chains = [c for c in chains if len(c) >= 3]
            if not chains:
                continue
            # Report the band's height from percentiles, not min/max. Blackburrow
            # has two stray triangles 650 units above everything else, and they
            # stretched a label to "-51..603" for a band that is really flat.
            zc = sorted(sum(p[2] for p in t) / 3.0 for t in sel)
            q = lambda f: zc[min(len(zc) - 1, int(len(zc) * f))]
            layers.append({
                'z': [round(q(0.01)), round(q(0.99))],
                'n': len(sel),
                'lines': [[[round(x), round(y)] for x, y in c] for c in chains],
            })
        layers.sort(key=lambda L: L['z'][0])
        out[z['slug']] = {'short': short, 'layers': layers}
        report.append((z['slug'], f'{len(layers)} layer(s)', len(floors),
                       sum(len(c) for L in layers for c in L['lines'])))

    json.dump(out, open('assets/zone-geometry.json', 'w', encoding='utf-8', newline='\n'),
              separators=(',', ':'))
    size = os.path.getsize('assets/zone-geometry.json')
    print(f"{'zone':14s} {'layers':>12s} {'floor tris':>11s} {'points':>8s}")
    for slug, lay, nf, npts in report:
        print(f"{slug:14s} {lay:>12s} {nf:11d} {npts:8d}")
    print(f"\nassets/zone-geometry.json  {size/1024:.0f} KB")


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_EQ)
