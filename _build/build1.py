import os, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT,'_build'))
import json
from _partials import head, bar, foot, TOOLS, wordnum
import heroart

# THE HOME PAGE'S ART IS A REAL DUNGEON.
# Najena's walkable floor, read out of the game's own mesh. It is the one piece
# of imagery this site can honestly own: screenshots are Daybreak's, stock
# fantasy art is nobody's, and generated art is exactly what a guildmate meant
# when they called the site AI slop. This is a measurement, like every figure
# on the page, and it carries its source line for the same reason they do.
HERO_ZONE = 'najena'
_hp, _hw, _hh = heroart.paths(HERO_ZONE, box=1000, precision=0)
_hstat = heroart.stats(HERO_ZONE)
# Stagger the draw-in so it reads as a survey rather than a switch being
# thrown. Delays are assigned here rather than by nth-child, which would need
# one CSS rule per path.
hero_art = (f'<div class="hero-art" aria-hidden="true">'
            f'<svg viewBox="0 0 {_hw} {_hh}" preserveAspectRatio="xMidYMid meet">'
            + "".join(f'<path {heroart.SAFE_ATTRS} d="{d}" style="--d:{i * 14}ms"/>'
                      for i, d in enumerate(_hp))
            + '</svg></div>')
hero_src = (f'<p class="hero-src">Najena, drawn from the game&rsquo;s own mesh &mdash; '
            f'<b>{_hstat["paths"]} paths, {_hstat["points"]:,} points</b>, '
            f'{_hstat["layers"]} storeys</p>')

Z = json.load(open('assets/zones-index.json', encoding='utf-8'))
# Counts are read from the mined data, never typed. The Index once published
# "389 items" while the data held 452 and its own counter said so on screen.
IX = json.load(open('assets/index-data.json', encoding='utf-8'))
# From extract.py's own count, not counted again here. Counting the raw rows
# put groups and fragments in the total and printed 451 beside The Index's 441.
NITEMS = IX['counts']['item_pages']
NNAMED = IX['counts']['named_pages']
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

# Home page: colour objects rather than table rows. The contour rings are
# anchored to a different corner per survey so the cards do not read as one
# texture repeated — each looks like a different piece of the same map.
#
# The list is ten long because the site had ten zones, and it was indexed
# directly: the eleventh survey crashed the home page build. It cycles now, so
# the eleventh reuses the first corner rather than stopping the build. Adding a
# zone is meant to need no layout change, and this was the one place it did.
_CORNERS = [("86%","118%"),("14%","112%"),("92%","104%"),("8%","120%"),("78%","110%"),
            ("20%","104%"),("94%","116%"),("10%","106%"),("70%","120%"),("30%","110%")]


def corner(i):
    return _CORNERS[i % len(_CORNERS)]

try:
    COV = json.load(open('assets/coverage.json', encoding='utf-8'))['zones']
except (OSError, ValueError, KeyError):
    COV = {}


def _gate(z):
    lv = z["verify_level"]
    label = {"full":"all three gates cleared","partial":"partial — "+(z.get("verify_gate") or ""),
             "none":"not verified — "+(z.get("verify_gate") or "")}[lv]
    return f'<span class="gate {lv}" title="{label}"></span>'


def _cov(z):
    """What a PLAYER can get from this zone, which is not what the three gates
    measure. Gate 3 asks whether a coordinate lands on drawn floor - a build
    input for our own maps - so Plane of Fear scored zero with both its gods
    parsed at three difficulties. See docs/WHAT-COUNTS.md."""
    c = COV.get(z['slug'])
    if not c:
        return ''
    got = [k for k, f in c['facets'].items() if f['level'] == 'measured']
    tip = '; '.join(f"{k}: {f['detail']}" for k, f in c['facets'].items())
    return (f'<span class="cov" title="{tip}">'
            f'<b>{c["score"]}</b>/{c["max_score"]}'
            + (f' &middot; {len(got)} measured' if got else '') + '</span>')

# THE PLATE CARDS CARRY THEIR OWN ZONE, DRAWN.
#
# Until now every card wore the same ornament: `.contour`, a CSS
# repeating-radial-gradient of concentric rings. It read as contour lines and
# it was not one — a decorative layer inventing a map, on a site that will not
# print a respawn timer it has not read in a source. The prettiest thing on the
# home page was the least true thing on it.
#
# Each card now carries the real walkable floor of its own zone, from the
# game's mesh. Thirteen of them cost 22 KB gzipped, which is less than one
# small image, and every card is a different shape because every dungeon is.
def plate_art(slug):
    d, w, h = heroart.paths(slug, box=100, precision=0, max_paths=60)
    if not d:
        return ''
    return (f'<span class="plate-art" aria-hidden="true">'
            f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet">'
            + "".join(f'<path {heroart.SAFE_ATTRS} d="{p}"/>' for p in d)
            + '</svg></span>')


