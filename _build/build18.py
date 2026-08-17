"""learn/reading-the-plans.html — the caveats, written once instead of thirteen times.

WHY
---
Every survey carried the same three explanations, printed in full on each page:
what the floor plan draws and what it leaves out, what the route line is and is
not, and what the inherited spawn percentages mean. Measured across thirteen
surveys on 11 August 2026, twenty-three sentences appeared on three or more
pages and accounted for 2,841 words — the single largest block of text on the
site, and all of it the same paragraph repeated.

The honesty was right. Printing it thirteen times was the bloat two readers
bounced off. It lives here now, and each survey keeps one line and a link.

This page is deliberately wordy. It is the one place where the long version is
the point.
"""
import os, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
import backstab as _BS
from _partials import head, bar, foot

# Counted from the built surveys rather than typed: it said four when eight
# carry a measured section, and it would have said four after the ninth too.
import glob as _glob
_N_MEAS = sum(1 for _p in _glob.glob('public/dungeons/*.html')
              if 'Measured in play' in open(_p, encoding='utf-8', errors='replace').read())


Z = json.load(open('assets/zones-index.json', encoding='utf-8'))
G = json.load(open('assets/zone-geometry.json', encoding='utf-8'))
NZONES = len(Z)
NGEO = sum(1 for z in Z if z['slug'] in G)

CSS = '''<style>
.rp h2{margin-top:var(--s-7)}
.rp .q{border-left:3px solid var(--instr);padding:2px 0 2px 18px;margin:var(--s-5) 0;
  font-family:"Saira Condensed",sans-serif;font-size:clamp(18px,3.2vw,23px);
  font-weight:500;line-height:1.3;color:var(--bone);max-width:58ch}
.rp .kv{list-style:none;margin:var(--s-5) 0 0;padding:0;display:grid;gap:1px;
  background:var(--rule);border:1px solid var(--rule);border-radius:var(--r);overflow:hidden}
.rp .kv li{background:var(--panel);padding:13px 16px;display:grid;
  grid-template-columns:minmax(0,190px) minmax(0,1fr);gap:6px 20px}
.rp .kv b{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--faint)}
.rp .kv span{color:var(--dim);font-size:14.5px;line-height:1.55}
@media(max-width:640px){.rp .kv li{grid-template-columns:1fr}}
</style>'''


