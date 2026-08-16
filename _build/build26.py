"""learn/contamination.html — what our own pages look like under the scanner.

WHY THIS PAGE EXISTS AND WHY IT IS ABOUT US
-------------------------------------------
Every EverQuest Legends reference is part Project 1999 text describing a game
that stopped existing in 2001. This site's whole claim is that it can tell the
difference. On 14 August 2026 an outside audit found six classic haste figures
sitting inside our own *verified* tier, which is the strongest argument
available that the claim needed a tool behind it rather than a habit.

So there is a scanner, and it is pointed here. **A scanner that only finds
other people's contamination is an attack ad, not an audit**, and the ordering
is the entire point: this publishes what it finds about eqlsource, and if it is
ever pointed outward it comes here first and the results go up either way.

WHAT THE NUMBERS MEAN
---------------------
The page is careful not to read as "we found 291 errors". A hit is a question.
Legends kept a great deal of classic EverQuest intact and most of these
patterns are probably fine. The distinction that matters is marked against
unmarked, and it is stated in those terms throughout.
"""
import os, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

try:
    C = json.load(open('assets/contamination.json', encoding='utf-8'))
except (OSError, ValueError):
    print('learn/contamination.html: no assets/contamination.json, skipped')
    raise SystemExit(0)

SIGS = C['signatures']
CHANGED = [s for s in SIGS if s['certainty'] == 'changed']
CONV = [s for s in SIGS if s['certainty'] == 'convention']
act_u = sum(s['unmarked'] for s in CHANGED)
act_m = sum(s['marked'] for s in CHANGED)
conv_u = sum(s['unmarked'] for s in CONV)
conv_m = sum(s['marked'] for s in CONV)

CSS = '''<style>
.cn table{border-collapse:collapse;width:100%;font-size:14px;margin:var(--s-5) 0 0}
.cn th{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--faint);text-align:left;padding:9px 10px;
  border-bottom:1px solid var(--rule2);white-space:nowrap}
.cn td{padding:10px;border-bottom:1px solid var(--rule);vertical-align:top}
.cn tr:last-child td{border-bottom:0}
.cn .sig{font-family:"IBM Plex Mono",monospace;font-size:12.5px;color:var(--bone);white-space:nowrap}
.cn .n{font-family:"IBM Plex Mono",monospace;font-size:15px;text-align:right;white-space:nowrap}
.cn .n.bad{color:var(--warn-t,#E0A56B)}
.cn .n.ok{color:var(--faint)}
.cn .what{color:var(--dim);font-size:13.5px;line-height:1.5}
.cn .what b{color:var(--bone)}
.cn .tw{overflow-x:auto}
.cn .score{display:flex;flex-wrap:wrap;gap:1px;background:var(--rule);
  border:1px solid var(--rule);border-radius:var(--r);overflow:hidden;margin:var(--s-6) 0 0}
.cn .score div{background:var(--panel);padding:15px 20px;flex:1 1 150px}
.cn .score b{display:block;font-family:"Saira Condensed",sans-serif;font-size:30px;
  font-weight:700;color:var(--bone);line-height:1}
.cn .score b.good{color:var(--ok)}
.cn .score span{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--faint);display:block;margin-top:6px}
</style>'''


def rows(sigs):
    out = []
    for s in sigs:
        files = ', '.join(os.path.basename(p) for p in list(s['files'])[:3])
        out.append(
            f'<tr><td class="sig">{s["id"]}</td>'
            f'<td class="n {"bad" if s["unmarked"] else "ok"}">{s["unmarked"]}</td>'
            f'<td class="n ok">{s["marked"]}</td>'
            f'<td class="what"><b>Classic:</b> {s["classic"]}<br>'
            f'<b>Legends:</b> {s["legends"]}<br>'
            f'<b>What would settle it:</b> {s["settle"]}'
            f'<br><span style="color:var(--faint)">Found in: {files}</span></td></tr>')
    return ''.join(out)


