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
# records what it copied in assets/sky-ledger.json. The home page and both tool
# pages link and quote that file, so it runs before any of them. It does not
# fail on a machine without the Ledger repo - the copy and the record are both
# committed, same rule as geometry.py and the game's own files.
python3 _build/skyledger.py
python3 _build/extract.py
# Grades each zone on what a PLAYER needs - bosses, loot, difficulty,
# inherited advice, farming value - computed from the measured data.
# Runs before build1, which prints it on the plate cards.
python3 _build/coverage.py
# Copies the committed trailer and poster into public/ under a content hash.
# Runs before build1, which prints their filenames into the home page.
python3 _build/media.py
python3 _build/build1.py
python3 _build/build2.py
python3 _build/build3.py
# The Sky Ledger page. Prints every dataset figure out of assets/sky-ledger.json.
python3 _build/build28.py
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
python3 _build/build19.py
python3 _build/build20.py
python3 _build/build21.py
python3 _build/build22.py
# The contamination report. Reads assets/contamination.json, which
# scripts/contamination.py writes by hand - the scan is not part of the build.
python3 _build/build26.py
python3 _build/build24.py
python3 _build/build14.py
python3 _build/build15.py
python3 _build/sightings.py
# One shared locator plan per zone, plus the bounds build17.py needs to
# turn a recorded /loc into a position on it.
python3 _build/plans.py
python3 _build/build17.py
# Joins the catalogue, the measured sightings and the planar sets, so it runs
# after sightings.py has written the second of those and build17.py has made
# the item pages it links to.
python3 _build/build25.py
python3 _build/build404.py
# Search indexes the built pages, so it has to run after every generator that
# writes one. Keep it last but for the sitemap.
# The public data contract. Runs after every generator that writes the
# assets it reads, and before the sitemap so /data/ is listed.
python3 _build/publicdata.py
python3 _build/build27.py
python3 _build/build23.py
python3 _build/sitemap.py
python3 scripts/stamp.py
echo "Rebuilt. Commit and push, or drag the folder to Netlify."
