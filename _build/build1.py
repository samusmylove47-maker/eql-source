import os, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT,'_build'))
import json
from _partials import head, bar, foot

Z = json.load(open('assets/zones-index.json', encoding='utf-8'))
# Counts are read from the mined data, never typed. The Index once published
# "389 items" while the data held 452 and its own counter said so on screen.
IX = json.load(open('assets/index-data.json', encoding='utf-8'))
NITEMS, NNAMED = len(IX['items']), len(IX['named'])
MAPS = {"najena","splitpaw","lowerguk","nagafenslair","mistmoore"}
BYS = {z['slug']: z for z in Z}

def zsub(z):
    return f"{z['levels']}"


# ---------------------------------------------------------------- HOME
zrows = "\n".join(
  f'''    <a class="zrow" href="dungeons/{z['slug']}.html" style="--c:{z['accent']}">
      <span class="pn">{z['plate']:02d}</span>
      <span><span class="zt">{z['title']}</span><span class="zs">{zsub(z)}</span></span>
      <span class="cell zonesub"><em>Respawn</em>{z['respawn'] or 'not recorded'}</span>
      <span class="cell"><em>ZEM</em>{z['zem']} <span style="color:var(--faint)">/ {z['zem_pct']}%</span></span>
      <span class="cell"><em>Map</em>{'yes' if z['slug'] in MAPS else '—'}</span>
      <span class="bar"></span></a>''' for z in Z)

# Home page: ten colour objects rather than ten table rows. The contour rings
# are anchored to a different corner per plate so the ten cards do not read as
# one texture repeated — each looks like a different piece of the same map.
_CORNERS = [("86%","118%"),("14%","112%"),("92%","104%"),("8%","120%"),("78%","110%"),
            ("20%","104%"),("94%","116%"),("10%","106%"),("70%","120%"),("30%","110%")]

def _gate(z):
    lv = z["verify_level"]
    label = {"full":"all three gates cleared","partial":"partial — "+(z.get("verify_gate") or ""),
             "none":"not verified — "+(z.get("verify_gate") or "")}[lv]
    return f'<span class="gate {lv}" title="{label}"></span>'

plates = "\n".join(
  f'''    <a class="plate contour" href="dungeons/{z['slug']}.html"
       style="--c:{z['accent']};--cx:{_CORNERS[i][0]};--cy:{_CORNERS[i][1]}">
      <span class="lvl">{z['levels'].split(' (')[0]}</span>{_gate(z)}
      <span class="num">{z['plate']:02d}</span>
      <h3 class="pt">{z['title']}</h3>
      <span class="meta"><span>ZEM <b>{z['zem']}</b></span><span>Respawn <b>{z['respawn'] or 'not recorded'}</b></span>{'<span>Map <b>yes</b></span>' if z['slug'] in MAPS else ''}</span>
    </a>''' for i, z in enumerate(Z))

nfull = sum(1 for z in Z if z["verify_level"]=="full")
npart = sum(1 for z in Z if z["verify_level"]=="partial")
nnone = sum(1 for z in Z if z["verify_level"]=="none")

from changelog import ENTRIES, TONE

recent = "\n".join(
  f'''      <li class="ch" style="--c:{TONE[e['kind']]}">
        <span class="k">{e['kind']}</span>
        <span class="t">{e['title']}</span>
        <span class="d">{e['date']}</span>
      </li>''' for e in ENTRIES[:4])

