import os, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT,'_build'))
import json
from _partials import head, bar, foot

Z = json.load(open('assets/zones-index.json', encoding='utf-8'))
MAPS = {"najena","splitpaw","lowerguk","nagafenslair","mistmoore"}
TOPLV = {"najena":35,"splitpaw":42,"crushbone":22,"befallen":25,"blackburrow":20,
         "lowerguk":49,"nagafenslair":55,"thehole":56,"warrens":25,"mistmoore":45}
CEIL = 56

def zsub(z):
    return f"{z['levels']}"

# ---------------------------------------------------------------- HOME
bars = "\n".join(
  f'''    <a class="sb" href="dungeons/{z['slug']}.html" style="--c:{z['accent']};--h:{round(TOPLV[z['slug']]/CEIL*100)}%;--d:{i*70}ms">
      <i></i><u>{z['title']}</u><b>{z['plate']:02d}</b></a>'''
  for i, z in enumerate(Z))

zrows = "\n".join(
  f'''    <a class="zrow" href="dungeons/{z['slug']}.html" style="--c:{z['accent']}">
      <span class="pn">{z['plate']:02d}</span>
      <span><span class="zt">{z['title']}</span><span class="zs">{zsub(z)}</span></span>
      <span class="cell zonesub"><em>Respawn</em>{z['respawn'] or 'not recorded'}</span>
      <span class="cell"><em>ZEM</em>{z['zem']} <span style="color:var(--faint)">/ {z['zem_pct']}%</span></span>
      <span class="cell"><em>Map</em>{'yes' if z['slug'] in MAPS else '—'}</span>
      <span class="bar"></span></a>''' for z in Z)

nfull = sum(1 for z in Z if z["verify_level"]=="full")
npart = sum(1 for z in Z if z["verify_level"]=="partial")
nnone = sum(1 for z in Z if z["verify_level"]=="none")

