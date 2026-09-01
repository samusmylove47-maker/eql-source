"""archive/index.html — the original survey plates, kept whole.

WHY THIS PAGE EXISTS
--------------------
The site began as ten hand-built coordinate plots. Every named mob's `/loc` was
read off the wiki, transformed into page space, and drawn by hand into an SVG
with a numbered legend beside it. They were the first thing this project made
and for a while they were the whole of it — the pages were called plates because
that is what they were.

Then `_build/geometry.py` learned to read the game's own `.s3d` mesh archives,
and the floor plans that came out of it are better in every direction that
matters: the walls are the game's walls rather than an outline drawn around some
dots, the storeys separate, the named filter by storey, and every coordinate is
checked against walkable floor at build time. Six impossible Najena positions
were caught that way and withheld. The hand plots could not have caught them,
because the hand plots had nothing to check against.

So the plates were retired from the guides on 10 August 2026. They are not
deleted, and this is not sentiment: they are the record of how the survey was
done before it could be done properly, and a reader who wants to know whether
we improved or merely changed can compare them here against the live floor plans.

The blocks are stored verbatim in assets/archive-plates.json, exactly as they
last shipped. Nothing here is re-rendered or tidied.
"""
import os, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

Z = json.load(open('assets/zones-index.json', encoding='utf-8'))
BY = {z['slug']: z for z in Z}
ARCH = json.load(open('assets/archive-plates.json', encoding='utf-8'))

order = sorted(ARCH, key=lambda s: BY[s]['plate'])

# Ten drawings at their natural size make a long page. A jump list is
# navigation, not restyling — the drawings themselves stay untouched.
jump = ('<nav class="arch-jump"><span>Jump to</span>' + ''.join(
    f'<a href="#plate-{slug}">{BY[slug]["plate"]:02d} {BY[slug]["title"]}</a>'
    for slug in order) + '</nav>')

blocks = ''.join(
    f'''
  <article class="arch" id="plate-{slug}" style="--c:{BY[slug]['accent']}">
    <div class="arch-head">
      <span class="arch-n">{BY[slug]['plate']:02d}</span>
      <div>
        <h2>{BY[slug]['title']}</h2>
        <p class="arch-meta">Plate {BY[slug]['plate']:02d} &middot; retired 10 Aug 2026 &middot;
          <a href="../dungeons/{slug}">the survey that replaced it &rarr;</a></p>
      </div>
    </div>
    {ARCH[slug]}
  </article>''' for slug in order)

CSS = '''<style>
.arch-jump{display:flex;flex-wrap:wrap;gap:7px;align-items:center;margin:22px 0 0}
.arch-jump span{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--faint);margin-right:4px}
.arch-jump a{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--dim);
  border:1px solid var(--line);border-radius:3px;padding:4px 9px;text-decoration:none}
.arch-jump a:hover{color:var(--ink);border-color:var(--dim)}
.arch{border-top:1px solid var(--line);padding:30px 0 6px}
.arch-head{display:flex;gap:16px;align-items:flex-start;margin:0 0 6px}
.arch-n{font-family:"IBM Plex Mono",monospace;font-size:34px;line-height:1;color:var(--c-t);
  opacity:.65;font-weight:500}
.arch-head h2{margin:0;font-family:"Saira Condensed",sans-serif;font-weight:600;
  text-transform:uppercase;letter-spacing:.02em;font-size:26px;color:var(--ink)}
.arch-meta{margin:3px 0 0;font-family:"IBM Plex Mono",monospace;font-size:11.5px;
  letter-spacing:.08em;text-transform:uppercase;color:var(--faint)}
.arch-meta a{color:var(--c-t)}
/* The archived blocks carry the plate markup as it last shipped. It is not
   restyled — a restyled archive is not an archive. */
.arch section{border:0;padding:0}
.arch h2 .num{display:none}
.arch svg{max-width:100%;height:auto;display:block;border:1px solid var(--line);
  border-radius:4px;background:var(--surface-1)}
.arch .legend ol{list-style:none;margin:14px 0 0;padding:0;display:grid;
  grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:5px}
.arch .legend li{display:grid;grid-template-columns:26px 1fr auto;gap:8px;align-items:baseline;
  font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--dim)}
/* Lifted at the point of use: two of the ten accents fail 4.5:1 as 12px
   text on this ground. The accent itself is never altered — see CLAUDE.md. */
.arch .legend .n{color:var(--c-t)}
.arch .legend .lv{color:var(--faint)}
.arch .lede{color:var(--dim);font-size:14px;line-height:1.6;max-width:70ch}
</style>'''

page = head("The original plates",
  "The ten hand-built coordinate plots EQL Source began with, kept whole after the "
  "mesh-derived floor plans replaced them in August 2026.",
  rel="../", extra=CSS, og="archive", canon="archive/index", robots="noindex") + bar("../") + f'''
<main>
<div class="shell"><div class="note danger" style="margin-top:22px" id="archive-warn"><strong>Kept exactly as they last shipped, and some of it is known to be wrong.</strong> The Najena plate carries six coordinates later found to sit 57&ndash;513 units outside the zone. Nothing here is corrected &mdash; that is what an archive is &mdash; so read it as a record, not as guidance. The <a href="../dungeons/">surveys</a> are current.</div></div>


<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="../">EQL Source</a> &nbsp;/&nbsp; Archive</p>
    <h1 class="display">Where this<br><em>started.</em></h1>
    <p class="hero-lede">Ten hand-built coordinate plots. Every named mob&rsquo;s <code>/loc</code>
      read off the wiki, transformed into page space and drawn by hand, with a numbered legend
      beside it. They were the first thing this project made, and the pages were called
      <em>plates</em> because that is what they were.</p>
    <p class="hero-sig"><span>{len(order)} plates</span><span>Retired 10 Aug 2026</span>
      <span>Kept verbatim</span></p>
  </div>
</section>

<section class="band" style="border-top:0;padding-top:0">
  <div class="shell">
    <div class="note"><strong>Why they were retired, and why they are still here.</strong>
      <code>geometry.py</code> learned to read the game&rsquo;s own mesh archives, and the floor
      plans that came out are better in every direction that matters: the walls are the
      game&rsquo;s walls rather than an outline drawn around some dots, the storeys separate, the
      named filter by storey, and every coordinate is checked against walkable floor at build time.
      <strong>Six impossible Najena positions were caught that way and withheld.</strong> The hand
      plots could not have caught them, because they had nothing to check against.
      <br><br>These are kept because they are the record of how the survey was done before it could
      be done properly &mdash; and because anyone who wants to judge whether we improved or merely
      changed should be able to put the two side by side. They are stored exactly as they last
      shipped. Nothing here has been re-rendered or tidied.</div>
{jump}
{blocks}
  </div>
</section>

</main>
''' + foot("../")

os.makedirs('public/archive', exist_ok=True)
open('public/archive/index.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"archive/index.html written: {len(order)} original plates kept verbatim")
