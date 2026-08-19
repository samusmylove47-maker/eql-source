"""learn/motes.html — what a mote is worth, and why converting them can cost you.

WHERE THIS COMES FROM, AND THE ONE THING TO SETTLE
--------------------------------------------------
An infographic, "EverQuest Legends Mote & Upgrade Guide", supplied 11 Aug 2026
and described as released by the developers in their Discord.

**The artefact itself is branded by a creator, not by the developers.** It
carries "THE GAME IS" as its logo and www.youtube.com/@THEGAMEIS twice, top and
bottom. Developers sharing a creator's work in an official channel does not make
that work a developer statement, and the difference is two whole tiers: a
developer post is tier 1 and prints bare, a named creator's guide is tier 3 and
carries a badge.

So it is published as **T3 throughout** until someone shows the developers wrote
it. If they did, this page gets stronger and the badges come off - it is a one
link question, not a research project.

WHY IT IS WORTH PUBLISHING ANYWAY
---------------------------------
Because it cross-checks. Three of its four testable claims agree with patch
notes we already hold:

  - 2:1 conversion, any two motes into one of the next rank   -> 21 June note
  - motes upgrade spells                                       -> 29 June note
  - three Void Gems a week from raids                          -> 28 July note,
    which describes "Void-touched Potential" earned up to 3 times per week from
    raid activities through voidlings. Same cadence, same source. Probably the
    same system under a different name, and we do not assert that they are one
    thing because nobody has said so.

And one does not, which is recorded on the page rather than smoothed over: the
21 June note says the conversion construct "can only accept ranks 1-8", while
the guide shows ten ranks.
"""
import os, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

M = json.load(open('assets/motes.json', encoding='utf-8'))
MOTES, COSTS = M['motes'], M['tier_costs']

CSS = '''<style>
.mt{border-collapse:collapse;width:100%;font-size:14px;margin:var(--s-5) 0}
.mt th{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.15em;
  text-transform:uppercase;color:var(--faint);text-align:left;padding:10px 12px;
  border-bottom:1px solid var(--rule2);white-space:nowrap}
.mt td{padding:9px 12px;border-bottom:1px solid var(--rule);vertical-align:baseline}
.mt tr:last-child td{border-bottom:0}
.mt .r{font-family:"IBM Plex Mono",monospace;text-align:right;white-space:nowrap}
.mt .nm{font-family:"Saira Condensed",sans-serif;font-size:15.5px;font-weight:600;color:var(--bone)}
.mt .sx{color:var(--instr)}
.mt .ix{color:var(--ok)}
.costbar{display:flex;flex-wrap:wrap;gap:1px;margin:var(--s-5) 0;
  background:var(--rule);border:1px solid var(--rule);border-radius:var(--r);overflow:hidden}
.costbar div{background:var(--panel);padding:9px 13px;flex:1 1 78px;text-align:center}
.costbar b{display:block;font-family:"IBM Plex Mono",monospace;font-size:10px;
  letter-spacing:.14em;color:var(--faint)}
.costbar span{font-family:"Saira Condensed",sans-serif;font-size:19px;font-weight:600;color:var(--bone)}
</style>'''

rows = "".join(
    f'<tr><td class="r">{m["rank"]}</td><td class="nm">{m["name"]}</td>'
    f'<td class="r sx">{m["spell_xp"]:,}</td><td class="r ix">{m["item_xp"]}</td></tr>'
    for m in MOTES)
costs = "".join(f'<div><b>T{c["tier"]}</b><span>{c["xp"]:,}</span></div>' for c in COSTS)

