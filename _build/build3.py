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
.disputed{text-decoration:line-through;text-decoration-color:#D9837C;
  text-decoration-thickness:2px;color:#8A9998}
.ph-ev{margin:10px 0 12px;padding-left:18px;line-height:1.62}
.ph-ev li{margin:0 0 7px}
.inj-contact{margin:26px 0 0;padding:15px 17px;border:1px solid #2E3A41;border-radius:4px;
  background:rgba(255,255,255,.02)}
.inj-contact p{margin:0;color:#9FADAC;font-size:14px;line-height:1.6}
.inj-contact strong{color:#E6E9E4}
.inj-contact a{color:#8FBEE4}
.inj-contact .nolog{margin-top:7px;font-size:12.5px;color:#7D9096}
.ph-note{margin:0 0 16px;padding:13px 15px;border-radius:4px;font-size:14px;line-height:1.6}
.ph-note strong{display:block;margin-bottom:4px}
.ph-yes{border-left:3px solid #5FA37E;background:rgba(95,163,126,.07);color:#AEB9B8}
.ph-yes strong{color:#8FD3AD}
.ph-note a{color:#8FBEE4}

/* The trimmed plate blocks. Answer-first lists, a key chain drawn as a chain,
   and dangers that read as dangers. Injected because plates carry their own CSS. */
ul.why{list-style:none;margin:0;padding:0;display:grid;gap:10px}
ul.why li{padding:12px 15px;border:1px solid #2E3A41;border-left:3px solid var(--acc,#D9A227);
  border-radius:4px;background:#151B1F;color:#AEB9B8;font-size:15px;line-height:1.55}
ul.why b{color:#E6E9E4}
ol.chain{list-style:none;margin:0 0 14px;padding:0;display:grid;gap:0}
ol.chain li{display:grid;grid-template-columns:minmax(140px,auto) 1fr auto;gap:12px;
  align-items:baseline;padding:11px 14px;border:1px solid #2E3A41;border-bottom:0;
  background:#151B1F;color:#8A9998;font-size:14px}
ol.chain li:first-child{border-radius:4px 4px 0 0}
ol.chain li:last-child{border-bottom:1px solid #2E3A41;border-radius:0 0 4px 4px}
ol.chain b{color:#E6E9E4;font-size:15px}
ol.chain .cm{font-family:"IBM Plex Mono",monospace;font-size:11.5px;color:#7D9096}
ol.chain .ck{font-family:"IBM Plex Mono",monospace;font-size:12.5px;color:var(--acct,#E8C25F)}
@media(max-width:640px){ol.chain li{grid-template-columns:1fr;gap:3px}}
ul.danger-list,ul.tightlist{list-style:none;margin:0;padding:0;display:grid;gap:9px}
ul.danger-list li,ul.tightlist li{padding:11px 14px;border-left:3px solid #2E3A41;
  background:rgba(255,255,255,.02);color:#9FADAC;font-size:14.5px;line-height:1.55}
ul.danger-list li{border-left-color:#C9453A}
ul.danger-list b,ul.tightlist b{color:#E6E9E4}
p.tight{color:#9FADAC;font-size:14px;line-height:1.6;margin:0}
</style>"""

# The plates and tools are standalone pages with their own footers, so foot()
# never reaches them - and they are the most-read pages on the site. A door only
# on the pages nobody arrives at is not a door.
# THE PLACEHOLDER STATEMENT
# Spawn percentages on every survey are inherited classic data: they describe
# the chance a named appears instead of its placeholder. The developer patch
# note removed placeholders from all ten of these zones and Upper Guk, so every
# percentage on the site is historical. It is printed rather than deleted, with
# this note above it, because deleting what a source says is how a record stops
# being checkable.
PH_CONFIRMED = """
<div class="ph-note ph-yes"><strong>Named spawn every cycle. No placeholders here.</strong>
  Percentages below are inherited classic data and describe nothing about this zone now.
  <a href="REL_learn/reading-the-plans.html">Why they are still printed &rarr;</a></div>"""

CONTACT = """
<div class="inj-contact">
  <p><strong>Found something this page gets wrong, or something the wiki does?</strong>
    That is the most useful thing anyone can send us, and every finding is credited by name.
    <a href="https://github.com/samusmylove47-maker/eql-source/issues/new?template=finding.yml">Send
    a finding</a> &middot; <a href="REL_learn/still-true.html">see what is already open</a>.</p>
  <p class="nolog">Please do not attach a combat log to a public issue &mdash; they can carry
    private chat. Say you have one and we will ask.</p>
</div>"""


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



# ---------------------------------------------------------------------------
# THE RETRACTION HAS TO REACH THE ROW
#
# The placeholder question was settled at tier 1 on 10 Aug: the patch note names
# eleven dungeons placeholders were removed from. Every affected survey grew a
# header saying so. The roster rows underneath kept saying "Placeholder is an
# earth elemental" in bold and present tense, three lines below a header saying
# there are none.
#
# That is the shape of every remaining defect an outside reader has found here:
# a decision reaches the authored layer and stops at the boundary with the
# generated one. The header is written by hand; the rows come out of the mine.
# Nothing connected them.
#
# This connects them. `placeholders_removed` already existed in zones-index.json
# and nothing read it. Now the renderer reads it and marks every placeholder
# assertion in a roster cell as historical, so the header is a summary of the
# table rather than a disclaimer about it.
PH_CLAIM = re.compile(
    # "there are none here" and "not a placeholder" are the corrected form
    # and must not be struck. Only a bare present-tense assertion is marked.
    r'(?<!not a )(?<!are no )'
    + chr(92) + 'b'
    + r'([Pp]laceholders? (?:is|are) [^<.]{2,70}?)(?=[.<])')
PH_MARK_CSS = """<style>
.ph-old{text-decoration:line-through;text-decoration-color:#C9453A;
  text-decoration-thickness:1px;color:#7D9096}
.ph-old-tag{font-family:"IBM Plex Mono",monospace;font-size:9px;letter-spacing:.12em;
  text-transform:uppercase;color:#D46C64;border:1px solid #6A2F2B;border-radius:2px;
  padding:1px 4px;margin-left:5px;white-space:nowrap;text-decoration:none;display:inline-block}
</style>"""


def mark_placeholders(h, slug):
    """Strike placeholder claims in roster cells where the patch note removed them."""
    z = BY.get(slug)
    if not z or not z.get('placeholders_removed'):
        return h, 0
    n = 0

    def one(m):
        nonlocal n
        n += 1
        return (f'<span class="ph-old" title="Historical. The 28 July 2026 patch note '
                f'removed placeholders from this zone.">{m.group(1)}</span>'
                f'<span class="ph-old-tag">was</span>')

    # only inside the roster's notes cells, never in body prose
    def cell(cm):
        return '<td class="src">' + PH_CLAIM.sub(one, cm.group(1)) + '</td>'

    h = re.sub(r'<td class="src">(.*?)</td>', cell, h, flags=re.S)
    return h, n


PH_MARKED = []


def inject(src, dst, rel, crumb, crumb_href, here, extra="", subs=None, own_bar=False,
           wh_slug=None, ph_zone=None, og_card=None, canon=None):
    h = open(src, encoding='utf-8').read()
    if wh_slug:
        h, nwh = mark_withheld(h, wh_slug)
        if nwh:
            h = h.replace('</head>', WH_CSS + '</head>', 1)
    if subs:
        for a, b in subs:
            h = h.replace(a, b)
    if ph_zone:
        h, nph = mark_placeholders(h, ph_zone)
        if nph:
            h = h.replace('</head>', PH_MARK_CSS + '</head>', 1)
            PH_MARKED.append((ph_zone, nph))
    css = RETURN_CSS + (UNPIN if own_bar else '')
    # Surveys, maps and tools are standalone pages that never call head(), so
    # their share cards and canonicals are injected here. Without this the
    # ten most-read pages on the site were the ten with no card.
    social = ""
    zdata = BY.get(canon.split("/")[-1].replace("-map", "")) if canon else None
    if og_card:
        url = _CFG.get("site_url", "").rstrip("/")
        img = f"{url}/assets/og/{og_card}.png"
        title = re.search(r"<title>([^<]*)</title>", h)
        title = title.group(1).strip() if title else SITE
        desc = re.search(r'<meta name="description" content="([^"]*)"', h)
        desc = desc.group(1) if desc else ""
        if not desc:
            # Fifteen of the seventeen standalone pages have no description of
            # their own, so a Discord embed would carry a title and an image and
            # no sentence. The subtitle is already the one-line summary of the
            # page - it is what the subtitle is for.
            sub = re.search(r'<p class="subtitle">(.*?)</p>', h, re.S)
            if sub:
                desc = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", sub.group(1))).strip()
            if desc and zdata:
                # Entities belong in HTML, not in a plain-text share snippet.
                # A share snippet is plain text in an attribute: no entities, and
                # no bare "<" for a parser to trip over.
                clean = (lambda t: re.sub(r"&[a-z]+;", " ",
                         t.replace("&le;", "at most ").replace("<=", "at most ")
                          .replace("&ndash;", "-").replace("&mdash;", "-")
                          .replace("&minus;", "-").replace("<", "")).strip())
                desc = (f"{clean(desc)}. Levels {clean(zdata['levels'].split(' (')[0])}, "
                        f"respawn {clean(zdata['respawn'] or 'not recorded')}. "
                        f"Every figure sourced and dated.")
            h = h.replace('<meta name="viewport"',
                          f'<meta name="description" content="{desc}">'
                          '<meta name="viewport"', 1)
        social = (f'<meta property="og:title" content="{title}">'
                  f'<meta property="og:description" content="{desc}">'
                  f'<meta property="og:type" content="website">'
                  f'<meta property="og:site_name" content="{SITE}">'
                  f'<meta property="og:image" content="{img}">'
                  f'<meta property="og:image:width" content="1200">'
                  f'<meta property="og:image:height" content="630">'
                  f'<meta name="twitter:card" content="summary_large_image">'
                  f'<meta name="twitter:title" content="{title}">'
                  f'<meta name="twitter:description" content="{desc}">'
                  f'<meta name="twitter:image" content="{img}">')
        if canon:
            social += f'<link rel="canonical" href="{url}/{canon}">'
    h = h.replace('</head>', f'<link rel="icon" href="{rel}favicon.svg" type="image/svg+xml">' + social + css + '</head>', 1)
    h = re.sub(r'<body([^>]*)>', lambda m: '<body%s>\n' % m.group(1) + bar_html(rel, crumb, crumb_href, here, extra), h, count=1)
    if ph_zone:
        z_ = BY.get(ph_zone, {})
        note = PH_CONFIRMED.replace('REL_', rel)
        # above the roster, which is the table the percentages live in
        k = h.find('Named roster')
        if k > 0:
            k = h.find('</h2>', k) + len('</h2>')
            h = h[:k] + note + h[k:]
    if '</footer>' in h:
        h = h.replace('</footer>', CONTACT.replace('REL_', rel) + '\n</footer>', 1)
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
           f"Survey {z['plate']:02d} &middot; {z['title']}", extra, wh_slug=s, ph_zone=s,
           og_card=f"dungeons-{s}", canon=f"dungeons/{s}")
# ---- maps
for s in MAPS:
    z = BY[s]
    extra = (f'<span class="ns-sep">/</span><a href="{s}.html" '
             f'style="color:color-mix(in srgb, {z["accent"]} 56%, #E6E9E4)">&larr; Survey</a>')
    n += 1
    inject(os.path.join(SRC, f'{s}-map.html'), f'public/dungeons/{s}-map.html', '../', 'Dungeons', 'dungeons/index.html',
           f"{z['title']} &middot; map", extra,
           og_card=f"dungeons-{s}", canon=f"dungeons/{s}-map")
# ---- tools
inject(os.path.join(SRC,'eql-sky-tracker.html'), 'public/tools/plane-of-sky.html', '../',
       'Tools', 'tools/index.html', 'Plane of Sky tracker', own_bar=True,
       og_card='tools', canon='tools/plane-of-sky')
inject(os.path.join(SRC,'eql-race-unlocks.html'), 'public/tools/race-unlocks.html', '../',
       'Tools', 'tools/index.html', 'Race unlock tracker',
       extra='<span class="ns-sep">/</span><a href="combo-calculator.html">Combo calculator &rarr;</a>',
       own_bar=True, og_card='tools', canon='tools/race-unlocks')
# calculator = same app, boots on the calc tab, shares the same save key
inject(os.path.join(SRC,'eql-race-unlocks.html'), 'public/tools/combo-calculator.html', '../',
       'Tools', 'tools/index.html', 'Race &amp; primary calculator',
       extra='<span class="ns-sep">/</span><a href="race-unlocks.html">&larr; Race unlocks</a>',
       subs=[(' show("track");\n})();', ' show("calc");\n})();'),
             ('<title>Race Unlock Tracker', '<title>Race &amp; Primary Calculator')],
       own_bar=True, og_card='tools', canon='tools/combo-calculator')
n += 3
if PH_MARKED:
    tot=sum(n for _,n in PH_MARKED)
    print(f'placeholder claims struck as historical: {tot} across {len(PH_MARKED)} surveys')
print(f"imported {n} pages")
