"""tools/gap-engine.html — the surface for Session E's gap engine.

WHAT THIS PAGE IS, AND WHAT IT IS NOT, TODAY
--------------------------------------------
The engine is a contract and a running function in another repository. It is not
yet a bundle this site can serve. So this page **describes the tool and renders a
synthetic sample**, and says so in the first screenful. It does not offer a file
input, because a control that does nothing is the empty-class-picker failure this
repository already carries a scar from — a tool shipped with every check green
and a dead picker, because nothing here could tell a full pane from a working
one.

When E ships a bundle, the sample block becomes the live output and the wiring is
one generator change. Until then the page is honest about being a preview rather
than looking finished.

EVERY FIGURE ON IT IS SYNTHETIC, AND THAT IS STRUCTURAL RATHER THAN CAREFUL
---------------------------------------------------------------------------
`assets/gap-engine.json` is E's `fixtures/sample-report.json`, vendored whole
with its own `_fixture`, `_why` and `_never` fields intact so the warning travels
with the data instead of being left behind in E's repository.

E's reasoning, which is better than the rule it replaces: a landing page has to
show what a tool looks like, an empty tool is unsellable, and **the natural
sample is a real log because a real log is what we have.** The moment a sample
renders a real character's numbers, per-character DPS ships inside the page's
bytes under the tool's own banner — and nobody would have decided to do that. It
would simply be the easiest way to make the page look finished. So the fixture
removes the opportunity rather than restating the rule.

If this page needs different numbers to look right, change the fixture's. They
are not claims and cannot be wrong.

THE TWO REGISTERS ARE THE POINT OF THE LAYOUT
----------------------------------------------
`measured` and `deltas` are different kinds of claim and the page renders them as
different registers — the same discipline the surveys already use for a measured
figure against a badged one. `measured` came out of a log. Every `delta` is a
DIFFERENCE against that reader's own observed baseline, never a level, because
the schema has no field for an absolute modelled number. A surface author cannot
render a modelled ceiling as a live readout by accident; there is nothing to read
it from.

REFUSALS ARE NOT A FOOTNOTE
---------------------------
They get the same heading level, the same card treatment and the same column
width as the deltas, immediately beside them. The Director's instruction was "as
prominently as", and "as prominently as" is a judgement someone can shade later
while believing they are complying. Equal markup is checkable, so scripts/check.py
fails the build if the refusals block is missing or if it carries fewer entries
than the data holds.

The reason is E's: a tool that silently omits what it cannot do fails open. A
reader sees a short list and reads it as "nothing else to improve", when the
truth may be "I could not see your gear". That is this site's own rule about
never deleting a flagged gap, arriving from another direction.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

R = json.load(open('assets/gap-engine.json', encoding='utf-8'))

# THE PAGE REFUSES TO BUILD FROM ANYTHING BUT A FIXTURE.
#
# This is the whole privacy guarantee reduced to four lines. If someone ever
# points this generator at a real report - the obvious shortcut when the engine
# starts producing them - the build stops rather than publishing a character's
# figures. The check is on the data rather than on the intention.
if not R.get('_fixture'):
    sys.exit("gap-engine: assets/gap-engine.json is not marked _fixture. This "
             "page renders SYNTHETIC data only; a real report must never be "
             "published here. See HANDOFF.md and E's fixtures/sample-report.json")

M, D, RF, COV = R['measured'], R['deltas'], R['refusals'], R['coverage']
CTX = R['context']

# Every delta must be a difference. The schema makes an absolute impossible, so
# this costs nothing and is checked anyway - the Director's instruction, and the
# cheap check is the one worth having when the expensive one is structural.
_bad = [d for d in D if not str(d.get('unit', '')).startswith('dps_delta')]
if _bad:
    sys.exit(f"gap-engine: {len(_bad)} delta(s) carry a unit that is not a "
             f"difference: {[d.get('unit') for d in _bad]}. A modelled absolute "
             f"must never reach a page")

REASON_LABEL = {
    'computable_from_catalogue': 'someone else does this better',
    'no_log_evidence': 'a log cannot see it',
    'instrument_unverified': 'the instrument is unproven',
    'privacy': 'refused, with no override',
    'out_of_scope': 'out of scope',
}


def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


# THE BASELINE TRAVELS WITH THE NUMBER, IN THE SAME SENTENCE.
#
# The first version of this page printed "+98.4" beside the words "against this
# character's own measured baseline", with the baseline itself — 214.6 — about
# two kilobytes higher up the document. That satisfies the letter of "a delta is
# a difference" and misses the point, and the Director found it by applying a
# test I had not: DOES THE CLAIM SURVIVE BEING EXCERPTED.
#
# It does not. The overlay teaser is a delta with no page around it. "+98.4"
# travelling alone is a number a reader will read as a score, which is the exact
# thing E's schema removes the field for. "+98.4 — 46% of your measured 214.6"
# cannot be misread and cannot be excerpted into meaninglessness.
#
# This is the same fault as a share card asserting a figure the body hedges,
# which this repository already gates against. I did not connect them.
def baseline_phrase(d):
    """"82% of your measured 105.2 DPS" — the comparison, never a bare number.

    THE SHARE IS THE ENGINE'S, NOT MINE. An earlier version of this function
    computed `value / measured.dps` here. E now emits `share_of_observed_dps`
    per delta, so computing it again would be two implementations of one
    quantity that can disagree — the exact duplication this repository spends
    its time removing, and the reason `zones-index.json` holds the revamp date
    instead of two generators holding it.

    The fallback computes it only when the engine did not supply it, and says
    plainly when there is no baseline at all rather than printing the delta as
    though it stood by itself.
    """
    base = M.get('dps')
    share = d.get('share_of_observed_dps')
    if share is None:
        try:
            share = float(d['value']) / float(base)
        except (TypeError, ValueError, ZeroDivisionError):
            return 'no measured baseline to compare against'
    return (f"{round(float(share) * 100)}% of your measured {base} DPS "
            f"({M.get('dps_window', 'window not stated')})")


def deltas_html():
    out = []
    for d in D:
        req = d.get('requires') or {}
        bits = ' &middot; '.join(
            f'{esc(k)}: {esc(", ".join(v) if isinstance(v, list) else v)}'
            for k, v in req.items())
        out.append(f'''
      <li class="ge-d">
        <p class="ge-lane">{esc(d['lane'])}<span class="ge-kind">{esc(d.get('kind', ''))}</span></p>
        <p class="ge-stat">{esc(d['statement'])}</p>
        <p class="ge-val"><b>+{esc(d['value'])}</b><span>{esc(baseline_phrase(d))}</span></p>
        {f'<p class="ge-mat">{esc(d["materiality"])}</p>' if d.get('materiality') else ''}
        {f'<p class="ge-req">{bits}</p>' if bits else ''}
        <p class="ge-fals"><em>What would show this wrong:</em> {esc(d.get('falsifier', 'not recorded'))}</p>
      </li>''')
    return "".join(out)


# A REFUSAL LIVING INSIDE `measured`, AND IT IS THE SHARPEST THING ON THE PAGE.
#
# E's resist entries carry `rate: null` with a note saying the denominator is
# unknown and NO RATE IS CLAIMED. That is the refusals discipline applied inside
# the measured register rather than in the refusals list — a count is published,
# the rate it obviously implies is not, and the reason is given in the same
# object.
#
# The temptation this removes is exact and this site has fallen for its cousin:
# "resisted 2 times" invites a page to print a resist rate, because a rate is
# what a reader wants. Without landings there is no denominator, and a rate
# computed from a numerator alone is invented. Rendering the null AS a null,
# with its note, is the whole point of carrying the field.
def resists_html():
    rs = M.get('resists') or []
    if not rs:
        return ''
    rows = "".join(f'''
      <li class="ge-nr">
        <p class="ge-lane">{esc(r.get('spell', 'unnamed'))}<span class="ge-kind r">no denominator</span></p>
        <p class="ge-stat">Resisted {esc(r.get('resisted'))} times, landed
          {esc(r.get('landed'))} &mdash; <strong>no rate is claimed</strong>.</p>
        <p class="ge-fals"><em>Why:</em> {esc(r.get('note', 'not recorded'))}</p>
      </li>''' for r in rs)
    return f'''
    <h3 class="ge-sub">Counted, but not turned into a rate</h3>
    <p class="lede">A count with no denominator is not a rate, and the engine says so in
      the data rather than leaving a page to work it out.</p>
    <ul class="ge-list">{rows}
    </ul>'''


def refusals_html():
    out = []
    for r in RF:
        out.append(f'''
      <li class="ge-r">
        <p class="ge-lane">{esc(r['lane'])}<span class="ge-kind r">{esc(REASON_LABEL.get(r['reason'], r['reason']))}</span></p>
        <p class="ge-stat">{esc(r.get('detail', ''))}</p>
        <p class="ge-fals"><em>What would settle it:</em> {esc(r.get('what_would_settle_it', 'not recorded'))}</p>
      </li>''')
    return "".join(out)


CSS = '''<style>
.ge-two{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));
  gap:var(--s-5);align-items:start;margin:var(--s-5) 0 0}
.ge-col>h3{font-family:"Saira Condensed",sans-serif;font-size:clamp(19px,2.4vw,23px);
  font-weight:600;text-transform:uppercase;letter-spacing:.04em;color:var(--bone);
  margin:0 0 4px;display:flex;align-items:baseline;gap:9px}
.ge-col>h3 b{font-family:"IBM Plex Mono",monospace;font-size:12px;font-weight:500;
  letter-spacing:.12em;color:var(--faint)}
.ge-col>p.lede{margin:0 0 var(--s-4)}
.ge-list{list-style:none;margin:0;padding:0;display:grid;gap:1px;
  background:var(--rule);border:1px solid var(--rule);border-radius:var(--r);overflow:hidden}
.ge-list li{background:var(--panel);padding:15px 17px}
.ge-lane{margin:0;font-family:"IBM Plex Mono",monospace;font-size:11.5px;
  letter-spacing:.1em;text-transform:uppercase;color:var(--faint);
  display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.ge-kind{border:1px solid var(--rule2);border-radius:3px;padding:1px 6px;
  font-size:10px;letter-spacing:.09em;color:var(--dim)}
.ge-kind.r{border-color:var(--warn-t);color:var(--warn-t)}
/* A no-rate row is styled like a refusal because it IS one, but it carries
   its own class so scripts/check.py can count refusals without counting
   these too. Sharing .ge-r made the check print "4 refusal(s)" against 3
   in the data, and made its equal-weight comparison measure the wrong
   quantity. */
.ge-stat{margin:7px 0 0;color:var(--bone);font-size:15.5px;line-height:1.5}
.ge-val{margin:9px 0 0;display:flex;align-items:baseline;gap:9px;flex-wrap:wrap}
.ge-val b{font-family:"IBM Plex Mono",monospace;font-size:21px;color:var(--ok-t)}
.ge-val span{font-size:12.5px;color:var(--faint)}
.ge-req,.ge-fals{margin:8px 0 0;font-size:13px;line-height:1.55;color:var(--dim)}
.ge-mat{margin:7px 0 0;font-size:12.5px;line-height:1.5;color:var(--faint);
  font-style:normal}
.ge-sub{font-family:"Saira Condensed",sans-serif;font-size:clamp(18px,2.2vw,21px);
  font-weight:600;text-transform:uppercase;letter-spacing:.04em;color:var(--bone);
  margin:var(--s-6) 0 4px}
.ge-req{font-family:"IBM Plex Mono",monospace;font-size:11.5px;color:var(--faint)}
.ge-fals em{font-style:normal;color:var(--faint)}
.ge-meas{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,190px),1fr));
  gap:1px;background:var(--rule);border:1px solid var(--rule);border-radius:var(--r);
  overflow:hidden;margin:var(--s-5) 0 0}
.ge-meas>div{background:var(--panel);padding:14px 16px}
.ge-meas b{display:block;font-family:"IBM Plex Mono",monospace;font-size:22px;color:var(--bone)}
.ge-meas span{display:block;margin-top:4px;font-family:"IBM Plex Mono",monospace;
  font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--faint)}
.ge-meas em{display:block;margin-top:8px;font-style:normal;font-size:13px;
  line-height:1.5;color:var(--dim)}
.ge-sample{border-left:3px solid var(--warn);background:rgba(201,69,58,.06);
  padding:13px 16px;margin:var(--s-5) 0 0;border-radius:0 var(--r) var(--r) 0}
.ge-sample strong{color:var(--bone)}
.ge-sample p{margin:0;color:var(--dim);font-size:14.5px;line-height:1.6}
</style>'''

page = head(
    "Gap engine",
    "A tool that reads your own EverQuest Legends combat log and says what to "
    "change — and says plainly what it will not answer and why. Every figure "
    "on this page is synthetic.",
    rel="../", extra=CSS, og="tools", canon="tools/gap-engine") + bar("../") + f'''
<main>

<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp;
      <a href="index.html">Tools</a> &nbsp;/&nbsp; Gap engine</p>
    <h1 class="display">Gap engine.</h1>
    <p class="hero-lede">Every other tracker here tells you what you have. This one reads your
      combat log and tells you <strong>what to change</strong> &mdash; as a difference against
      what you are already doing, never a score to hit. And it says out loud what it
      <strong>will not</strong> answer.</p>
    <p class="hero-sig"><span>Reads your log</span><span>Your log never leaves this machine</span><span>Not yet live</span></p>
  </div>
</section>

<div class="shell">

  <section class="band" style="border-top:0;padding-top:0">
    <div class="ge-sample">
      <p><strong>This page is a preview and every number on it is invented.</strong> The engine
        runs, on real logs, in its own repository &mdash; it is not yet wired into this site, so
        there is no file input here rather than one that does nothing. A control that invites you
        to drop in a log and then does nothing would be the page lying to you, and this is a tool
        whose whole claim is that it refuses to overstate.</p>
      <p style="margin-top:10px"><strong>What would make it live:</strong> the engine ships as a
        bundle. When it does, this page reads your log in your browser and sends nothing &mdash;
        there is no server to send it to, and this site holds no logs at all, so it could not
        compute your figures even if it wanted to.</p>
      <p style="margin-top:10px"><em>{esc(R['_why'])}</em></p>
    </div>
  </section>

  <section class="band">
    <div class="sechead"><span class="n">01</span><div><h2 class="sec">Measured, and modelled, are shown as two different things</h2>
      <p class="lede" style="margin:0">A page that mixes them invites you to trust the weaker
        one.</p></div></div>

    <p class="lede"><strong>Measured</strong> comes out of the log, computed in your browser.
      A DPS figure always carries the window it was measured over: four shipped meters use four
      denominators, and the spread is more than double.</p>

    <div class="ge-meas">
      <div><b>{esc(M['dps'])}</b><span>DPS &middot; {esc(M['dps_window'])}</span>
        <em>{esc(M['dps_window_note'])}</em></div>
      <div><b>{esc(round(M['crit_rate'] * 100, 2))}%</b><span>Crit rate</span>
        <em>Counted from the log&rsquo;s own crit lines, over the hits above.</em></div>
      <div><b>{esc(M['hits_counted'])}</b><span>Hits counted</span>
        <em>Across {esc(M['engagements'])} engagements.
          {esc(M['killing_blows_excluded_from_rates'])} killing blows are excluded from the
          rates: a killing blow is truncated by the target dying.</em></div>
      <div><b>{esc(M['stance_inferred'])}</b><span>Stance &middot; inferred</span>
        <em>{esc(M['stance_evidence'])}</em></div>
    </div>

    {resists_html()}
  </section>

  <section class="band">
    <div class="sechead"><span class="n">02</span><div><h2 class="sec">What it found, and what it refused</h2>
      <p class="lede" style="margin:0">These two columns carry equal weight on purpose. A tool
        that shows only what it found reads as &ldquo;nothing else to improve&rdquo;.</p></div></div>

    <div class="ge-two">
      <div class="ge-col">
        <h3>Deltas <b>{len(D)}</b></h3>
        <p class="lede">Every one is a <strong>difference against your own measured
          baseline</strong>. The output has no field for a modelled absolute, so a page cannot
          print one by accident.</p>
        <ul class="ge-list">{deltas_html()}
        </ul>
      </div>

      <div class="ge-col">
        <h3>Refusals <b>{len(RF)}</b></h3>
        <p class="lede">What it <strong>declined</strong>, with the reason and what would
          settle it. A tool that silently omits what it cannot do fails open: a short list reads
          as good news.</p>
        <ul class="ge-list">{refusals_html()}
        </ul>
      </div>
    </div>
  </section>

  <section class="band">
    <div class="sechead"><span class="n">03</span><div><h2 class="sec">What it saw, and what it assumed</h2></div></div>
    <p class="lede"><strong>Observed:</strong> {esc(", ".join(COV['inputs_observed']))}.
      <br><strong>Assumed, and therefore a source of error:</strong>
      {esc(", ".join(COV['inputs_assumed']))}.</p>
    <div class="note sig"><strong>Where it stops.</strong> {esc(COV['note'])}</div>
  </section>

</div>
</main>
''' + foot("../")

open('public/tools/gap-engine.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"tools/gap-engine.html written: {len(D)} deltas, {len(RF)} refusals, "
      f"fixture={R['_fixture']}")