plates = "\n".join(
  f'''    <a class="plate" href="dungeons/{z['slug']}.html" style="--c:{z['accent']}">
      {plate_art(z['slug'])}
      <span class="lvl"><b>{z['plate']:02d}</b> &middot; {z['levels'].split(' (')[0]}</span>{_gate(z)}
      <span class="num" aria-hidden="true">{z['plate']:02d}</span>
      <h3 class="pt">{z['title']}</h3>
      <span class="meta"><span>ZEM <b>{z['zem']}</b></span><span>Respawn <b>{z['respawn'] or 'not recorded'}</b></span>{_cov(z)}</span>
    </a>''' for i, z in enumerate(Z))

nfull = sum(1 for z in Z if z["verify_level"]=="full")
npart = sum(1 for z in Z if z["verify_level"]=="partial")
nnone = sum(1 for z in Z if z["verify_level"]=="none")

# THE PROMOTED TOOL.
# Sky Ledger goes directly under the hero and the atlas moves down. It is not a
# card in a row of equals: what it does that no other Sky tracker does — spend a
# held turn-in piece once instead of counting it against every test that wants
# it — is a correctness property, and the tracker it replaced was ours.
#
# Both figures are read out of assets/sky-ledger.json, which _build/skyledger.py
# counts from the Ledger's own dataset. The tool's README types "three quests"
# about an item its data wants twice; that is the exact reason nothing here is
# typed beside the data it claims to come from.
SL = json.load(open('assets/sky-ledger.json', encoding='utf-8'))
# The overlay door. A release exists now, so the home page offers the download
# directly rather than routing a reader through the tool page to find out there
# is nothing to download. Falls back to the tool page where no release is
# recorded, so a build without the Ledger repo still produces a working link.
_SL_REL = (SL.get('release') or {}).get('overlay') or {}
SL_OVERLAY_HREF = _SL_REL.get('url') or 'tools/sky-ledger.html'
SL_OVERLAY_LABEL = (f'Download the overlay &middot; {_SL_REL["mb"]} MB &rarr;'
                    if _SL_REL.get('mb') else 'The overlay &rarr;')

SL_APP, SL_DS = SL['app'], SL['dataset']

feature = f'''
<section class="band feat">
  <div class="shell">
    <div class="featwrap">
      <div class="featgrid">
        <div>
          <p class="eyebrow">Plane of Sky &middot; <b>reads your own log</b></p>
          <h2 class="feath">Sky Ledger</h2>
          <p class="featlede">It follows your combat log while you play and says which of the
            {SL_DS['quests']} Plane of Sky class-unlock tests you can hand in <strong>now</strong> &mdash; and what
            the missing pieces drop from. In a browser with nothing to install, or as an
            overlay on the game.</p>
          <p class="featsub"><strong>It knows a turn-in piece can only be spent once.</strong>
            {SL_DS['contested']} of its {SL_DS['items']} turn-in items are wanted by more than one test. Holding one
            does not make several quests ready, and every other tracker &mdash; including the
            one this replaces, which was ours &mdash; counts it against all of them. It also
            refuses to print a drop rate it cannot measure: a dry streak reads as a bound,
            <code>&lt;28% &middot; 0/9</code>, never <code>0%</code>.</p>
          <div class="featdoors">
            <a class="featdoor lead" href="app/{SL_APP['file']}">Run it in your browser &rarr;</a>
            <a class="featdoor" href="{SL_OVERLAY_HREF}">{SL_OVERLAY_LABEL}</a>
            <a class="featdoor" href="tools/sky-ledger.html">What it does &rarr;</a>
          </div>
        </div>
        <ul class="featclaims">
          <li><b>{SL_DS['contested']} of {SL_DS['items']}</b>
            <span class="lab">Turn-in items wanted twice or more</span>
            <span class="why">One piece finishes one test. It pools what you hold and spends
              each unit on the test closest to done.</span></li>
          <li><b>&lt;28% &middot; 0/9</b>
            <span class="lab">How a dry streak prints</span>
            <span class="why">Zero drops in nine kills bounds the rate; it does not measure
              it. <code>0%</code> would tell you to stop farming.</span></li>
        </ul>
      </div>
      <p class="featfoot">No install &middot; nothing uploaded &middot; build {SL_APP['hash']} &middot; {SL_APP['kb']} KB</p>
    </div>
  </div>
</section>
'''

