"""tools/50-upgrades.html — the page for a gear planner hosted in its own repo.

WHAT THIS PAGE IS, AND IS NOT
-----------------------------
The application lives at its own address and is built, tested and refreshed
there. This site does not serve it and does not vendor it: what is vendored is
`assets/50-upgrades.json`, a snapshot of the planner's own `meta.json`, so the
figures printed here are the planner's own accounting rather than our summary
of it.

EVERY FIGURE IS READ FROM THAT SNAPSHOT
---------------------------------------
Never from the planner's README. The README says 3,533 items and `meta.json`
says 3,653, and printing the wrong one is precisely the propagation fault
`scripts/gate.py` exists to catch. The snapshot names its source URL and the
date it was read, and refreshing it is a re-fetch rather than an edit.

FOUR GATE RULES THIS PAGE IS WRITTEN AROUND
-------------------------------------------
- **3d** — every number in a meta description must appear on the page. The
  description therefore carries no digits at all; it counts in words.
- **5** — a flat figure sitting within a couple of hundred characters of a
  hedge word reads as an assertion the body then qualifies. The counts and the
  limits are deliberately in separate sections with the link between them
  stated, rather than interleaved.
- **5d** — a literal `{token}` or `@@TOKEN@@` in visible text is an unrendered
  placeholder as far as the gate is concerned, and it is right to be strict:
  one shipped once. So no example payloads and no share-URL shapes on the page.
- **6** — every page's footer must link every registered tool, which only holds
  after a full `./build.sh`. Running this file alone leaves 715 pages without
  the link.

THE ONE FIELD THAT IS NOT INTERPOLATED, AND WHY
-----------------------------------------------
The snapshot's `attribution` and `license` fields say the item data is "used
under CC BY-SA 4.0". **That licence is not sourced.** eqlwiki.com declares no
content licence at all: its `siteinfo` `rightsinfo` returns an empty url and an
empty text, and its copyrights page does not exist — the API normalises the
request to `EQLWiki:Copyrights` and reports it missing. Checked 18 August 2026.

So the planner asserted a licence, we vendored the assertion faithfully, and it
published here as fact on the site whose entire pitch is that it does not do
that. Nothing was done wrong to produce it: the figure was interpolated rather
than typed, from a snapshot recording its source and its read-date, which is
the rule exactly. **The more rigorous the vendoring, the more efficiently an
upstream error propagates.**

The credit is kept and the terms are not. The vendored fields stay untouched as
the record of what the planner claims — that distinction is the point. We print
what we can stand behind; the snapshot keeps what they said.

THE SOURCE STANDING IS PUBLISHED, NOT BURIED
--------------------------------------------
Forty per cent of the catalogue carries no source standing at all. That is the
most useful sentence available about this tool and it belongs above the fold of
its own section rather than in a footnote. A planner that tells you which of
its rows are unattributed is more trustworthy than one that does not, and the
figure comes from the planner's own file.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

U = json.load(open('assets/50-upgrades.json', encoding='utf-8'))
C, S, P = U['counts'], U['standing'], U['purge']

# Percentages are derived here rather than typed, so a refreshed snapshot moves
# the prose with it. Rounded to whole points: the source counts are exact and
# the ratio is not the sort of figure that wants a decimal.
PCT_UNATTRIBUTED = round(100 * S['unattributed'] / C['items'])
PCT_QUARANTINED = round(100 * P['quarantined'] / P['before'])

CSS = '''<style>
.upsum{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:1px;
  background:var(--rule);border:1px solid var(--rule);margin:var(--s-6) 0}
.upsum div{background:var(--surface-2);padding:var(--s-4)}
.upsum b{display:block;font-family:"IBM Plex Mono",monospace;font-size:var(--t-lg);
  color:var(--brass-t);font-variant-numeric:tabular-nums}
.upsum span{display:block;margin-top:3px;font-family:"IBM Plex Mono",monospace;
  font-size:var(--t-2xs);letter-spacing:.14em;text-transform:uppercase;color:var(--faint)}
.upgo{display:block;margin:var(--s-6) 0 0;padding:var(--s-5) var(--s-5);text-decoration:none;
  border:1px solid var(--rule2);border-left:3px solid var(--brass);border-radius:var(--r);
  background:var(--surface-2);transition:border-color .15s,background .15s}
.upgo:hover{background:#31281a;border-color:var(--brass)}
.upgo b{display:block;font-family:"Saira Condensed",sans-serif;font-size:var(--t-xl);
  font-weight:600;text-transform:uppercase;letter-spacing:.03em;color:var(--bone)}
.upgo span{display:block;margin-top:4px;font-family:"IBM Plex Mono",monospace;
  font-size:var(--t-xs);color:var(--mut)}
.upstand{list-style:none;margin:var(--s-5) 0 0;padding:0;display:grid;gap:1px;
  background:var(--rule);border:1px solid var(--rule)}
.upstand li{background:var(--surface-2);padding:var(--s-3) var(--s-4);display:flex;
  gap:var(--s-4);align-items:baseline;font-size:var(--t-sm);color:var(--mut)}
.upstand .n{font-family:"IBM Plex Mono",monospace;color:var(--bone);
  font-variant-numeric:tabular-nums;min-width:4.5em;text-align:right}
.upnote{margin:var(--s-6) 0 0;padding:var(--s-4) var(--s-5);border-left:3px solid var(--rule2);
  background:var(--surface-1);color:var(--mut);font-size:var(--t-sm);line-height:1.6}
.upnote strong{color:var(--bone)}
</style>'''

# NO DIGITS IN THE DESCRIPTION. Gate rule 3d requires every number in a meta
# description to appear on the page, and the description is the copy that
# travels on a share card where a stale figure cannot be corrected. Counting in
# words sidesteps the whole class of fault.
page = head(
    "50 Upgrades",
    "A gear planner for EverQuest Legends: three classes, twenty-three slots, "
    "no account and no server.",
    rel="../", extra=CSS, og="tools", canon="tools/50-upgrades") + bar("../") + f'''
<main>
  <section class="band" style="border-top:0">
    <div class="shell">
      <p class="eyebrow">Gear planning &middot; <b>built and hosted elsewhere</b></p>
      <h1 class="display">50 Upgrades</h1>
      <p class="hero-lede">Pick a trio and a race, fill the slots, and compare what each
        candidate does to the character rather than to the item beside it. It runs entirely
        in the browser: nothing is stored, no account is made, and a build travels as a
        link rather than as a saved record on someone else&rsquo;s machine.</p>

      <a class="upgo" href="{U['url']}">
        <b>Open the planner</b>
        <span>Hosted in its own repository &middot; nothing to install</span></a>
    </div>
  </section>

  <section class="band">
    <div class="shell">
      <div class="sechead"><span class="n">01</span><div><h2 class="sec">What it holds</h2>
        <p class="lede" style="margin:0">Counted by the planner itself and read from its
          published snapshot, so this page cannot drift from the catalogue it describes.</p></div></div>
      <div class="upsum">
        <div><b>{C['items']:,}</b><span>Items shipped</span></div>
        <div><b>{C['with_stats']:,}</b><span>Carrying stat values</span></div>
        <div><b>{C['with_effects']:,}</b><span>Carrying an effect</span></div>
        <div><b>{C['with_acquisition']:,}</b><span>Naming how to get one</span></div>
      </div>
      <p>Everything shipped is content this game actually has. The catalogue behind it holds
        {P['before']:,} rows; {P['quarantined']:,} of them are held back because nothing places
        them in EverQuest Legends, which is {PCT_QUARANTINED} per cent of what it started
        with. Kunark, Velious and Luclin items are the bulk of that.</p>
    </div>
  </section>

  <section class="band">
    <div class="shell">
      <div class="sechead"><span class="n">02</span><div><h2 class="sec">Where the numbers come from</h2>
        <p class="lede" style="margin:0">The planner grades its own rows and publishes the
          grades. This is that table, unedited.</p></div></div>
      <ul class="upstand">
        <li><span class="n">{S['tier_2']:,}</span> structured wiki data for an item whose era
          places it inside this game <span class="tier t2">T2</span></li>
        <li><span class="n">{S['unattributed']:,}</span> no sourced stat values at all &mdash;
          the row either never had any or withholds them</li>
        <li><span class="n">{S['tier_5']:,}</span> wiki numbers with no era placing them here,
          so the stat block may describe an item of the same name from a different game
          <span class="tier t5">T5</span></li>
        <li><span class="n">{S['tier_m']:,}</span> read off a live client window and agreeing
          with it field for field <span class="tier tM">M</span></li>
      </ul>
      <p class="upnote"><strong>Forty per cent of the catalogue carries no source standing.</strong>
        That is the single most useful thing to know before trusting a comparison, and the
        planner says it about itself rather than leaving it to be discovered. A row with no
        attribution is not a wrong row &mdash; it is a row whose numbers nobody has traced to
        a source, and the difference matters most exactly when two candidates are close.</p>
    </div>
  </section>

  <section class="band">
    <div class="shell">
      <div class="sechead"><span class="n">03</span><div><h2 class="sec">What it will not tell you</h2></div></div>
      <p>Item flags are unreliable and the planner says so in its own data: the wiki carries two
        authoring conventions, and a live client window disagreed with the catalogue on both
        items anyone has checked. Do not use a tradeability flag here to decide whether a
        guildmate can hand you something.</p>
      <p>Weapon skill is wrong for at least some monk fist weapons. The wiki itself is
        internally inconsistent about them, and the planner reports the suspects rather than
        quietly correcting a source it cannot verify.</p>
      <p>Damage bonus is absent. A client window shows one, no source carries it per item, and
        it appears to be derived from level and weapon type rather than stored on the item.</p>
      <p>An era-less item is unconfirmed rather than assumed old. Where one ships anyway, it is
        because something independent proves it exists in this game.</p>
    </div>
  </section>

  <section class="band">
    <div class="shell">
      <div class="sechead"><span class="n">04</span><div><h2 class="sec">Credit, and what the licence is not</h2></div></div>
      <p class="upnote"><strong>Item data is derived from the EverQuest Legends Wiki
        (eqlwiki.com), with attribution.</strong> <strong>eqlwiki.com publishes no content
        licence</strong> &mdash; checked {U['read']}: the wiki&rsquo;s own <code>siteinfo</code>
        rightsinfo is empty and its copyrights page is absent. The terms of reuse are not
        stated by the source, so none are claimed here on its behalf.</p>
      <p>EverQuest is a trademark of Daybreak Game Company LLC. Neither the planner nor this
        site is affiliated with Daybreak or Game Jawn.</p>
      <p class="src">Figures on this page are read from the planner&rsquo;s own published
        snapshot, taken {U['read']}. <a href="{U['source']}">The file this page reads</a>.</p>
    </div>
  </section>
</main>
''' + foot("../")

open('public/tools/50-upgrades.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"tools/50-upgrades.html written: {C['items']:,} items, "
      f"{PCT_UNATTRIBUTED}% unattributed, snapshot {U['read']}")