home = head("Accurate, sourced and kept current",
  "EverQuest Legends reference kept honest: progression trackers, a searchable loot index, 3D raid encounter guides and dungeon survey plates. Every claim names its source and its date.") + bar() + f'''
<main>

<section class="hero">
  <div class="shell">
    <p class="eyebrow">EverQuest Legends &middot; <b>surveyed, sourced, dated</b></p>
    <h1 class="display">The reference<br>that shows<br><em>its working.</em></h1>
    <p class="hero-lede">Legends moves every week, and most of what the community reads about it is
      classic EverQuest text in a Legends-shaped hole. Every figure here names the page it came from
      and the day it was read. Every gap says so out loud.</p>
    <p class="hero-sig"><span>{len(Z)} plates surveyed</span><span>{NITEMS} items indexed</span><span>{NNAMED} named recorded</span><span>{nfull} fully verified</span></p>
  </div>
</section>

<section class="band doors">
  <div class="shell">
    <div class="sechead"><div><h2 class="sec">Start here</h2>
      <p class="lede" style="margin:0">Three ways in, depending on what you came for.</p></div></div>
    <div class="doorgrid">

      <a class="door contour" href="tools/index-search.html" style="--c:var(--bone);--cx:88%;--cy:116%">
        <span class="dq">I need to find something</span>
        <h3 class="dt">The Index</h3>
        <p class="dd">Every item and named mob across the surveyed dungeons, searchable in one place.
          Ask where a thing drops, filter by class and slot, or find the named you have not met.</p>
        <span class="dgo">Search {NITEMS} items &rarr;</span>
      </a>

      <a class="door contour" href="dungeons/index.html" style="--c:var(--z01);--cx:12%;--cy:110%">
        <span class="dq">I am going into a zone</span>
        <h3 class="dt">The survey plates</h3>
        <p class="dd">Population tables, named rosters with spawn data, loot tied to its drop source,
          and coordinates re-derived from <code>/loc</code> records. Navigation maps where they exist.</p>
        <span class="dgo">{len(Z)} plates, {len(MAPS)} maps &rarr;</span>
      </a>

      <a class="door contour" href="tools/index.html" style="--c:var(--instr);--cx:84%;--cy:104%">
        <span class="dq">I am planning a character</span>
        <h3 class="dt">The trackers</h3>
        <p class="dd">Class unlocks, race unlocks and the primary-slot decision you can never take back.
          Progress packs into the page URL, so nothing is stored and nothing is lost.</p>
        <span class="dgo">Three trackers &rarr;</span>
      </a>

    </div>
    <p class="doornote">Raid encounters live under <a href="raids/index.html">Raids</a> &mdash; boss fights
      rendered in three dimensions, because a paragraph about where to stand has never been as clear as
      being shown.</p>
  </div>
</section>

<section class="band ledger">
  <div class="shell">
    <div class="split">
      <div>
        <div class="sechead"><div><h2 class="sec">What changed</h2>
          <p class="lede" style="margin:0">Typed by what it was, so a correction never reads as new
            content. Every entry is public, including the ones that make us look worse.</p></div></div>
        <ul class="chlist">
{recent}
        </ul>
        <p style="margin-top:var(--s-5)"><a class="link" href="sources.html#changelog"
          style="margin:0">The full change log &rarr;</a></p>
      </div>

      <aside class="standard contour" style="--c:var(--instr);--cx:92%;--cy:112%">
        <h3 class="stdh">Why you can check us</h3>
        <p class="stdp">Every claim carries the weight of its source. Tiers 1 and 2 print plain;
          anything weaker carries its badge wherever it appears
          &mdash; <span class="tier t3">T3</span> <span class="tier t4">T4</span> <span class="tier t5">T5</span></p>
        <ol class="stdscale">
          <li style="--tc:#5FA37E"><b>Developer statements</b><span>Patch notes and direct answers</span></li>
          <li style="--tc:#7FB2C7"><b>Structured wiki data</b><span>Infoboxes, tables, coordinate records</span></li>
          <li style="--tc:#D9A227"><b>Named community guides</b><span>Attributed, maintained, one reading</span></li>
          <li style="--tc:#D9762A"><b>Aggregators</b><span>Mined snapshots, stale after a patch</span></li>
          <li style="--tc:#D46C64"><b>Inherited classic prose</b><span>Project 1999 text. Quoted, marked</span></li>
        </ol>
        <p class="stdfoot"><a class="link" href="sources.html" style="margin:0">The full standard, and
          every open gap &rarr;</a></p>
      </aside>
    </div>
  </div>
</section>

</main>
''' + foot()
open('index.html','w',encoding='utf-8',newline='\n').write(home)

# ---------------------------------------------------------------- DUNGEONS
drows = "\n".join(
  f'''    <a class="zrow" href="{z['slug']}.html" style="--c:{z['accent']}">
      <span class="pn">{z['plate']:02d}</span>
      <span><span class="zt">{z['title']}</span><span class="zs">{zsub(z)} &middot; /who {z['who']}</span></span>
      <span class="cell zonesub"><em>Respawn</em>{z['respawn'] or 'not recorded'}</span>
      <span class="cell"><em>ZEM</em>{z['zem']} <span style="color:var(--faint)">/ {z['zem_pct']}%</span></span>
      <span class="cell"><em>Verified</em>{ {'full':'full','partial':'partial','none':'not yet'}[z['verify_level']] }</span>
      <span class="bar"></span></a>''' for z in Z)

mapcards = "\n".join(
  f'''      <a class="card" href="{s}-map.html" style="--c:{[z for z in Z if z['slug']==s][0]['accent']}">
        <div class="kicker">Navigation map</div>
        <h3 class="t">{[z for z in Z if z['slug']==s][0]['title']}</h3>
        <p class="d">Field document. Plotted routes, numbered camps and the pulls that matter, kept under 1,300 words
          so it stays usable on a second monitor.</p>
        <div class="foot"><span>Companion</span><span class="go">Open &rarr;</span></div></a>''' for s in
  [z['slug'] for z in Z if z['slug'] in MAPS])

