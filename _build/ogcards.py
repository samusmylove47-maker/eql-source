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
The site's three faces are Saira Condensed, IBM Plex Mono and Public Sans. None
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
BG, INK, DIM, FAINT = "#10161A", "#E6E9E4", "#AEB9B8", "#7D9096"
BONE, INSTR, EMBER = "#D5DBD8", "#5C93C4", "#C4623A"

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

# One per section. These carry no per-page data, so they say what the section is.
SECTIONS = [
    ("home", BONE, "EVERQUEST LEGENDS", "Sourced. Dated.",
     [("Surveys", str(len(Z))), ("Items indexed", "452"), ("Named recorded", "209")],
     "every claim names its source and the date it was read"),
    ("dungeons", BONE, "DUNGEON SURVEYS", "Every zone, surveyed",
     [("Floor plans", "from the game meshes"), ("Coordinates", "checked at build time")],
     "walls drawn from the game's own files"),
    ("tools", INSTR, "TOOLS", "No account. Nothing sent.",
     [("Trackers", "five"), ("Your progress", "travels in the link")],
     "share by link, works offline"),
    ("raids", EMBER, "RAID ENCOUNTERS", "Positioning in 3D",
     [("Model", "turn it, phase it"), ("Every figure", "sourced and dated")],
     "schematic where it is schematic, and it says so"),
    ("learn", INSTR, "IS IT STILL TRUE?", "You know a lot that is wrong",
     [("Entries", "six"), ("Open questions", "named, not hidden")],
     "twenty-five years of habit, tested"),
    ("sources", BONE, "ACCURACY", "Where every claim came from",
     [("Tiers", "M, 1 to 5, and C"), ("Change log", "typed and dated")],
     "gaps are named, not smoothed over"),
    ("archive", FAINT, "ARCHIVE", "Where this started",
     [("Original plates", "ten"), ("Retired", "10 Aug 2026")],
     "kept exactly as they last shipped"),
]
for slug, accent, eyebrow, title, facts, footer in SECTIONS:
    made.append(card(f"public/assets/og/{slug}.png", accent, eyebrow, title, facts, footer))

total = sum(os.path.getsize(p) for p in made)
print(f"og cards: {len(made)} written, {total/1024:.0f} KB total")
