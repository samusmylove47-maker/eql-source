#!/usr/bin/env bash
# EQL Source - full site rebuild.
# Edit a plate in _build/source/, or edit assets/zones-index.json, then run this.
set -e
cd "$(dirname "$0")"
# extract.py mines the originals in _build/source/, so it depends on nothing
# else and must run FIRST: the pages below print their counts from its output
# rather than carrying numbers typed by hand.
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
python3 _build/build14.py
python3 _build/build15.py
python3 _build/build17.py
python3 _build/build404.py
python3 _build/sitemap.py
python3 scripts/stamp.py
echo "Rebuilt. Commit and push, or drag the folder to Netlify."