home = head("Accurate, sourced and kept current",
  "EverQuest Legends reference kept honest: progression trackers, a searchable loot index, 3D raid encounter guides and dungeon survey plates. Every claim names its source and its date.") + bar() + f'''
<main>
<div class="shell">
  <section style="padding:clamp(48px,9vw,104px) 0 0">
    <p class="eyebrow">EverQuest Legends &middot; <b>a fan reference, updated daily</b></p>
    <h1 class="display">Accurate,<br>sourced,<br><em>and kept</em><br>current.</h1>
    <p class="lede" style="margin-top:30px;font-size:clamp(17px,2.2vw,20px)">Legends is three months old and moves every
      week. Most of what the community reads about it is classic EverQuest text in a Legends-shaped hole &mdash; written
      for a game with one class per character and no difficulty dial. <strong>This site exists to be the version you can
      trust.</strong> Every figure names the page it came from and the day it was read. Every gap says so out loud.</p>

    <dl class="index-strip">
      <div class="ix"><dt>Tools</dt><dd>4<small>progression trackers and a searchable index, no account needed</small></dd></div>
      <div class="ix"><dt>Items indexed</dt><dd>452<small>with the mob that drops each one</small></dd></div>
      <div class="ix"><dt>Named mobs</dt><dd>208<small>levels, coordinates and spawn notes</small></dd></div>
      <div class="ix"><dt>Survey plates</dt><dd>{len(Z)}<small>{nfull} verified to the full three-gate standard &middot; {npart} partial &middot; {nnone} not yet</small></dd></div>
      <div class="ix"><dt>Open gaps</dt><dd>8<small>listed publicly, not hidden</small></dd></div>
    </dl>
  </section>
</div>

<section class="band">
  <div class="shell">
    <div class="sechead"><span class="n">01</span>
      <div><h2 class="sec">What we are trying to do</h2></div></div>
    <div class="pledge">
      <h3>Four commitments</h3>
      <ol>
        <li><div class="lh">Name the source, name the date</div>
          <div class="ld">Every number traces to a page we can point at, with the day it was read. If we cannot
            source it, we do not print it.</div></li>
        <li><div class="lh">Say when we do not know</div>
          <div class="ld">A guide that reads &ldquo;unresolved&rdquo; in the right place is worth more than one that
            reads smoothly and is quietly wrong. Our open questions are published, not buried.</div></li>
        <li><div class="lh">Grade the evidence in public</div>
          <div class="ld">Anything that is not a developer statement or structured wiki data carries a visible tier
            badge, so you always know how much weight a claim can bear.</div></li>
        <li><div class="lh">Check it every day</div>
          <div class="ld">The wikis move daily and the game patches weekly. Sources are re-checked twice a day, and
            anything predating the last patch that touched its subject is flagged rather than trusted.</div></li>
      </ol>
    </div>

    <h3 style="margin-top:42px">How we grade a source</h3>
    <p class="lede">Higher tiers override lower ones, always. <strong>Tier 1 and Tier 2 claims are printed
      plain.</strong> Anything below that carries its badge wherever it appears, like this:
      <span class="tier t3">T3</span> <span class="tier t4">T4</span> <span class="tier t5">T5</span></p>
    <div class="tier-scale">
      <div class="ts" style="--tc:#5FA37E"><div class="n">Tier 1 &middot; strongest</div>
        <div class="h">Developer statements</div>
        <div class="d">Official patch notes and direct developer answers. Dated, authoritative, and they override
          everything below.</div><span class="mark">printed without a badge</span></div>
      <div class="ts" style="--tc:#7FB2C7"><div class="n">Tier 2</div>
        <div class="h">Structured wiki data</div>
        <div class="d">Infoboxes, NPC tables, item tables and coordinate records &mdash; fields somebody entered from
          the live game.</div><span class="mark">printed without a badge</span></div>
      <div class="ts" style="--tc:#D9A227"><div class="n">Tier 3</div>
        <div class="h">Named community guides</div>
        <div class="d">Maintained, dated, attributed work by a named author. Reliable, but it is one person&rsquo;s
          reading of the game.</div><span class="mark">badged <span class="tier t3">T3</span></span></div>
      <div class="ts" style="--tc:#D9762A"><div class="n">Tier 4</div>
        <div class="h">Aggregators and snapshots</div>
        <div class="d">Item databases and mined-data snapshots. Good for a second opinion; stale the moment a patch
          lands.</div><span class="mark">badged <span class="tier t4">T4</span></span></div>
      <div class="ts" style="--tc:#C9453A"><div class="n">Tier 5 &middot; handle with care</div>
        <div class="h">Inherited classic prose</div>
        <div class="d">Wiki text imported from Project 1999, describing a single-class game at fixed difficulty. Quoted
          only when marked as classic.</div><span class="mark">badged <span class="tier t5">T5</span></span></div>
    </div>
    <div class="note warn"><strong>Two systems break almost all inherited advice.</strong> Characters run
      <em>three</em> classes at once, and difficulty D0&ndash;D4 changes what mobs <em>do</em> rather than what level
      they are. Any line that says &ldquo;you need a full group of level 50s&rdquo; came from a game where neither was
      true. Where we quote it, we mark it.</div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><span class="n">02</span>
      <div><h2 class="sec">Tools</h2>
        <p class="lede" style="margin:0">No account, no login, no server holding your data. Everything you tick is
          packed into the page URL &mdash; bookmark it, paste it in guild chat, open it anywhere.</p></div>
      <a class="link" href="tools/index.html">All tools &rarr;</a></div>
    <div class="cards c2">
      <a class="card" href="tools/index-search.html" style="--c:var(--bone)">
        <div class="kicker">New &middot; searchable</div><h3 class="t">The Index</h3>
        <p class="d">Every item and named mob across the ten surveyed dungeons in one place. Ask where something drops,
          filter by class and slot, or find which named you still have not met. 452 items, 208 named, each linked back
          to the plate it came from.</p>
        <div class="foot"><span>Loot &amp; named lookup</span><span class="go">Open &rarr;</span></div></a>
      <a class="card" href="tools/plane-of-sky.html" style="--c:var(--instr)">
        <div class="kicker">Progression</div><h3 class="t">Plane of Sky tracker</h3>
        <p class="d">Build your trio and get every class-unlock test it owes &mdash; 95 quests, 222 components, each
          tagged with the island and boss that drops it. With slot-competition analysis, because three classes means
          three item pools fighting over the same slots.</p>
        <div class="foot"><span>All 560 trios</span><span class="go">Open &rarr;</span></div></a>
      <a class="card" href="tools/race-unlocks.html" style="--c:var(--instr)">
        <div class="kicker">Progression</div><h3 class="t">Race unlock tracker</h3>
        <p class="d">All sixteen race unlocks with their factions, methods and honest work counts. Mark what you want
          and it merges the grinds into one shopping list, stripping the duplicated steps.</p>
        <div class="foot"><span>Merged routes</span><span class="go">Open &rarr;</span></div></a>
      <a class="card" href="tools/combo-calculator.html" style="--c:var(--instr)">
        <div class="kicker">Planning</div><h3 class="t">Race &amp; primary calculator</h3>
        <p class="d">The primary slot is the only one you can never change. Name the class that must sit there and the
          race you want, and it costs every route to both &mdash; without arguing you out of the requirement.</p>
        <div class="foot"><span>Takes you literally</span><span class="go">Open &rarr;</span></div></a>
    </div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><span class="n">03</span>
      <div><h2 class="sec">Raid encounters</h2>
        <p class="lede" style="margin:0">Boss fights you can orbit. Positioning, radii and phase transitions rendered
          in three dimensions, because a paragraph about where to stand has never been as clear as being shown.</p></div>
      <a class="link" href="raids/index.html">Encounter index &rarr;</a></div>
    <div class="cards c2">
      <a class="card" href="raids/eye-of-veeshan.html" style="--c:var(--ember)">
        <div class="kicker">Plane of Sky &middot; Island 8 &middot; final boss</div><h3 class="t">Eye of Veeshan</h3>
        <p class="d">32,000 hit points and 865 damage a swing. Full 3D model of the island stack, the pull-down to
          Island 7, and the aggro-transfer trick that moves him without keying your whole force.</p>
        <div class="foot"><span>3D model</span><span class="go">Open &rarr;</span></div></a>
      <div class="card" style="--c:var(--rule2)">
        <div class="kicker">In build</div><h3 class="t">The rest of Sky</h3>
        <p class="d">Spiroc Lord next &mdash; the vanquisher squad-respawn logic sets kill order and is nearly
          impossible to hold in your head from prose. Then Island 6&rsquo;s bee split tree, which is a decision graph
          rather than a tactic.</p>
        <div class="chipline"><span class="pill warn">D4 behaviour needs field data</span></div>
        <div class="foot"><span>Queued</span></div></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><span class="n">04</span>
      <div><h2 class="sec">Dungeon survey plates</h2>
        <p class="lede" style="margin:0">Deep reference for every revamped zone: population tables, named rosters with
          spawn data, loot tied to drop sources, and plotted coordinate maps. Bar height is the top of each zone&rsquo;s
          level band.</p></div>
      <a class="link" href="dungeons/index.html">All plates &rarr;</a></div>
    <div class="spectrum" style="margin-top:26px">
      <div class="spec-label"><span>The survey &middot; plate order</span><span>bar height = top of level band</span></div>
      <div class="spec-bars">
{bars}
      </div>
      <div class="spec-key"><span>01 &nbsp;Najena</span><span>10 &nbsp;Castle Mistmoore</span></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><span class="n">05</span>
      <div><h2 class="sec">What we do not know</h2>
        <p class="lede" style="margin:0">Published because a reference that hides its holes is not a reference.</p></div>
      <a class="link" href="sources.html#gaps">All open questions &rarr;</a></div>
    <div class="cards c3">
      <div class="card" style="--c:var(--warn)"><div class="kicker">Biggest gap</div><h3 class="t">D4 boss behaviour</h3>
        <p class="d">Difficulty raises how often mobs run extra class kits, and raid bosses go triple-class at D3
          &mdash; but nobody has published which kits attach to which boss. It closes with combat logs, not
          research.</p></div>
      <div class="card" style="--c:var(--warn)"><div class="kicker">Raids</div><h3 class="t">Sky geometry</h3>
        <p class="d">Plane of Sky has never been surveyed, so our Eye of Veeshan model is schematic rather than
          measured. A handful of <code>/loc</code> readings would fix it.</p></div>
      <div class="card" style="--c:var(--ok)"><div class="kicker">How to help</div><h3 class="t">Send a screenshot</h3>
        <p class="d">Most of our open questions close with one tooltip, one log line or one <code>/loc</code>. In-game
          observation outranks everything on this page, including us.</p></div>
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
        <span><span class="zt" style="font-size:19px">{[z for z in Z if z["slug"]=="befallen"][0]["title"]}</span>
        <span class="zs">{[z for z in Z if z["slug"]=="befallen"][0]["verify_gate"]}</span></span>
        <span class="cell zonesub"></span><span class="cell"></span>
        <span class="cell"><em>Gate</em>{ {"partial":"open","none":"unstarted"}[[z for z in Z if z["slug"]=="befallen"][0]["verify_level"]] }</span>
        <span class="bar"></span></div>
      <div class="zrow" style="--c:{[z for z in Z if z["slug"]=="thehole"][0]["accent"]}">
        <span class="pn">{[z for z in Z if z["slug"]=="thehole"][0]["plate"]:02d}</span>
        <span><span class="zt" style="font-size:19px">{[z for z in Z if z["slug"]=="thehole"][0]["title"]}</span>
        <span class="zs">{[z for z in Z if z["slug"]=="thehole"][0]["verify_gate"]}</span></span>
        <span class="cell zonesub"></span><span class="cell"></span>
        <span class="cell"><em>Gate</em>{ {"partial":"open","none":"unstarted"}[[z for z in Z if z["slug"]=="thehole"][0]["verify_level"]] }</span>
        <span class="bar"></span></div>
      <div class="zrow" style="--c:{[z for z in Z if z["slug"]=="warrens"][0]["accent"]}">
        <span class="pn">{[z for z in Z if z["slug"]=="warrens"][0]["plate"]:02d}</span>
        <span><span class="zt" style="font-size:19px">{[z for z in Z if z["slug"]=="warrens"][0]["title"]}</span>
        <span class="zs">{[z for z in Z if z["slug"]=="warrens"][0]["verify_gate"]}</span></span>
        <span class="cell zonesub"></span><span class="cell"></span>
        <span class="cell"><em>Gate</em>{ {"partial":"open","none":"unstarted"}[[z for z in Z if z["slug"]=="warrens"][0]["verify_level"]] }</span>
        <span class="bar"></span></div>
      <div class="zrow" style="--c:{[z for z in Z if z["slug"]=="crushbone"][0]["accent"]}">
        <span class="pn">{[z for z in Z if z["slug"]=="crushbone"][0]["plate"]:02d}</span>
        <span><span class="zt" style="font-size:19px">{[z for z in Z if z["slug"]=="crushbone"][0]["title"]}</span>
        <span class="zs">{[z for z in Z if z["slug"]=="crushbone"][0]["verify_gate"]}</span></span>
        <span class="cell zonesub"></span><span class="cell"></span>
        <span class="cell"><em>Gate</em>{ {"partial":"open","none":"unstarted"}[[z for z in Z if z["slug"]=="crushbone"][0]["verify_level"]] }</span>
        <span class="bar"></span></div>
      <div class="zrow" style="--c:{[z for z in Z if z["slug"]=="blackburrow"][0]["accent"]}">
        <span class="pn">{[z for z in Z if z["slug"]=="blackburrow"][0]["plate"]:02d}</span>
        <span><span class="zt" style="font-size:19px">{[z for z in Z if z["slug"]=="blackburrow"][0]["title"]}</span>
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
      <div class="card" style="--c:var(--rule2)"><div class="kicker">Queued</div>
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
