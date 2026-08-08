"""tools/faction-impact.html — what a night's grinding does to your unlocks.

Faction is a constant EverQuest problem and nobody has built a tool for it. You
grind a zone, and hours later a vendor will not speak to you, or an unlock you
had not started is now expensive.

Two sources, and the page keeps them visibly apart:

- WHAT A FACTION IS FOR comes from the race-unlock work, tier 3, Alanna's guide.
  Which races need it, which quest steps raise it.
- WHAT MOVES IT is measured from our own combat logs, tier M. Only zones we have
  actually played are covered, and the page says exactly which those are rather
  than implying the rest are safe.

The honesty problem here is particular: a faction tool that stays quiet about a
zone reads as "this zone is fine". So coverage is stated at the top, every
uncovered zone is listed by name, and the search says "not measured" rather
than returning nothing.
"""
import os, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

try:
    D = json.load(open('assets/faction-data.json', encoding='utf-8'))
except (OSError, ValueError):
    D = dict(steps={}, races={}, measured={})

ZONES = json.load(open('assets/zones-index.json', encoding='utf-8'))


def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


measured = D['measured']
steps, races = D['steps'], D['races']

# every faction we know anything about, and what we know
index = {}
for key, st in steps.items():
    for g in st['gain']:
        f = index.setdefault(g['faction'], dict(raised_by=[], needed_by=[], moved_in=[]))
        f['raised_by'].append(dict(step=st['name'], delta=g['delta'],
                                   zone=st['zone'], npc=st['npc']))
for code, r in races.items():
    for fac in r['factions']:
        index.setdefault(fac, dict(raised_by=[], needed_by=[], moved_in=[]))['needed_by'].append(r['name'])
for zone, z in measured.items():
    for mob, facs in z['per_mob'].items():
        for fac, delta in facs.items():
            index.setdefault(fac, dict(raised_by=[], needed_by=[], moved_in=[]))
            entry = next((e for e in index[fac]['moved_in'] if e['zone'] == zone), None)
            if not entry:
                entry = dict(zone=zone, per_kill=None, biggest=None, mob=None)
                index[fac]['moved_in'].append(entry)
            if entry['biggest'] is None or abs(delta) > abs(entry['biggest']):
                entry['biggest'], entry['mob'] = delta, mob
            if entry['per_kill'] is None or abs(delta) < abs(entry['per_kill']):
                entry['per_kill'] = delta

covered = sorted(measured)
uncovered = [z['title'] for z in ZONES
             if not any(z['title'].lower().split()[-1] in c.lower() for c in covered)]

zone_cards = ''
for zone, z in measured.items():
    def facline(names, sign):
        if not names:
            return '<li class="fnone">nothing recorded</li>'
        out = ''
        for f in names:
            e = next((e for e in index.get(f, {}).get('moved_in', []) if e['zone'] == zone), None)
            detail = ''
            if e:
                detail = (f'<span class="fdelta">{e["per_kill"]:+d} a kill'
                          + (f', up to {e["biggest"]:+d} from {esc(e["mob"])}'
                             if e['biggest'] != e['per_kill'] else '') + '</span>')
            # Three cases, not two. A faction can be required by a race, or
            # merely raised by a step that a race uses — and calling the second
            # "no unlock needs this" contradicted the step list printed directly
            # below, where King Tearis Thex plainly helps High Elf and Wood Elf.
            uses = index.get(f, {}).get('needed_by', [])
            via = sorted({r for e in (z.get('steps_helped', []) + z.get('steps_undone', []))
                          if f in e['factions'] for r in e['races']})
            if uses:
                note = f'<span class="fuse">required for {esc(", ".join(uses))}</span>'
            elif via:
                note = (f'<span class="fuse">not required by any unlock, but raised by quest '
                        f'steps used for {esc(", ".join(via))}</span>')
            else:
                note = '<span class="fuse dim">no unlock we track uses this</span>'
            out += f'<li class="{sign}"><b>{esc(f)}</b>{detail}{note}</li>'
        return out

    undone = ''.join(
        f'<li><b>{esc(e["name"])}</b> raises {esc(", ".join(e["factions"]))}'
        + (f' &mdash; used for {esc(", ".join(e["races"]))}' if e['races'] else '')
        + '</li>' for e in z.get('steps_undone', []))
    helped = ''.join(
        f'<li><b>{esc(e["name"])}</b> raises {esc(", ".join(e["factions"]))}'
        + (f' &mdash; used for {esc(", ".join(e["races"]))}' if e['races'] else '')
        + '</li>' for e in z.get('steps_helped', []))

    zone_cards += f'''
  <article class="fzone">
    <div class="fzhead">
      <h3>{esc(zone)}</h3>
      <span class="fzmeta">D{z.get("difficulty")} &middot; measured across {z["kills"]} kills
        &middot; {esc(z.get("date") or "")}</span>
    </div>
    <div class="fcols">
      <div><h4 class="fdown">Falls</h4><ul class="flist">{facline(z["falling"], "down")}</ul></div>
      <div><h4 class="fup">Rises</h4><ul class="flist">{facline(z["rising"], "up")}</ul></div>
    </div>
    {"<h4 class='fwarn'>Quest steps this undoes</h4><ul class='fsteps'>" + undone + "</ul>" if undone else ""}
    {"<h4 class='fgood'>Quest steps this helps</h4><ul class='fsteps'>" + helped + "</ul>" if helped else ""}
    {"<p class='fnothing'>Nothing here touches a race unlock we track, in either direction.</p>" if not undone and not helped else ""}
  </article>'''