def page():
    return (head("How to read a floor plan",
                 "What the floor plans on the EverQuest Legends dungeon surveys draw, what they "
                 "deliberately leave out, and what the route line is and is not.",
                 rel="../", extra=CSS, og="dungeons", canon="learn/reading-the-plans")
            + bar("../") + f'''
<main>
<section class="hero page">
  <div class="shell rp">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp;
      <a href="index.html">Learn</a> &nbsp;/&nbsp; Reading a floor plan</p>
    <h1 class="display">How to read<br><em>a floor plan.</em></h1>
    <p class="hero-lede">{NGEO} of our {NZONES} surveys carry one. They are not redrawn from
      published maps &mdash; they are computed from the zone&rsquo;s own geometry in the game
      files. That makes them trustworthy in a specific way and useless in a few others, and it
      is worth knowing which is which before you follow one into a dungeon.</p>
  </div>
</section>

<section class="band" style="border-top:0;padding-top:0">
  <div class="shell rp">

    <h2 class="sec">What the line is</h2>
    <p class="lede">A line marks the edge of the walkable floor &mdash; a wall, or a drop.
      Nothing more than that.</p>
    <ul class="kv">
      <li><b>Not marked</b><span>Doors, locks, and one-way drops. A gap in a line is as likely
        to be a ledge you fall off as a doorway you walk through.</span></li>
      <li><b>Not a published map</b><span>It is derived from the game&rsquo;s mesh. It is our own
        computation of where the floor ends, not a copy of anyone&rsquo;s drawing.</span></li>
      <li><b>Walkable floor only</b><span>Surfaces a standing character could stand on. In a zone
        you swim through &mdash; Kedge Keep especially &mdash; large parts of where you can
        actually go have no floor under them, so the plan under-draws the space.</span></li>
      <li><b>Storeys are separated</b><span>Where a zone stacks, each band of height is its own
        layer and the control above the plan isolates one at a time. A flattened map cannot show
        you a room that sits directly above another one.</span></li>
    </ul>

    <h2 class="sec">The check that runs on every coordinate</h2>
    <p class="lede">Under each plan is a line like &ldquo;18 of these 18 positions land on the
      drawn floor&rdquo;. That sentence is doing more work than it looks.</p>
    <p>The coordinates come from published <code>/loc</code> records. The floor comes from the
      game&rsquo;s mesh. <strong>They are two completely independent sources, and both have to be
      right for a point to land on floor.</strong> When the count is short, one of them is wrong
      and the survey says so rather than drawing the point anyway.</p>
    <p>It has already earned its keep: the check caught six impossible positions in Najena that
      the old hand-drawn plots had no way to test, because a hand-drawn plot has nothing to be
      checked against.</p>

    <h2 class="sec">The route line, and what it is not</h2>
    <p class="q">It is an order to take them in, not a path through the zone.</p>
    <p>Where a survey offers a farming route, the line runs from named mob to named mob in a
      sensible order. <strong>It knows nothing about walls, doors, locks or drops.</strong> A
      segment that appears to cross a wall is the drawing being honest about what it is: a
      sequence, drawn straight, not a route anyone walked.</p>
    <p>It starts at the lowest-level named mob as a stand-in for starting near the entrance,
      because the zone line is not recorded for every zone. The distance quoted is straight-line
      travel and will always be shorter than the walk.</p>

    <h2 class="sec">Spawn percentages you will see in the rosters</h2>
    <p>Where a roster carries a percentage, it is inherited from classic EverQuest, where a named
      mob shared its spawn point with a placeholder and the number described how often you got
      the one you wanted.</p>
    <p><strong>The 28 July 2026 patch note removed placeholders from eleven dungeons.</strong>
      In those zones the named mob spawns every cycle, and the inherited percentage describes
      nothing about the zone now. Each survey says in place which case it is in. Where nothing
      has been published either way, it says that instead of guessing.</p>

    <h2 class="sec" id="measured">What a combat log can and cannot tell you</h2>
    <p class="lede">{_N_MEAS} surveys carry figures measured from our own play. They are the strongest
      evidence on the site and they generalise to almost nothing.</p>
    <ul class="kv">
      <li><b>A drop seen once</b><span>is seen once. One session is a sample, not a rate, and no
        drop rate can be read from it. Where a survey says a thing dropped, that is a count.</span></li>
      <li><b>Damage figures</b><span>describe that trio, at that level, against those mobs, on
        that date. A different level or a different trio changes all of them.</span></li>
      <li><b>Resist rates</b><span>depend on the character&rsquo;s own resistances and alternate
        abilities. Treat a spell table as what happened to one build, not as a property of the
        mob. The useful part is the kill order.</span></li>
      <li><b>Absent mobs</b><span>are not missing. A log records what happened, so anything that
        never attacked us and never cast anything does not appear.</span></li>
      <li><b>Spell names</b><span>are printed exactly as the game printed them.</span></li>
      <li><b>Never a combined average</b><span>for a mob that backstabs. Our Mistmoore log has
        familiars at {_BS.damage_phrase()}; one number across both describes neither.</span></li>
    </ul>

    <h2 class="sec">Why there are no invented maps here</h2>
    <p>An image model will draw a convincing dungeon map, with a legend and a scale bar and a
      compass rose, and every spatial relationship in it will be invented. We tested one against
      the zone it claimed to depict: the position it printed for its boss, twice, sat
      <strong>210 units outside the zone&rsquo;s entire extent</strong> and 458 units from any
      geometry at all.</p>
    <p>The archives are on your disk and ours. <strong>We would rather read the map than imagine
      it</strong>, and everything on these plans is read.</p>

  </div>
</section>
</main>
''' + foot("../"))


os.makedirs('public/learn', exist_ok=True)
out = page()
open('public/learn/reading-the-plans.html', 'w', encoding='utf-8', newline='\n').write(out)
print(f"learn/reading-the-plans.html written: the caveats, once instead of {NZONES} times")
