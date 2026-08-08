# Shared HTML partials for every page on the site.
import json, os
_cfg = json.load(open("site.config.json", encoding="utf-8")) if os.path.exists("site.config.json") else {}
SITE = _cfg.get("site_name", "EQL Source")
TAG  = _cfg.get("site_tagline", "Survey")

def head(title, desc, rel="", extra=""):
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
<link rel="preconnect" href="https://fonts.googleapis.com">
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
      <a href="{rel}learn/raid-access.html">Learn</a>
      <a href="{rel}sources.html">Accuracy</a>
    </nav>
  </div>
</header>'''

def foot(rel=""):
    return f'''<footer class="site-foot">
  <div class="shell">
    <div class="foot-grid">
      <div><h4>Dungeons</h4><ul>
        <li><a href="{rel}dungeons/index.html">All survey plates</a></li>
        <li><a href="{rel}dungeons/najena.html">Najena</a></li>
        <li><a href="{rel}dungeons/lowerguk.html">Lower Guk</a></li>
        <li><a href="{rel}dungeons/mistmoore.html">Castle Mistmoore</a></li>
      </ul></div>
      <div><h4>Raids</h4><ul>
        <li><a href="{rel}raids/index.html">Encounter index</a></li>
        <li><a href="{rel}raids/eye-of-veeshan.html">Eye of Veeshan</a></li>
      </ul></div>
      <div><h4>Tools</h4><ul>
        <li><a href="{rel}tools/plane-of-sky.html">Plane of Sky tracker</a></li>
        <li><a href="{rel}tools/race-unlocks.html">Race unlock tracker</a></li>
        <li><a href="{rel}tools/combo-calculator.html">Race and primary calculator</a></li>
        <li><a href="{rel}tools/index-search.html">The Index</a></li>
      </ul></div>
      <div><h4>Learn</h4><ul>
        <li><a href="{rel}learn/raid-access.html">How raid access works</a></li>
      </ul></div>
      <div><h4>About</h4><ul>
        <li><a href="{rel}sources.html">Sourcing standard</a></li>
        <li><a href="{rel}sources.html#gaps">Known gaps</a></li>
        <li><a href="{rel}sources.html#changelog">Change log</a></li>
      </ul></div>
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
