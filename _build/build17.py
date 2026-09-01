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
from _partials import head, bar, foot, NAME_INDEX
from derived import clip as _clip
from withheld import WITHHELD, MARK

Z = {z['slug']: z for z in json.load(open('assets/zones-index.json', encoding='utf-8'))}
IX = json.load(open('assets/index-data.json', encoding='utf-8'))
# Measured drops, joined by _build/sightings.py. This is the only thing on these
# pages that is not a transcription of somebody else's wiki. It reaches the page
# as a mob name and a set of difficulty tiers; the session dates, the character
# and the tally stay in the dataset, where they belong.
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
.ent-top{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,246px);
  gap:var(--s-6);align-items:start}
@media(max-width:760px){.ent-top{grid-template-columns:1fr}}
.locator{margin:20px 0 0;display:flex;flex-direction:column;gap:8px}
.loc-plan{position:relative;display:block;border:1px solid var(--rule);
  border-radius:4px;background:var(--surface-1);padding:10px;overflow:hidden}
.loc-fit{position:relative;display:block;line-height:0}
.loc-plan img{width:100%;height:auto;display:block;opacity:.8}
/* The mark is the point of the whole thing: it is where the mob actually
   stands, from its recorded /loc. Drawn as a survey station rather than a pin —
   a ring with a centre dot, which is what a plotted position looks like on a
   real plan and what the site's own floor plans already use. */
.loc-mark{position:absolute;width:13px;height:13px;margin:-6.5px 0 0 -6.5px;
  border:1.5px solid var(--c);border-radius:50%;
  box-shadow:0 0 0 2px var(--surface-1)}
.loc-mark::after{content:"";position:absolute;inset:3.5px;border-radius:50%;
  background:var(--c)}
/* The needle sits in the plan's corner, over the plan's own padding rather
   than over the drawing, and it is the one mark on these pages that carries a
   fact. Kept small and low-contrast on purpose: the caption is what states the
   orientation, and this only has to make it visible at a glance. */
.loc-n{position:absolute;top:8px;right:8px;width:9px;height:16px;
  color:var(--mut);opacity:.75;pointer-events:none}
.locator figcaption{font-family:"IBM Plex Mono",monospace;font-size:10px;
  letter-spacing:.1em;text-transform:uppercase;color:var(--faint);line-height:1.6}
.locator figcaption b{color:color-mix(in srgb, var(--c) 58%, var(--bone));font-weight:500}
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
.drops.seen li{border-left-color:var(--ok-t)}
.drops.seen b{color:var(--ink)}
/* The badge carries the whole provenance claim for the block below it, so it
   sits in the heading rather than in a sentence. Raised off the middle: the
   heading is uppercase, and middle aligns to x-height, which reads low. */
