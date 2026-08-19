"""tools/inventory.html — paste your inventory, see what this site knows about it.

WHY
---
`/outputfile inventory` writes a tab-separated dump of everything a character
carries. It is a wall of text: 533 rows across the two dumps we have seen, more
than half of them empty sockets. Nobody reads it.

Every item in it that we know anything about already has a page here, and 153
of them have measured drop sightings nobody else has. The dump and the site
have never been introduced. This introduces them.

WHAT IT ANSWERS
---------------
"Where do I get another one of these" - our named-mob pages, and where a drop
has been measured in play, the mob. NOT how many times it was watched dropping:
which mob drops what is a fact about the game, and a sighting tally is a record
of one player's evening. The tier M badge already says it was measured.

"How much of the planar sets am I actually carrying" - matched against the same
116 pieces the gear tool ranks, so the two agree by construction.

"How much upgrade headroom is left" - you hold a +N; drops floor at the zone
difficulty and cap at +4, and everything above that is made rather than found.

WHAT IT REFUSES TO DO
---------------------
No stats, no scoring, no "your gear rates 7/10". The dump carries no stats at
all - only names, IDs and counts - so any number of that kind would be invented.
Where we know nothing about an item, the tool says so rather than padding.

An unrecognised item is a gap in THIS catalogue, and it says so. Getting that
the wrong way round would read as though the reader had done something wrong.

NOTHING LEAVES THE BROWSER
--------------------------
The parse happens in the page. There is no upload, no request, no storage. An
inventory names a character and lists what they own, and that is the reader's
to keep. The page says so where the box is, not in a footnote.
"""
import os, re, sys, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

CAT = json.load(open('assets/index-data.json', encoding='utf-8'))
SIGHT = json.load(open('assets/sightings.json', encoding='utf-8'))
PLANAR = json.load(open('assets/planar.json', encoding='utf-8'))
try:
    IDS = json.load(open('assets/item-ids.json', encoding='utf-8'))['items']
except (OSError, ValueError, KeyError):
    IDS = {}


def norm(s):
    """The catalogue's join key. Same one extract.py and sightings.py use, so a
    match here means the same thing it means everywhere else."""
    s = re.sub(r'^(a|an|the)\s+', '', (s or '').strip(), flags=re.I)
    return re.sub(r'[^a-z0-9]+', '', s.lower())


# ---- the lookup the page ships with -----------------------------------------
# Keyed on the normalised name so the browser does not have to reimplement our
# matching rules, and so an apostrophe or a leading article cannot cause a miss.
know = {}
for it in CAT['items']:
    if it.get('kind') != 'item':
        continue
    k = norm(it['n'])
    e = know.setdefault(k, dict(n=it['n'], u=it.get('u'), z=[], d=''))
    if it.get('zt') and it['zt'] not in e['z']:
        e['z'].append(it['zt'])
    if it.get('d') and not e['d']:
        e['d'] = it['d']

for item, rows in SIGHT.get('by_item', {}).items():
    k = norm(item)
    e = know.setdefault(k, dict(n=item, u=None, z=[], d=''))
    # WHICH mob drops it, never how many times it was watched doing so. The
    # sighting count ranks the candidates here and then stays behind: a tally of
    # what one player saw on one evening is a record of that evening, and the
    # fact a reader needs is the mob. How many OTHER mobs drop it is a fact about
    # the item, so that number stays and they are counted rather than named,
    # which keeps the sentence to one line.
    top = max(rows, key=lambda r: r.get('n', 0))
    e['seen'] = dict(mob=top['mob'], others=len(rows) - 1)

PSET = {}
for it in PLANAR['items']:
    PSET[norm(it['n'])] = it['set']
    e = know.setdefault(norm(it['n']), dict(n=it['n'], u=None, z=[], d=''))
    e['set'] = it['set']

for name, iid in IDS.items():
    k = norm(name)
    if k in know:
        know[k]['id'] = iid

DATA = dict(know=know, sets=sorted({v['set'] for v in know.values() if v.get('set')}))

