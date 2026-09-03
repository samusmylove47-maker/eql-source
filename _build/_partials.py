# Shared HTML partials for every page on the site.
import json, os, hashlib
_cfg = json.load(open("site.config.json", encoding="utf-8")) if os.path.exists("site.config.json") else {}
SITE = _cfg.get("site_name", "EQL Source")
TAG  = _cfg.get("site_tagline", "Survey")


def _asset_v(path):
    """A short content hash, appended to the stylesheet URL.

    WHY THIS EXISTS, 16 Aug 2026
    ----------------------------
    assets/site.css is one stable URL that every page on the site loads, and it
    had no version on it. A browser that had seen the old file kept serving it:
    the whole repalette, the display face and both pieces of survey art were
    invisible in a browser that had loaded the site once before, and the page
    rendered as unstyled black shapes over a bare headline. It took a
    stylesheet-by-stylesheet inspection to find, because the site was correct
    and only the reader's copy was stale.

    Cloudflare publishes on every merge to main, so this is not a local
    annoyance: it is what every returning visitor would have seen after a
    redesign. The hash changes only when the file does, so an unchanged
    stylesheet still caches for as long as the host says.
    """
    try:
        return hashlib.sha1(open(path, 'rb').read()).hexdigest()[:8]
    except OSError:
        return ''


CSS_V = _asset_v('public/assets/site.css')
# THE FOUR FACES ARE SERVED FROM THIS ORIGIN, AND THAT IS THE POINT.
#
# Until 30 August 2026 these three lines were a preconnect to
# fonts.googleapis.com, a preconnect to fonts.gstatic.com, and a stylesheet from
# the first — on every page. So 715 of 717 published pages disclosed a reader's
# IP address to Google before anything rendered, and several of those pages said
# "Nothing transmitted" while doing it. We had published that exact criticism
# about a collaborator's application.
#
# Served from here the disclosure stops existing rather than being disclosed
# better. The files are byte-identical copies fetched once by
# _build/fetchfonts.py; see that file for why they are Google's own subsets
# rather than ours.
FONTS_V = _asset_v('public/assets/fonts/fonts.css')

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
# WITHDRAWN 18 AUG 2026: character sheet, planar gear targets, inventory reader.
# All three are superseded by 50 Upgrades, which does what each of them did and
# does it against a catalogue none of them had: a trio's eligibility as the
# union of three classes, every slot, every item from +0 to +10, and an
# inventory it reads for itself. Shipping a worse copy of something already
# available is the rule this project applies to other people's tools; it applies
# to ours.
#
# Same shape as the Sky tracker withdrawal on 17 Aug and the same handling: the
# pages are deleted, the reason stays here where the next session will look, the
# change log records it, and there is no tombstone page. The old URLs 301 to
# 50 Upgrades in public/_redirects, in both address forms.
#
# _build/planardata.py and _build/inventory.py both SURVIVE and are no part of
# this. Neither renders a page: the first writes assets/planar.json, which the
# measured-drop matcher needs or it discards every planar set drop as trash, and
# the second writes assets/item-ids.json, published as items.v1.json.
# THE "=" IS IDENTITY. THE LINE BESIDE IT IS THE DESCRIPTION.
#
# Ruled 31 Aug 2026. EQLS reads aloud as "equals", so the tools are one family:
# =Index, =Sky, =Upgrades, =Gaps, =Lockouts, =Races, =Combos, =Faction. That
# makes eight tools legible as one product rather than eight unrelated ones,
# which was its own audit finding.
#
# IT DOES NOT SOLVE THE STRANGER TEST AND IS NOT ASKED TO. The audit found our
# names tell a stranger nothing, and "=Lockouts" tells them no more than
# "Lockouts" did - the prefix is identity, not description. The Director
# collapsed those two problems and unfixed them when I said so. So every entry
# carries `tagline`: the sentence that does the descriptive work, written for
# somebody who has never heard of this site and wants to know whether the thing
# is for them.
#
# `name` IS DISPLAY ONLY AND SO IS `foot`. Every URL on this site is built from
# `slug` (see _foot_links, line 277), so renaming a tool moves no address and
# breaks no share card, no canonical, no sitemap entry and no external link.
# That is why this rename is safe and why a SLUG rename would not be.
TOOLS = [
    dict(slug="index-search",     name="=Index", foot="=Index",
         tagline="Every item and named mob we have recorded, searchable in one place"),
    # Replaced tools/plane-of-sky.html on 17 Aug 2026. Ours counted a held
    # turn-in piece against every test that wanted it; Sky Ledger spends each
    # unit once. Two Sky trackers is the "which do I use" problem and after
    # that property the older one is the wrong answer.
    dict(slug="sky-ledger",       name="=Sky", foot="=Sky",
         tagline="Which Plane of Sky class unlocks you can hand in right now"),
    # A gear planner built in its own repository and hosted there. This site
    # carries a description page and links out; the application is not ours to
    # serve and its data is refreshed on its own cadence.
    dict(slug="50-upgrades",      name="=Upgrades", foot="=Upgrades",
         tagline="What to wear at 50, for a trio, across every slot"),
    # Session E's gap engine. The page is a PREVIEW: the engine runs in its own
    # repository and is not yet a bundle this site can serve, so the page renders
    # a synthetic fixture and says so rather than offering a control that does
    # nothing.
    dict(slug="gap-engine",       name="=Gaps", foot="=Gaps",
         tagline="Reads your combat log and says what to change, and what it will not answer"),
    # Promoted 26 Aug 2026, having been copied into public/app/ on the 25th and
    # deliberately left unlinked until Session D reported. It is the only tool
    # here that answers "what is still open", and it says "not looked" where it
    # has no history rather than guessing.
    dict(slug="lockouts",         name="=Lockouts", foot="=Lockouts",
         tagline="What is still open to you this week, read from your own log"),
    dict(slug="race-unlocks",     name="=Races", foot="=Races",
         tagline="Which races you have unlocked and what each one still costs"),
    dict(slug="combo-calculator", name="=Combos", foot="=Combos",
         tagline="Pick the class that must sit in your primary slot, and cost every route to it"),
    dict(slug="faction-impact",   name="=Faction", foot="=Faction",
         tagline="What killing in a zone does to every faction it touches"),
]

