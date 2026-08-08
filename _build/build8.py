"""raids/plane-of-sky.html — island-by-island, for small groups.

SOURCING. Nearly everything tactical on this page comes from one source: a
post-launch video walkthrough by Archmage Flux, published 7 August 2026, in which
the creator farms every island solo and says so. That is tier 3 — a named,
dated, attributed account — and it is badged as such throughout.

Why that source is worth more here than the wiki: it is post-launch (the game
launched 28 July 2026), it is first-hand play rather than inherited text, and the
creator states their trio, their health pool and their gear level, which is what
makes the advice interpretable. A tactic that works for one trio at one gear
level is not a universal truth, and the page says so.

WHAT IS DELIBERATELY ABSENT. No boss hit points, armour class or damage figures,
except the one the source states from play. Every published stat block for these
bosses traces to eqlwiki pages created in 2025 and early 2026, before the game
existed — see the provenance test in CLAUDE.md.
"""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

# tier: the creator's own difficulty rating, presented as their judgement
ISLANDS = [
    dict(n=2, name="Protector of Sky", tier="B", c="var(--z02)",
         spawn="Pull the azoraks near where you arrive. The boss spawns after a couple of kills.",
         watch="Azoraks have a very large aggro radius. Wait until you can stand in the corner "
               "without pulling more before you take the boss.",
         note="Straightforward. Nothing here punishes a mistake badly."),
    dict(n=3, name="Gorgalosk", tier="B", c="var(--z03)",
         spawn="The boss can be started directly. It arrives with one add.",
         watch="Two problems compound each other. Adds path into the boss room &mdash; through the "
               "doorway, or patrolling in &mdash; and the boss resists slow more than most. The "
               "trash also stuns.",
         note="Fine when it goes well, genuinely nasty when it does not. The source reports more "
              "avoidable deaths here than on any other island, from a slow resist arriving at the "
              "same time as unexpected adds."),
    dict(n=4, name="Keeper of Souls", tier="S", c="var(--z06)",
         spawn="Wait until nothing is near the boss, then pull it to the island edge and fight "
               "along the wall.",
         watch="Nothing, if the pull is clean. The source reports the boss staying solo every time "
               "it was pulled solo.",
         note="Rated the easiest island of the eight. Low resist rate, no adds, no mechanics that "
              "require positioning beyond the initial pull."),
    dict(n=5, name="Spiroc Lord", tier="A", c="var(--z01)",
         spawn="Pull a few spirocs to a corner. The Spiroc Guardian spawns after roughly two to "
               "four kills. Kill the Guardian in that same corner, then move to the Lord.",
         watch="The trash are rangers and druids, so expect damage shields and small heals rather "
               "than burst. Invisibility or stealth gets you to the Lord without re-pulling.",
         note="More to clear than the islands before it, but little that can go badly wrong. Fight "
              "the Lord near the teleport."),
    dict(n=6, name="Bazzt Zzzt", tier="B", c="var(--z01)",
         spawn="From one specific position the boss can be pulled with a single bee. Kill that bee "
               "by the teleport pad.",
         watch="<strong>The boss splits into smaller adds.</strong> The source's route is to leave "
               "at that moment &mdash; take the teleport to island 7, clear onward, and return "
               "later to finish the boss from the island's east side, where it can be pulled alone.",
         note="Described as the most technically demanding island other than the Eye. Pacification "
              "gets the boss solo directly, but needs extended range to reach. Feign death serves "
              "the same purpose. The drops are among the best in the game."),
    dict(n=7, name="Sister of the Spire", tier="A", c="var(--z05)",
         spawn="She can be walked up to and pulled directly. She often spawns alongside undine "
               "spirits; solo, she is straightforward.",
         watch="<strong>The drakes are the real danger, not the boss.</strong> They cast, and the "
               "source reports fire damage approaching 2,000 on a character with a 5,600 health "
               "pool. Adds are less frequent here than on island 3, but far more punishing.",
         note="The source gives the Sister roughly 16,000 health from play, and describes her as "
              "only mildly resistant. This is the one boss figure on this page taken from "
              "observation rather than from a pre-launch wiki page."),
    dict(n=8, name="Eye of Veeshan", tier="A", c="var(--ember)",
         spawn="No trash. The source states it is not possible to pull adds on this island.",
         watch="<strong>The entire fight turns on whether slow lands.</strong> Landed early, it is "
               "comfortable. Resisted repeatedly, the boss hits hard enough that recovery from a "
               "low health pool is unlikely.",
         note="With feign death the risk largely disappears &mdash; attempt the slow, feign if it "
              "resists, try again. Without it, a run of resists is the failure case. "
              "<a href=\"eye-of-veeshan.html\">The 3D encounter guide</a> covers positioning and "
              "the pull-down in detail."),
]

TIER_TONE = {"S": "var(--ok)", "A": "var(--instr)", "B": "var(--z01)"}

cards = "\n".join(f'''
      <article class="island contour" style="--c:{i['c']};--cx:{88 if i['n']%2 else 12}%;--cy:11{i['n']%3}%">
        <span class="isl-n">Island {i['n']}</span>
        <span class="isl-tier" style="--tc:{TIER_TONE[i['tier']]}">{i['tier']} tier</span>
        <h3 class="isl-name">{i['name']}</h3>
        <dl class="isl-body">
          <dt>Getting the boss</dt><dd>{i['spawn']}</dd>
          <dt>What catches people</dt><dd>{i['watch']}</dd>
          <dt>In practice</dt><dd>{i['note']}</dd>
        </dl>
      </article>''' for i in ISLANDS)

