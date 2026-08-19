import os, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT,'_build'))
import json, re, shutil, os
from withheld import WITHHELD, REASON, MARK
# Phrases a survey must not type for itself — the experience ranking above all.
# See _build/derived.py for why one typed superlative became four typed
# ordinals before this existed.
import derived
from _partials import CSS_V, THEME_BOOT, FONTS, bar
_CFG = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"site.config.json"), encoding="utf-8"))
SITE = _CFG["site_name"]
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'source')
Z = json.load(open('assets/zones-index.json', encoding='utf-8'))
BY = {z['slug']: z for z in Z}

RETURN_CSS = ""

def bar_html(rel, crumb, crumb_href, here, extra=""):
    """The same leather running head as every other page.

    Surveys used to get a breadcrumb strip (`.ns-bar`) with no Dungeons / Raids
    / Tools / Learn. Opening a plate from the home spread felt like leaving
    the site for a PDF. The current mark is `crumb`, which already matches a
    nav label. `here` is the page name and belongs in the mast crumb, not in
    a second bar.
    """
    return bar(rel, current=crumb, extra=extra)

# Pages that already have a sticky bar of their own. Both bars pin to top:0,
# and this one wins on z-index, so on the race tracker it covered 73% of the
# tool's own tab-and-save bar the moment you scrolled. The breadcrumb is the
# less important of the two, so it stops following on those pages.
UNPIN = '<style>.ns-bar,.site-bar{position:static}</style>'