# `blurb` is what the Learn hub prints under each title. It lives here so the
# hub, the footer and the nav all read one list — six Learn pages existed and
# the header's Learn link went to one article, with no way to see the rest.
LEARN = [
    dict(slug="still-true", name="Is it still true?",
         blurb="Inherited advice, tested against Legends. What classic did, what happens now, "
               "the evidence with tiers and dates, and what would settle the open ones."),
    dict(slug="difficulty", name="What difficulty changes",
         blurb="D0 to D4 does not raise mob levels. What it does raise, and one boss measured at "
               "all five tiers showing where the class kit widens."),
    dict(slug="motes", name="Motes, and what they are worth", foot="Motes",
         blurb="Spells scale doubled, items scale flat. That one difference decides every mote "
               "decision, including why converting them upward costs you."),
    dict(slug="raid-access", name="How raid access works",
         blurb="Instances, lockouts and voidlings. Which door gives you the boss and which gives "
               "you an empty zone."),
    dict(slug="deity", name="Deity, and the level 11 lock",
         blurb="The third permanent choice, and how permanent it actually is."),
    dict(slug="reading-the-plans", name="How to read a floor plan",
         foot="Reading a floor plan",
         blurb="What the floor plans draw, what they deliberately leave out, and what a combat "
               "log can and cannot tell you."),
    dict(slug="contamination", name="What the scanner finds here",
         foot="Contamination",
         blurb="We scan our own pages for Project 1999 conventions and publish what turns up. "
               "Pointed at us, not at anybody else."),
]

_WORDS = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six",
          7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten"}