.ent h2.sec .tier{margin-left:9px;vertical-align:.24em}
.src{margin:0;font-size:13px;color:var(--dim)}
.src a{color:var(--dim)}
</style>'''


# THE FIELDS THAT DECIDE ANYTHING.
#
# An item page used to print one word in its Slot row - "Primary" - because
# extract.py kept the first token of a cell reading "Primary · 1H Slash ·
# 15 / 46 · lore · no drop". So the surveys' 159 "no drop" markings reached none
# of the item pages, no weapon carried a damage or a delay, and two weapons could
# not be compared anywhere on the site. extract.py now parses the whole cell;
# these render it.
#
# THE RULE THAT MATTERS MOST IS THE NEGATIVE ONE. Tradeability is the fact that
# decides whether a guildmate can hand you the item, so its row is always
# present - but where the survey records no restriction the row says
# "not recorded" and the page says in words that silence is not permission.
# There is no code path anywhere below that prints "tradeable".

NOT_RECORDED = ('<em style="color:var(--faint)">not recorded &mdash; the survey '
                'names no restriction, which is not the same as recording that '
                'there is none</em>')
FROM_ROW = ('<em style="color:var(--faint)"> &mdash; from a row listing several '
            'items behind one cell, so this describes the row</em>')


def trade_row(a):
    """The tradeability dd. Never absent, never guessed."""
    if a.get('tf'):
        return ', '.join(esc(f) for f in a['tf']) + (FROM_ROW if a.get('rowdesc') else '')
    if a.get('tfs'):
        # One row writes its restriction into the stats cell, and writes it
        # alongside a note that another flag was removed. Parsing that into a
        # flag would assert the wrong one half the time, so the page points at
        # the survey's own words instead of paraphrasing them.
        return ('<em style="color:var(--faint)">recorded in the stats line below, '
                'not the slot column &mdash; read it there</em>')
    return NOT_RECORDED


def weapon_rows(a):
    """Damage, delay and the ratio derived from them. Nothing without both."""
    out = []
    if a.get('wt'):
        out.append(("Weapon type", esc(a['wt']) + (FROM_ROW if a.get('rowdesc') else '')))
    dmg, dly = a.get('dmg'), a.get('dly')
    if dmg is not None and dly is not None and dly:
        # Derived, and only where both inputs are present. Damage per unit of
        # delay is how two weapons are compared; it is arithmetic on the
        # survey's own two figures, not a figure from anywhere.
        out.append(("Damage / delay",
                    f'{dmg} / {dly} <span style="color:var(--faint)">'
                    f'&middot; ratio {dmg / dly:.2f}, derived</span>'))
    elif dmg is not None or dly is not None:
        out.append(("Damage / delay",
                    f'{dmg if dmg is not None else "not recorded"} / '
                    f'{dly if dly is not None else "not recorded"}'))
    if a.get('bs') is not None:
        out.append(("Backstab", str(a['bs'])))
    if a.get('rng') is not None:
        out.append(("Range", str(a['rng'])))
    if a.get('ch'):
        out.append(("Charges", esc(a['ch'])))
    return out


def seen_block(rows, label):
    """Measured drops: which mob, and the difficulty tiers it was recorded at.

    THE BADGE IS THE PROOF, SO THE SENTENCE IS NOT NEEDED. This block used to
    print a tally and up to three dated sessions per row - "seen 73x, 10 Aug
    2026 D1, 11 Aug 2026 D1, 11 Aug 2026 D2" - under a heading naming whose
    logs they were. All of that existed to establish that the measurement
    happened, which a tier M badge states in two characters. The finding is
    that this mob drops this item, and it survives whole.

    THE TIERS ARE A SET, NOT A DATED LIST. Seen four times at D1 and once at
    D3 reads "D1, D3": the difficulty is a fact about where the drop was
    recorded, the repetition is a fact about who played what. Absence from the
    set is not evidence a tier does not drop it, which is what the caveat says.

    A denominator was never in this data - nothing here counts kills - so no
    row above and no sentence below may be read as a rate.
    """
    if not rows:
        return ''
    li = []
    for r in rows:
        name = r['item'] if 'item' in r else r['mob']
        tiers = sorted({x['difficulty'] for x in r['sessions']
                        if x.get('difficulty') is not None})
        band = ', '.join(f'D{d}' for d in tiers)
        li.append(f'<li><b>{esc(name)}</b>'
                  + (f'<span>Recorded at {band}</span>' if band else '')
                  + '</li>')
    return (f'<h2 class="sec">{label} <span class="tier tM">TIER M</span></h2>'
            f'<ul class="drops seen">{"".join(li)}</ul>'
            f'<p class="src"><b>Observed, not a rate</b> &mdash; no kill count sits '
            f'behind this, and the tiers are those recorded rather than the only '
            f'ones that drop it. '
            f'<a href="../learn/reading-the-plans.html#measured">What a log can tell you</a>.</p>')



# THE LOCATOR. 674 of the site's pages had no graphic of any kind, and these are
# the pages a search engine lands a stranger on. Each now shows the zone it
# belongs to, drawn from the game's own mesh — and where we hold a named mob's
# /loc, a mark on that drawing showing where it actually stands.
#
# The plan is a shared file per zone (public/assets/plans/<slug>.svg), not
# inline SVG: a reader working through several items from one dungeon fetches
# it once. See _build/plans.py, which also writes the bounds this reads.
try:
    _PB = json.load(open('assets/zone-plan-bounds.json', encoding='utf-8'))['zones']
except (OSError, ValueError, KeyError):
    _PB = {}
sys.path.insert(0, os.path.join(ROOT, '_build'))
from plans import locate as _locate


def locator(zslug, ztitle, loc=None):
    """The zone plan, with a position mark where one can be placed honestly."""
    if not zslug or zslug not in _PB:
        return ''
    pos = _locate(_PB.get(zslug), loc) if loc else None
    mark = ''
    if pos:
        mark = (f'<span class="loc-mark" style="left:{pos[0]}%;top:{pos[1]}%"></span>')
    # A mob we hold no usable /loc for gets the plan and no mark, and the
    # caption says which — an unmarked plan is a gap stated, not a gap hidden.
    cap = (f'{esc(ztitle)} &middot; <b>/loc {esc(loc)}</b>' if pos
           else f'{esc(ztitle)} &middot; position not recorded' if loc is not None
           else esc(ztitle))
    # No loading="lazy": this sits at the top of the page and is the first
    # graphic a reader sees, so deferring it delays the largest paint for no
    # gain. width/height carry the plan's real aspect so the box is reserved
    # at its true shape and the page does not shift when it arrives.
    b = _PB[zslug]
    # ORIENTATION, STATED. 673 pages drew an oriented plan and 13 said which way
    # was up - the thirteen surveys. The convention is real and recorded in
    # _build/plans.py: +Y is north, +X is west, and both invert into page
    # coordinates. Its own comment warns that getting it wrong "looks plausible
    # enough to ship", which is exactly why a reader should not have to assume it.
    #
    # The needle is aria-hidden and the fact is in the caption as words, because
    # the image carries alt="" and the caption is what a screen reader gets. A
    # drawn arrow alone would assert the orientation to sighted readers only.
    needle = ('<svg class="loc-n" viewBox="0 0 14 24" fill="none" stroke="currentColor" '
              'stroke-width="1.3" stroke-linejoin="round" aria-hidden="true" '
              'focusable="false"><path d="M7 22V4"></path>'
              '<path d="M3 8 7 2l4 6z" fill="currentColor" stroke="none"></path></svg>')
    return (f'<figure class="locator">'
            f'<span class="loc-plan"><span class="loc-fit"><img src="../assets/plans/{zslug}.svg" alt="" '
            f'width="{b["w"]:.0f}" height="{b["h"]:.0f}" decoding="async">{mark}</span>{needle}</span>'
            f'<figcaption>{cap}<br>North is up &middot; floor from the game&rsquo;s own mesh</figcaption>'
            f'</figure>')

def page(kind, title, eyebrow, accent, facts, extra_html, desc, canon,
         locator_html=''):
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
      <a href="../tools/index-search.html">{NAME_INDEX}</a> &nbsp;/&nbsp; {eyebrow}</p>
    <h1 class="display">{esc(title)}</h1>
    <div class="ent-top">
      <dl class="facts">{rows}</dl>
      {locator_html}
    </div>
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
    seen = seen_block(SIGHT['by_item'].get(name, []), 'Dropped by')
    # The cell every field above was read out of, printed whole. A parser that
    # drops a fact looks exactly like a survey that never recorded it, and this
    # line is the only thing on the page that can tell the two apart.
    verbatim = (f'<p class="src" style="margin-top:18px"><b>As '
                f'{esc(rows[0]["zt"])} records it:</b> '
                f'&ldquo;{esc(a["sr"])}&rdquo;</p>') if a.get('sr') else ''
    caveat = ('' if a.get('tf') or a.get('tfs') else
              '<p class="src" style="margin-top:8px">The survey records no trade '
              'restriction for this item. <b>Read that as unrecorded, not as '
              'tradeable</b> &mdash; it may be No Drop and unnoted. One screenshot '
              'of the item description would settle it.</p>')
    extra = (f'<h2 class="sec">Where it drops</h2><ul class="srcs">{zones}</ul>{seen}{also_html}'
             f'{verbatim}{caveat}'
             f'<p class="src" style="margin-top:18px">Figures are the survey&rsquo;s own. '
             f'<a href="../sources.html">How we source</a>.</p>')
    desc = (f"{name} in EverQuest Legends: "
            + (f"{a['sr']}. " if a.get('sr') else "")
            # A META DESCRIPTION CANNOT CARRY A BADGE, SO IT MUST NOT CARRY THE
            # CLAIM. This is the text Google shows, and it was publishing
            # "Haste +10% T5" - a classic import, in a search snippet, with
            # nothing to mark it unverified and no tooltip to explain it. A
            # figure that needs a badge to be honest cannot appear where badges
            # do not exist, so a graded stats line is omitted here rather than
            # flattened into an assertion.
            + (f"{a['st'][:90]}. " if a.get('st') and not a.get('stt') else "")
            + f"Drops in {', '.join(sorted({r['zt'] for r in rows}))}.")
    facts = [
        ("Slot", esc(a['sl']) if a.get('sl') else None),
        *weapon_rows(a),
        # Always present, and "not recorded" where the survey is silent. This is
        # the row a reader came for: it decides whether the item can be handed
        # over, and it used to be missing from all 442 pages without a trace.
        ("Tradeability", trade_row(a)),
        ("Also flagged", ', '.join(esc(f) for f in a['hf']) if a.get('hf') else None),
        ("What it is for", esc(a['use']) if a.get('use') else None),
        # Where a loot row listed several items behind one stats cell, the stats
        # describe the row and not this item. Say which rather than assert them.
        # THE SURVEY'S GRADING TRAVELS WITH THE FIGURE.
        #
        # extract.py used to strip the badge's markup and leave its letters, so
        # this printed "Haste +10% T5" as plain prose - the grading reduced to
        # noise on the page and absent from the tooltip that explained it. It
        # carries `stt` now and the badge is rendered rather than spelled.
        #
        # CLAUDE.md: tiers 1 and 2 print plain; 3, 4 and 5 carry a visible badge
        # WHEREVER THE CLAIM APPEARS. A catalogue page is where the claim
        # appears.
        ("Stats" if not a.get('shared') else "Stats, from a shared row",
         (esc(a['st']) + (f' <span class="tier {a["stt"]}">{a["stt"][1:].upper()}</span>'
                          if a.get('stt') else '')
          + ('' if not a.get('shared') else
          ' <em style="color:var(--faint)">&mdash; this row lists several items '
          'behind one stats cell, so this line describes the row</em>'))
         if a.get('st') else None),
        ("Classes", esc(cls_txt) if cls_txt else None),
        ("Zones", esc(', '.join(sorted({r['zt'] for r in rows})))),
    ]
    # A row whose value is None prints "not recorded", which is right for Slot,
    # Stats and Classes and noise for a Range on a breastplate. Those rows are
    # built above only where the survey has something to put in them.
    facts = [(k, v) for k, v in facts
             if v is not None or k in ("Slot", "Stats", "Stats, from a shared row",
                                       "Classes")]
    if a.get('kind') == 'group':
        facts.insert(0, ("What this is",
                         "A family named by the survey row, not a single item"))
    s = slug(name)
    open(f'public/items/{s}.html', 'w', encoding='utf-8', newline='\n').write(
        page("item", name, "Item", a['a'], facts, extra, desc[:180], f"items/{s}",
             locator(a['z'], a['zt'])))
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
        f'<span>{esc(d["sr"] or d["s"])}{" &middot; " + esc(d["st"][:60]) if d.get("st") else ""}{f' <span class="tier {d["stt"]}">{d["stt"][1:].upper()}</span>' if d.get("stt") else ""}</span></li>'
        for d in drops)
    # THE LEDE IS GATED ON BOTH SOURCES, BECAUSE THERE ARE TWO.
    #
    # `drops` is the survey's loot table; `seen` is what we measured in play.
    # This tested only the first and then appended the second regardless, so a
    # mob with no survey entry and real measured drops printed "No drops
    # recorded - a gap, not an empty mob" DIRECTLY ABOVE a list of its recorded
    # drops. 30 named pages did exactly that.
    #
    # "A gap, not an empty mob" is a claim about our evidence, and it is false
    # when we hold evidence. It is only printed now when both sources are empty,
    # which is the state it was written to describe.
    seen = seen_block(SIGHT['by_named'].get(nm['n'], []), 'Observed drops')
    if drops:
        extra = f'<h2 class="sec">What it drops</h2><ul class="drops">{dl}</ul>'
    elif seen:
        extra = ''
    else:
        extra = '<p class="lede">No drops recorded &mdash; a gap, not an empty mob.</p>'
    extra += seen
    extra += (f'<p class="src" style="margin-top:18px">From the '
              f'<a href="../dungeons/{nm["z"]}.html">{esc(nm["zt"])} survey</a>.</p>')
    desc = (f"{nm['n']} in {nm['zt']}, EverQuest Legends"
            + (f", level {nm['lv']}" if nm.get('lv') else "")
            + (f". {_clip(nm['no'], 100)}" if nm.get('no') else "."))
    facts = [
        ("Level", esc(nm['lv']) if nm.get('lv') else None),
        ("Race and class", esc(nm['rc']) if nm.get('rc') else None),
        # WITHHOLDING APPLIES TO THE PAGE, NOT TO THE PLATE.
        #
        # These pages printed all six withheld Najena coordinates as bare
        # positions - "Position −670, −119" on rathyl.html - while the plate
        # three clicks away said "withheld". The coordinates were withheld
        # because they sit 57 to 513 units outside the zone's own drawn floor,
        # so publishing them here was publishing a position we had already
        # decided we do not trust.
        #
        # It survived because gate.py rule 4 hardcoded its scan to
        # public/dungeons/{slug}.html. The rule was right and its reach was one
        # directory wide; it now scans every page, which is what found this.
        ("Position", MARK if (nm.get('z'), nm.get('n')) in WITHHELD
         else (esc(nm['loc']) if nm.get('loc') else None)),
        ("Zone", f'<a href="../dungeons/{nm["z"]}.html">{esc(nm["zt"])}</a>'),
    ]
    if nm.get('no'):
        facts.append(("Notes", esc(nm['no'])))
    open(f'public/named/{s}.html', 'w', encoding='utf-8', newline='\n').write(
        page("named", nm['n'], "Named mob", nm['a'], facts, extra, desc[:180], f"named/{s}",
             locator(nm['z'], nm['zt'], nm.get('loc') or '')))
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
      <a href="../tools/index-search.html">{NAME_INDEX}</a></p>
    <h1 class="display">{title}</h1>
    <p class="lede">{blurb} To filter by class, slot or zone, use
      <a href="../tools/index-search.html">{NAME_INDEX}</a>.</p>
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