from changelog import ENTRIES, TONE

recent = "\n".join(
  f'''      <li class="ch" style="--c:{TONE[e['kind']]}">
        <span class="k">{e['kind']}</span>
        <span class="t">{e['title']}</span>
        <span class="d">{e['date']}</span>
      </li>''' for e in ENTRIES[:4])

home = head("Accurate, sourced and kept current",
  "EverQuest Legends reference kept honest: progression trackers, a searchable loot index, dungeon surveys and the Plane of Sky island by island. Every claim names its source and its date.", og="home", canon="index") + bar() + f'''
<main>

<section class="hero">
  {hero_art}
  <div class="shell">
    <p class="eyebrow">EverQuest Legends &middot; <b>surveyed, sourced, dated</b></p>
    <h1 class="display">Norrath,<br><em>measured.</em></h1>
    <p class="hero-lede">Most of what this community reads about Legends is classic EverQuest text in
      a Legends-shaped hole. We go in with the log running and write down what actually happened.
      Every figure names its source and the day it was read, and every gap says so out loud.</p>
    <p class="hero-sig"><span>{len(Z)} zones surveyed</span><span>{NITEMS} items indexed</span><span>{NNAMED} named recorded</span><span>{nfull} fully verified</span></p>
  </div>
  {hero_src}
</section>
{feature}
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
        <h3 class="dt">The surveys</h3>
        <p class="dd">Population tables, named rosters with spawn data, loot tied to its drop source,
          and coordinates re-derived from <code>/loc</code> records.</p>
        <span class="dgo">{len(Z)} surveys, {len(MAPS)} maps &rarr;</span>
      </a>

      <a class="door contour" href="tools/index.html" style="--c:var(--instr);--cx:84%;--cy:104%">
        <span class="dq">I am planning a character</span>
        <h3 class="dt">The trackers</h3>
        <p class="dd">Class unlocks, race unlocks and the primary-slot decision you can never take back.
          Progress packs into the page URL, so nothing is stored and nothing is lost.</p>
        <span class="dgo">{wordnum(len(TOOLS))} trackers &rarr;</span>
      </a>

    </div>
    <p class="doornote">Raid encounters live under <a href="raids/index.html">Raids</a> &mdash; one zone
      written up in full, measured in play.</p>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><div><h2 class="sec">The atlas</h2>
      <p class="lede" style="margin:0">Thirteen dungeons, each drawn from the game&rsquo;s own mesh.
        No two are the same shape because no two dungeons are.</p></div>
      <a class="link" href="dungeons/index.html">Every survey &rarr;</a></div>
    <div class="plates">
{plates}
    </div>
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
open('public/index.html','w',encoding='utf-8',newline='\n').write(home)

# ---------------------------------------------------------------- DUNGEONS
drows = "\n".join(
  f'''    <a class="zrow" href="{z['slug']}.html" style="--c:{z['accent']}">
      <span class="pn">{z['plate']:02d}</span>
      <span><span class="zt">{z['title']}</span><span class="zs">{zsub(z)} &middot; /who {z['who']}</span></span>
      <span class="cell zonesub"><em>Respawn</em>{z['respawn'] or 'not recorded'}</span>
      <span class="cell"><em>ZEM</em>{z['zem']} <span style="color:var(--faint)">/ {z['zem_pct']}%</span></span>
      <span class="cell"><em>Verified</em>{ {'full':'full','partial':'partial','none':'not yet'}[z['verify_level']] }</span>
      <span class="bar"></span></a>''' for z in Z)


# The survey cards live here, on the surveys page. The home page links to this
# page rather than reproducing it.  NOT ANY MORE, 16 Aug 2026: it did not
# reproduce it and it did not link it either. The home page never showed a
# single zone — the site's entire subject was invisible from its front door,
# which is most of why a visitor's eye slid off it. The atlas is on both pages
# now, and this is the same card.
dplates = "\n".join(
  f'''      <a class="plate" href="{z['slug']}.html" style="--c:{z['accent']}">
        {plate_art(z['slug'])}
        <span class="lvl"><b>{z['plate']:02d}</b> &middot; {z['levels'].split(' (')[0]}</span>{_gate(z)}
        <span class="num" aria-hidden="true">{z['plate']:02d}</span>
        <h3 class="pt">{z['title']}</h3>
        <span class="meta"><span>ZEM <b>{z['zem']}</b></span><span>Respawn <b>{z['respawn'] or 'not recorded'}</b></span>{_cov(z)}</span>
      </a>''' for i, z in enumerate(Z))

# The open gates, generated rather than written out five times by hand. Sorted
# so unverified zones come before partial ones — the worse state reads first.
# Every gate cleared is a state this page has never been in before, so it needs
# its own copy rather than a sentence about zero partials and zero unverified.
# When something regresses the old wording comes back on its own.
_open = [z for z in Z if z['verify_level'] != 'full']
if _open:
    verdict = (f"By that standard <strong>{nfull} of {len(Z)}</strong> are verified, "
               f"{npart} are partial and {nnone} are not verified at all. Partial surveys are "
               f"complete and useful; they have simply not cleared every gate. Which gate is open "
               f"is recorded per zone rather than averaged into a single number that would "
               f"read better than the truth.")
    asidec, asideh = "var(--warn)", "Open gates"
else:
    verdict = (f"By that standard <strong>all {len(Z)} are verified</strong>, as of 9 August 2026. "
               f"That is a floor, not a finish: it means every survey has been checked against its "
               f"live source and every coordinate lands somewhere a player can stand. It does not "
               f"mean the zones are fully documented. Where a figure is missing or a source is a "
               f"Project 1999 import, the survey says so in place, and those gaps are listed on each "
               f"plate rather than folded into this number.")
    asidec, asideh = "var(--ok)", "The three gates, cleared"

_ORDER = {"none": 0, "partial": 1, "full": 2}
# With gates open, the panel names them. With none open, listing ten cleared
# zones would be ten paragraphs saying the same thing, so it names the three
# gates instead and says what each one actually proves - which is the part a
# reader needs in order to judge the word "verified".
_CLEARED = [
  ("Source read in full", "Every survey's wiki page was fetched whole and its roster re-compared "
   "against the survey, not sampled. It is how Kelynn was found missing from Crushbone."),
  ("History from the API", "Edit history taken from MediaWiki, never the page footer. Footers were "
   "stale on four of the first five zones checked; Befallen's was two months out."),
  ("Coordinates on drawn floor", "All 176 plotted positions land within 120 units of walkable floor "
   "extracted from the game's own mesh files. Six impossible Najena coordinates were caught this "
   "way and withheld."),
]
if _open:
    gaterows = "\n".join(
      f'''      <li class="gaterow" style="--c:{z['accent']}">
        <span class="gn">{z['plate']:02d}</span>
        <span class="gz">{z['title']}</span>
        <span class="gs">{z['verify_gate']}</span>
        <span class="gl">{'unstarted' if z['verify_level']=='none' else 'open'}</span>
      </li>'''
      for z in sorted(_open, key=lambda z: (_ORDER[z['verify_level']], z['plate'])))
else:
    gaterows = "\n".join(
      f'''      <li class="gaterow" style="--c:var(--ok)">
        <span class="gn">{i+1:02d}</span>
        <span class="gz">{title}</span>
        <span class="gs">{what}</span>
        <span class="gl">cleared</span>
      </li>''' for i, (title, what) in enumerate(_CLEARED))


dung = head("Dungeon surveys",
  f"{len(Z)} revamped EverQuest Legends dungeons surveyed from primary sources: population tables, named rosters, loot with drop sources and plotted coordinate maps.",
  rel="../", og="dungeons", canon="dungeons/index") + bar("../") + f'''
