import os, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT,'_build'))
import json
from _partials import head, bar, foot, TOOLS, wordnum

# Counts are printed from the mined data, never typed. The tools index said
# "208 named" while every other page said 209, four days after a change log
# entry promised exactly this.
IX = json.load(open("assets/index-data.json", encoding="utf-8"))
N_ITEMS, N_NAMED = len(IX["items"]), len(IX["named"])

# The known-gaps section reads the ledger rather than describing it from
# memory. On 9 Aug the gate was redefined, every zone reached full, and this
# section still said five had not cleared - on the page whose whole job is
# admitting what is wrong.
ZONES = json.load(open("assets/zones-index.json", encoding="utf-8"))

# Per-zone provenance, lifted off the surveys on 10 Aug 2026. The plates carried
# 4,033 words explaining which wiki revision a figure came from and why a marker
# pair collides - true, useful to us, and not what a player standing at a zone
# line needs. It lives here now, whole, and each survey links to its section.
BYSLUG = {z["slug"]: z for z in ZONES}
PROV = json.load(open("assets/zone-provenance.json", encoding="utf-8"))
WP = json.load(open("assets/wiki-provenance.json", encoding="utf-8"))["zones"]

# Ten prose blocks that each said the same four facts in a different order are
# one table. "not recorded" is written into the cell rather than left blank,
# because an empty cell reads as "nothing to report" and that is a different
# claim from "we did not establish this".
_rows = "".join(
    f'<tr><td class="nmob"><a href="#zone-{s_}">{BYSLUG[s_]["title"]}</a></td>'
    f'<td class="wp-date">{WP[s_]["edited"]}</td>'
    f'<td class="wp-rev">{WP[s_]["revision"]}</td>'
    f'<td>{WP[s_]["editor"]}</td>'
    f'<td>{"<b>Project 1999 import</b>, " + WP[s_]["p99_origin"] if WP[s_]["p99_origin"] else "&mdash;"}</td>'
    f'<td class="wp-note">{WP[s_]["note"]}</td></tr>'
    for s_ in sorted(WP, key=lambda k: BYSLUG[k]["plate"]))

wiki_table = f"""<div class="tw"><table class="wp">
  <thead><tr><th>Zone</th><th>Wiki page last edited</th><th>Revision</th><th>Editor</th>
    <th>Origin</th><th>What that means here</th></tr></thead>
  <tbody>{_rows}</tbody>
</table></div>"""
_np99 = sum(1 for v in WP.values() if v["p99_origin"])
_nrev = sum(1 for v in WP.values() if v["revision"] != "not recorded")

prov_blocks = "".join(
    f'<div class="zprov" id="zone-{slug}" style="--c:{BYSLUG[slug]["accent"]}">'
    f'<h3>{BYSLUG[slug]["title"]}</h3>' + "".join(notes) + '</div>'
    for slug, notes in sorted(PROV.items(), key=lambda kv: BYSLUG[kv[0]]["plate"]))
N_OPEN = sum(1 for z in ZONES if z["verify_level"] != "full")

if N_OPEN:
    gates_card = (
        '<div class="card" style="--c:var(--warn)"><div class="kicker">Dungeons</div>'
        '<h3 class="t">Verification gates</h3>'
        f'<p class="d">{wordnum(N_OPEN)} of the {len(ZONES)} surveys have not cleared the full '
        'three-gate standard. Which gate is open is listed against each zone on the '
        '<a href="dungeons/index.html" style="color:var(--warn-t)">plates page</a>.</p></div>')
else:
    gates_card = (
        '<div class="card" style="--c:var(--ok)"><div class="kicker">Dungeons</div>'
        '<h3 class="t">Verification gates, all cleared</h3>'
        '<p class="d">All ten surveys have passed all three gates, and the evidence for each '
        'is recorded on the <a href="dungeons/index.html" style="color:var(--ok)">plates page</a>. '
        'That is not the same as complete. It means each survey has been checked against its live '
        'source and every coordinate lands somewhere a player can stand &mdash; the gaps listed '
        'here are what remains.</p></div>')
# The change log lives in one place. sources.html renders all of it and the home
# page shows the most recent few; before 9 Aug 2026 this page kept its own
# hand-written copy, which had drifted eight entries behind - every correction
# made on 8 and 9 August was missing from the page CLAUDE.md points readers at.
from changelog import ENTRIES, TONE, TAG

chrows = "\n".join(
  f'''      <div class="zrow" style="--c:{TONE[e["kind"]]}"><span class="pn">{TAG[e["kind"]]}</span>
        <span><span class="zt">{e["title"]}</span><span class="zs">{e["body"]}</span></span>
        <span class="cell zonesub"><em>Type</em>{e["kind"]}</span><span class="cell"><em>Date</em>{e["date"]}</span>
        <span class="cell"></span><span class="bar"></span></div>''' for e in ENTRIES)

