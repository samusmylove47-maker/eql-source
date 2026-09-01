"""Is the staleness watcher pointed at everything the build reads?

WHY THIS EXISTS
---------------
scripts/stamp.py fingerprints the build's inputs so that scripts/check.py can
refuse a tree whose public/ is older than its sources. That check works. On
31 August 2026 it was found to be aimed away from two of its own inputs:

  - public/assets/site.css, hand-edited, hashed into the stylesheet URL of every
    page by _partials._asset_v precisely so a returning reader is not served a
    cached copy of the old one. Editing it without rebuilding left check.py at
    exit 0, so the cache-busting hash silently stopped being recomputed.
  - _build/planar_raw.txt, read by _build/planardata.py, which build.sh runs to
    write assets/planar.json.

BOTH HAVE THE SAME SHAPE AND IT IS NOT "SOMEONE FORGOT A FILE". Every entry in
INPUTS is keyed on an EXTENSION - "_build/*.py", "assets/*.json". So a build
input sitting in a COVERED DIRECTORY with an UNCOVERED EXTENSION is invisible,
and the set of extensions a generator might read is open-ended. Two instances
turned up in one night, one directory apart. The next generator that reads a
.csv, a .yaml or a .tsv reopens the hole and nothing would mention it.

TWO FAULT SHAPES THAT LOOK ALIKE AND NEED DIFFERENT REMEDIES
------------------------------------------------------------
This repository already hunts one of them: an instrument that CANNOT FAIL. A
dead regex, a hash asserted only to be stable across rebuilds, a check whose
branch nothing reaches. The remedy is a matched pair - break the thing and prove
the check notices - and scripts/gate_selftest.py exists to do exactly that.

The fault this file is about is the other one: AN INSTRUMENT THAT WORKS
PERFECTLY AND IS AIMED AWAY FROM THE THING. stamp.py's fingerprint was never
broken. It was correct, sensitive to every byte of every file it covered, and
simply not pointed at site.css - the one file whose whole purpose is cache
invalidation, so a correct and sensitive hash was rendered inert by a watcher
that could not see its input.

A MATCHED PAIR CANNOT FIND THAT, and this is the part worth keeping. Mutate a
covered input and the check fails exactly as it should; the pair passes and
proves nothing about the region outside it. The remedy for an aimed-away
instrument is not a test, it is a COVERAGE AUDIT: enumerate what the thing is
pointed at, enumerate what it ought to be pointed at, and subtract. That is what
this file does, and it is why it is not another case in gate_selftest.py.

Told apart by one question: would the check pass if the code were correct? If no,
it may be dead - use a matched pair. If yes, ask what it is looking at.

Covering the directory instead of the extension was considered and rejected:
"_build/*" sweeps in every scratch file anyone leaves there, so the stamp moves
for edits that change no output. Enumeration is right; what was missing is
something that notices when the enumeration falls behind. That is this file.

WHAT IT DOES NOT KNOW, AND WHY THAT IS PRINTED RATHER THAN COMMENTED
--------------------------------------------------------------------
It finds paths written as literals inside open(). It cannot see a path built
from a variable or an f-string, and most of this repo's file access is exactly
that. So it audits a MINORITY of read sites and it must never be read as
"everything the build reads is covered".

The count of what it could NOT see is therefore part of its output, not a note
in this docstring - and it NAMES ITS EXIT. scripts/inputprobe.py answers the
question this one raises, by recording what the build actually opens at runtime.
A caveat a reader cannot resolve is a permanent shrug; one that points at the
instrument which resolves it is a map. The dynamic region is not evenly empty:
_media/ was hiding in it. A checker that reports a clean sweep while seeing a fraction
of the field is the fault it was built to catch, wearing a badge - the same
shape as an empty `unknown` list asserting a comparison was complete.

SCOPE
-----
Only _build/*.py, because those are what produce public/. A checker in scripts/
reading a file does not make that file a build input, and public/ and state/
paths are OUTPUTS that checkers read back - flagging those would produce six
false findings for every true one.

Only files that EXIST are reported. A generator naming a path that is not there
is a different bug, and one the generator itself will raise loudly.
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stamp import INPUTS          # one definition of the covered set, never two

SEP = os.sep

# A build input whose staleness matters lives in one of these. Everything under
# public/ is generated, and state/ holds the stamp itself, which would be
# circular.
ROOTS = ("_build/", "assets/")

# open('literal'  -- the only form this can resolve.
_LITERAL = re.compile(r"""open\(\s*['"]([^'"]+)['"]""")

# A quoted mode beginning w, a or x. Anchored on the quotes so a path that
# merely contains the letter is not mistaken for a write.
_WRITE_MODE = re.compile(r"""['"][wax]b?\+?['"]""")


def covered():
    """Every path the stamp actually fingerprints, expanded from its globs."""
    out = set()
    for pat in INPUTS:
        for f in glob.glob(pat):
            out.add(f.replace(SEP, "/"))
    return out


def audit():
    """(gaps, literal_read_sites, dynamic_sites_not_visible).

    A gap is (path, generator): a file that exists, lives under a build-input
    root, is opened for reading by a literal path in a generator, and is not
    fingerprinted by stamp.py.
    """
    cov = covered()
    gaps = []
    literal = 0
    dynamic = 0

    for gen in sorted(glob.glob("_build/*.py")):
        src = open(gen, encoding="utf-8").read()
        for m in re.finditer(r"open\(\s*([^)]{0,120})", src):
            call = "open(" + m.group(1)
            hit = _LITERAL.match(call)
            if not hit:
                dynamic += 1
                continue
            if _WRITE_MODE.search(call):
                continue                      # a write is not an input
            literal += 1
            path = hit.group(1).replace(SEP, "/")
            if not path.startswith(ROOTS):
                continue
            if not os.path.exists(path):
                continue
            if path in cov:
                continue
            gaps.append((path, gen.replace(SEP, "/")))

    return gaps, literal, dynamic


def run(fail, report):
    """Called by check.py. `fail` records a blocking failure, `report` prints."""
    gaps, literal, dynamic = audit()
    for path, gen in gaps:
        size = os.path.getsize(path)
        fail(f"{path} ({size:,} bytes) is read by {gen} but scripts/stamp.py "
             f"does not fingerprint it, so editing it leaves public/ stale and "
             f"every check green. Add a glob covering it to stamp.py's INPUTS")
    # THE LIMIT IS PART OF THE RESULT. See the docstring: a clean line here
    # means "nothing found among the sites I can see", never "nothing to find".
    report(f"build inputs: {literal} literal read site(s) checked, "
           f"{dynamic} dynamic site(s) not visible to this check "
           f"(run scripts/inputprobe.py to see those)")


if __name__ == "__main__":
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(ROOT)
    _gaps, _lit, _dyn = audit()
    for _p, _g in _gaps:
        print(f"  GAP  {_p}  read by {_g}")
    print(f"  {_lit} literal read site(s) checked, "
          f"{_dyn} dynamic site(s) not visible to this check")
    sys.exit(1 if _gaps else 0)
