"""public/auras.html — the destination the home-page band had none of.

WHY THIS PAGE EXISTS
--------------------
On 1 Sep 2026 the home page carried a full-width EQLS Auras band with an
autoplaying trailer and **zero `<a>` elements**, and the word "Auras" appeared on
no other page of the 715. A reader who wanted the thing had nowhere to go. That
was tolerable while it was a teaser; it stops being tolerable on the day it is
released, which is today.

WHAT THIS FILE MAY AND MAY NOT DO
---------------------------------
EQLS Auras is Shara's project. Shara has creative and production control and her
copy reaches us through the owner. **No build session writes a claim about what
it does.** Every sentence rendered here is read from `assets/auras.json`, where it
was moved verbatim out of `_build/build1.py` — so the band and this page cannot
drift apart, and neither can be edited by anyone but the owner.

A NULL FIELD RENDERS NOTHING. There is no download address for this product
anywhere in this repository, so this page says nothing about how to get it. When
`download.url` is filled the control appears. **The alternative — a plausible
GitHub releases URL — is the one thing this project refuses on every other page,
and a launch is not a reason to start.**

MEDIA IS A DROP-IN. Shara's stills and GIFs land in `_media/`, `media.py` hashes
them, their keys go in `media.gallery`, and each renders in a fixed 16:9 slot.
Adding one moves no layout, so assets arriving late cost a rebuild and not a
redesign.

THE TRAILER IS DEFERRED, and that is not optional: `scripts/mediadefer.js`
fails the build if any `<video>` carries an eager `src` or `poster`. The pattern
here is the home page's, for the same reason — 2.19 MB of trailer must not load
before a reader has seen anything.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

A = json.load(open('assets/auras.json', encoding='utf-8'))
MEDIA = json.load(open('assets/media.json', encoding='utf-8'))

CSS = '''<style>
.au-hero .display{max-width:16ch}
.au-lede{font-size:var(--t-lg);color:var(--dim);line-height:1.5;max-width:52ch;
  margin:var(--s-4) 0 0;text-wrap:balance}
.au-plat{font-family:"IBM Plex Mono",monospace;font-size:var(--t-2xs);
  letter-spacing:.14em;text-transform:uppercase;color:var(--faint);margin:var(--s-4) 0 0}
.au-body p{color:var(--mut);font-size:var(--t-base);line-height:1.65;max-width:70ch;
  margin:0 0 var(--s-4)}
.au-shot{margin:0 0 var(--s-5);border:1px solid var(--rule);border-radius:var(--r);
  overflow:hidden;background:var(--surface-2)}
.au-shot video,.au-shot img{display:block;width:100%;height:auto;aspect-ratio:16/9;
  object-fit:cover}
.au-shot figcaption{font-family:"IBM Plex Mono",monospace;font-size:var(--t-2xs);
  letter-spacing:.1em;text-transform:uppercase;color:var(--faint);
  padding:10px 14px;border-top:1px solid var(--rule)}
.au-grid{display:grid;gap:var(--s-4);grid-template-columns:repeat(auto-fit,minmax(320px,1fr))}
.au-get{display:inline-flex;align-items:center;gap:var(--s-3);margin:var(--s-5) 0 0;
  padding:13px 22px;border-radius:var(--r);background:var(--bone);color:var(--surface-0);
  font-family:"Saira Condensed",sans-serif;font-weight:700;font-size:var(--t-lg);
  text-transform:uppercase;letter-spacing:.03em;text-decoration:none}
.au-get:hover{filter:brightness(1.08)}
.au-links{list-style:none;margin:var(--s-5) 0 0;padding:0;display:grid;gap:1px;
  background:var(--rule);border:1px solid var(--rule);border-radius:var(--r);overflow:hidden}
.au-links li{background:var(--panel);padding:13px 16px}
.au-links a{color:var(--instr-t);text-decoration:none;font-weight:600}
.au-links span{display:block;color:var(--faint);font-size:var(--t-sm);margin-top:3px}
.au-pending{margin:var(--s-5) 0 0;padding:14px 16px;border:1px dashed var(--rule);
  border-radius:var(--r);color:var(--faint);font-size:var(--t-sm);line-height:1.6;max-width:62ch}
</style>'''


def shot(key, caption=None, vid=False):
    """One fixed 16:9 slot. Video is deferred; an image is lazy."""
    m = MEDIA.get(key)
    if not m:
        return ''
    src = f"assets/media/{m['file']}"
    cap = f'<figcaption>{caption}</figcaption>' if caption else ''
    if vid:
        # CLICK TO PLAY. This is the first thing on the page, so "load when
        # visible" means "load immediately" - 839 KB before the reader has read a
        # word. The poster is the page; the motion is opt-in. Same reasoning and
        # same shape as the home-page band.
        poster = MEDIA.get(A['media'].get('poster') or '', {})
        pv = f"assets/media/{poster['file']}" if poster else ''
        return (f'<figure class="au-shot" id="auwrap2" data-video="{src}" data-poster="{pv}">'
                f'<img src="{pv}" width="1600" height="900" alt="">'
                f'<button class="vplay" type="button">Play</button>'
                f'{cap}</figure>')
    w = m.get('w') or 1600
    h = m.get('h') or 900
    return (f'<figure class="au-shot"><img src="{src}" loading="lazy" alt="" '
            f'width="{w}" height="{h}">{cap}</figure>')


DL = A.get('download') or {}
if DL.get('url'):
    _label = DL.get('label') or f"Download {A['name']}"
    _ver = f" <span>{DL['version']}</span>" if DL.get('version') else ''
    get = f'<a class="au-get" href="{DL["url"]}">{_label}{_ver}</a>'
else:
    # NOT A PLACEHOLDER FOR A READER TO PUZZLE OVER. It says only what is true:
    # this page does not yet carry the address. It disappears the moment
    # assets/auras.json carries one.
    get = ('<p class="au-pending">No download address is published here yet. '
           'This page will carry it as soon as there is one to carry.</p>')

_links = A.get('links') or []
links = ''
if _links:
    rows = ''.join(
        f'<li><a href="{l["href"]}">{l["label"]}</a>'
        + (f'<span>{l["note"]}</span>' if l.get('note') else '') + '</li>'
        for l in _links)
    links = f'<ul class="au-links">{rows}</ul>'

gallery = ''.join(shot(k) for k in (A['media'].get('gallery') or []))
if gallery:
    gallery = f'<div class="au-grid">{gallery}</div>'

body = ''.join(f'<p>{p}</p>' for p in A['body'])

page = (head(A['name'],
             "EQLS Auras reads your EverQuest Legends combat log and draws your "
             "buffs over the game as icons that count down.",
             rel="", extra=CSS, og="tools", canon="auras")
        + bar("") + f'''
<main>
<section class="hero page au-hero">
  <div class="shell">
    <p class="crumb"><a href="./">EQL Source</a> &nbsp;/&nbsp; {A['name']}</p>
    <h1 class="display">{A['name']}</h1>
    <p class="au-lede">{A['lede']}</p>
    <p class="au-plat">{A['platform']}</p>
    {get}
  </div>
</section>

<section class="band" style="border-top:0;padding-top:0">
  <div class="shell">
    {shot(A['media'].get('trailer'), A.get('caption'), vid=True)}
    {gallery}
    <div class="au-body">{body}</div>
    {links}
  </div>
  <script>
  (function(){{
    var w=document.getElementById('auwrap2');
    if(!w) return;
    var b=w.querySelector('.vplay');
    if(!b) return;
    b.addEventListener('click',function(){{
      var v=document.createElement('video');
      v.src=w.getAttribute('data-video');
      v.setAttribute('poster',w.getAttribute('data-poster'));
      v.muted=true; v.loop=true; v.playsInline=true; v.controls=true;
      v.setAttribute('width','1600'); v.setAttribute('height','900');
      w.replaceChild(v,w.querySelector('img'));
      b.remove();
      var p=v.play(); if(p&&p.catch) p.catch(function(){{}});
    }});
  }})();
  </script>
</section>
</main>
''' + foot(""))

open('public/auras.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"auras.html written: download {'published' if DL.get('url') else 'NOT YET SET'}, "
      f"{len(A['media'].get('gallery') or [])} gallery slot(s), {len(_links)} link(s)")
