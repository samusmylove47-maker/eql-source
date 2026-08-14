"""sets/index.html — all eighteen planar sets, as plain tables.

WHY THIS EXISTS
---------------
An outside audit made a point worth acting on: the site built 671 static pages
specifically so its data would be crawlable, and then shipped seven tools whose
data is invisible to the same crawlers. Everything in the planar gear tool
arrives as one JSON blob and is drawn by JavaScript, so the delivered HTML
contains a heading, five preset buttons, and nothing else.

This is not a "fallback" and is not hidden from anyone. It is the reference page
the tool was always implicitly promising - the whole of every set, in order, in
a table you can read, link to and search. The tool answers "what should I chase";
this answers "what is in the Shaman set". Both are worth having and only one of
them was built.

Every set gets an anchor, so a link can point at one.
"""
import os, re, sys, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

P = json.load(open('assets/planar.json', encoding='utf-8'))
ITEMS, SETCLASS = P['items'], P['setClass']

# WHERE EACH SET ACTUALLY DROPS.
# Every stat here is a classic-era item record read off a wiki page. Until 14
# August nothing on this site could say where a single one of these pieces
# comes from in Legends - the tool ranked 116 pieces and could not name one
# source. These are our own kills: a count of what we watched drop, and from
# what. A count, never a rate.
def _keyname(s):
    s = re.sub(r'\s*\+\d+\s*$', '', s or '')
    s = re.sub(r'^(a|an|the)\s+', '', s.strip(), flags=re.I)
    return re.sub(r'[^a-z0-9]+', '', s.lower())


SET_DROPS = collections.defaultdict(collections.Counter)   # set -> mob -> n
SET_ZONES = collections.defaultdict(collections.Counter)   # set -> zone -> n
try:
    _S = json.load(open('assets/sightings.json', encoding='utf-8'))
    _byname = {_keyname(i['n']): i['set'] for i in ITEMS}
    for _item, _rows in _S.get('by_item', {}).items():
        _set = _byname.get(_keyname(_item))
        if not _set:
            continue
        for _r in _rows:
            SET_DROPS[_set][_r['mob']] += _r['n']
            for _s in _r.get('sessions', []):
                if _s.get('zone'):
                    SET_ZONES[_set][_s['zone']] += 1
except (OSError, ValueError):
    pass
CLASS_NAME = P['classNames']
SLOTS = P['slots']

STAT = [("ac", "AC"), ("str", "STR"), ("sta", "STA"), ("agi", "AGI"), ("dex", "DEX"),
        ("wis", "WIS"), ("int", "INT"), ("cha", "CHA"), ("hp", "HP"), ("mana", "MANA"),
        ("svmagic", "MR"), ("svfire", "FR"), ("svcold", "CR"),
        ("svdisease", "DR"), ("svpoison", "PR")]

by_set = collections.OrderedDict()
for it in ITEMS:
    by_set.setdefault(it['set'], []).append(it)
