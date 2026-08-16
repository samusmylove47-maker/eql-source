"""items/ and named/ — one page per item and per named mob.

WHY
---
eqlwiki wins every long-tail item search for one structural reason: it has a
page per item and we have none. Everything we hold about the 452 items and 209
named mobs lives inside a client-side search on one page, so the delivered HTML
contains zero item rows and there is nothing to crawl, link, or paste.

This generates the pages that were missing. Every one is a real address a reader
can bookmark or drop into chat, cross-linked to the survey it came from.

ONE PAGE PER NAME, NOT PER ROW
------------------------------
Six item names appear in two zones each - Red Dragon Scales drops in Nagafen's
Lair and The Hole, Gargoyle Eye in Lower Guk and Castle Mistmoore. Making two
pages would split the answer and force a slug like red-dragon-scales-2 on
whichever lost the race. One page per name, listing every zone that drops it, is
both the honest shape and the one a reader wants.

THIN PAGES ARE THE RISK, SO THESE ARE NOT THIN
----------------------------------------------
An item page carries its slot, stats, class and race restrictions, every mob
that drops it and every zone, plus the level band of those zones. A named page
carries level, race and class, position, its notes, and everything it drops with
the stats of each. Both link back to the survey and to each other. That is a
page worth landing on rather than a stub built to farm a search engine.

Where a field is unrecorded it says so. 157 items have no class list because
they come from quest-component tables that carry no class column, and the page
says that rather than leaving a blank that reads as "no restrictions".
"""
import json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

Z = {z['slug']: z for z in json.load(open('assets/zones-index.json', encoding='utf-8'))}
IX = json.load(open('assets/index-data.json', encoding='utf-8'))
# What we have watched drop, joined by _build/sightings.py. This is the only
# thing on these pages that is not a transcription of somebody else's wiki.
try:
    SIGHT = json.load(open('assets/sightings.json', encoding='utf-8'))
except (OSError, ValueError):
    SIGHT = {'by_named': {}, 'by_item': {}}

CLASSES = {
    "WAR": "Warrior", "CLR": "Cleric", "PAL": "Paladin", "RNG": "Ranger",
    "SHD": "Shadow Knight", "DRU": "Druid", "MNK": "Monk", "BRD": "Bard",
    "ROG": "Rogue", "SHM": "Shaman", "NEC": "Necromancer", "WIZ": "Wizard",
    "MAG": "Magician", "ENC": "Enchanter", "BST": "Beastlord", "BER": "Berserker",
}


def slug(s):
    s = re.sub(r'&[a-z]+;', ' ', s)
    s = re.sub(r"[^\w\s-]", '', s.lower())
    return re.sub(r'[\s_]+', '-', s).strip('-')[:60]


def display(name):
    """Lowercase a leading article, leave everything else exactly as typed.

    In EverQuest the article is meaningful: "a dracoliche" is one of many and
    "Drelzna" is the only one. An audit asked for the A-Z to be title-cased,
    which would erase that distinction on every generic mob. What is genuinely
    inconsistent is only the article's own case - the source writes both
    "A cloaked dhampyre" and "a dracoliche" - so that is all this touches.
    """
    return re.sub(r'^(An?|The)\b', lambda m: m.group(1).lower(), name)


def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


CSS = '''<style>
.ent{max-width:74ch}
.ent .facts{list-style:none;margin:20px 0 0;padding:0;display:grid;
  grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:2px 22px}
.ent .facts div{padding:9px 0;border-top:1px solid var(--line)}
.ent .facts dt{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--faint);margin:0 0 3px}
.ent .facts dd{margin:0;color:var(--ink);font-size:15px}
.ent .facts dd.none{color:var(--faint);font-style:italic}
.srcs{list-style:none;margin:22px 0 0;padding:0;display:grid;gap:9px}
.srcs li{border-left:3px solid var(--c);background:var(--panel,#1E1914);padding:12px 15px;
  border-radius:0 4px 4px 0}
.srcs b{color:var(--ink)}
.srcs span{display:block;font-family:"IBM Plex Mono",monospace;font-size:11.5px;
  color:var(--faint);margin-top:3px}
.srcs a{color:var(--ink)}
.drops{list-style:none;margin:18px 0 0;padding:0;display:grid;
  grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:7px}
.drops li{border-left:2px solid var(--line);padding:3px 0 3px 10px;font-size:14px;color:var(--dim)}
.drops a{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--line)}
.drops span{display:block;font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--faint)}
.drops.seen li{border-left-color:var(--ok)}
.drops.seen b{color:var(--ink)}
.src{margin:0;font-size:13px;color:var(--dim)}
.src a{color:var(--dim)}
</style>'''


