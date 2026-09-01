"""tools/lockouts.html — the page for the lockout tracker.

WHY THIS TOOL IS PROMOTED
-------------------------
It answers one question nothing else here answers: **what is still open.** Every
other tracker on this site tells you what you have done; this one tells you what
you may still do, which is the question you actually have at the start of an
evening.

And it holds this site's standard on its own, arrived at in another repository:
where it has no history for a boss it prints **not looked**, not "available".
Guessing "open" would be the useful-looking answer and the wrong one, in the one
direction that wastes a night.

EVERY FIGURE IS READ, AND TWO OF THEM ARE READ OUT OF THE APPLICATION ITSELF
---------------------------------------------------------------------------
The build facts — hash, size, date — come from assets/lockouts.json, which
_build/lockouts.py writes when it copies the app.

The timing figures do not live in that manifest. They live in the application,
so they are parsed out of the served bundle at build time. That matters more
here than anywhere else on the site, because the figure is the entire subtlety
of the tool:

  * `differenceFromReplaySeconds` is 514,800 — exactly 5 days 23 hours — and is
    marked `observed`. It is the DIFFERENCE between the boss lockout timer and
    the replay timer, arrived at by subtraction, which cancels the unknown
    elapsed time. That is why it holds whatever the elapsed time was.
  * `days` is 6 and is marked `conditional`, on the Replay Timer period being
    exactly one hour.

**The six days is not measured and this page must never say it is.** The
Director asserted it as fact and retracted it this week; re-importing that error
into a page would be the retraction failing to propagate, which is the fault
this project keeps finding in its own work.

So the page prints the difference as the fact and the period as the condition,
and if the constants cannot be found in the bundle the build FAILS rather than
quietly printing a page with the interesting part missing.

THREE THINGS THIS PAGE MUST NOT SAY
-----------------------------------
1. Not "resets Tuesday" as the lockout rule. Tuesday is `RESET_RULE`, and it is
   scoped in the app to the weekly task and its Void-Touched Potential token.
   The instance lockout is a separate, rolling object with no weekday at all.
2. Not "six-day lockout" as measured. See above.
3. Not a countdown, anywhere. The owner ruled it out and the module refuses to
   emit one — for two reasons, one of which is that the reset hour is not
   recorded, so a ticking number would be inventing precision.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

LK = json.load(open('assets/lockouts.json', encoding='utf-8'))
APP = LK['app']
HREF = f"../app/{APP['file']}"
SERVED = os.path.join('public', 'app', APP['file'])


def model():
    """The timing constants, parsed out of the application we actually serve.

    Not typed, and not read from a sibling repository either: the bundle in
    public/app/ is the thing a reader will run, so it is the only copy whose
    numbers this page is entitled to describe.
    """
    try:
        src = open(SERVED, encoding='utf-8', errors='replace').read()
    except OSError:
        sys.exit(f"lockouts page: {SERVED} is not there. Run "
                 f"python3 _build/lockouts.py first")
    out = {}
    for key, pattern in (
            ('diff_s', r'differenceFromReplaySeconds:\s*(\d+)'),
            ('diff_prov', r"differenceProvenance:\s*'([a-z ]+)'"),
            ('days', r'days:\s*(\d+)'),
            ('days_prov', r"daysProvenance:\s*'([a-z ]+)'")):
        m = re.search(pattern, src)
        if not m:
            # Loudly. A page that silently loses the one figure it exists to
            # explain still builds, still validates, and is worthless.
            sys.exit(f"lockouts page: {key} not found in {APP['file']}. The "
                     f"app changed shape; fix this parse rather than removing "
                     f"the figure from the page")
        out[key] = m.group(1)
    return out


M = model()
DIFF_S = int(M['diff_s'])
# Computed, so the words cannot disagree with the number beside them.
_d, _rem = divmod(DIFF_S, 86400)
_h = _rem // 3600
DIFF_WORDS = f"{_d} days {_h} hours"
DIFF_EXACT = f"{DIFF_S:,}"

CSS = '''<style>
.slrun h2{font-family:"Saira Condensed",sans-serif;font-weight:600;font-size:var(--t-lg);
  letter-spacing:.04em;text-transform:uppercase;margin:0 0 var(--s-2);color:var(--bone)}
.lkgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));
  gap:1px;background:var(--rule);border:1px solid var(--rule);border-radius:var(--r);
  overflow:hidden;margin:var(--s-5) 0 0}
.lkgrid>div{background:var(--panel);padding:15px 17px}
.lkgrid b{display:block;font-family:"IBM Plex Mono",monospace;font-size:20px;
  color:var(--bone);letter-spacing:.01em}
.lkgrid span{display:block;margin-top:4px;font-family:"IBM Plex Mono",monospace;
  font-size:11px;letter-spacing:.13em;text-transform:uppercase;color:var(--faint)}
/* Direct child only. `.lkgrid em` also caught the emphasis INSIDE the note and
   set it display:block, so "Distinct from open and from done" broke across four
   lines. Caught by reading the built page, which no check here can do. */
.lkgrid>div>em{display:block;margin-top:9px;font-style:normal;font-size:14px;
  line-height:1.55;color:var(--dim)}
.lkgrid em em{font-style:italic}
.lktimers{list-style:none;margin:var(--s-5) 0 0;padding:0;display:grid;gap:1px;
  background:var(--rule);border:1px solid var(--rule);border-radius:var(--r);overflow:hidden}
.lktimers li{background:var(--panel);padding:14px 17px;display:grid;
  grid-template-columns:minmax(0,190px) minmax(0,1fr);gap:6px 20px}
.lktimers b{font-family:"Saira Condensed",sans-serif;font-size:17px;font-weight:600;
  text-transform:uppercase;letter-spacing:.03em;color:var(--bone)}
.lktimers span{color:var(--dim);font-size:14.5px;line-height:1.55}
.lktimers .p{display:inline-block;margin-left:7px;font-family:"IBM Plex Mono",monospace;
  font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--faint);
  border:1px solid var(--rule2);border-radius:3px;padding:1px 5px;vertical-align:2px}
@media(max-width:640px){.lktimers li{grid-template-columns:1fr}}
</style>'''

page = head(
    "Lockout tracker",
    "A browser tool that reads your EverQuest Legends combat log and says which "
    "raid lockouts are still open. It says “not looked” where it has no "
    "history, and every figure carries where it came from.",
    rel="../", extra=CSS, og="tools", canon="tools/lockouts") + bar("../") + f'''
<main>

<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp;
      <a href="index.html">Tools</a> &nbsp;/&nbsp; Lockout tracker</p>
    <h1 class="display">Lockout tracker.</h1>
    <p class="hero-lede">Every other tracker here tells you what you have done. This one
      tells you <strong>what is still open</strong> &mdash; which is the question you have at
      the start of an evening. It reads your own combat log, in the browser.
      <strong>Nothing is uploaded</strong>; there is no server to upload to.</p>
    <p class="hero-sig"><span>Reads your log</span><span>Your log never leaves</span><span>No install</span></p>
  </div>
</section>

<div class="shell">

  <section class="band" style="border-top:0;padding-top:0">
    <div class="slrun">
      <a href="{HREF}" style="--c:var(--instr)">
        <h2>Run it in your browser</h2>
        <p>One file, {APP['kb']} KB, served from this site. Point it at your log and it
          works out what is still open from what it can see there.</p>
        <p class="m">Build {APP['hash']} &middot; nothing installed &middot; your log never leaves this machine</p>
        <span class="go">Open the app &rarr;</span>
      </a>
    </div>
    <!-- THE TOOL CANNOT READ A LOG THE GAME NEVER WROTE.
         The word "/log on" appeared nowhere on this page and nowhere in the
         served application, while EverQuest writes no log until it is asked to.
         A reader who has never enabled it opens the tool, gets a full week of
         "not looked", and is given nothing anywhere to act on - which is CORRECT
         behaviour and USELESS OUTPUT at the same time, and no amount of accuracy
         in the grid closes that.
         The wording is the site's own, from tools/sky-ledger.html: "Anything
         looted before /log on is invisible." Reused rather than re-authored. -->
    <p class="note" style="margin-top:var(--s-5)"><strong>All &ldquo;not looked&rdquo;?
      Start with the log.</strong> The game writes one only when asked:
      <code>/log on</code> begins it. Anything earlier is invisible, which is what the
      grid is telling you.</p>
  </section>

  <section class="band">
    <div class="sechead"><span class="n">01</span><div><h2 class="sec">It says &ldquo;not looked&rdquo; rather than guessing</h2>
      <p class="lede" style="margin:0">This is why it is promoted here, and it is a
        correctness property rather than a feature.</p></div></div>
    <p class="lede">A cell it has no history for reads <strong>not looked</strong>. It does not
      read <em>open</em>. The two are different claims and only one of them is true: an empty
      log says nothing about whether a boss is available, and the guess that looks most useful
      is wrong in the one direction that costs you a night.</p>
    <p class="lede">The same discipline runs through the rest of it. It will only report a
      lockout as <strong>refused</strong> where a positive control is present in the log to
      prove a refusal would have been visible; otherwise it degrades to <strong>unknown</strong>
      rather than inventing a lock. And repeat kills of one boss at one tier are recorded but
      never counted twice &mdash; a kill proves the fight happened, not that a second
      completion was consumed.</p>
    <div class="lkgrid">
      <div><b>not looked</b><span>The state that does the work</span>
        <em>Distinct from <em>open</em> and from <em>done</em>. No history is not evidence
          of availability.</em></div>
      <div><b>unknown</b><span>Where a refusal could not be seen</span>
        <em>Reported instead of a lock whenever the log cannot prove a refusal would have
          shown up.</em></div>
      <div><b>{APP['kb']} KB</b><span>The whole application</span>
        <em>One file, build <code>{APP['hash']}</code>, read {LK['read']}.</em></div>
    </div>
  </section>

  <section class="band">
    <div class="sechead"><span class="n">02</span><div><h2 class="sec">Three timers, and it refuses to merge them</h2>
      <p class="lede" style="margin:0">Most of what is said about lockouts in this game is one
        of these three mistaken for another.</p></div></div>
    <ul class="lktimers">
      <li><b>Weekly task</b><span>Turns over on a Tuesday, and this is the only weekday
        anywhere in the model. It governs <strong>the weekly task and its Void-Touched
        Potential token</strong> &mdash; not instance loot.<span class="p">stated, not measured</span>
        The hour is not recorded, so on the turnover day itself the tool evaluates both
        possibilities and marks the cells that disagree <code>unknown</code>.</span></li>
      <li><b>Instance lockout</b><span>A rolling timer. No weekday, no boundary, and
        <strong>not a weekly reset</strong>. This is the one people describe as resetting on
        Tuesday, and it does not.<span class="p">rolling</span></span></li>
      <li><b>Replay timer</b><span>Also rolling, about an hour, and it governs
        <strong>re-entry rather than loot</strong>. The tool records it so it can be kept out
        of the lockout cells; it is the likely origin of the community &ldquo;rolling 18
        hours&rdquo; claim.<span class="p">re-entry only</span></span></li>
    </ul>
  </section>

  <section class="band">
    <div class="sechead"><span class="n">03</span><div><h2 class="sec">What is measured, and what only follows from it</h2>
      <p class="lede" style="margin:0">The distinction is the whole subtlety, and it is easy to
        state one as the other.</p></div></div>
    <p class="lede"><strong>The measured figure is a difference, not a duration.</strong> Between
      the replay timer and the boss timer there are exactly <strong>{DIFF_WORDS}</strong>
      &mdash; {DIFF_EXACT} seconds. It is arrived at by subtracting one from the other, and the
      subtraction cancels how long ago the lock was taken, which is why it holds whatever that
      elapsed time was. That is the part that does not depend on an assumption.</p>
    <p class="lede"><strong>A {M['days']}-day lockout is what follows</strong> <em>if</em> the replay
      period is exactly one hour. The tool marks that figure <code>{M['days_prov']}</code> and
      names the condition, rather than publishing it as a measurement. This page does the same:
      it is a reasonable reading, it is not a thing anyone has timed, and the difference between
      those two sentences is the reason this site exists.</p>
    <div class="lkgrid">
      <div><b>{DIFF_WORDS}</b><span>The difference &middot; {M['diff_prov']}</span>
        <em>{DIFF_EXACT} seconds between the two timers. Independent of elapsed time,
          because it is a subtraction.</em></div>
      <div><b>{M['days']} days</b><span>The period &middot; {M['days_prov']}</span>
        <em>Follows only if the replay period is exactly one hour. Not measured.</em></div>
      <div><b>No countdown</b><span>Deliberately absent</span>
        <em>The reset hour is not recorded, so a ticking number would be inventing
          precision the log cannot support.</em></div>
    </div>
  </section>

  <section class="band">
    <div class="sechead"><span class="n">04</span><div><h2 class="sec">Every figure carries where it came from</h2></div></div>
    <p class="lede">Nothing leaves the module as a bare number. Each value carries its own
      provenance &mdash; observed, inferred, or not recorded &mdash; and <strong>the labels are
      attached per figure rather than per object</strong>, so a measured quantity and an assumed
      one sitting in the same record do not inherit one another's standing. The difference above
      is marked <code>{M['diff_prov']}</code> and the period beside it <code>{M['days_prov']}</code>,
      in the same constant.</p>
    <p class="lede">That is the rule this site had to learn the expensive way, on the Plane of
      Sky dataset, where one <em>verified</em> flag covered thirty-odd claims read from different
      pages on different days. It was reached here independently, in another repository, and it
      is the strongest single reason to trust the output.</p>
    <div class="note sig"><strong>Where it stops.</strong> It reports what your log has seen and
      says so where it has seen nothing. It does not know what you did on a character whose log
      you have not given it, it does not know the reset hour, and it does not count a repeat kill
      as a second completion.</div>
  </section>

</div>
</main>
''' + foot("../")

open('public/tools/lockouts.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"tools/lockouts.html written: build {APP['hash']}, "
      f"difference {DIFF_WORDS} ({M['diff_prov']}), period {M['days']}d ({M['days_prov']})")
