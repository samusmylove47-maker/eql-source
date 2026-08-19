"""data/index.html — the human half of the public data contract.

The JSON at /data/index.json is what a machine reads. This is what a person
reads before deciding whether to depend on us, which is the actual decision
being asked of them.

It exists to answer four questions and nothing else: what is here, what may I
do with it, what will you promise not to break, and what is this data NOT good
for. The fourth is the one nobody else in this community answers, and it is the
reason to use ours.
"""
import os, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

IDX = json.load(open('public/data/index.json', encoding='utf-8'))
DS = IDX['datasets']

CSS = '''<style>
.dt .ds{border-top:1px solid var(--rule);padding:var(--s-5) 0}
.dt .ds:last-of-type{border-bottom:1px solid var(--rule)}
.dt .ds h3{font-family:"Saira Condensed",sans-serif;font-size:22px;font-weight:700;
  text-transform:uppercase;letter-spacing:.02em;margin:0;color:var(--bone)}
.dt .ds .u{font-family:"IBM Plex Mono",monospace;font-size:12.5px;margin:6px 0 0}
.dt .ds .u a{color:var(--instr);text-decoration:none;border-bottom:1px solid transparent}
.dt .ds .u a:hover{border-color:var(--instr)}
.dt .ds .m{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--faint);margin:5px 0 0}
.dt .ds p{margin:9px 0 0;color:var(--dim);font-size:14.5px;line-height:1.6;max-width:70ch}
.dt .ds ul{margin:9px 0 0;padding-left:18px;color:var(--faint);font-size:13.5px;line-height:1.6;max-width:72ch}
.dt pre{background:#10151A;border:1px solid var(--rule);border-radius:4px;padding:14px 16px;
  overflow-x:auto;font-family:"IBM Plex Mono",monospace;font-size:12.5px;color:var(--dim);
  line-height:1.6;margin:var(--s-5) 0 0}
.dt .promise{list-style:none;margin:var(--s-5) 0 0;padding:0;display:grid;gap:1px;
  background:var(--rule);border:1px solid var(--rule);border-radius:var(--r);overflow:hidden}
.dt .promise li{background:var(--panel);padding:13px 16px;color:var(--dim);font-size:14px;line-height:1.55}
</style>'''


def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


cards = ''.join(
    f'''<div class="ds">
      <h3>{esc(d['title'])}</h3>
      <p class="u"><a href="{esc(d['url'])}">{esc(d['url'])}</a></p>
      <p class="m">v{esc(d['version'])} &middot; {d['bytes']//1024} KB &middot; hash {esc(d['hash'])}</p>
      <p>{esc(d['description'])}</p>
    </div>''' for d in DS)

promises = ''.join(f'<li>{esc(s)}</li>' for s in IDX['stability'])

page = (head("Public data",
             "Versioned, per-claim-sourced EverQuest Legends data, free to "
             "consume. Plane of Sky quests with provenance, measured drop "
             "sources, surveyed zones and item IDs.",
             rel="../", extra=CSS, og="tools", canon="data/index")
        + bar("../") + f'''
<main id="main">
<section class="hero page">
  <div class="shell dt">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp; Public data</p>
    <h1 class="display">Take the data.<br><em>Please.</em></h1>
    <p class="hero-lede">Nobody in this community publishes machine-readable data, so every
      tool re-transcribes the same wiki pages and inherits the same 1999 errors doing it.
      Here is ours: {len(DS)} datasets, versioned, with a source recorded per claim. Free to
      use, no key, no rate limit, CORS open.</p>
    <p class="hero-sig"><span>{len(DS)} datasets</span>
      <span>{sum(d['bytes'] for d in DS)//1024} KB total</span>
      <span>no key required</span></p>
  </div>
</section>

<section class="band" style="border-top:0;padding-top:0">
  <div class="shell dt">
    <pre>curl {IDX['source']}/data/index.json</pre>

    <h2 class="sec">What is here</h2>
    {cards}

    <h2 class="sec">What we promise</h2>
    <ul class="promise">{promises}</ul>

    <h2 class="sec">What you may do with it</h2>
    <div class="note"><strong>{esc(IDX['terms']['summary'])}</strong>
      <br><br><strong>The measured data is ours.</strong> {esc(IDX['terms']['measured'])}
      <br><br><strong>The inherited data is not.</strong> {esc(IDX['terms']['inherited'])}
      <br><br><strong>No warranty.</strong> {esc(IDX['terms']['warranty'])}</div>

    <h2 class="sec">What this data is not good for</h2>
    <div class="note"><strong>Drop rates.</strong> The sightings file is a count of measured
      drops, and a drop seen once is seen once. There is no denominator in it and
      you cannot compute one. If you publish a percentage from this, you have invented it.
      <br><br><strong>Anything marked below tier 2.</strong> Every claim carries its tier.
      A tier 5 figure is inherited Project 1999 prose that nobody has checked against
      Legends, and roughly a third of what any reference in this space publishes is that.
      <a href="../learn/contamination.html">We scan ourselves for it</a> and publish what
      turns up. Read the provenance before you present a number as fact.
      <br><br><strong>Completeness.</strong> Thirteen zones of far more &mdash; ten dungeons and
      two of the planes &mdash; plus the Plane of Sky written up separately, and a limited sample
      of measured play behind it. Everything here states what it does not know; that is the most
      useful field in the file.</div>

    <h2 class="sec">If you build something with it</h2>
    <p style="color:var(--dim);font-size:15px;line-height:1.65;max-width:70ch;margin:var(--s-5) 0 0">
      Tell us and we will link it. If a field you need is missing, or a shape is awkward to
      consume, <a href="https://github.com/samusmylove47-maker/eql-source/issues/new">open an
      issue</a> &mdash; the point of publishing this is that it gets used, and a schema
      nobody can use is a press release.
      <br><br>And if you find something wrong in it, that is the most useful thing anyone
      can send us. Every finding is credited by name on <a href="../credits.html">the credits
      page</a>.</p>
  </div>
</section>
</main>
''' + foot("../"))

os.makedirs('public/data', exist_ok=True)
open('public/data/index.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"data/index.html written: {len(DS)} datasets, "
      f"{sum(d['bytes'] for d in DS)//1024} KB published")