def seen_block(rows, label):
    """Tier M sightings. A count of times watched, never a rate."""
    if not rows:
        return ''
    li = ''.join(
        f'<li><b>{esc(r["item"] if "item" in r else r["mob"])}</b>'
        f'<span>seen {r["n"]}&times; &middot; '
        + ' &middot; '.join(
            esc(f'{x["date"]}' + (f' D{x["difficulty"]}' if x.get('difficulty') is not None else ''))
            for x in r['sessions'][:3])
        + '</span></li>' for r in rows)
    return (f'<h2 class="sec">{label}</h2><ul class="drops seen">{li}</ul>'
            f'<p class="src">Counted from our own combat logs. <b>A count, not a rate</b> '
            f'&mdash; a drop seen once is seen once. '
            f'<a href="../learn/reading-the-plans.html#measured">What a log can tell you</a>.</p>')


def page(kind, title, eyebrow, accent, facts, extra_html, desc, canon):
    rows = ''.join(
        f'<div><dt>{k}</dt><dd{" class=\'none\'" if v is None else ""}>'
        f'{v if v is not None else "not recorded"}</dd></div>'
        for k, v in facts)
    return (head(title, desc, rel="../", extra=CSS, og="dungeons", canon=canon)
            + bar("../") + f'''
<main>
<section class="hero page">
  <div class="shell ent" style="--c:{accent}">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp;
      <a href="../tools/index-search.html">The Index</a> &nbsp;/&nbsp; {eyebrow}</p>
    <h1 class="display">{esc(title)}</h1>
    <dl class="facts">{rows}</dl>
  </div>
</section>
<section class="band" style="border-top:0;padding-top:0">
  <div class="shell ent" style="--c:{accent}">{extra_html}</div>
</section>
</main>
''' + foot("../"))


os.makedirs('public/items', exist_ok=True)
os.makedirs('public/named', exist_ok=True)

# ---- items, one page per distinct name --------------------------------------
# Fragments are not items. A loot cell reading "Mithril Vambraces <br> Greaves"
# was split into two, and "Greaves" got a page, a canonical URL and a share card.
# They are suppressed here and printed on their parent's page instead, as what
# the source row actually says. See assets/catalogue-fixes.json.
FRAG = collections.defaultdict(list)
for it in IX['items']:
    if it.get('kind') == 'fragment':
        FRAG[it['parent']].append(it['n'])

by_item = collections.OrderedDict()
for it in IX['items']:
    if it.get('kind') == 'fragment':
        continue
    by_item.setdefault(it['n'], []).append(it)

drops_by_mob = collections.defaultdict(list)
for it in IX['items']:
    if it.get('kind') == 'fragment':
        continue                      # no page to link to
    src = (it.get('d') or '').split('·')[0].strip()
    if src:
        drops_by_mob[(it['z'], src)].append(it)