def wordnum(n):
    """Small numbers read better as words in a headline, and the headline must
    still be printed from the list rather than typed."""
    return _WORDS.get(n, str(n))


SITE_URL = _cfg.get("site_url", "").rstrip("/")


def public_path(rel):
    """The address a built page is actually served at, relative to the site root.

    ONE RULE, TWO CONSUMERS. head() writes it into <link rel="canonical"> and
    _build/sitemap.py writes it into <loc>. They disagreed until 18 Aug 2026,
    and both were wrong in different ways:

      - the sitemap listed 716 URLs ending .html, every one of which 307s;
      - the ten index pages named a canonical that also 307s, because their
        generators pass canon="dungeons/index" and the host serves that at
        /dungeons/.

    A canonical that redirects is a page telling a search engine its own address
    is somewhere else, which is the one thing a canonical exists not to say.
    Nothing was broken for a reader — every form resolves — but a sitemap of
    redirecting URLs is indexed as redirects rather than as pages.

    Accepts either a built path (`public/dungeons/index.html`, `index.html`) or
    a bare canon string (`dungeons/index`), because the two callers hold
    different things and normalising here means neither has to remember.
    """
    rel = rel.replace(os.sep, "/")
    if rel.startswith("public/"):
        rel = rel[len("public/"):]
    if rel.endswith(".html"):
        rel = rel[:-len(".html")]
    if rel == "index":
        return ""                       # the site root, served at /
    if rel.endswith("/index"):
        return rel[:-len("index")]      # keeps the trailing slash: dungeons/
    return rel