page = (head("What the scanner finds here",
             "We scan our own pages for Project 1999 conventions and publish "
             "what turns up. Percentage haste, classic charge counts and "
             "classic resist blocks, counted, with what would settle each one.",
             rel="../", extra=CSS, og="tools", canon="learn/contamination")
        + bar("../") + f'''
<main>
<section class="hero page">
  <div class="shell cn">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp;
      <a href="index.html">Learn</a> &nbsp;/&nbsp; Contamination</p>
    <h1 class="display">What the scanner<br><em>finds here.</em></h1>
    <p class="hero-lede">Every EverQuest Legends reference is part Project 1999 text
      describing a game that stopped existing in 2001, and this one is no exception. So we
      built a scanner for it and pointed it at ourselves. <strong>This is what it finds on
      eqlsource</strong> &mdash; not on anybody else.</p>
    <div class="score">
      <div><b class="{'good' if act_u == 0 else ''}">{act_u}</b>
        <span>unmarked, on mechanics we know changed</span></div>
      <div><b>{act_m}</b><span>of those, marked</span></div>
      <div><b>{conv_u + conv_m}</b><span>classic formats, mostly harmless</span></div>
      <div><b>{C['scanned']}</b><span>files scanned</span></div>
    </div>
  </div>
</section>

<section class="band" style="border-top:0;padding-top:0">
  <div class="shell cn">
    <div class="note"><strong>A hit is a question, not a verdict.</strong> Legends kept a
      great deal of classic EverQuest intact, and most of these patterns are probably
      current. What a hit means is: <em>this figure carries a convention from a game whose
      numbers we know changed, and nobody has checked this one.</em>
      <br><br><strong>The number that matters is the first one.</strong> A classic figure
      carrying a badge is doing its job &mdash; it tells you where it came from and how far
      to trust it. The same figure printed bare is the fault this site exists to prevent.</div>

    <h2 class="sec">Mechanics we know changed</h2>
    <p class="lede">A hit here is probably a wrong number, because the mechanic it describes
      demonstrably works differently in Legends.</p>
    <div class="tw"><table>
      <thead><tr><th>Signature</th><th>Unmarked</th><th>Marked</th><th>What it is</th></tr></thead>
      <tbody>{rows(CHANGED)}</tbody>
    </table></div>

    <h2 class="sec">Classic formats</h2>
    <p class="lede">These are conventions rather than errors. They are usually harmless and
      often still current. They are counted because in aggregate they measure how much of a
      page was transcribed from a classic-era record, which is worth knowing even when every
      number in it is right.</p>
    <div class="tw"><table>
      <thead><tr><th>Signature</th><th>Unmarked</th><th>Marked</th><th>What it is</th></tr></thead>
      <tbody>{rows(CONV)}</tbody>
    </table></div>

    <div class="note"><strong>Why this page is about us and not about anyone else.</strong>
      Four other sites in this community publish EverQuest Legends data and every one of them
      carries inherited classic text, exactly as we do. We are not going to publish a league
      table of other people&rsquo;s contamination. <strong>A scanner that only finds someone
      else&rsquo;s rot is an attack ad</strong>, and the only version of this worth having is
      the one that runs here first and publishes the result whatever it says.
      <br><br>The six haste figures that started this were found by
      <a href="../sources.html#changelog">an outside audit</a>, not by us. That is the
      argument for owning a tool rather than a habit.</div>

    <p class="src">Run by hand with <code>scripts/contamination.py</code> over
      {C['scanned']} files: every survey and tool source, the Plane of Sky dataset, the
      planar sets, the mined catalogue and the mote values. The retired plate archive is
      excluded deliberately &mdash; it republishes superseded coordinates verbatim, is
      marked as history and is kept out of search.</p>
  </div>
</section>
</main>
''' + foot("../"))

os.makedirs('public/learn', exist_ok=True)
open('public/learn/contamination.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"learn/contamination.html written: {act_u} unmarked on changed mechanics, "
      f"{conv_u + conv_m} format hits across {C['scanned']} files")
