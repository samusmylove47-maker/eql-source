"""tools/planar-gear.html — pick a trio, target one piece per slot.

WHY
---
A guild member did this by hand: fed three class gear pages to an AI and asked
for the best combination across all three, "with some light coaching about how
you want to weight stats". It worked, and it is a good idea. It also requires
owning an AI subscription, knowing how to prompt one, and being willing to trust
an answer you cannot check.

This does the same job as a tool, from data anyone can audit: 116 planar pieces
mined from eqlwiki item infoboxes on 11 August 2026, with the source's absences
kept as absences.

WHAT MAKES IT DIFFERENT FROM A SPREADSHEET
------------------------------------------
A character in Legends carries three classes at once, so it can wear any piece
any of its three classes can wear - plus the two shared sets. That is a pool of
five sets per slot rather than one, and it is genuinely hard to hold in your
head. The tool exists to make that pool visible and let you commit to a target,
not to tell you what to want.

THE PRESETS ARE THE POINT
-------------------------
"Configure your weights" is how a tool loses the person it was built for. Four
named presets, each one a sentence a player would actually say. The scores are
printed so the ranking can be argued with.

WHAT IT DOES NOT DO
-------------------
It does not pretend to know drop rates, it does not rank sets against each
other overall, and it does not fill in a stat the wiki left blank. Beastlord has
two documented pieces and Berserker three; the tool says so where it shows them
rather than presenting a short list as a complete one.

THE DATA LIVES IN _build/planardata.py
--------------------------------------
This file used to compute the 116 pieces and write assets/planar.json as well as
render the page. Four other generators read that dataset — /sets/, the inventory
reader, the measured-drop matcher and the contamination scanner — so a page
generator was the sole producer of data a published contract depends on.
It renders. It does not write the dataset.
"""
import os, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot
from planardata import ITEMS, N_MISSING, BY_SET, DATA

CSS = '''<style>
.pg-step{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.2em;
  text-transform:uppercase;color:var(--faint);margin:0 0 10px}
.pg-classes{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:6px}
.pg-c{font-family:"Saira Condensed",sans-serif;font-size:16px;font-weight:600;
  text-transform:uppercase;letter-spacing:.03em;padding:7px 13px;border:1px solid var(--rule);
  color:var(--mut);transition:all .12s;background:transparent}
.pg-c:hover{color:var(--bone);border-color:var(--rule2)}
.pg-c[aria-pressed="true"]{border-color:var(--bone);color:var(--ground);background:var(--bone)}
.pg-c[disabled]{opacity:.32;cursor:not-allowed}
.pg-presets{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 6px}
.pg-p{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.08em;
  text-transform:uppercase;padding:8px 12px;border:1px solid var(--rule);color:var(--mut)}
.pg-p[aria-pressed="true"]{border-color:var(--instr);color:var(--instr);
  background:color-mix(in srgb, var(--instr) 12%, transparent)}
.pg-slot{border-top:1px solid var(--rule);padding:20px 0 6px}
.pg-slot h3{font-family:"Saira Condensed",sans-serif;font-size:21px;font-weight:700;
  text-transform:uppercase;letter-spacing:.03em;margin:0 0 3px;color:var(--bone)}
.pg-sub{font-family:"IBM Plex Mono",monospace;font-size:10.5px;color:var(--faint);
  letter-spacing:.09em;text-transform:uppercase;margin:0 0 12px}
.pg-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,268px),1fr));gap:8px}
.pg-card{border:1px solid var(--rule);background:var(--panel);padding:12px 14px;
  text-align:left;display:grid;gap:7px;transition:border-color .12s,background .12s}
.pg-card:hover{border-color:var(--rule2)}
.pg-card[aria-pressed="true"]{border-color:var(--ok);
  background:color-mix(in srgb, var(--ok) 9%, var(--panel))}
.pg-nm{font-family:"Saira Condensed",sans-serif;font-size:17px;font-weight:600;
  color:var(--bone);line-height:1.15;display:flex;justify-content:space-between;gap:10px}
.pg-score{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--instr);flex:0 0 auto}
.pg-card[aria-pressed="true"] .pg-score{color:var(--ok)}
.pg-set{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--faint)}
.pg-stats{display:flex;flex-wrap:wrap;gap:3px 8px;font-family:"IBM Plex Mono",monospace;
  font-size:11.5px;color:var(--dim)}
.pg-stats b{color:var(--bone);font-weight:500}
.pg-fx{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--warn)}
.pg-none{border:1px dashed var(--rule);padding:16px;color:var(--mut);font-size:14px}
.pg-lock{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--ok)}
.pg-summary{position:sticky;bottom:0;background:rgba(14,19,21,.97);backdrop-filter:blur(10px);
  border-top:1px solid var(--rule2);padding:13px 0;margin-top:26px;z-index:20}
.pg-tot{display:flex;flex-wrap:wrap;gap:5px 16px;font-family:"IBM Plex Mono",monospace;
  font-size:12px;color:var(--dim)}
.pg-tot b{color:var(--bone)}
.pg-t{font-family:"IBM Plex Mono",monospace;font-size:9px;letter-spacing:.12em;
  text-transform:uppercase;color:#D9A227;border:1px solid rgba(217,162,39,.45);
  border-radius:2px;padding:1px 5px;margin-left:7px;white-space:nowrap}
.pg-warn{border-left:3px solid var(--warn);padding:3px 0 3px 14px;margin:14px 0;
  color:var(--mut);font-size:13.5px;line-height:1.6}
</style>'''

