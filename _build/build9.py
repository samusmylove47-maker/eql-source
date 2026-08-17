"""Measured-in-play sections, from assets/measured.json onto the surveys.

Reads what logstats.py counted and writes it into the matching plate, under the
floor plan. Nothing here interprets: it prints what was measured with the
conditions attached, because a figure from one session is a fact about that
session and not a property of the zone.

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


def escapes_html(s):
    """Fights the group broke off.

    A wiki records what a mob is. It does not record the moment a group decided
    a fight was lost, which is the judgement a reader actually wants, and a
    combat log is the only place it exists. Printed with what was engaged and
    what had just been cast, and with no claim that the fight is unwinnable —
    only that this group, at this level, chose to leave it.
    """
    esc_list = s.get('escapes') or []
    if not esc_list:
        return ''
    items = ''.join(
        f'<li><b>{esc(e["at"])}</b> &mdash; {esc(e["by"])} took the group out'
        + (f', with <b>{esc(", ".join(e["engaged"]))}</b> engaged' if e.get('engaged') else '')
        + (f'. Last thing cast before the call: <b>{esc(e["after"])}</b>' if e.get('after') else '')
        + '.</li>'
        for e in esc_list)
    # An escape is only a judgement about a fight if the group was in a position
    # to judge. Where the session carries a stated caveat — a client crashing,
    # for one — that has to appear beside the list rather than under it, because
    # "the group chose to leave" is exactly the wrong reading of a crash.
    warn = ''
    if s.get('caveat'):
        warn = (f'<div class="cond" style="border-left-color:var(--acct)">'
                f'<b>Read these against the conditions.</b> {esc(s["caveat"])}</div>')

    return (f'<h3 style="font-family:\'Saira Condensed\',sans-serif;text-transform:uppercase;'
            f'font-size:17px;letter-spacing:.04em;margin:18px 0 8px">Fights broken off</h3>'
            + warn
            + f'<ul style="margin:0 0 16px;padding-left:20px;color:var(--mut);font-size:14px;'
            f'line-height:1.7">{items}</ul>'
            f'<p class="caveat" style="margin:0 0 18px">An escape is a judgement, not a verdict. '
            f'It records that this group at this level chose to leave, which is worth knowing and is '
            f'written down nowhere else &mdash; but it is not evidence the fight cannot be won, and '
            f'the number of mobs engaged is usually the reason rather than the named itself.</p>')


def control_html(s):
    """What takes control away from you, and what cast it.

    The most actionable thing in a log, and it took a death to find. Counted by
    what the log says happened rather than by what a spell is assumed to be:
    Screaming Terror was taken for a fear spell and produced no fear behaviour
    at all, only a scream and a lockout.
    """
    c = s.get('control') or {}
    stuns = c.get('stuns') or {}
    if not stuns and not c.get('melee_stuns_avoided'):
        return ''
    rows = ''.join(
        f'<tr><td><span class="mob">{esc(sp)}</span></td>'
        f'<td class="n">{d["landed"]}</td>'
        f'<td>{esc(", ".join(f"{k} ({v})" for k, v in list(d["casters"].items())[:6])) or "&mdash;"}</td></tr>'
        for sp, d in stuns.items())
    total = sum(d['landed'] for d in stuns.values())
    lead = (f'<b>{c.get("melee_stuns_avoided", 0)}</b> stunning melee attacks were shrugged off, '
            f'and <b>{total}</b> stuns landed anyway &mdash; <b>every one of them from a spell</b>. '
            f'That gap is the point: an immunity to stunning <em>melee</em> attacks does nothing '
            f'about a spell, and the character being measured carried exactly that immunity.')
    if c.get('screams'):
        lead += (f' Screaming Terror landed {c["screams"]} times for '
                 f'<b>{c["scream_seconds"]} seconds</b> of being unable to act.')
    if c.get('fear_lines') == 0 and c.get('screams'):
        lead += (' It produced <b>no fear behaviour whatsoever</b> &mdash; no fleeing, nothing '
                 'the log calls fear &mdash; so despite the name it reads as a stun, and '
                 'fear protection does not appear to touch it.')
    return (f'<h3 style="font-family:\'Saira Condensed\',sans-serif;text-transform:uppercase;'
            f'font-size:17px;letter-spacing:.04em;margin:18px 0 8px">What takes control away</h3>'
            f'<div class="cond">{lead}</div>'
            f'<div class="tw"><table><thead><tr><th>Spell</th><th>Stuns landed</th><th>Cast by</th></tr></thead>'
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
    # Sessions can span days. Shara's Befallen runs at D1 cover 4, 6 and 7
    # August, and the character's level may well have moved between them, which
    # changes every hit rate in the table. They are still merged — the samples
    # are small individually — but the span is stated and the page carries a
    # caveat rather than presenting three days as one afternoon.
    dates = sorted({s['date'] for s in sessions})
    out['days'] = len(dates)
    out['date'] = dates[0] if len(dates) == 1 else f"{dates[0]} to {dates[-1]}"
    out['window'] = (f"{sessions[0]['window'].split('-')[0]}-{sessions[-1]['window'].split('-')[-1]}"
                     if len(dates) == 1 else f"{len(sessions)} sittings")
    out['kills'] = sum(s['kills'] for s in sessions)
    out['you_hit'] = sum(s['you_hit'] for s in sessions)
    out['you_miss'] = sum(s['you_miss'] for s in sessions)
    out['sessions_merged'] = len(sessions)

    for key in ('drop_tiers', 'faction'):
        c = collections.Counter()
        for s in sessions:
            c.update(s.get(key) or {})
        out[key] = dict(c.most_common()) if key == 'faction' else dict(sorted(c.items()))

    out['stamps'] = [x for s in sessions for x in s.get('stamps', [])]
    out['escapes'] = [x for s in sessions for x in s.get('escapes', [])]

    # A caveat on any merged part applies to the whole, because the merged
    # figures include it. Dropping it here is how a warning recorded against
    # the afternoon sessions failed to reach the page that averages them in.
    cav = [s['caveat'] for s in sessions if s.get('caveat')]
    if cav:
        out['caveat'] = cav[0]

    mobs = {}
    for s in sessions:
        for name, d in s['mobs'].items():
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
    out['mobs'] = mobs
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


def section(sess_list, zone_title):
    # Merge only what was measured under the same conditions: same difficulty
    # and the same character. A healer's log and a tank's describe different
    # fights from different sides, and averaging them would describe neither.
    best = max(sess_list, key=lambda z: z['kills'])
    same = [z for z in sess_list
            if z.get('difficulty') == best.get('difficulty')
            and z.get('character') == best.get('character')]
    s = merge(sorted(same, key=lambda z: (z['date'], z['window'])))

    # NAME WHAT IS MEASURED AND NOT SHOWN.
    # Only the largest group renders, so a zone logged at two difficulties
    # published one and dropped the other in silence - The Hole had 70 kills at
    # Base, two named mobs and their drops among them, that no page mentioned.
    # Rendering every group would repeat this whole section's framing per block.
    # Naming the remainder costs a sentence and turns a silent loss into a
    # stated one, which is the rule everywhere else on this site.
    rest = collections.Counter()
    for z in sess_list:
        if z in same or not z['kills']:
            continue
        rest[(z.get('difficulty'), z.get('character'))] += z['kills']
    also = ''
    if rest:
        # Capped at three. Unbounded, this line grows every time the zone is
        # played again - it reached six entries on Nagafen's Lair and pushed
        # the page through its prose ceiling, which would have meant raising
        # the ceiling every session forever. The total is still stated.
        ranked = sorted(rest.items(), key=lambda kv: -kv[1])
        bits = ', '.join(
            f'{n} at D{d}' + (f' from {esc(c)}&rsquo;s log' if c != s.get('character') else '')
            for (d, c), n in ranked[:3])
        extra = sum(n for _k, n in ranked[3:])
        if extra:
            bits += f', and {extra} more across {len(ranked) - 3} other runs'
        also = (f' <b>Also measured here and not shown below:</b> {bits}. '
                f'Conditions differ, so those kills are not averaged into these figures.')
    # Stamps used to be bare strings and are now {at, text, conditions}; accept
    # either so an older measured.json still renders.
    def txt(v):
        return v['text'] if isinstance(v, dict) else v

    CLASSES = r'\b(BRD|WAR|CLR|SHM|NEC|DRU|ROG|MNK|BER|PAL|SHD|RNG|WIZ|MAG|ENC|BST)\b'
    stamps = s.get('context') or s['stamps']
    who = next((txt(x) for x in stamps if re.search(CLASSES, txt(x))), None)
    # Only stamps that state a condition reach the page. The rest is party chat:
    # "I will provide her logs separate later" was being republished as though
    # it described the fight.
    notes = [(txt(x), x.get('at') if isinstance(x, dict) else None, True)
             for x in s['stamps']
             if txt(x) != who and isinstance(x, dict) and x.get('conditions')]

    named, trash = [], []
    for name, d in s['mobs'].items():
        (trash if ARTICLE.match(name) else named).append((name, d))
    named.sort(key=lambda kv: -(kv[1]['swings'] or 0))
    trash.sort(key=lambda kv: -(kv[1]['swings'] or 0))

    def rows(items):
        out = []
        for name, d in items:
            if not d['swings'] and not d['casts'] and not d['loot']:
                continue
            land = f"{100*d['landed']/d['swings']:.0f}%" if d['swings'] else '&mdash;'
            dmg = (f"{d['avg']:g} avg &middot; {d['max']} max" if d['avg'] is not None
                   else 'not measured')
            if d.get('backstabs'):
                dmg += (f'<span class="sub">backstab {d["backstab_avg"]:g} avg &middot; '
                        f'{d["backstab_max"]} max, seen {d["backstabs"]}&times;</span>')
            casts = ', '.join(f'{esc(k)}' for k in list(d['casts'])[:6]) or '&mdash;'
            loot = ', '.join(esc(k) for k in list(d['loot'])[:6]) or '&mdash;'
            out.append(
                f'<tr><td><span class="mob">{esc(name)}</span>'
                f'<span class="sub">{"seen casting: " + casts if d["casts"] else "no casts logged"}</span></td>'
                f'<td class="n">{d["swings"] or "&mdash;"}</td><td class="n">{land}</td>'
                f'<td class="n">{dmg}</td><td>{loot}</td></tr>')
        return ''.join(out)

    hdr = ('<tr><th>Mob</th><th>Swings at us</th><th>Landed</th>'
           '<th>Damage</th><th>Dropped</th></tr>')
    tables = ''
    if named:
        tables += (f'<h3 style="font-family:\'Saira Condensed\',sans-serif;text-transform:uppercase;'
                   f'font-size:17px;letter-spacing:.04em;margin:18px 0 8px">Named</h3>'
                   f'<div class="tw"><table><thead>{hdr}</thead><tbody>{rows(named)}</tbody></table></div>')
    if trash:
        tsw = sum(d['swings'] or 0 for _n, d in trash)
        tld = sum(d['landed'] or 0 for _n, d in trash)
        rate = f'{100*tld/tsw:.0f}%' if tsw else 'not measured'
        # Ordinary mobs stop being itemised here. Sixty rows of "a dark elf
        # noble" was the largest block on a measured section, and nobody plans
        # an evening around trash damage averages. The aggregate keeps the scale.
        tables += (f'<p class="trash">Plus <b>{len(trash)}</b> ordinary mob types over '
                   f'<b>{tsw:,}</b> swings, landing {rate}. Not itemised.</p>')

    yh, ym = s['you_hit'], s['you_miss']
    hitrate = f"{100*yh/(yh+ym):.1f}%" if (yh + ym) else 'not measured'
    tiers = ', '.join(f'+{k} &times;{v}' for k, v in s['drop_tiers'].items()) or 'none recorded'
    facs = ', '.join(esc(f) for f in list(s['faction'])[:8]) or 'none recorded'
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
        f'<b>{("One session" if s.get("sessions_merged", 1) < 2 else str(s["sessions_merged"]) + " sessions")}, '
        f'{esc(s["date"])}, {esc(s["window"])}.</b> '
        + f'Measured from <b>{esc(s.get("character") or "an unnamed character")}</b>&rsquo;s log. '
        + (f'<b>Measured across {s["days"]} days</b>, so the character&rsquo;s level may have '
           f'changed within the span &mdash; treat the landing rates as an average over that '
           f'range rather than a figure for one level. ' if s.get('days', 1) > 1 else '')
        # A stamp is party chat, so it reaches everyone's log. Shara's Befallen
        # runs carried "Avenrae BRD WAR BER" and were printing it as though it
        # described the character whose log this is. It only describes the
        # subject when it names them.
        + (f'<b>{esc(who)}</b> ' if who and s.get('character')
           and who.lower().startswith(str(s['character']).lower())
           else (f'Party context noted in chat at the time: <em>{esc(who)}</em> ' if who else ''))
        + f'Zone entered as <b>{esc(zone_title)} ({diff})</b>. '
        + f'{s["kills"]} kills across {s["distinct"]} kinds of mob; our own swings landed '
        + f'<b>{hitrate}</b> of the time ({yh + ym} attempts). Drops seen: {tiers}. '
        + f'Faction moved: {facs}.{also}'
        + (''.join(
            f'<br><b>{"Conditions changed at" if c else "Noted at"} {esc(at)}:</b> {esc(n)}'
            if at else f'<br><b>Noted at the time:</b> {esc(n)}'
            for n, at, c in notes) if notes else '')
        + f'</div>{control_html(s)}{escapes_html(s)}{tables}'
        # "counts from one session" was typed, so a page merging three sessions
        # printed "3 sessions" in its header and "one session" in its caveat.
        # The same fault the propagation gate exists for, in a sentence about
        # not over-reading evidence.
        f'<p class="caveat"><strong>What this is and is not.</strong> These are counts'
        f'{" from one session" if s.get("sessions_merged", 1) < 2 else ""}, not rates. '
        f'A drop seen once is seen once, and figures describe this '
        f'trio at this level on this date. '
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
        block = section(lst, by_key[key(next(x['zone'] for x in lst))]['title'])
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
