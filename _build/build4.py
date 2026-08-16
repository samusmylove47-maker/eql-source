import os, sys, json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT,'_build'))
from _partials import head, bar, foot

# WE HAVE KILLED HIM NOW, AND THE PAGE HAS TO SAY SO.
# This page was written when the Eye was a boss nobody here had fought, and its
# whole frame is the logistics of keying a raid to island 8. Three kills on
# 14-15 August 2026 contradict that frame, and one of them contradicts the
# imported stat block outright: our fullest complete view of the fight is 18,914
# damage, and damage to kill sits ABOVE hit points. A 32,000 hit point boss
# cannot die to it. The figure stays on the page, marked, because a marked
# source figure is more useful than a hole - but it no longer stands unopposed.
EYE = [f for f in json.load(open('assets/raids-measured.json', encoding='utf-8'))
       if f['boss'] == 'Eye of Veeshan']
EYE_M = next(b for b in json.load(open('assets/sky-loot.json', encoding='utf-8'))['bosses']
             if b['boss'] == 'Eye of Veeshan')
EYE_N = len(EYE)
EYE_ATK = (min(f['attackers'] for f in EYE), max(f['attackers'] for f in EYE))
EYE_SEC = (min(f['seconds'] for f in EYE), max(f['seconds'] for f in EYE))
# The fullest view is the one the parser did not mark a floor: a fight we joined
# late tells us the total is at least N, which bounds nothing from above.
EYE_FULL = max((f['damage_low'] for f in EYE if not f.get('damage_is_floor')), default=None)
EYE_MAX = max(f['damage_low'] for f in EYE)

VIEWER_CSS = '''<style>
.enc{background:var(--panel);border:1px solid var(--rule);margin:26px 0}
.enc-top{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:12px 16px;border-bottom:1px solid var(--rule)}
.enc-top .lbl{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--faint)}
.phases{display:flex;gap:6px;flex-wrap:wrap;margin-left:auto}
.ph{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.13em;text-transform:uppercase;
  padding:7px 12px;border:1px solid var(--rule);color:var(--mut);transition:all .15s}
.ph:hover{color:var(--bone);border-color:var(--rule2)}
/* The pressed tint darkens the background, so the raw ember label came out at
   3.25:1 — the active button was harder to read than the inactive ones. */
.ph[aria-pressed="true"]{border-color:var(--ember);color:var(--ember-t);background:rgba(196,72,46,.1)}
#stage{width:100%;height:clamp(360px,54vh,600px);display:block;background:#070402;cursor:grab;touch-action:none}
#stage:active{cursor:grabbing}
.enc-legend{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,190px),1fr));gap:1px;
  background:var(--rule);border-top:1px solid var(--rule)}
.enc-legend>*{min-width:0}
.lg{background:var(--panel);padding:11px 14px}
.lg .sw{display:inline-block;width:9px;height:9px;margin-right:8px;vertical-align:middle}
.lg .nm{font-family:"Saira Condensed",sans-serif;font-size:15px;font-weight:600;text-transform:uppercase;letter-spacing:.03em}
.lg .ds{font-family:"IBM Plex Mono",monospace;font-size:10px;color:var(--dim);display:block;margin-top:2px;line-height:1.5}
.enc-note{padding:12px 16px;border-top:1px solid var(--rule);font-size:13px;color:var(--mut);line-height:1.55}
.enc-note strong{color:var(--txt)}
.statline{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,130px),1fr));gap:1px;
  background:var(--rule);border:1px solid var(--rule);margin:26px 0}
.statline>*{min-width:0}
.stx{background:var(--panel);padding:14px 16px}
.stx dt{font-family:"IBM Plex Mono",monospace;font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--dim);margin-bottom:5px}
.stx dd{margin:0;font-family:"Saira Condensed",sans-serif;font-size:30px;font-weight:700;line-height:.92;color:var(--bone)}
.stx dd small{display:block;font-family:"Public Sans",sans-serif;font-size:11px;font-weight:400;
  color:var(--dim);letter-spacing:0;line-height:1.4;margin-top:5px}
.steps{counter-reset:s;list-style:none;padding:0;margin:20px 0 0}
.steps li{counter-increment:s;position:relative;padding:14px 0 14px 52px;border-bottom:1px solid var(--rule)}
.steps li::before{content:counter(s,decimal-leading-zero);position:absolute;left:0;top:14px;
  font-family:"IBM Plex Mono",monospace;font-size:14px;font-weight:600;color:var(--ember-t)}
.steps .sh{font-family:"Saira Condensed",sans-serif;font-size:19px;font-weight:700;text-transform:uppercase;
  letter-spacing:.02em;color:var(--bone);line-height:1.15}
.steps .sb{font-size:14px;color:var(--mut);margin-top:4px;max-width:72ch}
.loot{width:100%;border-collapse:collapse;font-size:13.5px;margin-top:8px}
.loot th{font-family:"IBM Plex Mono",monospace;font-size:9px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--dim);text-align:left;padding:10px 12px;background:var(--panel2);border-bottom:1px solid var(--rule)}
.loot td{padding:9px 12px;border-bottom:1px solid var(--rule);background:var(--panel);vertical-align:top}
.loot tr:last-child td{border-bottom:0}
.loot .it{font-family:"Saira Condensed",sans-serif;font-size:15px;font-weight:600;color:var(--bone);letter-spacing:.02em}
.loot .cl{font-family:"IBM Plex Mono",monospace;font-size:10.5px;color:var(--ember-t);letter-spacing:.06em}
.scroller{overflow-x:auto;border:1px solid var(--rule);margin:8px 0 0}
.scroller:focus-visible{outline:2px solid var(--bone);outline-offset:2px}
.scroller table{min-width:560px}
</style>'''

