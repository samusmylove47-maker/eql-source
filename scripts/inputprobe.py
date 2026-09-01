"""Does stamp.py fingerprint everything the build actually reads?

Hand-run, like conformance.js and mediadefer.js. NOT part of build.sh.

WHY THIS EXISTS
---------------
scripts/inputscover.py answers the same question by reading the generators for
literal paths, and prints on every run that it cannot see the dynamic ones. That
line was honest and it was a dead end: a caveat a reader has no way to resolve.

It was also not theoretical. _media/ is a build input read only through
glob() and os.path.join() on a variable, so no source-reading audit resolves it,
and stamp.py did not cover it. A grep of glob() roots missed it too, for the same
reason one level up. Every static method fails on the same thing.

This one fails differently. It patches builtins.open in every Python process the
build starts, so it records what the build ACTUALLY opened. By the time open() is
called a path is just a string, so computed, globbed and data-driven reads are
all visible.

Run it when someone adds a generator, or changes how one reads its inputs.

    python3 scripts/inputprobe.py

WHAT IT CANNOT SEE, AND WHY THAT REFUSES RATHER THAN WARNS
-----------------------------------------------------------
It only sees builtins.open. A generator using pathlib, io.open, os.open,
Path.read_text or shutil.copy would be invisible, and the probe would print a
confident total over an incomplete observation.

Today no generator uses any of those. That is a property of the code, not a
guarantee, and a tool whose soundness rests on an unenforced property of the
thing it observes is precisely the fault it exists to hunt. So the property is
CHECKED FIRST, and a violation makes this refuse to report at all rather than
report a number it cannot stand behind.

The scan carries its own positive control: it also looks for `open(`, which must
be present. A scanner that finds none of the eight forbidden routes because its
matching is broken would otherwise look identical to a clean repository.
"""
import glob
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from stamp import INPUTS

SEP = os.sep

# Reads this probe cannot observe. Each would open a file without going through
# builtins.open, so the recording would silently under-report.
BLIND_ROUTES = [
    ("pathlib", r"\bpathlib\b"),
    ("Path(", r"\bPath\s*\("),
    (".read_text(", r"\.read_text\s*\("),
    (".read_bytes(", r"\.read_bytes\s*\("),
    ("io.open(", r"\bio\.open\s*\("),
    ("os.open(", r"\bos\.open\s*\("),
    ("shutil.copy", r"\bshutil\.copy"),
    ("np.load(", r"\bnp\.load\s*\("),
]

# The control. If this stops matching, the scan above is broken and its silence
# means nothing.
CONTROL = ("open(", r"\bopen\s*\(")

# Everything under these is generated or is the stamp itself, not an input.
OUTPUT_ROOTS = ("public/", "state/", ".git/")

RECORDER = '''"""Written by scripts/inputprobe.py. Records what the build opens."""
import atexit, builtins, os

_LOG = os.environ.get("EQLS_OPENLOG")
_seen = set()
_real_open = builtins.open


def _logging_open(file, mode="r", *a, **kw):
    try:
        m = mode if isinstance(mode, str) else "r"
        if "w" not in m and "a" not in m and "x" not in m:
            if isinstance(file, (str, bytes, os.PathLike)):
                _seen.add(os.path.abspath(os.fspath(file)))
    except Exception:
        pass
    return _real_open(file, mode, *a, **kw)


def _flush():
    if not _LOG or not _seen:
        return
    try:
        fd = os.open(_LOG, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
        os.write(fd, ("\\n".join(sorted(_seen)) + "\\n").encode("utf-8", "replace"))
        os.close(fd)
    except Exception:
        pass


if _LOG:
    builtins.open = _logging_open
    atexit.register(_flush)
'''


def scan_routes():
    """(violations, control_hits). Condition for reporting at all."""
    violations = []
    control = 0
    for gen in sorted(glob.glob("_build/*.py")):
        src = open(gen, encoding="utf-8").read()
        control += len(re.findall(CONTROL[1], src))
        for name, pattern in BLIND_ROUTES:
            if re.search(pattern, src):
                violations.append((gen.replace(SEP, "/"), name))
    return violations, control


def covered():
    out = set()
    for pat in INPUTS:
        for f in glob.glob(pat):
            out.add(os.path.abspath(f).replace(SEP, "/"))
    return out


