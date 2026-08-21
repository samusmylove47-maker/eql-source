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
import backstab as _BS
from _partials import head, bar, foot

LABEL = {'changed': 'Changed', 'same': 'Still true', 'open': 'Open'}
TONE = {'changed': 'var(--warn-t)', 'same': 'var(--ok)', 'open': 'var(--instr)'}

# The Mistmoore backstab damage, read out of the dataset at build time so no
# copy of it can go stale here. Only the damage a mob deals is published: how
# many swings were logged, over how many sessions and by whom, is a fact about
# an evening rather than about the game, and the Tier M badge already says the
# measurement happened.
_BSE = _BS.evidence()
_BSDMG = (f" Melee reaches {_BSE['melee_max']} and backstab {_BSE['bs_max']}, which is why no "
          "single average is printed for a mob that backstabs." if _BSE else "")

ENTRIES = [
    dict(status='open',
         q='Is haste a percentage, or a flat attack-speed value?',
         classic='A percentage that divides weapon delay. The formula everyone quotes is '
                 '<code>new delay = delay / (1 + haste)</code>, with haste as a decimal, and '
                 'item tooltips read <em>Haste +41%</em>.',
         legends='<strong>The two best sources in this community disagree, and we were '
                 'republishing one of them without noticing.</strong> EQL Tools states that '
                 'slow and haste in Legends are <em>flat values on an attack-speed stat</em> '
                 '&mdash; a mob at 100 attack speed with 60 haste sits at 160, and the numbers '
                 'add rather than compounding. eqlwiki&rsquo;s own <em>Haste Guide</em>, edited '
                 '4 August 2026, still carries the classic percentage formula and cites '
                 'classic-era raid content around it.',
         note='This is not an abstract question for us. <strong>Six Plane of Sky reward '
              'tooltips on this site carry percentage haste</strong> &mdash; five of them the '
              'identical <em>+41%</em>, which is a copied constant rather than five readings '
              '&mdash; they are marked suspect in place rather than deleted.',
         evidence=[
             ('T3', 'EQL Tools <em>Slow, haste &amp; crowd control</em>, read 14 Aug 2026',
              'States flat attack-speed values for Legends, with a worked example.'),
             ('T5', 'eqlwiki <em>Haste Guide</em>, read 14 Aug 2026',
              'Classic percentage formula, and the surrounding content describes classic-era '
              'raid targets. Last edited 4 Aug 2026, which is after launch and does not by '
              'itself make the mechanic current.'),
         ],
         settle='One screenshot of a Legends haste item tooltip. If it reads a bare number '
                'rather than a percentage, EQL Tools is right and every percentage figure on '
                'this site is a classic import.',
         credit=''),
    dict(status='changed',
         q='Do Journeyman&rsquo;s Boots still come from a quest, or do they drop?',
         classic='On Live in 1999 the boots were made a quest reward on 13 October, and '
                 'Project 1999 text records that they &ldquo;formerly dropped from Drelzna in '
                 'Najena&rdquo; before that change. That sentence is imported into '
                 'eqlwiki&rsquo;s Drelzna page, where it sits inside a structured NPC record '
                 'and reads like current data.',
         legends='<strong>They drop from Drelzna, and there is no quest.</strong> A first-hand '
                 'report, 14 August 2026: seen dropping for other players and confirmed by '
                 'guildmates. eqlwiki&rsquo;s <em>item</em> record agrees, naming Najena and '
                 'Drelzna as the source.',
         note='This is the shape of mistake this register exists for, and an auditor made it: '
              'reading the classic sentence inside the structured NPC page and '
              'grading our survey against it. The survey had read the item record and was '
              'right. <strong>A tier 5 sentence inside a tier 2 container is the most '
              'dangerous object in this ecosystem</strong>, because it wears the wrong clothes.',
         evidence=[
             ('Report', 'First-hand report, 14 Aug 2026',
              'The boots seen dropping for other players, confirmed by guildmates. First-hand '
              'and unparsed, so it carries no tier: the scale ranks readings of documents, and '
              'this is neither a document nor a log.'),
             ('T2', 'eqlwiki <em>Journeyman&rsquo;s Boots</em> item record',
              'Names Najena and Drelzna as the source.'),
             ('T5', 'eqlwiki <em>Drelzna</em> NPC page',
              'Carries the Project 1999 sentence about the 1999 quest change, verbatim.'),
         ],
         settle='One combat log line showing the loot. No parsed session here holds a Drelzna '
                'kill, so this stays a report until a parse replaces it.',
         credit=''),
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
         credit='Raised 10 August 2026, after an AI assistant gave two confident and '
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
             ('Report', 'A player report, 9 August 2026',
              'First-hand, in Kedge Keep, using a sword and landing hits. Unconfirmed: a report '
              'of play, not a parsed log.'),
             ('T5', 'eqlwiki <em>Kedge Keep</em>, read 9 Aug 2026',
              'Classic Era import. Silent on weapon types underwater. Neither confirms nor denies.'),
         ],
         settle='One combat log line showing a slashing or blunt weapon landing normal damage on '
                'a mob while submerged. If a penalty exists it should show as a visible drop in '
                'average damage against the same mob type fought on land.',
         credit='Credited on the credits page.'),

    dict(status='changed',
         q='Is a class-locked epic quest closed to everyone else?',
         classic='On Live EverQuest and on Project 1999 a class epic is a class quest. The '
                 'Fiery Avenger is the paladin epic, and the quest steps as well as the reward '
                 'are understood to be paladin-only.',
         legends='<strong>The quest is not class-locked. The reward still is.</strong> A '
                 'non-paladin completed every step of the Fiery Avenger, final turn-in included. '
                 'The item it returns is unchanged: <code>Class: PAL</code>, 2H Slashing, 33/44, '
                 'Flame Shock combat effect at level 45, Virtuous Bash worn effect.',
         note='So the two halves separate. <strong>Doing the quest and being able to hold the '
              'reward are different permissions</strong>, and only the second is still a class '
              'gate &mdash; which a trio carrying Paladin would clear. This is one epic, on one '
              'character. It is a reason to test the other fifteen, not evidence about them: '
              '<strong>we have no report on any other epic and do not assume this generalises.</strong>',
         evidence=[
             ('Report', 'A player report, 10 August 2026',
              'First-hand: &ldquo;can now confirm can do all parts of the fiery avenger '
              'including final turn in as a non paladin&rdquo;. Reported with an in-game '
              'screenshot of the completed item. A report of play, not a parsed log.'),
             ('Report', 'Item inspection, 10 August 2026',
              'The reward reads <code>Class: PAL</code>, <code>Race: ALL</code>, Lore Equipped, '
              'No Trade. The class restriction on the item itself has not changed.'),
         ],
         settle='The same run on a second epic with a different class gate would show whether '
                'this is the rule or one quest&rsquo;s wiring. A log of the final turn-in dialogue '
                'would raise this from a report to a measurement.',
         credit='Credited on the credits page. The same player raised the underwater '
                'weapon question above.'),

    dict(status='changed',
         q='Does killing a raid boss lock you out for the week?',
         classic='Classic EverQuest has no lockout at all. A boss has a spawn timer, and whoever '
                 'is standing there when it pops gets the kill.',
         legends='<strong>The lockout is per difficulty, not per boss.</strong> The patch notes '
                 'establish a weekly bonus-loot lockout resetting Tuesdays at 8AM PST, and that a '
                 'kill made while locked still returns one guaranteed drop from the boss&rsquo;s '
                 'unique table. What they do not say is that D0 through D4 each carry their own '
                 'lockout &mdash; so the same boss can be run once per tier.',
         note='That reframes a raid week. A first clear at D0 costs nothing at D1 and above, so '
              'there is no reason to open at a difficulty you are unsure of. <strong>The '
              'per-difficulty part is a player report, not a patch note</strong>, and the notes '
              'neither state it nor contradict it.',
         evidence=[
             ('T1', 'Patch notes, 23 June 2026',
              '&ldquo;you will only receive 1 piece of loot per named raid creature that has its '
              'own lockout. The raid bonus loot lockouts reset every Tuesday at 8AM PST.&rdquo;'),
             ('T1', 'Patch notes, 28 July 2026',
              '&ldquo;Killing a raid boss while you have a loot lockout will now give one '
              'guaranteed drop from that boss&rsquo;s unique treasure tables.&rdquo;'),
             # A NAMED THIRD PARTY KEEPS HER NAME.
             #
             # The depersonalisation pass replaced this with "a player report"
             # and deleted her two further observations. That is the opposite
             # error: the rule is that OUR characters do not appear, and
             # Annalise is not us. Stripping a contributor's credit to protect
             # someone else's privacy is misattribution, and she is credited by
             # name on the credits page for exactly these findings.
             ('Report', 'Annalise (AnnaWulf), 10 August 2026',
              '&ldquo;weekly lock out per difficulty and then daily lock out for 1 loot item till '
              'a tues reset&rdquo;. She also reports a D4 Lord Nagafen taking a long time even '
              'with a group, and D1 hit-point pools being a drag solo.'),
         ],
         settle='Kill one boss at D0, then open the same boss at D1 and check whether the full '
                'loot lockout applies or only the daily one.',
         credit='Per-difficulty behaviour reported by a player, 10 August 2026. Credited on the '
                'credits page.'),

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
              'ordinary trash types backstab while the same types cast Root, Screaming Terror and '
              'Shadow Vortex. Backstab is a rogue ability and a spell list is not, so that mob '
              'type carries two kits at D1, on trash.',
         evidence=[
             ('Tier M', 'Measured in play, Castle Mistmoore at Awakened',
              'Both trash types backstab, and both are logged casting.' + _BSDMG),
             ('T1', 'Zone line on entry',
              '<code>You have entered The Castle of Mistmoore 1 (Awakened).</code> The number and '
              'the name agree, and the modal loot drop of +1 agrees independently.'),
         ],
         settle='Settled for D1 and D2, and for the kits: <a href="difficulty.html">bosses measured '
                'at D3 and D4</a> carry every spell each cast, Cazic-Thule and Innoruuk '
                'among them. <strong>What is still pinned by nobody is D3 and D4 hit points</strong> '
                '&mdash; damage to kill bounds them from above and no further.',
         credit=''),

    dict(status='changed',
         q='Do named mobs still have placeholders?',
         classic='A named shares its spawn point with a placeholder. You kill the placeholder '
                 'repeatedly until the named appears, and published spawn percentages describe how '
                 'often it does.',
         legends='<strong>Gone in six dungeons, and this entry was wrong about the rest.</strong> The '
                 '28 July patch note names <strong>six</strong> &mdash; The Hole, Nagafen&rsquo;s Lair, '
                 'Lower Guk, Lair of the Splitpaw, The Warrens, Castle Mistmoore. It never mentions '
                 'Upper Guk. <strong>Najena keeps the claim</strong> on the 23 June revamp note, which is '
                 'no longer published anywhere a reader can reach. <strong>Befallen and Blackburrow keep '
                 'it</strong> on a dated eqlwiki category revision &mdash; tier 2, not a patch note. '
                 '<strong>Crushbone loses it outright</strong>: no source names it, and its percentages '
                 'are live again rather than struck. Plane of Fear, Plane of Hate and Kedge Keep were '
                 'never on the list and nothing is established for them.',
         note='We carried this as open while the patch note said it plainly the whole time. <strong>The lesson is about where we looked</strong>, not about the answer.',
         evidence=[
             ('T1', 'Developer patch notes',
              '&ldquo;Removed placeholders from and lowered maximum respawn times in several '
              'dungeons: The Hole, Nagafen&rsquo;s Lair, Lower Guk, Lair of the Splitpaw, The '
              'Warrens, Castle Mistmoore.&rdquo; <strong>That is the whole list.</strong> This '
              'register printed the same sentence with <em>Upper Guk, Crushbone, Befallen, '
              'Blackburrow, Najena</em> appended inside the quotation marks, badged T1, until '
              '18 August 2026 &mdash; when the note was fetched and stored verbatim at '
              '<code>sources/raw/2026-07-28-eql-update-notes.txt</code>. Five zone names had '
              'been added to a developer quotation.'),
             ('Report', 'First-hand play',
              'Confirmed in play across these zones before this site existed, and again at one '
              'camp across consecutive cycles with no placeholder seen.'),
             ('T5', 'eqlwiki individual mob pages, against',
              '<em>Drelzna</em>: &ldquo;Her placeholder is a necromancer that spawns in front of '
              'the chair.&rdquo; Classic text nobody has revisited. It is wrong.'),
         ],
         settle='Settled by the patch note for the six it names, and on weaker sources for three more. <strong>What it does not '
                'settle is the second half of its own sentence</strong> &mdash; maximum respawn '
                'times were lowered and no figures were published, so every respawn on this site '
                'is a pre-patch ceiling rather than a current value.',
         credit=''),

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
.st-entry{border:1px solid #40372D;border-left:3px solid var(--c);border-radius:4px;
  padding:20px 22px;margin:0 0 18px;background:var(--surface-2)}
.st-head{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;margin:0 0 14px}
.st-status{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--c-t);border:1px solid var(--c);border-radius:3px;
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
  rel="../", extra=CSS, og="learn", canon="learn/still-true") + bar("../") + f'''
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
