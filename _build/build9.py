"""Measured-in-play sections, from assets/measured.json onto the surveys.

Reads what logstats.py counted and writes a ZONE REFERENCE into the matching
plate, under the floor plan: which mobs cast what, which backstab, which stuns
land and what casts them, and what dropped.

WHAT THIS SECTION IS NOT ALLOWED TO PUBLISH. Not session counts, dates, windows
or hours played. Not character names, levels or trios. Not kill counts, swing
counts, hit rates, per-mob sighting counts or per-tier loot tallies. Not party
chat, not disconnections, not fights broken off. Every one of those is a fact
about one player's evening rather than about the zone, and the site is generic.

The TIER M badge on the heading already says the claim was verified in play. A
sentence whose only job is to prove the measurement happened is therefore
redundant, and it goes. What survives is the finding, stated without the count:
"stuns here arrive as spells, not as melee", never "882 shrugged off, 296
landed". The counts still drive the ordering and the selection; they just do not
reach the page.

Runs after build6.py, which has already injected the floor plan. Both write into
pages build3.py regenerates from _build/source every build, so neither
accumulates.

If assets/measured.json is missing or holds no session for a zone, that plate is
left exactly as it was. Nothing here is required for the site to build.
"""
import os, sys, json, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

ARTICLE = re.compile(r'^(?:a|an|the)\s+', re.I)


def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


# Normalising is not enough on its own: in play, Lower Guk is "The Ruins of Old
# Guk" and Upper Guk is "The City of Guk". Aliases are listed explicitly rather
# than guessed at by similarity, because a wrong match would attach one zone's
# measurements to another zone's plate, which is worse than no match at all.
# A zone with no plate — Upper Guk, Kerra Isle — is reported as unmatched, not
# silently dropped.
ALIASES = {
    'ruinsoldguk': 'lowerguk',
    'cityguk': 'upperguk',
    # The Hole's long name. 94 kills of measured data sat unattached to the
    # survey for it, reported as unmatched every build and read past.
    #
    # The right-hand side is the NORMALISED key, not the slug. They coincide for
    # Lower Guk and do not for The Hole, whose title normalises to 'hole' once
    # the article is stripped - so an alias written as 'thehole' matches nothing
    # and fails exactly like no alias at all.
    'ruinsoldpaineel': 'hole',
}

# A public group instance appends " - Group" to the zone name. It is the same
# zone, so it belongs on the same survey; the difficulty and the window already
# distinguish the sessions from each other.
GROUP_SUFFIX = re.compile(r'\s*-\s*group\s*$', re.I)


def key(name):
    """Zone names differ between the game and the site: 'The Castle of
    Mistmoore' against 'Castle Mistmoore'. Strip the articles and join up."""
    s = GROUP_SUFFIX.sub('', (name or ''))
    s = re.sub(r'\b(the|of|a|an)\b', ' ', s.lower())
    s = re.sub(r'[^a-z0-9]', '', s)
    return ALIASES.get(s, s)


CSS = """
<style>
.meas{margin:34px 0 10px}
.meas h2{font-family:"Saira Condensed",sans-serif;font-weight:600;text-transform:uppercase;
  letter-spacing:.02em;font-size:clamp(21px,3.4vw,28px);margin:0 0 8px}
.meas .cond{border-left:2px solid var(--accd);background:#201A15;padding:12px 16px;
  margin:0 0 18px;color:var(--mut);font-size:14px}
.meas .cond b{color:var(--bone)}
.meas .tw{overflow-x:auto;margin:0 0 14px;-webkit-overflow-scrolling:touch}
.meas table{width:100%;min-width:520px;border-collapse:collapse;font-size:14px}
.meas th{text-align:left;font-family:"IBM Plex Mono",monospace;font-size:10.5px;
  letter-spacing:.14em;text-transform:uppercase;color:#B6ABA1;font-weight:500;
  border-bottom:1px solid #40372D;padding:0 12px 7px 0}
.meas td{border-bottom:1px solid #322A23;padding:9px 12px 9px 0;vertical-align:top}
.meas td.n{font-family:"IBM Plex Mono",monospace;white-space:nowrap;color:#D3CFCB}
.meas .mob{color:var(--bone);font-weight:600}
.meas .sub{display:block;color:#9C958E;font-size:12.5px;margin-top:3px}
.meas .caveat{color:var(--faint);font-size:13.5px;margin:0;max-width:80ch}
.tierM{display:inline-block;font-family:"IBM Plex Mono",monospace;font-size:10px;
  letter-spacing:.1em;padding:1px 5px;border:1px solid var(--accd);border-radius:3px;
  color:var(--acct);vertical-align:2px}
@media(max-width:760px){.meas .tw{overflow-x:visible}
  .meas table{min-width:0}
  .meas table,.meas thead,.meas tbody,.meas tr,.meas td,.meas th{display:block}
  .meas thead{display:none}.meas td{border:0;padding:2px 0}
  .meas tr{border-bottom:1px solid #322A23;padding:10px 0;display:block}}
</style>"""


