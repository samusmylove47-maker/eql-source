"""learn/index.html — the hub six Learn pages never had.

WHY
---
Six Learn pages existed. The header's Learn link went to `still-true.html`, and
the breadcrumb on every Learn page read "EQL Source / Learn / …" with *Learn*
pointing back at that same one article. A reader who wanted to know what else
was in Learn had only the footer.

Given that the Learn set now holds the register of inherited advice and the
measured difficulty ramp — the two things on this site that exist nowhere else
— that was the cheapest structural win available and it sat unbuilt.

Driven by the LEARN registry in _partials.py, so the hub, the footer and the
nav cannot disagree about what Learn contains.
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot, LEARN, wordnum

CSS = '''<style>
.lh{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));
  gap:var(--s-4);margin-top:var(--s-6)}
.lh a{background:var(--surface-1);padding:22px 24px;display:grid;gap:8px;align-content:start;
  text-decoration:none;border:1px solid var(--rule);border-radius:var(--r);
  box-shadow:var(--lift);transition:transform var(--speed),box-shadow var(--speed),border-color var(--speed)}
.lh a:hover{transform:translateY(-2px);box-shadow:var(--shadow-2);border-color:var(--rule2)}
.lh a:first-child{grid-column:1/-1;padding:clamp(24px,3vw,36px);
  background:linear-gradient(160deg,color-mix(in srgb, var(--brass) 10%, var(--sheet)), var(--sheet))}
.lh a:first-child h3{font-size:clamp(28px,4vw,42px)}
.lh h3{font-family:"Saira Condensed",sans-serif;font-size:22px;font-weight:700;
  text-transform:uppercase;letter-spacing:.02em;color:var(--bone);margin:0;line-height:1.1}
.lh p{margin:0;color:var(--dim);font-size:14.5px;line-height:1.6}
.lh .go{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--faint)}
.lh a:hover .go{color:var(--bone)}
@media(max-width:720px){.lh{grid-template-columns:1fr}.lh a:first-child{grid-column:auto}}
</style>'''

cards = "\n".join(
    f'''      <a href="{it["slug"]}.html">
        <h3>{it["name"]}</h3>
        <p>{it["blurb"]}</p>
        <span class="go">Read &rarr;</span>
      </a>''' for it in LEARN)

page = (head("Learn",
             "Explainers for EverQuest Legends: what inherited advice still holds, what difficulty "
             "actually changes, what motes are worth, and how to read our floor plans.",
             rel="../", extra=CSS, og="home", canon="learn/index")
        + bar("../") + f'''
<main id="main">
<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp; Learn</p>
    <h1 class="display">{wordnum(len(LEARN))} things<br><em>worth knowing.</em></h1>
    <p class="hero-lede">Every EverQuest Legends player is a returning EverQuest player carrying
      twenty-five years of muscle memory, and a large amount of what they know is now wrong. These
      are the pages about which parts.</p>
  </div>
</section>

<section class="band" style="border-top:0;padding-top:0">
  <div class="shell">
    <div class="lh">
{cards}
    </div>
  </div>
</section>
</main>
''' + foot("../"))

open('public/learn/index.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"learn/index.html written: {len(LEARN)} explainers")
