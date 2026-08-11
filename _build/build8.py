"""raids/plane-of-sky.html — the ring, the key chain, and the measured elevation.

WHY THIS PAGE WAS REBUILT
-------------------------
The first version was one creator's solo route, framed by their trio, health
pool and gear level. That framing is now out: a tactic that works for one trio
at one gear level is not a fact about the zone, and printing it as the page's
spine made the guide about a player rather than about Sky.

What replaced it is the structure, which is true for everyone:

  THE RING. Sky's teleporters form a cycle - 1 to 2 to ... to 8, and 8 back to
  1 - with island 1.5 hanging off it as a shortcut. Once you see that, the
  six-boss circuit stops being a list of instructions to memorise and becomes
  one and a half laps. Drawn, not described.

  THE KEY CHAIN. Three keys bought from the Key Master on island 1, then every
  boss drops the key to the next island. Gated progression, drawn as a chain.

  THE ELEVATION. Read from airplane.s3d by _build/skyislands.py. 2,878 units of
  vertical range across 21 separate bodies of walkable floor. CLAUDE.md has
  carried "Plane of Sky geometry - never surveyed" as an open gap since this
  site began, and this closes the measuring half of it.

WHAT THE ELEVATION CANNOT DO, AND SAYS SO
-----------------------------------------
It cannot tell you which measured body is "island 4". That mapping lives in the
teleporter network, not in the mesh, and no /loc reading from Sky exists to
anchor it. The chart is drawn unlabelled and the page asks for the ten readings
that would label it. Drawing a guess would be worth less than drawing nothing.

NO NAMES, NO TIMES
------------------
Contributors are credited on credits.html, once, with a link to their work.
Individual clear times and trio-specific experience do not appear at all - one
source reported an 8-12 minute circuit and said in the same breath that they had
not timed it.
"""
import os, sys, json, math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

SKY = json.load(open('assets/sky-islands.json', encoding='utf-8'))
ISL = SKY['islands']

# The ring. `key` is what the boss drops; island 1 is where you buy the first
# three. Everything here is structure rather than tactics, and two independent
# post-launch accounts agree on all of it.
RING = [
    dict(id="1",   boss="Thunder Spirit Princess", key="Key of Swords",
         note="Where you arrive, and where the Key Master sells the first three keys."),
    dict(id="2",   boss="Protector of Sky", key="Key of Misfortune",
         note="Azaracks. Large aggro radius and a large social radius, so a pull tends to become "
              "the island."),
    dict(id="3",   boss="The Gorgalosk", key="Key of Beasts",
         note="Gorgons, gazers and a heart harpie in the tower. Gusts of wind are invisible and "
              "need see-invis to spot."),
    dict(id="4",   boss="Keeper of Souls", key="Avian Key",
         note="Pegasi, and adds that keep coming. The Overseer of Air stands at the windmill "
              "tower and is one of the six on the circuit."),
    dict(id="5",   boss="The Spiroc Lord", key="Key of the Swarm",
         note="Spirocs have a low aggro radius and a high social one, so the outer edge is quiet "
              "and the middle is not."),
    dict(id="6",   boss="Bazzt Zzzt", key="Key of Scale",
         note="Three bees. The middle one is the boss and dies into three successive forms; the "
              "last of them drops the key."),
    dict(id="7",   boss="Sister of the Spire", key="Veeshan's Key",
         note="Nothing here aggros except the boss."),
    dict(id="8",   boss="Eye of Veeshan", key="&mdash;",
         note="The Hand of Veeshan wanders this island and is the last of the six."),
]
SPUR = dict(id="1.5", boss="Noble Dojorn", key="&mdash;",
            note="Off island 1, and it returns you to island 2. A blade storm guards it.")

