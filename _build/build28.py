"""tools/sky-ledger.html — the page for the tool that replaced our own.

WHY THIS PAGE EXISTS AND THE OLD TRACKER DOES NOT
-------------------------------------------------
Our Plane of Sky tracker asked you to tick boxes. Sky Ledger reads your combat
log while you play and works the same thing out from it — and it does one thing
ours could not do at all: **a turn-in piece can only be spent once.** Ours
counted a held item against every test that wants it, so one Djinni War Blade
made two quests read as ready when it can only ever finish one. That is not a
nicer skin on what we published; it is a correctness property we lacked.

Two Sky trackers on one site is the "which do I use" question, and after that
the older one is the wrong answer. tools/plane-of-sky.html is withdrawn.

EVERY FIGURE ON THIS PAGE IS READ, NOT TYPED
--------------------------------------------
The dataset counts come out of assets/sky-ledger.json, which _build/skyledger.py
writes by counting the Ledger's own sky.json. See that file for why: the tool's
README carries "does not make three quests ready" about an item the dataset
wants twice, which is the same fault in miniature.

Nothing here describes how the tool feels to use. Nobody on this site has driven
it against a live log yet, and a drawing — or an adjective — is an assertion.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

SL = json.load(open('assets/sky-ledger.json', encoding='utf-8'))
APP, DS = SL['app'], SL['dataset']
REL = SL.get('release') or {}
OV = REL.get('overlay') or {}
# The two screenshots and the trailer poster, hashed by _build/media.py. Absent
# on a machine that has never run it, so the shots degrade to nothing rather
# than to a broken image.
try:
    MEDIA = json.load(open('assets/media.json', encoding='utf-8'))
except (OSError, ValueError):
    MEDIA = {}


def shot(stem, alt, cap):
    m = MEDIA.get(stem)
    if not m:
        return ''
    # width/height are required, not decorative: without them the box is 2px
    # tall before the bytes arrive, `loading="lazy"` never sees it enter the
    # viewport, and the browser never requests the image at all.
    dim = f' width="{m["w"]}" height="{m["h"]}"' if m.get('w') else ''
    return (f'<figure class="slshot"><img src="../assets/media/{m["file"]}" alt="{alt}"'
            f'{dim} loading="lazy" decoding="async">'
            f'<figcaption>{cap}</figcaption></figure>')


SHOTS = ''
if MEDIA.get('sky-ledger-ready') or MEDIA.get('sky-ledger-setup'):
    SHOTS = ('<div class="slshots">'
             + shot('sky-ledger-ready',
                    'The overlay listing seven ready quests, each showing only the items to hand over',
                    'Ready quests. Under each tester, the pieces to hand them &mdash; nothing else, '
                    'because that is the question you have standing at the NPC.')
             + shot('sky-ledger-setup',
                    'The setup panel: whose kills count, the class picker, and what to track',
                    'Setup. The number on each class is how many tests it owes.')
             + '</div>')
HREF = f"../app/{APP['file']}"
# A version we could not read is not a version. Printing "vNone" beside three
# real figures is the kind of small lie that makes a reader distrust the rest.
VER = f'<span>v{SL["version"]}</span>' if SL.get('version') else ''

# The two doors, or an honest sentence where no release exists. Sizes are read
# off the packages by skyledger.py; a button that lies about a 100 MB download
# is worse than no button.
def _downloads():
    ov, br = REL.get('overlay') or {}, REL.get('browser') or {}
    if not ov.get('url'):
        return ('<div class="note warn"><strong>No release is published yet.</strong> '
                'The browser build above is the whole application apart from '
                'click-through and real transparency.</div>')
    return (
        '<p class="dlrow">'
        f'<a class="dl" href="{ov["url"]}"><b>Download the overlay</b>'
        f'<span>Windows &middot; {ov.get("mb", "?")} MB &middot; unzip and run, no installer</span></a>'
        f'<a class="dl alt" href="{br.get("url", REL.get("page", "#"))}"><b>Or the single file</b>'
        f'<span>One HTML page &middot; {br.get("mb", "?")} MB &middot; opens in any browser</span></a>'
        '</p>')


DOWNLOADS = _downloads()


CSS = '''<style>
.dlrow{display:flex;flex-wrap:wrap;gap:12px;margin:20px 0 10px;max-width:none}
.dl{flex:1 1 260px;display:block;padding:15px 17px;text-decoration:none;
  border:1px solid var(--rule2);border-left:3px solid var(--brass);
  background:var(--surface-2);border-radius:4px;transition:border-color .15s,background .15s}
.dl:hover{background:var(--surface-2);border-color:var(--brass)}
.dl b{display:block;font-family:"Saira Condensed",sans-serif;font-size:19px;font-weight:600;
  text-transform:uppercase;letter-spacing:.03em;color:var(--bone)}
.dl span{display:block;margin-top:3px;font-family:"IBM Plex Mono",monospace;
  font-size:11.5px;color:var(--mut);letter-spacing:.02em}
.dl.alt{border-left-color:var(--instr-t)}
.dl.alt:hover{border-color:var(--instr-t)}

/* Two doors, and they are not equals: one runs the thing, one explains it. */
.slrun{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,290px),1fr));
  gap:var(--s-4);margin:var(--s-6) 0 0}
.slrun>a,.slrun>div{display:block;background:var(--surface-1);border:1px solid var(--rule2);
  border-radius:var(--r);padding:var(--s-5) var(--s-5) var(--s-4);text-decoration:none;
  border-top:3px solid var(--c,var(--instr))}
.slrun a:hover{background:var(--surface-2);border-color:var(--instr-t)}
.slrun h2{font-family:"Saira Condensed",sans-serif;font-weight:700;font-size:var(--t-xl);
  text-transform:uppercase;letter-spacing:.015em;color:var(--bone);margin:0 0 6px}
.slrun p{margin:0;color:var(--mut);font-size:var(--t-base);line-height:1.55}
.slrun .m{font-family:"IBM Plex Mono",monospace;font-size:var(--t-2xs);letter-spacing:.13em;
  text-transform:uppercase;color:var(--faint);margin:10px 0 0}
.slrun .go{display:block;margin-top:12px;font-family:"IBM Plex Mono",monospace;
  font-size:var(--t-xs);letter-spacing:.1em;text-transform:uppercase;color:var(--instr-t)}

/* The claims. Big mono figure, small caption — the numbers ARE the argument. */
.slfacts{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,215px),1fr));
  gap:1px;background:var(--rule);border:1px solid var(--rule);border-radius:var(--r);
  overflow:hidden;margin:var(--s-5) 0 0}
.slfacts div{background:var(--surface-1);padding:var(--s-4) 18px}
.slfacts b{display:block;font-family:"IBM Plex Mono",monospace;font-size:var(--t-2xl);
  font-weight:600;color:var(--bone);line-height:1.15}
.slfacts span{display:block;font-family:"IBM Plex Mono",monospace;font-size:var(--t-2xs);
  letter-spacing:.13em;text-transform:uppercase;color:var(--faint);margin-top:7px}
.slfacts em{display:block;font-style:normal;color:var(--mut);font-size:var(--t-sm);
  line-height:1.5;margin-top:9px}

/* The honest-limits list. One row per thing the tool refuses to guess at. */
.sllim{list-style:none;margin:var(--s-5) 0 0;padding:0;display:grid;gap:1px;
  background:var(--rule);border:1px solid var(--rule);border-radius:var(--r);overflow:hidden}
.sllim li{background:var(--surface-1);padding:14px 18px;color:var(--mut);
  font-size:var(--t-base);line-height:1.6}
.sllim b{color:var(--bone)}
.sllim code{font-family:"IBM Plex Mono",monospace;font-size:.92em;color:var(--txt)}

.slkeys{width:100%;border-collapse:collapse;font-size:var(--t-sm);margin:var(--s-4) 0 0}
.slkeys td{border-bottom:1px solid var(--rule);padding:9px var(--s-4) 9px 0;color:var(--mut)}
.slkeys td:first-child{font-family:"IBM Plex Mono",monospace;color:var(--instr-t);
  white-space:nowrap;width:1%}
</style>'''

facts = f'''<div class="slfacts">
  <div><b>{DS['contested']} of {DS['items']}</b><span>Turn-in items wanted twice or more</span>
    <em>One held piece finishes one test. Every other tracker, ours included,
      counted it against all of them.</em></div>
  <div><b>&lt;28% &middot; 0/9</b><span>How a dry streak prints</span>
    <em>Never <code>0%</code>. Nine kills with no drop bounds the rate; it does not
      measure it, and <code>0%</code> would tell you to stop farming.</em></div>
  <div><b>Counted &middot; discarded</b><span>Two figures, never merged</span>
    <em>Kills it cannot place print as their own number rather than folding
      quietly into the total.</em></div>
</div>'''

page = head("Sky Ledger",
    # Read, like the body twelve lines down. This said 95 while the body said
    # {DS['quests']}, in the file whose own docstring forbids exactly that -
    # and gate rule 5 cannot see it, because it only fires where metadata
    # asserts what the body hedges, not where the two carry one quantity from
    # two origins. A share card is the copy that travels off-site.
    f"Sky Ledger reads your EverQuest Legends combat log and says which of the "
    f"{DS['quests']} Plane of Sky class-unlock tests you can hand in now. Runs "
    f"in a browser with no install, or as an overlay on the game.",
    rel="../", extra=CSS, og="tools", canon="tools/sky-ledger") + bar("../") + f'''
<main>

<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="../">EQL Source</a> &nbsp;/&nbsp;
      <a href="./">Tools</a> &nbsp;/&nbsp; Sky Ledger</p>
    <h1 class="display">Sky Ledger.</h1>
    <p class="hero-lede">It reads your own combat log and works out which of the
      {DS['quests']} Plane of Sky class-unlock tests you can hand in right now, and what the
      missing pieces drop from. Run it in a browser with nothing to install, or as an
      overlay on top of the game. <strong>Nothing is uploaded</strong> &mdash; there is no
      server to upload to.</p>
    <p class="hero-sig"><span>{DS['quests']} tests</span><span>{DS['turnin_slots']} turn-in slots</span><span>{DS['classes']} classes</span>{VER}</p>
  </div>
</section>

<div class="shell">

  <section class="band" style="border-top:0;padding-top:0">
    <div class="slrun">
      <a href="{HREF}" style="--c:var(--instr)">
        <h2>Run it in your browser</h2>
        <p>One file, {APP['kb']} KB, served from this site. Chrome or Edge on desktop can
          follow your log file live; Firefox and Safari cannot, so drop the log on
          the panel for a one-off read.</p>
        <p class="m">Build {APP['hash']} &middot; nothing installed &middot; your log never leaves this machine</p>
        <span class="go">Open the app &rarr;</span>
      </a>
      <a href="{OV.get('url', '#overlay')}" style="--c:var(--brass)">
        <h2>Put it over the game</h2>
        <p>The browser build cannot pass clicks through to the game and can only fake
          transparency. The Electron shell fixes both, with two global hotkeys and a
          continuous opacity slider.</p>
        <p class="m">Windows &middot; portable &middot; {OV.get('mb', '?')} MB &middot; unzip and run</p>
        <span class="go">Download the overlay &rarr;</span>
      </a>
    </div>
  </section>

  <section class="band">
    <div class="sechead"><span class="n">01</span><div><h2 class="sec">A piece can only be spent once</h2>
      <p class="lede" style="margin:0">This is the whole reason it is promoted here, and it is
        a correctness property rather than a feature.</p></div></div>
    <p class="lede"><strong>{DS['contested']} of the {DS['items']} turn-in items are wanted by more than one
      test</strong>, and all {DS['runes']} wind runes are among them &mdash; one of them is asked for by
      {DS['most_contested_tests']} separate tests. Hold one and exactly one test can be completed with it.
      Sky Ledger pools what you hold, spends each unit on the test closest to completion, and
      marks the contested pieces with how short you are.</p>
    <p class="lede"><strong>Every other tracker counts that item against every test that wants
      it</strong>, and tells you several quests are ready when one is. Ours did. That is what a
      checklist does when it has no idea what else is on the list, and it is not fixable by
      ticking more carefully.</p>
    {facts}
  </section>

  <section class="band">
    <div class="sechead"><span class="n">02</span><div><h2 class="sec">It holds this site's standard on its own</h2>
      <p class="lede" style="margin:0">Arrived at separately, by the same person, which is worth
        saying plainly rather than presenting as a coincidence.</p></div></div>
    <ul class="sllim">
      <li><b>It refuses to publish a drop rate it cannot measure.</b> No site publishes
        community drop rates for Sky, so it does not print one. It prints what your log has
        seen: drops over kills of that mob, with the sample size attached.</li>
      <li><b>A dry streak is a ceiling, not a zero.</b> Nine kills with no drop reads
        <code>&lt;28% &middot; 0/9</code>. Zero successes in nine trials bounds the rate and does
        not measure it &mdash; the same reasoning as the <code>damage_is_floor</code> marker on
        the raid figures here.</li>
      <li><b>It reports what it threw away.</b> Kills it could not place, bag sales whose
        contents the client never named, trades it would not guess at. The tally it discarded
        prints beside the tally it kept. The strip hides itself when there is nothing to
        admit.</li>
      <li><b>Its parsing is checked against the client's own string table.</b>
        <code>You have slain %1!</code> is id 12113 in <code>eqstr_us.txt</code>, read out of the
        install &mdash; the same class of evidence as our floor plans being read out of the
        <code>.s3d</code> meshes rather than drawn by hand.</li>
      <li><b>It understands Legends instancing.</b> A zone arrives as
        <code>The Plane of Sky 3 (Fused)</code>. That <code>&lt;n&gt; (&lt;Tier&gt;)</code> suffix
        is not in any client string file and classic EverQuest never had it, so an exact match
        against a zone name could never see it.</li>
      <li><b><code>X died.</code> names no killer, so it is never counted as yours.</b> Those
        lines are reported rather than guessed at.</li>
    </ul>
  </section>

  <section class="band">
    <div class="sechead"><span class="n">03</span><div><h2 class="sec">What it will not tell you</h2>
      <p class="lede" style="margin:0">Its own limits, in our type. They are limits of the log,
        mostly, and none of them are fixable by trying harder.</p></div></div>
    <ul class="sllim">
      <li><b>The log only knows what happened while it was running.</b> Anything looted before
        <code>/log on</code> is invisible. An <code>/outputfile inventory</code> dump at a banker
        covers that; the tool takes the larger of the two counts rather than adding them, so one
        item never reads as two.</li>
      <li><b>Wind runes can never have a measured rate.</b> They drop zone-wide from anything and
        they are alternate currency, so no log can count them. They are entered by hand and
        labelled as such.</li>
      <li><b>A sold bag is a hole the log cannot fill.</b>
        <code>You receive &hellip; for the contents of your bag.</code> never names what was
        inside, so those items may still read as held. The tool says so rather than pretending
        otherwise.</li>
      <li><b>A closed trade is not proof of a turn-in.</b> Walk the wrong class's pieces to the
        wrong giver and they come straight back, one refusal per item, and the trade still
        closes. Refusals only count when the line names your character.</li>
      <li><b>Five classes carry a <code>?</code>.</b> Ranger, Rogue, Shadow Knight, Shaman and
        Wizard have no confirmed Legends-era reward stat blocks. Their turn-ins are current; the
        stat numbers may still be classic. <a href="../sources#gaps">The same gap is open
        here</a>, because the data came from us.</li>
      <li><b>Two items have sources that disagree.</b> The Efreeti Great Staff and the Efreeti
        Statuette are attributed differently by us and by eqlegendstools. Both are marked in the
        panel rather than silently resolved.</li>
    </ul>
  </section>

  <section class="band" id="overlay">
    <div class="sechead"><span class="n">04</span><div><h2 class="sec">The overlay</h2>
      <p class="lede" style="margin:0">The same application in an Electron shell, so it can sit on
        top of the game instead of beside it.</p></div></div>
    <p class="lede">Both hotkeys are global, so they work while the game has focus. Position,
      size, opacity and click-through are remembered between runs. Exclusive fullscreen draws
      over every other window, this one included &mdash; use Windowed or Borderless.</p>
    <p class="lede"><a href="https://youtu.be/gmH4wm6pHz8">Watch it run, 18 seconds &rarr;</a>
      &nbsp;&middot;&nbsp;
      <a href="https://youtu.be/hxq2qY1FXtg">The full tutorial, 1:15 &rarr;</a></p>
    {SHOTS}
    <table class="slkeys">
      <tr><td>Ctrl+Shift+O</td><td>show and hide the panel</td></tr>
      <tr><td>Ctrl+Shift+L</td><td>click-through &mdash; the panel stops eating clicks</td></tr>
      <tr><td>slider</td><td>opacity, continuous from 15% to 100% rather than fixed steps</td></tr>
    </table>
    {DOWNLOADS}
    <p class="cm">Both carry build {APP['hash']}, the same one served above. Exclusive fullscreen
      draws over every window including this one &mdash; use Windowed or Borderless.</p>
  </section>

  <section class="band">
    <div class="sechead"><span class="n">05</span><div><h2 class="sec">Who made it, and what it replaced</h2></div></div>
    <div class="note sig"><strong>Sky Ledger is a separate project</strong>, with its own test
      suite and its own documentation. It is served here rather than rebuilt here.</div>
    <div class="note"><strong>Our own Plane of Sky tracker is withdrawn.</strong> It is the tool
      Sky Ledger supersedes, and running both would only ask a reader to pick. Its quest data
      lives on: <a href="../data/">the Sky dataset is published</a> with a source
      recorded per claim, and Sky Ledger&rsquo;s own dataset was extracted from it. The zone
      itself is written up at <a href="../raids/plane-of-sky">Plane of Sky, island by
      island</a>.</div>
    <div class="note"><strong>Credit where the parsing came from.</strong> The log-line cases that
      break naive counting &mdash; the autosell tail, combine consumption, upgrade-tier suffixes,
      and handbacks that name the player &mdash; were identified by <b>sowoky</b> in
      eqltools.com&rsquo;s <code>sky-core</code>, and reimplemented rather than copied. Two of
      them appear in no client string file at all, so they could only ever have been found by
      reading a real log. Quest data was cross-checked against
      eqlegendstools.com and loadoutlegends.com, which agree
      independently at {DS['quests']} tests, {DS['turnin_slots']} turn-in slots and {DS['items']} unique turn-in items.</div>
  </section>

</div>
</main>
''' + foot("../")

open('public/tools/sky-ledger.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"tools/sky-ledger.html written: build {APP['hash']}, "
      f"{DS['contested']}/{DS['items']} contested")