page = head("Faction impact checker",
  "What grinding an EverQuest Legends zone does to your faction standing, and which race unlocks it "
  "helps or costs. Measured from our own combat logs rather than assumed.",
  rel="../") + bar("../") + f'''
<main>

<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp;
      <a href="index.html">Tools</a> &nbsp;/&nbsp; Faction impact</p>
    <h1 class="display">What tonight<br><em>costs you later.</em></h1>
    <p class="hero-lede">Faction moves while you are not looking. You clear a zone for six hours and
      find out afterwards that an unlock you had not started is now expensive, or that a vendor has
      stopped speaking to you. This checks that before you commit the evening.</p>
    <p class="hero-sig"><span>{len(index)} factions</span><span>{len(covered)} zone measured</span>
      <span>{len(steps)} quest steps</span><span>{len(races)} races</span></p>
  </div>
</section>

<div class="shell">
  <div class="note warn"><strong>Read the coverage before you trust a silence.</strong> The faction
    movement here is <em>measured from our own combat logs</em>, so it covers only zones we have
    actually played and counted: <strong>{esc(", ".join(covered)) or "none yet"}</strong>. Every other
    zone on this site is <strong>not measured</strong>, and this page will tell you so rather than
    return an empty result that looks like good news. What a faction is <em>for</em> &mdash; which
    races need it, which quest steps raise it &mdash; comes from the race unlock work and covers
    everything we hold. <strong>An absent zone means we have not looked, never that it is safe.</strong></div>
</div>

<section class="band" style="border-top:0;padding-top:0">
  <div class="shell">
    <div class="sechead"><span class="n">Search</span><div><h2 class="sec">Look up a faction</h2>
      <p class="lede" style="margin:0">Type any faction, race or zone. It answers what raises it, what
        needs it, and where we have seen it move.</p></div></div>
    <input id="q" class="fsearch" type="search" placeholder="Mayong Mistmoore, High Elf, Bat Wings&hellip;"
      autocomplete="off" aria-label="Search factions, races and quest steps">
    <div id="res" class="fres" aria-live="polite"></div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><span class="n">Measured</span><div><h2 class="sec">Zones we have counted</h2>
      <p class="lede" style="margin:0">Faction movement recorded from play, with the size per kill and
        the worst single mob. <span class="tier tM">TIER M</span></p></div></div>
    {zone_cards or "<p class='fnothing'>No zone measured yet.</p>"}
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><span class="n">Not measured</span><div><h2 class="sec">Where we cannot answer</h2></div></div>
    <div class="note"><strong>These zones have plates but no faction measurement:</strong>
      {esc(", ".join(uncovered)) or "none"}. Faction data for them would come from a combat log of an
      hour in the zone &mdash; the same way the measured zone above was produced. Until then this page
      has nothing to say about them, and says nothing rather than guessing.</div>
  </div>
</section>

</main>
<script>
const FAC = {json.dumps(index, separators=(",", ":"))};
const RACES = {json.dumps({k: v['name'] for k, v in races.items()}, separators=(",", ":"))};
const q = document.getElementById('q'), res = document.getElementById('res');
function esc(s){{return String(s).replace(/[&<>"]/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}})[c]);}}
function card(name, f){{
  let h = '<article class="fcard"><h3>' + esc(name) + '</h3>';
  if (f.needed_by.length) h += '<p class="fneed"><b>Needed for:</b> ' + f.needed_by.map(esc).join(', ') + '</p>';
  else h += '<p class="fneed dim">No race unlock we track requires this.</p>';
  if (f.raised_by.length) {{
    h += '<p class="fsub">Raised by</p><ul>';
    f.raised_by.forEach(r => {{ h += '<li>' + esc(r.step) + ' <span class="d">' + (r.delta>0?'+':'') + r.delta +
      (r.zone ? ' &middot; ' + esc(r.zone) : '') + '</span></li>'; }});
    h += '</ul>';
  }}
  if (f.moved_in.length) {{
    h += '<p class="fsub">Seen moving in play</p><ul>';
    f.moved_in.forEach(m => {{ h += '<li>' + esc(m.zone) + ' <span class="d">' + (m.per_kill>0?'+':'') + m.per_kill +
      ' a kill' + (m.biggest !== m.per_kill ? ', up to ' + (m.biggest>0?'+':'') + m.biggest + ' from ' + esc(m.mob) : '') +
      '</span></li>'; }});
    h += '</ul>';
  }} else {{
    h += '<p class="fsub dim">We have not measured this moving anywhere.</p>';
  }}
  return h + '</article>';
}}
function run(){{
  const t = q.value.trim().toLowerCase();
  if (t.length < 2) {{ res.innerHTML = ''; return; }}
  const hits = Object.keys(FAC).filter(k =>
    k.toLowerCase().includes(t) ||
    FAC[k].needed_by.some(r => r.toLowerCase().includes(t)) ||
    FAC[k].raised_by.some(r => (r.step + ' ' + (r.zone||'')).toLowerCase().includes(t)) ||
    FAC[k].moved_in.some(m => m.zone.toLowerCase().includes(t)));
  if (!hits.length) {{
    res.innerHTML = '<p class="fnothing">Nothing matches &ldquo;' + esc(q.value) +
      '&rdquo;. That means we hold no record of it &mdash; not that it has no effect.</p>';
    return;
  }}
  res.innerHTML = hits.sort().slice(0, 24).map(k => card(k, FAC[k])).join('');
}}
q.addEventListener('input', run);
</script>
''' + foot("../")

open('tools/faction-impact.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"tools/faction-impact.html written: {len(index)} factions, "
      f"{len(covered)} zone(s) measured, {len(uncovered)} not")
