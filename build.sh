#!/usr/bin/env bash
# EQL Source - full site rebuild.
# Edit a plate in _build/source/, or edit assets/zones-index.json, then run this.
set -e
cd "$(dirname "$0")"
python3 _build/build1.py
python3 _build/build2.py
python3 _build/build3.py
python3 _build/build4.py
python3 _build/extract.py
python3 _build/build5.py
python3 _build/sitemap.py
echo "Rebuilt. Commit and push, or drag the folder to Netlify."
