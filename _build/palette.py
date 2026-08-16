"""assets/norrath-palette.json — the colours of Norrath, measured from the game's art.

    python3 _build/palette.py "<path to the EverQuest Legends install>"

Run by hand, like geometry.py and ogcards.py. It needs the game installed and a
rebuild must work on a machine without it.

WHY MEASURE A PALETTE INSTEAD OF CHOOSING ONE
---------------------------------------------
This site's whole method is that a figure comes from a source, is dated, and is
never typed from memory. The design system was the one part exempt from that:
its colours were picked by eye, and the result reads as a generic dark developer
theme rather than as Norrath. Guildmates called it bland, and they were right.

So the palette is measured the same way everything else here is. Each zone's
.s3d holds the textures the zone is actually built from - brick, moss, lava,
bone, water - as DXT1, which stores two endpoint colours per 4x4 block. Reading
every endpoint in every texture and weighting by how often it occurs gives the
true colour distribution of a zone as the game draws it.

Najena comes out ox-blood and rust because Najena IS ox-blood and rust. No
amount of taste would have produced that from a swatch picker, and the number is
checkable against the source, which is the point.

WHAT THIS DOES NOT DO, DELIBERATELY
-----------------------------------
It does not extract, convert, save or publish a single texture. Daybreak's art
stays Daybreak's and is never committed - the same rule geometry.py follows for
the meshes. What comes out is a list of colour values and how common each one
is. A colour is a measurement of the art, not a copy of it, in the same way a
zone's height in game units is a measurement of the mesh.
"""
import os, sys, json, struct, colorsys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, '_build'))
from geometry import read_s3d

# The zones the site covers, plus the two planes and Sky. Keyed by our slug so
# the output joins straight onto zones-index.json.
ZONES = {
    'najena': 'najena', 'splitpaw': 'paw', 'crushbone': 'crushbone',
    'befallen': 'befallen', 'blackburrow': 'blackburrow', 'lowerguk': 'guktop',
    'nagafenslair': 'soldungb', 'thehole': 'hole', 'warrens': 'warrens',
    'mistmoore': 'mistmoore', 'planeoffear': 'fearplane',
    'planeofhate': 'hateplane', 'kedgekeep': 'kedge', 'planeofsky': 'airplane',
}


def rgb565(v):
    """One DXT1 endpoint to 8-bit RGB. The low bits are replicated into the
    empty ones rather than left at zero, which is what the hardware does and
    what stops every colour reading slightly too dark."""
    r = (v >> 11) & 0x1F
    g = (v >> 5) & 0x3F
    b = v & 0x1F
    return (r << 3) | (r >> 2), (g << 2) | (g >> 4), (b << 3) | (b >> 2)


def dxt1_endpoints(data):
    """Every block's two endpoint colours. This is a sample of the texture's
    palette, not a decode of it: we want what colours the art uses and how
    often, and the per-pixel indices do not change that answer enough to be
    worth decompressing 32 KB per texture to find out."""
    out = []
    for o in range(0, len(data) - 7, 8):
        c0, c1 = struct.unpack_from('<HH', data, o)
        out.append(rgb565(c0))
        out.append(rgb565(c1))
    return out


def texture_colours(s3d_path):
    try:
        files = read_s3d(s3d_path)
    except Exception as e:
        return None, str(e)
    hits = collections.Counter()
    n_tex = 0
    for name, blob in files.items():
        if not name.lower().endswith('.bmp') or blob[:4] != b'DDS ':
            continue
        (_size, _flags, h, w, _pitch, _depth, _mips) = struct.unpack_from('<7I', blob, 4)
        fourcc = struct.unpack_from('<4s', blob, 84)[0]
        if fourcc != b'DXT1':
            continue
        n_tex += 1
        for c in dxt1_endpoints(blob[128:]):
            hits[c] += 1
    return (hits, n_tex), None


def describe(rgb):
    r, g, b = (v / 255 for v in rgb)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return dict(hex='#%02X%02X%02X' % rgb, h=round(h * 360), s=round(s * 100),
                l=round(l * 100))


def dominant(hits, k=8):
    """The k most common colours, spread out in hue and lightness.

    A plain most-common list returns eight shades of the same grey, because a
    dungeon is mostly one stone. Colours are bucketed by hue and lightness
    first, and the loudest member of each bucket represents it, so the result
    describes the zone's range rather than its average.
    """
    buckets = collections.defaultdict(collections.Counter)
    for c, n in hits.items():
        d = describe(c)
        # Greys have no meaningful hue, so they go in one bucket per lightness
        # band rather than being scattered across the wheel by rounding noise.
        key = ('grey', d['l'] // 20) if d['s'] < 12 else (d['h'] // 30, d['l'] // 25)
        buckets[key][c] += n
    best = []
    for key, members in buckets.items():
        c, n = members.most_common(1)[0]
        best.append((n, sum(members.values()), c))
    best.sort(key=lambda t: -t[1])
    return [dict(describe(c), weight=tot) for _n, tot, c in best[:k]]


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else None
    if not src or not os.path.isdir(src):
        print('usage: python3 _build/palette.py "<EverQuest Legends install dir>"')
        print('Run by hand. The game is not needed to build the site.')
        return 1
    os.chdir(ROOT)
    out = {}
    for slug, short in ZONES.items():
        p = os.path.join(src, short + '.s3d')
        if not os.path.exists(p):
            print(f'  {slug:<14} no {short}.s3d, skipped')
            continue
        got, err = texture_colours(p)
        if err:
            print(f'  {slug:<14} {err}')
            continue
        hits, n_tex = got
        pal = dominant(hits)
        out[slug] = dict(archive=short + '.s3d', textures=n_tex,
                         samples=sum(hits.values()), palette=pal)
        swatch = ' '.join(c['hex'] for c in pal[:5])
        print(f'  {slug:<14} {n_tex:>3} textures  {sum(hits.values()):>8,} samples  {swatch}')

    doc = {
        '_comment': [
            'The colours of Norrath, measured from the game art by _build/palette.py.',
            'DXT1 endpoint colours across every zone texture, bucketed by hue and',
            'lightness so the list describes a zone range rather than its average.',
            'NO GAME ART IS EXTRACTED, CONVERTED OR PUBLISHED - only colour values.',
            'Run by hand: the game install is not needed to build the site.',
        ],
        'zones': out,
    }
    json.dump(doc, open('assets/norrath-palette.json', 'w', encoding='utf-8',
                        newline='\n'), indent=1)
    print(f'\nnorrath-palette.json: {len(out)} zones measured')
    return 0


if __name__ == '__main__':
    sys.exit(main())