CIRCUIT = ["6", "7", "8", "1", "1.5", "4", "8"]     # the six kills, in order taken

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
    # nodes
    for isl in RING + [SPUR]:
        x, y = pts[isl["id"]]
        big = isl["id"] != "1.5"
        kill = isl["id"] in CIRCUIT
        out.append(f'<g class="node{" kill" if kill else ""}" data-i="{isl["id"]}">')
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
    zs = [i["z"][1] for i in ISL]
    x0, x1 = min(xs), max(xs)
    z0, z1 = SKY["zmin"], SKY["zmax"]
    sx = lambda v: pad + (v - x0) / (x1 - x0) * (W - pad * 2)
    sz = lambda v: H - pad - (v - z0) / (z1 - z0) * (H - pad * 2)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Side elevation of the Plane of Sky, '
           f'{len(ISL)} bodies of walkable floor across {z1 - z0:.0f} units of height">']
    # height gridlines every 500 units
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
    out.append('</svg>')
    return "".join(out)


CSS = '''<style>
.sky-ring{max-width:620px;margin:0 auto}
.sky-ring svg,.sky-elev svg{display:block;width:100%;height:auto;overflow:visible}
.edge{fill:none;stroke:var(--rule2);stroke-width:1.6;color:var(--rule2)}
.edge.spur{stroke-dasharray:5 4}
.node circle{fill:var(--panel);stroke:var(--rule2);stroke-width:1.6}
.node.kill circle{stroke:var(--ember,#D9762A);stroke-width:2.4;
  fill:color-mix(in srgb, var(--ember,#D9762A) 14%, var(--panel))}
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
.chain li.kill{background:color-mix(in srgb, var(--ember,#D9762A) 7%, var(--panel))}
@media(max-width:620px){.chain li{grid-template-columns:38px minmax(0,1fr)}.chain .k{text-align:left;grid-column:2}}
.circuit{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:var(--s-5) 0 0;
  font-family:"IBM Plex Mono",monospace;font-size:13px;color:var(--dim)}
/* The ember accent is 3.84:1 as 13px text on this panel. The brief says lift a
   derived variant rather than touch the accent, so the border stays ember and
   the numeral is blended toward bone until it clears AA. */
.circuit b{display:inline-flex;align-items:center;justify-content:center;min-width:30px;height:30px;
  border:1px solid var(--ember,#D9762A);font-weight:600;padding:0 6px;
  color:color-mix(in srgb, var(--ember,#D9762A) 58%, var(--bone))}
.circuit span{color:var(--faint)}
</style>'''

chain_rows = "\n".join(
    f'''      <li{' class="kill"' if i["id"] in CIRCUIT else ''}>
        <span class="i">{i["id"]}</span><span class="b">{i["boss"]}</span>
        <span class="k">{i["key"]}</span>
        <span class="nt">{i["note"]}</span></li>'''
    for i in [RING[0], SPUR] + RING[1:])

circuit_html = "".join(
    (f'<b>{s}</b>' if k % 2 == 0 else '<span>&rarr;</span>')
    for k, s in enumerate(sum([[c, ""] for c in CIRCUIT], [])[:-1]))

