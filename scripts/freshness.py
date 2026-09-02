#!/usr/bin/env python3
"""Prove the committed output is what a fresh build produces.

    python3 scripts/freshness.py

WHAT IT CATCHES, AND WHY NOTHING ELSE CAN
-----------------------------------------
CLAUDE.md section 4 states the fault in as many words: "Generated files are
overwritten by ./build.sh. A rebuild silently throws away anything edited in
place; check.py will not catch it."

That is exact. check.py runs AFTER build.sh, so by the time it looks, the tree
has already been regenerated and whatever was hand-edited is gone. It validates
the rebuilt page and reports green. The edit is lost, the check passed, and
nothing in the repo noticed.

scripts/stamp.py does not close it either. The stamp fingerprints the build
INPUTS, so it catches a stale tree - output older than the generators that made
it. It cannot catch the opposite: inputs untouched, output edited by hand. The
stamp is current and the page is wrong.

This closes it from the other side. Commit everything, rebuild, and require the
tree to be unchanged. A file that differs is a file whose committed content is
not what its generator produces, which means one of two things and both matter:

  * someone edited a generated file in place, and the next build will discard it
  * a generator was changed and its output was never rebuilt before committing

WHY IT IS A SCRIPT AND NOT A HABIT
----------------------------------
It was a habit for one evening, run by hand before merges, and it caught nothing
because it was never wrong. That is exactly when a habit is most likely to be
dropped. Every fault caught on 1 September 2026 was caught by a mechanism
somebody had built earlier - the propagation gate, the self-test verifying its
own mutations applied, conformance.js measuring a box escaping its wrapper -
and none by anybody remembering a principle at the right moment.

It is deliberately NOT part of build.sh or check.py. It runs a build, so calling
it from either would recurse; and it needs a committed tree to compare against,
which is a state that exists before a commit rather than during one. Hand-run,
like scripts/conformance.js and scripts/prose_budget.py, and for the same reason:
some checks answer a question the build cannot ask about itself.

EXIT CODES
----------
0  the committed output is exactly what a fresh build produces
1  it is not, and the differing paths are listed
2  the tree was already dirty, so there was nothing to compare against
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def dirty():
    """Paths git reports as changed.

    THE OUTPUT IS NOT STRIPPED AS A WHOLE, AND THAT IS THE POINT.
    `git status --porcelain` writes two status characters then a space, and for
    an unstaged modification the first of those is a SPACE. Stripping the
    combined output therefore removes one column from the FIRST LINE ONLY, and
    that path comes back missing its leading character.

    This did exactly that on its first run and reported `ublic/index.html`.
    Every line after the first was correct, which is what made it read as a
    display quirk rather than a parse bug - a helper that trims whitespace,
    harmless everywhere else, silently corrupting the one format where leading
    whitespace carries meaning.
    """
    r = subprocess.run(("git", "status", "--porcelain"), cwd=ROOT,
                       capture_output=True, text=True)
    out = []
    for line in r.stdout.split("\n"):
        if not line.strip():
            continue
        path = line[3:].strip()
        # A rename reads "R  old -> new"; the new name is the one on disk.
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        out.append(path.strip('"'))
    return out


def main():
    before = dirty()
    if before:
        # NOT A FAILURE OF THE THING BEING TESTED. A dirty tree means there is
        # no committed state to compare a rebuild against, so the gate cannot
        # answer its question either way - and a check that reports "pass"
        # when it could not run is the fault this repo keeps finding.
        print(f"  {len(before)} uncommitted path(s); nothing to compare a rebuild against.")
        print("  Commit or set the work aside first, then run this. Showing the first few:")
        for p in before[:8]:
            print(f"    {p}")
        return 2

    print("  tree is clean; rebuilding")
    build = subprocess.run(["bash", "build.sh"], cwd=ROOT,
                           capture_output=True, text=True, env=os.environ.copy())
    if build.returncode != 0:
        print(f"  build.sh exited {build.returncode}")
        print("  " + "\n  ".join((build.stderr or build.stdout).strip().split("\n")[-12:]))
        return 1

    after = dirty()
    if not after:
        print("  0 path(s) changed - the committed output is exactly what a fresh build produces")
        return 0

    print(f"  {len(after)} path(s) differ from what the generators produce:")
    for p in after[:30]:
        print(f"    {p}")
    if len(after) > 30:
        print(f"    ... and {len(after) - 30} more")
    print()
    print("  Either a generated file was edited in place - the next build will throw")
    print("  that away - or a generator changed and its output was never rebuilt.")
    print("  Both are silent: check.py runs after the build and sees only the rebuilt")
    print("  tree, so it reports green either way. Rebuild, review the diff, commit it.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
