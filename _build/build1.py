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

home = head("Accurate, sourced and kept current",
  "EverQuest Legends reference kept honest: progression trackers, a searchable loot index, 3D raid encounter guides and dungeon survey plates. Every claim names its source and its date.") + bar() + f'''
<main>

<section class="hero">
  <div class="shell">
    <div class="hero-grid">
      <div>
        <p class="eyebrow">EverQuest Legends &middot; <b>surveyed, sourced, dated</b></p>
        <h1 class="display">Ten dungeons,<br><em>measured.</em></h1>
        <p class="hero-sig"><span>N 353</span><span>E 105</span><span>Plate 01 &mdash; 10</span></p>
      </div>
      <div class="hero-aside">
        <p class="lede">Legends moves every week, and most of what the community reads about it is
          classic EverQuest text in a Legends-shaped hole. This is the surveyed version.</p>
        <dl style="margin-top:var(--s-5)">
          <div><dt>{NITEMS}</dt><dd><b>items indexed</b>each with the mob that drops it</dd></div>
          <div><dt>{NNAMED}</dt><dd><b>named mobs</b>levels, coordinates, spawn notes</dd></div>
        </dl>
      </div>
    </div>

  </div>
</section>

<section class="band" style="border-top:0;padding-top:0">
  <div class="shell">
    <div class="sechead">
      <div><h2 class="sec">The plates</h2>
        <p class="lede" style="margin:0">Population tables, named rosters with spawn data, loot tied to
          its drop source, and coordinates re-derived from <code>/loc</code> records.</p></div>
      <a class="link" href="dungeons/index.html">All plates and maps &rarr;</a></div>
    <div class="plates">
{plates}
    </div>
    <div class="note"><strong>{nfull} of {len(Z)} have cleared all three verification gates.</strong>
      {npart} are partial and {nnone} are not verified at all. Which gate is open is recorded against
      each zone rather than averaged away. Partial plates are complete and useful; they have simply
      not cleared every gate.</div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead">
      <div><h2 class="sec">Tools</h2>
        <p class="lede" style="margin:0">No account, no login, no server holding your data. What you tick
          is packed into the page URL &mdash; bookmark it, paste it in guild chat, open it anywhere.</p></div>
      <a class="link" href="tools/index.html">All tools &rarr;</a></div>
    <div class="cards lead">
      <a class="card feature figured contour" href="tools/index-search.html"
         style="--c:var(--bone);--cx:92%;--cy:118%">
        <span class="fig">{NITEMS}</span>
        <div class="kicker">Loot &amp; named lookup</div>
        <h3 class="t">The Index</h3>
        <p class="d">Every item and named mob across the ten surveyed dungeons, in one searchable place.
          Ask where something drops, filter by class and slot, or find which named you still have not met.</p>
        <div class="chipline"><span class="pill">{NITEMS} items</span><span class="pill">{NNAMED} named</span><span class="pill">Cross-zone</span></div>
        <div class="foot"><span>Built from our own plates</span><span class="go">Open &rarr;</span></div></a>

      <a class="card figured contour" href="tools/plane-of-sky.html"
         style="--c:var(--instr);--cx:14%;--cy:112%">
        <span class="fig">95</span>
        <div class="kicker">Progression</div><h3 class="t">Plane of Sky</h3>
        <p class="d">Build your trio and get every class-unlock test it owes &mdash; 95 quests, 222 components,
          each tagged with the island and boss that drops it.</p>
        <div class="foot"><span>All 560 trios</span><span class="go">Open &rarr;</span></div></a>

      <a class="card figured contour" href="tools/race-unlocks.html"
         style="--c:var(--instr);--cx:88%;--cy:106%">
        <span class="fig">16</span>
        <div class="kicker">Progression</div><h3 class="t">Race unlocks</h3>
        <p class="d">Sixteen races with their factions, methods and honest work counts. Mark what you want
          and it merges the grinds into one list, stripping the duplicated steps.</p>
        <div class="foot"><span>Merged routes</span><span class="go">Open &rarr;</span></div></a>

      <a class="card figured contour" href="tools/combo-calculator.html"
         style="--c:var(--instr);--cx:20%;--cy:118%">
        <span class="fig">560</span>
        <div class="kicker">Planning</div><h3 class="t">Race &amp; primary</h3>
        <p class="d">The primary slot is the only one you can never change. Name the class that must sit
          there and the race you want, and it costs every route to both.</p>
        <div class="foot"><span>Takes you literally</span><span class="go">Open &rarr;</span></div></a>
    </div>
  </div>
</section>

<section class="band ember">
  <div class="shell">
    <div class="ember-grid">
      <div>
        <h2 class="sec">Boss fights<br>you can orbit</h2>
        <p class="lede">Positioning, radii and phase transitions rendered in three dimensions, because a
          paragraph about where to stand has never been as clear as being shown. Drag to orbit, or use the
          arrow keys.</p>
        <p style="margin:var(--s-5) 0 0"><a class="link" href="raids/eye-of-veeshan.html"
          style="margin:0;border-color:var(--ember)">Open the Eye of Veeshan &rarr;</a></p>
      </div>
      <dl class="ember-stats">
        <div><dt>Hit points</dt><dd>32,000</dd></div>
        <div><dt>Damage a swing</dt><dd>865</dd></div>
        <div><dt>Island</dt><dd>8</dd></div>
        <div><dt>Encounters built</dt><dd>1</dd></div>
      </dl>
    </div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead">
      <div><h2 class="sec">How we grade a source</h2>
        <p class="lede" style="margin:0">Higher tiers override lower ones, always. Tier 1 and Tier 2 print
          plain; anything below carries its badge wherever the claim appears, like this:
          <span class="tier t3">T3</span> <span class="tier t4">T4</span> <span class="tier t5">T5</span></p></div>
      <a class="link" href="sources.html">The full standard &rarr;</a></div>
    <div class="tier-scale scale-strip">
      <div class="ss" style="--tc:#5FA37E"><div class="n">Tier 1</div><div class="h">Developer</div>
        <div class="d">Patch notes and direct answers. Dated, authoritative, override everything below.</div></div>
      <div class="ss" style="--tc:#7FB2C7"><div class="n">Tier 2</div><div class="h">Wiki data</div>
        <div class="d">Infoboxes, NPC and item tables, coordinate records. Entered from the live game.</div></div>
      <div class="ss" style="--tc:#D9A227"><div class="n">Tier 3</div><div class="h">Named guides</div>
        <div class="d">Maintained, attributed work. Reliable, but one person&rsquo;s reading of the game.</div></div>
      <div class="ss" style="--tc:#D9762A"><div class="n">Tier 4</div><div class="h">Aggregators</div>
        <div class="d">Mined snapshots. Good for a second opinion; stale the moment a patch lands.</div></div>
      <div class="ss" style="--tc:#D46C64"><div class="n">Tier 5</div><div class="h">Classic prose</div>
        <div class="d">Wiki text imported from Project 1999. Quoted only when marked as classic.</div></div>
    </div>
    <div class="note warn"><strong>Two systems break almost all inherited advice.</strong> Characters run
      <em>three</em> classes at once, and difficulty D0&ndash;D4 changes what mobs <em>do</em> rather than what
      level they are. Any line saying &ldquo;you need a full group of level 50s&rdquo; came from a game where
      neither was true. Where we quote it, we mark it.</div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead">
      <div><h2 class="sec">What we do not know</h2>
        <p class="lede" style="margin:0">Published because a reference that hides its holes is not a
          reference.</p></div>
      <a class="link" href="sources.html#gaps">All open questions &rarr;</a></div>
    <dl class="gaplist">
      <a href="sources.html#gaps"><dt>D4 boss behaviour</dt>
        <dd>Raid bosses go triple-class at D3, but nobody has published which kits attach to which boss.
          Closes with combat logs, not research.</dd></a>
      <a href="sources.html#gaps"><dt>Plane of Sky geometry</dt>
        <dd>Never surveyed, so the Eye of Veeshan model is schematic rather than measured. A handful of
          <code>/loc</code> readings would fix it.</dd></a>
      <a href="sources.html#gaps"><dt>Respawn ceilings</dt>
        <dd>The 28 July patch lowered maximums without publishing figures. Affected plates state pre-patch
          timers as ceilings.</dd></a>
      <div><dt>Send a screenshot</dt>
        <dd>Most of these close with one tooltip, one log line or one <code>/loc</code>. In-game
          observation outranks everything on this page, including us.</dd></div>
    </dl>
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

dung = head("Dungeon survey plates",
  "Ten revamped EverQuest Legends dungeons surveyed from primary sources: population tables, named rosters, loot with drop sources and plotted coordinate maps.",
  rel="../") + bar("../") + f'''
