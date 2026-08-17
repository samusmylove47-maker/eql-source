"""raids/plane-of-sky.html — what the zone costs, the ring, and the key chain.

WHY THIS PAGE WAS REWRITTEN, 15 AUGUST 2026
-------------------------------------------
The page described a zone that needs a full raid. It does not, and we now hold
the evidence: 43 boss fights over 14-15 August 2026, 15 named bosses, a median
of four attackers and a thinnest fight of two. The most expensive boss in the
zone cost 26,158 damage. Cazic-Thule at Refined costs 382,035.

That is not a detail to append to a page written the other way round. Every
other reference in this community says "raid", ours said it too, and a reader
planning a night in Sky was being told to bring fifty people to a zone three
can clear. The measured cost is now the page's first section and its headline.

WHAT SURVIVED THE REWRITE
-------------------------
  THE RING. Sky's teleporters form a cycle - 1 to 2 to ... to 8, and 8 back to
  1 - with island 1.5 hanging off it as a shortcut. Structure, true for
  everyone, and the logs did not contradict a single edge of it.

  THE KEY CHAIN. Three keys bought from the Key Master on island 1, then every
  boss drops the key to the next island. The logs confirmed six of the seven
  predicted drops, each from exactly the boss the chain names. That is the
  first independent confirmation of the chain anyone holds.

  THE ELEVATION. Read from airplane.s3d by _build/skyislands.py. 2,878 units of
  vertical range across 21 separate bodies of walkable floor, still unlabelled
  and still saying so.

WHAT THE MEASUREMENT DOES NOT COVER, AND SAYS SO
------------------------------------------------
Every Sky fight we hold is at base difficulty. Nothing here generalises to D1
and above, and the page states that where the figures are, not in a footnote.

Damage to kill is not hit points. It is an upper bound on them, and where the
parser marked a fight `damage_is_floor` we arrived after the boss was engaged
and the total is a lower bound instead. Both are printed as what they are.

NO NAMES, NO TIMES
------------------
Every Sky fight in the logs is a public pick-up raid and our character dealt
between 2% and 63% of the damage. Other players are counted and discarded.
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
FIGHTS = LOOT['fights']

# The ring. `key` is what the boss drops; island 1 is where you buy the first
# three. Structure rather than tactics, and two independent post-launch accounts
# agree on all of it. `boss` is joined to the measured table by name, so a
# spelling that drifts here shows up as an unmeasured island rather than
# silently printing nothing.
# THE ZONE, IN THE ORDER YOU DO IT.
#
# This replaced a "circuit" ordering optimised for repeat farming, which is not
# what someone opening this page needs: they need the progression. Structure —
# which teleporter goes where, which boss holds which key — is agreed by two
# independent post-launch accounts and contradicted by nothing in our logs.
#
# `boss` joins to the measured table by name. A spelling that drifts here shows
# up as an island with no figures rather than silently printing nothing.
RING = [
    dict(id="1", name="The landing", boss="Thunder Spirit Princess", key="Key of Swords",
         what="Where the zone drops you, and where the Key Master stands. The first three keys "
              "are bought here rather than killed for.",
         tactics="Buy your keys before anything else. Nothing on this island has to die."),
    dict(id="1.5", name="The spur", boss="Noble Dojorn", key="&mdash;",
         what="Hangs off the landing rather than sitting on the loop, and its teleporter returns "
              "you to island 2 rather than to 1. A blade storm guards the approach.",
         tactics="The shortest detour in the zone, and it drops the efreeti line."),
    dict(id="2", name="The azarack island", boss="Protector of Sky", key="Key of Misfortune",
         what="Azaracks, with a large aggro radius and a large social radius.",
         tactics="A pull here tends to become the island. Work from the edge."),
    dict(id="3", name="The gorgon island", boss="Gorgalosk", key="Key of Beasts",
         what="Gorgons, gazers, and a heart harpie in the tower.",
         tactics="Gusts of wind are invisible and need see-invis to spot. They are why people "
                 "fall off this island."),
    dict(id="4", name="The pegasus island", boss="Keeper of Souls", key="Avian Key",
         what="Pegasi, and adds that keep coming. The Overseer of Air stands at the windmill "
              "tower and is a second kill on the same island.",
         tactics="Two bosses here, not one. The adds do not stop, so kill to a timer rather "
                 "than clearing to zero."),
    dict(id="5", name="The spiroc island", boss="The Spiroc Lord", key="Key of the Swarm",
         what="Spirocs, with a low aggro radius and a high social one. The Spiroc Guardian is "
              "here too.",
         tactics="The outer edge is quiet and the middle is not. Work the rim."),
    dict(id="6", name="The bee island", boss="Bazzt Zzzt", key="Key of Scale",
         what="Six named bees, not one &mdash; Bazzt Zzzt, Bazzzazzt, Bzzazzt, Bzzzt, Bizazzzt "
              "and Bzizzzt all died here on the same nights, and no source we hold mentions "
              "more than the first.",
         tactics="Do not bring poison. Across four of the six we resisted Deadly Poison 164 "
                 "times, the largest resist count anywhere in the zone."),
    dict(id="7", name="The spire", boss="Sister of the Spire", key="Veeshan&rsquo;s Key",
         what="Almost empty. Nothing here aggros except the boss.",
         tactics="The cheapest boss in the zone and the safest island to regroup on."),
    dict(id="8", name="The final island", boss="Eye of Veeshan", key="&mdash;",
         what="Two bosses. The Eye sits at the front; the Hand of Veeshan wanders the back, near "
              "the teleporter that returns you to the landing.",
         tactics=None),
]
SPUR = RING[1]

CIRCUIT = ["6", "7", "8", "1", "1.5", "4", "8"]     # the six kills, in order taken

# The bee island. Named as the log names them, ordered by how many fights we
# hold, so the table's own evidence sets the order rather than a guess at which
# one is "the" boss.
BEES = ["Bazzt Zzzt", "Bazzzazzt", "Bzzazzt", "Bzzzt", "Bizazzzt", "Bzizzzt"]

# For scale. Read from the same parser as the Sky figures rather than typed, so
# the comparison cannot drift away from the table it compares against.
def plane_god(name):
    fs = [f for f in RAIDS if f['boss'] == name and f['difficulty'] == 4]
    return max((f['damage_low'] for f in fs), default=None)


CT = plane_god('Cazic-Thule')
IN = plane_god('Innoruuk, the Prince of Hate')
BIGGEST = max(b['damage_max'] for b in LOOT['bosses'])
SMALLEST = min(b['damage_max'] for b in LOOT['bosses'] if not b['single_observation'])
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
    # nodes. A ringed node is one the circuit kills; a hollow one is a boss we
    # have never found, which on today's data is island 1 and only island 1.
    for isl in RING + [SPUR]:
        x, y = pts[isl["id"]]
        big = isl["id"] != "1.5"
        kill = isl["id"] in CIRCUIT
        unseen = isl["boss"] not in MEAS
        cls = " kill" if kill else ""
        cls += " unseen" if unseen else ""
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

# ------------------------------------------------------------- the cost table

def isle_rows():
    """One block per island, in the order a group actually does them."""
    out = []
    for i in RING:
        m = MEAS.get(i['boss'])
        if m:
            d = dmg_cell(m)
            atk = (f"{m['attackers_min']}&ndash;{m['attackers_max']}"
                   if m['attackers_min'] != m['attackers_max'] else str(m['attackers_min']))
            secs = (f"{m['seconds_min']}&ndash;{m['seconds_max']}s"
                    if m['seconds_min'] != m['seconds_max'] else f"{m['seconds_min']}s")
            fig = (f'<span class="isle-fig"><b>{d}</b> damage'
                   f'<span>{secs} &middot; {atk} attackers <span class="tier tM">M</span></span></span>')
            drops = ", ".join(x['item'] for x in m['loot'][:4])
            loot = f'<p class="isle-loot"><em>Seen dropping</em> {drops}</p>' if drops else ''
        else:
            # Island 1's boss has never appeared in a log of ours. Saying so on
            # the island is more use than a blank cell in a table elsewhere.
            fig = ('<span class="isle-fig isle-none"><b>Never found</b>'
                   '<span>no kill, no sighting, no log line</span></span>')
            loot = ''
        second = (f' <span class="isle-2nd">and {i["second"]}</span>') if i.get('second') else ''
        tac = f'<p class="isle-tac">{i["tactics"]}</p>' if i.get('tactics') else ''
        key = (f'<span class="isle-key">Drops {i["key"]}</span>'
               if i['key'] not in ('&mdash;', None) else '')
        out.append(f'''      <li class="isle" id="island-{i["id"].replace(".","-")}">
        <span class="isle-n">{i["id"]}</span>
        <div class="isle-body">
          <h3 class="isle-name">{i["name"]}</h3>
          <p class="isle-boss">{i["boss"]}{second} {key}</p>
          <p class="isle-what">{i["what"]}</p>
          {tac}
          {loot}
        </div>
        {fig}
      </li>''')
    return "\n".join(out)


def cost_rows():
    rows = []
    for b in sorted(LOOT['bosses'], key=lambda b: -b['damage_max']):
        d = dmg_cell(b)
        secs = (f"{b['seconds_min']}&ndash;{b['seconds_max']}s"
                if b['seconds_min'] != b['seconds_max'] else f"{b['seconds_min']}s")
        atk = (f"{b['attackers_min']}&ndash;{b['attackers_max']}"
               if b['attackers_min'] != b['attackers_max'] else f"{b['attackers_min']}")
        exp = f"{b['exp_pct_per_kill']:.2f}%" if b['exp_pct_per_kill'] else '&mdash;'
        one = ' <span class="once">once</span>' if b['single_observation'] else ''
        rows.append(
            f'<tr><td class="dname">{label(b["boss"])}{one}</td>'
            f'<td class="dn">{b["fights"]}</td><td class="dn">{d}</td>'
            f'<td class="dn">{secs}</td><td class="dn">{atk}</td><td class="dn">{exp}</td></tr>')
    return "\n".join(rows)


# -------------------------------------------------------------- the key chain
KEYS = {k['key']: k for k in LOOT['keys']}


def chain_rows():
    """The key chain, and whether the log confirmed each link.

    The island descriptions moved into the walkthrough above, so this is now
    only what it is evidence for: which predicted drop actually landed.
    """
    rows = []
    for i in RING:
        if i['key'] in ('&mdash;', None):
            continue
        seen = KEYS.get(i['key'].replace('&rsquo;', "'"))
        if seen and seen['boss'] == i['boss']:
            mark = (f'<span class="ok">confirmed &times;{seen["n"]}</span> '
                    f'<span class="tier tM">M</span>')
        else:
            mark = '<span class="gap">not seen</span>'
        rows.append(
            f'''      <li>
        <span class="i">{i["id"]}</span><span class="b">{i["boss"]}</span>
        <span class="k">{i["key"]}</span>
        <span class="ev">{mark}</span></li>''')
    return "\n".join(rows)


def bee_rows():
    out = []
    for name in BEES:
        b = MEAS.get(name)
        if not b:
            continue
        one = ' <span class="once">once</span>' if b['single_observation'] else ''
        out.append(f'<tr><td class="dname">{label(name)}{one}</td><td class="dn">{b["fights"]}</td>'
                   f'<td class="dn">{dmg_cell(b)}</td>'
                   f'<td class="dnote">{", ".join(i["item"] for i in b["loot"][:3]) or "&mdash;"}</td></tr>')
    return "\n".join(out)


POISON = LOOT['resisted'].get('Deadly Poison', {})
POISON_N = sum(POISON.values())

EFR = LOOT['efreeti_sources']


def seen_list(items):
    """"Efreeti Standard &times;2, Efreeti War Axe" - the count only where it is
    more than one, because "&times;1" reads as a rate and this is a tally."""
    return ", ".join(i if n <= 1 else f'{i} &times;{n}' for i, n in items.items())


efr_rows = "\n".join(
    f'<tr><td class="dname">{label(mob)}</td><td class="dnote">{seen_list(items)}</td></tr>'
    for mob, items in EFR.items())

CSS = '''<style>
.sky-ring{max-width:620px;margin:0 auto}
.sky-ring svg,.sky-elev svg{display:block;width:100%;height:auto;overflow:visible}
.edge{fill:none;stroke:var(--rule2);stroke-width:1.6;color:var(--rule2)}
.edge.spur{stroke-dasharray:5 4}
.node circle{fill:var(--panel);stroke:var(--rule2);stroke-width:1.6}
.node.kill circle{stroke:var(--ember,#D9762A);stroke-width:2.4;
  fill:color-mix(in srgb, var(--ember,#D9762A) 14%, var(--panel))}
/* An island whose boss we have never found. Dashed rather than absent: the
   teleporter is there, the boss is the thing we cannot vouch for. */
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
.chain{list-style:none;margin:var(--s-5) 0 0;padding:0;display:grid;gap:1px;
  background:var(--rule);border:1px solid var(--rule);border-radius:var(--r);overflow:hidden}
.chain li{background:var(--panel);padding:13px 16px;display:grid;
  grid-template-columns:44px minmax(0,1fr) minmax(0,150px);gap:6px 16px;align-items:baseline}
.chain .i{font-family:"Saira Condensed",sans-serif;font-size:21px;font-weight:700;color:var(--bone)}
.chain .b{font-family:"Saira Condensed",sans-serif;font-size:17px;font-weight:600;color:var(--bone)}
.chain .k{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--instr);
  letter-spacing:.05em;text-align:right}
.chain .nt{grid-column:2/-1;color:var(--dim);font-size:14px;line-height:1.55;margin-top:2px}
.chain .ev{grid-column:2/-1;margin-top:6px}
.chain li.kill{background:color-mix(in srgb, var(--ember,#D9762A) 7%, var(--panel))}
@media(max-width:620px){.chain li{grid-template-columns:38px minmax(0,1fr)}.chain .k{text-align:left;grid-column:2}}
.ok,.gap{font-family:"IBM Plex Mono",monospace;font-size:var(--t-2xs);letter-spacing:.1em;
  text-transform:uppercase}
.ok{color:var(--ok)}
.gap{color:var(--warn-t,#D9A227)}
.once{font-family:"IBM Plex Mono",monospace;font-size:var(--t-2xs);letter-spacing:.1em;
  text-transform:uppercase;color:var(--faint);font-weight:400}
.circuit{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:var(--s-5) 0 0;
  font-family:"IBM Plex Mono",monospace;font-size:13px;color:var(--dim)}
/* The ember accent is 3.84:1 as 13px text on this panel. The brief says lift a
   derived variant rather than touch the accent, so the border stays ember and
   the numeral is blended toward bone until it clears AA. */
.circuit b{display:inline-flex;align-items:center;justify-content:center;min-width:30px;height:30px;
  border:1px solid var(--ember,#D9762A);font-weight:600;padding:0 6px;
  color:color-mix(in srgb, var(--ember,#D9762A) 58%, var(--bone))}
.circuit span{color:var(--faint)}
.scale{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,210px),1fr));
  gap:1px;background:var(--rule);border:1px solid var(--rule);border-radius:var(--r);
  overflow:hidden;margin:var(--s-5) 0 0}
.scale div{background:var(--panel);padding:14px 16px}
.scale .n{font-family:"Saira Condensed",sans-serif;font-size:27px;font-weight:700;
  color:var(--bone);line-height:1.1}
.scale .l{font-family:"IBM Plex Mono",monospace;font-size:var(--t-2xs);color:var(--dim);
  letter-spacing:.08em;text-transform:uppercase;margin-top:5px}

/* ---------- the island walkthrough ----------------------------------------
   One block per island, in progression order. The number is the island's own
   label — 1.5 really is called that — so it is set as data rather than as a
   list counter, which could only ever produce 1..9. */
.isles{list-style:none;margin:var(--s-5) 0 0;padding:0;display:grid;gap:1px;
  background:var(--rule);border:1px solid var(--rule);border-radius:var(--r);overflow:hidden}
.isle{background:var(--panel);padding:var(--s-5);display:grid;
  grid-template-columns:56px minmax(0,1fr) minmax(0,190px);gap:var(--s-3) var(--s-5);
  align-items:start}
@media(max-width:820px){.isle{grid-template-columns:44px minmax(0,1fr)}
  .isle-fig{grid-column:2}}
.isle-n{font-family:"Cinzel",Georgia,serif;font-size:26px;font-weight:700;color:var(--brass-t);
  line-height:1;font-variant-numeric:tabular-nums}
.isle-name{font-family:"Cinzel",Georgia,serif;font-size:var(--t-lg);font-weight:600;
  text-transform:uppercase;letter-spacing:.02em;color:var(--bone);margin:0 0 4px}
.isle-boss{font-family:"IBM Plex Mono",monospace;font-size:var(--t-xs);letter-spacing:.08em;
  text-transform:uppercase;color:var(--mut);margin:0 0 var(--s-3)}
.isle-2nd{color:var(--faint)}
.isle-key{display:inline-block;margin-left:8px;padding:1px 7px;border:1px solid var(--rule2);
  border-radius:var(--r);color:var(--brass-t);font-size:var(--t-2xs)}
.isle-what{margin:0 0 var(--s-2);color:var(--txt);font-size:var(--t-base);line-height:1.6}
.isle-tac{margin:0;color:var(--mut);font-size:var(--t-sm);line-height:1.6;
  border-left:2px solid var(--brass);padding-left:var(--s-3)}
.isle-loot{margin:var(--s-3) 0 0;font-family:"IBM Plex Mono",monospace;font-size:var(--t-2xs);
  letter-spacing:.06em;color:var(--faint);line-height:1.7}
.isle-loot em{font-style:normal;color:var(--dim);text-transform:uppercase;margin-right:6px}
.isle-fig{text-align:right;font-family:"IBM Plex Mono",monospace;font-size:var(--t-2xs);
  color:var(--faint);letter-spacing:.06em;line-height:1.6}
.isle-fig b{display:block;font-family:"Saira Condensed",sans-serif;font-size:var(--t-xl);
  font-weight:700;color:var(--bone);letter-spacing:0;line-height:1.1}
.isle-fig em{font-style:normal;font-size:.7em;color:var(--faint)}
.isle-none b{color:var(--warn-t);font-size:var(--t-lg)}
@media(max-width:820px){.isle-fig{text-align:left}}

/* Island 8 is the only ordered procedure on the page, so it is the only thing
   set as numbered steps. */
.steps8{counter-reset:s;list-style:none;margin:var(--s-5) 0 0;padding:0}
.steps8 li{counter-increment:s;position:relative;padding:var(--s-4) 0 var(--s-4) 52px;
  border-bottom:1px solid var(--rule);color:var(--txt);line-height:1.65}
.steps8 li:last-child{border-bottom:0}
.steps8 li::before{content:counter(s,decimal-leading-zero);position:absolute;left:0;top:var(--s-4);
  font-family:"IBM Plex Mono",monospace;font-size:var(--t-sm);font-weight:600;color:var(--brass-t)}
.steps8 b{color:var(--bone);font-weight:600}
</style>'''

page = (head("Plane of Sky",
             "The Plane of Sky measured: 43 boss fights at base difficulty, a median of four "
             "attackers, the ring of eight islands, and the key chain confirmed against the log.",
             rel="../", extra=CSS, og="raids", canon="raids/plane-of-sky")
        + bar("../") + f'''
<main>
<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp;
      <a href="index.html">Raids</a> &nbsp;/&nbsp; Plane of Sky</p>
    <h1 class="display">The Plane<br><em>of Sky.</em></h1>
    <p class="hero-lede"><strong>Nine islands on a one-way teleporter loop, each gated by a key
      the island below it drops.</strong> The whole zone in the order you do it, with what every
      boss cost us to kill. <strong>It is not a raid zone</strong>, whatever else you have read.</p>
    <p class="hero-sig"><span>{FIGHTS["n"]} fights, {FIGHTS["bosses"]} bosses</span>
      <span>median {FIGHTS["attackers_median"]} attackers</span>
      <span>all at base difficulty</span></p>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><div><h2 class="sec">How the zone works</h2></div></div>
    <p class="lede"><strong>You arrive on island 1 and the Key Master is standing there.</strong>
      Buy the first three keys from him. After that every island&rsquo;s boss drops the key to the
      next one, so the order is fixed: <strong>1 &rarr; the spur at 1.5 &rarr; 2 &rarr; 3 &rarr; 4
      &rarr; 5 &rarr; 6 &rarr; 7 &rarr; 8</strong>. Island 1.5 hangs off the landing and its
      teleporter puts you on 2 rather than back on 1, so it costs nothing to take on the way past.
      <strong>Six of the seven predicted key drops landed in our logs</strong>, each from
      exactly the boss named below; the seventh is unchecked because we have never found the
      Thunder Spirit Princess. <span class="tier tM">TIER M</span></p>
    <p class="lede"><strong>Nothing in the Plane of Sky sees through invisibility.</strong> That is
      the opposite of Fear and Hate, and it is the single most useful fact about the zone: you can
      walk past almost everything and kill only what you came for.</p>
    <div class="sky-ring">{ring_svg()}</div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><div><h2 class="sec">Island by island</h2>
      <p class="lede" style="margin:0">In progression order. Figures are from our own combat logs
        at base difficulty. <span class="tier tM">TIER M</span></p></div></div>
    <ol class="isles">
{isle_rows()}
    </ol>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><div><h2 class="sec">Island 8, in full</h2>
      <p class="lede" style="margin:0">Two bosses on one island, and the only part of the zone
        where the order matters. Reported by the site&rsquo;s owner, who has cleared it about ten
        times.</p></div></div>
    <ol class="steps8">
      <li><b>Go invisible before you take the portal up.</b> Nothing here sees invis, so you
        arrive unengaged and choose your own opening.</li>
      <li><b>Walk around to the back of the island</b>, to the teleporter that returns you to the
        landing. The Hand of Veeshan wanders there.</li>
      <li><b>Kill the Hand of Veeshan at the back.</b> It drops the efreeti line.</li>
      <li><b>Walk back to the front and kill the Eye of Veeshan</b> where it stands.</li>
      <li><b>Slow them both.</b> That is the whole fight.</li>
    </ol>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><div><h2 class="sec">What a Sky boss costs</h2>
      <p class="lede" style="margin:0">Measured from our own combat logs on 14 and 15 August 2026.
        <span class="tier tM">TIER M</span></p></div></div>
    <div class="scale">
      <div><p class="n">{fmt(BIGGEST)}</p><p class="l">Dearest boss in Sky</p></div>
      <div><p class="n">{fmt(CT)}</p><p class="l">Cazic-Thule at Refined</p></div>
      <div><p class="n">{RATIO}&times;</p><p class="l">The difference</p></div>
    </div>
    <p class="lede" style="margin-top:var(--s-5)">The hardest thing in Sky dies to whoever happens
      to be standing there.</p>
    <div class="note"><strong>Damage to kill is not hit points.</strong> It counts every
      attacker and sits above a boss&rsquo;s health rather than measuring it. A figure marked
      <em>or more</em> is a fight we joined late, so it is a floor.</div>
    <div class="note danger"><strong>All of it is base difficulty.</strong> D0 is the only tier we
      have played Sky at, so nothing here describes Awakened or above.</div>
    <div class="note"><strong>None of it was one trio.</strong> Every Sky fight in our logs is a
      public pick-up raid of {FIGHTS["attackers_min"]} to {FIGHTS["attackers_max"]} players. The
      site&rsquo;s owner reports the zone can be soloed; our
      thinnest logged fight is {FIGHTS["attackers_min"]}, so that stands unconfirmed.</div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><div><h2 class="sec">Where the efreeti gear comes from</h2>
      <p class="lede" style="margin:0">An audit on 14 August 2026 flagged the source of the efreeti
        line as unresolved between this site and eqlegendstools. Three mobs dropped it in front of
        us. <span class="tier tM">TIER M</span></p></div></div>
    <div class="tw"><table class="dtable">
      <thead><tr><th>Dropped by</th><th>Seen</th></tr></thead>
      <tbody>
{efr_rows}
      </tbody></table></div>
    <p class="lede" style="margin-top:var(--s-5)">All three stand on the back half of the circuit
      &mdash; the spur at 1.5, the windmill tower on 4, and island 8. <strong>This is what we
      watched drop over two nights, not a drop rate</strong>, and it does not rule out sources we
      did not kill.</p>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><div><h2 class="sec">How high it actually is</h2>
      <p class="lede" style="margin:0">Read from the zone&rsquo;s own mesh on 11 August 2026.
        Nobody has published this before, and it is ours rather than anyone&rsquo;s drawing.</p></div></div>
    <div class="sky-elev">{elev_svg()}</div>
    <p class="lede"><strong>{len(ISL)} separate bodies of walkable floor across
      {SKY["zmax"] - SKY["zmin"]:,.0f} units of height</strong>, from
      {SKY["zmin"]:,.0f} to {SKY["zmax"]:,.0f}. Seen from the side, west to east. Each mark is
      sized by how much floor it holds. For comparison, the deepest dungeon we have measured spans
      about 600 units top to bottom.</p>
    <div class="note"><strong>The two axes are not at the same scale.</strong> Height is drawn at
      {ELEV_VE:.2f} of its true size against the horizontal, so <strong>Sky reads about
      {1/ELEV_VE:.1f} times flatter here than it is</strong>. That is normal for a section drawing
      and it is why surveyors print the figure on the drawing rather than in a caption.</div>
    <div class="note danger"><strong>These are not labelled, and that is deliberate.</strong> The
      mesh says where every piece of floor is; it does not say which piece is &ldquo;island 4&rdquo;.
      That lives in the teleporter network, and <strong>one <code>/loc</code> per island &mdash;
      {len(RING)} readings &mdash; would label this chart permanently</strong> and let us draw each
      island properly. Drawing a guess would be worth less than drawing nothing.</div>
    <p class="lede">A body of floor is not always an island: a tower counts separately from the
      ground it stands on, which is why there are {len(ISL)} marks and {len(RING)} places to stand.</p>
  </section>

<section class="band">
  <div class="shell">
    <div class="sechead"><div><h2 class="sec">What we do not know</h2></div></div>
    <ul class="chain">
      <li><span class="i">1</span><span class="b">Anything about Sky above D0</span>
        <span class="k">one logged run</span>
        <span class="nt">All {FIGHTS["n"]} fights are at base difficulty. One session at Awakened
          would say whether the tiers change this zone the way they change a dungeon.</span></li>
      <li><span class="i">2</span><span class="b">The Thunder Spirit Princess</span>
        <span class="k">one kill</span>
        <span class="nt">Island 1&rsquo;s boss, and the only one on the ring that has never
          appeared in a log of ours &mdash; not killed, not seen, not named. Its key is the one
          link in the chain still unconfirmed.</span></li>
      <li><span class="i">3</span><span class="b">Which measured body is which island</span>
        <span class="k">{len(RING)} /loc readings</span></li>
      <li><span class="i">4</span><span class="b">Whether there is a tenth island</span>
        <span class="k">one sighting</span>
        <span class="nt">One account counts ten, listing 1&ndash;8, 1.5 and an Efreeti island.
          The efreeti drops do not settle it &mdash; all three sources are already on the
          ring.</span></li>
      <li><span class="i">5</span><span class="b">Boss hit points at any difficulty</span>
        <span class="k">nobody has these</span>
        <span class="nt">Every published stat block for these bosses traces to a wiki page
          created before the game existed.</span></li>
      <li><span class="i">6</span><span class="b">Which Sky drops are quest turn-ins</span>
        <span class="k">a turn-in list</span>
        <span class="nt">One account lists items said to be safe to sell. We are not republishing
          it: a reader who vendors a quest component on our word has been badly served.</span></li>
    </ul>
    <p class="lede" style="margin-top:var(--s-5)">The measured half of this page comes from
      {LOOT["loot_lines"]} looted items and {FIGHTS["n"]} parsed fights across
      {" and ".join(FIGHTS["dates"])}. The tactics came from players who went and looked, named on
      the <a href="../credits.html">credits page</a>.</p>
  </div>
</section>
</main>
''' + foot("../"))

open('public/raids/plane-of-sky.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"raids/plane-of-sky.html rebuilt: ring of {len(RING)}, {len(ISL)} measured bodies, "
      f"{FIGHTS['n']} fights over {FIGHTS['bosses']} bosses, {len(KEYS)} keys confirmed")
