"""Faction data out of the race-unlock tool, plus what our own logs measured.

WHY THIS IS WORTH BUILDING
--------------------------
Faction is a real and constant EverQuest problem and nobody has built a tool for
it. Grinding a zone quietly wrecks unlocks you have not started yet, and you
find out hours later when a vendor will not speak to you.

Two halves, from two very different sources:

- WHAT A FACTION IS FOR. Mined from _build/source/eql-race-unlocks.html, where
  the race unlock work already recorded which factions each race needs and which
  quest steps raise them. Tier 3, from Alanna's guide.

- WHAT MOVES IT. Measured from our own combat logs by logstats.py. Killing in
  Castle Mistmoore moves five factions at once, and the size depends on the mob
  rather than its rank: Xicotl is -300 to Mayong Mistmoore where trash is -5,
  while Enynti — also named — is -5 like anything else.

The second half is the part no wiki has, and it is what makes the tool worth
using rather than a table anyone could copy.

Writes assets/faction-data.json. Run by build.sh; the measured half is skipped
cleanly when assets/measured.json is absent.
"""
import os, re, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SRC = '_build/source/eql-race-unlocks.html'

# "Dreadguard Inner +5 · Dark Bargainers +10 — per 4 wings" -> [(name, delta)]
GAIN = re.compile(r'([A-Za-z][A-Za-z\' `]*?)\s*([+-]\d+)')


def block(text, start):
    """The balanced {...} beginning at or after `start`."""
    i = text.index('{', start)
    depth = 0
    for j in range(i, len(text)):
        if text[j] in '{[':
            depth += 1
        elif text[j] in '}]':
            depth -= 1
            if depth == 0:
                return text[i:j + 1]
    return ''


def entries(obj_text):
    """Split a JS object literal into its top-level key: {...} members."""
    out, i = {}, 1
    while i < len(obj_text):
        m = re.compile(r'([A-Za-z_][\w]*)\s*:\s*\{').search(obj_text, i)
        if not m:
            break
        b = block(obj_text, m.end() - 1)
        out[m.group(1)] = b
        i = m.end() - 1 + len(b)
    return out


def field(b, name):
    m = re.search(rf'\b{name}\s*:\s*"((?:[^"\\]|\\.)*)"', b)
    return m.group(1).replace('\\"', '"') if m else None


def arr(b, name):
    m = re.search(rf'\b{name}\s*:\s*\[(.*?)\]', b, re.S)
    return re.findall(r'"([^"]+)"', m.group(1)) if m else []


def num(b, name):
    m = re.search(rf'\b{name}\s*:\s*(\d+)', b)
    return int(m.group(1)) if m else None


def build():
    h = open(SRC, encoding='utf-8').read()
    steps_txt = block(h, re.search(r'\bSTEPS\s*=', h).end())
    races_txt = block(h, re.search(r'\bRACES\s*=', h).end())

    steps = {}
    for key, b in entries(steps_txt).items():
        gain = field(b, 'gain') or ''
        steps[key] = dict(
            name=field(b, 'n'), kind=field(b, 'kind'), zone=field(b, 'zone'),
            npc=field(b, 'npc'), item=field(b, 'item'), qty=num(b, 'qty'),
            hours=field(b, 'hrs'), note=field(b, 'note'),
            gain_raw=gain,
            gain=[dict(faction=n.strip(), delta=int(d)) for n, d in GAIN.findall(gain)])

    races = {}
    for code, b in entries(races_txt).items():
        races[code] = dict(
            name=field(b, 'n'), align=field(b, 'align'), city=field(b, 'city'),
            tier=num(b, 'tier'), factions=arr(b, 'facs'), steps=arr(b, 'steps'),
            classes=arr(b, 'prim'), why=field(b, 'why'))

    # ---- what our own play measured -------------------------------------
    measured = {}
    try:
        sessions = json.load(open('assets/measured.json', encoding='utf-8'))
    except (OSError, ValueError):
        sessions = []
    for s in sessions:
        if not s.get('zone'):
            continue
        z = measured.setdefault(s['zone'], dict(
            difficulty=s.get('difficulty'), date=s.get('date'),
            kills=0, per_mob={}, factions=collections.Counter()))
        z['kills'] += s.get('kills', 0)
        for mob, facs in (s.get('faction_by_mob') or {}).items():
            z['per_mob'].setdefault(mob, facs)
            for f in facs:
                z['factions'][f] += 1
    for z in measured.values():
        z['factions'] = sorted(z['factions'])

    # What a zone's faction movement touches. Checking only the factions a race
    # *requires* misses most of it: a race lists three requirements, but the
    # steps that unlock it move a dozen factions between them, and undoing a
    # step's side gain is just as expensive as losing a requirement. So both are
    # traced, and a step's effect is carried back to every race that uses it.
    step_races = collections.defaultdict(set)
    for code, r in races.items():
        for st in r['steps']:
            step_races[st].add(r['name'])

    for zone, z in measured.items():
        falling = {f for facs in z['per_mob'].values() for f, d in facs.items() if d < 0}
        rising = {f for facs in z['per_mob'].values() for f, d in facs.items() if d > 0}
        z['falling'], z['rising'] = sorted(falling), sorted(rising)

        z['steps_undone'], z['steps_helped'] = [], []
        for key, st in steps.items():
            gains = {g['faction'] for g in st['gain'] if g['delta'] > 0}
            if gains & falling:
                z['steps_undone'].append(dict(step=key, name=st['name'],
                                              factions=sorted(gains & falling),
                                              races=sorted(step_races.get(key, []))))
            if gains & rising:
                z['steps_helped'].append(dict(step=key, name=st['name'],
                                              factions=sorted(gains & rising),
                                              races=sorted(step_races.get(key, []))))

        z['damages'] = sorted({n for r in races.values() if falling & set(r['factions'])
                               for n in [r['name']]}
                              | {n for e in z['steps_undone'] for n in e['races']})
        z['helps'] = sorted({n for r in races.values() if rising & set(r['factions'])
                             for n in [r['name']]}
                            | {n for e in z['steps_helped'] for n in e['races']})

    data = dict(steps=steps, races=races, measured=measured)
    json.dump(data, open('assets/faction-data.json', 'w', encoding='utf-8', newline='\n'),
              indent=1)

    named_facs = {f['faction'] for s in steps.values() for f in s['gain']}
    print(f"faction data: {len(steps)} quest steps, {len(races)} races, "
          f"{len(named_facs)} factions named in quest rewards, "
          f"{len(measured)} zone(s) measured from logs")
    for zone, z in measured.items():
        print(f"   {zone}: {len(z['factions'])} factions move across {z['kills']} kills"
              + (f"; risks {', '.join(z['damages'])}" if z['damages'] else '')
              + (f"; helps {', '.join(z['helps'])}" if z['helps'] else ''))


if __name__ == '__main__':
    build()
