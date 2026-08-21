"""raids/plane-of-sky.html — the zone as a survey sheet.

THE FORMAT
----------
This page is on the Castle Mistmoore survey format, which the site's owner calls
its best guide section. The order is fixed and it is the point:

  masthead (eyebrow, Cinzel title, subtitle, deck) -> particulars strip ->
  jump strip -> the drawing -> cautions, high -> the roster -> what drops ->
  what it costs -> the measured chart -> what is still open.

Cautions sit second rather than last, because a hazard read after the fact is
not a warning. The roster is the payload and it is a table, not prose.

The sheet grammar is copied from _build/source/mistmoore.html — a fixed
graticule behind, a neatlined sheet sliding over it, section kickers hanging in
the left margin — but not its colours. Mistmoore keeps its zone accent; raids
keep ember. This page loads assets/site.css and the block below rides on top of
it, so every token here is the site's own.

WHAT THE PAGE PUBLISHES
-----------------------
  THE RING. Sky's teleporters form a cycle - 1 to 2 to ... to 8, and 8 back to
  1 - with island 1.5 hanging off it as a shortcut. Structure, true for
  everyone, and nothing measured contradicts a single edge of it.

  THE KEY CHAIN. Three keys bought from the Key Master on island 1, then every
  boss drops the key to the next island. How many of those drops are confirmed
  is COUNTED from the parse, not typed: the page said "six of seven" in three
  places, which is three copies of a figure free to drift from its data.

  THE ELEVATION. Read from airplane.s3d by _build/skyislands.py. 2,878 units of
  vertical range across 21 separate bodies of walkable floor, still unlabelled
  and still saying so.

WHAT THE MEASUREMENT DOES NOT COVER, AND SAYS SO
------------------------------------------------
Every Sky figure here is at base difficulty. Nothing generalises to D1 and
above, and the page states that where the figures are, not in a footnote.

Damage to kill is not hit points. It is an upper bound on them, and where the
parser marked a fight `damage_is_floor` the fight was joined after the boss was
engaged and the total is a lower bound instead. Both print as what they are.

NO DIARY
--------
The page publishes findings about the zone, not a record of anyone's play. No
kill counts, no fight counts, no attacker counts, no session dates, no
experience per kill, no character names. A tier M badge already means the claim
was measured in play; the page does not have to publish the log to earn it.
Contributors are credited on credits.html, once, with a link to their work.
"""
import os, sys, json, math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

SKY = json.load(open('assets/sky-islands.json', encoding='utf-8'))
ISL = SKY['islands']
LOOT = json.load(open('assets/sky-loot.json', encoding='utf-8'))
RAIDS = json.load(open('assets/raids-measured.json', encoding='utf-8'))

MEAS = {b['boss']: b for b in LOOT['bosses']}
FIGHTS = LOOT['fights']            # build-console diagnostics only, never rendered

# The most-resisted spell in the zone, read from the parse rather than typed.
# The bee island names it, and a typed spell name goes stale exactly the way a
# typed count does: the tactic line here cited a resist count that the parse had
# since quadrupled.
TOP_RESIST = max(LOOT['resisted'].items(), key=lambda kv: sum(kv[1].values()))[0]

# THE ZONE, IN THE ORDER YOU DO IT.
#
# This replaced a "circuit" ordering optimised for repeat farming, which is not
# what someone opening this page needs: they need the progression. Structure —
# which teleporter goes where, which boss holds which key — is agreed by two
# independent post-launch accounts and contradicted by nothing in our logs.
#
# `boss` joins to the measured table by name. A spelling that drifts here shows
# up as an island with no figures rather than silently printing nothing.
#
# `tactics` is gone from every island. Four of the five lines it held were
# hazards, and a hazard belongs on the hazard rail near the top of the page
# rather than nine screens down beside the boss it happens to concern; the
# other two restated the figure in the column beside them. Everything that
# survived is in Cautions, once.
RING = [
    dict(id="1", name="The landing", boss="Thunder Spirit Princess", key="Key of Swords",
         what="Where the zone drops you, and where the Key Master stands. Nothing here has to die."),
    dict(id="1.5", name="The spur", boss="Noble Dojorn", key="&mdash;",
         what="Off the loop: its teleporter returns you to island 2 rather than to 1, so it costs "
              "nothing to take on the way past."),
    dict(id="2", name="The azarack island", boss="Protector of Sky", key="Key of Misfortune",
         what="Azaracks, with a large aggro radius and a large social radius."),
    dict(id="3", name="The gorgon island", boss="Gorgalosk", key="Key of Beasts",
         what="Gorgons, gazers, and a heart harpie in the tower."),
    dict(id="4", name="The pegasus island", boss="Keeper of Souls", key="Avian Key",
         what="Pegasi, and adds that keep coming. The Overseer of Air stands at the windmill "
              "tower and is a second kill on the same island."),
    dict(id="5", name="The spiroc island", boss="The Spiroc Lord", key="Key of the Swarm",
         what="Spirocs, with a low aggro radius and a high social one. The Spiroc Guardian is "
              "here too."),
    dict(id="6", name="The bee island", boss="Bazzt Zzzt", key="Key of Scale",
         what="Six named bees, not one &mdash; Bazzt Zzzt, Bazzzazzt, Bzzazzt, Bzzzt, Bizazzzt "
              "and Bzizzzt all spawn here, and no published source names more than the first."),
    dict(id="7", name="The spire", boss="Sister of the Spire", key="Veeshan&rsquo;s Key",
         what="Almost empty. Nothing here aggros except the boss."),
    dict(id="8", name="The final island", boss="Eye of Veeshan", key="&mdash;",
         what="Two bosses. The Eye sits at the front; the Hand of Veeshan wanders the back, near "
              "the teleporter that returns you to the landing."),
]
SPUR = RING[1]

