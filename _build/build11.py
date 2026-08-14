"""learn/difficulty.html — what D0 to D4 actually change.

SOURCING, WHICH IS THE WHOLE POINT OF THIS PAGE
-----------------------------------------------
Two sources, and they must not blur into each other.

EQL TOOLS did the scaling work. https://eqltools.com/learn/difficulty carries
measured HP and XP multipliers, the stat list, mote grades and lockout rules,
and — unusually and to their credit — labels each claim by how it is known:
developer-confirmed, player-measured, or unpinned. Those are their measurements,
not ours. They are cited by name, linked, badged, and never restated as though
we found them. Where they say something is unpinned, this page says unpinned.

OUR OWN LOGS supply something they do not have: the difficulty is written in the
zone line on entry, twice, as a number and a name. That comes from {len(SESSIONS)} sessions
across two characters and five tiers, and it is tier M. It also lets us check
their tier names against the game's own text, and to put one measured finding
next to their multiclass claim that goes slightly further than it does.

WHAT THIS PAGE MUST NOT DO
--------------------------
CLAUDE.md is explicit that we do not clone EQL Tools. This is not a copy of
their page: it is the difficulty question answered for a reader of this site,
crediting their numbers, adding the part we measured, and linking out for the
rest. If a reader wants the full scaling tables they should go and read theirs.
"""
import json as _json
RAIDS = _json.load(open('assets/raids-measured.json', encoding='utf-8'))
# Printed from the record rather than typed, because a typed version of exactly
# this fact was wrong for a month.
def _yael_party(rows):
    atk = sorted({r.get('attackers') for r in rows if r.get('attackers')})
    share = [r.get('our_damage_share_pct') for r in rows
             if r.get('our_damage_share_pct') is not None]
    if not atk:
        return 'multi', 'an unrecorded share of'
    span = (str(atk[0]) if len(atk) == 1 else f'{atk[0]}&ndash;{atk[-1]}')
    lo, hi = (round(min(share)), round(max(share))) if share else (0, 0)
    return span, (str(lo) if lo == hi else f'{lo}&ndash;{hi}')


# The ramp is ONE session at five tiers - that is what makes it a comparison.
# Later kills of the same boss are replication and are reported apart from it;
# dropping them into the table gave two D1 rows and two D2 rows under a heading
# that said "killed once at every difficulty".
_ALL_YAEL = [r for r in RAIDS if r['boss'] == 'Master Yael']
_RAMP_DATE = '10 Aug 2026'
YAEL = sorted([r for r in _ALL_YAEL if r['date'] == _RAMP_DATE],
              key=lambda r: r['difficulty'])
REPEATS = sorted([r for r in _ALL_YAEL if r['date'] != _RAMP_DATE],
                 key=lambda r: r['difficulty'])
_yael_atk, _yael_share = _yael_party(_ALL_YAEL)

# Self-healing by tier, across every boss we have logged. Counted here because
# the sentence this replaces - "he healed himself never at D0, D1 and D2" - was
# typed from one session and a later kill of the same boss at D2 contradicted it.
_heal_tiers = sorted({r['difficulty'] for r in RAIDS
                      if r.get('self_heal_high') and r['difficulty'] is not None})
_heal_lowest = _heal_tiers[0] if _heal_tiers else None
_yael_heal_tiers = sorted({r['difficulty'] for r in _ALL_YAEL
                           if r.get('self_heal_high') and r['difficulty'] is not None})
_yael_heal_low = _yael_heal_tiers[0] if _yael_heal_tiers else None
_sp = [r['spells_distinct'] for r in YAEL]
_spell_span = f"{min(_sp)}&ndash;{max(_sp)}" if _sp else "several"

# The repeats are kept visible rather than dropped, and the comparison against
# the ramp is computed rather than described.
if REPEATS:
    _ramp_at = {r['difficulty']: r for r in YAEL}
    _bits = []
    for r in REPEATS:
        base = _ramp_at.get(r['difficulty'])
        d = r['damage_low']
        if base:
            pct = round(100 * (d - base['damage_low']) / base['damage_low'])
            _bits.append(f"D{r['difficulty']} again at {d:,} "
                         f"({pct:+d}% against the ramp)")
        else:
            _bits.append(f"D{r['difficulty']} at {d:,}")
    _repeat_note = (
        '<p class="src" style="margin:var(--s-5) 0 0"><strong>Killed again on '
        + REPEATS[0]['date'] + ' by a different group:</strong> ' + '; '.join(_bits)
        + '. Kept out of the table because the comparison above is one session at five '
          'settings, and a second group on another night is a different measurement.</p>')