CSS = '''<style>
.iv-drop{border:1px dashed var(--rule2);border-radius:var(--r);padding:var(--s-6);
  background:var(--panel);margin:var(--s-5) 0 0}
.iv-drop textarea{width:100%;min-height:150px;background:#10151A;color:var(--dim);
  border:1px solid var(--rule);border-radius:4px;padding:12px 14px;
  font-family:"IBM Plex Mono",monospace;font-size:12px;line-height:1.6;resize:vertical}
.iv-drop textarea:focus{outline:2px solid var(--instr);outline-offset:1px}
.iv-priv{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--instr);margin:0 0 10px}
.iv-how{color:var(--faint);font-size:13px;margin:10px 0 0}
.iv-how code{color:var(--dim)}
.iv-btn{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.12em;
  text-transform:uppercase;padding:10px 18px;border:1px solid var(--instr);
  background:transparent;color:var(--instr);cursor:pointer;border-radius:3px;margin:12px 8px 0 0}
.iv-btn:hover{background:var(--instr);color:#0B0F12}
.iv-btn.sec{border-color:var(--rule2);color:var(--mut)}
.iv-btn.sec:hover{background:var(--rule);color:var(--bone)}
.iv-sum{display:flex;flex-wrap:wrap;gap:1px;background:var(--rule);border:1px solid var(--rule);
  border-radius:var(--r);overflow:hidden;margin:var(--s-6) 0 0}
.iv-sum div{background:var(--panel);padding:14px 20px;flex:1 1 130px}
.iv-sum b{display:block;font-family:"Saira Condensed",sans-serif;font-size:28px;
  font-weight:700;color:var(--bone);line-height:1}
.iv-sum span{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--faint);display:block;margin-top:5px}
.iv-tw{overflow-x:auto;margin:var(--s-6) 0 0}
.iv-t{border-collapse:collapse;width:100%;min-width:660px;font-size:13.5px}
.iv-t th{font-family:"IBM Plex Mono",monospace;font-size:9px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--faint);text-align:left;padding:9px 10px;
  border-bottom:1px solid var(--rule2);white-space:nowrap}
.iv-t td{padding:9px 10px;border-bottom:1px solid var(--rule);vertical-align:top}
.iv-t tr:last-child td{border-bottom:0}
.iv-t .nm{font-family:"Saira Condensed",sans-serif;font-size:15.5px;font-weight:600;color:var(--bone)}
.iv-t .nm a{color:var(--bone);text-decoration:none;border-bottom:1px solid var(--rule2)}
.iv-t .nm a:hover{border-color:var(--instr);color:var(--instr)}
.iv-t .tier{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--instr)}
.iv-t .where{color:var(--dim);font-size:13px;line-height:1.5}
.iv-t .none{color:var(--faint);font-style:italic}
.iv-aug{color:var(--faint);font-size:10px;letter-spacing:.08em;text-transform:uppercase}
.iv-seen{color:var(--warn-t,#E0A56B);font-family:"IBM Plex Mono",monospace;font-size:11.5px}
.iv-setb{display:inline-block;font-family:"IBM Plex Mono",monospace;font-size:9.5px;
  letter-spacing:.1em;text-transform:uppercase;color:var(--instr);
  border:1px solid var(--instr);border-radius:2px;padding:1px 6px;margin-left:7px}
.iv-filt{display:flex;flex-wrap:wrap;gap:6px;margin:var(--s-5) 0 0}
.iv-filt button{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.08em;
  text-transform:uppercase;padding:6px 12px;border:1px solid var(--rule);background:transparent;
  color:var(--mut);cursor:pointer;border-radius:3px}
.iv-filt button[aria-pressed="true"]{border-color:var(--instr);color:var(--instr)}
.iv-err{color:var(--warn-t,#E0A56B);font-size:13.5px;margin:var(--s-5) 0 0}
@media(max-width:640px){.iv-sum div{flex:1 1 100%}}
</style>'''

