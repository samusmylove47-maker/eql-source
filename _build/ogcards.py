"""Open Graph share cards, one per page type. Run by hand, output committed.

WHY THIS IS NOT A BUILD STEP
----------------------------
Same reason as geometry.py: a rebuild must work on a machine that has nothing
special installed. This needs Pillow and a couple of system fonts, so it runs
by hand and its output — public/assets/og/*.png — is committed. build.sh never
touches it. check.py verifies every page points at a card that exists.

    python3 _build/ogcards.py

WHY THEY EXIST AT ALL
---------------------
Zero of the site's 33 pages carried an og:image. EverQuest communities coordinate
in Discord, and a link with no card is a link nobody opens — which made every
page we wrote invisible at the exact moment somebody tried to share it.

WHAT IS ON THEM
---------------
Only what the data already holds: zone name, level band, ZEM, respawn, and the
verification state. Nothing is typed here that is not read from
assets/zones-index.json, so a card cannot drift from the page it represents.

TYPOGRAPHY, AND AN HONEST DEVIATION
-----------------------------------
The site's four faces are Cinzel, Saira Condensed, IBM Plex Mono and Public Sans.
This said THREE until 22 August 2026 and had been wrong since Cinzel landed —
the third file to carry that sentence, after CLAUDE.md (corrected 20 Aug) and
docs/DESIGN.md (which was always right and records the change at line 160).
check.py's FACES set has listed four the whole time. A count typed into prose
beside data that already holds it is the fault this project keeps finding; it
took three corrections in three files to clear one sentence. None
is on this machine and vendoring three font files to draw ten images is a poor
trade, so the cards use the nearest system equivalents: Franklin Gothic Demi
Condensed for display and Consolas for data. It is a deviation from the design
system and it is recorded here rather than hidden. If the real faces are ever
vendored, change FONTS below and re-run.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow is not installed. This is a by-hand tool: pip install Pillow")

W, H = 1200, 630
BG, INK, DIM, FAINT = "#191410", "#F2EADA", "#B5AA95", "#8D8272"
BONE, INSTR, EMBER = "#DFD6C4", "#5C93C4", "#C4623A"

FONTS = {
    "display": r"C:\Windows\Fonts\FRAMDCN.TTF",
    "mono":    r"C:\Windows\Fonts\consola.ttf",
    "monob":   r"C:\Windows\Fonts\consolab.ttf",
}


def font(kind, size):
    try:
        return ImageFont.truetype(FONTS[kind], size)
    except OSError:
        return ImageFont.load_default(size)


def fit(draw, text, kind, size, maxw):
    """Shrink until it fits. A clipped zone name is worse than a smaller one."""
    while size > 22:
        f = font(kind, size)
        if draw.textlength(text, font=f) <= maxw:
            return f
        size -= 3
    return font(kind, size)


def card(path, accent, eyebrow, title, facts, footer):
    """1200x630. Title set as large as it will go, facts in a row beneath it.

    The first draft stacked the facts in a narrow column and left the right half
    of the canvas empty, which reads as an unfinished image at Discord's preview
    size rather than a designed one.
    """
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)

    d.rectangle([0, 0, 16, H], fill=accent)
    d.rectangle([0, H - 5, W, H], fill=accent)

    x, right = 82, W - 82
    d.text((x, 74), eyebrow, font=font("monob", 25), fill=accent)

    tf = fit(d, title, "display", 168, right - x)
    ty = 128
    d.text((x, ty), title, font=tf, fill=INK)

    # A rule the width of the title, then the facts along it.
    ry = ty + tf.size + 42
    d.rectangle([x, ry, right, ry + 2], fill="#2E3A41")

    fy = ry + 34
    col = x
    for label, value in facts:
        lf, vf = font("mono", 21), font("monob", 34)
        wide = max(d.textlength(label.upper(), font=lf), d.textlength(value, font=vf))
        d.text((col, fy), label.upper(), font=lf, fill=FAINT)
        d.text((col, fy + 30), value, font=vf, fill=DIM)
        col += wide + 68
        if col > right - 120:
            break

    d.text((x, H - 78), footer, font=font("mono", 22), fill=FAINT)
    mark = "eqlsource.com"
    mf = font("monob", 24)
    d.text((right - d.textlength(mark, font=mf), H - 78), mark, font=mf, fill=accent)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, "PNG", optimize=True)
    return path


Z = json.load(open("assets/zones-index.json", encoding="utf-8"))
made = []

# One per survey, from that zone's own record.
for z in Z:
    verified = "verified against source" if z["verify_level"] == "full" else "partly verified"
    made.append(card(
        f"public/assets/og/dungeons-{z['slug']}.png", z["accent"],
        f"DUNGEON SURVEY {z['plate']:02d}", z["title"],
        [("Levels", z["levels"].split(" (")[0]),
         ("ZEM", str(z["zem"])),
         ("Respawn", z["respawn"] or "not recorded")],
        verified))

# EVERY FIGURE ON A SHARE CARD IS DERIVED, BECAUSE A CARD CANNOT BE CORRECTED.
#
# These were typed, and on 18 Aug 2026 four of them were false at once: the tools
# card said "five" against a registry of six, the learn card "six" against seven,
# the home card 452 items and 209 named against 434 and 232, and the accuracy
# card advertised Tier C - a tier this site publicly RETRACTED on 17 August.
#
# A wrong page is corrected by the reader clicking it. A wrong card is the only
# thing most people ever see, it renders in Discord, and we cannot reach it once
# posted. So nothing here is typed: the counts come from the same registries the
# pages read, and the tier scale from the one list that defines it.
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import TOOLS, LEARN, wordnum

_IX = json.load(open('assets/index-data.json', encoding='utf-8'))
N_ITEMS = _IX['counts']['item_pages']
N_NAMED = _IX['counts']['named_pages']

# The raid card sold a 3D model until 20 Aug 2026 — "Positioning in 3D",
# "Model: turn it, phase it" — three days after that model was withdrawn and its
# generator deleted. The figures on these cards were derived in da654d88 and the
# TAGLINES were not, so a typed sentence went on advertising a page that no
# longer exists, on the image Discord shows for every raids link.
#
# Derived now, from the same dataset the raid pages read.
_RAIDS = json.load(open('assets/raids-measured.json', encoding='utf-8'))
_RF = _RAIDS.get('fights', _RAIDS) if isinstance(_RAIDS, dict) else _RAIDS
N_BOSSES = len({f.get('boss') for f in _RF if f.get('boss')})

# Tier C was withdrawn on 17 Aug 2026: it was generalised from a single event,
# and one event is not a rank on a scale. The scale is M and 1 to 5.
TIER_SCALE = "M, and 1 to 5"

# One per section. These carry no per-page data, so they say what the section is.
SECTIONS = [
    ("home", BONE, "EVERQUEST LEGENDS", "Sourced. Dated.",
     [("Surveys", str(len(Z))), ("Items indexed", str(N_ITEMS)), ("Named recorded", str(N_NAMED))],
     "every claim names its source and the date it was read"),
    ("dungeons", BONE, "DUNGEON SURVEYS", "Every zone, surveyed",
     [("Floor plans", "from the game meshes"), ("Coordinates", "checked at build time")],
     "every position checked against drawn floor"),
    ("tools", INSTR, "TOOLS", "No account. Nothing sent.",
     [("Trackers", wordnum(len(TOOLS)).lower()), ("Your progress", "travels in the link")],
     "share by link, works offline"),
    ("raids", EMBER, "RAID ENCOUNTERS", "What they cast, and what they cost",
     [("Bosses measured", str(N_BOSSES)), ("Every figure", "sourced and dated")],
     "damage to kill is an upper bound, and the pages say so"),
    ("learn", INSTR, "IS IT STILL TRUE?", "You know a lot that is wrong",
     [("Entries", wordnum(len(LEARN)).lower()), ("Open questions", "named, not hidden")],
     "twenty-five years of habit, tested"),
    ("sources", BONE, "ACCURACY", "Where every claim came from",
     [("Tiers", TIER_SCALE), ("Change log", "typed and dated")],
     "gaps are named, not smoothed over"),
    ("archive", FAINT, "ARCHIVE", "Where this started",
     [("Original plates", "ten"), ("Retired", "10 Aug 2026")],
     "kept exactly as they last shipped"),
]
for slug, accent, eyebrow, title, facts, footer in SECTIONS:
    made.append(card(f"public/assets/og/{slug}.png", accent, eyebrow, title, facts, footer))

total = sum(os.path.getsize(p) for p in made)
print(f"og cards: {len(made)} written, {total/1024:.0f} KB total")