def head(title, desc, rel="", extra="", og="home", canon=None, robots=None):
    """Page head.

    `og` names the share card in public/assets/og/. `canon` is the page's path
    from the site root, without the .html — that is the address a search engine
    should keep and the one a canonical tag has to name.

    This said the host "301s" .html to the extensionless form. It does not: it
    answers 307, measured live on 1 Sep 2026. The distinction matters because a
    307 is temporary and passes nothing on, which is exactly why the canonical
    tag has to carry the claim rather than the status code. Internal links are
    extensionless now, so nothing on the site follows that redirect anyway.
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
        # Normalised rather than trusted. Every generator passes its own canon
        # string and ten of them passed "<dir>/index", which the host 307s.
        lines.append(f'<link rel="canonical" href="{SITE_URL}/{public_path(canon)}">')
    # The archive republishes coordinates we have since established are wrong.
    # Keeping it verbatim is right; letting a search engine land a reader on it
    # is not - "kept verbatim" was allowed to override "marked on sight".
    robots_tag = f'<meta name="robots" content="{robots}">' if robots else ""
    social = "\n".join(lines) + "\n"
    canonical = ""

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{robots_tag}
<title>{title} — {SITE}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title} — {SITE}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
{social}{canonical}<link rel="stylesheet" href="{rel}assets/fonts/fonts.css{'?v=' + FONTS_V if FONTS_V else ''}">
<link rel="icon" href="{rel}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{rel}assets/site.css{'?v=' + CSS_V if CSS_V else ''}">
<script>/* Torchlight is the default and the CSS says so, so this only ever has
   work to do for a reader who chose daylight. It runs before first paint to
   avoid a flash of the wrong ground, and it is wrapped because localStorage
   throws outright in a browser with cookies blocked - the site must render
   dark in that case, not fail to render. */
(function(){{try{{var t=localStorage.getItem("eqls-theme");
if(t==="light"||t==="dark")document.documentElement.setAttribute("data-theme",t);}}catch(e){{}}}})()</script>
{extra}</head>
<body>'''

NAME_INDEX = next(t['name'] for t in TOOLS if t['slug'] == 'index-search')

# PLAIN LANGUAGE IN THE NAV, THE BRAND EVERYWHERE ELSE.
#
# The global nav read "=Index" - the product name, in the one place a stranger
# looks first, telling them nothing. It reads "Items & mobs" now. The footer,
# the tools hub and the tool pages keep the "=" mark, which is the brand rather
# than decoration, and NAME_INDEX still drives those.
#
# This deliberately reintroduces two labels for one tool, a day after they were
# unified. The unification was right: the fault was four places drifting BY
# ACCIDENT. Two labels chosen for two audiences is a decision, and both still
# come from this file.
#
# The note is here and not beside the markup: written into the f-string it
# shipped on all 717 pages and moved the hero 632 bytes down. Third time.
_NAV_INDEX = NAME_INDEX

def bar(rel=""):
    # THE HOME LINK IS THE ONE HREF THAT CANNOT SIMPLY LOSE ITS FILENAME.
    # `rel` is "" on a root page, so `{rel}index.html` would become an empty
    # href, which a browser reads as "this page" - the masthead would stop
    # leading home from the home page. "./" is the root of the current
    # directory, which is what index.html was.
    HOME = rel or "./"
    return f'''<header class="site-bar">
  <div class="shell">
    <a class="mark" href="{HOME}"><span class="m1">{SITE}</span><span class="m2">{TAG}</span></a>
    <button class="burger" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="site-nav" id="nav">
      <a href="{rel}dungeons/">Dungeons</a>
      <a href="{rel}raids/">Raids</a>
      <a href="{rel}tools/">Tools</a>
      <a href="{rel}tools/index-search">Items &amp; mobs</a>
      <a href="{rel}learn/">Learn</a>
      <a href="{rel}sources">Accuracy</a>
      <a href="{rel}search" class="nav-find">Site search</a>
    </nav>
    <button class="lamp" type="button">
      <svg class="lantern" viewBox="0 0 100 126" fill="none" stroke="currentColor"
        stroke-width="1.15" stroke-linejoin="round" aria-hidden="true" focusable="false">
        <path d="M50 4v10"/><path d="M34 20h32l6 10H28Z"/><path d="M30 30v60h40V30"/>
        <path d="M26 90h48l-5 10H31Z"/><path d="M38 38v44M50 34v52M62 38v44" opacity=".55"/>
        <ellipse cx="50" cy="62" rx="9" ry="13" opacity=".7"/>
        <path d="M34 14a16 8 0 0 1 32 0" stroke-width=".9"/>
      </svg>
      <span class="lamp-to-day">Daylight</span><span class="lamp-to-torch">Torchlight</span>
    </button>
  </div>
</header>
<script>/* Labelled by DESTINATION, not by state: it reads DAYLIGHT while you are
   in torchlight. The label itself is set in CSS so it is correct before this
   runs and stays correct with JavaScript off; only the switching needs script.
   A CSS-only toggle would need a checkbox ahead of every themed element in
   source order, and the chrome is injected into pages whose body order we do
   not control. */
(function(){{var b=document.querySelector(".lamp");if(!b)return;
b.addEventListener("click",function(){{var d=document.documentElement;
var next=d.getAttribute("data-theme")==="light"?"dark":"light";
d.setAttribute("data-theme",next);
try{{localStorage.setItem("eqls-theme",next);}}catch(e){{}}}});}})()</script>'''

# EQLS AURAS IS NOT IN `TOOLS`, AND IT STILL NEEDS A ROUTE IN.
#
# It is Shara's product rather than one of our browser trackers, so it is not in
# the registry: adding it there would change the tool count, demand a card on a
# hub whose heading counts trackers, and generate a tools/ page for a thing that
# is downloaded rather than run in a tab.
#
# But until 2 Sep 2026 THE ONLY LINK TO /auras ON THE WHOLE SITE WAS INSIDE THE
# HOME PAGE'S FEATURED BAND. Measured: two pages carried the href, and one of
# them was /auras itself, which is not a route in. When the featured slot rotates
# to another product the site's only door to this one rotates with it, and no
# check would say a word - the footer rule tests registered tools, and this is
# not one.
#
# So it is a hand-written entry beside the generated ones. The name is read from
# assets/auras.json rather than typed, because her name lives in one place and
# this file is not it.
AURAS_NAME = json.load(open('assets/auras.json', encoding='utf-8'))['name']


def _foot_links(items, folder, rel):
    """Footer list items for a registry. Generated so the footer cannot drift
    from the pages it is meant to link."""
    return "\n".join(
        f'        <li><a href="{rel}{folder}/{it["slug"]}">'
        f'{it.get("foot", it["name"])}</a></li>' for it in items)


def foot(rel=""):
    return f'''<footer class="site-foot">
  <div class="shell">
    <div class="foot-grid">
      <nav aria-label="Dungeons"><p class="fh">Dungeons</p><ul>
        <li><a href="{rel}dungeons/">All surveys</a></li>
        <li><a href="{rel}dungeons/najena">Najena</a></li>
        <li><a href="{rel}dungeons/lowerguk">Lower Guk</a></li>
        <li><a href="{rel}dungeons/mistmoore">Castle Mistmoore</a></li>
        <li><a href="{rel}items/">Every item</a></li>
        <li><a href="{rel}named/">Every named mob</a></li>
        <li><a href="{rel}sets/">Every planar set</a></li>
      </ul></nav>
      <nav aria-label="Raids"><p class="fh">Raids</p><ul>
        <li><a href="{rel}raids/">Encounter index</a></li>
        <li><a href="{rel}raids/plane-of-sky">Plane of Sky, island by island</a></li>
      </ul></nav>
      <nav aria-label="Tools"><p class="fh">Tools</p><ul>
{_foot_links(TOOLS, "tools", rel)}
        <li><a href="{rel}auras">{AURAS_NAME}</a></li>
      </ul></nav>
      <nav aria-label="Learn"><p class="fh">Learn</p><ul>
{_foot_links(LEARN, "learn", rel)}
      </ul></nav>
      <nav aria-label="About"><p class="fh">About</p><ul>
        <li><a href="{rel}search">Search the site</a></li>
        <li><a href="{rel}data/">Public data</a></li>
        <li><a href="{rel}credits">Credits</a></li>
        <li><a href="{rel}archive/">The original plates</a></li>
        <li><a href="{rel}sources">Sourcing standard</a></li>
        <li><a href="{rel}sources#gaps">Known gaps</a></li>
        <li><a href="{rel}sources#changelog">Change log</a></li>
      </ul></nav>
    </div>
    <div class="foot-contact">
      <p><strong>Found something the site gets wrong, or something the wiki does?</strong>
        That is the most useful thing anyone can send us, and every finding is credited by name.
        <a href="https://github.com/samusmylove47-maker/eql-source/issues/new?template=finding.yml">Send
        a finding</a> &middot; <a href="{rel}learn/still-true">see what is already open</a>.</p>
      <p class="foot-nolog">Please do not attach a combat log to a public issue &mdash; they can
        carry private chat. Say you have one and we will ask.</p>
    </div>
    <p class="foot-legal">
      Every claim on this site names its source and the date that source was read. Where a source is
      uncertain, contradicted or stale, the page says so rather than smoothing it over.<br>
      Unofficial fan resource. Not affiliated with or endorsed by Daybreak Game Company, Game Jawn
      or Darkpaw Studios. EverQuest is a registered trademark of Daybreak Game Company LLC.
    </p>
    <svg class="rule-mark" width="100%" height="9" viewBox="0 0 1160 9"
      preserveAspectRatio="none" fill="none" stroke="currentColor" stroke-width="1"
      aria-hidden="true" focusable="false"><path d="M0 4.5h486"/><path
      d="M674 4.5h486"/><path d="M580 1l7 3.5-7 3.5-7-3.5z"/><path
      d="M508 4.5h44M608 4.5h44" stroke-width=".7" opacity=".75"/><path
      d="M566 4.5h-8M594 4.5h8" stroke-width=".7" opacity=".5"/></svg>
  </div>
</footer>
<script src="{rel}assets/site.js"></script>
</body>
</html>'''