page = head("Plane of Sky, island by island",
  "How to reach each Plane of Sky boss in EverQuest Legends with the fewest pulls, from a "
  "post-launch solo run. Spawn conditions, what goes wrong, and which islands punish mistakes.",
  rel="../") + bar("../") + f'''
<main>

<section class="hero page ember-hero">
  <div class="shell">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp;
      <a href="index.html">Raids</a> &nbsp;/&nbsp; Plane of Sky</p>
    <h1 class="display">Every island,<br><em>fewest pulls.</em></h1>
    <p class="hero-lede">What has to die before each boss appears, what tends to go wrong, and which
      islands forgive a mistake. Written from a post-launch solo run rather than from inherited raid
      text, and badged <span class="tier t3">T3</span> because it rests on one named account.</p>
    <p class="hero-sig"><span>7 islands</span><span>Solo route</span><span>Post-launch</span><span>Read 8 Aug 2026</span></p>
  </div>
</section>

<div class="shell">
  <div class="note"><strong>Read the source's position before you use its advice.</strong> This comes
    from a player running <em>warrior, rogue and shaman</em> with roughly 5,600 health after shaman
    buffs, describing their own gear as middle of the road, playing alone. Slow and feign death appear
    throughout because that trio has them. A trio without slow will find islands 3 and 8 substantially
    harder than the ratings here suggest, and the ratings are that player's judgement rather than a
    measurement.</div>
</div>

<section class="band" style="border-top:0;padding-top:0">
  <div class="shell">
    <div class="sechead"><div><h2 class="sec">The islands</h2>
      <p class="lede" style="margin:0">Ordered by progression. Each island's key drops from the boss
        below it, so the route is fixed even when the tactics are not.</p></div></div>
    <div class="islands">
{cards}
    </div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="split">
      <div>
        <div class="sechead"><div><h2 class="sec">What this changes</h2>
          <p class="lede" style="margin:0">Three things in this account contradict how Plane of Sky is
            usually described, and all three matter for a small group.</p></div></div>
        <ol class="findings">
          <li><b>It is a solo farm.</b> Every island here was cleared alone. Advice written for raids
            of dozens does not merely over-prepare you &mdash; it sends you to the wrong islands and
            the wrong pulls.</li>
          <li><b>Slow is the deciding mechanic, not damage.</b> On islands 3 and 8 the fight is
            decided by whether slow lands. That is a resist check, and no published hit point total
            tells you anything about it.</li>
          <li><b>The dangerous thing is rarely the boss.</b> On island 7 the drakes hit far harder
            than the Sister. On island 3 the adds do more damage than the boss's own kit.</li>
        </ol>
      </div>
      <aside class="standard contour" style="--c:var(--warn);--cx:90%;--cy:112%">
        <h3 class="stdh">Still unknown</h3>
        <p class="stdp">Named here rather than guessed at. Each closes with observation, not reading.</p>
        <ul class="gatelist">
          <li class="gaterow" style="--c:var(--warn)"><span class="gn">01</span>
            <span class="gz">Boss health</span><span class="gl">unrecorded</span>
            <span class="gs">Only the Sister of the Spire has a figure from play, roughly 16,000.
              Every other published total traces to a pre-launch wiki import.</span></li>
          <li class="gaterow" style="--c:var(--warn)"><span class="gn">02</span>
            <span class="gz">Difficulty tier</span><span class="gl">unstated</span>
            <span class="gs">The source does not say which difficulty these runs were at. D0 and D4
              are different fights, so treat the ratings as a floor.</span></li>
          <li class="gaterow" style="--c:var(--warn)"><span class="gn">03</span>
            <span class="gz">Class kits at D3+</span><span class="gl">unpublished</span>
            <span class="gs">Raid bosses run three classes from D3. Which kits attach to which Sky
              boss is recorded nowhere. <a href="../learn/difficulty.html">What difficulty
              changes</a> sets out what is known about the tiers and what is not.</span></li>
        </ul>
      </aside>
    </div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><span class="n">Sourcing</span><div><h2 class="sec">Where this came from</h2></div></div>
    <div class="note"><strong>&ldquo;Plane of Sky Speed Guide&rdquo;, Archmage Flux</strong>, published
      7 August 2026, 9 minutes 4 seconds. <span class="tier t3">T3</span> &mdash; a named, dated,
      first-hand account. Source of every spawn condition, route and hazard on this page, and of the
      Sister of the Spire health figure. Chapter marks: island 2 at 0:00, island 3 at 0:46, island 4
      at 1:59, island 5 at 2:42, island 6 at 3:49, island 7 at 5:49, island 8 at 7:32.
      <a href="https://www.youtube.com/watch?v=jcx6Db-ACVE">Watch it</a>.</div>
    <div class="note"><strong>everquestlegends.com patch notes, 16 June 2026.</strong>
      <span class="tier t1">T1</span> Source of the Sky spawn restructure: bosses drop the key to the
      next island, trash no longer drops key parts, and several bosses changed between static and
      conditional spawns.</div>
    <div class="note warn"><strong>What is not sourced here, and why there are so few numbers.</strong>
      Every published hit point, armour class and damage figure for these bosses traces to eqlwiki
      pages created between January 2025 and March 2026 &mdash; before EverQuest Legends existed. The
      Spiroc Lord's page dates to January 2025; Bazzt Zzzt's to November 2025, never edited since.
      Those are Project 1999 imports and this site does not print them as Legends fact. The single
      exception is the Sister's health, which the source states from play.</div>
  </div>
</section>

</main>
''' + foot("../")

open('raids/plane-of-sky.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"raids/plane-of-sky.html written: {len(ISLANDS)} islands")
