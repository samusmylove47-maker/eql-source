# Shared HTML partials for every page on the site.
import json, os
_cfg = json.load(open("site.config.json", encoding="utf-8")) if os.path.exists("site.config.json") else {}
SITE = _cfg.get("site_name", "EQL Source")
TAG  = _cfg.get("site_tagline", "Survey")

# ---------------------------------------------------------------------------
# The site's own navigation registries. Nothing here may be typed twice.
#
# The footer was hand-written and drifted: it listed four tools of five, and the
# faction impact checker - the most original tool on the site - appeared in no
# footer on any page, reachable only from the tools index. The tools index said
# "Five trackers" while the home page said "Three". One list fixes all of it,
# and scripts/check.py fails the build if a file in public/tools/ is missing
# from TOOLS.
#
# `name` is the display name. `foot` is the shorter footer label where the full
# name would wrap; where they are the same, `foot` is omitted.
TOOLS = [
    dict(slug="character",        name="Character sheet"),
    dict(slug="index-search",     name="The Index"),
    dict(slug="plane-of-sky",     name="Plane of Sky tracker"),
    dict(slug="race-unlocks",     name="Race unlock tracker"),
    dict(slug="combo-calculator", name="Race and primary calculator"),
    dict(slug="faction-impact",   name="Faction impact checker"),
]

LEARN = [
    dict(slug="still-true",  name="Is it still true?"),
    dict(slug="raid-access", name="How raid access works"),
    dict(slug="difficulty",  name="What difficulty changes"),
    dict(slug="deity",       name="Deity, and the level 11 lock"),
]

_WORDS = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six",
          7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten"}


def wordnum(n):
    """Small numbers read better as words in a headline, and the headline must
    still be printed from the list rather than typed."""
    return _WORDS.get(n, str(n))


SITE_URL = _cfg.get("site_url", "").rstrip("/")


def head(title, desc, rel="", extra="", og="home", canon=None):
    """Page head.

    `og` names the share card in public/assets/og/. `canon` is the page's path
    from the site root, without the .html — the host 301s .html to the
    extensionless form, so that is the address a search engine should keep and
    the one a canonical tag has to name.
    """
    # Share cards must be absolute: Discord and Twitter fetch them from their own
    # servers, where a relative path resolves to nothing.
    card = f"{SITE_URL}/assets/og/{og}.png" if SITE_URL else f"{rel}assets/og/{og}.png"
    lines = [
        f'<meta property="og:image" content="{card}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:site_name" content="{SITE}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{title} — {SITE}">',
        f'<meta name="twitter:description" content="{desc}">',
        f'<meta name="twitter:image" content="{card}">',
    ]
    if canon is not None and SITE_URL:
        lines.append(f'<link rel="canonical" href="{SITE_URL}/{canon}">')
    social = "\n".join(lines) + "\n"
    canonical = ""

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — {SITE}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title} — {SITE}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
{social}{canonical}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Public+Sans:wght@400;600&family=Saira+Condensed:wght@600;700&display=swap" rel="stylesheet">
<link rel="icon" href="{rel}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{rel}assets/site.css">
{extra}</head>
<body>'''

def bar(rel=""):
    return f'''<header class="site-bar">
  <div class="shell">
    <a class="mark" href="{rel}index.html"><span class="m1">{SITE}</span><span class="m2">{TAG}</span></a>
    <button class="burger" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="site-nav" id="nav">
      <a href="{rel}tools/index.html">Tools</a>
      <a href="{rel}tools/index-search.html">The Index</a>
      <a href="{rel}raids/index.html">Raids</a>
      <a href="{rel}dungeons/index.html">Dungeons</a>
      <a href="{rel}learn/still-true.html">Learn</a>
      <a href="{rel}sources.html">Accuracy</a>
    </nav>
  </div>
</header>'''

def _foot_links(items, folder, rel):
    """Footer list items for a registry. Generated so the footer cannot drift
    from the pages it is meant to link."""
    return "\n".join(
        f'        <li><a href="{rel}{folder}/{it["slug"]}.html">'
        f'{it.get("foot", it["name"])}</a></li>' for it in items)


def foot(rel=""):
    return f'''<footer class="site-foot">
  <div class="shell">
    <div class="foot-grid">
      <div><h4>Dungeons</h4><ul>
        <li><a href="{rel}dungeons/index.html">All surveys</a></li>
        <li><a href="{rel}dungeons/najena.html">Najena</a></li>
        <li><a href="{rel}dungeons/lowerguk.html">Lower Guk</a></li>
        <li><a href="{rel}dungeons/mistmoore.html">Castle Mistmoore</a></li>
        <li><a href="{rel}items/index.html">Every item</a></li>
        <li><a href="{rel}named/index.html">Every named mob</a></li>
      </ul></div>
      <div><h4>Raids</h4><ul>
        <li><a href="{rel}raids/index.html">Encounter index</a></li>
        <li><a href="{rel}raids/plane-of-sky.html">Plane of Sky, island by island</a></li>
        <li><a href="{rel}raids/eye-of-veeshan.html">Eye of Veeshan</a></li>
      </ul></div>
      <div><h4>Tools</h4><ul>
{_foot_links(TOOLS, "tools", rel)}
      </ul></div>
      <div><h4>Learn</h4><ul>
{_foot_links(LEARN, "learn", rel)}
      </ul></div>
      <div><h4>About</h4><ul>
        <li><a href="{rel}archive/index.html">The original plates</a></li>
        <li><a href="{rel}sources.html">Sourcing standard</a></li>
        <li><a href="{rel}sources.html#gaps">Known gaps</a></li>
        <li><a href="{rel}sources.html#changelog">Change log</a></li>
      </ul></div>
    </div>
    <div class="foot-contact">
      <p><strong>Found something the site gets wrong, or something the wiki does?</strong>
        That is the most useful thing anyone can send us, and every finding is credited by name.
        <a href="https://github.com/samusmylove47-maker/eql-source/issues/new?template=finding.yml">Send
        a finding</a> &middot; <a href="{rel}learn/still-true.html">see what is already open</a>.</p>
      <p class="foot-nolog">Please do not attach a combat log to a public issue &mdash; they can
        carry private chat. Say you have one and we will ask.</p>
    </div>
    <p class="foot-legal">
      Every claim on this site names its source and the date that source was read. Where a source is
      uncertain, contradicted or stale, the page says so rather than smoothing it over.<br>
      Unofficial fan resource. Not affiliated with or endorsed by Daybreak Game Company, Game Jawn
      or Darkpaw Studios. EverQuest is a registered trademark of Daybreak Game Company LLC.
    </p>
  </div>
</footer>
<script src="{rel}assets/site.js"></script>
</body>
</html>'''
