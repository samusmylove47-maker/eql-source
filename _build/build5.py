import os, sys, json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT); sys.path.insert(0, os.path.join(ROOT,'_build'))
from _partials import head, bar, foot

# One read, used for both the counts printed in the page and the data embedded
# in it, so the sentence and the tool can never disagree. They did: the page
# claimed 389 items while this very file shipped 452 to the counter beside it.
IX = json.load(open('assets/index-data.json', encoding='utf-8'))
# Fragments are not items and have no page, so they are not searchable things.
# They stay in index-data.json as a record of what the source row said, and are
# printed on their parent's page - see assets/catalogue-fixes.json.
IX['items'] = [i for i in IX['items'] if i.get('kind') != 'fragment']
# Counted once, in extract.py. Filtering fragments here and not groups was why
# this page printed 441 while the home page printed 451: two files, two
# definitions, neither of them reading the `kind` field that exists to settle it.
NITEMS = IX['counts']['item_rows']
NNAMED = IX['counts']['named_pages']
# Two counts, both true, and the site published them for a day without saying
# which was which: rows, because some items drop in two zones, against pages,
# because a page is per name.
NPAGES = IX['counts']['item_pages']
# The zone count is printed too. It was typed as "ten" in two sentences on
# this page and stayed at ten when the site reached thirteen.
NZONES = len(json.load(open('assets/zones-index.json', encoding='utf-8')))

CSS = '''<style>
.ix-controls{position:sticky;top:58px;z-index:30;background:rgba(14,19,21,.96);
  backdrop-filter:blur(10px);border-bottom:1px solid var(--rule);padding:14px 0 12px;margin-bottom:0}
.ix-search{width:100%;font-family:"IBM Plex Mono",monospace;font-size:15px;padding:13px 15px;
  background:var(--panel2);border:1px solid var(--rule2);color:var(--bone)}
.ix-search:focus{outline:2px solid var(--bone);outline-offset:-1px}
/* Pinned rather than left to the browser default, which varies by engine and
   in one common case lands at 4.69:1 — passing by 0.19 and only by accident. */
.ix-search::placeholder{color:var(--dim);opacity:1}
.ix-row{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:11px}
.ix-row .lab{font-family:"IBM Plex Mono",monospace;font-size:9px;letter-spacing:.2em;
  text-transform:uppercase;color:var(--faint);margin-right:2px}
.fchip{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.1em;text-transform:uppercase;
  padding:5px 9px;border:1px solid var(--rule);color:var(--mut);transition:all .12s}
.fchip:hover{color:var(--bone);border-color:var(--rule2)}
.fchip[aria-pressed="true"]{border-color:var(--bone);color:var(--bone);background:rgba(230,233,228,.07)}
.fchip.z[aria-pressed="true"]{border-color:var(--zc);background:transparent;
  color:var(--zc);color:color-mix(in srgb, var(--zc) 68%, var(--bone))}
.ix-mode{display:flex;gap:0;border:1px solid var(--rule)}
.ix-mode button{font-family:"Saira Condensed",sans-serif;font-size:15px;font-weight:600;
  text-transform:uppercase;letter-spacing:.05em;padding:7px 16px;color:var(--mut)}
.ix-mode button[aria-pressed="true"]{background:var(--bone);color:var(--ground)}
.ix-count{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.12em;
  text-transform:uppercase;color:var(--faint);margin-left:auto}
.ix-results{margin-top:2px}
.res{display:grid;grid-template-columns:4px minmax(0,2.1fr) 96px minmax(0,2fr) minmax(0,1.5fr) 120px;
  gap:14px;align-items:start;padding:13px 0 13px 14px;border-bottom:1px solid var(--rule);
  background:linear-gradient(90deg,var(--zc) 0 3px,transparent 3px)}
.res:hover{background:linear-gradient(90deg,var(--zc) 0 3px,var(--panel) 3px)}
.res .nm{font-family:"Saira Condensed",sans-serif;font-size:19px;font-weight:600;
  letter-spacing:.015em;color:var(--bone);line-height:1.15}
/* The name is the way in to the item's own page. Underlined always, so it reads
   as a link without hovering; the accent appears on hover and focus. */
a.nm{text-decoration:none;border-bottom:1px solid var(--line);transition:border-color .12s}
a.nm:hover{border-bottom-color:var(--zc)}
a.nm:focus-visible{outline:2px solid var(--zc);outline-offset:3px;border-radius:2px}
.res .sub{font-family:"IBM Plex Mono",monospace;font-size:10px;color:var(--faint);
  letter-spacing:.05em;display:block;margin-top:3px}
.res .cell{font-family:"IBM Plex Mono",monospace;font-size:11.5px;color:var(--mut);line-height:1.5}
.res .cell em{font-style:normal;display:block;font-size:8.5px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--faint);margin-bottom:3px}
.res .zone{text-align:right}
.res .zone a{font-family:"Saira Condensed",sans-serif;font-size:16px;font-weight:600;
  text-transform:uppercase;letter-spacing:.03em;text-decoration:none;
  /* Raw zone accents run 2.87:1 (Mistmoore) and 3.90:1 (Crushbone) here. 68%
     is the blanket blend that clears 4.5:1 for all ten, hovered row included. */
  color:var(--zc);
  color:color-mix(in srgb, var(--zc) 68%, var(--bone))}
.res .zone a:hover{text-decoration:underline}
.res .cls{display:flex;gap:3px;flex-wrap:wrap;margin-top:4px}
.res .cls span{font-family:"IBM Plex Mono",monospace;font-size:8.5px;letter-spacing:.08em;
  padding:1px 4px;border:1px solid var(--rule2);color:var(--dim)}
.res .cls span.hit{border-color:var(--bone);color:var(--bone)}
@media(max-width:940px){
  .res{grid-template-columns:minmax(0,1fr) auto;gap:6px 12px}
  .res .cell:nth-of-type(2){display:none}
  .res .zone{grid-column:2;grid-row:1}
}
.ix-empty{border:1px dashed var(--rule);padding:36px;text-align:center;color:var(--mut);margin-top:24px}
mark{background:rgba(230,233,228,.22);color:var(--bone);padding:0 1px}
</style>'''