# The key chain, counted rather than typed. KEYS is what the parse confirms;
# PREDICTED is what the ring above says should drop. Both sides of "six of
# seven" now come from a source that moves when the evidence does.
KEYS = {k['key']: k for k in LOOT['keys']}
PREDICTED = [i for i in RING if i['key'] not in ('&mdash;', None)]
CONFIRMED = [i for i in PREDICTED if i['key'].replace('&rsquo;', "'") in KEYS]
UNCONFIRMED = [i for i in PREDICTED if i not in CONFIRMED]

# For scale. Read from the same parser as the Sky figures rather than typed, so
# the comparison cannot drift away from the table it compares against.
def plane_god(name):
    fs = [f for f in RAIDS if f['boss'] == name and f['difficulty'] == 4]
    return max((f['damage_low'] for f in fs), default=None)


CT = plane_god('Cazic-Thule')
BIGGEST = max(b['damage_max'] for b in LOOT['bosses'])
RATIO = round(CT / BIGGEST) if CT else None


def fmt(n):
    return f"{n:,}"


def label(name):
    """The log writes "the Hand of Veeshan" with a lowercase article, which is
    correct as a join key and looks like a typo at the head of a table row.
    Capitalised for display only - the key that matches the measured data is
    never touched."""
    return name[0].upper() + name[1:] if name[:1].islower() else name


def dmg_cell(b):
    """A floor is marked wherever the figure appears. The bee table printed the
    bare number while the boss table above it said "or more" for the same
    fight, which is two different claims about one measurement."""
    d = fmt(b['damage_max'])
    return f'{d}&nbsp;<em>or more</em>' if b['damage_max_is_floor'] else d


# ---------------------------------------------------------------- the ring SVG
def ring_svg():
    W = H = 560
    cx = cy = W / 2
    R = 196
    pts = {}
    n = len(RING)
    for i, isl in enumerate(RING):
        a = -math.pi / 2 + i * 2 * math.pi / n
        pts[isl["id"]] = (cx + R * math.cos(a), cy + R * math.sin(a))
    # 1.5 sits inside the arc between 1 and 2
    a1 = -math.pi / 2
    a2 = -math.pi / 2 + 2 * math.pi / n
    am = (a1 + a2) / 2
    pts["1.5"] = (cx + (R - 62) * math.cos(am), cy + (R - 62) * math.sin(am))

    out = [f'<svg viewBox="0 0 {W} {H}" role="img" '
           f'aria-label="The Plane of Sky teleporter network, a ring of eight islands with '
           f'island 1.5 as a spur">']
    out.append('<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" '
               'markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/>'
               '</marker></defs>')
    # ring arcs
    for i in range(n):
        a, b = RING[i]["id"], RING[(i + 1) % n]["id"]
        (x1, y1), (x2, y2) = pts[a], pts[b]
        out.append(f'<path class="edge" d="M{x1:.1f},{y1:.1f} A{R},{R} 0 0 1 {x2:.1f},{y2:.1f}" '
                   f'marker-end="url(#ar)"/>')
    # the spur, both directions
    for a, b in (("1", "1.5"), ("1.5", "2")):
        (x1, y1), (x2, y2) = pts[a], pts[b]
        out.append(f'<line class="edge spur" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" '
                   f'y2="{y2:.1f}" marker-end="url(#ar)"/>')
    # nodes. A dashed node is a boss with no measurement of its own, which on
    # today's data is island 1 and only island 1. Nodes were also ringed to mark
    # one night's kill order, which said nothing about the zone and everything
    # about a session; that highlight is gone.
    for isl in RING + [SPUR]:
        x, y = pts[isl["id"]]
        big = isl["id"] != "1.5"
        unseen = isl["boss"] not in MEAS
        cls = " unseen" if unseen else ""
        out.append(f'<g class="node{cls}" data-i="{isl["id"]}">')
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{26 if big else 19}"/>')
        out.append(f'<text class="nid" x="{x:.1f}" y="{y + 5:.1f}">{isl["id"]}</text>')
        lx = cx + (R + 46) * (x - cx) / max(1e-6, math.hypot(x - cx, y - cy))
        ly = cy + (R + 46) * (y - cy) / max(1e-6, math.hypot(x - cx, y - cy))
        if big:
            out.append(f'<text class="nb" x="{lx:.1f}" y="{ly:.1f}">{isl["boss"]}</text>')
        out.append('</g>')
    out.append(f'<text class="ctr" x="{cx}" y="{cy - 6}">8 teleporters,</text>')
    out.append(f'<text class="ctr" x="{cx}" y="{cy + 16}">one loop</text>')
    out.append('</svg>')
    return "".join(out)