BODY = '''
<main>
<div class="shell">
  <div class="page-head">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp; <a href="index.html">Raids</a> &nbsp;/&nbsp; Plane of Sky</p>
    <p class="eyebrow" style="color:var(--ember-t)">Island 8 &middot; Butterfly Island &middot; final boss</p>
    <h1>Eye of<br>Veeshan</h1>
    <p class="lede">Mechanically among the simplest fights in the zone, and <strong>we have now killed him
      @@EYE_N@@ times with @@EYE_ATK_LO@@ to @@EYE_ATK_HI@@ attackers, in @@EYE_SEC_LO@@ to @@EYE_SEC_HI@@
      seconds</strong> <span class="tier tM">TIER M</span>. What is hard here is the logistics, not the
      boss: reaching him means keying everyone to the top of a nine-island stack where a single knockback
      destroys every key a player is carrying.</p>
  </div>

  <section class="band" style="border-top:0;padding-top:clamp(28px,4vw,44px)">
    <dl class="statline">
      <div class="stx"><dt>Hit points</dt><dd class="disputed">32,000 <span class="tier t5">T5</span><small>pre-launch import &mdash; our own kills contradict it, see below</small></dd></div>
      <div class="stx"><dt>Damage to kill</dt><dd>@@EYE_FULL@@ <span class="tier tM">M</span><small>fullest of @@EYE_N@@ kills, base difficulty</small></dd></div>
      <div class="stx"><dt>Melee damage</dt><dd>@@EYE_MAXHIT@@ max <span class="tier tM">M</span><small>@@EYE_AVG@@ average over @@EYE_LANDED@@ hits on one character</small></dd></div>
      <div class="stx"><dt>Island</dt><dd>8<small>Butterfly</small></dd></div>
      <div class="stx"><dt>Key</dt><dd>Veeshan&rsquo;s<small>from island 7 Sirran</small></dd></div>
      <div class="stx"><dt>Trash</dt><dd>None<small>the Hand, if up</small></dd></div>
      <div class="stx"><dt>Death touch</dt><dd>?<small>sources conflict &mdash; see below</small></dd></div>
    </dl>

    <div class="note"><strong>The 32,000 cannot be right.</strong> Damage to kill counts every attacker and
      sits <em>above</em> a boss&rsquo;s health rather than measuring it, so a boss that dies to
      @@EYE_FULL@@ damage does not have 32,000 hit points. That is our fullest view of @@EYE_N@@ kills on
      14&ndash;15 August 2026, all at base difficulty <span class="tier tM">TIER M</span>. <strong>It is
      evidence against the figure rather than a replacement for it</strong> &mdash; a client log records
      only what one character witnessed, so a total can be short but never long, and we still cannot tell
      you what the number actually is. The imported figure stays on the page, struck, because a marked
      source figure is more useful than a hole.</div>

    <div class="note warn"><strong>The one thing to settle before you pull.</strong> The wiki&rsquo;s Dangers section
      states plainly that boss NPCs no longer death touch. The Island 8 walkthrough directly below it describes a tank
      rotation built entirely around the Eye death touching. The Dangers line is the Legends-era edit; the walkthrough
      is inherited Project 1999 text. <strong>Bring the rotation anyway.</strong> If death touch is gone you have
      over-prepared by two warriors. If it is not and you assumed it was, you lose your main tank thirty seconds in
      with no replacement warmed up.</div>
  </section>

  <section class="band">
    <div class="sechead"><span class="n">01</span><div><h2 class="sec">The encounter in space</h2>
      <p class="lede" style="margin:0">Drag to orbit, scroll to zoom. Switch phases to see where people stand and where
        the boss ends up.</p></div></div>

    <div class="enc">
      <div class="enc-top">
        <span class="lbl">Plane of Sky &middot; islands 7 &amp; 8</span>
        <div class="phases">
          <button class="ph" data-phase="0" aria-pressed="true">Approach</button>
          <button class="ph" data-phase="1" aria-pressed="false">Pull down</button>
          <button class="ph" data-phase="2" aria-pressed="false">Engage on 7</button>
          <button class="ph" data-phase="3" aria-pressed="false">Fight on 8</button>
        </div>
      </div>
      <canvas id="stage" tabindex="0" role="img" aria-label="Three-dimensional schematic of Plane of Sky islands 7 and 8 showing raid positioning for the Eye of Veeshan encounter. Focus this diagram and use the arrow keys to orbit, plus and minus to zoom."></canvas>
      <div class="enc-legend">
        <div class="lg"><span class="nm"><span class="sw" style="background:#C4482E"></span>Eye of Veeshan</span>
          <span class="ds">died to @@EYE_FULL@@ damage, base difficulty</span></div>
        <div class="lg"><span class="nm"><span class="sw" style="background:#7FB2C7"></span>Main tank</span>
          <span class="ds">rotation of three to four</span></div>
        <div class="lg"><span class="nm"><span class="sw" style="background:#F2EADA"></span>Raid stack</span>
          <span class="ds">melee in, casters back</span></div>
        <div class="lg"><span class="nm"><span class="sw" style="background:#D9A227"></span>Bait / puller</span>
          <span class="ds">eats the first touch</span></div>
        <div class="lg"><span class="nm"><span class="sw" style="background:#5FA37E"></span>Ashtray portal</span>
          <span class="ds">one-way, keyed</span></div>
      </div>
      <p class="enc-note"><strong>This model is schematic, not surveyed.</strong> Island proportions and the vertical
        offset are drawn to communicate the relationship between 7 and 8, not to scale from game coordinates. Every
        other guide on this site plots from real <code>/loc</code> data; this one cannot yet, because Plane of Sky
        coordinates have not been surveyed. <strong>That is the next thing to fix</strong> &mdash; a handful of
        <code>/loc</code> readings from the two islands would turn this into a measured model.</p>
    </div>
  </section>

  <section class="band">
    <div class="sechead"><span class="n">02</span><div><h2 class="sec">Getting him down to Island 7</h2>
      <p class="lede" style="margin:0">Almost nobody keys a full raid to Island 8. You bring him to a force that is
        already standing on 7, which is where you killed Sister of the Spire anyway.</p></div></div>

    <div class="note sig"><strong>Why it is worth the trouble.</strong> Island 8 is small and every player who goes up
      needs Veeshan&rsquo;s Key, earned by turning a Replica of the Wyrm Queen in to the Sirran that spawns on Sister of
      the Spire&rsquo;s corpse. Island 7 is large, your raid is already on it, and it costs you nothing. The only people
      who need to be keyed are the one or two running the pull.</div>

    <ol class="steps">
      <li><div class="sh">Park a pet on Island 8</div>
        <div class="sb">A pet class clicks up, drops a pet and sets it to guard. The pet does not need to survive
          anything &mdash; it needs to be a leash the Eye will follow.</div></li>
      <li><div class="sh">Get the owner back down</div>
        <div class="sb">A wizard ports the pet class to Island 1 and they run back up to 7 with the raid. The reported
          alternative is to leave a corpse on 7 with a three-hour rez timer beforehand and take the rez back down, which
          avoids needing a wizard at all.</div></li>
      <li><div class="sh">Walk the pet into the Eye</div>
        <div class="sb">With the owner on 7, order the pet onto the Eye. The Ploktor variant is cleaner: a shaman on 7
          duels a keyed player standing on 8, sends the pet up to attack them, has the pet Guard then Back off next to
          the Eye, then binds sight on the pet to target the Eye directly and orders the attack.</div></li>
      <li><div class="sh">Transfer the aggro before he lands</div>
        <div class="sb">The moment the pull starts, everyone spams a fast, disposable buff on the pet owner &mdash;
          Bracer of the Hidden is the classic tool. Each landed buff hands the caster aggro. On the way down the Eye
          will kill the pet owner and probably one buffer. That is the intended cost.</div></li>
      <li><div class="sh">Engage on open ground</div>
        <div class="sb">Once he is on 7 it is a tank-and-spank with a rotation. Fight him away from the port-in pad and
          well clear of the temple, and keep melee push disciplined &mdash; a boss pushed onto a hill can drop under the
          world, and mobs that go under the world summon players under it with them, which drops you to Freeport and
          destroys every key you hold.</div></li>
    </ol>

    <div class="note warn"><strong>The failure that ends the night.</strong> Not a wipe &mdash; wipes are recoverable.
      It is somebody getting knocked, flung or pushed off an island. Buffs are stripped on zone-in, no teleport works
      inside the zone, and falling destroys every Plane of Sky key you are carrying and drops you in the bay off East
      Freeport. Anyone who falls is finished for the run.</div>
  </section>

  <section class="band">
    <div class="sechead"><span class="n">03</span><div><h2 class="sec">Tanking it</h2></div></div>
    <p class="lede">There are no adds, no phases and no movement requirement, so this is a sustained-damage check on
      your healers rather than a burst check. <strong>How long a check, we cannot tell you.</strong> The only published
      figures for the Eye predate the game and contradict each other &mdash; see the sourcing section. Bring more
      healing than you think and time the first minute yourself.</p>
    <div class="cards c3" style="margin-top:24px">
      <div class="card" style="--c:var(--ember)"><div class="kicker">If death touch is live</div>
        <h3 class="t">Rotate three</h3>
        <p class="d">Send someone expendable in first to eat the opening touch &mdash; that buys the first real tank a
          clean window. Have the next tank at full health with a defensive ready before the current one dies, not after.
          Aggro re-establishment after a swap is the part that goes wrong.</p></div>
      <div class="card" style="--c:var(--ok)"><div class="kicker">If it is gone</div>
        <h3 class="t">One tank, rolled heals</h3>
        <p class="d">A single geared warrior with defensive up and clerics rolling heals holds it indefinitely. The
          fight becomes a mana-management problem rather than a survival one.</p></div>
      <div class="card" style="--c:var(--warn)"><div class="kicker">At D3 and above</div>
        <h3 class="t">Assume a class kit</h3>
        <p class="d">Raid bosses start appearing triple-class at D3. Nobody has published which kits attach to the Eye,
          so plan for the categories that hurt most: a cleric kit that heals through your damage, an enchanter kit that
          mezzes your tank, a magician kit that adds a pet. <strong>If you have logs, they close this gap.</strong></p></div>
    </div>
  </section>

  <section class="band">
    <div class="sechead"><span class="n">04</span><div><h2 class="sec">What he drops</h2>
      <p class="lede" style="margin:0">The Eye is the sole source of one component on eleven of the sixteen class
        unlock lines. Every trio in the game has at least one member who needs something here.</p></div>
      <a class="link" href="../tools/plane-of-sky.html">Track it &rarr;</a></div>
    <div class="scroller" tabindex="0" role="region" aria-label="Loot table, scrolls sideways"><table class="loot">
      <thead><tr><th>Component</th><th>Feeds</th><th>Reward</th></tr></thead>
      <tbody>
        <tr><td class="it">Ethereal Emerald</td><td class="cl">WAR</td><td>Fangol &mdash; 2H Slash 29 / 35, proc</td></tr>
        <tr><td class="it">Tear of Quellious</td><td class="cl">MNK</td><td>Golden Sash of Tranquility &mdash; 41% haste</td></tr>
        <tr><td class="it">Nebulous Diamond</td><td class="cl">BRD</td><td>Harmonic Spear</td></tr>
        <tr><td class="it">Mithril Bands</td><td class="cl">CLR &middot; BST</td><td>Baton of the Sky &middot; Windhowl</td></tr>
        <tr><td class="it">Storm Sky Opal</td><td class="cl">DRU</td><td>Espri</td></tr>
        <tr><td class="it">Large Sky Sapphire</td><td class="cl">ENC</td><td>Rod of the Protecting Winds</td></tr>
        <tr><td class="it">Hazy Opal &middot; Large Opal</td><td class="cl">MAG</td><td>Staff of the Magister &middot; Staff of Elemental Mastery: Air</td></tr>
        <tr><td class="it">Large Sky Diamond</td><td class="cl">PAL</td><td>Truvinan</td></tr>
        <tr><td class="it">Shimmering Pearl</td><td class="cl">RNG</td><td>Windstriker</td></tr>
        <tr><td class="it">Bloodsky Sapphire</td><td class="cl">ROG</td><td>Thornstinger</td></tr>
        <tr><td class="it">Blood Sky Ruby &middot; Fae Pauldrons</td><td class="cl">SHD</td><td>Khyldorn &middot; Pearlescent Pauldrons</td></tr>
        <tr><td class="it">Symbol of Veeshan</td><td class="cl">SHM</td><td>Garduk</td></tr>
        <tr><td class="it">Large Sky Lapis</td><td class="cl">WIZ</td><td>Nargon&rsquo;s Staff</td></tr>
      </tbody></table></div>
    <div class="note"><strong>The Hand of Veeshan shares the island</strong> and is usually not up. He spawns from
      killing the Overseer of Air, back on Island 4, and he carries the Efreeti weapons &mdash; the same ones Noble
      Dojorn drops on Island 1.5. If he is up, kill him first; he should be single-pullable from the north edge of
      Island 7.</div>
  </section>

  <section class="band">
    <div class="sechead"><span class="n">05</span><div><h2 class="sec">Sourcing</h2></div></div>
    <div class="note"><strong>eqlwiki.com/Plane_of_Sky</strong>, revision 151528, last edited 28 June 2026, read
      4 August 2026. Source of the island structure, the key chain, the pull-down strategies and the Hand of Veeshan
      spawn condition. The Dangers section is a Legends-era edit; the island walkthroughs are an inherited Project 1999
      import and are marked as such wherever quoted.</div>
    <div class="note warn"><strong>The Eye&rsquo;s stat block is not Legends data, and we published it as though it
      were.</strong> Corrected 8 August 2026. Three problems, found by applying the provenance test in
      <code>CLAUDE.md</code>:
      <br><br>
      <strong>One.</strong> The 32,000 hit points come from <em>eqlwiki.com/Eye_of_Veeshan</em>, whose oldest revision
      is 25 March 2026 by an account named <code>imported&gt;Kistraxx</code> &mdash; four months before EverQuest
      Legends launched on 28 July 2026. It is a Project 1999 import.
      <br><br>
      <strong>Two.</strong> The melee figure is contradicted within eqlwiki itself. The Plane of Sky page gives 865 a
      swing; the Eye&rsquo;s own page gives 200 to 200. That is a factor of four, and both pages predate launch.
      <br><br>
      <strong>Three.</strong> That stat block lists the Eye as a single class, Warrior, at level 70. Legends raid
      bosses run three classes from D3, and a single-class stat block is a classic stat block.
      <br><br>
      Both figures now carry a <span class="tier t5">T5</span> badge, and the tanking section no longer reasons from
      either. What replaces them is in-game observation: time the fight and count the swings.
      <br><br>
      <strong>Done, 14&ndash;15 August 2026.</strong> The Eye swung at one of our characters @@EYE_SWINGS@@
      times and landed @@EYE_LANDED@@, for @@EYE_AVG@@ on average and
      @@EYE_MAXHIT@@ at most <span class="tier tM">TIER M</span>. That is nearer the lower of the two
      inherited figures than the higher, but it <strong>does not settle them</strong>: mitigation differs per target,
      and what a boss does to one character is not what it does to a tank.</div>
    <div class="note"><strong>eqprogression.com</strong>, Plane of Sky Quests / Class Unlocks, read 4 August 2026.
      Source of the component-to-reward mapping in the loot table.</div>
    <div class="note warn"><strong>Not sourced, and stated as unknown:</strong> whether death touch is live at launch,
      what class kits the Eye runs at D3 and D4, and the real coordinate geometry of islands 7 and 8. All three close
      with in-game observation.</div>
  </section>
</div>
</main>
'''

