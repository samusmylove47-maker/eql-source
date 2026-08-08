import os, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT,'_build'))
from _partials import head, bar, foot

# ---------------------------------------------------------------- TOOLS
tools = head("Tools", "Three EverQuest Legends progression trackers: Plane of Sky class unlocks, race unlocks, and a race-and-primary-class calculator. No account, progress travels in the link.", rel="../") + bar("../") + '''
<main>
<div class="shell">
  <div class="page-head">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp; Tools</p>
    <h1>Tools</h1>
    <p class="lede">Three trackers. No account, no login, no server holding your data. Everything you tick is packed
      into the page URL &mdash; bookmark it, paste it into guild chat, mail it to yourself. Open it anywhere and the
      sheet rebuilds exactly. They also autosave in your browser, so day to day you can just come back.</p>
  </div>

  <section class="band" style="border-top:0;padding-top:clamp(30px,5vw,50px)">
    <div class="cards c2">
      <a class="card" href="index-search.html" style="--c:var(--bone)">
        <div class="kicker">Lookup &middot; 452 items, 208 named</div>
        <h3 class="t">The Index</h3>
        <p class="d">Every item and named mob recorded across the ten surveyed dungeons, searchable in one place.
          Filter by class, slot and zone, or search a drop source to see everything a given mob carries. Each result
          links back to the plate it was mined from, so you can read the surrounding context before planning a night
          around it.</p>
        <div class="chipline"><span class="pill">Cross-zone</span><span class="pill">Class filter</span><span class="pill">No upload</span></div>
        <div class="foot"><span>Built from our own plates</span><span class="go">Open &rarr;</span></div></a>

      <a class="card" href="plane-of-sky.html" style="--c:var(--instr)">
        <div class="kicker">Progression &middot; all 560 trios</div>
        <h3 class="t">Plane of Sky tracker</h3>
        <p class="d">Pick your three classes and it builds the character sheet: every class-unlock test the trio owes,
          each component tagged with the island and boss that drops it, and an island ladder that recounts what is left
          as you tick things off. Includes slot-competition analysis, because three classes means three item pools
          fighting over the same equipment slots.</p>
        <div class="chipline"><span class="pill">95 quests</span><span class="pill">222 components</span><span class="pill">16 classes</span></div>
        <div class="foot"><span>Share link</span><span class="go">Open &rarr;</span></div></a>

      <a class="card" href="race-unlocks.html" style="--c:var(--instr)">
        <div class="kicker">Progression &middot; 16 unlocks</div>
        <h3 class="t">Race unlock tracker</h3>
        <p class="d">Every race unlock with its required factions, the recommended method, and honest work counts &mdash;
          items to gather, kills, hours. Mark the races you want and the route page merges their grinds into a single
          shopping list, stripping out the duplicated steps. Wood Elf and High Elf share two of three outright.</p>
        <div class="chipline"><span class="pill">Faction routes</span><span class="pill">Merged list</span></div>
        <div class="foot"><span>Share link</span><span class="go">Open &rarr;</span></div></a>

      <a class="card" href="combo-calculator.html" style="--c:var(--instr)">
        <div class="kicker">Planning</div>
        <h3 class="t">Race &amp; primary calculator</h3>
        <p class="d">The primary slot is the only one you can never change &mdash; it locks at level 11 and every
          loadout you ever build will contain it. Name the class that must sit there and the race you want, and it
          costs every route to both. It takes the requirement literally instead of talking you out of it.</p>
        <div class="chipline"><span class="pill">Launcher races</span><span class="pill">Token vs grind</span></div>
        <div class="foot"><span>Shares progress</span><span class="go">Open &rarr;</span></div></a>
    </div>

    <div class="note sig"><strong>Where these stop, and who to go to next.</strong> These are progression and
      reference tools built on quest, faction and survey data. For client-mined numbers, combat log parsing, spellbook
      diffing, AA planning and 3D zone geometry, <a href="https://eqltools.com" style="color:var(--bone)">EQL Tools</a>
      is excellent and does all of it properly. We link rather than duplicate; there is no sense in shipping a worse
      copy of a tool that already exists.</div>
    <div class="note sig"><strong>The race tracker and the calculator share one save.</strong> They are two views of the
      same sheet, so a race you mark unlocked in the tracker is treated as available by the calculator straight away.
      The Plane of Sky tracker keeps its own separate save.</div>
    <div class="note"><strong>On privacy.</strong> Nothing is transmitted anywhere. The autosave uses your browser&rsquo;s
      own storage and the share link carries a compressed bitfield in the URL fragment &mdash; the part of a URL that is
      never sent to a server. A fully filled sheet comes out around ninety characters.</div>
  </section>
</div>
</main>
''' + foot("../")
open('tools/index.html','w',encoding='utf-8',newline='\n').write(tools)

