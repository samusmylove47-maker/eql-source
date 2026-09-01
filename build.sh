#!/usr/bin/env bash
# EQL Source - full site rebuild.
# Edit a plate in _build/source/, or edit assets/zones-index.json, then run this.
set -e
cd "$(dirname "$0")"
# extract.py mines the originals in _build/source/, so it depends on nothing
# else and must run FIRST: the pages below print their counts from its output
# rather than carrying numbers typed by hand.
# Validates assets/sky.json and exits non-zero if it is malformed, if a claim
# names a source that does not exist, or if a dataset invariant moved. Runs
# before anything renders it.
python3 _build/skydata.py
# Copies the Sky Ledger browser build into public/app/ under a content hash and
# BOTH COPIERS BELOW HONOUR EQLS_SKIP_APPS. Set it when the branch is not about
# an app, and the committed copies are kept exactly as they are:
#
#     EQLS_SKIP_APPS=1 ./build.sh
#
# Without it, every build on every branch picks up whatever the sibling repos
# have built since the branch point - which is a publish decision, made by
# whoever happened to rebuild. Unset stays the default: a guard that silently
# stopped a real publish would be worse than the problem. See _build/appskip.py.
#
# records what it copied in assets/sky-ledger.json. The home page and both tool
# pages link and quote that file, so it runs before any of them. It does not
# fail on a machine without the Ledger repo - the copy and the record are both
# committed, same rule as geometry.py and the game's own files.
python3 _build/skyledger.py
# The EQLS Lockouts app, copied under its content hash the same way. Nothing
# links it yet - the tool is not promoted - so this ships the copy only, and
# check.py WARNs for as long as that stays true.
python3 _build/lockouts.py
python3 _build/extract.py
# Grades each zone on what a PLAYER needs - bosses, loot, difficulty,
# inherited advice, farming value - computed from the measured data.
# Runs before build1, which prints it on the plate cards.
python3 _build/coverage.py
# Copies the committed trailer and poster into public/ under a content hash.
# Runs before build1, which prints their filenames into the home page.
python3 _build/media.py
# The EQLS Auras page. Runs BEFORE build1.py because the home-page band reads
# the same assets/auras.json and links this page; a band pointing at a page
# that does not exist yet would fail the link check on a clean tree.
python3 _build/build32.py
python3 _build/build1.py
python3 _build/build2.py
python3 _build/build3.py
# The Sky Ledger page. Prints every dataset figure out of assets/sky-ledger.json.
python3 _build/build28.py
# tools/lockouts.html. Reads the timing constants out of the served bundle, so
# it must run after lockouts.py has put that bundle in public/app/.
python3 _build/build30.py
# tools/gap-engine.html. Reads assets/gap-engine.json, which is E's synthetic
# fixture; the generator refuses to build from anything not marked _fixture.
python3 _build/build31.py
# The 50 Upgrades description page. Reads assets/50-upgrades.json, which is a
# vendored snapshot of the planner's own meta.json rather than anything we count.
python3 _build/build29.py
python3 _build/build5.py
python3 _build/build6.py
python3 _build/build7.py
# The Plane of Sky's measured half. Derives from measured.json and
# raids-measured.json, so it must run before build8.py renders it.
python3 _build/skyloot.py
python3 _build/build8.py
python3 _build/extract_faction.py
python3 _build/build9.py
python3 _build/build10.py
python3 _build/build11.py
python3 _build/build12.py
python3 _build/build13.py
python3 _build/build18.py
# planardata.py writes assets/planar.json. The page that used to render beside
# it — the planar gear tool — was withdrawn on 18 Aug 2026, and the dataset
# outlived it exactly as the split was built to allow: /sets/, sightings.py and
# the contamination scanner all still read it.
python3 _build/planardata.py
python3 _build/build20.py
python3 _build/build21.py
python3 _build/build22.py
# The contamination report. Reads assets/contamination.json, which
# scripts/contamination.py writes by hand - the scan is not part of the build.
python3 _build/build26.py
python3 _build/build24.py
python3 _build/build14.py
python3 _build/sightings.py
# One shared locator plan per zone, plus the bounds build17.py needs to
# turn a recorded /loc into a position on it.
python3 _build/plans.py
python3 _build/build17.py
python3 _build/build404.py
# Search indexes the built pages, so it has to run after every generator that
# writes one. Keep it last but for the sitemap.
# The public data contract. Runs after every generator that writes the
# assets it reads, and before the sitemap so /data/ is listed.
python3 _build/publicdata.py
python3 _build/build27.py
python3 _build/build23.py
# THE SELF-AUDIT NOW RUNS IN THE BUILD, because its ARTIFACT is published.
#
# scripts/contamination.py was hand-run. On 1 Sep 2026 its scope changed in code
# - six signatures, and it began scanning public/ instead of only the build
# inputs - and assets/contamination.json was last regenerated on 14 AUGUST. So
# /learn/contamination published "24 files scanned, 291 unmarked" for eighteen
# days while the code that produced it had moved on. Nothing was blocked and no
# check was red: the output IS the stale thing.
#
# It costs 1.7 seconds and needs no network, no browser and no game install, so
# the reason it was manual does not survive contact with the fact that a reader
# sees its number.
#
# ORDER MATTERS BOTH WAYS. It scans public/**, so it must run after the pages
# exist; build26.py renders its result, so that must run after the scan. Hence
# here, at the end, with build26 repeated rather than moved - the earlier run
# keeps the page present for the scan, and this one gives it today's numbers.
python3 scripts/contamination.py --write
python3 _build/build26.py
python3 _build/sitemap.py
python3 scripts/stamp.py
# WHAT THIS BUILD SWEPT IN, SAID LAST, WHERE A PERSON ACTUALLY LOOKS.
#
# Six times in four days a ./build.sh run for an unrelated reason has copied a
# newer third-party bundle into public/app/ and swept the old one, putting an
# app republish into a branch that had nothing to do with it. Twice it reached a
# pull request: once naming the wrong hash in its own title, once carrying 1,428
# lines of sitemap churn into a docs-only change.
#
# Every one was caught by diffing against main before pushing, and none by
# noticing at the time - because the copy announces itself two hundred lines up,
# in the middle of fifty generators, while you are watching for something else.
#
# This is not a new safeguard. It is the existing habit made cheaper: the diff
# is still the thing that catches it, and this only makes the thing worth
# diffing visible without asking for it. On this repository every release of a
# sibling tool needs a commit here, so any build is a publish decision.
python3 - <<'SWEEP'
import subprocess, sys
try:
    out = subprocess.run(['git', 'status', '--porcelain', '--',
                          'public/app', 'assets/lockouts.json',
                          'assets/sky-ledger.json', 'assets/gap-engine-app.json'],
                         capture_output=True, text=True, timeout=20).stdout.strip()
except Exception:
    sys.exit(0)                      # not a git tree, or git absent: say nothing
if not out:
    sys.exit(0)
lines = [l for l in out.splitlines() if l.strip()]
print()
print('  ' + '=' * 68)
print('  THIS BUILD CHANGED A SERVED APPLICATION. That is a publish decision.')
print('  ' + '=' * 68)
for l in lines:
    print('   ', l)
print()
print('  If you are on a branch about something else, these do not belong in it.')
print('  Check before you commit:  git diff --stat origin/main -- public/app assets')
SWEEP
echo "Rebuilt. Open a pull request; merging to main is what publishes."