BODY = f'''
<main>
<div class="shell">
  <div class="page-head">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp; <a href="index.html">Tools</a> &nbsp;/&nbsp; The Index</p>
    <h1>The Index</h1>
    <p class="lede">Every item and every named mob recorded across the {NZONES} surveyed dungeons, in one searchable
      place. Ask it where something drops, what a zone holds for your classes, or which named you still have not
      met. <strong>{NPAGES} items and {NNAMED} named</strong>, each tied back to the survey it came from.</p>
    <p class="lede">Every name here opens its own page. You can also browse the full
      <a href="../items/index.html">A to Z of items</a> or the
      <a href="../named/index.html">A to Z of named mobs</a>.</p>
  </div>
</div>

<div class="ix-controls">
  <div class="shell">
    <input class="ix-search" id="q" type="search" autocomplete="off" spellcheck="false"
      placeholder="Search an item, a mob, a stat, a drop source&hellip;">
    <div class="ix-row">
      <div class="ix-mode">
        <button data-mode="items" aria-pressed="true">Loot</button>
        <button data-mode="named" aria-pressed="false">Named</button>
      </div>
      <span class="ix-count" id="count"></span>
    </div>
    <div class="ix-row" id="rowClass"><span class="lab">Class</span></div>
    <div class="ix-row" id="rowSlot"><span class="lab">Slot</span></div>
    <div class="ix-row" id="rowZone"><span class="lab">Zone</span></div>
  </div>
</div>

<div class="shell">
  <div class="ix-results" id="results"></div>
  <div class="note" style="margin-top:34px"><strong>What this is and is not.</strong> It indexes the loot and named
    tables from our own surveys &mdash; so its coverage is exactly the {NZONES} zones we have surveyed, not the whole
    game. {NPAGES} items, {NITEMS} rows: six drop in two zones. Stats are quoted as the survey records them, which means anything the survey flagged as uncertain is uncertain
    here too. Follow the zone link to read the surrounding context before you plan a night around a drop.</div>
  <div class="note sig"><strong>Looking for a gear upgrade check against your own inventory?</strong>
    <a href="https://eqltools.com/gear" style="color:var(--bone)">EQL Tools has one</a> that reads your inventory file
    and finds items that beat what you are wearing. That is a different job from this, done well, and there is no sense
    in us building a worse copy.</div>
</div>
</main>
'''