<main>

<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp; Dungeons</p>
    <h1 class="display">{wordnum(len(Z))} zones,<br><em>surveyed.</em></h1>
    <p class="hero-lede">Each shipping a deep-reference survey and, where built, a navigation map
      companion. Population tables, named rosters with spawn data, loot tied to its drop source, and
      coordinates re-derived from the wiki&rsquo;s <code>/loc</code> records and checked against the
      floor the game itself draws.</p>
    <p class="hero-sig"><span>{len(Z)} surveys</span><span>{len(MAPS)} maps</span><span>{nfull} fully verified</span><span>{npart} partial</span><span>{nnone} unverified</span></p>
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
            wiki page was fetched in full and its roster re-compared, <em>its edit history was
            fetched</em> &mdash; not merely the footer date &mdash; and <em>every coordinate lands on
            drawn floor</em>, within 120 units of geometry extracted from the game&rsquo;s own mesh
            files.</p></div></div>
        <p class="lede">{verdict}</p>
      </div>
      <aside class="standard contour" style="--c:{asidec};--cx:90%;--cy:110%">
        <h3 class="stdh">{asideh}</h3>
        <ul class="gatelist">
{gaterows}
        </ul>
      </aside>
    </div>
  </div>
</section>


</main>
''' + foot("../")
open('public/dungeons/index.html','w',encoding='utf-8',newline='\n').write(dung)

print("home + dungeons index written")
