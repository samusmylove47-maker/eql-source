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
RING = [
    dict(id="1",   boss="Thunder Spirit Princess", key="Key of Swords",
         note="Where you arrive, and where the Key Master sells the first three keys."),
    dict(id="2",   boss="Protector of Sky", key="Key of Misfortune",
         note="Azaracks. Large aggro radius and a large social radius, so a pull tends to become "
              "the island."),
    dict(id="3",   boss="Gorgalosk", key="Key of Beasts",
         note="Gorgons, gazers and a heart harpie in the tower. Gusts of wind are invisible and "
              "need see-invis to spot."),
    dict(id="4",   boss="Keeper of Souls", key="Avian Key",
         note="Pegasi, and adds that keep coming. The Overseer of Air stands at the windmill "
              "tower and is a separate kill on the same island."),
    dict(id="5",   boss="The Spiroc Lord", key="Key of the Swarm",
         note="Spirocs have a low aggro radius and a high social one, so the outer edge is quiet "
              "and the middle is not. The Spiroc Guardian is here too."),
    dict(id="6",   boss="Bazzt Zzzt", key="Key of Scale",
         note="Bees, and more of them than any source we hold lists &mdash; six named variants "
              "went down here."),
    dict(id="7",   boss="Sister of the Spire", key="Veeshan's Key",
         note="Nothing here aggros except the boss."),
    dict(id="8",   boss="Eye of Veeshan", key="&mdash;",
         note="The Hand of Veeshan wanders this island and is the last of the circuit."),
]
SPUR = dict(id="1.5", boss="Noble Dojorn", key="&mdash;",
            note="Off island 1, and it returns you to island 2. A blade storm guards it.")

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
    rows = []
    for i in [RING[0], SPUR] + RING[1:]:
        seen = KEYS.get(i['key'])
        if seen and seen['boss'] == i['boss']:
            mark = (f'<span class="ok">confirmed &times;{seen["n"]}</span> '
                    f'<span class="tier tM">M</span>')
        elif i['key'] == '&mdash;':
            mark = ''
        else:
            mark = '<span class="gap">not seen</span>'
        cls = ' class="kill"' if i["id"] in CIRCUIT else ''
        rows.append(
            f'''      <li{cls}>
        <span class="i">{i["id"]}</span><span class="b">{i["boss"]}</span>
        <span class="k">{i["key"]}</span>
        <span class="nt">{i["note"]}</span>
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
    <h1 class="display">Sky is not a<br><em>raid zone.</em></h1>
    <p class="hero-lede"><strong>Every reference in this community described a zone that needs a
      full raid, and so did this page until today.</strong> Over two nights we recorded
      {FIGHTS["n"]} fights against {FIGHTS["bosses"]} of its bosses. The median fight had
      {FIGHTS["attackers_median"]} attackers, the thinnest had {FIGHTS["attackers_min"]}, and the
      most expensive boss in the zone cost {fmt(BIGGEST)} damage.</p>
    <p class="hero-sig"><span>{FIGHTS["n"]} fights, {FIGHTS["bosses"]} bosses</span>
      <span>median {FIGHTS["attackers_median"]} attackers</span>
      <span>all at base difficulty</span></p>
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
    <div class="tw"><table class="dtable">
      <thead><tr><th>Boss</th><th>Fights</th><th>Damage to kill</th><th>Fight</th>
        <th>Attackers</th><th>Exp each</th></tr></thead>
      <tbody>
{cost_rows()}
      </tbody></table></div>
    <div class="note"><strong>Damage to kill is not hit points.</strong> It is the damage that had
      to be dealt, which is what you actually plan around, and it sits above the boss&rsquo;s health
      rather than measuring it. Where a row reads <em>or more</em> we joined after the boss was
      engaged and the figure is a floor. Where it reads <em>once</em> we have a single fight and no
      way to tell a cheap boss from a kill we arrived at the end of &mdash; Bzizzzt&rsquo;s only
      record is 614 damage over three seconds, and its siblings take twenty thousand.</div>
    <div class="note danger"><strong>Every one of these fights is at base difficulty.</strong>
      D0 is the only tier we have played Sky at, so nothing on this page describes Awakened or
      above. Difficulty raises how much of a boss&rsquo;s class kit appears, and on this evidence
      we cannot say what that does here.</div>
    <div class="note"><strong>None of these were our trio alone.</strong> Every Sky fight in the
      logs is a public pick-up raid of {FIGHTS["attackers_min"]} to {FIGHTS["attackers_max"]}
      players. The site&rsquo;s owner reports the zone can be soloed
      <span class="tier tc">TIER C</span>; our thinnest logged fight is
      {FIGHTS["attackers_min"]} attackers, so that stands unconfirmed until a one-attacker kill
      appears in a log.</div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><div><h2 class="sec">The ring</h2>
      <p class="lede" style="margin:0">Every teleporter runs one way. Ringed islands are the ones
        the standard circuit kills; a dashed ring is a boss we have never found.</p></div></div>
    <div class="sky-ring">{ring_svg()}</div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><div><h2 class="sec">The key chain, confirmed</h2>
      <p class="lede" style="margin:0">Three keys are bought from the Key Master on island 1.
        After that every boss drops the key to the island above it. The chain was inherited from
        two post-launch accounts and had never been checked against a log.</p></div></div>
    <ul class="chain">
{chain_rows()}
    </ul>
    <p class="lede" style="margin-top:var(--s-5)"><strong>Six of the seven predicted drops
      landed, each from exactly the boss the chain names.</strong> The seventh is unchecked rather
      than wrong: we never found the Thunder Spirit Princess, so the Key of Swords has no
      measurement behind it either way.</p>
    <div class="note"><strong>Nothing in the Plane of Sky sees through invisibility.</strong>
      That is the opposite of Fear and Hate, where see-invis is the main hazard, and it is why the
      circuit can skip most of the zone rather than clear it.</div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><div><h2 class="sec">The circuit, and the bee island</h2>
      <p class="lede" style="margin:0">The islands worth killing on a repeat run, in the order the
        ring makes cheapest.</p></div></div>
    <div class="circuit">{"".join((f"<b>{s}</b>" if k % 2 == 0 else "<span>&rarr;</span>") for k, s in enumerate(sum([[c, ""] for c in CIRCUIT], [])[:-1]))}</div>
    <p class="lede" style="margin-top:var(--s-5)">Bee island first, then up through 7 and 8; the
      loop returns you to 1 for the spur at 1.5; then round again for the Overseer of Air on 4 and
      the Hand of Veeshan on 8. <strong>Two visits to island 8, and they are different kills</strong>
      &mdash; the Eye on the first pass, the Hand on the second.</p>
    <p class="lede"><strong>Island 6 runs six named bees, not one.</strong> No source we hold
      mentions this, and they are not one mob in successive forms as this page said until today:
      the Key of Scale came off Bazzt Zzzt itself, three times.</p>
    <div class="tw"><table class="dtable">
      <thead><tr><th>Bee</th><th>Fights</th><th>Damage to kill</th><th>Seen dropping</th></tr></thead>
      <tbody>
{bee_rows()}
      </tbody></table></div>
    <div class="note"><strong>Do not bring poison to the bees.</strong> They cast Deadly Poison at
      us constantly and we resisted it {POISON_N} times across four of the six variants
      <span class="tier tM">M</span>. That is the largest resist count in the zone by a wide
      margin, and it is the one piece of the bee island that changes what you pack.</div>
    <div class="note"><strong>We do not publish a clear time.</strong> The one figure we have was
      given by someone who said in the same sentence that they had not timed it, and a time is a
      fact about a player rather than about the zone.</div>
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
      and it is why surveyors print the figure on the drawing rather than in a caption. It had been
      missing from this chart since 11 August 2026, which made the proportion an invented one.</div>
    <div class="note danger"><strong>These are not labelled, and that is deliberate.</strong> The
      mesh says exactly where every piece of floor is. It does not say which piece is
      &ldquo;island 4&rdquo; &mdash; that lives in the teleporter network, and no
      <code>/loc</code> reading from Sky exists to anchor it. <strong>One <code>/loc</code> per
      island &mdash; {len(RING)+1} of them, or {len(RING)+2} if the Efreeti island is a separate
      place &mdash; would label this chart permanently.</strong> Drawing a guess would be worth
      less than drawing nothing.</div>
    <p class="lede">A body of floor is not always an island: a tower counts separately from the
      ground it stands on, which is why there are {len(ISL)} marks and {len(RING)+1} places to
      stand.</p>
  </div>
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
        <span class="k">{len(RING)+1} /loc readings</span></li>
      <li><span class="i">4</span><span class="b">Whether there is a tenth island</span>
        <span class="k">one sighting</span>
        <span class="nt">One account counts ten, listing 1&ndash;8, 1.5 and an Efreeti island.
          The efreeti gear does not settle it: we watched it drop on three islands that are
          already on the ring, which is evidence about where the gear comes from and none at all
          about whether a tenth place exists.</span></li>
      <li><span class="i">5</span><span class="b">Boss hit points at any difficulty</span>
        <span class="k">nobody has these</span>
        <span class="nt">Damage to kill bounds them from above, and every published stat block for
          these bosses traces to wiki pages created before the game existed.</span></li>
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
