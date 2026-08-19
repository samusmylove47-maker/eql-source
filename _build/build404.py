"""404.html — a wrong address that still lands somewhere navigable.

Two reasons this exists. The redirect rules that hide internal files point at a
404 page, and without one the host falls back to its own default, which looks
like a broken site rather than ours. And a withdrawn page — the campaign plate,
for one — should send a reader onward rather than into a dead end.
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot, TOOLS, wordnum

page = head("Page not found",
  "That page is not here. The dungeon surveys, tools and the Plane of Sky guide are all one click away.",
  rel="", og="home") + bar("") + f'''
<main id="main">

<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="index.html">EQL Source</a> &nbsp;/&nbsp; Not found</p>
    <h1 class="display">Nothing here,<br><em>but it is nearby.</em></h1>
    <p class="hero-lede">That address does not exist on this site. Either it was mistyped, or it
      pointed at something since withdrawn &mdash; when a page is removed we record it on the change
      log rather than leaving it to rot.</p>
    <p class="hero-sig"><span>404</span><span>Try one of these</span></p>
  </div>
</section>

<div class="shell">
  <section class="band" style="border-top:0;padding-top:0">
    <div class="cards c2">
      <a class="card" href="dungeons/index.html" style="--c:var(--z01)">
        <div class="kicker">Every zone</div>
        <h3 class="t">Dungeon surveys</h3>
        <p class="d">Every surveyed zone, each with a floor plan derived from the game&rsquo;s own
          geometry, its named mobs, and what they drop.</p>
        <div class="foot"><span>Start here</span><span class="go">Open &rarr;</span></div></a>

      <a class="card" href="tools/index.html" style="--c:var(--instr)">
        <div class="kicker">{wordnum(len(TOOLS))} trackers</div>
        <h3 class="t">Tools</h3>
        <p class="d">Progression trackers, The Index, and the faction impact checker. No account,
          nothing transmitted.</p>
        <div class="foot"><span>Share by link</span><span class="go">Open &rarr;</span></div></a>

      <a class="card" href="raids/index.html" style="--c:var(--ember)">
        <div class="kicker">Encounters</div>
        <h3 class="t">Raids</h3>
        <p class="d">The Plane of Sky island by island, with what every boss cost us to kill.</p>
        <div class="foot"><span>Built from play</span><span class="go">Open &rarr;</span></div></a>

      <a class="card" href="sources.html" style="--c:var(--bone)">
        <div class="kicker">Accuracy</div>
        <h3 class="t">Sources and change log</h3>
        <p class="d">Where every claim comes from, and every correction we have made, typed and
          dated.</p>
        <div class="foot"><span>Dated</span><span class="go">Open &rarr;</span></div></a>
    </div>
  </section>
</div>

</main>
''' + foot()

open('public/404.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"404.html written: {len(page)} bytes")