page = (head("Motes, and what they are worth",
             "The ten mote ranks in EverQuest Legends, what each is worth to a spell and to an "
             "item, and why converting motes upward can cost you item upgrade XP.",
             rel="../", extra=CSS, og="tools", canon="learn/motes")
        + bar("../") + f'''
<main id="main">
<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp;
      <a href="index.html">Learn</a> &nbsp;/&nbsp; Motes</p>
    <h1 class="display">Spells scale doubled.<br><em>Items scale flat.</em></h1>
    <p class="hero-lede">That one difference decides every mote decision you will make. A mote is
      worth <strong>2<sup>rank&minus;1</sup></strong> to a spell and <strong>exactly its rank</strong>
      to an item &mdash; so a rank 10 mote is 512 spell XP and 10 item XP. Everything below follows
      from it.</p>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><div><h2 class="sec">The ten ranks</h2></div></div>
    <table class="mt">
      <thead><tr><th>Rank</th><th>Mote</th><th class="r">Spell XP</th><th class="r">Item XP</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <p class="src">Table <span class="tier t3">T3</span> &mdash; see the sourcing note at the foot
      of this page.</p>

    <h3 class="sec" style="font-size:19px">What each upgrade tier costs</h3>
    <div class="costbar">{costs}</div>
    <p class="lede">The cost curve doubles too, so a spell mote and a spell tier scale together.
      An item does not: its tiers double while its motes stay flat, which is why high tiers get
      expensive in a way spells never do.</p>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><div><h2 class="sec">The rule that saves you the most</h2>
      <p class="lede" style="margin:0">Always spend the lowest mote you are allowed to.</p></div></div>
    <div class="note"><strong>You may use a mote equal to your item&rsquo;s current tier, or one
      rank above it. Nothing else.</strong> A tier 5 item takes rank 5 or rank 6 motes; rank 4 is
      too low to apply and rank 7 too high. <span class="tier t3">T3</span></div>
    <div class="note danger"><strong>Converting upward destroys item XP.</strong> Two motes make
      one of the next rank, and to a spell that is free &mdash; two rank 5s are 32 spell XP and one
      rank 6 is 32. To an <em>item</em> it is a loss: two rank 5s are <strong>10</strong> item XP
      and the rank 6 they become is <strong>6</strong>. <strong>Four item XP gone, every
      time.</strong> Convert for spells; never convert to feed an item.</div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><div><h2 class="sec">Void Gems</h2></div></div>
    <p class="lede">A raid reward, three a week, and each one advances an item a full rank
      outright. Because item tiers double in cost while motes stay flat, a gem is worth least at
      low tiers and most at high ones &mdash; the guide&rsquo;s advice is motes through +7 and gems
      for +8, +9 and +10. <span class="tier t3">T3</span></p>
    <div class="note"><strong>This is probably the token the patch notes call Void-touched
      Potential</strong>, which the 28 July note describes as earned up to three times a week from
      raid activities through voidlings. Same cadence, same source. <strong>Nobody has said the two
      names are one thing, so we do not.</strong></div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><div><h2 class="sec">Where this came from, and one thing that does not fit</h2></div></div>
    <div class="note"><strong>Sourcing.</strong> An infographic, the <em>EverQuest Legends Mote
      &amp; Upgrade Guide</em>, supplied to us on 11 August 2026 and described as released by the
      developers in their Discord. <strong>The artefact itself is branded by a creator</strong>
      &mdash; it carries a YouTube channel name and URL, top and bottom, and no developer mark.
      Developers sharing a creator&rsquo;s work is not the same as writing it, and the difference is
      two tiers, so everything here is badged <span class="tier t3">T3</span>. Show us the
      developers wrote it and the badges come off. The creator is on our
      <a href="../credits.html">credits page</a>.</div>
    <div class="note warn"><strong>One claim does not fit the patch notes.</strong> The guide shows
      ten mote ranks. The 21 June 2026 note says the conversion construct
      &ldquo;can only accept ranks 1-8&rdquo;. Either it was extended since, or ranks 9 and 10
      exist but cannot be reached by converting. <strong>We do not know which, and one attempt to
      convert two rank 8 motes would answer it.</strong></div>
  </div>
</section>
</main>
''' + foot("../"))

open('public/learn/motes.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"learn/motes.html written: {len(MOTES)} ranks, {len(COSTS)} upgrade tiers")
