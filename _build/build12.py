"""learn/deity.html — the third permanent choice, and how permanent it isn't.

WHY THIS PAGE EXISTS
--------------------
Race, primary class and deity all lock at level 11. The site already ships a
calculator for the first two. Deity is the third and the least covered anywhere:
eqlwiki's Deity page is a stub with no text, its Category:Deity has names and no
articles, and its starting faction standings carry a cleanup banner admitting
inaccuracies specific to Legends.

TWO THINGS THIS PAGE DOES THAT NOBODY ELSE DOES
-----------------------------------------------
1. It says the lock is reversible and what that costs. The Producer's Letter of
   8 July 2026 prices a Deity Unlock Token at 500 IR, and 500 IR is $4.99. That
   is tier 1, from the publisher, and it changes the decision completely — most
   guides present the choice as permanent and stop there.

2. It relates the two published positions on agnostic accurately. An earlier
   version of the backlog said they contradict each other and that saying so was
   our adjudication remit. Both were read in full: they do not contradict. One
   is a claim about risk, the other names a benefit and a cost in one sentence.
   Writing that up as a disagreement would have invented one. What is true is
   narrower and more useful — the wiki's advice omits a cost, on a choice that
   cannot be retaken for free.

SOURCING
--------
T1  Producer's Letter, 8 Jul 2026 — token prices, IR pricing.
T5  eqlwiki Starting Faction Standings, last edited 15 Jun 2026 — six weeks BEFORE
    EverQuest Legends launched on 28 July 2026, so it fails the provenance test in
    CLAUDE.md and is a Project 1999 import however structured it looks — the standings
    themselves, quoted with its own cleanup banner and its TBA holes NAMED. The
    holes are the point: a reader planning around Rivervale or Kelethin needs to
    know the data is absent, not assume silence means neutral.
T3  eqlwiki Newbie Guide (7 Aug 2026, WIP) and everquestguides.com New Player
    FAQ (3 Jul, updated 24 Jul 2026) — the agnostic advice.
T4  "Best value is Bristlebane and Solusek Ro" — explicitly player consensus,
    single source, badged as such and not endorsed.
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot


def esc_join(items):
    """Comma list with a final 'and', so prose reads as prose."""
    if len(items) == 1:
        return items[0]
    return ', '.join(items[:-1]) + ' and ' + items[-1]

# Deities as listed on the eqlwiki starting-faction page, read 8 Aug 2026.
DEITIES = ["Bertoxxulous", "Bristlebane", "Cazic Thule", "Innoruuk", "Prexus",
           "Quellious", "Rallos Zek", "Solusek Ro", "The Tribunal", "Tunare"]

# Places that page marks TBA. Named rather than smoothed over.
HOLES = ["High Keep", "Rivervale", "Kelethin", "Cabilis", "most Velious factions"]

TOKENS = [("Deity", "500 IR", "about $4.99"),
          ("Race", "1,000 IR", "about $9.98"),
          ("Primary class", "1,500 IR", "about $14.97")]

# Ratios derived from TOKENS rather than typed. The prose read "a third of what
# it costs to change your race, a fifth of your primary class" beside a table
# giving 500 / 1,000 / 1,500 IR — a half and a third. Both figures were wrong,
# on the page whose whole argument is that the three choices are priced
# differently.
_IR = {name: int(cost.split()[0].replace(',', '')) for name, cost, _ in TOKENS}
_FRAC = {2: 'half', 3: 'a third', 4: 'a quarter', 5: 'a fifth', 6: 'a sixth'}


def _ratio(bigger):
    n = _IR[bigger] / _IR['Deity']
    return _FRAC.get(round(n), f'1/{n:g}') if abs(n - round(n)) < 1e-6 else f'{1/n:.2f} of'



trows = ''.join(
    f'<tr><td class="dname">{what}</td><td class="dn">{ir}</td><td class="dnote">{usd}</td></tr>'
    for what, ir, usd in TOKENS)

page = head("Deity, and the level 11 lock",
  "Deity locks at level 11 in EverQuest Legends alongside race and primary class — and unlocks again "
  "for 500 Iridium. What the choice costs, what the published advice leaves out, and where the "
  "faction data simply stops.",
  rel="../", og="learn", canon="learn/deity") + bar("../") + f'''
<main id="main">

<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp; Learn
      &nbsp;/&nbsp; Deity</p>
    <h1 class="display">Permanent,<br><em>until you spend $4.99.</em></h1>
    <p class="hero-lede">Deity locks at level 11 with your race and primary class, and almost every
      guide stops there. It should not. The publisher sells a token that unlocks it again, and it is
      the cheapest of the three by a wide margin &mdash; which turns the most agonised-over decision
      in character creation into the least expensive one to get wrong.</p>
    <p class="hero-sig"><span>Locks at 11</span><span>500 IR to undo</span>
      <span>{len(DEITIES)} deities</span><span>Plus agnostic</span></p>
  </div>
</section>

<section class="band" style="border-top:0;padding-top:0">
  <div class="shell">
    <div class="sechead"><span class="n">The fact</span>
      <div><h2 class="sec">The lock is reversible, and priced</h2>
      <p class="lede" style="margin:0">From the publisher, in the Producer&rsquo;s Letter of 8 July
        2026. This is the part that changes the decision.</p></div></div>
    <div class="tw"><table class="dtable">
      <thead><tr><th>Unlock token</th><th>Cost</th><th>Roughly</th></tr></thead>
      <tbody>{trows}</tbody>
    </table></div>
    <p>Iridium sells at 500 IR for $4.99, so a deity change costs about five dollars &mdash;
      <strong>{_ratio("Race")} what it costs to change your race, {_ratio("Primary class")} of
      your primary class</strong>.
      The three choices lock together at level 11 and are usually discussed as though they carry the
      same weight. They do not.</p>
    <div class="note"><strong>What that does and does not mean.</strong> The prices are official
      <span class="tier t1">T1</span> and current to 8 July 2026. What the letter does not say is
      whether changing deity re-runs your starting faction adjustments or leaves standings where your
      first choice put them. <strong>Nobody has published an answer</strong>, and it matters: if
      standings do not follow the change, a token buys the label and not the consequences. Treat the
      token as reversing the choice, not necessarily its history.</div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><span class="n">Agnostic</span>
      <div><h2 class="sec">The advice, and what it leaves out</h2></div></div>
    <div class="split">
      <div>
        <p class="lede">Two guides cover this. They are usually cited against each other. Read in
          full, <strong>they do not disagree</strong> &mdash; one simply says less than the other.</p>
        <blockquote class="quote">&ldquo;If your class allows, choosing Agnostic is always a safe
          bet.&rdquo;
          <cite>eqlwiki Newbie Guide, last edited 7 August 2026. Carries a work-in-progress banner.
            <span class="tier t3">T3</span></cite></blockquote>
        <blockquote class="quote">&ldquo;It dodges the enemies a deity makes and locks you out of
          every deity-specific item and faction perk.&rdquo;
          <cite>everquestguides.com, New Player FAQ, 3 July 2026, updated 24 July 2026.
            <span class="tier t3">T3</span></cite></blockquote>
        <p>The first is a claim about <em>risk</em>. The second names a benefit and a cost in the
          same breath, and nowhere says agnostic is unsafe. <strong>Both are true.</strong> Agnostic
          is the low-risk choice, and low risk is paid for in items and perks you cannot reach.</p>
        <p>So the useful correction is not that someone is wrong. It is that
          <strong>&ldquo;always a safe bet&rdquo; is advice with the price left off</strong>, offered
          for a decision that locks at level 11. Safe and free are different things, and on a
          permanent choice the difference is the whole question.</p>
      </div>
      <aside class="standard contour" style="--c:var(--instr);--cx:88%;--cy:112%">
        <h3 class="stdh">Reading it straight</h3>
        <p class="stdp">Agnostic buys you fewer enemies and costs you the deity-gated content. Which
          way that trades depends on things nobody has measured.</p>
        <ul class="gatelist">
          <li class="gaterow" style="--c:var(--instr)"><span class="gn">01</span>
            <span class="gz">How much content is deity-gated</span><span class="gl">unpublished</span>
            <span class="gs">No list of deity-specific items or quests exists on any source we
              have checked. Without it, the cost of agnostic cannot be sized.</span></li>
          <li class="gaterow" style="--c:var(--instr)"><span class="gn">02</span>
            <span class="gz">Whether a token restores faction</span><span class="gl">unstated</span>
            <span class="gs">The Producer&rsquo;s Letter prices the token and says nothing about
              standings.</span></li>
          <li class="gaterow" style="--c:var(--warn)"><span class="gn">03</span>
            <span class="gz">&ldquo;Best value: Bristlebane, Solusek Ro&rdquo;</span>
            <span class="gl">player consensus</span>
            <span class="gs">One source, describing what players settle on rather than anything
              measured. <span class="tier t4">T4</span> Recorded because it is what is out there,
              not because we can support it.</span></li>
        </ul>
      </aside>
    </div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><span class="n">Faction</span>
      <div><h2 class="sec">Where the data stops</h2>
      <p class="lede" style="margin:0">Starting standings come from eqlwiki
        <span class="tier t2">T2</span>, last edited 15 June 2026. It covers
        {len(DEITIES)} deities plus agnostic across nineteen starting cities.</p></div></div>
    <div class="note warn"><strong>That page carries its own cleanup banner, and we are repeating it
      rather than quietly relying on the table underneath:</strong> &ldquo;This page requires cleanup
      or revision. It may contain incomplete information, inaccuracies specific to EverQuest Legends,
      or details from a different era or Live revamp that do not apply to EQL.&rdquo;
      <br><br><strong>It is marked TBA at {esc_join(HOLES)}.</strong> Those are holes, not zeroes. If
      you are planning around any of them, the standing is <em>unknown</em> &mdash; do not read the
      blank as neutral. Naming them is the most useful thing this page can do with that source.</div>
    <p>The deities it covers: {esc_join(DEITIES)}, and agnostic. eqlwiki&rsquo;s own
      <em>Deity</em> page is a redirect stub with no text, and its deity category lists names with no
      articles behind them, so the standings table is effectively the only structured deity data
      published anywhere.</p>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><span class="n">Sourcing</span><div><h2 class="sec">Where this came from</h2></div></div>
    <div class="note"><strong><a href="https://www.everquestlegends.com/news/eqlegends-producers-letter-july-2026">Producer&rsquo;s
      Letter, 8 July 2026</a></strong> <span class="tier t1">T1</span> Token prices and Iridium
      pricing. Official and dated.</div>
    <div class="note"><strong><a href="https://eqlwiki.com/Starting_Faction_Standings">eqlwiki
      &mdash; Starting Faction Standings</a></strong> <span class="tier t5">T5</span> Last edited
      15 June 2026. Source of the standings, its cleanup banner and its TBA holes, all quoted rather
      than absorbed.</div>
    <div class="note"><strong><a href="https://eqlwiki.com/Newbie_Guide">eqlwiki &mdash; Newbie
      Guide</a></strong> <span class="tier t3">T3</span> Last edited 7 August 2026, work in progress.
      Source of the &ldquo;safe bet&rdquo; line.</div>
    <div class="note"><strong><a href="https://www.everquestguides.com/everquest-articles/everquest-legends-the-new-player-faq/">everquestguides.com
      &mdash; New Player FAQ</a></strong> <span class="tier t3">T3</span> 3 July 2026, updated 24
      July 2026. Source of the cost of agnostic, of independent corroboration that a deity token
      exists, and of the Bristlebane and Solusek Ro ranking &mdash; which it attributes to players
      rather than to measurement, so it is carried here as <span class="tier t4">T4</span>.</div>
  </div>
</section>

</main>
''' + foot("../")

open('public/learn/deity.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"learn/deity.html written: {len(DEITIES)} deities, {len(HOLES)} data holes named")