# shared sets first, then class sets alphabetically by the class they serve
order = sorted(by_set, key=lambda s: (SETCLASS.get(s) is not None,
                                      CLASS_NAME.get(SETCLASS.get(s) or '', s)))


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def esc_mob(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


CSS = '''<style>
.ps{border-collapse:collapse;width:100%;font-size:13.5px;margin:var(--s-4) 0 0;min-width:640px}
.ps th{font-family:"IBM Plex Mono",monospace;font-size:9px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--faint);text-align:left;padding:9px 10px;
  border-bottom:1px solid var(--rule2);white-space:nowrap}
.ps td{padding:8px 10px;border-bottom:1px solid var(--rule);vertical-align:baseline}
.ps tr:last-child td{border-bottom:0}
.ps .nm{font-family:"Saira Condensed",sans-serif;font-size:15px;font-weight:600;color:var(--bone)}
.ps .sl{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.1em;color:var(--faint)}
.ps .st{font-family:"IBM Plex Mono",monospace;font-size:11.5px;color:var(--dim);line-height:1.5}
.ps .fx{color:var(--warn-t,#E0A56B)}
.setblk{border-top:1px solid var(--rule);padding-top:var(--s-6);margin-top:var(--s-6)}
.setblk h2{font-family:"Saira Condensed",sans-serif;font-size:26px;font-weight:700;
  text-transform:uppercase;letter-spacing:.02em;margin:0;color:var(--bone)}
.setblk .who{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.1em;
  color:var(--faint);margin:4px 0 0;text-transform:uppercase}
.setnav{display:flex;flex-wrap:wrap;gap:6px;margin:var(--s-5) 0 0}
.setnav a{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.08em;
  text-transform:uppercase;padding:6px 10px;border:1px solid var(--rule);color:var(--mut);
  text-decoration:none}
.setnav a:hover{border-color:var(--bone);color:var(--bone)}
.seen{font-size:13.5px;color:var(--dim);margin:6px 0 0;line-height:1.55;max-width:76ch}
.seen b{color:var(--bone)}
.seen.none{color:var(--faint);font-style:italic}
.tw{overflow-x:auto}
</style>'''


def stats_of(it):
    parts = [f'{lab} <b>{it[k]}</b>' for k, lab in STAT if it.get(k) is not None]
    return ' &middot; '.join(parts) or '&mdash;'


blocks = []
for s in order:
    rows = sorted(by_set[s], key=lambda i: SLOTS.index(i['s']) if i['s'] in SLOTS else 99)
    cls = SETCLASS.get(s)
    who = (f'{CLASS_NAME.get(cls, cls)} only' if cls else
           'Shared &mdash; ' + ', '.join(rows[0]['c']))
    body = "".join(
        f'<tr><td class="nm">{i["n"]}</td><td class="sl">{i["s"]}</td>'
        f'<td class="st">{stats_of(i)}'
        + (f'<br><span class="fx">Effect: {i["fx"]}</span>' if i.get('fx') else '')
        + '</td></tr>' for i in rows)
    short = len(rows) < 7
    note = ('' if not short else
            f'<p class="src">Only {len(rows)} of the seven slots are recorded. '
            f'{"Beastlord and Berserker did not exist in classic EverQuest, which is why their "
               "sets are the least documented." if cls in ("BST", "BER") else
               "The rest are not on the source."}</p>')
    drops = SET_DROPS.get(s)
    if drops:
        top = drops.most_common(6)
        zones = ', '.join(z for z, _ in SET_ZONES.get(s, collections.Counter()).most_common(2))
        seen = ('<p class="seen"><b>We have watched this drop</b> '
                + ', '.join(f'{esc_mob(m)} &times;{n}' for m, n in top)
                + (f' &mdash; {esc_mob(zones)}' if zones else '')
                + '. <span class="tier tM">TIER M</span> Counts from our own kills, '
                  'never a rate.</p>')
    else:
        seen = ('<p class="seen none">We have not watched any piece of this set drop. '
                'That is a gap in our logs, not evidence the set is hard to get.</p>')
    blocks.append(
        f'<section class="setblk" id="{slug(s)}">'
        f'<h2>{s}</h2><p class="who">{who} &middot; {len(rows)} recorded</p>{seen}'
        f'<div class="tw"><table class="ps">'
        f'<thead><tr><th>Piece</th><th>Slot</th><th>Stats</th></tr></thead>'
        f'<tbody>{body}</tbody></table></div>{note}</section>')

nav = "".join(f'<a href="#{slug(s)}">{s}</a>' for s in order)

page = (head("Every planar set",
             f"All {len(by_set)} planar armour sets in EverQuest Legends, piece by piece with "
             f"stats: the sixteen class sets plus Lustrous Russet and Midnight Clad.",
             rel="../", extra=CSS, og="tools", canon="sets/index")
        + bar("../") + f'''
<main>
<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp;
      <a href="../tools/planar-gear.html">Planar gear</a> &nbsp;/&nbsp; Every set</p>
    <h1 class="display">Every planar set,<br><em>piece by piece.</em></h1>
    <p class="hero-lede">All {len(by_set)} sets and {len(ITEMS)} pieces &mdash; the sixteen class
      sets plus the two shared ones. Want to know what to <em>chase</em> rather than what exists?
      <a href="../tools/planar-gear.html">The gear tool</a> ranks these against your trio.</p>
    <p class="hero-sig"><span>{len(by_set)} sets</span><span>{len(ITEMS)} pieces</span>
      <span><span class="tier t3">T3</span> classic-era records</span></p>
    <div class="setnav">{nav}</div>
  </div>
</section>

<section class="band" style="border-top:0;padding-top:0">
  <div class="shell">
    <div class="note"><strong>Every stat here is a classic-era item record</strong>
      <span class="tier t3">T3</span> &mdash; read from each item&rsquo;s own page and not
      confirmed against Legends piece by piece. A blank is a blank on the source, never a zero.</div>
    {"".join(blocks)}
  </div>
</section>
</main>
''' + foot("../"))

os.makedirs('public/sets', exist_ok=True)
open('public/sets/index.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"sets/index.html written: {len(by_set)} sets, {len(ITEMS)} pieces, crawlable")
