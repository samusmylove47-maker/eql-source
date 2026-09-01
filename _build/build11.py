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

MEASUREMENT IN PLAY supplies something they do not have: the difficulty is
written in the zone line on entry, twice, as a number and a name. It is tier M.
It also lets us check their tier names against the game's own text, and to put
one measured finding next to their multiclass claim that goes slightly further
than it does.

WHAT NEVER REACHES THE PAGE
---------------------------
The play behind a tier M figure. Session counts, dates, kill tallies, attacker
counts, damage shares and character names are all read to derive a finding and
none of them print: the badge is the claim that we measured it, and the finding
is what a reader needs. Findings are still DERIVED from the data at build time,
never typed — a generic sentence is not a licence to remember a number.

WHAT THIS PAGE MUST NOT DO
--------------------------
CLAUDE.md is explicit that we do not clone EQL Tools. This is not a copy of
their page: it is the difficulty question answered for a reader of this site,
crediting their numbers, adding the part we measured, and linking out for the
rest. If a reader wants the full scaling tables they should go and read theirs.
"""
import json as _json
RAIDS = _json.load(open('assets/raids-measured.json', encoding='utf-8'))

# THE ZONE THIS FINDING COMES FROM HAS SINCE BEEN REVAMPED.
#
# The trash-multiclass measurement is Castle Mistmoore's, and Castle Mistmoore
# changed on 18 August 2026. The finding is not withdrawn - it was true of the
# zone it was taken in - but a reader meeting it here has no way to know it
# predates the revamp unless this page says so.
#
# Read from assets/zones-index.json so the survey and this page cannot drift:
# one date, one edit, both pages move.
_ZI = _json.load(open('assets/zones-index.json', encoding='utf-8'))
_MM = next((z for z in _ZI if z.get('slug') == 'mistmoore'), {})
_REVAMP = (('<strong>Measured before the ' + _MM['revamped'] + ' revamp.</strong> '
            'The zone has changed since; the reading stands for the zone as it was.')
           if _MM.get('revamped') else '')

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

# The repeats are kept as a statement about the measurement, not as a second
# night's scoreboard: what a reader needs is that the same boss at the same tier
# does not reproduce, and by how far. Dates, groups and per-run totals are read
# to compute that and are not printed.
_bits = []
if REPEATS:
    _ramp_at = {r['difficulty']: r for r in YAEL}
    for r in REPEATS:
        base = _ramp_at.get(r['difficulty'])
        if base and base['damage_low']:
            pct = round(100 * (r['damage_low'] - base['damage_low']) / base['damage_low'])
            _bits.append(f"D{r['difficulty']} {pct:+d}%")
_repeat_note = (
    '<p class="src" style="margin:var(--s-5) 0 0"><strong>The same boss measured again at the '
    'same tiers does not reproduce:</strong> ' + ', '.join(_bits) + ' against the ramp above. '
    'Damage to kill is what a fight cost, not a constant &mdash; raid size, gear and misses all '
    'count towards it.</p>') if _bits else ''

# The other two bosses. Shown because the corrections above cite them - a reader
# told "Lady Vox heals itself at D0" should be able to see the row.
# A fight whose difficulty NOTHING resolved sorts last and prints as unresolved.
#
# The Eye of Veeshan, killed 15 August 2026, is the first: the Plane of Sky
# carries no numbered zone line and the kill dropped nothing that carried an
# independent tier, so neither of the two readings CLAUDE.md describes fired.
# That is a real state and the rules are explicit about it - when the loot and
# the zone line cannot agree, the difficulty is unresolved and the page says so.
#
# Sorting on it crashed the build outright, which is the better failure. The
# temptation is to default the tier to 0 and lose the distinction between
# "measured at base" and "we do not know"; a boss at an unknown tier is exactly
# the row a reader must not misread as a D0 measurement.
_OTHERS = sorted([r for r in RAIDS if r['boss'] != 'Master Yael'],
                 key=lambda r: (r['boss'], -1 if r['difficulty'] is None
                                else r['difficulty']))

# ONE ROW PER BOSS PER TIER, NOT ONE ROW PER KILL.
#
# A row per kill made the table a record of how many times each boss had been
# killed at each setting, which is a fact about a player's play and not about
# the game. It also read badly: twelve rows of the same wasp at D0 said nothing
# the first row had not.
#
# Collapsing it needs the rule CLAUDE.md already sets - trust the fullest view
# of a boss at a tier and treat the rest as lower bounds. So a group with any
# complete view drops its partial ones; a group with nothing but partial views
# keeps the strongest of them, which is the highest, and stays marked a floor.
def _fullest(rows):
    full = [r for r in rows if not r.get('damage_is_floor')]
    if full:
        return full, False
    return [max(rows, key=lambda r: r['damage_high'])], True


def _span(lo, hi, fmt='{:,}'):
    return fmt.format(lo) if lo == hi else f'{fmt.format(lo)}&ndash;{fmt.format(hi)}'


_groups = []
for r in _OTHERS:
    if _groups and _groups[-1][0] == (r['boss'], r['difficulty']):
        _groups[-1][1].append(r)
    else:
        _groups.append(((r['boss'], r['difficulty']), [r]))

_other_rows = ''
for (boss, diff), rows in _groups:
    use, is_floor = _fullest(rows)
    dmg = _span(min(r['damage_low'] for r in use), max(r['damage_high'] for r in use))
    secs = _span(min(r['seconds'] for r in use), max(r['seconds'] for r in use), '{}')
    heal_hi = max(r['self_heal_high'] for r in use)
    heal = _span(min(r['self_heal_low'] for r in use), heal_hi, '{}') if heal_hi else '&mdash;'
    _other_rows += (
        f'<tr><td class="nmob">{boss}</td><td class="lv">'
        + ('D%d' % diff if diff is not None
           else '<span class="unk" title="No numbered zone line, and nothing dropped carrying '
                'an independent tier">not resolved</span>')
        + f'</td><td class="lv">{dmg}{" <em>floor</em>" if is_floor else ""}</td>'
        + f'<td class="lv">{secs}s</td>'
        + f'<td class="lv">{max(r["spells_distinct"] for r in use)}</td>'
        + f'<td class="lv">{heal}</td></tr>')

# Which of the high-tier bosses the aside names. A count of what we have killed
# is a record of our play, so the aside names the bosses and leaves the tally.
_PLANES = sorted({r['boss'].split(',')[0] for r in RAIDS if r['difficulty'] in (3, 4)
                  and r['boss'].startswith(('Cazic-Thule', 'Innoruuk'))})

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
# The error bar: where one kill was recorded twice, how far the two records
# disagree. It describes the method, not the run, so it prints.
_spreads = [r["damage_spread_pct"] for r in RAIDS if len(r["observers"]) > 1]
_worst = max(_spreads) if _spreads else 0
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
    # THE GAME'S WORD FOR THIS TIER IS "NORMAL". "Base" is ours.
    #
    # Printing both as if they were alternatives put our own inferred label
    # beside the game's actual name and made them look equivalent. They are
    # not: searching every `You have entered` line in every staged log for
    # `0 (`, `Base` or `Normal` returns ZERO matches, so the zone line never
    # names this tier at all. The instance invite does, and it says Normal.
    # That is the whole reason D0 has a name, and it is why the note now
    # says where the name comes from rather than offering a choice of two.
    (0, 'Normal', 'the open world, and any instance run at base. The zone line never names this tier; the instance invite does, and that is where the name comes from'),
    (1, 'Awakened', 'the first instanced tier'),
    (2, 'Adaptive', ''),
    (3, 'Fused', ''),
    (4, 'Refined', 'the current maximum'),
]

# WHICH TIERS HAVE BEEN MEASURED, not how much they were played.
# The counters still run, because whether a tier is verified has to be derived
# rather than asserted - but what reaches the page is the verdict, and the tier
# M badge beside it already says we measured it. Session and kill tallies are a
# record of one player's evening and belong to that player, not to a reference
# page.
seen = collections.defaultdict(lambda: dict(sessions=0, zones=set()))
agree = both = 0
for s in SESSIONS:
    d = s.get('difficulty')
    if d is None:
        continue
    e = seen[d]
    e['sessions'] += 1
    if s.get('zone'):
        e['zones'].add(s['zone'])
    if s.get('difficulty_label_agrees') is not None:
        both += 1
        agree += 1 if s['difficulty_label_agrees'] else 0
# The cross-check prints as a verdict, never as a score line.
label_check = ('have never disagreed where the line carried both' if both and agree == both
               else 'do not always agree, so read the number')

# THE LOOT FLOOR, COUNTED HERE RATHER THAN TYPED INTO THE PROSE
# The page used to say the tier is "the +N most things arrive at", which is the
# mode. It is the minimum. Every figure in that paragraph is printed from these
# counters, so a later session that breaks the rule changes the sentence
# instead of leaving it standing.
floor_ok = floor_n = modal_ok = 0
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
    # The modal reading, scored over the SAME sessions as the floor. "The
    # commonest value missed two" was typed beside a computed floor figure and
    # was wrong: it misses three.
    modal_ok += 1 if max(tiers.items(), key=lambda kv: kv[1])[0] == str(d) else 0
    for k, v in tiers.items():
        k = int(k)
        below += v if k < d else 0
        at_tier += v if k == d else 0
        above += v if k > d else 0
drops_total = below + at_tier + above
above_pct = round(100 * above / max(1, drops_total))
# Two findings, each stated only if the data still supports it.
below_line = ('<strong>No upgradeable drop has been seen below the tier of the zone it dropped '
              'in</strong> <span class="tier tM">TIER M</span>, and about '
              f'{above_pct}% roll above' if not below else
              '<strong>A drop can land below the tier of the zone it dropped in</strong> '
              f'<span class="tier tM">TIER M</span>, and about {above_pct}% roll above')
floor_clause = ('The floor names the tier where the commonest value does not always. '
                if modal_ok < floor_ok else '')

rows = ''
for n, name, note in TIERS:
    e = seen.get(n)
    ours = ('<span class="tier tM">M</span> verified in play' if e and e['sessions']
            else '<span class="dim">not verified here yet</span>')
    rows += (f'<tr><td class="dn">D{n}</td><td class="dname">{name}</td>'
             f'<td class="dnote">{note or "&mdash;"}</td><td>{ours}</td></tr>')

covered = sorted({s['zone'] for s in SESSIONS if s.get('zone')})
# WHETHER A MEASURED ZONE HAS A SURVEY. The page used to list every zone we have
# played in, which is a record of play rather than a fact about the game. The
# coverage gap behind the list is real and stays, stated as a gap and derived
# from the same data.
import re as _re
_ZT = {z['title'].lower() for z in json.load(open('assets/zones-index.json', encoding='utf-8'))}
_ALIAS = {'the ruins of old guk': 'lower guk', 'the ruins of old paineel': 'the hole',
          'the castle of mistmoore': 'castle mistmoore'}


def _has_survey(zone):
    k = _re.sub(r'\s+\d+\s*\(.*?\)$', '', zone or '').replace(' - Group', '').strip().lower()
    return _ALIAS.get(k, k) in _ZT


_no_survey = sum(1 for z in covered if not _has_survey(z))

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
      <span>The zone line names yours</span></p>
  </div>
</section>

<div class="shell">
  <div class="note"><strong>Where this comes from.</strong> The scaling work on
    this page is <strong>not ours</strong>. <a href="https://eqltools.com/learn/difficulty">EQL Tools
    measured it</a> <span class="tier t3">T3</span> and, to their credit, labels every claim by how it
    is known &mdash; developer-confirmed, player-measured, or unpinned. Their figures are credited
    below and linked, never restated as though we found them, and where they say a thing is not pinned
    down, neither do we. <strong>The rest is measured in play</strong>
    <span class="tier tM">TIER M</span>: how the tier is written in the game, and one observation
    about class kits that goes a step further than the published claim. If you want the full scaling
    tables, read theirs &mdash; this page answers the question for a reader of this site and points
    you at them for the rest.</div>
</div>

<section class="band" style="border-top:0;padding-top:0">
  <div class="shell">
    <div class="sechead"><span class="n">The tiers</span><div><h2 class="sec">Five settings</h2>
      <p class="lede" style="margin:0">The names are the game&rsquo;s own. EQL Tools lists them, and
        the game prints them on entry &mdash; two sources that did not derive from each other.</p></div></div>
    <div class="tw"><table class="dtable">
      <thead><tr><th>Tier</th><th>Name</th><th>Note</th><th>Measured</th></tr></thead>
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
    <p>A zone line with no number and no name is <strong>base difficulty</strong> &mdash; the open
      world, or an instance run at base. <strong>The number and the name {label_check}</strong>
      <span class="tier tM">TIER M</span>. So you never have to remember which setting you picked.</p>
    <p>Loot gives a third reading, and <strong>difficulty is a floor</strong>: your tier is the
      <em>lowest</em> <code>+N</code> you see, not the commonest. {below_line} &mdash;
      so anything over the floor is luck, and <strong>three drops settle it</strong>.
      {floor_clause}Read the
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
            <span class="gs">Measured at D3 and D4 in the table below, {" and ".join(_PLANES)}
              among them. <em>Hit points</em> remain unpinned.</span></li>
        </ul>
      </aside>
    </div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><span class="n">Measured</span>
      <div><h2 class="sec">The ramp, measured on one boss at all five tiers</h2>
      <p class="lede" style="margin:0">Master Yael, in the group instance of The Hole, measured at
        every difficulty &mdash; same boss, same group, five settings, so the tier is the only
        thing that changed between the rows.</p>
      <p class="src" style="margin:8px 0 0"><strong>Damage to kill counts every attacker</strong>,
        so read these as what the fight costs a raid rather than what one party deals.</p></div></div>
    <!-- .tw, not .scroller. `.scroller` is real but only inside the thirteen
         self-contained survey pages, which carry their own inline stylesheet
         and define it there. This page loads the SHARED site.css, which has
         never defined it - so the wrapper resolved to overflow:visible, the
         table pushed the document 4px past 390, and it was the only viewport
         overflow on the site: 717 pages, one finding. `.tw` is the shared
         stylesheet's overflow-x:auto wrapper and sixteen pages already use it.
         Borrowing a class across a stylesheet boundary fails silently, because
         an undefined class is not an error in CSS. -->
    <div class="tw"><table>
      <thead><tr><th>Tier</th><th>Damage to kill</th><th>Fight</th><th>Spells</th>
        <th>Self-heals</th><th>What he cast</th></tr></thead>
      <tbody>{_yael_rows}</tbody>
    </table></div>
    {_repeat_note}
    <div class="note"><strong>The kit broadens as the tier rises.</strong> From D0 to D4 he casts
      {_spell_span} distinct spells, and the heals, fear and damage over time appear in the upper
      half. <span class="tier tM">TIER M</span>
      <br><br><strong>Self-healing is not gated behind a tier.</strong> This boss heals itself at
      D{_yael_heal_low}, and Lady Vox at D{_heal_lowest}, the lowest there is. What the tier decides
      is how <em>much</em> of the kit turns up.
      <br><br><strong>Read a self-heal count as events, not decisions.</strong> A run of them at
      the top tier is one effect ticking every six seconds for the same 22 hit points &mdash; the
      same shape Lady Vox shows at hers.</div>
    <h3 class="sec" style="font-size:19px;margin-top:var(--s-6)">The other bosses</h3>
    <p class="lede" style="margin:0">Same shape, different bosses. <strong>One row per boss per
      tier, taking the fullest view of each</strong>, so a range is how far two measurements of the
      same fight sat apart. Most were measured in a group instance rather than the open zone. A row
      marked <em>floor</em> was measured from part-way into the fight, so it is a lower bound
      rather than the cost of the fight.</p>
    <div class="tw"><table>
      <thead><tr><th>Boss</th><th>Tier</th><th>Damage to kill</th><th>Fight</th>
        <th>Spells</th><th>Self-heals</th></tr></thead>
      <tbody>{_other_rows}</tbody>
    </table></div>
    <div class="note"><strong>Where the ranges come from.</strong> One view of a fight witnesses
      only part of it, so two records of the same kill differ by whatever each missed &mdash;
      between nothing and {_worst}% here. <strong>That spread is the method&rsquo;s error bar,
      measured rather than assumed</strong>, and it is why some counts print as a range. A thin
      view reads low, never high, which is why a <em>floor</em> row is a lower bound.
      <br><br><strong>Damage to kill is not hit points.</strong> These bosses heal, so it is an
      upper bound carrying the raid&rsquo;s gear and misses with it.</div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><span class="n">Measured</span>
      <div><h2 class="sec">One measurement that goes further</h2></div></div>
    <div class="note"><strong>The published claim is that <em>named</em> mobs are often multiclass
      from D2. It is on ordinary trash at D1.</strong> In Castle Mistmoore at Awakened, two trash
      types &mdash; <em>an initiate familiar</em> and <em>a pledge familiar</em> &mdash; backstab,
      and the same types cast Root, Screaming Terror, Shadow Vortex, Shock of Poison and Engulfing
      Darkness. <span class="tier tM">TIER M</span>
      <br><br>Backstab is the part that settles it. A spell list on its own proves little, because
      those spells could plausibly sit in one broad caster kit &mdash; but backstab is a rogue
      ability, and a mob type doing both is running two kits. At D1, on trash.
      <br><br><strong>Its limit, stated:</strong> the measurement aggregates by mob type, so whether
      a single individual carries both kits cannot be told apart from two individuals carrying one
      each. It is one zone at one tier. It does not contradict the published claim about named mobs;
      it suggests the behaviour starts earlier and lower than the claim implies.
      <br><br>{_REVAMP}</div>
    <p class="lede"><strong>Where a zone has a survey, its measured figures are under
      <em>Measured in play</em>.</strong>{" Not every zone measured this way has a survey here." if _no_survey else ""}</p>
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
    <div class="note"><strong>Measured in play</strong> <span class="tier tM">TIER M</span>
      Parsed from combat logs. Source of the zone-line reading, the loot-tier
      correspondence and the multiclass observation. A figure derived this way carries the tier M
      badge and names the zone and tier it was measured at; the play behind it is not published.</div>
  </div>
</section>

</main>
''' + foot("../")

open('public/learn/difficulty.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"learn/difficulty.html written: {len(seen)} tiers verified in play")