# ---------------------------------------------------------------- RAIDS
raids = head("Raid encounters", "Interactive 3D encounter guides for EverQuest Legends raid bosses: positioning, radii, phase transitions and pull strategy rendered in space.", rel="../") + bar("../") + '''
<main>
<div class="shell">
  <div class="page-head">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp; Raids</p>
    <h1>Encounters</h1>
    <p class="lede">Boss fights you can orbit. Each encounter is built as an interactive three-dimensional diagram
      &mdash; the platform, the boss, the raid stack, the radii that matter and the routes between them &mdash; because
      a paragraph about where to stand has never once been as clear as being shown.</p>
  </div>

  <section class="band" style="border-top:0;padding-top:clamp(30px,5vw,50px)">
    <div class="sechead"><span class="n">Live</span><div><h2 class="sec">Plane of Sky</h2>
      <p class="lede" style="margin:0">Nine islands, each gated by a key that only drops once the island below is
        cleared. Progression is vertical and unforgiving: fall off and every key you are carrying is destroyed.</p></div></div>
    <div class="cards c2">
      <a class="card" href="eye-of-veeshan.html" style="--c:var(--ember)">
        <div class="kicker">Island 8 &middot; Butterfly Island &middot; final boss</div>
        <h3 class="t">Eye of Veeshan</h3>
        <p class="d">32,000 hit points and 865 damage a swing. Mechanically one of the simplest fights in the zone and
          logistically one of the hardest, because getting to him means keying your entire raid to Island 8 &mdash;
          unless you pull him down instead.</p>
        <div class="chipline"><span class="pill live">3D model</span><span class="pill">Pull strategy</span><span class="pill">Tank rotation</span></div>
        <div class="foot"><span>Full guide</span><span class="go">Open &rarr;</span></div></a>

      <div class="card" style="--c:var(--dim)">
        <div class="kicker">Queued &middot; islands 5, 6, 7, 4, 3</div>
        <h3 class="t">Spiroc Lord &rarr; Gorgalosk</h3>
        <p class="d">The build order is set by which fights a diagram actually helps with. Island 5 first: the
          vanquisher squad-respawn logic determines kill order and is almost impossible to hold in your head from prose.
          Then Island 6&rsquo;s bee split tree, which is a decision graph, not a tactic.</p>
        <div class="chipline"><span class="pill warn">Needs field data</span></div>
        <div class="foot"><span>In build</span></div></div>
    </div>

    <div class="note warn"><strong>On difficulty tiers.</strong> These guides describe the encounters as documented.
      D0&ndash;D4 does <em>not</em> raise mob levels &mdash; it makes mobs run player-style class kits, widens aggro
      ranges and pre-upgrades loot. Named mobs are often multiclass from D2 and raid bosses start appearing triple-class
      at D3. That means a D4 pull can contain cleric-kit adds that chain-stun and heal, and no published source
      documents which kits attach to which boss. <strong>Encounter-specific D4 behaviour is the single biggest gap on
      this site, and it can only be closed with combat logs from people who have actually done it.</strong></div>

    <div class="note"><strong>One documented conflict, unresolved.</strong> The wiki&rsquo;s Dangers section states that
      boss NPCs no longer death touch. The island walkthroughs immediately below it describe death touch rotations on
      Keeper of Souls, the Spiroc Lord, Bazzt Zzzt, Sister of the Spire and the Eye. The Dangers line is the
      Legends-era edit; the walkthrough prose is inherited classic text. Every guide here assumes no death touch and
      tells you where that assumption would cost you if it is wrong.</div>
  </section>
</div>
</main>
''' + foot("../")
open('raids/index.html','w',encoding='utf-8',newline='\n').write(raids)