PAGE_JS = r'''<script>
(function(){
  var D = window.__IV__, K = D.know;
  function norm(s){
    s = (s||'').trim().replace(/^(a|an|the)\s+/i,'');
    return s.toLowerCase().replace(/[^a-z0-9]+/g,'');
  }
  // The dump writes the upgrade tier as a suffix and the augment form in
  // brackets. Both belong to the same underlying item, so both come off before
  // we look anything up.
  function strip(n){
    var t = null, m = n.match(/\s*\+(\d+)\s*$/);
    if(m){ t = +m[1]; n = n.slice(0, m.index); }
    var ex = /\s*\(Exaltation\)\s*$/.test(n);
    if(ex) n = n.replace(/\s*\(Exaltation\)\s*$/,'');
    return {base: n.trim(), tier: t, exalt: ex};
  }
  function parse(text){
    var rows = [], section = 'inv';
    text.split(/\r?\n/).forEach(function(line){
      if(!line.trim()) return;
      var f = line.split('\t');
      if(f[0] === 'Location') return;
      if(f[0] === 'KeyRing'){ section = 'key'; return; }
      var name, id, count;
      if(section === 'inv'){ if(f.length < 5) return; name=f[1]; id=+f[2]; count=+f[3]||1; }
      else { if(f.length < 3) return; name=f[1]; id=+f[2]; count=1; }
      if(!name || name === 'Empty' || !id) return;
      var s = strip(name);
      rows.push({base:s.base, tier:s.tier, exalt:s.exalt, id:id, count:count});
    });
    return rows;
  }
  // One line per distinct item. The dump lists a stack of 390 Bone Chips and
  // eleven separate Refugee Shrouds; both are one row here, with the best tier
  // held and how many were found.
  function fold(rows){
    var by = {};
    rows.forEach(function(r){
      var k = norm(r.base);
      var e = by[k] || (by[k] = {base:r.base, key:k, id:r.id, n:0, best:null, exalt:0});
      // An Exaltation is an augment, not another copy of the wearable item.
      // Counting the two together read as "2 pairs of Golden Efreeti Boots"
      // when it was one pair and one augment socketed elsewhere.
      if(r.exalt) e.exalt += r.count; else e.n += r.count;
      if(r.tier !== null && (e.best === null || r.tier > e.best)) e.best = r.tier;
    });
    return Object.keys(by).map(function(k){ return by[k]; });
  }
  var state = {rows: [], filter: 'all'};
  function render(){
    var out = document.getElementById('iv-out');
    if(!state.rows.length){ out.innerHTML=''; return; }
    var rows = state.rows.slice();
    if(state.filter === 'known')  rows = rows.filter(function(r){ return K[r.key]; });
    if(state.filter === 'seen')   rows = rows.filter(function(r){ return K[r.key] && K[r.key].seen; });
    if(state.filter === 'planar') rows = rows.filter(function(r){ return K[r.key] && K[r.key].set; });
    if(state.filter === 'unknown')rows = rows.filter(function(r){ return !K[r.key]; });
    rows.sort(function(a,b){
      var ka = K[a.key], kb = K[b.key];
      var sa = (ka&&ka.seen?2:0) + (ka?1:0), sb = (kb&&kb.seen?2:0) + (kb?1:0);
      if(sa !== sb) return sb - sa;
      return a.base.localeCompare(b.base);
    });
    var known = state.rows.filter(function(r){ return K[r.key]; }).length;
    var seen  = state.rows.filter(function(r){ return K[r.key] && K[r.key].seen; }).length;
    var plan  = state.rows.filter(function(r){ return K[r.key] && K[r.key].set; }).length;
    var body = rows.map(function(r){
      var k = K[r.key];
      var nm = k && k.u ? '<a href="../items/'+k.u+'.html">'+esc(k.n)+'</a>' : esc(r.base);
      var setb = k && k.set ? '<span class="iv-setb">'+esc(k.set)+'</span>' : '';
      var tier = r.best === null ? '&mdash;' : '+'+r.best;
      var where;
      if(!k){
        where = '<span class="none">not catalogued here</span>';
      } else {
        var bits = [];
        if(k.seen) bits.push('<span class="iv-seen">drops from '+esc(k.seen.mob)+
                             (k.seen.others ? ', and '+k.seen.others+' other mob'+
                              (k.seen.others>1?'s':'') : '')+
                             ' <span class="tier tM">M</span></span>');
        if(k.d) bits.push(esc(k.d));
        if(k.z && k.z.length) bits.push('<span class="none">'+esc(k.z.join(', '))+'</span>');
        // A planar piece with no survey row is not an unrecorded drop - we
        // simply catalogue the planes by set rather than by mob. Saying "no
        // drop source recorded" there reads as a gap that is not one.
        if(!bits.length && k.set)
          bits.push('<a href="../sets/index.html">'+esc(k.set)+' set</a> &mdash; ' +
                    'catalogued by set rather than by mob');
        where = bits.length ? bits.join('<br>') : '<span class="none">no drop source recorded</span>';
      }
      var qty = (r.n>1?r.n:'') +
        (r.exalt ? '<span class="iv-aug" title="Exaltation - an augment form of this item">'+
                   (r.n?' ':'')+r.exalt+'&times; aug</span>' : '');
      return '<tr><td class="nm">'+nm+setb+'</td><td class="tier">'+tier+'</td>'+
             '<td class="tier">'+(qty||'&mdash;')+'</td><td class="where">'+where+'</td></tr>';
    }).join('');
    out.innerHTML =
      '<div class="iv-sum">'+
        '<div><b>'+state.rows.length+'</b><span>distinct items</span></div>'+
        '<div><b>'+known+'</b><span>we have a page for</span></div>'+
        '<div><b>'+seen+'</b><span>with a measured drop source</span></div>'+
        '<div><b>'+plan+'</b><span>planar set piece'+(plan===1?'':'s')+'</span></div>'+
      '</div>'+
      '<div class="iv-filt">'+
        btn('all','Everything')+btn('seen','Measured drop')+btn('planar','Planar')+
        btn('known','In our catalogue')+btn('unknown','Not in it')+
      '</div>'+
      '<div class="iv-tw"><table class="iv-t"><thead><tr>'+
      '<th>Item</th><th>Best held</th><th>Count</th><th>What we know about it</th>'+
      '</tr></thead><tbody>'+body+'</tbody></table></div>';
    Array.prototype.forEach.call(out.querySelectorAll('.iv-filt button'), function(b){
      b.onclick = function(){ state.filter = b.getAttribute('data-f'); render(); };
    });
  }
  function btn(f,label){
    return '<button data-f="'+f+'" aria-pressed="'+(state.filter===f)+'">'+label+'</button>';
  }
  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }

  document.getElementById('iv-go').onclick = function(){
    var t = document.getElementById('iv-in').value;
    var err = document.getElementById('iv-err');
    var rows = parse(t);
    if(!rows.length){
      err.textContent = t.trim()
        ? 'No item rows found. This wants the whole file that /outputfile inventory writes, tabs and all - pasting from a spreadsheet drops the tabs.'
        : 'Paste the contents of the inventory file first.';
      state.rows = []; render(); return;
    }
    err.textContent = '';
    state.rows = fold(rows);
    render();
  };
  document.getElementById('iv-clear').onclick = function(){
    document.getElementById('iv-in').value = '';
    document.getElementById('iv-err').textContent = '';
    state.rows = []; render();
  };
})();
</script>'''