# ---------------------------------------------------------------- TOOLS
tools = head("Tools", f"{wordnum(len(TOOLS))} EverQuest Legends progression trackers: Plane of Sky class unlocks, race unlocks, and a race-and-primary-class calculator. No account, progress travels in the link.", rel="../", og="tools", canon="tools/index") + bar("../") + f'''
<main>

<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp; Tools</p>
    <h1 class="display">{wordnum(len(TOOLS))} trackers,<br><em>no account.</em></h1>
    <p class="hero-lede">No login, no server holding your data. Everything you tick is packed into the
      page URL &mdash; bookmark it, paste it into guild chat, mail it to yourself. Open it anywhere and
      the sheet rebuilds exactly. They autosave in your browser too, so day to day you can just come back.</p>
    <p class="hero-sig"><span>Nothing transmitted</span><span>Share by link</span><span>Works offline</span></p>
  </div>
</section>

<div class="shell">
  <section class="band" style="border-top:0;padding-top:0">
    <div class="cards c2">
      <a class="card" href="character.html" style="--c:var(--ok)">
        <div class="kicker">One sheet &middot; one link</div>
        <h3 class="t">Character sheet</h3>
        <p class="d">Your trio, your race unlocks and your Plane of Sky progress in a single address.
          Bookmark it, paste it into guild chat, open it on another machine and everything is where
          you left it &mdash; including the two trackers, which it fills in for you.</p>
        <div class="chipline"><span class="pill">No account</span><span class="pill">Nothing sent</span><span class="pill">Downloadable</span></div>
        <div class="foot"><span>Start here</span><span class="go">Open &rarr;</span></div></a>

      <a class="card" href="index-search.html" style="--c:var(--bone)">
        <div class="kicker">Lookup &middot; {N_ITEMS} items, {N_NAMED} named</div>
        <h3 class="t">The Index</h3>
        <p class="d">Every item and named mob recorded across the {len(ZONES)} surveyed dungeons, searchable in one place.
          Filter by class, slot and zone, or search a drop source to see everything a given mob carries. Each result
          links back to the survey it was mined from, so you can read the surrounding context before planning a night
          around it.</p>
        <div class="chipline"><span class="pill">Cross-zone</span><span class="pill">Class filter</span><span class="pill">No upload</span></div>
        <div class="foot"><span>Built from our own surveys</span><span class="go">Open &rarr;</span></div></a>

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

      <a class="card" href="faction-impact.html" style="--c:var(--ok)">
        <div class="kicker">Planning &middot; measured from play</div>
        <h3 class="t">Faction impact checker</h3>
        <p class="d">Faction moves while you are not looking, and you find out hours later when a vendor stops
          speaking to you. Name a zone, a faction or a race and it says what rises, what falls, how far per kill,
          and which unlocks that helps or costs. The movement is counted from our own combat logs rather than
          assumed, so it states plainly which zones we have measured and which we have not.</p>
        <div class="chipline"><span class="pill">Measured</span><span class="pill">Coverage stated</span></div>
        <div class="foot"><span>From our own logs</span><span class="go">Open &rarr;</span></div></a>

      <a class="card" href="planar-gear.html" style="--c:var(--warn)">
        <div class="kicker">Endgame &middot; five sets per slot</div>
        <h3 class="t">Planar gear targets</h3>
        <p class="d">A trio can wear planar armour from all three of its classes plus the two shared sets, so
          five sets compete for every slot and holding that in your head is genuinely hard. Pick three classes,
          choose what you are optimising for from five named presets, and lock a target per slot. No weights to
          configure. Built from 116 item records with every blank left blank.</p>
        <div class="chipline"><span class="pill">116 pieces</span><span class="pill">No configuring</span></div>
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
open('public/tools/index.html','w',encoding='utf-8',newline='\n').write(tools)

# ---------------------------------------------------------------- RAIDS
raids = head("Raid encounters", "Interactive 3D encounter guides for EverQuest Legends raid bosses: positioning, radii, phase transitions and pull strategy rendered in space.", rel="../", og="raids", canon="raids/index") + bar("../") + '''
<main>

<section class="hero page ember-hero">
  <div class="shell">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp; Raids</p>
    <h1 class="display">Boss fights<br><em>you can orbit.</em></h1>
    <p class="hero-lede">Each encounter is an interactive three-dimensional diagram &mdash; the platform,
      the boss, the stack, the radii that matter and the routes between them &mdash; because a paragraph
      about where to stand has never once been as clear as being shown.</p>
    <p class="hero-sig"><span>Drag to orbit</span><span>Arrow keys work too</span><span>No plugin</span></p>
  </div>
</section>