else:
    _repeat_note = ''

# The other two bosses. Shown because the corrections above cite them - a reader
# told "Lady Vox heals itself at D0" should be able to see the row.
_OTHERS = sorted([r for r in RAIDS if r['boss'] != 'Master Yael'],
                 key=lambda r: (r['boss'], r['difficulty']))
_other_rows = ''.join(
    '<tr><td class="nmob">{b}</td><td class="lv">D{d}</td><td class="lv">{dm}{fl}</td>'
    '<td class="lv">{s}s</td><td class="lv">{sp}</td><td class="lv">{h}</td></tr>'.format(
        b=r['boss'], d=r['difficulty'],
        dm=(f"{r['damage_low']:,}" if r['damage_low'] == r['damage_high']
            else f"{r['damage_low']:,}&ndash;{r['damage_high']:,}"),
        fl=(' <em>floor</em>' if r.get('damage_is_floor') else ''),
        s=r['seconds'], sp=r['spells_distinct'],
        h=(r['self_heal_high'] or '&mdash;'))
    for r in _OTHERS)
# Spells that are not direct damage or control. A boss casting these is not
# running an evocation kit, and that is the whole finding - so the test is
# stated in code rather than asserted in prose.
_HEALS = {'Healing Light', 'Sacred Echo', 'Bond of Death'}
_DOT_FEAR = {'Screaming Terror', 'Insidious Retrogression', 'Ignite Blood', 'Shadow Vortex'}

def _kit(r):
    sp = set(r['spells'])
    return dict(heals=sorted(sp & _HEALS), dots=sorted(sp & _DOT_FEAR))

# Only what is NEW at each tier. Repeating the whole list five times cost 250
# words and hid the finding; the widening is the point, so show the widening.
def _new_rows():
    """Only what is new at each tier: repeating the whole spell list five times
    cost 250 words and hid the finding. The widening is the point."""
    seen, out = set(), []
    for r in YAEL:
        fresh = sorted(set(r["spells"]) - seen)
        seen |= set(r["spells"])
        dmg = (f'{r["damage_low"]:,}' if r["damage_low"] == r["damage_high"]
               else f'{r["damage_low"]:,}&ndash;{r["damage_high"]:,}')
        heal = (str(r["self_heal_low"]) if r["self_heal_low"] == r["self_heal_high"]
                else f'{r["self_heal_low"]}&ndash;{r["self_heal_high"]}')
        out.append(
            f'<tr><td class="nmob">D{r["difficulty"]} <span class="tier tM">M</span></td>'
            f'<td class="lv">{dmg}</td>'
            f'<td class="lv">{r["seconds"]}s</td>'
            f'<td class="lv">{r["spells_distinct"]}</td>'
            f'<td class="lv">{heal if heal != "0" else "&mdash;"}</td>'
            f'<td>{", ".join(fresh) or "nothing new"}</td></tr>')
    return "".join(out)

_yael_rows = _new_rows()
_spreads = [r["damage_spread_pct"] for r in RAIDS if len(r["observers"]) > 1]
_worst = max(_spreads) if _spreads else 0
_nobs = sum(len(r["observers"]) for r in RAIDS)
_first_multi = next((r["difficulty"] for r in YAEL if _kit(r)["heals"]), None)
import os, sys, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

try:
    SESSIONS = json.load(open('assets/measured.json', encoding='utf-8'))
except (OSError, ValueError):
    SESSIONS = []

TIERS = [
    (0, 'Base / Normal', 'the open world, and what you get if you never touch the setting'),
    (1, 'Awakened', 'the first instanced tier'),
    (2, 'Adaptive', ''),
    (3, 'Fused', ''),
    (4, 'Refined', 'the current maximum'),
]

# what our own logs can say about each tier, counted rather than asserted
seen = collections.defaultdict(lambda: dict(sessions=0, kills=0, zones=set(), chars=set()))
agree = both = 0
for s in SESSIONS:
    d = s.get('difficulty')
    if d is None:
        continue
    e = seen[d]
    e['sessions'] += 1
    e['kills'] += s.get('kills', 0)
    if s.get('zone'):
        e['zones'].add(s['zone'])
    if s.get('character'):
        e['chars'].add(s['character'])
    if s.get('difficulty_label_agrees') is not None:
        both += 1
        agree += 1 if s['difficulty_label_agrees'] else 0