def main():
    print("  scripts/inputprobe.py - what the build actually reads")
    print()

    # ---- condition: can this probe see everything? --------------------------
    violations, control = scan_routes()
    if not control:
        print("  REFUSING TO REPORT: the route scan found no `open(` anywhere in")
        print("  _build/*.py, so its own matching is broken and its silence about")
        print("  the other eight routes means nothing.")
        return 2
    if violations:
        print("  REFUSING TO REPORT. This probe records builtins.open and nothing")
        print("  else, and these generators read by a route it cannot observe:")
        for gen, name in violations:
            print(f"    {gen}  uses  {name}")
        print()
        print("  Any total printed now would be computed over an incomplete")
        print("  observation and would look exactly like a clean result. Either")
        print("  change those reads to open(), or extend this probe to patch the")
        print("  route they use.")
        return 1
    print(f"  read routes: {len(BLIND_ROUTES)} unobservable route(s) checked, none used")
    print(f"               ({control} open() call sites found, so the scan works)")

    # ---- run the build under the recorder -----------------------------------
    tmp = tempfile.mkdtemp(prefix="eqls-probe-")
    with open(os.path.join(tmp, "sitecustomize.py"), "w",
              encoding="utf-8", newline="\n") as fh:
        fh.write(RECORDER)
    logpath = os.path.join(tmp, "opened.txt")

    env = dict(os.environ)
    env["PYTHONPATH"] = tmp + os.pathsep + env.get("PYTHONPATH", "")
    env["EQLS_OPENLOG"] = logpath
    # The app copiers reach into sibling repositories, which are outside this
    # repo and correctly not fingerprinted. Skipping them also stops the probe
    # republishing someone else's build as a side effect of a measurement.
    env["EQLS_SKIP_APPS"] = "1"

    try:
        r = subprocess.run(["bash", "build.sh"], env=env,
                           capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
    except FileNotFoundError:
        print("  WARN  no bash on PATH, so the build could not be run and")
        print("        nothing was observed. This says nothing about coverage.")
        return 0
    if r.returncode != 0:
        print(f"  the build failed (exit {r.returncode}), so nothing was observed:")
        print("   ", (r.stderr or r.stdout).strip().splitlines()[-1:] or "")
        return 1

    if not os.path.exists(logpath):
        print("  WARN  the build ran but recorded nothing, which means the")
        print("        recorder was not loaded. Treat this as a FAILED READ, not")
        print("        as a clean result.")
        return 1

    with open(logpath, encoding="utf-8", errors="replace") as fh:
        read = {ln.strip().replace(SEP, "/") for ln in fh if ln.strip()}

    root = ROOT.replace(SEP, "/").rstrip("/") + "/"
    cov = covered()
    inputs, gaps = 0, []
    for p in sorted(read):
        if not p.startswith(root):
            continue
        rel = p[len(root):]
        if rel.startswith(OUTPUT_ROOTS) or "__pycache__" in rel:
            continue
        if not os.path.isfile(p):
            continue
        inputs += 1
        if p not in cov:
            gaps.append(rel)

    print(f"  observed:    {len(read)} path(s) opened for reading, "
          f"{inputs} of them build inputs")
    print(f"  fingerprint: {len(cov)} path(s) covered by stamp.py INPUTS")
    print()

    # ---- the limits, in the output, not in a comment ------------------------
    print("  NOT OBSERVED BY THIS RUN:")
    print("    - one build. A conditional branch not taken read nothing, so this")
    print("      is everything read on this run, not everything readable.")
    print("    - EQLS_SKIP_APPS was set, so skyledger.py and lockouts.py did not")
    print("      read the sibling repos. Those live outside this repository and")
    print("      are correctly not fingerprinted; the copies are hash-verified.")
    print("    - hand-run generators build.sh never calls: geometry.py (reads the")
    print("      game install), ogcards.py, fetchfonts.py (reads the network).")
    print("      media.py reads _media/, which IS covered - run it under this")
    print("      probe directly if you change it.")
    print()

    if gaps:
        print("  READ BY THE BUILD AND NOT FINGERPRINTED:")
        for g in gaps:
            print(f"    {g:52} {os.path.getsize(g):>9,} B")
        print()
        print("  Add a glob covering these to scripts/stamp.py INPUTS. Until then,")
        print("  editing one leaves public/ stale with every check green.")
        return 1

    print("  Every build input observed on this run is fingerprinted.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
