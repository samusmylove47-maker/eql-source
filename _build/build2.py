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
# Declared by extract.py, not counted again here. len(IX["items"]) is 451 raw
# rows including groups and fragments; the site publishes 435 item pages, and
# this page printed the raw number beside The Index's own 435.
N_ITEMS, N_NAMED = IX["counts"]["item_pages"], IX["counts"]["named_pages"]

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

# Sky Ledger's dataset counts, read out of assets/sky-ledger.json rather than
# typed. _build/skyledger.py counts them from the tool's own sky.json.
SLD = json.load(open("assets/sky-ledger.json", encoding="utf-8"))["dataset"]
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
<main id="main">

<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp; Tools</p>
    <h1 class="display">{wordnum(len(TOOLS))} trackers,<br><em>no account.</em></h1>
    <p class="hero-lede">No login, no server holding your data. What you tick is packed into the page
      URL &mdash; bookmark it, paste it into guild chat, open it anywhere and the sheet rebuilds exactly.
      <strong>Sky Ledger is the exception</strong>: it reads your combat log rather than asking you to
      tick anything.</p>
    <p class="hero-sig"><span>Nothing transmitted</span><span>Share by link</span><span>Works offline</span></p>
  </div>
</section>

<div class="shell">
  <section class="band" style="border-top:0;padding-top:0">
    <div class="cards c2">
      <a class="card feature" href="sky-ledger.html" style="--c:var(--instr)">
        <div class="kicker">Progression &middot; reads your combat log</div>
        <h3 class="t">Sky Ledger</h3>
        <p class="d">It follows your own log and says which of the {SLD['quests']} Plane of Sky class-unlock tests you
          can hand in now, and what the missing pieces drop from. <strong>A turn-in piece can only be spent
          once</strong> &mdash; {SLD['contested']} of the {SLD['items']} items are wanted by more than one test, so holding one does
          not make several quests ready. It prints a dry streak as a bound rather than as a zero, and it
          replaces the tracker published here before it.</p>
        <div class="chipline"><span class="pill">{SLD['quests']} tests</span><span class="pill">{SLD['contested']} contested items</span><span class="pill">No install</span></div>
        <div class="foot"><span>Runs in the browser</span><span class="go">Open &rarr;</span></div></a>

      <a class="card" href="index-search.html" style="--c:var(--bone)">
        <div class="kicker">Lookup &middot; {N_ITEMS} items, {N_NAMED} named</div>
        <h3 class="t">The Index</h3>
        <p class="d">Every item and named mob recorded across the {len(ZONES)} surveyed dungeons, searchable in one place.
          Filter by class, slot and zone, or search a drop source to see everything a given mob carries. Each result
          links back to the survey it was mined from, so you can read the surrounding context before planning a night
          around it.</p>
        <div class="chipline"><span class="pill">Cross-zone</span><span class="pill">Class filter</span><span class="pill">No upload</span></div>
        <div class="foot"><span>Built from the surveys</span><span class="go">Open &rarr;</span></div></a>

      <a class="card" href="character.html" style="--c:var(--ok)">
        <div class="kicker">One sheet &middot; one link</div>
        <h3 class="t">Character sheet</h3>
        <p class="d">Your trio, your race unlocks and your Plane of Sky progress in a single address.
          Bookmark it, paste it into guild chat, open it on another machine and everything is where
          you left it &mdash; including the two trackers, which it fills in for you.</p>
        <div class="chipline"><span class="pill">No account</span><span class="pill">Nothing sent</span><span class="pill">Downloadable</span></div>
        <div class="foot"><span>Start here</span><span class="go">Open &rarr;</span></div></a>

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
          and which unlocks that helps or costs. The movement is counted from parsed combat logs rather than
          assumed, so it states plainly which zones are measured and which are not.</p>
        <div class="chipline"><span class="pill">Measured</span><span class="pill">Coverage stated</span></div>
        <div class="foot"><span>Measured in play</span><span class="go">Open &rarr;</span></div></a>

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
      <a class="card" href="inventory.html" style="--c:var(--ok)">
        <div class="kicker">Lookup</div>
        <h3 class="t">What have I got?</h3>
        <p class="d">Paste the wall of tab-separated text <code>/outputfile inventory</code> writes and read it
          back as a list of what you carry, with the item&rsquo;s page, its zone, its planar set and where the
          thing has been measured dropping. Nothing is uploaded; the parse happens in the page.</p>
        <div class="chipline"><span class="pill">Nothing uploaded</span><span class="pill">No gear score</span></div>
        <div class="foot"><span>Paste and read</span><span class="go">Open &rarr;</span></div></a>
    </div>

    <div class="note sig"><strong>Where these stop.</strong> Client-mined numbers, spellbook
      diffing, AA planning and 3D zone geometry belong to other tools. What is built here is what
      nobody else holds &mdash; quests, factions, routes, measured play, and a Sky tracker that
      knows a turn-in piece can only be spent once.</div>
    <div class="note sig"><strong>The race tracker and the calculator share one save.</strong> A race you mark unlocked
      in the tracker is available in the calculator straight away. Sky Ledger keeps its own, because what it holds is
      read from your log rather than ticked.</div>
    <div class="note"><strong>On privacy.</strong> Nothing is transmitted anywhere. The autosave uses your browser&rsquo;s
      own storage and the share link carries a compressed bitfield in the URL fragment &mdash; the part of a URL that is
      never sent to a server.</div>
  </section>