SCRIPT = '<script>window.__IX__=' + json.dumps(IX, separators=(",",":")) + ';</script>' + '''<script>
(async function(){
  var D=null, mode="items", q="", fC=new Set(), fS=new Set(), fZ=new Set();
  var $=function(s){return document.querySelector(s)};
  var esc=function(s){return String(s==null?"":s).replace(/[&<>"]/g,function(m){
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[m]})};
  D=window.__IX__;
  if(!D){ $("#results").innerHTML='<div class="ix-empty">Index data did not load.</div>'; return; }

  var zones={};
  D.items.concat(D.named).forEach(function(r){ zones[r.z]={t:r.zt,a:r.a,p:r.p}; });
  function chips(el,list,set,cls){
    var host=$(el);
    list.forEach(function(v){
      var b=document.createElement("button");
      b.className="fchip"+(cls||""); b.textContent=(cls===" z"?zones[v].t:v);
      b.setAttribute("aria-pressed","false");
      if(cls===" z") b.style.setProperty("--zc",zones[v].a);
      b.onclick=function(){
        if(set.has(v)){set.delete(v);b.setAttribute("aria-pressed","false");}
        else{set.add(v);b.setAttribute("aria-pressed","true");}
        render();
      };
      host.appendChild(b);
    });
  }
  chips("#rowClass",D.classes,fC);
  chips("#rowSlot",D.slots,fS);
  chips("#rowZone",Object.keys(zones).sort(function(a,b){return zones[a].p-zones[b].p}),fZ," z");

  function hl(s){
    if(!q) return esc(s);
    var t=esc(s), needle=esc(q);
    try{ return t.replace(new RegExp("("+needle.replace(/[.*+?^${}()|[\\]\\\\]/g,"\\\\$&")+")","ig"),"<mark>$1</mark>"); }
    catch(e){ return t; }
  }
  function matchItem(i){
    if(fZ.size&&!fZ.has(i.z)) return false;
    if(fS.size&&!fS.has(i.s)) return false;
    if(fC.size&&!i.c.some(function(c){return fC.has(c)||c==="ALL"})) return false;
    if(!q) return true;
    var s=(i.n+" "+i.sr+" "+i.st+" "+i.d+" "+i.zt).toLowerCase();
    return s.indexOf(q.toLowerCase())>-1;
  }
  function matchNamed(n){
    if(fZ.size&&!fZ.has(n.z)) return false;
    if(!q) return true;
    return (n.n+" "+n.rc+" "+n.no+" "+n.zt+" "+n.lv).toLowerCase().indexOf(q.toLowerCase())>-1;
  }
  function rowItem(i){
    return '<div class="res" style="--zc:'+i.a+'">'
      +'<span></span>'
      +'<span><a class="nm" href="../items/'+i.u+'.html">'+hl(i.n)+'</a>'
        +'<span class="cls">'+i.c.map(function(c){
            return '<span class="'+(fC.has(c)?"hit":"")+'">'+esc(c)+'</span>'}).join("")+'</span></span>'
      +'<span class="cell"><em>Slot</em>'+esc(i.s)+'</span>'
      +'<span class="cell"><em>Stats</em>'+(i.st?hl(i.st):"&mdash;")+'</span>'
      +'<span class="cell"><em>Dropped by</em>'+(i.d?hl(i.d):"&mdash;")+'</span>'
      +'<span class="cell zone"><em>Survey '+String(i.p).padStart(2,"0")+'</em>'
        +'<a href="../dungeons/'+i.z+'.html">'+esc(i.zt)+'</a></span></div>';
  }
  function rowNamed(n){
    return '<div class="res" style="--zc:'+n.a+'">'
      +'<span></span>'
      +'<span><a class="nm" href="../named/'+n.u+'.html">'+hl(n.n)+'</a>'
        +'<span class="sub">'+(n.rc?esc(n.rc)+" &middot; ":"")+(n.fl?"floor "+esc(n.fl)+" &middot; ":"")
        +(n.loc?"loc "+esc(n.loc):"")+'</span></span>'
      +'<span class="cell"><em>Level</em>'+(n.lv?esc(n.lv):"&mdash;")+'</span>'
      +'<span class="cell" style="grid-column:span 2"><em>Notes</em>'+(n.no?hl(n.no):"&mdash;")+'</span>'
      +'<span class="cell zone"><em>Survey '+String(n.p).padStart(2,"0")+'</em>'
        +'<a href="../dungeons/'+n.z+'.html">'+esc(n.zt)+'</a></span></div>';
  }
  function render(){
    var rows, html;
    if(mode==="items"){ rows=D.items.filter(matchItem); html=rows.map(rowItem).join(""); }
    else { rows=D.named.filter(matchNamed); html=rows.map(rowNamed).join(""); }
    $("#count").textContent=rows.length+" of "+(mode==="items"?D.items.length:D.named.length)
      +(mode==="items"?" items":" named");
    $("#results").innerHTML = html || '<div class="ix-empty">Nothing matches. Try fewer filters, '
      +'or search the drop source instead of the item.</div>';
    $("#rowSlot").style.display = mode==="items" ? "" : "none";
    $("#rowClass").style.display = mode==="items" ? "" : "none";
  }
  var t;
  $("#q").addEventListener("input",function(e){
    clearTimeout(t); t=setTimeout(function(){ q=e.target.value.trim(); render(); },110);
  });
  document.querySelectorAll("[data-mode]").forEach(function(b){
    b.onclick=function(){
      mode=b.dataset.mode;
      document.querySelectorAll("[data-mode]").forEach(function(x){
        x.setAttribute("aria-pressed",String(x.dataset.mode===mode))});
      render();
    };
  });
  render();
})();
</script>'''

page = head("The Index",
  f"Search every item and named mob across the {NZONES} surveyed EverQuest Legends dungeons. Filter by class, slot and zone, and see exactly which mob drops what.",
  rel="../", extra=CSS, og="tools", canon="tools/index-search") + bar("../") + BODY + foot("../").replace('</body>', SCRIPT + '\n</body>')
open('public/tools/index-search.html','w',encoding='utf-8',newline='\n').write(page)
print("The Index built:", len(page), "bytes")
