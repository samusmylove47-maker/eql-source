"""learn/still-true.html — the register of inherited advice, tested.

WHY THIS PAGE EXISTS
--------------------
Every EverQuest Legends player is a returning EverQuest player carrying
twenty-five years of muscle memory, and a large amount of what they know is now
wrong. Nobody in this ecosystem answers the question they actually have, which
is not "what is the respawn timer" but "is what I remember still true?"

eqlwiki cannot answer it: large parts of eqlwiki ARE the classic text. eqltools
computes what is currently true but never contrasts it with what people expect.
eqlegendstools does items. The gap is real and it is ours.

We had already written this product four times without naming it — multiclass,
D0-D4 not raising mob levels, "you need a full group of level 50s", the
Per-Level Hunting Guide being a P99 import. This page is where those live, and
where the next one goes.

THE RULE THIS PAGE ENFORCES ON ITSELF
-------------------------------------
An entry may be OPEN. That is not a failure state, it is the normal one. What
an entry may never be is confidently resolved on evidence that does not support
it. Two of the entries below exist because someone did exactly that:

  - A player asked an AI whether Paragon of Spirit stacks with Clarity. It
    answered that the buff uses "slots nine, ten and eleven", citing eqlwiki's
    Buff Lines page. That page describes slots 1-8 and a Layer 2, and mentions
    no slot 9, 10 or 11. It does not mention Paragon of Spirit at all, and the
    spell has no page on the wiki - the URL 404s. The answer was built on an
    absence and then backfilled from Live EverQuest and Project 1999, which is
    precisely the reasoning this site exists to refuse.

  - Asked to be more certain, the same tool returned MORE sources and MORE
    specificity. Confidence went up; evidence did not. Worth naming, because
    it is the failure mode every player using an AI assistant will meet.

STATUS VALUES
-------------
  changed  - classic behaviour does not apply, and we can show why
  same     - classic behaviour does apply, and we can show why
  open     - nobody has shown either, and we say what would
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

LABEL = {'changed': 'Changed', 'same': 'Still true', 'open': 'Open'}
TONE = {'changed': 'var(--warn-t)', 'same': 'var(--ok)', 'open': 'var(--instr)'}

ENTRIES = [
    dict(status='open',
         q='Does Paragon of Spirit stack with Clarity and bard regeneration songs?',
         classic='On Live EverQuest and on Project 1999 the beastlord line is widely reported to '
                 'occupy its own buff slots, so it stacks with enchanter Clarity and with bard '
                 'regeneration songs.',
         legends='<strong>Nobody has published an answer for Legends.</strong> Asked on 10 August '
                 '2026, an AI assistant answered that the spell uses &ldquo;slots nine, ten and '
                 'eleven&rdquo; and cited eqlwiki&rsquo;s <em>Buff Lines</em> page. We read that '
                 'page the same day. It describes slots 1&ndash;8 and a Layer 2. <strong>It '
                 'contains no slot 9, 10 or 11, and it does not mention Paragon of Spirit at '
                 'all.</strong> The spell has no page on eqlwiki either &mdash; the URL returns '
                 '404. The answer was reasoning from an absence, then backfilled from Live and '
                 'Project 1999.',
         note='Asked to be more certain because the answer was worth dozens of hours, the same '
              'tool returned more sources and more specific detail. <strong>Confidence rose; '
              'evidence did not.</strong> That is the failure mode every player using an AI '
              'assistant will meet, and it is worth more than this one spell.',
         evidence=[
             ('T2', 'eqlwiki <em>Buff Lines</em>, read 10 Aug 2026',
              'Lists Cantata of Replenishment at +13, Cassindra&rsquo;s Chorus of Clarity at '
              '+7 (+14 pulsed) and Clarity II at +11 in its mana regeneration tables. Slots run '
              '1&ndash;8 plus a Layer 2. Paragon of Spirit does not appear.'),
             ('&mdash;', 'eqlwiki <em>Paragon of Spirit</em>, read 10 Aug 2026',
              'No such page. HTTP 404.'),
         ],
         settle='Cast Paragon of Spirit, then have a bard sing Cantata of Replenishment and an '
                'enchanter cast Clarity on the same target. <strong>A screenshot of the buff bar '
                'showing all three at once settles it outright.</strong> The combat log adds the '
                'timestamps and any overwrite message &mdash; if one displaces another, the log '
                'shows the displaced spell wearing off within a second of the new cast rather '
                'than at its natural duration.',
         credit='Raised by Avenrae, 10 August 2026, after an AI assistant gave two confident and '
                'differently-worded answers.'),

    dict(status='open',
         q='Do slashing and blunt weapons still suffer underwater?',
         classic='In classic EverQuest, underwater combat is widely reported to have penalised '
                 'slashing and blunt weapons, leaving piercing as the sensible choice in water '
                 'zones. <strong>We have not sourced this to a citable record</strong>, and say '
                 'so rather than repeating it as established.',
         legends='<strong>Reported not to apply.</strong> A player fighting in Kedge Keep &mdash; '
                 'a zone that is entirely underwater &mdash; reports landing normal hits with a '
                 'sword.',
         note='eqlwiki&rsquo;s Kedge Keep page carries <code>{{Classic Era}}</code>, discusses '
              'breathing at length, and says nothing whatever about weapon types underwater. Its '
              'search returns zero results for &ldquo;underwater&rdquo; on a wiki whose own Kedge '
              'Keep page uses the word repeatedly, so <strong>the search index is unreliable and '
              'an empty result there proves nothing.</strong>',
         evidence=[
             ('Tier C', 'Annalise, 9 August 2026',
              'First-hand, in Kedge Keep, using a sword and landing hits. Unconfirmed: a report '
              'of play, not a parsed log.'),
             ('T5', 'eqlwiki <em>Kedge Keep</em>, read 9 Aug 2026',
              'Classic Era import. Silent on weapon types underwater. Neither confirms nor denies.'),
         ],
         settle='One combat log line showing a slashing or blunt weapon landing normal damage on '
                'a mob while submerged. If a penalty exists it should show as a visible drop in '
                'average damage against the same mob type fought on land.',
         credit='Found by Annalise, 9 August 2026.'),

    dict(status='changed',
         q='Can you still plan a character around one class?',
         classic='Every character is one class, chosen at creation and permanent.',
         legends='<strong>No. Characters run three classes at once.</strong> Two at creation, a '
                 'third at level 10, with primary class and race locking permanently at 11. The '
                 'active trio uses the level of the <em>lowest</em> class in it.',
         note='This invalidates a large amount of inherited advice in both directions, and it is '
              'the single biggest reason a classic guide can be confidently wrong about Legends.',
         evidence=[
             ('T1', 'Official documentation and the level 11 lock',
              'Published behaviour, not inferred. The deity, race and primary class unlock tokens '
              'are priced in the Producer&rsquo;s Letter of 8 July 2026, which only makes sense '
              'because those choices lock.'),
         ],
         settle='Settled.',
         credit=''),

    dict(status='changed',
         q='Does raising the difficulty just make mobs higher level?',
         classic='No equivalent existed. Difficulty tiers are new.',
         legends='<strong>No. D0&ndash;D4 does not raise mob levels at all.</strong> It gives mobs '
                 'player-style class kits, widens aggro ranges and pre-upgrades loot. The tiers '
                 'are named in game and the zone line prints the name on entry: D0 Base, D1 '
                 'Awakened, D2 Adaptive, D3 Fused, D4 Refined.',
         note='<strong>And it starts earlier than published.</strong> The published claim is that '
              'named mobs run multiclass from D2. In Castle Mistmoore at <strong>D1</strong>, two '
              'ordinary trash types backstabbed 39 times between them while the same types were '
              'logged casting Root, Screaming Terror and Shadow Vortex. Backstab is a rogue '
              'ability and a spell list is not, so that mob type carried two kits at D1, on trash.',
         evidence=[
             ('Tier M', 'Our own logs, Castle Mistmoore, 8 August 2026',
              '<em>An initiate familiar</em> 22 backstabs and <em>a pledge familiar</em> 17, '
              'alongside logged casts from the same types. Melee 1&ndash;38, backstab 100&ndash;143.'),
             ('T1', 'Zone line on entry',
              '<code>You have entered The Castle of Mistmoore 1 (Awakened).</code> The number and '
              'the name agree, and the modal loot drop of +1 agrees independently.'),
         ],
         settle='Settled for D1 and D2. <strong>D3 and D4 hit points are pinned by nobody</strong>, '
                'and which class kits attach to which raid boss at D3+ is unpublished. That needs '
                'a log from a raid at D3 or D4.',
         credit=''),

    dict(status='open',
         q='Do named mobs still have placeholders?',
         classic='Named mobs share a spawn point with placeholder mobs. You kill the placeholder '
                 'repeatedly until the named appears, and published spawn percentages describe '
                 'how often it does.',
         legends='<strong>Reported gone in the revamped dungeons</strong> &mdash; Befallen, '
                 'Blackburrow and Najena &mdash; where the named is reported to spawn every cycle.',
         note='The spawn percentages on our own Najena plate are almost certainly meaningless if '
              'this holds. They are left printed and struck through rather than deleted, because '
              'deleting them would hide what the source says.',
         evidence=[
             ('T1', 'Revamp patch note, 23 June 2026',
              'Promises &ldquo;a striking lack of placeholders for named mobs&rdquo;.'),
             ('Tier C', 'Avenrae, 9 August 2026',
              'Ten or more consecutive cycles at The Tenderizer with no placeholder seen, plus '
              'hours in Befallen and Blackburrow.'),
             ('T5', 'eqlwiki <em>Category:Named Mobs</em>',
              'States it plainly &mdash; but the sentence was added 10 July 2026, eighteen days '
              'before launch, on a page whose oldest revision is a February 2019 Project 1999 '
              'import. Intent, not observation.'),
             ('T5', 'eqlwiki individual mob pages, against',
              '<em>Drelzna</em>: &ldquo;Her placeholder is a necromancer that spawns in front of '
              'the chair.&rdquo; Classic text nobody has revisited. The only source of the four '
              'that disagrees.'),
         ],
         settle='A combat log across several consecutive cycles at one camp, showing the named on '
                'every spawn. That is one evening&rsquo;s play and it closes the question outright.',
         credit='Confirmed in play by Avenrae, 9 August 2026.'),

    dict(status='changed',
         q='Is the Per-Level Hunting Guide still good advice?',
         classic='It is one of the most-linked pages on the wiki.',
         legends='<strong>It is a Project 1999 import and it predates everything that matters.</strong> '
                 'It cites P1999 forums, carries the phrase &ldquo;As of June 2020&rdquo;, and '
                 'repeats the P99-specific claim that characters &ldquo;generally perform like '
                 'characters three or more levels higher&rdquo; &mdash; a statement about a '
                 'single-class server at fixed difficulty. It predates both multiclass and '
                 'D0&ndash;D4, so it is wrong in both directions.',
         note='',
         evidence=[
             ('T5', 'eqlwiki <em>Per-Level Hunting Guide</em>',
              'Project 1999 import by origin, with its own internal citations to P1999 forums.'),
         ],
         settle='Settled.',
         credit=''),
]


def entry_html(e, i):
    ev = ''.join(
        f'<li><span class="ev-t">{tier}</span><span class="ev-s">{src}</span>'
        f'<span class="ev-d">{detail}</span></li>'
        for tier, src, detail in e['evidence'])
    note = f'<p class="st-note">{e["note"]}</p>' if e['note'] else ''
    credit = f'<p class="st-credit">{e["credit"]}</p>' if e['credit'] else ''
    return f'''
  <article class="st-entry" id="q{i}" style="--c:{TONE[e['status']]}">
    <div class="st-head">
      <span class="st-status">{LABEL[e['status']]}</span>
      <h3>{e['q']}</h3>
    </div>
    <div class="st-split">
      <div><h4>What classic did</h4><p>{e['classic']}</p></div>
      <div><h4>What Legends does</h4><p>{e['legends']}</p></div>
    </div>
    {note}
    <h4 class="st-evh">The evidence</h4>
    <ul class="st-ev">{ev}</ul>
    <p class="st-settle"><strong>What would settle it.</strong> {e['settle']}</p>
    {credit}
  </article>'''


counts = {k: sum(1 for e in ENTRIES if e['status'] == k) for k in LABEL}
body = ''.join(entry_html(e, i + 1) for i, e in enumerate(ENTRIES))

CSS = '''<style>
.st-entry{border:1px solid #2E3A41;border-left:3px solid var(--c);border-radius:4px;
  padding:20px 22px;margin:0 0 18px;background:#151B1F}
.st-head{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;margin:0 0 14px}
.st-status{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--c);border:1px solid var(--c);border-radius:3px;
  padding:2px 7px;white-space:nowrap}
.st-head h3{margin:0;font-family:"Saira Condensed",sans-serif;font-weight:600;font-size:20px;
  letter-spacing:.01em;color:var(--ink)}
.st-split{display:grid;grid-template-columns:1fr 1fr;gap:20px}
@media(max-width:720px){.st-split{grid-template-columns:1fr;gap:14px}}
.st-split h4,.st-evh{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--faint);margin:0 0 5px}
.st-evh{margin:16px 0 7px}
.st-split p{margin:0;color:var(--dim);font-size:14.5px;line-height:1.6}
.st-note{margin:14px 0 0;padding:11px 13px;background:rgba(255,255,255,.03);
  border-left:2px solid var(--faint);color:var(--dim);font-size:14px;line-height:1.6}
.st-ev{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.st-ev li{display:grid;grid-template-columns:64px 1fr;gap:10px;align-items:start;
  font-size:13.5px;line-height:1.55}
.st-ev .ev-t{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.08em;
  color:var(--faint);padding-top:2px}
.st-ev .ev-s{color:var(--ink);font-weight:600}
.st-ev .ev-d{grid-column:2;color:var(--dim)}
@media(max-width:560px){.st-ev li{grid-template-columns:1fr}.st-ev .ev-d{grid-column:1}}
.st-settle{margin:16px 0 0;padding:12px 14px;border-left:3px solid var(--instr);
  background:rgba(92,147,196,.06);color:var(--dim);font-size:14px;line-height:1.6}
.st-settle strong{color:var(--ink)}
.st-credit{margin:10px 0 0;font-family:"IBM Plex Mono",monospace;font-size:12px;
  color:var(--faint)}
</style>'''

page = head("Is it still true?",
  "Inherited EverQuest advice tested against EverQuest Legends: what changed, what did not, and "
  "what nobody has established either way. Every entry names its evidence, its date and what would "
  "settle it.",
  rel="../", extra=CSS) + bar("../") + f'''
<main>

<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="../index.html">EQL Source</a> &nbsp;/&nbsp; Learn
      &nbsp;/&nbsp; Is it still true?</p>
    <h1 class="display">You already know<br><em>a lot that is wrong.</em></h1>
    <p class="hero-lede">Almost everyone playing EverQuest Legends played EverQuest, and arrives
      carrying twenty-five years of habit. Some of it still holds. Some of it was quietly replaced.
      The wiki cannot tell you which is which, because large parts of the wiki <em>are</em> the old
      text. This page is the register: one entry per piece of inherited advice, each with its
      evidence, its date, and what it would take to settle it.</p>
    <p class="hero-sig"><span>{len(ENTRIES)} entries</span>
      <span>{counts['changed']} changed</span><span>{counts['open']} open</span>
      <span>Every gap named</span></p>
  </div>
</section>

<section class="band" style="border-top:0;padding-top:0">
  <div class="shell">
    <div class="note"><strong>An open entry is the normal state, not a failure.</strong> What an
      entry may never be is confidently resolved on evidence that does not support it. Two of the
      entries below exist because that happened &mdash; an assistant answered a stacking question
      from a page that does not mention the spell, then, asked to be more certain, returned
      <em>more</em> sources and <em>more</em> specific detail. Confidence rose; evidence did not.
      If you only take one thing from this page, take that.</div>
{body}
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="sechead"><span class="n">Contribute</span>
      <div><h2 class="sec">Most of these close with one screenshot</h2>
      <p class="lede" style="margin:0">Not an argument, not another wiki read &mdash; one buff bar,
        one log line, one spawn cycle counted. Every entry above says exactly what would settle it,
        and anyone who settles one is credited by name on it.</p></div></div>
  </div>
</section>

</main>
''' + foot("../")

open('public/learn/still-true.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"learn/still-true.html written: {len(ENTRIES)} entries "
      f"({counts['changed']} changed, {counts['same']} still true, {counts['open']} open)")
