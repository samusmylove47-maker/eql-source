"""Measured-in-play sections, from assets/measured.json onto the plates.

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


def key(name):
    """Zone names differ between the game and the site: 'The Castle of
    Mistmoore' against 'Castle Mistmoore'. Strip the articles and join up."""
    s = re.sub(r'\b(the|of|a|an)\b', ' ', (name or '').lower())
    return re.sub(r'[^a-z0-9]', '', s)


CSS = """
<style>
.meas{margin:34px 0 10px}
.meas h2{font-family:"Saira Condensed",sans-serif;font-weight:600;text-transform:uppercase;
  letter-spacing:.02em;font-size:clamp(21px,3.4vw,28px);margin:0 0 8px}
.meas .cond{border-left:2px solid var(--accd);background:#161C21;padding:12px 16px;
  margin:0 0 18px;color:#AEB9B8;font-size:14px}
.meas .cond b{color:#E6E9E4}
.meas table{width:100%;border-collapse:collapse;margin:0 0 14px;font-size:14px}
.meas th{text-align:left;font-family:"IBM Plex Mono",monospace;font-size:10.5px;
  letter-spacing:.14em;text-transform:uppercase;color:#7D9096;font-weight:500;
  border-bottom:1px solid #2E3A41;padding:0 12px 7px 0}
.meas td{border-bottom:1px solid #232D32;padding:9px 12px 9px 0;vertical-align:top}
.meas td.n{font-family:"IBM Plex Mono",monospace;white-space:nowrap;color:#C9D1CF}
.meas .mob{color:#E6E9E4;font-weight:600}
.meas .sub{display:block;color:#8A9998;font-size:12.5px;margin-top:3px}
.meas .caveat{color:#7D9096;font-size:13.5px;margin:0;max-width:80ch}
.tierM{display:inline-block;font-family:"IBM Plex Mono",monospace;font-size:10px;
  letter-spacing:.1em;padding:1px 5px;border:1px solid var(--accd);border-radius:3px;
  color:var(--acct);vertical-align:2px}
@media(max-width:640px){.meas table,.meas thead,.meas tbody,.meas tr,.meas td,.meas th{display:block}
  .meas thead{display:none}.meas td{border:0;padding:2px 0}
  .meas tr{border-bottom:1px solid #232D32;padding:10px 0;display:block}}
</style>"""


def section(sess_list, zone_title):
    s = max(sess_list, key=lambda z: z['kills'])          # the fullest session
    stamps = s.get('context') or s['stamps']
    who = next((x for x in stamps if re.search(r'\b(BRD|WAR|CLR|SHM|NEC|DRU|ROG|MNK|BER|PAL|SHD|RNG|WIZ|MAG|ENC|BST)\b', x)), None)
    notes = [x for x in s['stamps'] if x is not who]

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
                   f'<table><thead>{hdr}</thead><tbody>{rows(named)}</tbody></table>')
    if trash:
        tables += (f'<h3 style="font-family:\'Saira Condensed\',sans-serif;text-transform:uppercase;'
                   f'font-size:17px;letter-spacing:.04em;margin:18px 0 8px">Everything else</h3>'
                   f'<table><thead>{hdr}</thead><tbody>{rows(trash)}</tbody></table>')

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
        f'<section class="meas">'
        f'<h2>Measured in play <span class="tierM">TIER M</span></h2>'
        f'<div class="cond">'
        f'<b>One session, {esc(s["date"])}, {esc(s["window"])}.</b> '
        f'{"<b>" + esc(who) + "</b> " if who else ""}'
        f'Zone entered as <b>{esc(zone_title)} ({diff})</b>. '
        f'{s["kills"]} kills across {s["distinct"]} kinds of mob; our own swings landed '
        f'<b>{hitrate}</b> of the time ({yh + ym} attempts). Drops seen: {tiers}. '
        f'Faction moved: {facs}.'
        + (''.join(f'<br><b>Noted at the time:</b> {esc(n)}' for n in notes) if notes else '')
        + f'</div>{tables}'
        f'<p class="caveat"><strong>What this is and is not.</strong> These are counts from one '
        f'session, not rates. A drop listed here was seen at least once and nothing more &mdash; no '
        f'drop rate can be read from it. Damage and landing figures describe this trio, at this '
        f'level, against these mobs, on this date; a different level or trio changes all of them. '
        f'Mobs that never attacked us and never cast anything are absent, because a log records what '
        f'happened rather than what was there. Spell names are as the game printed them.</p>'
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
        path = f'dungeons/{slug}.html'
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