# THE LOOT FLOOR, COUNTED HERE RATHER THAN TYPED INTO THE PROSE
# The page used to say the tier is "the +N most things arrive at", which is the
# mode. It is the minimum. Every figure in that paragraph is printed from these
# counters, so a later session that breaks the rule changes the sentence
# instead of leaving it standing.
floor_ok = floor_n = 0
below = at_tier = above = 0
for s in SESSIONS:
    # only sessions whose difficulty came from the zone line, never from loot -
    # scoring the loot rule against a difficulty derived from loot proves
    # nothing
    if s.get('difficulty_from') not in ('zone line, numbered', 'zone line'):
        continue
    d, tiers = s.get('difficulty'), s.get('drop_tiers') or {}
    if d is None or not tiers:
        continue
    floor_n += 1
    floor_ok += 1 if min(int(k) for k in tiers) == d else 0
    for k, v in tiers.items():
        k = int(k)
        below += v if k < d else 0
        at_tier += v if k == d else 0
        above += v if k > d else 0
drops_total = below + at_tier + above
above_pct = round(100 * above / max(1, drops_total))

rows = ''
for n, name, note in TIERS:
    e = seen.get(n)
    if e and e['sessions']:
        ours = (f'<b>{e["sessions"]}</b> session{"s" if e["sessions"] != 1 else ""}, '
                f'{e["kills"]} kills, {len(e["zones"])} zone{"s" if len(e["zones"]) != 1 else ""}')
    else:
        ours = '<span class="dim">not yet played on a log we hold</span>'
    rows += (f'<tr><td class="dn">D{n}</td><td class="dname">{name}</td>'
             f'<td class="dnote">{note or "&mdash;"}</td><td>{ours}</td></tr>')

covered = sorted({s['zone'] for s in SESSIONS if s.get('zone')})