SCRIPT = r'''<script src="../assets/vendor/three.min.js"></script>
<script>
(function(){
  var cv=document.getElementById('stage'); if(!cv||!window.THREE) return;
  var mq=window.matchMedia&&window.matchMedia('(prefers-reduced-motion:reduce)');
  var reduce=!!(mq&&mq.matches);
  // Honour the setting when it changes, not only at load.
  if(mq&&mq.addEventListener) mq.addEventListener('change',function(e){reduce=e.matches;});
  var C={ember:0xC4482E,tank:0x7FB2C7,raid:0xE6E9E4,bait:0xD9A227,portal:0x5FA37E,
         deck7:0x1E262B,deck8:0x232C32,edge:0x3A484F};

  var scene=new THREE.Scene(); scene.fog=new THREE.Fog(0x0A0E10,60,190);
  var cam=new THREE.PerspectiveCamera(42,1,0.1,500);
  var rend=new THREE.WebGLRenderer({canvas:cv,antialias:true,alpha:false});
  rend.setClearColor(0x0A0E10,1);

  scene.add(new THREE.AmbientLight(0xffffff,0.62));
  var key=new THREE.DirectionalLight(0xffffff,0.7); key.position.set(30,50,22); scene.add(key);
  var rim=new THREE.DirectionalLight(0x7FB2C7,0.3); rim.position.set(-30,10,-25); scene.add(rim);

  function island(r,y,col,segs){
    var g=new THREE.Group();
    var top=new THREE.Mesh(new THREE.CylinderGeometry(r,r*0.97,1.1,segs),
      new THREE.MeshLambertMaterial({color:col}));
    top.position.y=y; g.add(top);
    var base=new THREE.Mesh(new THREE.CylinderGeometry(r*0.95,r*0.18,r*0.75,segs),
      new THREE.MeshLambertMaterial({color:0x141A1D}));
    base.position.y=y-r*0.38-0.5; g.add(base);
    var ring=new THREE.Mesh(new THREE.TorusGeometry(r,0.12,6,segs),
      new THREE.MeshBasicMaterial({color:C.edge}));
    ring.rotation.x=Math.PI/2; ring.position.y=y+0.6; g.add(ring);
    for(var i=1;i<=3;i++){
      var gr=new THREE.Mesh(new THREE.TorusGeometry(r*i/4,0.03,4,segs),
        new THREE.MeshBasicMaterial({color:C.edge,transparent:true,opacity:0.35}));
      gr.rotation.x=Math.PI/2; gr.position.y=y+0.62; g.add(gr);
    }
    scene.add(g); return g;
  }
  island(22,0,C.deck7,14);   // island 7 — drake, large
  island(10.5,26,C.deck8,12);// island 8 — butterfly, small

  function marker(col,size,h){
    var g=new THREE.Group();
    var m=new THREE.Mesh(new THREE.CylinderGeometry(size*0.42,size*0.42,h||2.4,10),
      new THREE.MeshLambertMaterial({color:col}));
    m.position.y=(h||2.4)/2; g.add(m);
    var cap=new THREE.Mesh(new THREE.SphereGeometry(size*0.5,12,10),
      new THREE.MeshLambertMaterial({color:col}));
    cap.position.y=(h||2.4)+size*0.2; g.add(cap);
    var halo=new THREE.Mesh(new THREE.RingGeometry(size*0.9,size*1.15,20),
      new THREE.MeshBasicMaterial({color:col,side:THREE.DoubleSide,transparent:true,opacity:0.5}));
    halo.rotation.x=-Math.PI/2; halo.position.y=0.9; g.add(halo);
    scene.add(g); return g;
  }
  function radius(col,r,op){
    var m=new THREE.Mesh(new THREE.RingGeometry(r-0.35,r,48),
      new THREE.MeshBasicMaterial({color:col,side:THREE.DoubleSide,transparent:true,opacity:op}));
    m.rotation.x=-Math.PI/2; scene.add(m); return m;
  }
  function path(pts,col){
    var g=new THREE.BufferGeometry().setFromPoints(pts.map(function(p){return new THREE.Vector3(p[0],p[1],p[2]);}));
    var l=new THREE.Line(g,new THREE.LineDashedMaterial({color:col,dashSize:1.6,gapSize:1.1,transparent:true,opacity:0.9}));
    l.computeLineDistances(); scene.add(l); return l;
  }

  var boss=marker(C.ember,3.0,3.6);
  var tank=marker(C.tank,1.8,2.6);
  var bait=marker(C.bait,1.5,2.2);
  var raid=[]; for(var i=0;i<8;i++) raid.push(marker(C.raid,1.15,1.9));
  var portal=marker(C.portal,1.5,0.7);
  portal.position.set(15,1.1,11);
  var melee=radius(C.tank,7,0.42);
  var aoe=radius(C.ember,12,0.22);
  var pull=path([[0,28.6,0],[4,24,4],[10,14,9],[-7,2.6,-5]],C.bait);

  // phase definitions: [bossPos, tankPos, baitPos, raidCentre, raidRadius, notes]
  var P=[
    {b:[0,27.1,0],   t:[9,1.1,7],    k:[3.5,27.1,3],  c:[10,1.1,8],  r:5,  pull:false, aoe:false},
    {b:[0,27.1,0],   t:[7,1.1,6],    k:[2.5,27.1,2],  c:[9,1.1,7],   r:5,  pull:true,  aoe:false},
    {b:[-7,1.1,-5],  t:[-2.5,1.1,-1],k:[7,1.1,6],     c:[3,1.1,3],   r:7,  pull:true,  aoe:true},
    {b:[0,27.1,0],   t:[3.4,27.1,2.4],k:[-3.4,27.1,-2.4],c:[4.5,27.1,3.5],r:3.6,pull:false,aoe:true}
  ];
  var cur=0;
  function setPhase(i){
    cur=i; var p=P[i];
    boss.position.set(p.b[0],p.b[1],p.b[2]);
    tank.position.set(p.t[0],p.t[1],p.t[2]);
    bait.position.set(p.k[0],p.k[1],p.k[2]);
    for(var j=0;j<raid.length;j++){
      var a=j/raid.length*Math.PI*2;
      raid[j].position.set(p.c[0]+Math.cos(a)*p.r, p.c[1], p.c[2]+Math.sin(a)*p.r);
    }
    melee.position.set(p.b[0],p.b[1]-1.0,p.b[2]); melee.visible=true;
    aoe.position.set(p.b[0],p.b[1]-1.0,p.b[2]);  aoe.visible=p.aoe;
    pull.visible=p.pull;
    document.querySelectorAll('.ph').forEach(function(b){
      b.setAttribute('aria-pressed',String(+b.dataset.phase===i));});
  }
  document.querySelectorAll('.ph').forEach(function(b){
    b.addEventListener('click',function(){setPhase(+b.dataset.phase);});});

  // hand-rolled orbit — no extra dependency
  var az=0.68, pol=1.06, dist=68, tgt=new THREE.Vector3(0,12,0);
  var drag=false, lx=0, ly=0;
  function place(){
    cam.position.set(tgt.x+dist*Math.sin(pol)*Math.sin(az),
                     tgt.y+dist*Math.cos(pol),
                     tgt.z+dist*Math.sin(pol)*Math.cos(az));
    cam.lookAt(tgt);
  }
  function down(x,y){drag=true;lx=x;ly=y;}
  function move(x,y){
    if(!drag)return;
    az-=(x-lx)*0.008; pol=Math.max(0.22,Math.min(1.44,pol-(y-ly)*0.006));
    lx=x;ly=y;place();
  }
  cv.addEventListener('mousedown',function(e){down(e.clientX,e.clientY);});
  window.addEventListener('mousemove',function(e){move(e.clientX,e.clientY);});
  window.addEventListener('mouseup',function(){drag=false;});
  cv.addEventListener('touchstart',function(e){if(e.touches.length===1)down(e.touches[0].clientX,e.touches[0].clientY);},{passive:true});
  cv.addEventListener('touchmove',function(e){if(e.touches.length===1){move(e.touches[0].clientX,e.touches[0].clientY);e.preventDefault();}},{passive:false});
  window.addEventListener('touchend',function(){drag=false;});
  // Zoom only once the viewer has focus, so a page scroll that happens to pass
  // over the canvas keeps scrolling the page instead of being swallowed.
  cv.addEventListener('wheel',function(e){
    if(document.activeElement!==cv)return;
    dist=Math.max(34,Math.min(150,dist+e.deltaY*0.06)); place(); e.preventDefault();},{passive:false});

  // Keyboard orbit. Without this the diagram is pointer-only and unusable to
  // anyone navigating by keyboard.
  cv.addEventListener('keydown',function(e){
    var STEP=0.12, k=e.key, handled=true;
    if(k==='ArrowLeft')       az-=STEP;
    else if(k==='ArrowRight') az+=STEP;
    else if(k==='ArrowUp')    pol=Math.max(0.22,pol-STEP*0.6);
    else if(k==='ArrowDown')  pol=Math.min(1.44,pol+STEP*0.6);
    else if(k==='+'||k==='=') dist=Math.max(34,dist-6);
    else if(k==='-'||k==='_') dist=Math.min(150,dist+6);
    else handled=false;
    if(handled){place();e.preventDefault();}
  });

  function resize(){
    var w=cv.clientWidth, h=cv.clientHeight;
    if(!w||!h)return;
    rend.setPixelRatio(Math.min(window.devicePixelRatio||1,2));
    rend.setSize(w,h,false); cam.aspect=w/h; cam.updateProjectionMatrix();
  }
  window.addEventListener('resize',resize);

  var t=0;
  function loop(){
    requestAnimationFrame(loop);
    if(!reduce){ t+=0.012;
      var s=1+Math.sin(t*1.6)*0.045; boss.scale.set(s,1,s);
      if(P[cur].aoe) aoe.material.opacity=0.16+Math.sin(t*1.6)*0.09;
    }
    rend.render(scene,cam);
  }
  resize(); place(); setPhase(0); loop();
  setTimeout(resize,120);
})();
</script>'''