# --------------------------------------------------------- the elevation SVG
def elev_svg():
    W, H = 900, 380
    pad = 46
    xs = [i["cx"] for i in ISL]
    x0, x1 = min(xs), max(xs)
    z0, z1 = SKY["zmin"], SKY["zmax"]
    sx = lambda v: pad + (v - x0) / (x1 - x0) * (W - pad * 2)
    sz = lambda v: H - pad - (v - z0) / (z1 - z0) * (H - pad * 2)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Side elevation of the Plane of Sky, '
           f'{len(ISL)} bodies of walkable floor across {z1 - z0:.0f} units of height">']
    g = int(math.floor(z0 / 500) * 500)
    while g <= z1:
        y = sz(g)
        out.append(f'<line class="grid" x1="{pad}" y1="{y:.1f}" x2="{W - pad}" y2="{y:.1f}"/>')
        out.append(f'<text class="gl" x="{pad - 8}" y="{y + 4:.1f}">{g:+,}</text>')
        g += 500
    for i in ISL:
        x, y = sx(i["cx"]), sz(i["z"][1])
        r = max(4.0, min(26.0, math.sqrt(i["n"]) * 0.75))
        out.append(f'<ellipse class="isl" cx="{x:.1f}" cy="{y:.1f}" rx="{r:.1f}" '
                   f'ry="{max(2.5, r * 0.34):.1f}"><title>{i["n"]} floor triangles, '
                   f'centre {i["cx"]:.0f}, {i["cy"]:.0f}, height {i["z"][1]:.0f}</title></ellipse>')
    out.append(f'<text class="ax" x="{W - pad}" y="{H - 12}">west &rarr; east</text>')
    out.append(f'<text class="ax" x="{pad}" y="{H - 12}">height in game units, read from the mesh</text>')
    # VERTICAL EXAGGERATION, STATED.
    # The two axes are not at the same scale and never were: the horizontal
    # spans 3,059 units across the same drawing width that the vertical uses
    # for 2,878, so height is drawn at 0.38 of its true relative size and Sky
    # reads 2.6x flatter than it is. Every section drawing in every surveying
    # discipline prints this figure, for exactly this reason. Without it the
    # chart is an invented proportion, which is the one thing this site does
    # not publish - and it had been live since 11 Aug 2026.
    # Computed from the scales themselves so it cannot drift from the drawing.
    px_x = (W - pad * 2) / (x1 - x0)
    px_z = (H - pad * 2) / (z1 - z0)
    ve = px_z / px_x
    out.append(f'<text class="ax ve" x="{W - pad}" y="{pad - 16}">'
               f'vertical exaggeration &times;{ve:.2f}</text>')
    out.append('</svg>')
    return "".join(out)


# The elevation drawing's vertical exaggeration, from the same numbers the
# drawing scales by. The page states it in prose as well as on the chart, and
# both read this rather than either typing it.
_EXS = [i["cx"] for i in ISL]
ELEV_VE = ((380 - 92) / (SKY["zmax"] - SKY["zmin"])) / ((900 - 92) / (max(_EXS) - min(_EXS)))


def deepest_survey():
    """The tallest vertical span among the dungeons this site has drawn.

    A section drawing with no yardstick is unreadable, so the elevation's key
    compares Sky to the deepest zone we have surveyed. That comparison used to
    read "about 600 units", which assets/zone-geometry.json contradicts — the
    figure was typed beside the dataset it claims to come from, the fault
    CLAUDE.md section 3 records and _build/backstab.py exists to prevent.

    Read here instead, over the walkable floor of every drawn zone, so a deeper
    survey moves the sentence on the next build. Rounded to 50 units because the
    sentence says "about": Sky is measured from raw mesh extremes and the zone
    layers from trimmed percentiles, and a comparison across two slightly
    different measurements has no business printing a unit digit.
    """
    try:
        G = json.load(open('assets/zone-geometry.json', encoding='utf-8'))
    except (OSError, ValueError):
        return None
    best = 0
    for z in G.values():
        zs = [L['z'] for L in (z.get('layers') or []) if L.get('z')]
        if zs:
            best = max(best, max(v[-1] for v in zs) - min(v[0] for v in zs))
    return round(best / 50) * 50 if best else None


DEEPEST = deepest_survey()
DEEP_NOTE = (f' For comparison, the deepest dungeon surveyed on this site spans about '
             f'{DEEPEST:,.0f} units top to bottom.' if DEEPEST else '')

# ------------------------------------------------------------- the roster


def isle_rows():
    """One block per island, in the order a group actually does them."""
    out = []
    for i in RING:
        m = MEAS.get(i['boss'])
        if m:
            # Damage to kill is a property of the boss - an upper bound on its
            # health. How long a fight ran and how many people were in it are
            # properties of one evening, so neither is published.
            fig = (f'<span class="isle-fig"><b>{dmg_cell(m)}</b> damage to kill'
                   f'<span><span class="tier tM">M</span></span></span>')
            drops = ", ".join(x['item'] for x in m['loot'][:4])
            loot = f'<p class="isle-loot"><em>Drops</em> {drops}</p>' if drops else ''
        else:
            # Island 1's boss carries no measurement at all. Saying so on the
            # island is more use than a blank cell in a table elsewhere.
            fig = ('<span class="isle-fig isle-none"><b>Not recorded</b>'
                   '<span>no measured figure</span></span>')
            loot = ''
        key = (f'<span class="isle-key">Drops {i["key"]}</span>'
               if i['key'] not in ('&mdash;', None) else '')
        out.append(f'''      <li class="isle" id="island-{i["id"].replace(".","-")}">
        <span class="isle-n">{i["id"]}</span>
        <div class="isle-body">
          <h3 class="isle-name">{i["name"]}</h3>
          <p class="isle-boss">{i["boss"]} {key}</p>
          <p class="isle-what">{i["what"]}</p>
          {loot}
        </div>
        {fig}
      </li>''')
    return "\n".join(out)


# Three renderers stood here and none of them was called by the page: a boss
# cost table carrying fight counts, fight lengths, attacker ranges and
# experience per kill; a bee table carrying fight counts; and a key-chain list
# that printed "confirmed &times;N". Dead code that renders a class of figure
# the site no longer publishes is a loaded gun, so it is gone rather than
# tidied.