</div>
</main>
''' + foot("../")
open('public/tools/index.html','w',encoding='utf-8',newline='\n').write(tools)

# ---------------------------------------------------------------- RAIDS
# The Sky figures, read rather than typed. See CLAUDE.md: a number typed beside
# data drifts from it, and this page carried four of them.
#
# What is NOT read from here any more: fight counts, attacker medians and the
# thinnest fight. They measured an evening rather than the zone, and the claim
# they were propping up - that Sky is not a raid zone - stands on the cost
# comparison below, which is a comparison between two bosses.
try:
    _SL = json.load(open('assets/sky-loot.json', encoding='utf-8'))
    _SKY_BIGGEST = max(b['damage_max'] for b in _SL['bosses'])
    _SKY_KEYS = len(_SL['keys'])
    _CT = max((f['damage_low'] for f in json.load(open('assets/raids-measured.json', encoding='utf-8'))
               if f['boss'] == 'Cazic-Thule' and f['difficulty'] == 4), default=None)
    _SKY_RATIO = round(_CT / _SKY_BIGGEST) if _CT else None
except (OSError, ValueError, KeyError):
    _SKY_BIGGEST, _SKY_RATIO, _SKY_KEYS = None, None, 0

# The encounters written up, as a registry rather than as a hand-counted
# sentence. "One zone is written up in full" and the card beside it were two
# statements of the same fact, free to disagree the day a second page lands.
#
# The island count is deliberately NOT here. It belongs to _build/build8.py,
# which holds the ring the count comes from; typing 9 in a second file is the
# propagation fault scripts/gate.py exists to catch, and this page carried it
# three times over — "9", "9 islands", "Nine islands".
RAID_PAGES = [dict(slug="plane-of-sky", name="The Plane of Sky")]

# THE RAIDS INDEX IS ON THE MISTMOORE SHEET FORMAT, at the smallest size that
# still reads as the same object as raids/plane-of-sky.html: the graticule, the
# neatline, and the masthead grammar of eyebrow, Cinzel title, subtitle and
# deck. No spine and no kickers — this page has one section, and marginalia on
# a single card is decoration rather than structure.
#
# Ember stays the raids accent. The ember hero this replaced was the same idea
# said louder, and the two could not both lead the page.
RAIDS_CSS = """<style>
:root{--acc:var(--ember);--acct:var(--ember-t)}
.sheet .cards{margin-top:var(--s-6)}
.sheet .note{max-width:var(--measure-wide)}
</style>"""

raids = head("Raid encounters", "The Plane of Sky, island by island: the key chain, what each boss costs to kill, and the order to do it in.", rel="../", extra=RAIDS_CSS, og="raids", canon="raids/index") + bar("../") + f'''
<main id="main" class="raidx">
<div class="sky-wrap">
<div class="sheet">

<header class="mast">
  <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp; Raids</p>
  <p class="eyebrow">Encounter index</p>
  <div class="title"><h1>Raid encounters</h1><span class="leader"></span>
    <span class="plateno">{len(RAID_PAGES)}</span></div>
  <p class="subtitle">Written up once it has been fought and measured here</p>
  <p class="deck">An encounter is published because someone killed it, not because a description
    exists elsewhere. <strong>Sky is not a raid zone, whatever else you have read</strong> &mdash;
    its dearest boss costs about a {_SKY_RATIO}th of what Cazic-Thule costs at Refined, and every
    boss on the ring is measured below that.</p>
  <dl class="strip">
    <div class="cell"><dt>Key chain</dt><dd>{_SKY_KEYS} keys<small>confirmed in play</small></dd></div>
    <div class="cell"><dt>Difficulty</dt><dd>Base<small>D0, the only tier measured</small></dd></div>
    <div class="cell"><dt>Dearest boss</dt><dd>{_SKY_BIGGEST:,}<small>damage to kill, in Sky</small></dd></div>
  </dl>
</header>

