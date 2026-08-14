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
python3 _build/extract.py
python3 _build/build1.py
python3 _build/build2.py
python3 _build/build3.py
python3 _build/build4.py
python3 _build/build5.py
python3 _build/build6.py
python3 _build/build7.py
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
python3 _build/build24.py
python3 _build/build14.py
python3 _build/build15.py
python3 _build/sightings.py
python3 _build/build17.py
# Joins the catalogue, the measured sightings and the planar sets, so it runs
# after sightings.py has written the second of those and build17.py has made
# the item pages it links to.
python3 _build/build25.py
python3 _build/build404.py
# Search indexes the built pages, so it has to run after every generator that
# writes one. Keep it last but for the sitemap.
python3 _build/build23.py
python3 _build/sitemap.py
python3 scripts/stamp.py
echo "Rebuilt. Commit and push, or drag the folder to Netlify."