# Counted by extract.py so this page cannot disagree with the home page or The
# Index, which it did. n_items below still counts what this loop writes, and
# check.py compares the two - if they ever part, one of them is wrong and we
# want to know rather than to pick.
n_items_declared = IX['counts']['item_pages']
n_groups_declared = IX['counts']['item_groups']
GROUP_NAMES = {i['n'] for i in IX['items'] if i.get('kind') == 'group'}
n_items = n_groups = 0
for name, rows in by_item.items():
    a = rows[0]
    cls = a['c']
    cls_txt = ("Every class" if cls == ["ALL"]
               else ', '.join(CLASSES.get(c, c) for c in cls) if cls else None)
    zones = ''.join(
        f'<li><b><a href="../dungeons/{r["z"]}.html">{esc(r["zt"])}</a></b>'
        f'{" &mdash; off " + esc(r["d"]) if r.get("d") else ""}'
        f'<span>Survey {r["p"]:02d} &middot; levels {esc(Z[r["z"]]["levels"].split(" (")[0])}'
        f' &middot; ZEM {Z[r["z"]]["zem"]}</span></li>' for r in rows)
    # This line used to run fifteen words and appeared on all 446 item pages -
    # 6,690 words of the same sentence, the largest single block of repeated text
    # on the site. The survey is already linked above it; this only has to name
    # whose figures they are.
    also = sorted(set(FRAG.get(name, [])))
    also_html = (f'<p class="src" style="margin-top:14px"><b>The source row also lists:</b> '
                 f'{", ".join(esc(x) for x in also)}. We have not reconstructed full names for '
                 f'these &mdash; the row elides a shared prefix and guessing it would invent an '
                 f'item.</p>') if also else ''
    seen = seen_block(SIGHT['by_item'].get(name, []), 'Seen dropping, in our logs')
    extra = (f'<h2 class="sec">Where it drops</h2><ul class="srcs">{zones}</ul>{seen}{also_html}'
             f'<p class="src" style="margin-top:18px">Figures are the survey&rsquo;s own. '
             f'<a href="../sources.html">How we source</a>.</p>')
    desc = (f"{name} in EverQuest Legends: "
            + (f"{a['sr']}. " if a.get('sr') else "")
            + (f"{a['st'][:90]}. " if a.get('st') else "")
            + f"Drops in {', '.join(sorted({r['zt'] for r in rows}))}.")
    facts = [
        ("Slot", esc(a['sr']) if a.get('sr') else None),
        # Where a loot row listed several items behind one stats cell, the stats
        # describe the row and not this item. Say which rather than assert them.
        ("Stats" if not a.get('shared') else "Stats, from a shared row",
         (esc(a['st']) + ('' if not a.get('shared') else
          ' <em style="color:var(--faint)">&mdash; this row lists several items '
          'behind one stats cell, so this line describes the row</em>'))
         if a.get('st') else None),
        ("Classes", esc(cls_txt) if cls_txt else None),
        ("Zones", esc(', '.join(sorted({r['zt'] for r in rows})))),
    ]
    if a.get('kind') == 'group':
        facts.insert(0, ("What this is",
                         "A family named by the survey row, not a single item"))
    s = slug(name)
    open(f'public/items/{s}.html', 'w', encoding='utf-8', newline='\n').write(
        page("item", name, "Item", a['a'], facts, extra, desc[:180], f"items/{s}"))
    if name in GROUP_NAMES:
        n_groups += 1
    else:
        n_items += 1

# ---- named mobs -------------------------------------------------------------
n_named = 0
for nm in IX['named']:
    s = slug(nm['n'])
    drops = drops_by_mob.get((nm['z'], nm['n']), [])
    dl = ''.join(
        f'<li><a href="../items/{slug(d["n"])}.html">{esc(d["n"])}</a>'
        f'<span>{esc(d["sr"] or d["s"])}{" &middot; " + esc(d["st"][:60]) if d.get("st") else ""}</span></li>'
        for d in drops)
    extra = (f'<h2 class="sec">What it drops</h2><ul class="drops">{dl}</ul>'
             if drops else
             '<p class="lede">No drops recorded &mdash; a gap, not an empty mob.</p>')
    extra += seen_block(SIGHT['by_named'].get(nm['n'], []), 'Seen dropping, in our logs')
    extra += (f'<p class="src" style="margin-top:18px">From the '
              f'<a href="../dungeons/{nm["z"]}.html">{esc(nm["zt"])} survey</a>.</p>')
    desc = (f"{nm['n']} in {nm['zt']}, EverQuest Legends"
            + (f", level {nm['lv']}" if nm.get('lv') else "")
            + (f". {nm['no'][:100]}" if nm.get('no') else "."))
    facts = [
        ("Level", esc(nm['lv']) if nm.get('lv') else None),
        ("Race and class", esc(nm['rc']) if nm.get('rc') else None),
        ("Position", esc(nm['loc']) if nm.get('loc') else None),
        ("Zone", f'<a href="../dungeons/{nm["z"]}.html">{esc(nm["zt"])}</a>'),
    ]
    if nm.get('no'):
        facts.append(("Notes", esc(nm['no'])))
    open(f'public/named/{s}.html', 'w', encoding='utf-8', newline='\n').write(
        page("named", nm['n'], "Named mob", nm['a'], facts, extra, desc[:180], f"named/{s}"))
    n_named += 1