EFR = LOOT['efreeti_sources']


def seen_list(items):
    """The pieces a mob has been seen to drop, named and not counted. A tally of
    how many times each landed is a record of one player's farming, and the
    table's claim - that this mob is a source of the efreeti line - does not
    need it."""
    return ", ".join(items)


efr_rows = "\n".join(
    f'<tr><td class="dname">{label(mob)}</td><td class="dnote">{seen_list(items)}</td></tr>'
    for mob, items in EFR.items())

CSS = '''<style>
/* THE SKY SHEET
   ------------------------------------------------------------------
   The Castle Mistmoore grammar, on a page that loads assets/site.css: a fixed
   graticule behind, a translucent neatlined sheet sliding over it, and section
   kickers hanging in the left margin as marginalia.

   COPY THE MECHANISM, NOT THE COLOURS. Mistmoore is washed in its own zone
   accent; raids own ember, so --acc is ember here and every other value is a
   site token. Nothing below invents a colour, a size or a spacing step.

   This block is injected after site.css, so it wins at equal specificity. Two
   collisions are deliberate: site.css paints body and this page needs the
   background on html instead, so the graticule can sit above it; and site.css
   already owns body::after for the site-wide grain, so the washes ride on
   main.sky::before rather than displacing it. */
:root{--acc:var(--ember);--acct:var(--ember-t)}
html{background:var(--surface-0)}
body{background:transparent}

/* THE GRATICULE. Fixed to the viewport rather than background-attachment:fixed,
   so the sheet slides over a stationary grid without a full-page repaint.

   Two deliberate mechanics, both carried over intact. Major and minor rules
   share ONE 152px period per axis instead of two stacked gradients, because
   stacking makes the crossings compound and the compounding is what eats text
   contrast — with one period only two rules can ever coincide. And every stop
   terminates in rgba(228,210,174,0) rather than the keyword transparent,
   because older WebKit premultiplies transparent as transparent BLACK and draws
   a grey seam down each rule. */
body::before,main.sky::before{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none}
body::before{background-image:
  repeating-linear-gradient(180deg,
    rgba(228,210,174,.050) 0 1px, rgba(228,210,174,0) 1px 38px,
    rgba(228,210,174,.020) 38px 39px, rgba(228,210,174,0) 39px 76px,
    rgba(228,210,174,.020) 76px 77px, rgba(228,210,174,0) 77px 114px,
    rgba(228,210,174,.020) 114px 115px, rgba(228,210,174,0) 115px 152px),
  repeating-linear-gradient(90deg,
    rgba(228,210,174,.034) 0 1px, rgba(228,210,174,0) 1px 38px,
    rgba(228,210,174,.014) 38px 39px, rgba(228,210,174,0) 39px 76px,
    rgba(228,210,174,.014) 76px 77px, rgba(228,210,174,0) 77px 114px,
    rgba(228,210,174,.014) 114px 115px, rgba(228,210,174,0) 115px 152px)}
/* Lamplight at the head of the sheet, ember bleeding up from the foot, and a
   vignette that ONLY darkens — so it cannot cost contrast anywhere. The two
   washes are anchored at opposite ends and both fall to zero by 62%, so they
   never peak on the same pixel. */
main.sky::before{background-image:
  radial-gradient(115% 60% at 50% 0%, rgba(201,146,46,.060) 0%, rgba(201,146,46,0) 62%),
  radial-gradient(120% 55% at 50% 100%, rgba(196,72,46,.045) 0%, rgba(196,72,46,0) 60%),
  radial-gradient(135% 105% at 50% 42%, rgba(0,0,0,0) 44%, rgba(0,0,0,.42) 100%)}
@media print{body::before,main.sky::before{display:none}}
@media (prefers-contrast:more){body::before{display:none}}

/* THE SHEET. Translucent, so the graticule reads through it at reduced
   strength: one grid, two intensities. One soft shadow, because it floats. */
.sky-wrap{max-width:1200px;margin:0 auto;padding:var(--s-6) clamp(10px,2vw,26px) var(--s-8)}
.sheet{position:relative;padding:0 clamp(16px,3vw,44px) var(--s-8);
  background:color-mix(in srgb, var(--surface-0) 58%, transparent);border:1px solid var(--rule2);box-shadow:var(--shadow-2)}
.sheet::before{content:"";position:absolute;inset:var(--s-2);pointer-events:none;
  border:1px solid rgba(242,234,218,.085)}

/* THE CARTOUCHE. A chart's title block: eyebrow, name, a dotted leader running
   to the island count, then the particulars. */
.mast{padding:var(--s-7) 0 var(--s-5);border-bottom:1px solid var(--rule2)}
.mast .eyebrow{font-size:var(--t-2xs);letter-spacing:var(--tr-widest);color:var(--acct);
  margin:0 0 var(--s-4)}
.title{display:flex;align-items:flex-end;gap:var(--s-4)}
.mast h1{font-family:"Cinzel",Georgia,serif;font-weight:700;font-size:clamp(38px,6.6vw,74px);
  line-height:1.02;letter-spacing:.015em;margin:0;text-transform:uppercase;text-wrap:balance;
  color:var(--bone)}
.leader{flex:1 1 40px;height:1px;margin-bottom:.42em;
  background-image:repeating-linear-gradient(90deg,var(--rule2) 0 1px,rgba(0,0,0,0) 1px 5px)}
.plateno{font-family:"Cinzel",Georgia,serif;font-weight:700;line-height:.9;
  font-size:clamp(30px,5vw,58px);color:var(--acct)}
.subtitle{font-family:"Saira Condensed",sans-serif;font-weight:600;font-size:var(--t-md);
  color:var(--mut);letter-spacing:.02em;margin:var(--s-2) 0 var(--s-3);text-transform:uppercase}
/* THE DECK. What the zone is, what to come for, what kills you, and what the
   evidence does not cover. Four sentences, above everything else. */
.deck{color:var(--txt);margin:0 0 var(--s-5);max-width:66ch}
.deck strong{color:var(--bone)}

/* The particulars. Ruled by cell borders rather than by a coloured gap: with
   auto-fit the last row is often short, and a container background paints that
   empty slot as a slab. */
.strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));margin:0;
  border-top:1px solid var(--rule);border-left:1px solid var(--rule)}
.strip .cell{background:var(--panel);padding:var(--s-3);
  border-right:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.strip dt{font-family:"IBM Plex Mono",monospace;font-size:var(--t-2xs);
  letter-spacing:var(--tr-wide);text-transform:uppercase;color:var(--dim);margin:0 0 var(--s-1)}
.strip dd{margin:0;font-family:"Saira Condensed",sans-serif;font-size:var(--t-lg);
  font-weight:600;color:var(--bone);line-height:1.15}
.strip dd small{font-family:"Public Sans",sans-serif;font-size:var(--t-xs);font-weight:400;
  color:var(--mut);display:block;letter-spacing:0;line-height:1.4}
/* Nine screens with one address and no way down them. */
.jump{margin:var(--s-4) 0 0;padding:0;list-style:none;display:flex;flex-wrap:wrap;
  font-family:"IBM Plex Mono",monospace;gap:var(--s-1) var(--s-4);font-size:var(--t-2xs);
  letter-spacing:var(--tr-wide);text-transform:uppercase}
.jump a{color:var(--mut);text-decoration:none;border-bottom:1px solid var(--rule)}
.jump a:hover{color:var(--bone);border-color:var(--acct)}

/* THE SPINE. Above 1080px the sheet gains a left gutter, a hairline runs the
   length of the body, and each section's kicker hangs outside the text column —
   a rail the eye reads as a plate before it reads a word. The kicker names what
   the section is MADE OF; numbered headings are a generated-site tell. */
.sky-body section{margin-top:var(--s-7);position:relative;padding:0;border:0}
.kick{font-family:"IBM Plex Mono",monospace;font-size:var(--t-2xs);
  letter-spacing:var(--tr-wider);text-transform:uppercase;color:var(--dim);margin:0 0 var(--s-2)}
.sky-body h2{font-family:"Saira Condensed",sans-serif;font-weight:700;text-transform:uppercase;
  font-size:clamp(24px,3.6vw,36px);letter-spacing:.005em;line-height:1;
  margin:0 0 var(--s-2);color:var(--bone)}
@media(min-width:1080px){
  .sky-body{border-left:1px solid var(--rule2);padding-left:var(--s-6);margin-left:118px}
  .kick{position:absolute;left:-186px;width:150px;text-align:right;top:.5em;margin:0}
}
.sky-body .lede{margin:0 0 var(--s-4)}
.sky-body .note{max-width:var(--measure-wide)}

/* Hazards: one object with one rule, not five identically bordered boxes. */
ul.hz{list-style:none;margin:var(--s-5) 0 0;padding:0 0 0 var(--s-5);
  border-left:2px solid var(--warn);max-width:74ch}
ul.hz li{padding:var(--s-4) 0;border-top:1px solid var(--rule);color:var(--mut);
  font-size:var(--t-sm);line-height:1.62}
ul.hz li:first-child{border-top:0;padding-top:0}
ul.hz b{display:block;font-family:"Saira Condensed",sans-serif;font-weight:700;
  text-transform:uppercase;letter-spacing:.06em;font-size:var(--t-base);
  color:var(--warn-t);margin-bottom:var(--s-1)}
ul.hz strong{color:var(--bone)}

/* ---------- the drawings ---------- */
.sky-ring{max-width:620px;margin:0 auto}
.sky-ring svg,.sky-elev svg{display:block;width:100%;height:auto;overflow:visible}
.edge{fill:none;stroke:var(--rule2);stroke-width:1.6;color:var(--rule2)}
.edge.spur{stroke-dasharray:5 4}
.node circle{fill:var(--panel);stroke:var(--rule2);stroke-width:1.6}
/* An island whose boss carries no measurement. Dashed rather than absent: the
   teleporter is there, the boss is the thing that cannot be vouched for. */
.node.unseen circle{stroke-dasharray:4 3;fill:var(--panel)}
.nid{font-family:"Saira Condensed",sans-serif;font-size:19px;font-weight:700;fill:var(--bone);
  text-anchor:middle}
.nb{font-family:"IBM Plex Mono",monospace;font-size:10px;fill:var(--dim);text-anchor:middle;
  letter-spacing:.06em}
.ctr{font-family:"Saira Condensed",sans-serif;font-size:17px;font-weight:600;fill:var(--faint);
  text-anchor:middle;text-transform:uppercase;letter-spacing:.08em}
.sky-elev{border:1px solid var(--rule);background:var(--panel);padding:6px 4px;margin:var(--s-5) 0}
.grid{stroke:var(--rule);stroke-width:1}
.gl,.ax{font-family:"IBM Plex Mono",monospace;font-size:9.5px;fill:var(--faint)}
.gl{text-anchor:end}
.ax:last-of-type{text-anchor:start}
/* The exaggeration figure is not a footnote — it governs how the whole drawing
   should be read, so it sits at the top edge in the brass the chrome uses for
   its own apparatus. text-anchor is set explicitly because the :last-of-type
   rule above would otherwise left-anchor it off the drawing. */
.ve{text-anchor:end!important;fill:var(--brass-t);letter-spacing:.08em}
.isl{fill:color-mix(in srgb, var(--instr) 62%, transparent);stroke:var(--instr);stroke-width:1}

/* ---------- the roster ----------------------------------------------------
   One block per island, in progression order. The number is the island's own
   label — 1.5 really is called that — so it is set as data rather than as a
   list counter, which could only ever produce 1..9. */
.isles{list-style:none;margin:var(--s-5) 0 0;padding:0;display:grid;gap:1px;
  background:var(--rule);border:1px solid var(--rule);border-radius:var(--r);overflow:hidden}
.isle{background:var(--panel);padding:var(--s-5);display:grid;
  grid-template-columns:56px minmax(0,1fr) minmax(0,190px);gap:var(--s-3) var(--s-5);
  align-items:start}
@media(max-width:820px){.isle{grid-template-columns:44px minmax(0,1fr)}
  .isle-fig{grid-column:2;text-align:left}}
.isle-n{font-family:"Cinzel",Georgia,serif;font-size:26px;font-weight:700;color:var(--brass-t);
  line-height:1;font-variant-numeric:tabular-nums}
.isle-name{font-family:"Cinzel",Georgia,serif;font-size:var(--t-lg);font-weight:600;
  text-transform:uppercase;letter-spacing:.02em;color:var(--bone);margin:0 0 4px}
.isle-boss{font-family:"IBM Plex Mono",monospace;font-size:var(--t-xs);letter-spacing:.08em;
  text-transform:uppercase;color:var(--mut);margin:0 0 var(--s-3)}
.isle-key{display:inline-block;margin-left:8px;padding:1px 7px;border:1px solid var(--rule2);
  border-radius:var(--r);color:var(--brass-t);font-size:var(--t-2xs)}
.isle-what{margin:0;color:var(--txt);font-size:var(--t-base);line-height:1.6}
.isle-loot{margin:var(--s-3) 0 0;font-family:"IBM Plex Mono",monospace;font-size:var(--t-2xs);
  letter-spacing:.06em;color:var(--faint);line-height:1.7}
.isle-loot em{font-style:normal;color:var(--dim);text-transform:uppercase;margin-right:6px}
.isle-fig{text-align:right;font-family:"IBM Plex Mono",monospace;font-size:var(--t-2xs);
  color:var(--faint);letter-spacing:.06em;line-height:1.6}
.isle-fig b{display:block;font-family:"Saira Condensed",sans-serif;font-size:var(--t-xl);
  font-weight:700;color:var(--bone);letter-spacing:0;line-height:1.1}
.isle-fig em{font-style:normal;font-size:.7em;color:var(--faint)}
/* The badge sits under the caption rather than jammed against the end of it.
   .tier is inline-flex in site.css, so without this it reads as "damage to
   killM". Scoped to the direct child so the <em> inside the figure — the
   "or more" that marks a floor — is untouched. */
.isle-fig>span{display:block;margin-top:var(--s-1)}
.isle-none b{color:var(--warn-t);font-size:var(--t-lg)}

/* Island 8 is the only ordered procedure on the page, so it is the only thing
   set as numbered steps. */
.steps8{counter-reset:s;list-style:none;margin:var(--s-5) 0 0;padding:0;max-width:74ch}
.steps8 li{counter-increment:s;position:relative;padding:var(--s-4) 0 var(--s-4) 52px;
  border-bottom:1px solid var(--rule);color:var(--txt);line-height:1.65}
.steps8 li:last-child{border-bottom:0}
.steps8 li::before{content:counter(s,decimal-leading-zero);position:absolute;left:0;top:var(--s-4);
  font-family:"IBM Plex Mono",monospace;font-size:var(--t-sm);font-weight:600;color:var(--brass-t)}
.steps8 b{color:var(--bone);font-weight:600}

/* Tables: hairline rules and one brass head rule, which is what a ledger looks
   like. No cell fills and no box around the data. */
.sheet .dtable{border-top:2px solid var(--brass);min-width:520px}
.sheet .dtable th{border-bottom:1px solid var(--rule2)}

/* The page's one large figure: the argument made visible in a glance. */
.scale{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,210px),1fr));
  gap:1px;background:var(--rule);border:1px solid var(--rule);border-radius:var(--r);
  overflow:hidden;margin:var(--s-5) 0 0}
.scale div{background:var(--panel);padding:var(--s-4) var(--s-4)}
.scale .n{font-family:"Saira Condensed",sans-serif;font-size:var(--t-2xl);font-weight:700;
  color:var(--bone);line-height:1.1;margin:0;font-variant-numeric:tabular-nums}
.scale .x{color:var(--brass-t)}
.scale .l{font-family:"IBM Plex Mono",monospace;font-size:var(--t-2xs);color:var(--dim);
  letter-spacing:.08em;text-transform:uppercase;margin:5px 0 0}

/* What is still open. A ledger of gaps, each naming the evidence that closes
   it — the gap is the row, and the right-hand cell is the price. */
.chain{list-style:none;margin:var(--s-5) 0 0;padding:0;display:grid;gap:1px;
  background:var(--rule);border:1px solid var(--rule);border-radius:var(--r);overflow:hidden}
.chain li{background:var(--panel);padding:13px 16px;display:grid;
  grid-template-columns:44px minmax(0,1fr) minmax(0,150px);gap:6px 16px;align-items:baseline}
.chain .i{font-family:"Saira Condensed",sans-serif;font-size:21px;font-weight:700;color:var(--bone)}
.chain .b{font-family:"Saira Condensed",sans-serif;font-size:17px;font-weight:600;color:var(--bone)}
.chain .k{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--instr-t);
  letter-spacing:.05em;text-align:right}
.chain .nt{grid-column:2/-1;color:var(--dim);font-size:14px;line-height:1.55;margin-top:2px}
@media(max-width:620px){.chain li{grid-template-columns:38px minmax(0,1fr)}
  .chain .k{text-align:left;grid-column:2}}

.imprint{font-family:"IBM Plex Mono",monospace;font-size:var(--t-2xs);
  letter-spacing:var(--tr-wide);text-transform:uppercase;color:var(--dim);
  margin:var(--s-7) 0 0;padding-top:var(--s-5);border-top:1px solid var(--rule2)}
</style>'''

