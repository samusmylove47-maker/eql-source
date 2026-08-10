"""tools/character.html — one sheet, one link.

WHAT THIS SOLVES
----------------
The site had three save states: the race tracker, the Plane of Sky tracker, and
the combo calculator sharing the race tracker's key. Three links to keep, three
things to lose. Nobody keeps three links.

This is one sheet that carries all of it in a single URL fragment. No account,
no server, nothing transmitted — the fragment is never sent to the host, which
is the same promise the trackers already make and the reason not to build a
database for this.

THE DESIGN DECISION THAT MATTERS
--------------------------------
The sheet CARRIES the tracker states verbatim rather than re-implementing them.
Each tracker owns a compact hash of its own; the sheet stores those two strings
inside its own fragment and writes them back into the trackers' localStorage on
load. So if a tracker changes its bit layout tomorrow, the sheet keeps working
and needs no update. A carrier cannot drift from what it carries.

WHAT IT DECODES, AND WHAT IT DELIBERATELY DOES NOT
--------------------------------------------------
Race unlocks are decoded and counted here. The bit layout is 2 flags plus one
per required faction, per race, and assets/faction-data.json holds exactly those
faction lists — verified identical to the tracker's own table before this was
written.

Plane of Sky progress is NOT decoded. Its layout is one bit per quest plus one
per component, and parsing the quest structure out of the tracker gave 200
components where the tool reports 222. A count that might be wrong is worse than
no count, so the sheet shows the trio and the character name — both plain text
in the tracker's own fragment — and links out for the detail.

Epic progress is not here at all. The site holds no structured epic quest data,
only components named in loot tables, and inventing a checklist is not an option.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

FD = json.load(open('assets/faction-data.json', encoding='utf-8'))
RACES = FD['races']
RORDER = ["DEF", "ELF", "HUMQ", "HIE", "HEF", "GNM", "DWF", "KER",
          "HUMF", "BAR", "FRG", "IKS", "ERU", "TRL", "HFL", "OGR"]
CLASSES = {
    "WAR": "Warrior", "CLR": "Cleric", "PAL": "Paladin", "RNG": "Ranger",
    "SHD": "Shadow Knight", "DRU": "Druid", "MNK": "Monk", "BRD": "Bard",
    "ROG": "Rogue", "SHM": "Shaman", "NEC": "Necromancer", "WIZ": "Wizard",
    "MAG": "Magician", "ENC": "Enchanter", "BST": "Beastlord", "BER": "Berserker",
}

RACE_JS = json.dumps({r: {"name": RACES[r]["name"],
                          "facs": len(RACES[r].get("factions", []))}
                      for r in RORDER}, separators=(",", ":"))
ORDER_JS = json.dumps(RORDER, separators=(",", ":"))
CLASS_JS = json.dumps(CLASSES, separators=(",", ":"))

CSS = '''<style>
.sheet{display:grid;gap:18px;margin:26px 0 0}
.card2{border:1px solid var(--line);border-radius:5px;background:var(--panel,#151B1F);padding:18px 20px}
.card2 h2{margin:0 0 4px;font-family:"Saira Condensed",sans-serif;font-weight:600;
  text-transform:uppercase;letter-spacing:.02em;font-size:19px;color:var(--ink)}
.card2 .sub{margin:0 0 14px;color:var(--faint);font-size:13px}
.idgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}
.idgrid label{display:block;font-family:"IBM Plex Mono",monospace;font-size:10.5px;
  letter-spacing:.14em;text-transform:uppercase;color:var(--faint);margin:0 0 4px}
.idgrid input,.idgrid select{width:100%;padding:9px 10px;background:#10161A;
  border:1px solid var(--line);border-radius:4px;color:var(--ink);font-size:14.5px;
  font-family:"IBM Plex Mono",monospace}
.idgrid input:focus,.idgrid select:focus{outline:2px solid var(--instr);outline-offset:1px}
.stat{display:flex;gap:26px;flex-wrap:wrap;margin:0 0 12px}
.stat div{min-width:96px}
.stat b{display:block;font-family:"IBM Plex Mono",monospace;font-size:27px;color:var(--ink)}
.stat span{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--faint)}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 0}
.chip2{font-family:"IBM Plex Mono",monospace;font-size:12px;padding:3px 9px;border-radius:3px;
  border:1px solid var(--line);color:var(--dim)}
.chip2.on{border-color:var(--ok);color:var(--ok)}
.chip2.want{border-color:var(--instr);color:var(--instr-t,#8FBEE4)}
.row{display:flex;gap:9px;flex-wrap:wrap;align-items:center;margin:14px 0 0}
.btn{padding:9px 15px;border-radius:4px;border:1px solid var(--line);background:#1A2126;
  color:var(--ink);font-family:"IBM Plex Mono",monospace;font-size:13px;cursor:pointer}
.btn:hover{border-color:var(--dim)}
.btn.primary{background:color-mix(in srgb,var(--instr) 20%,#1A2126);border-color:var(--instr)}
#link{width:100%;padding:10px;background:#10161A;border:1px solid var(--line);border-radius:4px;
  color:var(--dim);font-family:"IBM Plex Mono",monospace;font-size:12.5px;margin:10px 0 0}
.none{color:var(--faint);font-size:14px;margin:6px 0 0}
.card2 a{color:var(--instr-t,#8FBEE4)}
</style>'''

page = head("Character sheet",
  "One EverQuest Legends character sheet carrying your trio, race unlocks and Plane of Sky "
  "progress in a single link. No account, nothing transmitted.",
  rel="../", extra=CSS, og="tools", canon="tools/character") + bar("../") + f'''
<main>
<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp;
      <a href="index.html">Tools</a> &nbsp;/&nbsp; Character sheet</p>
    <h1 class="display">One sheet.<br><em>One link.</em></h1>
    <p class="hero-lede">Your trio, your race unlocks and your Plane of Sky progress in a single
      address you can bookmark or paste into guild chat. <strong>No account and nothing
      transmitted</strong> &mdash; everything after the <code>#</code> stays in your browser and is
      never sent to this site.</p>
    <p class="hero-sig"><span>One link</span><span>Nothing stored</span><span>Works offline</span></p>
  </div>
</section>

<section class="band" style="border-top:0;padding-top:0">
  <div class="shell">
    <div class="sheet">

      <div class="card2">
        <h2>Your character</h2>
        <p class="sub">Race and primary class lock at level 11. The trio uses the level of its
          lowest class.</p>
        <div class="idgrid">
          <div><label for="c-name">Name</label><input id="c-name" maxlength="24" placeholder="Avenrae"></div>
          <div><label for="c-race">Race</label><select id="c-race"></select></div>
          <div><label for="c-prim">Primary class</label><select id="c-prim"></select></div>
          <div><label for="c-lvl">Level</label><input id="c-lvl" type="number" min="1" max="50" placeholder="34"></div>
        </div>
        <div class="idgrid" style="margin-top:12px">
          <div><label for="c-t1">Class one</label><select id="c-t1"></select></div>
          <div><label for="c-t2">Class two</label><select id="c-t2"></select></div>
          <div><label for="c-t3">Class three</label><select id="c-t3"></select></div>
        </div>
      </div>

      <div class="card2">
        <h2>Race unlocks</h2>
        <p class="sub">Read from the race unlock tracker on this browser.</p>
        <div class="stat">
          <div><b id="r-done">0</b><span>Unlocked</span></div>
          <div><b id="r-want">0</b><span>On your route</span></div>
          <div><b id="r-left">16</b><span>Not started</span></div>
        </div>
        <div class="chips" id="r-chips"></div>
        <div class="row"><a class="btn" href="race-unlocks.html" id="r-open">Open the tracker &rarr;</a></div>
      </div>

      <div class="card2">
        <h2>Plane of Sky</h2>
        <p class="sub">Read from the Plane of Sky tracker on this browser.</p>
        <div class="stat">
          <div><b id="s-trio">&mdash;</b><span>Trio on the sheet</span></div>
        </div>
        <p class="none" id="s-none">Nothing saved yet. Pick a trio in the tracker and it appears here.</p>
        <div class="row"><a class="btn" href="plane-of-sky.html" id="s-open">Open the tracker &rarr;</a></div>
      </div>

      <div class="card2">
        <h2>Your link</h2>
        <p class="sub">Everything above, in one address. Bookmark it, paste it, mail it to yourself.</p>
        <input id="link" readonly>
        <div class="row">
          <button class="btn primary" id="copy">Copy link</button>
          <button class="btn" id="dl">Download as a file</button>
          <button class="btn" id="reset">Start over</button>
        </div>
        <p class="none"><strong>What is not here yet:</strong> epic quest progress. The site holds no
          structured epic data &mdash; only components named in loot tables &mdash; and a checklist
          invented from those would be a guess. It goes in when the data does.</p>
      </div>

    </div>
  </div>
</section>
</main>
''' + foot("../") + f'''
<script>
(function(){{
const RACES={RACE_JS}, RORDER={ORDER_JS}, CLASSES={CLASS_JS};
const RKEY="eqlrace:autosave", SKEY="posky:autosave", CKEY="eqlchar:autosave";
const $=s=>document.querySelector(s);
let st={{n:"",r:"",pc:"",lv:"",t:["","",""],R:"",S:""}};

function ls(k){{ try{{return localStorage.getItem(k)||"";}}catch(e){{return "";}} }}
function lset(k,v){{ try{{localStorage.setItem(k,v);}}catch(e){{}} }}

/* ---- carry, do not re-implement -------------------------------------- */
function compose(){{
  const p=["v=1"];
  if(st.n)p.push("n="+encodeURIComponent(st.n));
  if(st.r)p.push("r="+st.r);
  if(st.pc)p.push("pc="+st.pc);
  if(st.lv)p.push("lv="+st.lv);
  if(st.t.some(Boolean))p.push("t="+st.t.join("."));
  if(st.R)p.push("R="+encodeURIComponent(st.R));
  if(st.S)p.push("S="+encodeURIComponent(st.S));
  return "#"+p.join("&");
}}
function parse(h){{
  const p={{}};(h||"").replace(/^#/,"").split("&").forEach(kv=>{{
    const i=kv.indexOf("=");if(i>0)p[kv.slice(0,i)]=kv.slice(i+1);}});
  if(!p.v&&!p.R&&!p.S&&!p.n)return false;
  st.n=p.n?decodeURIComponent(p.n):"";
  st.r=p.r||""; st.pc=p.pc||""; st.lv=p.lv||"";
  st.t=(p.t||"").split(".").concat(["","",""]).slice(0,3);
  st.R=p.R?decodeURIComponent(p.R):"";
  st.S=p.S?decodeURIComponent(p.S):"";
  return true;
}}

/* ---- race unlocks: the one thing we decode --------------------------- */
function b64d(s){{s=s.replace(/-/g,"+").replace(/_/g,"/");
  const b=atob(s),o=new Uint8Array(b.length);
  for(let i=0;i<b.length;i++)o[i]=b.charCodeAt(i);return o;}}
function bitAt(u8,i){{return (u8[i>>3]>>(7-(i&7)))&1;}}
function raceProgress(){{
  const out={{done:[],want:[]}};
  const m=/(?:^|&)p=([^&]+)/.exec((st.R||"").replace(/^#/,""));
  if(!m)return out;
  let u8; try{{u8=b64d(m[1]);}}catch(e){{return out;}}
  let i=0;
  RORDER.forEach(r=>{{
    const owned=bitAt(u8,i), wanted=bitAt(u8,i+1);
    i+=2+RACES[r].facs;
    if(owned)out.done.push(r); else if(wanted)out.want.push(r);
  }});
  return out;
}}

/* ---- render ---------------------------------------------------------- */
function fillSelect(el,map,order,blank){{
  el.innerHTML='<option value="">'+blank+'</option>'+
    order.map(k=>`<option value="${{k}}">${{map[k].name||map[k]}}</option>`).join("");
}}
function render(){{
  $("#c-name").value=st.n; $("#c-lvl").value=st.lv;
  $("#c-race").value=st.r; $("#c-prim").value=st.pc;
  ["#c-t1","#c-t2","#c-t3"].forEach((s,i)=>$(s).value=st.t[i]||"");

  const rp=raceProgress();
  $("#r-done").textContent=rp.done.length;
  $("#r-want").textContent=rp.want.length;
  $("#r-left").textContent=RORDER.length-rp.done.length-rp.want.length;
  $("#r-chips").innerHTML=RORDER.map(r=>{{
    const cls=rp.done.includes(r)?"chip2 on":(rp.want.includes(r)?"chip2 want":"chip2");
    return `<span class="${{cls}}">${{RACES[r].name}}</span>`;}}).join("");

  const sc=/(?:^|&)c=([^&]+)/.exec((st.S||"").replace(/^#/,""));
  const trio=sc?sc[1].split(".").filter(Boolean):[];
  $("#s-trio").textContent=trio.length?trio.join(" · "):"—";
  $("#s-none").hidden=trio.length>0;

  // the tracker links carry the state, so opening one lands on your sheet
  $("#r-open").href="race-unlocks.html"+(st.R||"");
  $("#s-open").href="plane-of-sky.html"+(st.S||"");
  $("#link").value=location.origin+location.pathname+compose();
}}

function persist(){{
  const h=compose();
  try{{history.replaceState(null,"",location.pathname+h);}}catch(e){{}}
  lset(CKEY,h);
  // write the carried states back so each tracker opens where you left it
  if(st.R)lset(RKEY,st.R);
  if(st.S)lset(SKEY,st.S);
  render();
}}

function pull(){{ st.R=ls(RKEY)||st.R; st.S=ls(SKEY)||st.S; }}

/* ---- wire ------------------------------------------------------------ */
fillSelect($("#c-race"),RACES,RORDER,"Choose…");
const CORDER=Object.keys(CLASSES);
[["#c-prim"],["#c-t1"],["#c-t2"],["#c-t3"]].forEach(([s])=>
  fillSelect($(s),CLASSES,CORDER,"Choose…"));

$("#c-name").addEventListener("input",e=>{{st.n=e.target.value.slice(0,24);persist();}});
$("#c-lvl").addEventListener("input",e=>{{st.lv=e.target.value;persist();}});
$("#c-race").addEventListener("change",e=>{{st.r=e.target.value;persist();}});
$("#c-prim").addEventListener("change",e=>{{st.pc=e.target.value;persist();}});
["#c-t1","#c-t2","#c-t3"].forEach((s,i)=>
  $(s).addEventListener("change",e=>{{st.t[i]=e.target.value;persist();}}));

$("#copy").addEventListener("click",async()=>{{
  $("#link").select();
  try{{await navigator.clipboard.writeText($("#link").value);
    $("#copy").textContent="Copied";setTimeout(()=>$("#copy").textContent="Copy link",1400);}}
  catch(e){{document.execCommand&&document.execCommand("copy");}}
}});
$("#dl").addEventListener("click",()=>{{
  const blob=new Blob([JSON.stringify({{...st,link:$("#link").value}},null,1)],
    {{type:"application/json"}});
  const a=document.createElement("a");
  a.href=URL.createObjectURL(blob);
  a.download=(st.n||"character")+"-eqlsource.json";
  a.click();URL.revokeObjectURL(a.href);
}});
$("#reset").addEventListener("click",()=>{{
  if(!confirm("Clear this sheet? Your two trackers keep their own saves."))return;
  st={{n:"",r:"",pc:"",lv:"",t:["","",""],R:"",S:""}};
  lset(CKEY,"");persist();
}});

// A link beats a local save: arriving with one means you meant that character.
if(!parse(location.hash)){{ parse(ls(CKEY)); pull(); }}
else {{ if(st.R)lset(RKEY,st.R); if(st.S)lset(SKEY,st.S); }}
if(!st.R&&!st.S)pull();
render();
}})();
</script>
</body>
</html>'''

open('public/tools/character.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"tools/character.html written: {len(RORDER)} races, {len(CLASSES)} classes, "
      f"carries 2 tracker states")