WH_CSS = """
<style>
.wh{font-family:"IBM Plex Mono",monospace;font-size:.82em;letter-spacing:.06em;
  text-transform:uppercase;color:var(--warn-t);border-bottom:1px dotted var(--warn-t)}
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


# THE INJECTED CHROME USES TOKENS, AND THESE PAGES USED TO HAVE NONE.
# Surveys and imported tools now load site.css. TOKENS_CSS is still emitted as
# a belt so a page that carries its own :root (race-unlocks) cannot lose
# --bone if the stylesheet link is skipped, and so the ns-bar paints before
# the external file arrives.
def _tokens_from_site_css():
    try:
        css = open('public/assets/site.css', encoding='utf-8').read()
        block = re.search(r':root\{(.*?)\}', css, re.S).group(1)
    except (OSError, AttributeError):
        return ''
    keep = ('--surface-0', '--surface-1', '--surface-2', '--ground', '--panel',
            '--panel2', '--rule', '--rule2', '--line', '--ink', '--bone',
            '--txt', '--mut', '--dim', '--faint', '--ok', '--warn', '--warn-t',
            '--ember', '--ember-t', '--instr', '--instr-t', '--brass', '--brass-t',
            '--lava', '--lava-t', '--r', '--speed', '--bind', '--bind-ink',
            '--bind-mut', '--bind-faint', '--bind-line', '--bar-bg', '--sheet',
            '--plot-bg')
    # Strip comments BEFORE splitting. site.css documents nearly every token
    # inline, so a declaration arrives as "/* why this value */\n  --bone:#F2EADA"
    # and splitting on ':' hands back the comment rather than the name. The
    # first version of this matched nothing at all and emitted an empty block,
    # which looks identical to working.
    block = re.sub(r'/\*.*?\*/', '', block, flags=re.S)
    out = []
    for decl in block.split(';'):
        if ':' not in decl:
            continue
        name, _, value = decl.partition(':')
        if name.strip() in keep:
            out.append(f'{name.strip()}:{value.strip()};')
    return '<style>:root{' + ''.join(out) + '}</style>' if out else ''


TOKENS_CSS = _tokens_from_site_css()

CONTACT_CSS = ""

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
.ph-old{text-decoration:line-through;text-decoration-color:var(--warn);
  text-decoration-thickness:1px;color:var(--faint)}
.ph-old-tag{font-family:"IBM Plex Mono",monospace;font-size:9px;letter-spacing:.12em;
  text-transform:uppercase;color:var(--warn-t);border:1px solid var(--warn);border-radius:2px;
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
    # Surveys and imported tools now load site.css (theme tokens, sheet grammar,
    # ns-bar, contact). TOKENS_CSS remains as a belt: race-unlocks still carries
    # its own stylesheet and must not lose --bone if the link is ever skipped.
    css_v = f'?v={CSS_V}' if CSS_V else ''
    chrome = (THEME_BOOT
              + '<link rel="preconnect" href="https://fonts.googleapis.com">'
              + '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
              + f'<link href="{FONTS}" rel="stylesheet">'
              + TOKENS_CSS + CONTACT_CSS
              + f'<link rel="icon" href="{rel}favicon.svg" type="image/svg+xml">'
              + f'<link rel="stylesheet" href="{rel}assets/site.css{css_v}">'
              + social + css)
    h = h.replace('</head>', chrome + '</head>', 1)
    h = re.sub(r'<body([^>]*)>', lambda m: '<body%s>\n' % m.group(1) + bar_html(rel, crumb, crumb_href, here, extra), h, count=1)
    if ('dungeons/' in dst.replace('\\', '/') and '<p class="crumb">' not in h
            and '<header class="mast">' in h):
        crumb_line = (f'  <p class="crumb"><a href="{rel}index.html">{SITE}</a> &nbsp;/&nbsp; '
                      f'<a href="{rel}{crumb_href}">{crumb}</a></p>\n')
        h = h.replace('<header class="mast">', '<header class="mast">\n' + crumb_line, 1)
    if ph_zone:
        z_ = BY.get(ph_zone, {})
        note = PH_CONFIRMED.replace('REL_', rel)
        # ONLY WHERE THERE ARE PERCENTAGES TO EXPLAIN.
        #
        # This fired on every survey unconditionally. Once the spawn
        # percentages came out of the Castle Mistmoore roster, the page carried
        # a note reading "percentages below are inherited classic data" above a
        # table with no percentages in it, and a link inviting the reader to
        # find out why they were still printed. A cold reader hunted for what
        # it was warning them about.
        #
        # The note is worth keeping where the percentages remain: deleting what
        # a source says is how a record stops being checkable. It just has to
        # be about something.
        roster = h[h.find('Named roster'):] if 'Named roster' in h else ''
        if not re.search(r'>\s*~?\d{1,3}%', roster):
            note = ''
        # above the roster, which is the table the percentages live in
        k = h.find('Named roster')
        if k > 0:
            k = h.find('</h2>', k) + len('</h2>')
            h = h[:k] + note + h[k:]
    if '</footer>' in h:
        h = h.replace('</footer>', CONTACT.replace('REL_', rel) + '\n</footer>', 1)
    if '</body>' in h:
        h = h.replace('</body>', f'<script src="{rel}assets/site.js"></script>\n</body>', 1)
    else:
        h += f'\n<script src="{rel}assets/site.js"></script>\n'
    open(dst, 'w', encoding='utf-8', newline='\n').write(h)
    return len(h)

n = 0
# ---- plates
for z in Z:
    s = z['slug']
    extra = ''
    n += 1
    inject(os.path.join(SRC, f'{s}.html'), f'public/dungeons/{s}.html', '../', 'Dungeons', 'dungeons/index.html',
           f"Survey {z['plate']:02d} &middot; {z['title']}", extra, wh_slug=s, ph_zone=s,
           subs=derived.tokens(s),
           og_card=f"dungeons-{s}", canon=f"dungeons/{s}")
# ---- tools
#
# WITHDRAWN 17 AUG 2026: tools/plane-of-sky.html.
# _build/source/eql-sky-tracker.html was injected here with assets/sky.json
# substituted into it. Sky Ledger replaces it — it reads the player's own log
# and, unlike ours, spends a held turn-in piece once instead of counting it
# against every test that wants it. The source file stays in _build/source/
# because _build/skydata.py's `--from-html` escape hatch reads it and
# assets/sky.json is still published at /data/, but nothing renders it now.
# /tools/plane-of-sky.html 301s to /tools/sky-ledger.html in public/_redirects.
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
n += 2
if PH_MARKED:
    tot=sum(n for _,n in PH_MARKED)
    print(f'placeholder claims struck as historical: {tot} across {len(PH_MARKED)} surveys')
print(f"imported {n} pages")