<main>
<div class="shell">
  <div class="page-head">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp; Dungeons</p>
    <h1>Survey plates</h1>
    <p class="lede">Ten zones, each shipping a deep-reference plate and, where built, a navigation map companion.
      Population tables, named rosters with spawn data, loot tied to drop sources, and coordinates re-derived from the
      wiki&rsquo;s <code>/loc</code> records and collision-checked against the room list.</p>
  </div>

  <section class="band" style="border-top:0;padding-top:clamp(30px,5vw,50px)">
    <div class="sechead"><span class="n">All</span><div><h2 class="sec">The ten</h2></div></div>
    <div class="ztable">
{drows}
    </div>
    <div class="note"><strong>What &ldquo;verified&rdquo; means here, and why most of these are not.</strong> A zone
      counts as verified only when all three gates pass: its wiki page was fetched in full, <em>its edit history was
      fetched</em> &mdash; not just the footer date &mdash; and its coordinates were re-derived and collision-checked
      against the room list. By that standard {nfull} of {len(Z)} are verified, {npart} are partial and {nnone} are not
      verified at all. Partial plates are complete and useful; they have simply not cleared all three gates.</div>
    <div class="ztable" style="margin-top:14px">      <div class="zrow" style="--c:{[z for z in Z if z["slug"]=="befallen"][0]["accent"]}">
        <span class="pn">{[z for z in Z if z["slug"]=="befallen"][0]["plate"]:02d}</span>
        <span><span class="zt" style="font-size:var(--t-md)">{[z for z in Z if z["slug"]=="befallen"][0]["title"]}</span>
        <span class="zs">{[z for z in Z if z["slug"]=="befallen"][0]["verify_gate"]}</span></span>
        <span class="cell zonesub"></span><span class="cell"></span>
        <span class="cell"><em>Gate</em>{ {"partial":"open","none":"unstarted"}[[z for z in Z if z["slug"]=="befallen"][0]["verify_level"]] }</span>
        <span class="bar"></span></div>
      <div class="zrow" style="--c:{[z for z in Z if z["slug"]=="thehole"][0]["accent"]}">
        <span class="pn">{[z for z in Z if z["slug"]=="thehole"][0]["plate"]:02d}</span>
        <span><span class="zt" style="font-size:var(--t-md)">{[z for z in Z if z["slug"]=="thehole"][0]["title"]}</span>
        <span class="zs">{[z for z in Z if z["slug"]=="thehole"][0]["verify_gate"]}</span></span>
        <span class="cell zonesub"></span><span class="cell"></span>
        <span class="cell"><em>Gate</em>{ {"partial":"open","none":"unstarted"}[[z for z in Z if z["slug"]=="thehole"][0]["verify_level"]] }</span>
        <span class="bar"></span></div>
      <div class="zrow" style="--c:{[z for z in Z if z["slug"]=="warrens"][0]["accent"]}">
        <span class="pn">{[z for z in Z if z["slug"]=="warrens"][0]["plate"]:02d}</span>
        <span><span class="zt" style="font-size:var(--t-md)">{[z for z in Z if z["slug"]=="warrens"][0]["title"]}</span>
        <span class="zs">{[z for z in Z if z["slug"]=="warrens"][0]["verify_gate"]}</span></span>
        <span class="cell zonesub"></span><span class="cell"></span>
        <span class="cell"><em>Gate</em>{ {"partial":"open","none":"unstarted"}[[z for z in Z if z["slug"]=="warrens"][0]["verify_level"]] }</span>
        <span class="bar"></span></div>
      <div class="zrow" style="--c:{[z for z in Z if z["slug"]=="crushbone"][0]["accent"]}">
        <span class="pn">{[z for z in Z if z["slug"]=="crushbone"][0]["plate"]:02d}</span>
        <span><span class="zt" style="font-size:var(--t-md)">{[z for z in Z if z["slug"]=="crushbone"][0]["title"]}</span>
        <span class="zs">{[z for z in Z if z["slug"]=="crushbone"][0]["verify_gate"]}</span></span>
        <span class="cell zonesub"></span><span class="cell"></span>
        <span class="cell"><em>Gate</em>{ {"partial":"open","none":"unstarted"}[[z for z in Z if z["slug"]=="crushbone"][0]["verify_level"]] }</span>
        <span class="bar"></span></div>
      <div class="zrow" style="--c:{[z for z in Z if z["slug"]=="blackburrow"][0]["accent"]}">
        <span class="pn">{[z for z in Z if z["slug"]=="blackburrow"][0]["plate"]:02d}</span>
        <span><span class="zt" style="font-size:var(--t-md)">{[z for z in Z if z["slug"]=="blackburrow"][0]["title"]}</span>
        <span class="zs">{[z for z in Z if z["slug"]=="blackburrow"][0]["verify_gate"]}</span></span>
        <span class="cell zonesub"></span><span class="cell"></span>
        <span class="cell"><em>Gate</em>{ {"partial":"open","none":"unstarted"}[[z for z in Z if z["slug"]=="blackburrow"][0]["verify_level"]] }</span>
        <span class="bar"></span></div>
    </div>
  </section>

  <section class="band">
    <div class="sechead"><span class="n">Field</span><div><h2 class="sec">Navigation maps</h2>
      <p class="lede" style="margin:0">The companion document you keep open while you are in the zone.</p></div></div>
    <div class="cards c3">
{mapcards}
      <div class="card" style="--c:var(--dim)"><div class="kicker">Queued</div>
        <h3 class="t">Five to go</h3>
        <p class="d">Crushbone, Befallen, Blackburrow, The Hole and The Warrens have plates but no map yet. Blackburrow
          is next &mdash; it has an explicit three-floor structure, which makes it the strongest candidate for a full
          3D treatment rather than a flat plan.</p>
        <div class="foot"><span>In build</span></div></div>
    </div>
  </section>
</div>
</main>
''' + foot("../")
open('dungeons/index.html','w',encoding='utf-8',newline='\n').write(dung)

print("home + dungeons index written")