H3 = ('<h3 style="font-family:\'Saira Condensed\',sans-serif;text-transform:uppercase;'
      'font-size:17px;letter-spacing:.04em;margin:18px 0 8px">{}</h3>')


def control_html(s):
    """What takes control away from you, and what casts it.

    The most actionable thing in a zone, and it took a death to find. Read from
    what the log says happened rather than from what a spell is assumed to be:
    Screaming Terror was taken for a fear spell and produced no fear behaviour
    at all, only a scream and a lockout.

    The counts order the table and are not printed. How often a spell landed is
    a fact about how long one player stood in front of it; WHICH spells stun and
    WHAT casts them is a fact about the zone.
    """
    c = s.get('control') or {}
    stuns = c.get('stuns') or {}
    if not stuns:
        return ''
    ranked = sorted(stuns.items(), key=lambda kv: -kv[1]['landed'])
    rows = ''.join(
        f'<tr><td><span class="mob">{esc(sp)}</span></td>'
        f'<td>{esc(", ".join(list(d["casters"])[:6])) or "&mdash;"}</td></tr>'
        for sp, d in ranked)
    # The melee/spell contrast only holds where stunning melee attacks were in
    # fact shrugged off. Without that half there is no gap to point at, so the
    # sentence weakens rather than asserting something the data does not show.
    if c.get('melee_stuns_avoided'):
        lead = ('<b>Stuns here arrive as spells, not as melee.</b> Stunning melee attacks were '
                'shrugged off and the spells landed anyway, so an immunity to stunning '
                '<em>melee</em> attacks does nothing about them.')
    else:
        lead = '<b>These are the spells that take a turn away from you here.</b>'
    if c.get('screams'):
        lead += ' Screaming Terror locks you out of acting.'
        if c.get('fear_lines') == 0:
            lead += (' It produces <b>no fear behaviour whatsoever</b> &mdash; no fleeing, nothing '
                     'that behaves like fear &mdash; so despite the name it reads as a stun, and '
                     'fear protection does not appear to touch it.')
    return (H3.format('What takes control away')
            + f'<div class="cond">{lead}</div>'
            f'<div class="tw"><table><thead><tr><th>Spell</th><th>Cast by</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>'
            f'<p class="caveat" style="margin:0 0 18px"><b>Read this as a kill order.</b> '
            f'Whatever casts the spell at the top takes your turn away most often. '
            f'<a href="../learn/reading-the-plans.html#measured">Why it is not a property of the mob &rarr;</a></p>')