BODY = f'''
<main>
<div class="shell">
  <div class="page-head">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp;
      <a href="index.html">Tools</a> &nbsp;/&nbsp; Planar gear</p>
    <h1>Planar gear targets</h1>
    <p class="lede">Your trio can wear planar armour from all three of its classes, plus the two
      shared sets. That is five sets competing for every slot. Pick your three classes, choose
      what you are optimising for, and lock a target for each slot.
      <strong>{len(ITEMS)} pieces</strong> across
      <strong>{len(BY_SET)} sets</strong>, every figure from the item&rsquo;s own record.</p>
  </div>
</div>

<div class="shell">
  <div class="note" style="margin-bottom:18px"><strong>Every stat here is
    <span class="tier t3">T3</span> &mdash; a classic-era item record, not confirmed against
    Legends piece by piece.</strong> That matters more in this tool than in a table: a ranking
    tells you what to chase, and the ranking is only as good as the records under it. The badge
    repeats on every card and on your locked total so it is never off screen when you decide.</div>
  <p class="pg-step">Step 1 &mdash; your three classes</p>
  <div class="pg-classes" id="cls"></div>
  <p class="pg-sub" id="clshint">Pick three.</p>

    <p class="lede" style="margin-top:8px">Want the whole of every set rather than a ranking?
      <a href="../sets/index.html">All 18 sets, piece by piece &rarr;</a></p>
  <p class="pg-step" style="margin-top:22px">Step 2 &mdash; what are you optimising for</p>
  <div class="pg-presets" id="presets"></div>
  <p class="pg-sub" id="phint"></p>
</div>

<div class="shell" id="slots"></div>

<div class="pg-summary"><div class="shell">
  <div class="pg-tot" id="tot"><span>Pick three classes to begin.</span></div>
</div></div>

<div class="shell">
  <div class="note" style="margin-top:26px"><strong>Where these numbers come from.</strong>
    Every stat is read from that item&rsquo;s own page on eqlwiki, mined 11 August 2026. A blank
    on the source is shown as nothing here, never as a zero.
    <strong>These are classic-era item records</strong> &mdash; they are the best available and
    they have not been confirmed against Legends piece by piece. Where a set looks short, it is
    short on the wiki: <span id="thin"></span></div>
  <div class="note"><strong>One assumption, stated.</strong> The tool offers you any piece one of
    your three classes can wear. That follows how multiclass works elsewhere in the game, but we
    have not confirmed it for equipment specifically. If you find a piece your trio cannot equip,
    <a href="https://github.com/samusmylove47-maker/eql-source/issues/new?template=finding.yml">tell
    us</a> and we will correct it.</div>
  <div class="note"><strong>Wrist counts twice.</strong> You wear two, so the tool lets you lock
    two. The planar sets carry no rings or earrings, so those slots are not offered rather than
    guessed at.</div>
</div>
</main>
'''