page = (head("Plane of Sky",
             "The Plane of Sky as a ring: eight islands on a teleporter loop, the key chain that "
             "gates them, the six-boss circuit, and the first measured elevation of the zone.",
             rel="../", extra=CSS, og="raids", canon="raids/plane-of-sky")
        + bar("../") + f'''
<main>
<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp;
      <a href="index.html">Raids</a> &nbsp;/&nbsp; Plane of Sky</p>
    <h1 class="display">Sky is a ring,<br><em>not a ladder.</em></h1>
    <p class="hero-lede"><strong>Eight islands on a one-way teleporter loop, with a ninth hanging off it &mdash; and one more nobody has placed.</strong>
      Island 8 returns you to island 1, which is why the six-boss circuit everyone runs is not a
      list of instructions &mdash; it is one and a half laps.</p>
    <p class="hero-sig"><span>{len(RING)} on the loop, {len(RING)+1} you can stand on</span><span>3 keys bought, 6 dropped</span>
      <span>{SKY["zmax"] - SKY["zmin"]:,.0f} units of height</span></p>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><div><h2 class="sec">The ring</h2>
      <p class="lede" style="margin:0">Every teleporter runs one way. Ringed islands are the six
        the standard circuit kills.</p></div></div>
    <div class="sky-ring">{ring_svg()}</div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><div><h2 class="sec">The key chain</h2>
      <p class="lede" style="margin:0">Three keys are bought from the Key Master on island 1.
        After that every boss drops the key to the island above it, so the order is fixed even
        where the tactics are not.</p></div></div>
    <ul class="chain">
{chain_rows}
    </ul>
    <div class="note"><strong>Nothing in the Plane of Sky sees through invisibility.</strong>
      That is the opposite of Fear and Hate, where see-invis is the main hazard, and it is why the
      circuit can skip most of the zone rather than clear it.</div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><div><h2 class="sec">The six-boss circuit</h2>
      <p class="lede" style="margin:0">The islands worth killing on a repeat run, in the order the
        ring makes cheapest.</p></div></div>
    <div class="circuit">{circuit_html}</div>
    <p class="lede" style="margin-top:var(--s-5)">Bee island first, because the bee is the best
      thing to take with you; then up through 7 and 8; then the loop returns you to 1 for the spur
      at 1.5; then round again for the Overseer of Air on 4 and the Hand of Veeshan on 8.
      <strong>Two visits to island 8, and they are different kills</strong> &mdash; the Eye on the
      first pass, the Hand on the second.</p>
    <div class="note"><strong>We do not publish a clear time.</strong> The one figure we have was
      given by someone who said in the same sentence that they had not timed it, and a time is a
      fact about a player rather than about the zone.</div>
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
    <div class="note danger"><strong>These are not labelled, and that is deliberate.</strong> The
      mesh says exactly where every piece of floor is. It does not say which piece is
      &ldquo;island 4&rdquo; &mdash; that lives in the teleporter network, and no
      <code>/loc</code> reading from Sky exists to anchor it. <strong>One <code>/loc</code> per island &mdash; {len(RING)+1} of them, or
      {len(RING)+2} if the Efreeti island is a separate place &mdash; would label this chart
      permanently.</strong> Drawing a guess would
      be worth less than drawing nothing.</div>
    <p class="lede">A body of floor is not always an island: a tower counts separately from the ground
      it stands on, which is why there are {len(ISL)} marks and {len(RING)+1} places to stand.</p>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><div><h2 class="sec">What we do not know</h2></div></div>
    <ul class="chain">
      <li><span class="i">1</span><span class="b">Which measured body is which island</span>
        <span class="k">10 /loc readings</span></li>
      <li><span class="i">2</span><span class="b">What the tenth island is</span>
        <span class="k">one sighting</span>
        <span class="nt">One account counts ten, listing 1&ndash;8, 1.5 and an Efreeti island. We
          can place the Overseer of Air at the windmill tower on 4, but whether the Efreeti island
          is a separate place is unresolved.</span></li>
      <li><span class="i">3</span><span class="b">Boss hit points at any difficulty</span>
        <span class="k">a raid log</span>
        <span class="nt">Every published stat block for these bosses traces to wiki pages created
          before the game existed.</span></li>
      <li><span class="i">4</span><span class="b">Which Sky drops are quest turn-ins</span>
        <span class="k">a turn-in list</span>
        <span class="nt">One account lists items said to be safe to sell. We are not republishing
          it: a reader who vendors a quest component on our word has been badly served.</span></li>
    </ul>
    <p class="lede" style="margin-top:var(--s-5)">Everything tactical here came from players who
      went and looked, and they are named on the <a href="../credits.html">credits page</a> with
      links to their own work.</p>
  </div>
</section>
</main>
''' + foot("../"))

open('public/raids/plane-of-sky.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"raids/plane-of-sky.html rebuilt: ring of {len(RING)}, {len(ISL)} measured bodies, "
      f"{SKY['zmax'] - SKY['zmin']:,.0f} units of height")
