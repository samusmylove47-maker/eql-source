import os, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT,'_build'))
import json, re, shutil, os
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
.ns-bar a{color:#8A9998;text-decoration:none;border-bottom:1px solid transparent;transition:color .15s}
.ns-bar a:hover{color:#E6E9E4;border-color:#E6E9E4}
.ns-bar .ns-mark{font-family:"Saira Condensed",sans-serif;font-size:15px;font-weight:700;
 letter-spacing:.13em;color:#E6E9E4;text-decoration:none;border:0}
.ns-bar .ns-sep{color:#4E5C61}
.ns-bar .ns-tag{margin-left:auto;color:#4E5C61}
@media(max-width:640px){.ns-bar .ns-tag{display:none}}
</style>
"""

def bar_html(rel, crumb, crumb_href, here, extra=""):
    return (f'<div class="ns-bar"><a class="ns-mark" href="{rel}index.html">{SITE}</a>'
            f'<span class="ns-sep">/</span><a href="{rel}{crumb_href}">{crumb}</a>'
            f'<span class="ns-sep">/</span><span style="color:#D5DBD8">{here}</span>'
            f'{extra}<span class="ns-tag">Sourced &amp; dated &middot; updated daily</span></div>')

def inject(src, dst, rel, crumb, crumb_href, here, extra="", subs=None):
    h = open(src, encoding='utf-8').read()
    if subs:
        for a, b in subs:
            h = h.replace(a, b)
    h = h.replace('</head>', f'<link rel="icon" href="{rel}favicon.svg" type="image/svg+xml">' + RETURN_CSS + '</head>', 1)
    h = re.sub(r'<body([^>]*)>', lambda m: '<body%s>\n' % m.group(1) + bar_html(rel, crumb, crumb_href, here, extra), h, count=1)
    open(dst, 'w', encoding='utf-8', newline='\n').write(h)
    return len(h)

n = 0
# ---- plates
for z in Z:
    s = z['slug']
    extra = ''
    if s in MAPS:
        extra = f'<span class="ns-sep">/</span><a href="{s}-map.html" style="color:{z["accent"]}">Navigation map &rarr;</a>'
    n += 1
    inject(os.path.join(SRC, f'{s}.html'), f'dungeons/{s}.html', '../', 'Dungeons', 'dungeons/index.html',
           f"Plate {z['plate']:02d} &middot; {z['title']}", extra)
# ---- maps
for s in MAPS:
    z = BY[s]
    extra = f'<span class="ns-sep">/</span><a href="{s}.html" style="color:{z["accent"]}">&larr; Survey plate</a>'
    n += 1
    inject(os.path.join(SRC, f'{s}-map.html'), f'dungeons/{s}-map.html', '../', 'Dungeons', 'dungeons/index.html',
           f"{z['title']} &middot; map", extra)
# ---- campaign plate
n += 1
inject(os.path.join(SRC,'campaign-plate-10-to-50.html'), 'dungeons/campaign-10-to-50.html', '../',
       'Dungeons', 'dungeons/index.html', 'Campaign plate &middot; 10&ndash;50')

# ---- tools
inject(os.path.join(SRC,'eql-sky-tracker.html'), 'tools/plane-of-sky.html', '../',
       'Tools', 'tools/index.html', 'Plane of Sky tracker')
inject(os.path.join(SRC,'eql-race-unlocks.html'), 'tools/race-unlocks.html', '../',
       'Tools', 'tools/index.html', 'Race unlock tracker',
       extra='<span class="ns-sep">/</span><a href="combo-calculator.html">Combo calculator &rarr;</a>')
# calculator = same app, boots on the calc tab, shares the same save key
inject(os.path.join(SRC,'eql-race-unlocks.html'), 'tools/combo-calculator.html', '../',
       'Tools', 'tools/index.html', 'Race &amp; primary calculator',
       extra='<span class="ns-sep">/</span><a href="race-unlocks.html">&larr; Race unlocks</a>',
       subs=[(' show("track");\n})();', ' show("calc");\n})();'),
             ('<title>Race Unlock Tracker', '<title>Race &amp; Primary Calculator')])
n += 3
print(f"imported {n} pages")