def merge(sessions):
    """Combine sessions of the same zone and difficulty into one measurement.

    Taking the largest and discarding the rest threw away 127 kills and three
    named mobs measured nowhere else, because one afternoon in Mistmoore was cut
    into two sessions by a zone line. Sessions are only ever merged when zone
    and difficulty match, so nothing measured under different conditions is
    averaged together.
    """
    if len(sessions) == 1:
        return sessions[0]
    out = dict(sessions[0])
    # Sessions can span days, and the merged figures are the sum. None of the
    # dates, windows or per-session totals reach the page — they select and
    # order, nothing more — so the span needs no caveat any more: the page never
    # claims a period in the first place.
    out['kills'] = sum(s['kills'] for s in sessions)
    out['sessions_merged'] = len(sessions)

    for key in ('drop_tiers', 'faction'):
        c = collections.Counter()
        for s in sessions:
            c.update(s.get(key) or {})
        out[key] = dict(c.most_common()) if key == 'faction' else dict(sorted(c.items()))

    # ONE MOB TYPE, ONE ROW, WHATEVER CASE THE LOG WROTE IT IN.
    #
    # The parser records a mob under the capitalisation of the line it came
    # from: "A deathly usher backstabs YOU" and "You have slain a deathly
    # usher" are the same creature and were becoming two rows. Across the
    # Castle Mistmoore sessions that turned 66 real types into 121, and the
    # measured section published "113 ordinary mob types" for a zone holding
    # about 58 — a count nobody typed, derived from data that had been split
    # in half.
    #
    # Keyed on the lower-case name; the display name is whichever form the log
    # used first, so nothing invents a capitalisation the game does not use.
    mobs, shown = {}, {}
    for s in sessions:
        for raw, d in s['mobs'].items():
            name = raw.lower()
            shown.setdefault(name, raw)
            m = mobs.setdefault(name, dict(swings=0, landed=0, avg=None, max=None,
                                           backstabs=0, backstab_avg=None, backstab_max=None,
                                           casts=collections.Counter(), loot=collections.Counter(),
                                           _dmg=0.0, _bdmg=0.0))
            m['swings'] += d.get('swings') or 0
            if d.get('avg') is not None:
                m['_dmg'] += d['avg'] * (d.get('landed') or 0)
                m['max'] = max(m['max'] or 0, d.get('max') or 0)
            m['landed'] += d.get('landed') or 0
            if d.get('backstabs'):
                m['_bdmg'] += (d.get('backstab_avg') or 0) * d['backstabs']
                m['backstabs'] += d['backstabs']
                m['backstab_max'] = max(m['backstab_max'] or 0, d.get('backstab_max') or 0)
            m['casts'].update(d.get('casts') or {})
            m['loot'].update(d.get('loot') or {})
    for m in mobs.values():
        m['avg'] = round(m['_dmg'] / m['landed'], 1) if m['landed'] else None
        m['backstab_avg'] = round(m['_bdmg'] / m['backstabs'], 1) if m['backstabs'] else None
        m['casts'] = dict(m['casts'].most_common())
        m['loot'] = dict(m['loot'].most_common())
        del m['_dmg'], m['_bdmg']
    # Back to the log's own capitalisation for display.
    out['mobs'] = {shown[k]: v for k, v in mobs.items()}
    # Unique names, not the sum of per-session counts: the same gargoyle type
    # appearing in both halves of an afternoon is one kind of mob, not two.
    kinds = {k for s in sessions for k in (s.get('kinds') or [])}
    out['kinds'] = sorted(kinds)
    out['distinct'] = len(kinds) or max(s['distinct'] for s in sessions)

    ctl = dict(sessions[0].get('control') or {})
    if ctl:
        for k in ('melee_stuns_avoided', 'lockout_lines', 'fear_lines', 'screams', 'scream_seconds'):
            ctl[k] = sum((s.get('control') or {}).get(k, 0) for s in sessions)
        stuns = {}
        for s in sessions:
            for sp, d in ((s.get('control') or {}).get('stuns') or {}).items():
                e = stuns.setdefault(sp, dict(landed=0, casters=collections.Counter()))
                e['landed'] += d['landed']
                e['casters'].update(d.get('casters') or {})
        ctl['stuns'] = {k: dict(landed=v['landed'], casters=dict(v['casters'].most_common()))
                        for k, v in sorted(stuns.items(), key=lambda kv: -kv[1]['landed'])}
        out['control'] = ctl
    return out


def revamp_html(note):
    """A dated line saying the measurement predates a zone revamp.

    WHY THIS IS NOT OPTIONAL
    ------------------------
    A measured figure is a fact about the zone AS IT WAS. When the zone changes,
    every figure in this section keeps its provenance and loses its currency at
    the same instant, and nothing in the data knows that happened. Castle
    Mistmoore was revamped on 18 August 2026 and this survey publishes a
    thousand kills recorded before it: someone who farmed the new version this
    morning can contradict the flagship page in one message.

    The evidence is not withdrawn, because it is not wrong - it is dated. It
    says which side of the revamp it sits on and lets the reader decide.

    Read from `revamped_note` in assets/zones-index.json rather than written
    here, so a second revamped zone needs a data edit and no code.
    """
    if not note:
        return ''
    return ('<b class="revamp">' + note + '</b> ')


