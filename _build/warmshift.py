"""Rotate the hand-written plate palettes onto Norrath's measured warm axis.

    python3 _build/warmshift.py --dry      # report what would change
    python3 _build/warmshift.py            # rewrite _build/source/*.html

Run by hand, once, like prose_budget.py. It is not part of build.sh: a script
that rewrites its own inputs on every build is a script that eventually
rewrites something it should not.

WHY
---
The ten dungeon surveys and their maps are hand-written HTML in _build/source/
with their own inline stylesheets, predating the shared design system. They
carry roughly forty colours of their own, and nearly all of them are cool
slates: #8A9998 appears 281 times, #2E3A41 236 times.

On 16 Aug 2026 the site's chrome moved to a palette measured out of the game's
own textures, where Norrath's grounds are hue 15-30 and 62% of saturated colour
is warm. That left the site's deepest twenty pages sitting in the old cool
world while everything around them warmed up.

HOW, AND WHY THIS PARTICULAR HOW
--------------------------------
Luminance is preserved EXACTLY and only hue is rotated.

That matters more than it sounds. Every one of these pages was checked against
WCAG AA when it was written, and those ratios are a function of relative
luminance alone. Rotate hue at constant luminance and every contrast ratio on
every one of those pages is mathematically unchanged - there is nothing to
re-verify and nothing that can silently regress. Picking nicer-looking warm
colours by eye would have put all twenty pages back through an accessibility
audit to find out what broke.

WHAT IT LEAVES ALONE
--------------------
Signal colours and zone accents. A green that means "verified" and a red that
means "wrong" are carrying meaning, not temperature, and the ten zone accents
are permanent identity - CLAUDE.md is explicit that a zone owns its accent and
it is never reassigned. Only near-neutrals in the cool half of the wheel move,
which is exactly the set that made these pages read as slate.
"""
import os, re, sys, glob, colorsys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Norrath's measured ground hue, from assets/norrath-palette.json: the dominant
# grounds sit at hue 15-30 across 2.6 million samples. 30 is the middle of that
# and the hue of the most common single ground colour, #180C00.
WARM_HUE = 30 / 360

# Anything more saturated than this is carrying meaning rather than temperature.
# 0.30 was too loose: it swept up a teal at s=0.29 and a violet at s=0.26, both
# of which are somebody's accent rather than somebody's grey.
NEUTRAL_MAX_S = 0.22
# The cool half of the wheel, where the slates live. Stops short of violet,
# which in these files is used as a colour rather than as a neutral.
COOL_LO, COOL_HI = 140, 250

# Never touched, whatever their hue: signal colours and the ten zone accents.
KEEP = {
    '#5FA37E', '#C9453A', '#D46C64', '#C4482E', '#D76C55', '#7FB2C7',
    '#D9A227', '#45A6A0', '#BE4F3E', '#8E7BC7', '#5C93C4',
    '#7FA84F', '#E06B2A', '#8C7BE0', '#B5793C', '#A8324A',
    '#FF2800', '#FF6A4D', '#C9922E', '#D9A63F',
}

HEX = re.compile(r'#([0-9A-Fa-f]{6})\b')


def shift(hexv):
    """Warm one colour, or return it unchanged."""
    up = '#' + hexv[1:].upper()
    if up in KEEP:
        return None
    r, g, b = (int(hexv[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    deg = h * 360
    if s > NEUTRAL_MAX_S:
        return None
    if not (COOL_LO <= deg <= COOL_HI):
        return None
    # A true grey (s == 0) has no hue to rotate and no cast to correct. Giving
    # it one would tint every hairline on the page.
    if s < 0.012:
        return None

    # HOLD RELATIVE LUMINANCE, NOT HLS LIGHTNESS.
    # These are not the same thing and the difference is the whole point. WCAG
    # contrast is a function of relative luminance, which weights green at
    # 0.7152 and blue at 0.0722 - so rotating a slate to an amber at constant
    # HLS lightness moves the real luminance by as much as 0.059, and every
    # contrast ratio on the page moves with it. Rotate the hue, then solve for
    # the lightness that puts relative luminance back exactly where it was.
    target = _rel_lum_rgb(r, g, b)
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        rr, gg, bb = colorsys.hls_to_rgb(WARM_HUE, mid, s)
        if _rel_lum_rgb(rr, gg, bb) < target:
            lo = mid
        else:
            hi = mid
    rr, gg, bb = colorsys.hls_to_rgb(WARM_HUE, (lo + hi) / 2, s)
    return '#%02X%02X%02X' % (round(rr * 255), round(gg * 255), round(bb * 255))


def _rel_lum_rgb(r, g, b):
    """WCAG relative luminance from 0-1 floats."""
    def lin(c):
        return c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    return .2126 * lin(r) + .7152 * lin(g) + .0722 * lin(b)


def luminance(hexv):
    def lin(c):
        c /= 255
        return c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    r, g, b = (int(hexv[i:i + 2], 16) for i in (1, 3, 5))
    return .2126 * lin(r) + .7152 * lin(g) + .0722 * lin(b)


def main():
    dry = '--dry' in sys.argv
    os.chdir(ROOT)
    files = sorted(glob.glob('_build/source/*.html'))
    seen = {}
    for p in files:
        for m in HEX.finditer(open(p, encoding='utf-8').read()):
            hexv = '#' + m.group(1)
            seen[hexv.upper()] = seen.get(hexv.upper(), 0) + 1

    table = {}
    for hexv, n in sorted(seen.items(), key=lambda kv: -kv[1]):
        new = shift(hexv)
        if new:
            table[hexv] = new

    print(f'{len(seen)} distinct colours across {len(files)} source files; '
          f'{len(table)} will be warmed\n')
    # The number that actually matters is not luminance drift, it is how much
    # any real contrast ratio moves. Report that, against both page grounds.
    GROUNDS = ('#0B0704', '#1E1810')

    def ratio(a, b):
        x, y = luminance(a), luminance(b)
        hi, lo = max(x, y), min(x, y)
        return (hi + .05) / (lo + .05)

    print(f"  {'from':<9} {'to':<9} {'uses':>5}   worst contrast change")
    worst = 0.0
    for old, new in sorted(table.items(), key=lambda kv: -seen[kv[0]]):
        d = max(abs(ratio(old, g) - ratio(new, g)) for g in GROUNDS)
        worst = max(worst, d)
        print(f'  {old:<9} {new:<9} {seen[old]:>5}   {d:+.4f}')
    print(f'\nWorst contrast-ratio change anywhere: {worst:.4f}')
    print('Residual is 8-bit rounding only; hue rotates and relative luminance '
          'is solved back to the original.')
    if worst > 0.05:
        print('*** ABOVE 0.05 — re-verify the affected pages against AA. ***')

    if dry:
        print('\n--dry: nothing written')
        return 0

    changed = 0
    for p in files:
        s = open(p, encoding='utf-8').read()
        orig = s
        for old, new in table.items():
            s = re.sub(re.escape(old), new, s, flags=re.I)
        if s != orig:
            open(p, 'w', encoding='utf-8', newline='\n').write(s)
            changed += 1
    print(f'\n{changed} source files rewritten. Run ./build.sh.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
