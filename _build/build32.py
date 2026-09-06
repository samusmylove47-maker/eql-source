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
them, and their keys go in `sections[].images` - beside the section each one
illustrates - or in `media.gallery` for the flat set. Adding one moves no
layout, so assets arriving late cost a rebuild and not a redesign.

This said "each renders in a fixed 16:9 slot" until 6 Sep 2026. It does not, and
had not since the day before: EACH STILL KEEPS ITS OWN SHAPE. See the CSS
comment above `.au-shot img` for what the fixed slot did to a 322x408 portrait -
it cropped away 56 per cent of the one image carrying the claim beside it.

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
/* EACH STILL KEEPS ITS OWN SHAPE. This was aspect-ratio:16/9 with
   object-fit:cover, which is right when every asset is a 16:9 frame and
   destructive the moment one is not. Shara's seven run from 322x408 PORTRAIT to
   1123x710: measured 5 Sep 2026, the list-aura still scaled to 474px to cover a
   210px slot, so 56 per cent of it was cropped away - and that is the image
   carrying her "icon grid or list" claim, which is exactly what the crop
   removed. width/height are on every img, so the browser derives the correct
   ratio itself and still reserves the box before the bytes land. */
.au-shot video,.au-shot img{display:block;width:100%;height:auto}
.au-shot figcaption{font-family:"IBM Plex Mono",monospace;font-size:var(--t-2xs);
  letter-spacing:.1em;text-transform:uppercase;color:var(--faint);
  padding:10px 14px;border-top:1px solid var(--rule)}
/* start, not stretch: a figure sizes to its own image now that the images
   are different heights, so a short one does not grow a border to match
   the tallest in its row. */
.au-grid{display:grid;gap:var(--s-4);align-items:start;
  grid-template-columns:repeat(auto-fit,minmax(320px,1fr))}
.au-get{display:inline-flex;align-items:center;gap:var(--s-3);margin:var(--s-5) 0 0;
  padding:13px 22px;border-radius:var(--r);background:var(--bone);color:var(--surface-0);
  font-family:"Saira Condensed",sans-serif;font-weight:700;font-size:var(--t-lg);
  text-transform:uppercase;letter-spacing:.03em;text-decoration:none}
.au-get:hover{filter:brightness(1.08)}
/* Her sections. A heading, her lines, then whichever stills she put under it.
   Deliberately quiet: the copy is the product's pitch and the site's job here is
   to carry it legibly, not to restyle it. */
.au-feat{margin:var(--s-7) 0 0}
.au-feat h2{font-family:"Saira Condensed",sans-serif;font-size:var(--t-xl);
  font-weight:600;text-transform:uppercase;letter-spacing:.03em;color:var(--bone);
  margin:0 0 var(--s-3)}
.au-feat p{margin:0 0 var(--s-3);color:var(--mut);line-height:1.6}
.au-feat p strong{color:var(--bone)}
.au-feat .au-grid{margin-top:var(--s-4)}
.au-install{margin:var(--s-7) 0 0;padding:var(--s-5);border:1px solid var(--rule2);
  border-radius:var(--r);background:var(--surface-1)}
.au-install h2{font-family:"Saira Condensed",sans-serif;font-size:var(--t-lg);
  font-weight:600;text-transform:uppercase;letter-spacing:.03em;color:var(--bone);
  margin:0 0 var(--s-3)}
.au-install ol{margin:0;padding-left:1.3em;color:var(--mut);line-height:1.7}
.au-install .au-plat{margin-top:var(--s-3)}
.au-links{list-style:none;margin:var(--s-5) 0 0;padding:0;display:grid;gap:1px;
  background:var(--rule);border:1px solid var(--rule);border-radius:var(--r);overflow:hidden}
.au-links li{background:var(--panel);padding:13px 16px}
.au-links a{color:var(--instr-t);text-decoration:none;font-weight:600}
.au-links span{display:block;color:var(--faint);font-size:var(--t-sm);margin-top:3px}
.au-pending{margin:var(--s-5) 0 0;padding:14px 16px;border:1px dashed var(--rule);
  border-radius:var(--r);color:var(--faint);font-size:var(--t-sm);line-height:1.6;max-width:62ch}
</style>'''


def shot(key, caption=None, vid=False):
    """One slot, at the asset's OWN aspect ratio. Video is deferred; an image
    is lazy.

    Not 16:9. width and height come from the manifest and the browser derives
    the ratio, which is what stops a portrait still being cropped to a
    landscape box - and still reserves the space before the bytes land.

    Returns '' for a key the manifest does not hold. That is deliberate on a
    launch page, and it is why check.py walks every key this is called with:
    silent degradation and a silent regression are the same output."""
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
        # Intrinsic size from the manifest, not a typed 1600x900 - see the note
        # in build1.py. The old poster was that size by coincidence.
        pw, ph = poster.get('w') or 1600, poster.get('h') or 900
        return (f'<figure class="au-shot" id="auwrap2" data-video="{src}" data-poster="{pv}">'
                f'<img src="{pv}" width="{pw}" height="{ph}" alt="">'
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

# HER NINE SECTIONS, IN HER ORDER, WITH HER IMAGES UNDER THE HEADINGS SHE
# ASSIGNED THEM. Both come out of assets/auras.json, which extracted them from
# HIGHLIGHTS.md and her RELEASE-PAGE.md table rather than retyping either - see
# the note beside them there. Nothing on this page is our wording.
#
# The site carried three paragraphs of hers and one heading. She has nine
# sections and twenty lines, and nine of those lines describe features this page
# had never mentioned at all - travel routing and action-bar skinning among them.
def feature(sec):
    lines = "".join(
        f'<p><strong>{l["lead"]}</strong> {l["rest"]}</p>' if l.get("rest")
        else f'<p><strong>{l["lead"]}</strong></p>'
        for l in sec.get('lines') or [])
    imgs = "".join(shot(k) for k in (sec.get('images') or []))
    if imgs:
        imgs = f'<div class="au-grid">{imgs}</div>'
    return (f'<section class="au-feat"><h2>{sec["title"]}</h2>{lines}{imgs}</section>')


feats = "".join(feature(x) for x in (A.get('sections') or []))

# Her install steps sit beside the download, which is where somebody reads them.
# Ours compressed the same thing into one sentence in the band foot and did not
# mention what SmartScreen actually says.
_ins = A.get('install') or {}
install = ''
if _ins.get('steps'):
    _steps = "".join(f'<li>{t}</li>' for t in _ins['steps'])
    install = (f'<div class="au-install"><h2>Installing</h2><ol>{_steps}</ol>'
               + (f'<p class="au-plat">{_ins["note"]}</p>' if _ins.get('note') else '')
               + '</div>')

# The flat gallery is gone: every still now sits under the section its own
# author put it under. The key stays read so an unplaced image is still visible
# rather than silently dropped.
_placed = {k for x in (A.get('sections') or []) for k in (x.get('images') or [])}
gallery = ''.join(shot(k) for k in (A['media'].get('gallery') or []) if k not in _placed)
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
    <div class="au-body">{body}</div>
    {feats}
    {gallery}
    {install}
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
      var im=w.querySelector('img');
      if(im){{ v.setAttribute('width',im.getAttribute('width'));
               v.setAttribute('height',im.getAttribute('height')); }}
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