SCRIPT = ('<script>window.__PG__=' + json.dumps(DATA, separators=(",", ":")) + ';</script>'
          + '''<script>
(function(){
  var D=window.__PG__, $=function(s){return document.querySelector(s)};
  var KEY="eqlplanar:autosave";
  var trio=[], preset="ac", picks={};

  var PRESETS=[
    {k:"ac",   n:"Highest AC",        h:"Straight armour class. What most people mean by best.",
     f:function(i){return i.ac||0}},
    {k:"cast", n:"Mana and casting",  h:"Mana plus INT plus WIS, for a trio that spends its time casting.",
     f:function(i){return (i.mana||0)+(i.int||0)+(i.wis||0)}},
    {k:"all",  n:"Most total stats",  h:"Every attribute added up, plus hit points. A generalist.",
     f:function(i){return (i.str||0)+(i.sta||0)+(i.agi||0)+(i.dex||0)+(i.wis||0)+(i.int||0)+(i.cha||0)+(i.hp||0)}},
    {k:"fx",   n:"Clicky effects first", h:"Anything with a named effect wins, then AC breaks the tie.",
     f:function(i){return (i.fx?10000:0)+(i.ac||0)}},
    {k:"save", n:"Resistances",       h:"All five saves added together.",
     f:function(i){return (i.svmagic||0)+(i.svfire||0)+(i.svcold||0)+(i.svdisease||0)+(i.svpoison||0)}}
  ];
  var scorer=function(){for(var i=0;i<PRESETS.length;i++)if(PRESETS[i].k===preset)return PRESETS[i];return PRESETS[0]};

  // ---- state travels in the URL, same as every other tool here -------------
  function save(){
    var s=trio.join(",")+"|"+preset+"|"+Object.keys(picks).map(function(k){
      return k+"="+picks[k].join("~")}).join(";");
    try{localStorage.setItem(KEY,s)}catch(e){}
    history.replaceState(null,"","#"+encodeURIComponent(s));
  }
  function load(s){
    if(!s)return false;
    var p=s.split("|"); if(p.length<2)return false;
    trio=p[0]?p[0].split(","):[]; preset=p[1]||"ac"; picks={};
    (p[2]||"").split(";").forEach(function(chunk){
      if(!chunk)return; var kv=chunk.split("="); if(kv.length<2)return;
      picks[kv[0]]=kv[1].split("~").filter(Boolean);
    });
    return true;
  }

  function wearable(it){
    if(!trio.length)return false;
    for(var i=0;i<it.c.length;i++) if(trio.indexOf(it.c[i])>-1) return true;
    return false;
  }
  function candidates(slot){
    return D.items.filter(function(i){return i.s===slot && wearable(i)});
  }
  var STAT=[["ac","AC"],["str","STR"],["sta","STA"],["agi","AGI"],["dex","DEX"],
            ["wis","WIS"],["int","INT"],["cha","CHA"],["hp","HP"],["mana","MANA"],
            ["svmagic","MR"],["svfire","FR"],["svcold","CR"],["svdisease","DR"],["svpoison","PR"]];

  function statLine(i){
    return STAT.filter(function(s){return i[s[0]]!=null})
      .map(function(s){return '<span>'+s[1]+' <b>'+i[s[0]]+'</b></span>'}).join("");
  }

  function drawClasses(){
    $("#cls").innerHTML=D.classes.map(function(c){
      var on=trio.indexOf(c)>-1;
      var full=trio.length>=3 && !on;
      return '<button class="pg-c" data-c="'+c+'" aria-pressed="'+on+'"'+(full?' disabled':'')+
             ' title="'+D.classNames[c]+'">'+c+'</button>';
    }).join("");
    $("#clshint").textContent = trio.length<3
      ? "Pick "+(3-trio.length)+" more."
      : trio.map(function(c){return D.classNames[c]}).join(" · ");
  }
  function drawPresets(){
    $("#presets").innerHTML=PRESETS.map(function(p){
      return '<button class="pg-p" data-p="'+p.k+'" aria-pressed="'+(p.k===preset)+'">'+p.n+'</button>'
    }).join("");
    $("#phint").innerHTML=scorer().h+
      ' <span class="pg-t">Scored from T3 data</span>';
  }

  function drawSlots(){
    if(trio.length<3){ $("#slots").innerHTML=""; return; }
    var sc=scorer();
    $("#slots").innerHTML=D.slots.map(function(slot){
      var n=D.double[slot]||1;
      var list=candidates(slot).slice().sort(function(a,b){
        var d=sc.f(b)-sc.f(a); return d||a.n.localeCompare(b.n)});
      var chosen=picks[slot]||[];
      var body = list.length ? '<div class="pg-cards">'+list.map(function(i){
          var on=chosen.indexOf(i.n)>-1;
          return '<button class="pg-card" data-slot="'+slot+'" data-n="'+i.n.replace(/"/g,"&quot;")+'"'+
                 ' aria-pressed="'+on+'">'+
                 '<span class="pg-nm">'+i.n+'<span class="pg-score">'+sc.f(i)+'</span></span>'+
                 '<span class="pg-set">'+i.set+(i.cls?" · "+i.cls:" · shared")+
                 '<span class="pg-t">T3</span></span>'+
                 '<span class="pg-stats">'+statLine(i)+'</span>'+
                 (i.fx?'<span class="pg-fx">Effect: '+i.fx+'</span>':'')+
                 (on?'<span class="pg-lock">Locked as your target</span>':'')+
                 '</button>'}).join("")+'</div>'
        : '<div class="pg-none">Nothing recorded for this slot that your trio can wear. That is a '+
          'gap in the source, not an empty slot in the game.</div>';
      return '<section class="pg-slot"><h3>'+slot+(n>1?' <span class="pg-score">wear '+n+'</span>':'')+'</h3>'+
             '<p class="pg-sub">'+list.length+' available'+(n>1?' · lock up to '+n:'')+
             (chosen.length?' · '+chosen.length+' locked':'')+'</p>'+body+'</section>';
    }).join("");
  }

  function drawTotals(){
    var tot={}, locked=0;
    D.slots.forEach(function(s){
      (picks[s]||[]).forEach(function(nm){
        var it=D.items.filter(function(i){return i.n===nm&&i.s===s})[0];
        if(!it)return; locked++;
        STAT.forEach(function(st){ if(it[st[0]]!=null) tot[st[0]]=(tot[st[0]]||0)+it[st[0]] });
      });
    });
    var slotsTotal=D.slots.reduce(function(a,s){return a+(D.double[s]||1)},0);
    if(!locked){ $("#tot").innerHTML='<span>'+(trio.length<3?'Pick three classes to begin.'
      :'Nothing locked yet. Click a card to set it as your target.')+'</span>'; return; }
    $("#tot").innerHTML='<span><b>'+locked+'</b> of '+slotsTotal+' targets locked</span>'+
      '<span class="pg-t">T3 &mdash; classic-era item records</span>'+
      STAT.filter(function(s){return tot[s[0]]}).map(function(s){
        return '<span>'+s[1]+' <b>'+tot[s[0]]+'</b></span>'}).join("");
  }

  function redraw(){ drawClasses(); drawPresets(); drawSlots(); drawTotals(); save(); }

  document.addEventListener("click",function(e){
    var c=e.target.closest("[data-c]");
    if(c && !c.disabled){
      var k=c.dataset.c, at=trio.indexOf(k);
      if(at>-1) trio.splice(at,1); else if(trio.length<3) trio.push(k);
      // a piece locked for a class you just dropped is no longer yours to want
      Object.keys(picks).forEach(function(s){
        picks[s]=picks[s].filter(function(nm){
          var it=D.items.filter(function(i){return i.n===nm})[0];
          return it && wearable(it)});
        if(!picks[s].length) delete picks[s];
      });
      redraw(); return;
    }
    var p=e.target.closest("[data-p]");
    if(p){ preset=p.dataset.p; redraw(); return; }
    var card=e.target.closest(".pg-card");
    if(card){
      var slot=card.dataset.slot, nm=card.dataset.n, max=D.double[slot]||1;
      var cur=picks[slot]||[], at=cur.indexOf(nm);
      if(at>-1) cur.splice(at,1);
      else { cur.push(nm); if(cur.length>max) cur.shift(); }
      if(cur.length) picks[slot]=cur; else delete picks[slot];
      redraw();
    }
  });

  var thin=Object.keys(D.thin).map(function(s){
    return s+" has "+D.thin[s]+" piece"+(D.thin[s]===1?"":"s")+" recorded"}).join(", ");
  $("#thin").textContent = thin ? thin+". Beastlord and Berserker did not exist in classic "+
    "EverQuest, which is why their sets are the least documented." : "every set is complete.";

  if(!load(decodeURIComponent(location.hash.slice(1)))){
    try{ load(localStorage.getItem(KEY)) }catch(e){}
  }
  redraw();
})();
</script>''')

page = (head("Planar gear targets",
             "Pick your three classes and target the best planar armour available to you across "
             "all three class sets plus Lustrous Russet and Midnight Clad. "
             f"{len(ITEMS)} pieces, every stat from the item's own record.",
             rel="../", extra=CSS, og="tools", canon="tools/planar-gear")
        + bar("../") + BODY + foot("../").replace('</body>', SCRIPT + '\n</body>'))

open('public/tools/planar-gear.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"tools/planar-gear.html: {len(ITEMS)} pieces, {len(BY_SET)} sets, "
      f"{N_MISSING} unrecorded fields kept blank")
