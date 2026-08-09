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

INPUTS = ("_build/*.py", "_build/source/*.html", "assets/*.json",
          "site.config.json", "build.sh")


def fingerprint():
    h = hashlib.sha256()
    for pat in INPUTS:
        for f in sorted(glob.glob(pat)):
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