def section(sess_list, zone_title, revamp=None):
    # Merge only what was observed under the same conditions: same difficulty,
    # and the same vantage point. A healer's view of a fight and a tank's are
    # different fights, and averaging them would describe neither.
    best = max(sess_list, key=lambda z: z['kills'])
    same = [z for z in sess_list
            if z.get('difficulty') == best.get('difficulty')
            and z.get('character') == best.get('character')]
    s = merge(sorted(same, key=lambda z: (z['date'], z['window'])))

    # Runs at other difficulties are not merged in and are not listed either.
    # The line that listed them was a per-run kill tally, which is the diary
    # this section no longer keeps; what it protected against — a silent loss —
    # is covered by the heading, which now states the difficulty these
    # observations belong to instead of implying they cover the zone entire.

    named, trash = [], []
    for name, d in s['mobs'].items():
        (trash if ARTICLE.match(name) else named).append((name, d))
    # Alphabetical. Ordering by how often a mob swung at us ranked the table by
    # where one player happened to stand; a reference sorts by name.
    named.sort(key=lambda kv: kv[0].lower())

    def rows(items):
        out = []
        for name, d in items:
            if not d['swings'] and not d['casts'] and not d['loot']:
                continue
            # Damage is the mob's, so it stays. Swings and landing rates are the
            # player's afternoon, so they do not. A backstabber never gets a
            # combined average — the two numbers describe two different attacks.
            dmg = (f"{d['avg']:g} avg &middot; {d['max']} max" if d['avg'] is not None
                   else 'not measured')
            if d.get('backstabs'):
                dmg += (f'<span class="sub">backstab {d["backstab_avg"]:g} avg &middot; '
                        f'{d["backstab_max"]} max</span>')
            casts = ', '.join(f'{esc(k)}' for k in list(d['casts'])[:6]) or '&mdash;'
            loot = ', '.join(esc(k) for k in list(d['loot'])[:6]) or '&mdash;'
            out.append(
                f'<tr><td><span class="mob">{esc(name)}</span>'
                f'<span class="sub">{"casts: " + casts if d["casts"] else "no casts seen"}</span></td>'
                f'<td class="n">{dmg}</td><td>{loot}</td></tr>')
        return ''.join(out)

    hdr = '<tr><th>Mob</th><th>Damage dealt</th><th>Dropped</th></tr>'
    tables = ''
    if named:
        tables += (H3.format('Named')
                   + f'<div class="tw"><table><thead>{hdr}</thead>'
                   f'<tbody>{rows(named)}</tbody></table></div>')
    if trash:
        # Ordinary mobs are not itemised: sixty rows of "a dark elf noble" was
        # the largest block on any survey and nobody plans a run around it. The
        # one thing worth carrying out is which of them backstab, because a
        # backstabber hits several times harder from behind and the ordinary
        # ones doing it is the finding this site holds and others do not.
        bs = sorted(n for n, d in trash if d.get('backstabs'))
        line = 'Ordinary mobs are not itemised here.'
        if bs:
            # The log's own capitalisation is right at the head of a row and
            # wrong in the middle of a sentence: "A gypsy musician" mid-clause
            # reads as a new sentence starting. Only the leading article moves.
            shown = ', '.join(f'<b>{esc(n[0].lower() + n[1:] if ARTICLE.match(n) else n)}</b>'
                              for n in bs[:8])
            # "runs far above their melee" was the first draft and one mob broke
            # it: a forsaken revenant's biggest backstab is smaller than its
            # biggest swing. The average holds for every backstabber measured,
            # so the average is what the sentence claims.
            line += (f' These ordinary mobs backstab: {shown}'
                     + (', among others.' if len(bs) > 8 else '.')
                     + ' Backstab is a rogue ability, so ordinary mobs here carry class kits. '
                       'A backstab averages more damage than the same mob&rsquo;s melee.')
        tables += f'<p class="trash">{line}</p>'

    tk = sorted(int(k) for k in (s.get('drop_tiers') or {}))
    if not tk:
        tiers = 'No upgradeable drops recorded here.'
    elif len(tk) == 1:
        tiers = f'Upgradeable drops here came in at +{tk[0]}.'
    else:
        tiers = f'Upgradeable drops here ran +{tk[0]} to +{tk[-1]}.'
    facs = ', '.join(esc(f) for f in list(s['faction'])[:8])
    facs = f' Killing here moves faction with {facs}.' if facs else ''
    d, lab = s.get('difficulty'), s.get('difficulty_label')
    if lab and d is not None:
        diff = f'D{d}, {esc(lab)}'
    elif lab:
        diff = esc(lab)
    elif d is not None:
        diff = f'D{d}, read from the loot tier rather than the zone line'
    else:
        diff = 'not stated'
    if s.get('difficulty_agrees') is False:
        diff += (' &mdash; <b>but the zone name and the loot tier disagree</b>, '
                 'so treat the difficulty as unresolved')

    return (
        f'<section class="meas" id="measured">'
        f'<h2>Measured in play <span class="tierM">TIER M</span></h2>'
        f'<div class="cond">'
        f'<b>{esc(zone_title)}, run at {diff}.</b> '
        f'Everything below was observed in the live game rather than read from a '
        f'source: what these mobs cast, what they hit for, and what they dropped. '
        f'{tiers}{facs}{revamp_html(revamp)}'
        f'</div>{control_html(s)}{tables}'
        f'<p class="caveat"><strong>What this is and is not.</strong> Observations, not '
        f'rates. A drop seen once is not a drop rate, and nothing here is a probability. '
        f'Damage is what the mob dealt against the armour it met, so treat the maximum as '
        f'the shape of the hit rather than a constant. '
        f'<a href="../learn/reading-the-plans.html#measured">What a log can and cannot tell you &rarr;</a></p>'
        f'</section>')