# The plate cards live here, on the plates page. The home page links to this
# page rather than reproducing it.
dplates = "\n".join(
  f'''      <a class="plate contour" href="{z['slug']}.html"
         style="--c:{z['accent']};--cx:{_CORNERS[i][0]};--cy:{_CORNERS[i][1]}">
        <span class="lvl">{z['levels'].split(' (')[0]}</span>{_gate(z)}
        <span class="num">{z['plate']:02d}</span>
        <h3 class="pt">{z['title']}</h3>
        <span class="meta"><span>ZEM <b>{z['zem']}</b></span><span>Respawn <b>{z['respawn'] or 'not recorded'}</b></span>{'<span>Map <b>yes</b></span>' if z['slug'] in MAPS else ''}</span>
      </a>''' for i, z in enumerate(Z))

# The open gates, generated rather than written out five times by hand. Sorted
# so unverified zones come before partial ones — the worse state reads first.
_ORDER = {"none": 0, "partial": 1, "full": 2}
gaterows = "\n".join(
  f'''      <li class="gaterow" style="--c:{z['accent']}">
        <span class="gn">{z['plate']:02d}</span>
        <span class="gz">{z['title']}</span>
        <span class="gs">{z['verify_gate']}</span>
        <span class="gl">{'unstarted' if z['verify_level']=='none' else 'open'}</span>
      </li>'''
  for z in sorted((z for z in Z if z['verify_level'] != 'full'),
                  key=lambda z: (_ORDER[z['verify_level']], z['plate'])))

mapcards = "\n".join(
  f'''      <a class="door contour" href="{s}-map.html"
         style="--c:{BYS[s]['accent']};--cx:{_CORNERS[i][0]};--cy:{_CORNERS[i][1]}">
        <span class="dq">Navigation map</span>
        <h3 class="dt">{BYS[s]['title']}</h3>
        <p class="dd">The companion you keep open while you are in the zone. Plotted routes, numbered
          camps and the pulls that matter, kept short enough to stay usable on a second monitor.</p>
        <span class="dgo">Open the map &rarr;</span>
      </a>''' for i, s in enumerate(sorted(MAPS)))

dung = head("Dungeon survey plates",
  "Ten revamped EverQuest Legends dungeons surveyed from primary sources: population tables, named rosters, loot with drop sources and plotted coordinate maps.",
  rel="../") + bar("../") + f'''
<main>

<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp; Dungeons</p>
    <h1 class="display">Ten zones,<br><em>surveyed.</em></h1>
    <p class="hero-lede">Each shipping a deep-reference plate and, where built, a navigation map
      companion. Population tables, named rosters with spawn data, loot tied to its drop source, and
      coordinates re-derived from the wiki&rsquo;s <code>/loc</code> records and collision-checked
      against the room list.</p>
    <p class="hero-sig"><span>{len(Z)} plates</span><span>{len(MAPS)} maps</span><span>{nfull} fully verified</span><span>{npart} partial</span><span>{nnone} unverified</span></p>
  </div>
</section>

<section class="band" style="border-top:0;padding-top:0">
  <div class="shell">
    <div class="plates">
{dplates}
    </div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="split">
      <div>
        <div class="sechead"><div><h2 class="sec">What verified means</h2>
          <p class="lede" style="margin:0">A zone counts as verified only when all three gates pass: its
            wiki page was fetched in full, <em>its edit history was fetched</em> &mdash; not merely the
            footer date &mdash; and its coordinates were re-derived and collision-checked against the
            room list.</p></div></div>
        <p class="lede">By that standard <strong>{nfull} of {len(Z)}</strong> are verified,
          {npart} are partial and {nnone} are not verified at all. Partial plates are complete and
          useful; they have simply not cleared every gate. Which gate is open is recorded per zone
          rather than averaged into a single number that would flatter us.</p>
      </div>
      <aside class="standard contour" style="--c:var(--warn);--cx:90%;--cy:110%">
        <h3 class="stdh">Open gates</h3>
        <ul class="gatelist">
{gaterows}
        </ul>
      </aside>
    </div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><div><h2 class="sec">Navigation maps</h2>
      <p class="lede" style="margin:0">Five zones have one. Crushbone, Befallen, Blackburrow, The Hole
        and The Warrens do not yet &mdash; Blackburrow is next, because its explicit three-floor
        structure makes it the strongest candidate for a treatment other than a flat plan.</p></div></div>
    <div class="doorgrid">
{mapcards}
    </div>
  </div>
</section>

</main>
''' + foot("../")
open('dungeons/index.html','w',encoding='utf-8',newline='\n').write(dung)

print("home + dungeons index written")
