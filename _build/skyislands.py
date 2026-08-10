"""Plane of Sky island geometry, from the game's own mesh.

Run by hand, like geometry.py, for the same reason: it reads .s3d archives from
an EverQuest Legends install and a rebuild has to work on a machine without the
game. Output is assets/sky-islands.json, which IS committed.

    python3 _build/skyislands.py            # default install path
    python3 _build/skyislands.py <dir>

WHY THIS IS NOT geometry.py
---------------------------
geometry.py answers "where does the walkable floor stop", which is the right
question for a dungeon: one connected space, storeys stacked. Sky is the
opposite — a set of separate lumps of floor hanging in air with nothing between
them. Bands of elevation would slice islands in half and merge unrelated ones
that happen to share a height.

So this clusters instead. Triangle centroids are unioned when they sit within
GAP units of each other in three dimensions, and each surviving cluster is an
island. That is the shape of the actual problem.

WHAT THIS CAN AND CANNOT SAY
----------------------------
It measures every island's position, extent and height exactly. It CANNOT say
which measured island is "island 4", because that mapping lives in the
teleporter network and not in the geometry, and we have no /loc reading from
Sky to anchor it.

The page built from this says so. One /loc per island closes it, and until then
the islands are presented by measured height, unlabelled, which is the honest
shape of what we know. CLAUDE.md has carried "Plane of Sky geometry — never
surveyed" as an open gap since the site began; this closes the measurement half
of it and leaves the naming half open, out loud.
"""
import os, sys, json, math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
import geometry as G

DEFAULT_EQ = r"C:/Users/Public/Daybreak Game Company/Installed Games/EverQuest Legends"
GAP = 60.0          # 3D union distance. Islands are far further apart than this.
MIN_TRIS = 25       # below this a cluster is scenery, not a place you stand.


def clusters(floors):
    cent = [(sum(q[0] for q in t) / 3, sum(q[1] for q in t) / 3,
             sum(q[2] for q in t) / 3) for t in floors]
    n = len(cent)
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    # A spatial hash keeps this linear-ish. Without it the union pass is 38
    # million distance checks on this zone and takes minutes.
    buckets = {}
    for i, (x, y, z) in enumerate(cent):
        buckets.setdefault((int(x // GAP), int(y // GAP), int(z // GAP)), []).append(i)
    for (kx, ky, kz), ids in buckets.items():
        near = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    near += buckets.get((kx + dx, ky + dy, kz + dz), [])
        for i in ids:
            for j in near:
                if j > i and math.dist(cent[i], cent[j]) <= GAP:
                    ra, rb = find(i), find(j)
                    if ra != rb:
                        parent[rb] = ra
    out = {}
    for i in range(n):
        out.setdefault(find(i), []).append(i)
    return cent, out


def build(src_dir):
    path = os.path.join(src_dir, 'airplane.s3d')
    if not os.path.exists(path):
        raise SystemExit(f"no airplane.s3d under {src_dir}")
    tris = G.zone_triangles(path)
    floors = G.walkable(tris)
    cent, groups = clusters(floors)

    islands = []
    for g in sorted(groups.values(), key=len, reverse=True):
        if len(g) < MIN_TRIS:
            continue
        sel = [floors[i] for i in g]
        gx = [cent[i][0] for i in g]
        gy = [cent[i][1] for i in g]
        gz = [cent[i][2] for i in g]
        chains = [c for c in (G.simplify(c) for c in G.boundary_chains(sel)) if len(c) >= 3]
        # keep the largest outline only; the small interior ones are furniture
        chains.sort(key=len, reverse=True)
        islands.append({
            "n": len(g),
            "cx": round(sum(gx) / len(gx), 1),
            "cy": round(sum(gy) / len(gy), 1),
            "z": [round(min(gz), 1), round(sum(gz) / len(gz), 1), round(max(gz), 1)],
            "w": round(max(gx) - min(gx), 1),
            "h": round(max(gy) - min(gy), 1),
            "outline": [[round(p[0], 1), round(p[1], 1)] for p in chains[0]] if chains else [],
        })
    islands.sort(key=lambda i: -i["z"][1])          # highest first

    allz = [q[2] for t in floors for q in t]
    data = {
        "source": "airplane.s3d",
        "read": "2026-08-11",
        "tris": len(tris),
        "walkable": len(floors),
        "gap": GAP,
        "zmin": round(min(allz), 1),
        "zmax": round(max(allz), 1),
        "islands": islands,
    }
    json.dump(data, open('assets/sky-islands.json', 'w', encoding='utf-8', newline='\n'),
              separators=(',', ':'))
    print(f"sky-islands.json: {len(islands)} islands of {MIN_TRIS}+ triangles, "
          f"vertical range {data['zmax'] - data['zmin']:,.0f} units")
    for k, i in enumerate(islands):
        print(f"   {k+1:>2}  {i['n']:>5} tris  centre {i['cx']:>8.0f},{i['cy']:>8.0f}  "
              f"z {i['z'][1]:>7.0f}  span {max(i['w'], i['h']):>6.0f}")


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_EQ)