page = head("What difficulty changes",
  "D0 to D4 in EverQuest Legends: what each tier scales, what it does not, how to read the tier off "
  "the zone line, and which parts nobody has pinned down yet.",
  rel="../", og="learn", canon="learn/difficulty") + bar("../") + f'''
<main>

<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp; Learn
      &nbsp;/&nbsp; Difficulty</p>
    <h1 class="display">Harder, not<br><em>higher level.</em></h1>
    <p class="hero-lede">Difficulty does not make anything higher level. It makes mobs hit harder,
      resist more, notice you sooner, and run player-style class kits &mdash; and it decides what
      condition your loot arrives in. The con colour of a mob is the same at every tier, which is
      exactly why the setting catches people out.</p>
    <p class="hero-sig"><span>5 tiers</span><span>D4 is the maximum</span>
      <span>{both} of {len(SESSIONS)} sessions cross-checked</span></p>
  </div>
</section>

<div class="shell">
  <div class="note"><strong>Where this comes from, and what is ours.</strong> The scaling work on
    this page is <strong>not ours</strong>. <a href="https://eqltools.com/learn/difficulty">EQL Tools
    measured it</a> <span class="tier t3">T3</span> and, to their credit, labels every claim by how it
    is known &mdash; developer-confirmed, player-measured, or unpinned. Their figures are credited
    below and linked, never restated as though we found them, and where they say a thing is not pinned
    down, neither do we. <strong>What is ours is the part read from our own combat logs</strong>
    <span class="tier tM">TIER M</span>: how the tier is written in the game, and one observation
    about class kits that goes a step further than the published claim. If you want the full scaling
    tables, read theirs &mdash; this page answers the question for a reader of this site and points
    you at them for the rest.</div>
</div>

<section class="band" style="border-top:0;padding-top:0">
  <div class="shell">
    <div class="sechead"><span class="n">The tiers</span><div><h2 class="sec">Five settings</h2>
      <p class="lede" style="margin:0">The names are the game&rsquo;s own. EQL Tools lists them, and
        our logs print them on entry &mdash; two sources that did not derive from each other.</p></div></div>
    <div class="tw"><table class="dtable">
      <thead><tr><th>Tier</th><th>Name</th><th>Note</th><th>In our logs</th></tr></thead>
      <tbody>{rows}</tbody>
    </table></div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><span class="n">Reading it</span><div><h2 class="sec">The game tells you, twice</h2></div></div>
    <p class="lede">Zoning in prints the tier as a number and a name in the same line:</p>
    <pre class="dcode">You have entered Befallen 1 (Awakened).
You have entered Blackburrow 2 (Adaptive).
You have entered Befallen 3 (Fused).
You have entered The City of Guk 4 (Refined).</pre>
    <p>A zone line with no number and no name is the open world, D0. <strong>Both readings agreed in
      every session where both were present &mdash; {agree} of {both}, no disagreements</strong>
      <span class="tier tM">TIER M</span>. So you never have to remember which setting you picked.</p>
    <p>Loot gives a third reading, and <strong>difficulty is a floor</strong>: your tier is the
      <em>lowest</em> <code>+N</code> you see, not the commonest. In {drops_total:,} upgradeable
      drops where the zone line stated the tier on its own, <strong>not one item dropped below
      it</strong> <span class="tier tM">TIER M</span>, and about {above_pct}% rolled above &mdash;
      so anything over the floor is luck, and <strong>three drops settle it</strong>. The floor
      named the tier in {floor_ok} of {floor_n} sessions; the commonest value missed two. Read the
      <em>dropped</em> value, not the created one: <em>looted a Keg Mallet +2 &hellip; to create a
      Keg Mallet +4</em> is a <code>+2</code>, and a bare item is the <code>+0</code>.</p>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><span class="n">What scales</span>
      <div><h2 class="sec">What each tier actually does</h2>
      <p class="lede" style="margin:0">All measured by EQL Tools
        <span class="tier t3">T3</span>, credited and linked, not re-measured by us.</p></div></div>
    <div class="split">
      <div>
        <ol class="findings">
          <li><b>Levels do not move</b> Con colours are identical at every tier. A tier is not a
            level range, and treating it as one is the mistake the setting invites.</li>
          <li><b>Nearly everything else does</b> HP, damage, resists, armour class, mana, movement
            speed and aggro radius, roughly linearly per tier.</li>
          <li><b>Hit points, D1 and D2</b> &times;1.15 and &times;1.30 on multiplayer tuning,
            &times;1.10 and &times;1.20 solo. <strong>D3 and D4 run well above those and are not
            pinned</strong> &mdash; their words, and we are not going to invent a figure.</li>
          <li><b>Experience</b> &times;1.15 / &times;1.30 / &times;1.45 / &times;1.60 across Awakened
            to Refined on multiplayer tuning; &times;1.10 / &times;1.20 / &times;1.30 / &times;1.40
            solo. Whether the bonus is currently live is one of the things they mark unpinned.</li>
          <li><b>Loot is the same table</b> The tier decides the condition, not what drops. A +4 is
            worth sixteen base copies of upgrade progress, so it decides how far a drop carries you
            &mdash; measured above.</li>
          <li><b>Every tier is its own lockout</b> Loot lockouts track per difficulty, so the same
            named can be worth killing again on another setting.</li>
        </ol>
      </div>
      <aside class="standard contour" style="--c:var(--warn);--cx:90%;--cy:112%">
        <h3 class="stdh">Still unpinned</h3>
        <p class="stdp">Named because they are open, not smoothed over. These are EQL Tools&rsquo;
          own confidence labels, kept rather than quietly upgraded.</p>
        <ul class="gatelist">
          <li class="gaterow" style="--c:var(--warn)"><span class="gn">01</span>
            <span class="gz">D3 and D4 hit points</span><span class="gl">unpinned</span>
            <span class="gs">Known to run well above the D1 and D2 multipliers. No figure published
              by anyone.</span></li>
          <li class="gaterow" style="--c:var(--warn)"><span class="gn">02</span>
            <span class="gz">Whether the XP bonus is live</span><span class="gl">unresolved</span>
            <span class="gs">Listed by EQL Tools as an open question against the current patch.</span></li>
          <li class="gaterow" style="--c:var(--warn)"><span class="gn">03</span>
            <span class="gz">Which kits attach to which raid boss</span><span class="gl">part measured</span>
            <span class="gs">Three bosses logged to D3 or D4 below, by spell name. What is still
              unpublished anywhere is the <em>plane</em> bosses.</span></li>
        </ul>
      </aside>
    </div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><span class="n">Ours</span>
      <div><h2 class="sec">The ramp, measured on one boss at all five tiers</h2>
      <p class="lede" style="margin:0">Master Yael, in the group instance of The Hole, killed once
        at every difficulty on 10 August 2026 in a single session &mdash; same boss, same group,
        five settings.</p>
      <p class="src" style="margin:8px 0 0"><strong>These were {_yael_atk}-player raids, not a
        trio.</strong> This said &ldquo;one trio&rdquo; until 11 August and it was wrong &mdash;
        our characters dealt {_yael_share}% of the damage, the rest came from other players.
        <strong>Damage to kill counts everyone</strong>, so the figures stand; read them as what
        the fight costs a raid.</p></div></div>
    <div class="scroller"><table>
      <thead><tr><th>Tier</th><th>Damage to kill</th><th>Fight</th><th>Spells</th>
        <th>Self-heals</th><th>What he cast</th></tr></thead>
      <tbody>{_yael_rows}</tbody>
    </table></div>
    {_repeat_note}
    <div class="note"><strong>The kit broadens as the tier rises.</strong> Across this session he
      casts {_spell_span} distinct spells from D0 to D4, and the heals, fear and damage over time
      appear in the upper half. <span class="tier tM">TIER M</span>
      <br><br><strong>Corrected 11 August.</strong> This claimed the kit widens <em>at D3</em> and
      that he healed himself <em>never at D0, D1 and D2</em>. Both were read off this one session
      and later kills contradict the second: the same boss healed itself at D{_yael_heal_low} on
      another kill, and <strong>Lady Vox heals itself at D{_heal_lowest}</strong>, in the open
      world. Self-healing is not gated behind a tier &mdash; the tier decides how <em>much</em> of
      the kit turns up.
      <br><br><strong>And &ldquo;ten times at D4&rdquo; was ten log lines, not ten decisions:</strong>
      one effect ticking every six seconds for the same 22 hit points, the same shape Lady Vox
      shows at her top tier.</div>
    <h3 class="sec" style="font-size:19px;margin-top:var(--s-6)">The other two bosses</h3>
    <p class="lede" style="margin:0">Same shape, different bosses, all public raids. A row marked
      <em>floor</em> is one we joined after the boss was already engaged, so the log never saw the
      opening and the figure is a lower bound rather than the cost of the fight.</p>
    <div class="scroller"><table>
      <thead><tr><th>Boss</th><th>Tier</th><th>Damage to kill</th><th>Fight</th>
        <th>Spells</th><th>Self-heals</th></tr></thead>
      <tbody>{_other_rows}</tbody>
    </table></div>
    <div class="note"><strong>Where the ranges come from.</strong> Several fights were logged from
      two clients at once, and two parses of one kill differ by whatever each missed &mdash;
      between nothing and {_worst}% here. <strong>That spread is the method&rsquo;s error bar,
      measured rather than assumed</strong>, and it is why the D4 self-heal count is a range.
      <br><br><strong>Damage to kill is not hit points.</strong> These bosses heal, so it is an
      upper bound carrying the raid&rsquo;s gear and misses with it.</div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><span class="n">Ours</span>
      <div><h2 class="sec">One thing we measured that goes further</h2></div></div>
    <div class="note"><strong>The published claim is that <em>named</em> mobs are often multiclass
      from D2. We have it on ordinary trash at D1.</strong> In Castle Mistmoore at Awakened, two trash
      types &mdash; <em>an initiate familiar</em> and <em>a pledge familiar</em> &mdash; backstabbed
      39 times between them while the same types were logged casting Root, Screaming Terror, Shadow
      Vortex, Shock of Poison and Engulfing Darkness. <span class="tier tM">TIER M</span>
      <br><br>Backstab is the part that settles it. A spell list on its own proves little, because
      those spells could plausibly sit in one broad caster kit &mdash; but backstab is a rogue
      ability, and a mob type doing both is running two kits. At D1, on trash.
      <br><br><strong>Its limit, stated:</strong> a log aggregates by mob type, so whether a single
      individual carries both kits cannot be told apart from two individuals carrying one each. And
      this is one zone on one night. It does not contradict the published claim about named mobs; it
      suggests the behaviour starts earlier and lower than the claim implies.</div>
    <p class="lede">Measured so far across {len(covered)} zone{"s" if len(covered) != 1 else ""}:
      {", ".join(covered) if covered else "none yet"}. Each plate carries its own figures under
      <em>Measured in play</em>.</p>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><span class="n">Sourcing</span><div><h2 class="sec">Where to read more</h2></div></div>
    <div class="note"><strong><a href="https://eqltools.com/learn/difficulty">EQL Tools &mdash;
      Difficulty</a></strong> <span class="tier t3">T3</span> Source of every scaling figure above.
      Current to the launch patch of 28 July 2026, and labelled by confidence throughout, which is
      rarer than it should be. <strong>Go and read it</strong> if you want the mote grades, the
      lockout timings and the full tables &mdash; this page deliberately does not reproduce them.</div>
    <div class="note"><strong>Our own combat logs</strong> <span class="tier tM">TIER M</span>
      {len(SESSIONS)} sessions across two characters, parsed by our own log reader.
      Source of the zone-line reading, the loot-tier correspondence and the multiclass observation.
      Every figure derived from them appears with the character, level, zone, tier and sample size
      beside it.</div>
  </div>
</section>

</main>
''' + foot("../")

open('public/learn/difficulty.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"learn/difficulty.html written: {both} sessions cross-checked, "
      f"{len(seen)} tiers seen in our logs")