def main():
    try:
        sessions = json.load(open('assets/measured.json', encoding='utf-8'))
    except (OSError, ValueError):
        print('measured sections: no assets/measured.json, skipped')
        return
    zones = json.load(open('assets/zones-index.json', encoding='utf-8'))
    by_key = {key(z['title']): z for z in zones}

    grouped = collections.defaultdict(list)
    for s in sessions:
        z = by_key.get(key(s['zone']))
        if z and (s['kills'] or s['mobs']):
            grouped[z['slug']].append(s)

    done = 0
    for slug, lst in grouped.items():
        path = f'public/dungeons/{slug}.html'
        if not os.path.exists(path):
            continue
        h = open(path, encoding='utf-8').read()
        # RUNNING THIS TWICE MUST NOT PUBLISH THE SECTION TWICE.
        #
        # Injection is append-only and relies on build3.py having regenerated
        # the page first, which is true inside build.sh and not true of anyone
        # running this file on its own. A second copy is not merely untidy: the
        # prose ceiling exempts the measured table rows only inside the FIRST
        # measured section, so the duplicate's rows all count as prose and four
        # surveys blow their ceilings at once. Strip any previous copy first.
        h = re.sub(r'<section class="meas" id="measured">.*?</section>', '', h, flags=re.S)
        h = h.replace(CSS, '')
        _z = by_key[key(next(x['zone'] for x in lst))]
        block = section(lst, _z['title'], _z.get('revamped_note'))
        if '</main>' in h:
            h = h.replace('</main>', block + '</main>', 1)
        elif '</body>' in h:
            h = h.replace('</body>', block + '</body>', 1)
        else:
            continue
        h = h.replace('</head>', CSS + '</head>', 1)
        open(path, 'w', encoding='utf-8', newline='\n').write(h)
        done += 1
    unmatched = {s['zone'] for s in sessions
                 if s['zone'] and key(s['zone']) not in by_key}
    print(f'measured sections: {done} plate(s) updated from {len(sessions)} session(s)'
          + (f'; no plate for {sorted(unmatched)}' if unmatched else ''))


if __name__ == '__main__':
    main()