# BODY is a plain string, not an f-string, because it carries the 3D engine's
# JavaScript and every brace in it would need doubling. The measured figures are
# substituted by name instead. A leaked token renders as literal @@EYE_FULL@@ on
# the page, which scripts/gate.py now refuses to publish - the first version of
# this shipped "{EYE_FULL:,}" straight to the page and passed 723 checks.
MEASURED = {
    '@@EYE_N@@': str(EYE_N),
    '@@EYE_FULL@@': f'{EYE_FULL:,}',
    '@@EYE_ATK_LO@@': str(EYE_ATK[0]), '@@EYE_ATK_HI@@': str(EYE_ATK[1]),
    '@@EYE_SEC_LO@@': str(EYE_SEC[0]), '@@EYE_SEC_HI@@': str(EYE_SEC[1]),
    '@@EYE_SWINGS@@': str(EYE_M['melee_swings']),
    '@@EYE_LANDED@@': str(EYE_M['melee_landed']),
    '@@EYE_AVG@@': str(EYE_M['melee_avg']),
    '@@EYE_MAXHIT@@': str(EYE_M['melee_max']),
}
for _k, _v in MEASURED.items():
    BODY = BODY.replace(_k, _v)

page = head("Eye of Veeshan",
  "Interactive 3D raid guide for the Eye of Veeshan, final boss of the Plane of Sky: the pull-down to Island 7, tank rotation and the full component drop list. His hit points are a pre-launch import and this page says so.",
  rel="../", extra=VIEWER_CSS, og="raids", canon="raids/eye-of-veeshan") + bar("../") + BODY + foot("../").replace('</body>', SCRIPT + '\n</body>')
open('public/raids/eye-of-veeshan.html','w',encoding='utf-8',newline='\n').write(page)
print("raid guide written:", len(page), "bytes")