# ---- the two hub pages ------------------------------------------------------
# The Index builds its result rows in the browser from a JSON blob, so the HTML
# it serves contains no item links at all. A crawler that does not run the script
# sees an empty page, and the sitemap is then the only route to 655 addresses.
# These two are plain server-rendered A-Z lists: the honest hub, and the page a
# reader wants when they would rather browse than search.
HUB_CSS = '''<style>
.az{list-style:none;margin:0;padding:0;display:grid;
  grid-template-columns:repeat(auto-fill,minmax(215px,1fr));gap:5px 26px}
.az li{font-size:14.5px;line-height:1.45}
.az a{color:var(--dim);text-decoration:none;border-bottom:1px solid transparent}
.az a:hover{color:var(--ink);border-bottom-color:var(--line)}
.azh{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.16em;
  color:var(--faint);text-transform:uppercase;margin:26px 0 9px;
  border-top:1px solid var(--line);padding-top:9px}
.azh:first-of-type{margin-top:14px}
.azz{color:var(--faint)}
</style>'''


def hub(fname, title, desc, blurb, entries, folder):
    """entries: list of (name, slug, tail) already escaped."""
    body, letter = [], None
    for name, sl, tail in sorted(entries, key=lambda e: e[0].lower()):
        ch = name[0].upper()
        if not ch.isalpha():
            ch = '#'
        if ch != letter:
            if letter is not None:
                body.append('</ul>')
            letter = ch
            body.append(f'<h2 class="azh">{ch}</h2><ul class="az">')
        tag = f' <span class="azz">{tail}</span>' if tail else ''
        body.append(f'<li><a href="{sl}.html">{name}</a>{tag}</li>')
    body.append('</ul>')
    html = (head(title, desc, rel="../", extra=HUB_CSS, og="tools",
                 canon=f"{folder}/index") + bar("../") + f'''
<main>
<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp;
      <a href="../tools/index-search.html">The Index</a></p>
    <h1 class="display">{title}</h1>
    <p class="lede">{blurb} To filter by class, slot or zone, use
      <a href="../tools/index-search.html">The Index</a>.</p>
  </div>
</section>
<section class="band" style="border-top:0;padding-top:0">
  <div class="shell">{"".join(body)}</div>
</section>
</main>
''' + foot("../"))
    open(f'public/{folder}/index.html', 'w', encoding='utf-8',
         newline=chr(10)).write(html)


hub('index.html', 'Every item',
    f'An A to Z list of all {n_items} items recorded across the {len(Z)} surveyed '
    'EverQuest Legends dungeons, each linking to what drops it and where.',
    f'Every one of the {n_items} items the {len(Z)} dungeon surveys record, and the '
    f'zone each drops in &mdash; plus {n_groups} families the surveys name as a line '
    'rather than piece by piece.',
    [(esc(n), slug(n), esc(', '.join(sorted({r["zt"] for r in rows}))))
     for n, rows in by_item.items()], 'items')

hub('index.html', 'Every named mob',
    f'An A to Z list of all {n_named} named mobs recorded across the {len(Z)} '
    'surveyed EverQuest Legends dungeons, with level, position and drops.',
    f'Every one of the {n_named} named mobs the {len(Z)} dungeon surveys record, and '
    'the zone each spawns in.',
    [(esc(display(m['n'])), slug(m['n']), esc(m['zt'])) for m in IX['named']], 'named')

if (n_items, n_groups) != (n_items_declared, n_groups_declared):
    raise SystemExit(
        f"build17: wrote {n_items} item and {n_groups} family pages, but "
        f"extract.py counts {n_items_declared} and {n_groups_declared}. One of "
        f"them is wrong; do not publish a number until they agree.")
print(f"item and mob pages: {n_items} items + {n_groups} families, "
      f"{n_named} named ({n_items + n_groups + n_named + 2} new crawlable "
      f"addresses, hubs included)")
