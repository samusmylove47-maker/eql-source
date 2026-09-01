#!/usr/bin/env python3
"""Record what the current public/ was built from.

WHY
---
check.py validates the HTML on disk. It cannot tell a completed build from an
aborted one, so when a generator crashes half way the previous output stays
there and every check passes. That happened on 10 Aug 2026: build6.py was left
with a syntax error, build.sh stopped at it under `set -e`, and check.py
reported "All checks passed" against output built minutes earlier.

So build.sh stamps a hash of every input, and check.py recomputes it. A
mismatch means the tree on disk is not what the sources would produce.
"""
import glob, hashlib, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# THE TWO STYLESHEETS ARE INPUTS, AND LEAVING THEM OUT MADE THIS CHECK LIE.
#
# public/assets/site.css is hand-edited - it is the design system, and no
# generator writes it. _partials.py hashes it into CSS_V and puts that hash in
# the stylesheet URL of every page, precisely so a returning reader is not
# served a cached copy of the old one. That mechanism only works if the pages
# are REBUILT after the file changes.
#
# Measured 31 Aug 2026, matched pair:
#
#   edit public/assets/site.css, do not rebuild  ->  check.py exit 0, "All checks passed"
#   edit a covered input, do not rebuild         ->  check.py exit 1, "public/ is stale"
#
# So the detector was alive and specifically blind to the one file whose whole
# point is cache invalidation. The stylesheet changes, CSS_V does not, the URL
# does not, and every reader who has visited before keeps the old sheet - which
# is the exact incident _partials._asset_v was written after: "unstyled black
# shapes over a bare headline", found only by inspecting stylesheets one by one,
# because the site was correct and only the reader's copy was stale.
#
# fonts.css is the same shape via FONTS_V, and the same probe returned exit 0.
#
# Both are read-only during a build (only _partials.py, build3.py and the
# hand-run fetchfonts.py touch them), so adding them cannot make the stamp
# invalidate itself.
# AND THE GLOBS THEMSELVES ARE THE RISK, WHICH IS HOW site.css WAS MISSED.
#
# Every entry here is extension-specific, so a build input in a covered
# DIRECTORY with an uncovered EXTENSION is invisible. Audited 31 Aug 2026 by
# listing every literal path the generators open for reading and subtracting
# what these globs match. One survived: _build/planar_raw.txt, read by
# _build/planardata.py, which build.sh runs at line 73 to write
# assets/planar.json. Measured the same way as the stylesheets - edit it, do not
# rebuild, check.py exits 0.
#
# assets/planar.json IS covered, so a rebuild propagates. What nothing noticed
# was the raw file and the generated one disagreeing, which is the state you are
# left in by editing the source and walking away.
#
# The audit cannot see dynamic open() calls - 105 of them - so this list is
# "everything reachable by reading the source", not "everything". Re-run that
# audit when a generator starts reading a new kind of file.
# _media/ IS A BUILD INPUT AND A LITERAL-PATH AUDIT CANNOT SEE IT.
#
# _build/media.py:35 sets SRC = '_media' and copies from it under a content
# hash. Found 31 Aug 2026 by a fan-out reading the generators, AFTER a
# literal-path audit of my own had reported the coverage clean - media.py builds
# its paths with glob and os.path.join, so no source read resolves them. That is
# the stated limit of scripts/inputscover.py arriving as a real instance rather
# than a caveat, and it is why that check prints how many sites it could not see.
#
# Measured: edit a file in _media/, do not rebuild, check.py exits 0.
INPUTS = ("_build/*.py", "_build/*.txt", "_build/source/*.html", "assets/*.json",
          "_media/*", "site.config.json", "build.sh",
          "public/assets/site.css", "public/assets/fonts/fonts.css")


def fingerprint():
    h = hashlib.sha256()
    for pat in INPUTS:
        for f in sorted(glob.glob(pat)):
            if not os.path.isfile(f):
                continue          # a glob may match a directory; that is not an input
            if f.endswith("prose-budget.json"):
                continue          # written after the build, from the build
            h.update(f.replace(os.sep, "/").encode())
            h.update(open(f, "rb").read())
    return h.hexdigest()


if __name__ == "__main__":
    os.makedirs("state", exist_ok=True)
    json.dump({"inputs": fingerprint()},
              open("state/last-build.json", "w", encoding="utf-8"), indent=1)
    print("build stamped")