<section>
  <div class="cards c2">
    <a class="card" href="plane-of-sky.html" style="--c:var(--ember)">
      <div class="kicker">Complete &middot; island by island</div>
      <h3 class="t">The Plane of Sky</h3>
      <p class="d">The whole zone in the order you do it: the Key Master, the spur at 1.5, and
        every island through to the Eye and the Hand of Veeshan. What each boss costs to kill,
        where the efreeti gear comes from, and how high the place actually is.</p>
      <div class="chipline"><span class="pill">Key chain confirmed</span><span class="pill">Measured in play</span></div>
      <div class="foot"><span>Base difficulty</span><span class="go">Open &rarr;</span></div></a>
  </div>

  <div class="note warn"><strong>Difficulty does not raise mob levels.</strong> D0&ndash;D4 makes
    mobs run player-style class kits, widens aggro ranges and pre-upgrades loot. Named mobs are
    often multiclass from D2, and raid bosses start appearing triple-class at D3. Nothing
    measured here reaches above D0.</div>
</section>

</div>
</div>
</main>
''' + foot("../")
open('public/raids/index.html','w',encoding='utf-8',newline='\n').write(raids)

# ---------------------------------------------------------------- SOURCES
src = head("Sourcing standard", "How EQL Source sources, dates and verifies every claim, plus the current list of known gaps and open questions.", og="sources", canon="sources") + bar() + f'''
<main id="main">

<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="index.html">EQL Source</a> &nbsp;/&nbsp; Accuracy</p>
    <h1 class="display">Sourcing<br><em>standard.</em></h1>
    <p class="hero-lede">This site exists because most EverQuest Legends reference material is classic
      EverQuest text in a Legends-shaped hole. The only defence against that is a standard applied
      without exceptions, including the inconvenient ones.</p>
    <p class="hero-sig"><span>Six tiers</span><span>Every claim dated</span><span>Gaps published</span></p>
  </div>
</section>

<div class="shell">

  <section class="band" style="border-top:0;padding-top:clamp(30px,5vw,50px)">
    <div class="sechead"><div><h2 class="sec">The hierarchy</h2></div></div>
    <div class="cards c2">
      <div class="card" style="--c:var(--ok)"><div class="kicker">Tier M &middot; strongest</div>
        <h3 class="t">Measured combat logs</h3>
        <p class="d">First-hand instrument data, parsed rather than remembered. <strong>It outranks every read
          source for what it directly measures, and generalises to nothing beyond its stated conditions.</strong>
          The zone and difficulty are published with it; a single observation is a sighting, not a rate.
          <strong>The badge is the claim that it was measured</strong> &mdash; the session behind it is
          not published.</p></div>
      <div class="card" style="--c:var(--ok)"><div class="kicker">Tier 1 &middot; strongest read source</div>
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
    <div class="sechead"><div><h2 class="sec">Known gaps</h2>
      <p class="lede" style="margin:0">This list is expected to grow as verification deepens, not shrink.</p></div></div>
    <div class="cards c2">
      <div class="card" style="--c:var(--warn)"><div class="kicker">Raids</div><h3 class="t">D4 hit points</h3>
        <p class="d">Which class kits attach to which raid boss at D3 and D4 is <strong>no longer the gap</strong>
          &mdash; Cazic-Thule and Innoruuk are parsed at three tiers with every spell each cast. What is still
          pinned by nobody is hit points: damage to kill bounds them from above and no more.</p></div>
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
        <p class="d">The mesh gives 21 bodies of walkable floor and cannot say which is which island. <strong>One
          <code>/loc</code> per island &mdash; nine readings &mdash; would label the elevation chart permanently
          and let each island be drawn properly.</strong> The page says so in place.</p></div>
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
    <div class="sechead"><div><h2 class="sec">Where each zone's figures came from</h2>
      <p class="lede" style="margin:0">Which revision, read on which date, and what is still open per zone.
        This used to sit on the surveys themselves. It belongs here, where someone
        checking the working can find it in one place. <strong>It covers the original ten surveys</strong>;
        Plane of Fear, Plane of Hate and Kedge Keep were added later and are not in it yet.</p>
      <p class="lede"><strong>The same split applies to almost every row.</strong> A wiki
        page&rsquo;s infobox and its NPC and item tables are usually live Legends data, while its
        narrative sections &mdash; Dangers, Benefits, Traveling &mdash; are imported prose from
        before the game existed. Said once here rather than repeated under every zone
        below.</p></div></div>
    {wiki_table}
    <p class="lede" style="margin:16px 0 0">{_nrev} of the ten rows carry a revision id; the rest
      say so. {_np99} of the ten pages began as Project 1999 imports, which by the provenance test in
      the standard above makes their prose tier 5 however current the infobox is. The per-zone
      detail below is what did not fit in a cell.</p>
{prov_blocks}
  </section>

  <section class="band" id="changelog">
    <div class="sechead"><div><h2 class="sec">Change log</h2>
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
