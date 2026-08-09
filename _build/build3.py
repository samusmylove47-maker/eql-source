import os, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT,'_build'))
import json, re, shutil, os
from withheld import WITHHELD, REASON, MARK
_CFG = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"site.config.json"), encoding="utf-8"))
SITE = _CFG["site_name"]
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'source')
Z = json.load(open('assets/zones-index.json', encoding='utf-8'))
BY = {z['slug']: z for z in Z}
MAPS = ["najena","splitpaw","lowerguk","nagafenslair","mistmoore"]

RETURN_CSS = """
<style>
.ns-bar{background:#161D21;border-bottom:1px solid #293439;padding:11px 22px;display:flex;
 align-items:center;gap:13px;flex-wrap:wrap;font-family:"IBM Plex Mono",monospace;font-size:10px;
 letter-spacing:.16em;text-transform:uppercase;position:sticky;top:0;z-index:90}
.ns-bar a{color:#AEB9B8;text-decoration:none;border-bottom:1px solid transparent;transition:color .15s}
.ns-bar a:hover{color:#E6E9E4;border-color:#E6E9E4}
.ns-bar .ns-mark{font-family:"Saira Condensed",sans-serif;font-size:15px;font-weight:700;
 letter-spacing:.13em;color:#E6E9E4;text-decoration:none;border:0}
/* These carried the pre-AA greys. #4E5C61 measured 2.46:1 on this bar. The
   values here mirror assets/site.css's ramp; they are duplicated rather than
   referenced because this chrome is injected into standalone tool pages. */
.ns-bar .ns-sep{color:#7D9096}
.ns-bar .ns-tag{margin-left:auto;color:#7D9096}
@media(max-width:640px){.ns-bar .ns-tag{display:none}}
</style>
"""

def bar_html(rel, crumb, crumb_href, here, extra=""):
    return (f'<div class="ns-bar"><a class="ns-mark" href="{rel}index.html">{SITE}</a>'
            f'<span class="ns-sep">/</span><a href="{rel}{crumb_href}">{crumb}</a>'
            f'<span class="ns-sep">/</span><span style="color:#D5DBD8">{here}</span>'
            f'{extra}<span class="ns-tag">Sourced &amp; dated &middot; updated daily</span></div>')

# Pages that already have a sticky bar of their own. Both bars pin to top:0,
# and this one wins on z-index, so on the race tracker it covered 73% of the
# tool's own tab-and-save bar the moment you scrolled. The breadcrumb is the
# less important of the two, so it stops following on those pages.
UNPIN = '<style>.ns-bar{position:static}</style>'

WH_CSS = """
<style>
.wh{font-family:"IBM Plex Mono",monospace;font-size:.82em;letter-spacing:.06em;
  text-transform:uppercase;color:#D9837C;border-bottom:1px dotted #D9837C}
.whnote{margin:14px 0 0;padding:12px 14px;border-left:3px solid #C9453A;
  background:rgba(201,69,58,.06);color:#9FADAC;font-size:14px;line-height:1.55}
.whnote strong{color:#E6E9E4}
</style>"""


def mark_withheld(h, slug):
    """Replace the coordinate cell of every withheld mob, and say why once.

    Matched on the row rather than on the coordinate text, so a coordinate that
    also appears legitimately elsewhere on the page is untouched.
    """
    names = sorted(n for z, n in WITHHELD if z == slug)
    if not names:
        return h, 0
    hits = 0
    for name in names:
        # the roster row: name cell, then the loc cell immediately after
        pat = re.compile(
            r'(<td class="nmob">' + re.escape(name) + r'</td>\s*<td class="loc">)(.*?)(</td>)',
            re.S)
        h, n = pat.subn(lambda m: m.group(1) + MARK + m.group(3), h)
        hits += n
    if hits:
        note = ('<p class="whnote"><strong>Why six positions are missing.</strong> '
                + REASON.get(slug, '') + '</p>')
        # after the roster table that carries them
        i = h.find(MARK)
        j = h.find('</table>', i)
        if j > 0:
            j += len('</table>')
            h = h[:j] + note + h[j:]
    return h, hits


def inject(src, dst, rel, crumb, crumb_href, here, extra="", subs=None, own_bar=False,
           wh_slug=None):
    h = open(src, encoding='utf-8').read()
    if wh_slug:
        h, nwh = mark_withheld(h, wh_slug)
        if nwh:
            h = h.replace('</head>', WH_CSS + '</head>', 1)
    if subs:
        for a, b in subs:
            h = h.replace(a, b)
    css = RETURN_CSS + (UNPIN if own_bar else '')
    h = h.replace('</head>', f'<link rel="icon" href="{rel}favicon.svg" type="image/svg+xml">' + css + '</head>', 1)
    h = re.sub(r'<body([^>]*)>', lambda m: '<body%s>\n' % m.group(1) + bar_html(rel, crumb, crumb_href, here, extra), h, count=1)
    open(dst, 'w', encoding='utf-8', newline='\n').write(h)
    return len(h)

n = 0
# ---- plates
for z in Z:
    s = z['slug']
    extra = ''
    if s in MAPS:
        extra = (f'<span class="ns-sep">/</span><a href="{s}-map.html" '
                 f'style="color:color-mix(in srgb, {z["accent"]} 56%, #E6E9E4)">Navigation map &rarr;</a>')
    n += 1
    inject(os.path.join(SRC, f'{s}.html'), f'public/dungeons/{s}.html', '../', 'Dungeons', 'dungeons/index.html',
           f"Plate {z['plate']:02d} &middot; {z['title']}", extra, wh_slug=s)
# ---- maps
for s in MAPS:
    z = BY[s]
    extra = (f'<span class="ns-sep">/</span><a href="{s}.html" '
             f'style="color:color-mix(in srgb, {z["accent"]} 56%, #E6E9E4)">&larr; Survey plate</a>')
    n += 1
    inject(os.path.join(SRC, f'{s}-map.html'), f'public/dungeons/{s}-map.html', '../', 'Dungeons', 'dungeons/index.html',
           f"{z['title']} &middot; map", extra)
# ---- tools
inject(os.path.join(SRC,'eql-sky-tracker.html'), 'public/tools/plane-of-sky.html', '../',
       'Tools', 'tools/index.html', 'Plane of Sky tracker', own_bar=True)
inject(os.path.join(SRC,'eql-race-unlocks.html'), 'public/tools/race-unlocks.html', '../',
       'Tools', 'tools/index.html', 'Race unlock tracker',
       extra='<span class="ns-sep">/</span><a href="combo-calculator.html">Combo calculator &rarr;</a>',
       own_bar=True)
# calculator = same app, boots on the calc tab, shares the same save key
inject(os.path.join(SRC,'eql-race-unlocks.html'), 'public/tools/combo-calculator.html', '../',
       'Tools', 'tools/index.html', 'Race &amp; primary calculator',
       extra='<span class="ns-sep">/</span><a href="race-unlocks.html">&larr; Race unlocks</a>',
       subs=[(' show("track");\n})();', ' show("calc");\n})();'),
             ('<title>Race Unlock Tracker', '<title>Race &amp; Primary Calculator')],
       own_bar=True)
n += 3
print(f"imported {n} pages")