def page():
    n_seen = len(SIGHT.get('by_item', {}))
    n_cat = len({norm(i['n']) for i in CAT['items'] if i.get('kind') == 'item'})
    return (head("What have I got?",
                 f"Paste an EverQuest Legends inventory file and see what this site knows about "
                 f"every item in it: where it drops, which mobs are measured dropping it, and "
                 f"which planar set it belongs to. Nothing is uploaded.",
                 rel="../", extra=CSS, og="tools", canon="tools/inventory")
            + bar("../") + f'''
<main id="main">
<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp;
      <a href="index.html">Tools</a> &nbsp;/&nbsp; What have I got?</p>
    <h1 class="display">What have<br><em>I got?</em></h1>
    <p class="hero-lede">Your inventory file is a wall of tab-separated text and nobody reads it.
      Paste it here and it becomes a list of what you are carrying, with everything this site
      knows about each piece attached &mdash; including {n_seen} items whose drop source was
      measured in play rather than transcribed.</p>
    <p class="hero-sig"><span>{n_cat} items catalogued</span>
      <span>{n_seen} with a measured drop source</span><span>nothing uploaded</span></p>
  </div>
</section>

<section class="band" style="border-top:0;padding-top:0">
  <div class="shell">
    <div class="iv-drop">
      <p class="iv-priv">Nothing leaves this page</p>
      <p style="margin:0 0 12px;color:var(--dim);font-size:14px">The parsing happens in your
        browser. There is no upload and nothing is stored &mdash; an inventory names your
        character and lists what you own, and that stays yours. Close the tab and it is gone.</p>
      <textarea id="iv-in" spellcheck="false"
        placeholder="Paste the whole inventory file here, tabs and all."
        aria-label="Your inventory file"></textarea>
      <button class="iv-btn" id="iv-go">Read it</button>
      <button class="iv-btn sec" id="iv-clear">Clear</button>
      <p class="iv-err" id="iv-err" role="status"></p>
      <p class="iv-how">Type <code>/outputfile inventory</code> in game. It writes
        <code>&lt;Character&gt;_&lt;server&gt;-Inventory.txt</code> into your EverQuest Legends
        folder. Open it, select all, paste.</p>
    </div>

    <div id="iv-out"></div>

    <div class="note" style="margin-top:var(--s-7)">
      <strong>What this cannot tell you.</strong> The file carries names, IDs and counts &mdash;
      <strong>no stats at all</strong>. So there is no score here and no ranking of your gear:
      any such number would be invented rather than read. For what to chase next, the
      <a href="planar-gear.html">planar gear tool</a> ranks the sets against your trio, and
      <a href="../sets/index.html">every set</a> lists the pieces.
    </div>
    <div class="note">
      <strong>An unrecognised item marks a gap in this catalogue.</strong> It is mined from the
      dungeon surveys, so it covers the surveyed zones and nothing else. A row saying
      <em>not catalogued here</em> means that zone has not been written up yet.
    </div>
    <div class="note">
      <strong>On the number after the name.</strong> A drop arrives at the difficulty tier of the
      zone at minimum and occasionally one above, capping at +4 at Refined. Anything higher than
      +4 was made, not found. <a href="../learn/difficulty.html">How difficulty decides that
      &rarr;</a>
    </div>
  </div>
</section>
</main>
''' + '<script>window.__IV__=' + json.dumps(DATA, separators=(",", ":")) + ';</script>'
        + PAGE_JS + foot("../"))


os.makedirs('public/tools', exist_ok=True)
out = page()
open('public/tools/inventory.html', 'w', encoding='utf-8', newline='\n').write(out)
print(f"tools/inventory.html written: {len(DATA['know'])} items known, "
      f"{sum(1 for v in DATA['know'].values() if v.get('seen'))} with measured sightings, "
      f"{len(out)//1024} KB")
