"""tools/route.html — a levelling route for one trio, from any level to 50.

WHAT IT DOES
------------
Takes a class trio and a starting level and returns an ordered list of zones to
work through, each with the level window it covers and the items that trio can
actually use there. Every stop links to its survey.

WHY WE CAN BUILD THIS AND THE OTHER SITES CANNOT
------------------------------------------------
The join needs three things at once: zone level bands, zone experience
modifiers, and per-item class restrictions tied to the zone that drops them.
The first two are in assets/zones-index.json and the third is in
assets/index-data.json, mined from our own surveys. A tool that has the items
but not the surveys cannot say which zone to be in; a tool that has the zones
but not the item-to-class mapping cannot say what to pick up on the way.

WHAT IT IS NOT, AND THE PAGE SAYS SO
------------------------------------
It orders zones. It does not predict how long anything takes, because nothing in
our data measures that: ZEM is a multiplier on experience per kill, not a rate,
and we have no measurement of kills per hour for any trio. Any hours figure here
would be invented, so there is none.

It also does not know your gear, your group size, what is already camped, or
whether you can survive the top of a band. Those are the reasons a route that
reads well can still be wrong, and the reason the page asks for corrections.

ITEM ORDER IS NOT ARBITRARY
---------------------------
index-data.json preserves the order items appear on the survey, and every survey
puts its chase items first. So taking the first matches per zone surfaces the
things worth a detour rather than the first alphabetically. That is a real
signal from the data, not a ranking we invented.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

Z = json.load(open('assets/zones-index.json', encoding='utf-8'))
IX = json.load(open('assets/index-data.json', encoding='utf-8'))

CLASSES = {
    "WAR": "Warrior", "CLR": "Cleric", "PAL": "Paladin", "RNG": "Ranger",
    "SHD": "Shadow Knight", "DRU": "Druid", "MNK": "Monk", "BRD": "Bard",
    "ROG": "Rogue", "SHM": "Shaman", "NEC": "Necromancer", "WIZ": "Wizard",
    "MAG": "Magician", "ENC": "Enchanter", "BST": "Beastlord", "BER": "Berserker",
}


def band(text):
    """(lo, hi, tuned_lo, tuned_hi) from a zone's recorded level string.

    The strings are not uniform because the sources are not: "4-22", "7-25+",
    "8-35 (tuned 15-30)", and Splitpaw's "25-28 entrance ramping to 40-42 deep".
    Where a zone records a tuned range, that is the band people actually work,
    and the wider one is what the zone technically holds.
    """
    nums = [int(n) for n in re.findall(r'\d+', text)]
    if not nums:
        return None
    lo, hi = nums[0], max(nums)
    tuned = re.search(r'tuned\s*(\d+)\s*[-–]\s*(\d+)', text)
    if tuned:
        return lo, hi, int(tuned.group(1)), int(tuned.group(2))
    return lo, hi, lo, hi


ZONES = []
for z in sorted(Z, key=lambda x: x['plate']):
    b = band(z['levels'])
    if not b:
        continue
    lo, hi, tlo, thi = b
    items = []
    for it in IX['items']:
        if it['z'] != z['slug']:
            continue
        items.append({"n": it['n'], "s": it.get('s') or '', "c": it['c'],
                      "d": (it.get('d') or '').split('·')[0].strip()})
    ZONES.append({"slug": z['slug'], "t": z['title'], "a": z['accent'],
                  "lo": lo, "hi": hi, "tlo": tlo, "thi": thi,
                  "zem": z['zem'], "rs": z['respawn'] or "not recorded",
                  "it": items})

ZJS = json.dumps(ZONES, separators=(",", ":"))
CJS = json.dumps(CLASSES, separators=(",", ":"))

CSS = '''<style>
.rt-form{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;
  margin:24px 0 0;padding:18px 20px;border:1px solid var(--line);border-radius:5px;
  background:var(--panel,#151B1F)}
.rt-form label{display:block;font-family:"IBM Plex Mono",monospace;font-size:10.5px;
  letter-spacing:.14em;text-transform:uppercase;color:var(--faint);margin:0 0 4px}
.rt-form select,.rt-form input{width:100%;padding:9px 10px;background:#10161A;
  border:1px solid var(--line);border-radius:4px;color:var(--ink);
  font-family:"IBM Plex Mono",monospace;font-size:14.5px}
.rt-form select:focus,.rt-form input:focus{outline:2px solid var(--instr);outline-offset:1px}
.stop{border:1px solid var(--line);border-left:4px solid var(--c);border-radius:5px;
  background:var(--panel,#151B1F);padding:17px 20px;margin:0 0 14px}
.stop-h{display:flex;gap:14px;align-items:baseline;flex-wrap:wrap}
.stop-n{font-family:"IBM Plex Mono",monospace;font-size:23px;color:var(--c)}
.stop-h h3{margin:0;font-family:"Saira Condensed",sans-serif;font-weight:600;font-size:22px;
  text-transform:uppercase;letter-spacing:.02em;color:var(--ink)}
.stop-h h3 a{color:inherit;text-decoration:none;border-bottom:1px solid var(--line)}
.stop-h h3 a:hover{border-color:var(--c)}
.stop-lv{font-family:"IBM Plex Mono",monospace;font-size:13px;color:var(--dim);
  border:1px solid var(--line);border-radius:3px;padding:2px 8px}
.stop-m{font-family:"IBM Plex Mono",monospace;font-size:11.5px;color:var(--faint);
  letter-spacing:.06em;margin:8px 0 0}
.picks{list-style:none;margin:12px 0 0;padding:0;display:grid;
  grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:6px}
.picks li{font-size:13.5px;color:var(--dim);border-left:2px solid var(--line);padding:2px 0 2px 9px}
.picks b{color:var(--ink);font-weight:600}
.picks span{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--faint);display:block}
.rt-none{color:var(--faint);font-size:13.5px;margin:10px 0 0}
.also{margin:11px 0 0;font-size:13.5px;color:var(--dim);line-height:1.7}
.also b{color:var(--faint);font-family:"IBM Plex Mono",monospace;font-size:10.5px;
  letter-spacing:.13em;text-transform:uppercase;display:block;margin:0 0 3px}
.also a{color:var(--ink);border-bottom:1px solid var(--line);text-decoration:none}
.also span{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--faint)}
.rt-sum{margin:20px 0 16px;font-size:15px;color:var(--dim)}
.rt-sum b{color:var(--ink)}
.rt-warn{margin:14px 0 0;padding:12px 14px;border-left:3px solid var(--warn-t);
  background:rgba(201,69,58,.06);color:var(--dim);font-size:13.5px;line-height:1.6}
</style>'''

page = head("Levelling route",
  "Build an EverQuest Legends levelling route for your class trio from any level to 50: which "
  "zone at which level, and what each one drops that your three classes can use.",
  rel="../", extra=CSS, og="tools", canon="tools/route") + bar("../") + f'''
<main>
<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp;
      <a href="index.html">Tools</a> &nbsp;/&nbsp; Levelling route</p>
    <h1 class="display">Where to go,<br><em>and what to take.</em></h1>
    <p class="hero-lede">Pick your three classes and a starting level. It orders the ten surveyed
      zones by the level band each one covers and how much experience it returns, then lists what
      each drops that <em>your</em> trio can actually wear or wield.</p>
    <p class="hero-sig"><span>Ten zones</span><span>452 items filtered</span>
      <span>Every stop sourced</span></p>
  </div>
</section>

<section class="band" style="border-top:0;padding-top:0">
  <div class="shell">
    <div class="rt-form">
      <div><label for="r-t1">Class one</label><select id="r-t1"></select></div>
      <div><label for="r-t2">Class two</label><select id="r-t2"></select></div>
      <div><label for="r-t3">Class three</label><select id="r-t3"></select></div>
      <div><label for="r-lv">Starting level</label><input id="r-lv" type="number" min="1" max="49" value="10"></div>
    </div>

    <p class="rt-sum" id="r-sum"></p>
    <div id="r-out"></div>

    <div class="rt-warn"><strong>What this is not.</strong> It orders zones. It does not predict how
      long anything takes, because nothing we hold measures that &mdash; the zone experience
      modifier multiplies experience per kill, it is not a rate, and we have no kills-per-hour
      figure for any trio. An hours estimate here would be invented, so there is not one.
      <br><br>It also does not know your gear, your group, what is already camped, or whether you
      can survive the top of a band. If a stop is wrong for a reason like that,
      <a href="https://github.com/samusmylove47-maker/eql-source/issues/new?template=finding.yml">tell
      us</a> &mdash; that is exactly the correction we cannot make from here.</div>
  </div>
</section>
</main>
''' + foot("../") + f'''
<script>
(function(){{
const ZONES={ZJS}, CLASSES={CJS};
const $=s=>document.querySelector(s);
const esc=s=>String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");

function usable(item,trio){{
  if(item.c.includes("ALL"))return trio.length;
  return trio.filter(c=>item.c.includes(c)).length;
}}

function build(trio,start){{
  // For each level window, the zone with the best experience return AND the
  // other zones that cover it.
  //
  // Ranking on experience alone produced three stops for a whole career and
  // ignored seven of the ten surveys, because the three highest-ZEM zones happen
  // to tile 4 to 50 between them. That is a defensible answer to "where is
  // experience fastest" and a useless answer to "where should I go", which is
  // the question being asked. Neither is it our place to decide that a haste
  // belt beats a faster kill: the window shows both and the reader picks.
  const best=[];
  const from=Math.max(1,Math.min(49,start|0));
  for(let lv=from; lv<50; lv++){{
    const open=ZONES.filter(z=>lv>=z.lo && lv<z.hi);
    open.sort((a,b)=>{{
      const at=(lv>=a.tlo&&lv<=a.thi)?1:0, bt=(lv>=b.tlo&&lv<=b.thi)?1:0;
      if(at!==bt)return bt-at;
      if(b.zem!==a.zem)return b.zem-a.zem;
      return (a.hi-a.lo)-(b.hi-b.lo);
    }});
    best.push(open.length?open[0]:null);
  }}
  const route=[]; let i=0;
  while(i<best.length){{
    const z=best[i];
    let j=i; while(j<best.length && best[j]===z) j++;
    if(z){{
      const lo=from+i, hi=Math.min(from+j,50);
      // everything else open across this window, most useful loot first
      const also=ZONES.filter(x=>x!==z && x.lo<hi && x.hi>lo)
        .map(x=>({{z:x, n:x.it.filter(it=>usable(it,trio)>0).length}}))
        .sort((a,b)=>b.n-a.n || b.z.zem-a.z.zem);
      route.push({{z, from:lo, to:hi, also}});
    }}
    i=j;
  }}
  return route;
}}

function render(){{
  const trio=["#r-t1","#r-t2","#r-t3"].map(s=>$(s).value).filter(Boolean);
  const start=parseInt($("#r-lv").value||"10",10);
  if(trio.length<1){{
    $("#r-sum").innerHTML="Pick at least one class to see a route.";
    $("#r-out").innerHTML=""; return;
  }}
  const route=build(trio,start);
  const names=trio.map(c=>CLASSES[c]).join(", ");
  $("#r-sum").innerHTML=route.length
    ? `<b>${{route.length}} stops</b> from level ${{start}} to 50 for ${{esc(names)}}.`
    : `Nothing in the ten surveyed zones covers level ${{start}} upward.`;

  $("#r-out").innerHTML=route.map((s,i)=>{{
    const picks=s.z.it.filter(it=>usable(it,trio)>0).slice(0,6);
    const total=s.z.it.filter(it=>usable(it,trio)>0).length;
    const li=picks.map(p=>{{
      const n=usable(p,trio);
      const who=p.c.includes("ALL")?"all three":
        trio.filter(c=>p.c.includes(c)).map(c=>CLASSES[c]).join(", ");
      return `<li><b>${{esc(p.n)}}</b><span>${{esc(p.s)}} &middot; ${{esc(who)}}`
           + (p.d?` &middot; off ${{esc(p.d)}}`:"")+`</span></li>`;
    }}).join("");
    return `<article class="stop" style="--c:${{s.z.a}}">
      <div class="stop-h">
        <span class="stop-n">${{String(i+1).padStart(2,"0")}}</span>
        <h3><a href="../dungeons/${{s.z.slug}}.html">${{esc(s.z.t)}}</a></h3>
        <span class="stop-lv">level ${{s.from}} to ${{s.to}}</span>
      </div>
      <p class="stop-m">ZEM ${{s.z.zem}} &middot; respawn ${{esc(s.z.rs)}} &middot;
        zone band ${{s.z.lo}}&ndash;${{s.z.hi}}</p>
      ${{s.also.length ? `<p class="also"><b>Also open at ${{s.from}}&ndash;${{s.to}}:</b> `
        + s.also.map(o=>`<a href="../dungeons/${{o.z.slug}}.html">${{esc(o.z.t)}}</a>`
            + ` <span>ZEM ${{o.z.zem}}${{o.n?`, ${{o.n}} for this trio`:", nothing for this trio"}}</span>`).join(" &middot; ")
        + `</p>` : ""}}
      ${{picks.length
        ? `<ul class="picks">${{li}}</ul>`+(total>picks.length
            ? `<p class="rt-none">${{total-picks.length}} more here your trio can use &mdash; <a href="../dungeons/${{s.z.slug}}.html">the full loot table</a>.</p>`
            : "")
        : `<p class="rt-none">Nothing recorded here that this trio can use. You come for the experience, not the loot.</p>`}}
    </article>`;
  }}).join("");
}}

const order=Object.keys(CLASSES);
["#r-t1","#r-t2","#r-t3"].forEach((s,i)=>{{
  $(s).innerHTML='<option value="">Choose…</option>'+
    order.map(k=>`<option value="${{k}}">${{CLASSES[k]}}</option>`).join("");
  $(s).addEventListener("change",render);
}});
$("#r-lv").addEventListener("input",render);

// Seed from the character sheet if one is saved on this browser.
try{{
  const c=localStorage.getItem("eqlchar:autosave")||"";
  const t=/(?:^|&)t=([^&]+)/.exec(c.replace(/^#/,""));
  const l=/(?:^|&)lv=([^&]+)/.exec(c.replace(/^#/,""));
  if(t){{const a=t[1].split(".");["#r-t1","#r-t2","#r-t3"].forEach((s,i)=>{{if(a[i])$(s).value=a[i];}});}}
  if(l&&l[1])$("#r-lv").value=l[1];
}}catch(e){{}}
render();
}})();
</script>
</body>
</html>'''

open('public/tools/route.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"tools/route.html written: {len(ZONES)} zones, "
      f"{sum(len(z['it']) for z in ZONES)} items available to filter")
