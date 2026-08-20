"""Zone accent text variants, derived for each ground and checked against AA.

Imported by the generators that inject per-zone tokens. Writes no file of its
own; run directly to print the table and fail on any accent that cannot reach
contrast.

    python3 _build/accents.py            # print the table, exit 1 on a failure

WHY THIS EXISTS
---------------
Each zone owns one permanent accent and it is never reassigned. That accent is a
MATERIAL colour: the plate wash, the card border, the big numeral, a bar fill.
Non-text, so the 3:1 bar applies to it.

Type coloured with an accent is a different problem, and site.css says so in a
comment above the accent block: "Where one must carry text, blend toward --bone
at the point of use." That instruction is correct and unenforceable - it asks
every future rule to remember a derivation, and nothing checks that it did.

The site already solved this shape elsewhere. `--ember`/`--ember-t`,
`--brass`/`--brass-t`, `--lava`/`--lava-t`: a material colour and its text
variant, distinguished by suffix. The thirteen zone accents were the one family
that never got the `-t` half, and the surveys hand-picked one each instead.

MEASURED 20 AUG 2026, BEFORE CHANGING ANYTHING
----------------------------------------------
All thirteen hand-picked dark variants clear 4.5:1 on both the ground and the
panel. **So the dark theme has no defect and its values are not touched here.**
They were chosen by eye and they work; replacing thirteen working colours with
derived ones to satisfy a symmetry would be a change with no reader on its side.

What is missing is the other ground. On parchment, twelve of the thirteen
accents fail 4.5:1 as body text - the exception is Castle Mistmoore's #A8324A at
5.26, which is also the weakest of all thirteen on the dark ground at 3.08.
Accents are tuned to the ground they were drawn against, and there is now a
second ground.

THE DERIVATION
--------------
Mix the permanent accent toward ink in 2% steps; stop at the first value
clearing 4.5:1. Deterministic, thirteen in thirteen out, nothing hand-picked and
nothing to keep in sync. The permanent accent itself never changes.

Mistmoore returns UNCHANGED, because it already passes. That is the rule
behaving correctly rather than failing: its parchment text variant is the accent
itself. A minimum step count would deepen it to match the approved specimen, and
that is a one-line change here if it is ever wanted - it is recorded rather than
taken, because the ruling was to derive by the stated rule.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The two grounds a text variant has to clear, each with the colour a variant is
# mixed TOWARD to get away from it. Panel rather than page, because a label sits
# on the panel more often than on the bare sheet, and the panel is the harder of
# the two in daylight.
#
# The rule is one rule, mirrored: move the accent away from its own ground until
# it clears. On parchment that means toward ink; on graphite, toward bone.
GROUNDS = {
    'torch': ('#191309', '#F2EADA'),   # ground, toward
    'day':   ('#E7DCC6', '#241C12'),
}
DAYLIGHT_GROUND, DAYLIGHT_INK = GROUNDS['day']
TORCHLIGHT_GROUND = GROUNDS['torch'][0]

AA = 4.5
STEP = 0.02
MAX_STEPS = 60


def _srgb(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hexcolour):
    h = hexcolour.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    return sum(w * _srgb(int(h[i:i + 2], 16))
               for w, i in ((0.2126, 0), (0.7152, 2), (0.0722, 4)))


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def mix(a, b, t):
    a, b = a.lstrip('#'), b.lstrip('#')
    return '#%02X%02X%02X' % tuple(
        round(int(a[i:i + 2], 16) * (1 - t) + int(b[i:i + 2], 16) * t)
        for i in (0, 2, 4))


def derive(accent, ground=DAYLIGHT_GROUND, toward=DAYLIGHT_INK, target=AA):
    """The first value clearing `target` on `ground`, mixing toward `toward`.

    Returns (colour, steps). Raises where no mix in range reaches the target -
    the build must stop rather than publish type nobody can read.
    """
    out, steps = accent, 0
    while contrast(out, ground) < target:
        steps += 1
        if steps > MAX_STEPS:
            raise ValueError(
                f"{accent} cannot reach {target}:1 on {ground} by mixing toward "
                f"{toward} - it got to {contrast(out, ground):.2f} at "
                f"{MAX_STEPS * STEP:.0%}. Pick a different ground or a different "
                f"target; do not lower the bar.")
        out = mix(accent, toward, STEP * steps)
    return out, steps


def zones():
    with open(os.path.join(ROOT, 'assets', 'zones-index.json'),
              encoding='utf-8') as fh:
        return json.load(fh)


def variants(accent):
    """{'torch': (colour, steps, ratio), 'day': (...)} for one permanent accent."""
    out = {}
    for name, (ground, toward) in GROUNDS.items():
        colour, steps = derive(accent, ground, toward)
        out[name] = (colour, steps, contrast(colour, ground))
    return out


def table():
    """[(slug, accent, {theme: (colour, steps, ratio)})] for every zone."""
    return [(z['slug'], z['accent'], variants(z['accent']))
            for z in sorted(zones(), key=lambda e: e['slug'])]


def css_vars(slug_accent):
    """The two inline custom properties a card carries for one accent.

    An inline style cannot be theme-conditional, so a card cannot simply carry
    one --c-t. It carries BOTH derived variants under distinct names, and the
    theme blocks in site.css choose which one --c-t points at. That keeps the
    per-zone value exact rather than settling for one global mix ratio.
    """
    v = variants(slug_accent)
    return f"--c-t-torch:{v['torch'][0]};--c-t-day:{v['day'][0]}"


def main():
    rows = table()
    print(f"{'zone':<14}{'accent':<9}"
          f"{'torchlight -t':<15}{'ratio':>7}"
          f"{'   daylight -t':<16}{'ratio':>7}")
    bad = 0
    for slug, acc, v in rows:
        tc, _, tr = v['torch']
        dc, _, dr = v['day']
        if tr < AA or dr < AA:
            bad += 1
        print(f"{slug:<14}{acc:<9}{tc:<15}{tr:>7.2f}   {dc:<13}{dr:>7.2f}")
    print()
    print(f"{len(rows)} zones, {bad} failing {AA}:1 on their own ground")
    for name in GROUNDS:
        same = [r[0] for r in rows if r[2][name][1] == 0]
        if same:
            print(f"  {name}: unchanged by the rule (the accent already passes): "
                  f"{', '.join(same)}")
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
