import os, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT,'_build'))
import json
from _partials import head, bar, foot, TOOLS, wordnum

# The home page's door named this tool by hand while the nav and the footer
# read it from the registry, so a rename moved two of the three. It reads from
# the registry now. The doors for 'The surveys' and 'The trackers' name
# sections rather than tools and are deliberately left alone.
NAMES = {t['slug']: t['name'] for t in TOOLS}
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
# The five navigation maps were withdrawn on 17 Aug 2026 - every survey now
# carries a floor plan drawn from the game's own mesh, so a second hand-made
# map of the same zone was a worse copy of something already on the page.
# What a zone HAS is a plan, and that is computed from the geometry rather
# than listed here: a hand-kept set is exactly how "5 maps" outlived the maps.
try:
    PLANS = set(json.load(open('assets/zone-geometry.json', encoding='utf-8')))
except (OSError, ValueError):
    PLANS = set()
BYS = {z['slug']: z for z in Z}

def zsub(z):
    return f"{z['levels']}"


# ---------------------------------------------------------------- HOME
zrows = "\n".join(
  f'''    <a class="zrow" href="dungeons/{z['slug']}.html" style="--c:{z['accent']}">
      <span class="pn">{z['plate']:02d}</span>
      <span><span class="zt">{z['title']}</span><span class="zs">{zsub(z)}</span></span>
      <span class="cell zonesub"><em>Respawn</em>{z['respawn'] or 'not recorded'}</span>
      <span class="cell" title="Zone experience modifier: how fast the zone pays against a baseline of 75"><em>ZEM</em>{z['zem']} <span style="color:var(--faint)">/ {z['zem_pct']}%</span></span>
      <span class="cell"><em>Plan</em>{'yes' if z['slug'] in PLANS else '—'}</span>
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
# EQLS AURAS: ONE SOURCE FOR THE COPY, AND IT IS NOT THIS FILE.
# The band's text used to be written here, so this page and /auras.html would
# have been two copies of a third party's words drifting apart. It lives in
# assets/auras.json now. Shara has creative control of that product and her
# copy reaches us through the owner; no build session authors it.
AURAS = json.load(open('assets/auras.json', encoding='utf-8'))

SL = json.load(open('assets/sky-ledger.json', encoding='utf-8'))

# The planner's vendored snapshot, read BY FIELD PATH exactly as build29.py
# reads it. Same reason: the snapshot carried counts.purge.shipped under a
# catalogue label for as long as the two happened to be equal, and a figure that
# does not name its field gets read as the wrong quantity eventually.
UP = json.load(open('assets/50-upgrades.json', encoding='utf-8'))


def upfig(path):
    """One figure from the planner's snapshot, named by its upstream path."""
    try:
        return UP['figures'][path]
    except KeyError:
        raise SystemExit(
            f"assets/50-upgrades.json has no figure at {path!r}. Run "
            f"`node scripts/refresh-upgrades.mjs <YYYY-MM-DD>`, or fix the path.")
# The overlay door. A release exists now, so the home page offers the download
# directly rather than routing a reader through the tool page to find out there
# is nothing to download. Falls back to the tool page where no release is
# recorded, so a build without the Ledger repo still produces a working link.
_SL_REL = (SL.get('release') or {}).get('overlay') or {}
SL_OVERLAY_HREF = _SL_REL.get('url') or 'tools/sky-ledger.html'
SL_OVERLAY_LABEL = (f'Download the overlay &middot; {_SL_REL["mb"]} MB &rarr;'
                    if _SL_REL.get('mb') else 'The overlay &rarr;')

SL_APP, SL_DS = SL['app'], SL['dataset']
# The trailer and its poster, hashed by _build/media.py so a changed capture is
# a different cache key. Absent on a machine that has never run it, so the band
# degrades to no video rather than a broken element.
try:
    MEDIA = json.load(open('assets/media.json', encoding='utf-8'))
except (OSError, ValueError):
    MEDIA = {}

# 50 UPGRADES — first of the four bands, because it is the only one of them a
# stranger can use today. Sky Ledger ships too, but the planner is the link
# being posted; EQLS Auras is a teaser for a build that does not exist yet, and
# a teaser must not outrank a shipped product.
#
# THAT LAST RULE PLACED THE LOCKOUT BAND ON 26 AUG 2026 RATHER THAN BEING
# OVERRIDDEN BY IT. The tracker ships and Auras still does not, so the tracker
# goes above it: third, ahead of the teaser. The order is 50 Upgrades, Sky
# Ledger, Lockouts, Auras.
#
# Auras moving from third to fourth is the visible consequence, and it was put
# to the owner rather than decided here, because they had ruled on 17 Aug that
# the Auras band was not to move. They chose to apply the rule. Recorded because
# the alternative reading — that an exception was made — is the one a future
# session would otherwise draw from the diff.
#
# WHERE EACH FIGURE COMES FROM, BECAUSE THEY COME FROM TWO PLACES.
#
# Catalogue counts are interpolated from assets/50-upgrades.json by field path
# through upfig(), so they cannot drift from the planner's own accounting and
# cannot be read as the wrong quantity.
#
# The product claims — a trio, twenty-three slots, +0 to +10 — are NOT in that
# snapshot, because meta.json describes the catalogue rather than the interface.
# They are read off the planner's own landing page, 18 Aug 2026, which states:
# "Three classes at once, twenty-three slots including the two Any Slots, and
# every item upgradeable from +0 to +10". Typed here and sourced there, which is
# the rule when a claim has a source but no field.
#
# "Including the two Any Slots" is also the answer to a question this site
# carried open for a day: the snapshot's slots.worn.length is 18, which is slot
# TYPES in the data, while 23 is positions in the interface. Both are right and
# they count different things.
#
# NO HONEST-FRAMING FIGURES HERE, DELIBERATELY. The share of the catalogue with
# no source standing belongs on the tool page, where the full accounting sits
# one click away. A band that leads with its own caveat does not get clicked,
# and the caveat is not hidden — it is the first thing on the page this links to.
upgrades = f'''
<section class="band feat">
  <div class="shell">
    <div class="featwrap">
      <div class="featgrid">
        <div>
          <p class="eyebrow">Live now &middot; <b>no account, no server</b></p>
          <h2 class="feath">50 Upgrades</h2>
          <p class="featlede">Pick a trio and a race, fill twenty-three slots, and compare what
            each candidate does to the character rather than to the item beside it. Every item
            upgrades from +0 to +10, and the stat sheet recomputes as you touch it.</p>
          <p class="featsub">It holds {upfig('counts.items'):,} catalogue items, {upfig('counts.withStats'):,} of them
            carrying stat values. Eligibility is the union of your three classes, so a paladin
            in the mix opens plate for everyone, and points past a cap score nothing.</p>
          <p class="featsub">Your sets live in this browser and travel as a link. Every item
            window names where its numbers came from, and the full accounting of what is
            sourced and what is not is one click away.</p>
          <div class="featdoors">
            <a class="featdoor lead" href="{UP['url']}">Open the planner &rarr;</a>
            <a class="featdoor" href="tools/50-upgrades.html">What it does &rarr;</a>
          </div>
        </div>
      </div>
      <p class="featfoot">Built and hosted in its own repository &middot; snapshot read {UP['read']}</p>
    </div>
  </div>
</section>
'''

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
        <figure class="feattrailer">
          <video data-src="assets/media/{MEDIA['sky-ledger-trailer']['file']}"
                 data-poster="assets/media/{MEDIA['sky-ledger-poster']['file']}"
                 width="1600" height="900" muted loop playsinline
                 preload="none" id="sltrailer"
                 aria-label="The Sky Ledger overlay running over the game: quests marked ready,
                             the panel narrowed to its compact width, and the transparency
                             slider dimming it against the scenery."></video>
          <button class="vpause" type="button" id="slpause" aria-controls="sltrailer">Pause</button>
          <figcaption><span>The overlay in play &middot; 18s, silent</span>
            <a href="https://youtu.be/hxq2qY1FXtg">Full tutorial on YouTube, 1:15 &rarr;</a></figcaption>
        </figure>
      </div>
      <ul class="featclaimrow">
        <li><b>{SL_DS['contested']} of {SL_DS['items']}</b>
          <span class="lab">Turn-in items wanted twice or more</span>
          <span class="why">One piece finishes one test. It pools what you hold and spends
            each unit on the test closest to done.</span></li>
        <li><b>&lt;28% &middot; 0/9</b>
          <span class="lab">How a dry streak prints</span>
          <span class="why">Zero drops in nine kills bounds the rate; it does not measure
            it. <code>0%</code> would tell you to stop farming.</span></li>
      </ul>
      <p class="featfoot">No install &middot; nothing uploaded &middot; build {SL_APP['hash']} &middot; {SL_APP['kb']} KB</p>
      <script>
      /* NOTHING IS FETCHED UNTIL THIS BAND IS ACTUALLY APPROACHED.
         The trailer used to carry `autoplay`, which overrides preload and pulls
         the whole file during first paint. Both trailers and their posters came
         to 2.19 MB, roughly 80% of the page's load time, spent before a stranger
         had seen anything - and this band is below the fold, so most of that was
         for a picture nobody had scrolled to.
         The src and the poster are both held in data- attributes and attached on
         intersection. That costs the no-script reader the motion, which the
         `autoplay` attribute used to give them; it is the deliberate trade, and
         the still is still described by aria-label.
         Reduced-motion and narrow screens load the poster and NOT the video, so
         a tap is what spends the megabyte. This only ever takes motion away. */
      (function(){{
        var v=document.getElementById('sltrailer'), b=document.getElementById('slpause');
        if(!v||!b) return;
        var quiet=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        var small=window.matchMedia&&window.matchMedia('(max-width: 700px)').matches;
        function sync(){{ b.textContent=v.paused?'Play':'Pause'; }}
        function attach(motion){{
          if(!v.hasAttribute('poster')&&v.dataset.poster) v.setAttribute('poster',v.dataset.poster);
          if(!v.hasAttribute('src')&&v.dataset.src){{ v.setAttribute('src',v.dataset.src); v.load(); }}
          if(motion&&!quiet&&!small){{ var p=v.play(); if(p&&p.catch) p.catch(function(){{}}); }}
        }}
        if(window.IntersectionObserver){{
          var io=new IntersectionObserver(function(es){{
            for(var i=0;i<es.length;i++) if(es[i].isIntersecting){{ attach(true); io.disconnect(); return; }}
          }},{{rootMargin:'300px'}});
          io.observe(v);
        }} else {{ attach(true); }}
        b.addEventListener('click',function(){{ attach(false); v.paused?v.play():v.pause(); sync(); }});
        v.addEventListener('play',sync); v.addEventListener('pause',sync);
        sync();
      }})();
      </script>
    </div>
  </div>
</section>
'''

# EQLS AURAS — the band for the overlay, from Session C's adjudicated copy.
#
# THE NAME IS "EQLS Auras", NOT "EQL Source Auras" AND NOT "EQL Auras". It reads
# aloud as "Equals Auras", and it anchors a planned logo family — =Auras,
# =50Upgrades, =SkyLedger. Session C wrote "EQL Auras"; a first ruling changed
# it to "EQL Source Auras"; the owner overruled that on 18 Aug 2026 and this is
# the settled form. Do not expand it back on the grounds that it reads like an
# abbreviation. It is one.
#
# THE TEXT IS LIFTED FROM docs/auras/band.html, NOT RETYPED. That file is what
# the word count was measured against, and every sentence in it is backed claim
# by claim in docs/auras/CLAIMS.md. Four phrases are load-bearing and are not to
# be tidied by a later pass:
#
#   - "The idea is WeakAuras'" is a credit the site owes an influence. It is a
#     claim about design intent, sourced to the author rather than to the code.
#   - the from-scratch clause and the not-affiliated clause are what keep the
#     credit from reading as a claim of lineage or endorsement.
#   - "Targeting" is a claim about an intention rather than an event. The
#     project's own handoff says "dev build only, nothing shipped", so
#     "releasing" would be false. It must never be softened into a promise.
#   - "of its own" in the network sentence scopes the claim to the application's
#     code rather than to the Electron runtime beneath it.
#
# THE VIDEO LEADS. .featgrid is a single column at every width, so DOM order is
# reading order and the figure sits above the prose. That is deliberate: the
# overlay is a thing you have to see to understand, and the sentence explaining
# it lands better after you have watched it happen.
#
# NO IFRAME, EVER. An embed would make this page issue a third-party request on
# load, which is the one thing every claim on this site about running locally
# depends on not doing. The file is served from our own origin under a content
# hash by _build/media.py, exactly as the Sky Ledger trailer is.
#
# NO CONTROL IMPLYING SOUND. The encode carries no audio stream at all, so a
# mute button would offer to silence something that does not exist. Pause is the
# only control, and the caption says "silent" so a reader knows before they ask.
# THE LOCKOUT BAND. Third, above the Auras teaser, by the rule recorded above.
#
# Build facts read from assets/lockouts.json. The band deliberately carries no
# duration: the measured figure is a DIFFERENCE between two timers and the
# six-day period only follows from it if the replay period is exactly one hour.
# A landing-page band is the worst place to compress that into a number, so it
# says what the tool refuses to do and sends the reader to the page for the
# arithmetic. The Director asserted the six days as fact and retracted it this
# week; a band is the copy most likely to be quoted back.
LK_APP = json.load(open('assets/lockouts.json', encoding='utf-8'))['app']

lockouts = f'''
<section class="band feat">
  <div class="shell">
    <div class="featwrap">
      <div class="featgrid">
        <div>
          <p class="eyebrow">Live now &middot; <b>reads your own log</b></p>
          <h2 class="feath">Lockout tracker</h2>
          <p class="featlede">Every other tracker here tells you what you have done. This one
            tells you <strong>what is still open</strong>. It reads your combat log in the
            browser, and <strong>your log never leaves this machine</strong>.</p>
          <p class="featsub"><strong>With no history for a boss it says &ldquo;not looked&rdquo;,
            not &ldquo;open&rdquo;.</strong> An empty log is not evidence that something is
            available, and the useful-looking guess is wrong in the one direction that costs
            you a night.</p>
          <p class="featsub">It keeps the weekly task, the instance lockout and the replay timer
            apart, which is where most lockout advice goes wrong. Tuesday belongs to the weekly
            task; the instance lockout is rolling, with no weekday at all.</p>
          <div class="featdoors">
            <a class="featdoor lead" href="app/{LK_APP['file']}">Run it in your browser &rarr;</a>
            <a class="featdoor" href="tools/lockouts.html">What it does &rarr;</a>
          </div>
        </div>
      </div>
      <p class="featfoot">One file, {LK_APP['kb']} KB &middot; build {LK_APP['hash']} &middot; nothing installed &middot; your log never leaves this machine
    </div>
  </div>
</section>
'''

auras = f'''
<section class="band feat" id="auras" style="--c:var(--instr)">
  <div class="shell">
    <div class="featwrap">
      <div class="featgrid">
        <figure class="feattrailer" id="auwrap"
                data-video="assets/media/{MEDIA['auras-trailer']['file']}"
                data-poster="assets/media/{MEDIA['auras-poster']['file']}">
          <img src="assets/media/{MEDIA['auras-poster']['file']}" width="1600" height="900"
               alt="The EQLS Auras overlay running over the game, buff icons across the top
                    of the screen each counting down its own remaining time.">
          <button class="vplay" type="button">Play</button>
          <figcaption><span>{AURAS['caption']}</span></figcaption>
        </figure>
        <div>
          <p class="eyebrow">{AURAS['eyebrow']}</p>
          <h2 class="feath">{AURAS['name']}</h2>
          <p class="featlede">{AURAS['lede']}</p>
          <p class="featsub">{AURAS['body'][0]}</p>
          <p class="featsub">{AURAS['body'][1]}</p>
          <p class="featfoot">{AURAS['platform']}</p>
          <p class="feat-cta"><a href="auras.html">More about {AURAS['name']}</a></p>
        </div>
      </div>
      <script>
      /* CLICK TO PLAY, BECAUSE THIS BAND IS NOW ABOVE THE FOLD.
         The deferred-video pattern used elsewhere loads on intersection, which is
         correct for a band a reader scrolls to. Featuring this one moved it into
         the first screen, so "load when visible" became "load immediately" and put
         839 KB of trailer back in front of first paint - undoing the fix shipped
         yesterday, silently, as a side effect of a layout decision.
         scripts/mediadefer.js caught it.
         So the poster is the page and the video is opt-in. The reader sees the
         product at once for 175 KB; the motion costs bytes only if they ask. */
      (function(){{
        var w=document.getElementById('auwrap');
        if(!w) return;
        var b=w.querySelector('.vplay');
        if(!b) return;
        b.addEventListener('click',function(){{
          var v=document.createElement('video');
          v.src=w.getAttribute('data-video');
          v.setAttribute('poster',w.getAttribute('data-poster'));
          v.muted=true; v.loop=true; v.playsInline=true; v.controls=true;
          v.setAttribute('width','1600'); v.setAttribute('height','900');
          w.replaceChild(v,w.querySelector('img'));
          b.remove();
          var p=v.play(); if(p&&p.catch) p.catch(function(){{}});
        }});
      }})();
      </script>
    </div>
  </div>
</section>
''' if MEDIA.get('auras-trailer') and MEDIA.get('auras-poster') else ''

from changelog import ENTRIES, TONE

recent = "\n".join(
  f'''      <li class="ch" style="--c:{TONE[e['kind']]}">
        <span class="k">{e['kind']}</span>
        <span class="t">{e['title']}</span>
        <span class="d">{e['date']}</span>
      </li>''' for e in ENTRIES[:4])

# THE ART COMES AFTER THE WORDS IN SOURCE ORDER, AND ONLY IN SOURCE ORDER.
#
# `{hero_art}` used to sit inside <section class="hero"> ahead of the shell, and
# it is 21,654 bytes of path data — so the headline "Norrath, measured." did not
# appear until byte 26,689 of a 241,709-byte document. Everything a crawler, a
# link-preview generator, a reader on a slow connection or a screen reader met
# first was an aria-hidden decoration.
#
# Emitted after the shell it lands the h1 at 5,032: an 81.1% improvement for
# ZERO added bytes — the file is byte-identical at 241,709.
#
# THIS CHANGES NO PIXEL. `.hero-art` is position:absolute with an explicit
# z-index at site.css:706-707, so it is out of flow and its paint order does not
# depend on markup position. Verify that before moving it back for any reason.
#
# IT IS NOT A CASE FOR DELETING THE ART. Ruled 31 Aug 2026: the sixteen inline
# SVGs are 85.4% of RAW bytes but only 39.9% of the render-blocking path over
# the wire, because path data compresses about 10.6:1 while the search index
# that would replace them compresses at 3.7:1. Removing them to save weight
# makes the page 2.23x HEAVIER. The defect was order, not size.
#
# AND THIS NOTE BELONGS HERE RATHER THAN IN THE TEMPLATE. Written first as an
# HTML comment inside the f-string, it shipped 1,269 bytes of developer prose to
# every reader and pushed the h1 it was explaining down to 6,301 — undoing a
# fifth of the fix it documented. Caught by measuring the output rather than by
# reading the diff.
# UTILITY BEFORE METHODOLOGY, in the hero lede.
#
# The lede opened on three sentences about sourcing standards and named nothing a
# reader could actually do, so a stranger's first ten seconds went on why to
# trust us rather than on what is here. An external audit read the site as a
# personal diary rather than a reference, and this paragraph is the first thing
# it would have read.
#
# The sourcing sentence STAYS - it is the reason the site exists and it is what
# the tier badges are for - but it goes second. The positioning line about
# inherited classic text moved down to "Why you can check us", the band that
# exists to argue methodology. MOVED, NOT DELETED: it is a claim about the
# state of this community's references, and dropping it to shorten a lede would
# be tidying a finding away.
#
# The rationale lives here, in Python, and not in an HTML comment beside the
# markup. A previous note of mine was written into the f-string and shipped
# 1,269 bytes to every reader, which undid a fifth of the byte-offset fix it was
# describing.
home = head("Accurate, sourced and kept current",
  "EverQuest Legends reference kept honest: progression trackers, a searchable loot index, dungeon surveys and the Plane of Sky island by island. Every claim names its source and its date.", og="home", canon="index") + bar() + f'''
<main>

<section class="hero">
  <div class="shell">
    <!-- THE EYEBROW CARRIES CONTEXT, NOT A CLAIM, AND THAT IS DELIBERATE.
         It read "EverQuest Legends &middot; surveyed, sourced, dated" until
         18 Aug 2026. The hero was making the same promise three times over: the
         masthead tagline says Survey, the eyebrow said surveyed, sourced,
         dated, and the headline says NORRATH, MEASURED. Three statements of one
         idea do not reinforce it, they divide it, and the headline is much the
         strongest of them. The other two were competing with it.
         So the eyebrow names the game and stops. Do not restore the clause on
         the grounds that the eyebrow looks bare - bare is what lets the
         headline land. -->
    <p class="eyebrow">EverQuest Legends</p>
    <h1 class="display">Norrath,<br><em>measured.</em></h1>
    <p class="hero-lede">Find what a named mob drops, what to wear at 50, and which Plane of Sky
      turn-ins you can hand in right now. {wordnum(len(TOOLS)).capitalize()} trackers, no account, no server holding your
      data. Every figure names its source and the day it was read, and every gap says so out loud.</p>
    <form class="hero-find" method="get" action="tools/index-search.html" role="search">
      <label for="hq">Search {NITEMS} items and {NNAMED} named mobs</label>
      <input id="hq" name="q" type="search" autocomplete="off"
             placeholder="Dark Reaver, Najena, Fine Steel&hellip;">
      <button type="submit">Search</button>
    </form>
    <p class="hero-sig"><span>{len(Z)} zones surveyed</span><span>{NITEMS} items indexed</span><span>{NNAMED} named recorded</span><span>{nfull} fully verified</span></p>
  </div>
  {hero_art}
  {hero_src}
</section>
{auras}
{upgrades}
{feature}
{lockouts}
<section class="band doors">
  <div class="shell">
    <div class="sechead"><div><h2 class="sec">Start here</h2>
      <p class="lede" style="margin:0">Three ways in, depending on what you came for.</p></div></div>
    <div class="doorgrid">

      <a class="door contour" href="tools/index-search.html" style="--c:var(--bone);--cx:88%;--cy:116%">
        <span class="dq">I need to find something</span>
        <h3 class="dt">{NAMES['index-search']}</h3>
        <p class="dd">Every item and named mob across the surveyed dungeons, searchable in one place.
          Ask where a thing drops, filter by class and slot, or find the named you have not met.</p>
        <span class="dgo">Search {NITEMS} items &rarr;</span>
      </a>

      <a class="door contour" href="dungeons/index.html" style="--c:var(--z01);--cx:12%;--cy:110%">
        <span class="dq">I am going into a zone</span>
        <h3 class="dt">The surveys</h3>
        <p class="dd">Population tables, named rosters with spawn data, loot tied to its drop source,
          and coordinates re-derived from <code>/loc</code> records.</p>
        <span class="dgo">{len(Z)} surveys &rarr;</span>
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
        <b>ZEM</b> is the zone experience modifier &mdash; how fast a zone pays against a
        baseline of 75.</p></div>
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
        <p class="stdp">Most of what this community reads about Legends is classic EverQuest text
          in a Legends-shaped hole. Every claim here carries the weight of its source. Tiers 1 and 2 print plain;
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
    # Agreement, because these counts move. npart was 0 from the day this
    # sentence was written until 18 Aug 2026, so "1 are partial" was never
    # rendered and never seen — a sentence that only breaks on a value the data
    # has not taken yet still breaks.
    _v = lambda n: "is" if n == 1 else "are"
    verdict = (f"By that standard <strong>{nfull} of {len(Z)}</strong> {_v(nfull)} verified, "
               f"{npart} {_v(npart)} partial and {nnone} {_v(nnone)} not verified at all. Partial surveys are "
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
    <p class="hero-lede">Each carrying a floor plan drawn from the game&rsquo;s own mesh, population
      tables, named rosters with spawn data, loot tied to its drop source, and coordinates
      re-derived from the wiki&rsquo;s <code>/loc</code> records and checked against the floor the
      game itself draws. <b>ZEM</b> is the zone experience modifier &mdash; how fast a zone pays
      against a baseline of 75.</p>
    <p class="hero-sig"><span>{len(Z)} surveys</span><span>{len([z for z in Z if z['slug'] in PLANS])} with a floor plan</span><span>{nfull} fully verified</span><span>{npart} partial</span><span>{nnone} unverified</span></p>
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