<div class="shell">
  <section class="band" style="border-top:0;padding-top:0">
    <div class="sechead"><span class="n">Live</span><div><h2 class="sec">Plane of Sky</h2>
      <p class="lede" style="margin:0">Nine islands, each gated by a key that only drops once the island below is
        cleared. Progression is vertical and unforgiving: fall off and every key you are carrying is destroyed.</p></div></div>
    <div class="cards c2">
      <a class="card figured contour" href="plane-of-sky.html"
         style="--c:var(--z01);--cx:14%;--cy:112%">
        <span class="fig">7</span>
        <div class="kicker">Progression &middot; solo route</div>
        <h3 class="t">Every island, fewest pulls</h3>
        <p class="d">What has to die before each boss appears, what tends to go wrong, and which
          islands forgive a mistake. Written from a post-launch solo run rather than inherited raid
          text.</p>
        <div class="chipline"><span class="pill">7 islands</span><span class="pill">Solo</span></div>
        <div class="foot"><span>Sourced, badged T3</span><span class="go">Open &rarr;</span></div></a>

      <a class="card" href="eye-of-veeshan.html" style="--c:var(--ember)">
        <div class="kicker">Island 8 &middot; Butterfly Island &middot; final boss</div>
        <h3 class="t">Eye of Veeshan</h3>
        <p class="d">Mechanically one of the simplest fights in the zone and
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
open('public/raids/index.html','w',encoding='utf-8',newline='\n').write(raids)

# ---------------------------------------------------------------- SOURCES
src = head("Sourcing standard", "How EQL Source sources, dates and verifies every claim, plus the current list of known gaps and open questions.", og="sources", canon="sources") + bar() + f'''
<main>

<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="index.html">EQL Source</a> &nbsp;/&nbsp; Accuracy</p>
    <h1 class="display">Sourcing<br><em>standard.</em></h1>
    <p class="hero-lede">This site exists because most EverQuest Legends reference material is classic
      EverQuest text in a Legends-shaped hole. The only defence against that is a standard applied
      without exceptions, including the inconvenient ones.</p>
    <p class="hero-sig"><span>Five tiers</span><span>Every claim dated</span><span>Gaps published</span></p>
  </div>
</section>

<div class="shell">

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
      <div class="card" style="--c:var(--warn)"><div class="kicker">Travel</div><h3 class="t">Druid and wizard port levels</h3>
        <p class="d">Two wiki pages disagree &mdash; 25/27 against 19/29. The Travel Guide has been shown wrong on
          translocators, so it is weighted lower, but the conflict is open.</p></div>
      <div class="card" style="--c:var(--warn)"><div class="kicker">Raids</div><h3 class="t">Plane of Sky geometry</h3>
        <p class="d">The zone has never been surveyed, so the Eye of Veeshan model is schematic rather than measured.
          A handful of <code>/loc</code> readings from islands 7 and 8 would fix it. The page says so in place.</p></div>
      <div class="card" style="--c:var(--warn)"><div class="kicker">Dungeons</div><h3 class="t">Floor plans have no room names</h3>
        <p class="d">The plans are read from the game&rsquo;s own meshes, so they carry walls and storeys but no
          labels. Which chamber is which is still something you work out from the named roster.</p></div>
      {gates_card}
      <div class="card" style="--c:var(--ok)"><div class="kicker">Help wanted</div><h3 class="t">In-game confirmation</h3>
        <p class="d">Most of these close with a screenshot or a log line. If you have one, it is worth more than another
          hour of reading wikis.</p></div>
    </div>
  </section>

  <section class="band" id="provenance">
    <div class="sechead"><span class="n">03</span><div><h2 class="sec">Where each zone's figures came from</h2>
      <p class="lede" style="margin:0">Which revision, read on which date, and what is still open per zone.
        This used to sit on the surveys themselves. It belongs here, where someone
        checking our working can find all ten in one place.</p>
      <p class="lede"><strong>The same split applies to almost every row.</strong> A wiki
        page&rsquo;s infobox and its NPC and item tables are usually live Legends data, while its
        narrative sections &mdash; Dangers, Benefits, Traveling &mdash; are imported prose from
        before the game existed. Said once here rather than repeated under every zone
        below.</p></div></div>
    {wiki_table}
    <p class="lede" style="margin:16px 0 0">{_nrev} of the ten rows carry a revision id; the rest
      say so. {_np99} of the ten pages began as Project 1999 imports, which by the provenance test in
      our standard makes their prose tier 5 however current the infobox is. The per-zone detail
      below is what did not fit in a cell.</p>
{prov_blocks}
  </section>

  <section class="band" id="changelog">
    <div class="sechead"><span class="n">04</span><div><h2 class="sec">Change log</h2>
      <p class="lede" style="margin:0">Typed by what changed, so a correction is never mistaken for an addition.</p></div></div>
    <div class="ztable">
{chrows}
    </div>
  </section>
</div>
</main>
''' + foot()
open('public/sources.html','w',encoding='utf-8',newline='\n').write(src)
print("tools, raids, sources written")