page = (head("Plane of Sky",
             "The Plane of Sky measured at base difficulty: the ring of nine islands, the key "
             "chain confirmed in play, and what each boss costs to kill.",
             rel="../", extra=CSS, og="raids", canon="raids/plane-of-sky")
        + bar("../") + f'''
<main class="sky">
<div class="sky-wrap">
<div class="sheet">

<header class="mast">
  <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp;
    <a href="index.html">Raids</a> &nbsp;/&nbsp; Plane of Sky</p>
  <p class="eyebrow">Raid survey</p>
  <div class="title"><h1>The Plane of Sky</h1><span class="leader"></span>
    <span class="plateno">{len(RING)}</span></div>
  <p class="subtitle">Islands on a one-way loop, each gated by a key the island below it drops</p>
  <p class="deck">Every other reference calls Sky a raid zone. <strong>Its dearest boss costs
    about a {RATIO}th of what Cazic-Thule costs at Refined.</strong> Nothing here sees through
    invisibility, so you can walk past almost everything and kill only what you came for &mdash;
    and <strong>falling is what kills people</strong>, on gusts of wind you cannot see. Every
    figure below is base difficulty.</p>
  <dl class="strip">
    <div class="cell"><dt>Access</dt><dd>Key Master<small>island 1, first three keys</small></dd></div>
    <div class="cell"><dt>Key chain</dt><dd>{len(CONFIRMED)} of {len(PREDICTED)}<small>confirmed in play</small></dd></div>
    <div class="cell"><dt>Difficulty</dt><dd>Base<small>D0, the only tier measured</small></dd></div>
    <div class="cell"><dt>See invis</dt><dd>None<small>nothing in the zone</small></dd></div>
    <div class="cell"><dt>Dearest boss</dt><dd>{fmt(BIGGEST)}<small>damage to kill</small></dd></div>
    <div class="cell"><dt>Height</dt><dd>{SKY["zmax"] - SKY["zmin"]:,.0f}<small>units, {len(ISL)} bodies of floor</small></dd></div>
    <div class="cell"><dt>Efreeti gear</dt><dd>{len(EFR)} sources<small>back half of the ring</small></dd></div>
    <div class="cell"><dt>Return</dt><dd>8 &rarr; 1<small>the loop closes</small></dd></div>
  </dl>
  <ul class="jump">
    <li><a href="#cautions">Cautions</a></li>
    <li><a href="#islands">Island by island</a></li>
    <li><a href="#island8">Island 8</a></li>
    <li><a href="#drops">Drops</a></li>
    <li><a href="#cost">What it costs</a></li>
    <li><a href="#elevation">Elevation</a></li>
    <li><a href="#open">Open questions</a></li>
  </ul>
</header>

<div class="sky-body">

<section>
  <p class="kick">The zone, drawn</p>
  <h2 id="ring">The ring</h2>
  <p class="lede">Buy the first three keys from the Key Master on island 1. After that each
    boss drops the key to the next island, so the order is fixed.</p>
  <div class="sky-ring">{ring_svg()}</div>
  <div class="note"><strong>Every confirmed key dropped from exactly the boss the chain
    names</strong> <span class="tier tM">TIER M</span>. The one gap is island
    {UNCONFIRMED[0]["id"]}: the {UNCONFIRMED[0]["boss"]} has never been measured.</div>
</section>

<section>
  <p class="kick">Five hazards</p>
  <h2 id="cautions">Cautions</h2>
  <ul class="hz">
    <li><b>Falling</b> The gusts of wind on island 3 are <strong>invisible</strong> and need
      see-invis to spot. They are why people fall off it.</li>
    <li><b>Social radius</b> Azaracks on 2 and spirocs on 5 bring the island with them. Work the
      rim; the middle is where a pull becomes everything.</li>
    <li><b>Adds that do not stop</b> Island 4 keeps producing them. <strong>Kill to a timer</strong>
      rather than clearing to zero.</li>
    <li><b>The spur&rsquo;s approach</b> A blade storm guards the way on to island 1.5.</li>
    <li><b>Poison on island 6</b> The bees cast {TOP_RESIST}, resisted more often than any other
      spell in the zone.</li>
  </ul>
</section>

<section>
  <p class="kick">Position and behaviour</p>
  <h2 id="islands">Island by island</h2>
  <p class="lede">In progression order. Damage to kill is measured at base difficulty.
    <span class="tier tM">TIER M</span></p>
  <ol class="isles">
{isle_rows()}
  </ol>
</section>

<section>
  <p class="kick">The one procedure</p>
  <h2 id="island8">Island 8, in full</h2>
  <p class="lede">The only part of the zone where the order matters.</p>
  <ol class="steps8">
    <li><b>Go invisible before you take the portal up.</b> You arrive unengaged and choose your
      own opening.</li>
    <li><b>Walk to the back of the island</b>, to the teleporter that returns you to the landing.
      The Hand of Veeshan wanders there.</li>
    <li><b>Kill the Hand first.</b></li>
    <li><b>Then the Eye, where it stands.</b></li>
    <li><b>Slow them both.</b> That is the whole fight.</li>
  </ol>
</section>

<section>
  <p class="kick">Confirmed sources</p>
  <h2 id="drops">Where the efreeti gear comes from</h2>
  <p class="lede">The source of the line was unresolved between this site and eqlegendstools.
    <span class="tier tM">TIER M</span></p>
  <div class="tw"><table class="dtable">
    <thead><tr><th>Dropped by</th><th>Efreeti pieces it drops</th></tr></thead>
    <tbody>
{efr_rows}
    </tbody></table></div>
  <div class="note"><strong>Confirmed sources, not a drop rate.</strong> They do not rule out
    sources elsewhere in the zone.</div>
</section>

<section>
  <p class="kick">The comparison</p>
  <h2 id="cost">What a Sky boss costs</h2>
  <div class="scale">
    <div><p class="n">{fmt(BIGGEST)}</p><p class="l">Dearest boss in Sky</p></div>
    <div><p class="n">{fmt(CT)}</p><p class="l">Cazic-Thule at Refined</p></div>
    <div><p class="n x">{RATIO}&times;</p><p class="l">The difference</p></div>
  </div>
  <div class="note"><strong>Damage to kill is not hit points.</strong> It counts every attacker
    and sits above a boss&rsquo;s health rather than measuring it, so it is a ceiling on the zone
    rather than a target for one character. A figure marked <em>or more</em> comes from a fight
    joined after it started, so it is a floor.</div>
</section>

<section>
  <p class="kick">From the mesh</p>
  <h2 id="elevation">How high it actually is</h2>
  <p class="lede">Read from the zone&rsquo;s own mesh, west to east. <strong>{len(ISL)} separate
    bodies of walkable floor across {SKY["zmax"] - SKY["zmin"]:,.0f} units of height</strong>, from
    {SKY["zmin"]:,.0f} to {SKY["zmax"]:,.0f}. Each mark is sized by how much floor it holds, and a
    tower counts separately from the ground it stands on.{DEEP_NOTE}</p>
  <div class="sky-elev">{elev_svg()}</div>
  <div class="note"><strong>The two axes are not at the same scale.</strong> Height is drawn at
    {ELEV_VE:.2f} of its true size against the horizontal, so <strong>Sky reads about
    {1/ELEV_VE:.1f} times flatter here than it is</strong>.</div>
  <div class="note"><strong>The marks are not labelled, and that is deliberate.</strong> The mesh
    says where every piece of floor is; it does not say which piece is &ldquo;island 4&rdquo;.
    That lives in the teleporter network, and <strong>one <code>/loc</code> per island &mdash;
    {len(RING)} readings &mdash; would label this chart permanently</strong>.</div>
</section>

<section>
  <p class="kick">Named, not smoothed over</p>
  <h2 id="open">What we do not know</h2>
  <ul class="chain">
    <li><span class="i">1</span><span class="b">Anything about Sky above D0</span>
      <span class="k">one logged run</span>
      <span class="nt">One run at Awakened would say whether the tiers change this zone the way
        they change a dungeon.</span></li>
    <li><span class="i">2</span><span class="b">The {UNCONFIRMED[0]["boss"]}</span>
      <span class="k">one kill</span>
      <span class="nt">The only boss on the ring with no measurement of any kind.</span></li>
    <li><span class="i">3</span><span class="b">Which measured body is which island</span>
      <span class="k">{len(RING)} /loc readings</span></li>
    <li><span class="i">4</span><span class="b">Whether there is a tenth island</span>
      <span class="k">one sighting</span>
      <span class="nt">One account counts ten, listing 1&ndash;8, 1.5 and an Efreeti island. The
        efreeti drops do not settle it &mdash; every source is already on the ring.</span></li>
    <li><span class="i">5</span><span class="b">Boss hit points at any difficulty</span>
      <span class="k">nobody has these</span>
      <span class="nt">Every published stat block for these bosses traces to a wiki page created
        before the game existed.</span></li>
    <li><span class="i">6</span><span class="b">Which Sky drops are quest turn-ins</span>
      <span class="k">a turn-in list</span>
      <span class="nt">One account lists items said to be safe to sell. We are not republishing
        it: a reader who vendors a quest component on this site&rsquo;s word has been badly
        served.</span></li>
  </ul>
  <p class="imprint">Plane of Sky &middot; measured at base difficulty &middot; elevation derived
    from airplane.s3d &middot; tactics from players named on the
    <a href="../credits.html">credits page</a></p>
</section>

</div>
</div>
</div>
</main>
''' + foot("../"))

open('public/raids/plane-of-sky.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"raids/plane-of-sky.html rebuilt: ring of {len(RING)}, {len(ISL)} measured bodies, "
      f"{FIGHTS['n']} fights over {FIGHTS['bosses']} bosses, "
      f"{len(CONFIRMED)} of {len(PREDICTED)} keys confirmed")