# ---------------------------------------------------------------- SOURCES
src = head("Sourcing standard", "How EQL Source sources, dates and verifies every claim, plus the current list of known gaps and open questions.") + bar() + '''
<main>
<div class="shell">
  <div class="page-head">
    <p class="crumb"><a href="index.html">EQL Source</a> &nbsp;/&nbsp; Sources</p>
    <h1>Sourcing<br>standard</h1>
    <p class="lede">This site exists because most EverQuest Legends reference material is classic EverQuest text in a
      Legends-shaped hole. The only defence against that is a standard applied without exceptions, including the
      inconvenient ones.</p>
  </div>

  <section class="band" style="border-top:0;padding-top:clamp(30px,5vw,50px)">
    <div class="sechead"><span class="n">01</span><div><h2 class="sec">The hierarchy</h2></div></div>
    <div class="cards c2">
      <div class="card" style="--c:var(--ok)"><div class="kicker">Tier 1 &middot; strongest</div>
        <h3 class="t">Official patch notes</h3>
        <p class="d">Dated, authoritative, and they override everything below them. Anything published after a wiki
          page&rsquo;s last edit supersedes that page.</p></div>
      <div class="card" style="--c:var(--ok)"><div class="kicker">Tier 2</div>
        <h3 class="t">Structured wiki data</h3>
        <p class="d">Infoboxes, NPC tables, item tables, coordinate records on eqlwiki. Machine-shaped fields that
          somebody entered from the live game.</p></div>
      <div class="card" style="--c:var(--instr)"><div class="kicker">Tier 3</div>
        <h3 class="t">Named community guides</h3>
        <p class="d">eqprogression.com, and maintained wiki user guides such as Alanna&rsquo;s Race Unlock Guide.
          Named authors, actively updated, dated. Reliable, but they are one person&rsquo;s reading of the game.</p></div>
      <div class="card" style="--c:var(--instr)"><div class="kicker">Tier 4</div>
        <h3 class="t">Aggregators</h3>
        <p class="d">EQL Build Forge, EQ Legends Tools. Useful for cross-checking a number against a second pair of
          eyes. Each carries a snapshot date; anything older than the last patch is treated as stale.</p></div>
      <div class="card" style="--c:var(--warn)"><div class="kicker">Tier 5 &middot; marked on sight</div>
        <h3 class="t">Wiki prose</h3>
        <p class="d">Large parts are a Project 1999 import, sometimes word for word. It describes a single-class game
          at fixed difficulty. It is quoted only when marked as classic, never as Legends fact.</p></div>
    </div>
    <div class="note sig"><strong>Two systems break almost all inherited advice.</strong> Legends characters run
      <em>three</em> classes at once, and difficulty D0&ndash;D4 changes mob behaviour rather than mob level. Any line
      that says &ldquo;you need a full group of level 50s&rdquo; came from a game where neither was true, and is
      unreliable in both directions.</div>
  </section>

  <section class="band" id="gaps">
    <div class="sechead"><span class="n">02</span><div><h2 class="sec">Known gaps</h2>
      <p class="lede" style="margin:0">This list is expected to grow as verification deepens, not shrink.</p></div></div>
    <div class="cards c2">
      <div class="card" style="--c:var(--warn)"><div class="kicker">Raids</div><h3 class="t">D4 boss behaviour</h3>
        <p class="d">No published source documents which class kits attach to which raid boss at D3 and D4. Needs
          combat logs.</p></div>
      <div class="card" style="--c:var(--warn)"><div class="kicker">Plane of Sky</div><h3 class="t">Five class tooltips</h3>
        <p class="d">Ranger, Rogue, Shadow Knight, Shaman and Wizard reward stat blocks are unconfirmed for Legends.
          The turn-ins and drop sources are current; only the stats are missing.</p></div>
      <div class="card" style="--c:var(--warn)"><div class="kicker">Dungeons</div><h3 class="t">Respawn ceilings</h3>
        <p class="d">The 28 July patch lowered maximum respawn times without publishing figures. Affected plates state
          the pre-patch timer as a ceiling rather than a current value.</p></div>
      <div class="card" style="--c:var(--warn)"><div class="kicker">Dungeons</div><h3 class="t">Placeholder removals</h3>
        <p class="d">If placeholders are gone entirely, published spawn percentages may no longer mean anything.
          Unresolved, and it affects how every named roster should be written.</p></div>
      <div class="card" style="--c:var(--warn)"><div class="kicker">Travel</div><h3 class="t">Druid and wizard port levels</h3>
        <p class="d">Two wiki pages disagree &mdash; 25/27 against 19/29. The Travel Guide has been shown wrong on
          translocators, so it is weighted lower, but the conflict is open.</p></div>
      <div class="card" style="--c:var(--warn)"><div class="kicker">Raids</div><h3 class="t">Plane of Sky geometry</h3>
        <p class="d">The zone has never been surveyed, so the Eye of Veeshan model is schematic rather than measured.
          A handful of <code>/loc</code> readings from islands 7 and 8 would fix it. The page says so in place.</p></div>
      <div class="card" style="--c:var(--warn)"><div class="kicker">Dungeons</div><h3 class="t">Five missing maps</h3>
        <p class="d">Crushbone, Befallen, Blackburrow, The Hole and The Warrens have survey plates but no navigation
          map companion. Blackburrow is next; its explicit three-floor structure suits a 3D treatment.</p></div>
      <div class="card" style="--c:var(--warn)"><div class="kicker">Dungeons</div><h3 class="t">Verification gates</h3>
        <p class="d">Five of the ten plates have not cleared the full three-gate standard. Which gate is open is
          listed against each zone on the <a href="dungeons/index.html" style="color:var(--warn-t)">plates page</a>.</p></div>
      <div class="card" style="--c:var(--ok)"><div class="kicker">Help wanted</div><h3 class="t">In-game confirmation</h3>
        <p class="d">Most of these close with a screenshot or a log line. If you have one, it is worth more than another
          hour of reading wikis.</p></div>
    </div>
  </section>

  <section class="band" id="changelog">
    <div class="sechead"><span class="n">03</span><div><h2 class="sec">Change log</h2>
      <p class="lede" style="margin:0">Typed by what changed, so a correction is never mistaken for an addition.</p></div></div>
    <div class="ztable">
      <div class="zrow" style="--c:var(--ok)"><span class="pn">FIX</span>
        <span><span class="zt">Item count on The Index</span><span class="zs">The page described itself as holding &ldquo;389 items&rdquo; while the index it shipped held 452, and its own counter said 452 on screen. 389 was never correct at any point. Every count on the site is now printed from the mined data rather than typed by hand, so the sentence and the tool cannot disagree again</span></span>
        <span class="cell zonesub"><em>Type</em>Correction</span><span class="cell"><em>Date</em>7 Aug 2026</span>
        <span class="cell"></span><span class="bar"></span></div>
      <div class="zrow" style="--c:var(--bone)"><span class="pn">NEW</span>
        <span><span class="zt">Site launch</span><span class="zs">Ten plates, five maps, three tools, first raid encounter</span></span>
        <span class="cell zonesub"><em>Type</em>Addition</span><span class="cell"><em>Date</em>6 Aug 2026</span>
        <span class="cell"></span><span class="bar"></span></div>
      <div class="zrow" style="--c:var(--ok)"><span class="pn">FIX</span>
        <span><span class="zt">Tracker state handling</span><span class="zs">Changes made in the trio builder were never saved, so reloading restored the previous trio. Reset also left the trio and the calculator selections untouched. Both trackers now have separate <em>Clear ticks</em> and <em>Start over</em> actions</span></span>
        <span class="cell zonesub"><em>Type</em>Correction</span><span class="cell"><em>Date</em>6 Aug 2026</span>
        <span class="cell"></span><span class="bar"></span></div>
      <div class="zrow" style="--c:var(--ok)"><span class="pn">FIX</span>
        <span><span class="zt">Verification counting</span><span class="zs">Front page claimed 8 of 10 plates verified. By the project&rsquo;s own three-gate standard it is 5. Corrected, and the open gate is now named per zone</span></span>
        <span class="cell zonesub"><em>Type</em>Correction</span><span class="cell"><em>Date</em>6 Aug 2026</span>
        <span class="cell"></span><span class="bar"></span></div>
      <div class="zrow" style="--c:var(--ok)"><span class="pn">FIX</span>
        <span><span class="zt">Primary-slot logic</span><span class="zs">Calculator no longer suggests demoting a class you require in the primary slot</span></span>
        <span class="cell zonesub"><em>Type</em>Correction</span><span class="cell"><em>Date</em>6 Aug 2026</span>
        <span class="cell"></span><span class="bar"></span></div>
      <div class="zrow" style="--c:var(--z01)"><span class="pn">DAT</span>
        <span><span class="zt">Race unlock data</span><span class="zs">Rebuilt against Alanna&rsquo;s guide revision 166686</span></span>
        <span class="cell zonesub"><em>Type</em>Source refresh</span><span class="cell"><em>Date</em>5 Aug 2026</span>
        <span class="cell"></span><span class="bar"></span></div>
    </div>
    <div class="note"><strong>Update cadence.</strong> Legends patches weekly and the wikis move daily. Anything on this
      site that predates the most recent patch touching its subject is flagged in place rather than silently trusted.</div>
  </section>
</div>
</main>
''' + foot()
open('sources.html','w',encoding='utf-8',newline='\n').write(src)
print("tools, raids, sources written")
