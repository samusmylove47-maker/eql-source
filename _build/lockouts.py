"""Copy the EQLS Lockouts app into public/app/ under its content hash.

Run by build.sh. Output: public/app/eqls-lockouts.<hash>.html and
assets/lockouts.json.

WHAT THIS IS NOT, YET
---------------------
There is no tools/ page and no landing-page band for this tool, deliberately.
The Director's order of 25 August 2026 was to ship the copy step and hold the
promotion until Session D reports again. So for now the app is served under a
hashed URL that **nothing on the site links**, and that is the intended state
rather than an oversight.

check.py's Sky Ledger guard ends by requiring that some page link the hashed
file, on the reasoning that an unreachable 176 KB asset is a bug. That clause is
deliberately absent for this tool and a WARN stands in its place, so the
unpromoted state is visible in every single build instead of being silently
tolerated. When the tool is promoted, the WARN goes away on its own and the
clause should be turned on. A check that quietly permits the interim state is a
check that will still permit it a year from now.

WHY THE HASH IS COMPUTED HERE AND NOT READ OFF THE FILENAME
-----------------------------------------------------------
The Lockouts repo already names its own build `eqls-lockouts.<sha256[:8]>.html`
and writes a `latest.txt` pointer beside it. Both are conveniences, and neither
is evidence: a filename is a claim about bytes, and this project's standing rule
is that a figure citing data is read out of that data rather than carried along
beside it.

So the pointer names the file, the bytes are hashed here, and a disagreement
between the two is a hard failure rather than a silent copy. The hash we serve
under is a property of what we serve.

**sha256, not sha1.** skyledger.py uses sha1 because the Ledger's build does.
This matches the Lockouts build so that our served filename is byte-identical to
the one that repo produced, which makes "are the two repos in sync?" answerable
by comparing two strings. Do not unify them on one algorithm for tidiness — each
mirrors its own upstream, and that is the property worth having.

ABSENT REPO
-----------
A rebuild must work on a machine that does not have the Lockouts repo, exactly
as with skyledger.py and geometry.py. Where the repo is missing, the committed
copy stands and this exits 0.
"""
import datetime
import glob
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

OUT = 'assets/lockouts.json'
APPDIR = 'public/app'
PREFIX = 'eqls-lockouts'
NAME_RE = re.compile(r'^' + PREFIX + r'\.[0-9a-f]{8}\.html$')


def find_repo():
    """The Lockouts repo, wherever it is.

    An env var wins. Otherwise walk up from ROOT looking for the directory,
    which is what makes this work from a git worktree as well as from the main
    checkout — skyledger.py's fixed `../ClaSkyApp` and `../../ClaSkyApp`
    candidates resolve to neither when ROOT is `.claude/worktrees/<name>`, so
    the Ledger silently keeps its committed copy there. Same fault, avoided.
    """
    env = os.environ.get('EQLS_LOCKOUTS_REPO', '')
    if env and os.path.isdir(env):
        return os.path.abspath(env)
    here = ROOT
    for _ in range(7):
        cand = os.path.join(here, 'EQLSLockouts')
        if os.path.exists(os.path.join(cand, 'public', 'app')):
            return os.path.abspath(cand)
        parent = os.path.dirname(here)
        if parent == here:
            break
        here = parent
    return None


def source_build(repo):
    """(path, filename) of the build to copy, named by the repo's own pointer.

    `latest.txt` is how that repo says which build is current. Falling back to
    "whatever single file is in there" is deliberate and bounded: more than one
    candidate and no pointer is ambiguous, and this refuses to guess.
    """
    appdir = os.path.join(repo, 'public', 'app')
    pointer = os.path.join(appdir, 'latest.txt')
    if os.path.exists(pointer):
        named = open(pointer, encoding='utf-8').read().strip()
        if not NAME_RE.match(named):
            sys.exit(f"lockouts: {pointer} names {named!r}, which is not a "
                     f"hashed build filename")
        path = os.path.join(appdir, named)
        if not os.path.exists(path):
            sys.exit(f"lockouts: latest.txt names {named}, which is not in "
                     f"{appdir}. Rebuild the Lockouts app")
        return path, named
    found = sorted(os.path.basename(p)
                   for p in glob.glob(os.path.join(appdir, f'{PREFIX}.*.html'))
                   if NAME_RE.match(os.path.basename(p)))
    if len(found) == 1:
        return os.path.join(appdir, found[0]), found[0]
    if not found:
        return None, None
    sys.exit(f"lockouts: {len(found)} builds in {appdir} and no latest.txt to "
             f"say which is current: {', '.join(found)}")


def keep_committed():
    """Report on the copy already in the tree, and exit clean."""
    if not os.path.exists(OUT):
        print('lockouts: repo not found and no committed record — nothing to '
              'copy, and nothing links this tool yet either')
        return 0
    rec = json.load(open(OUT, encoding='utf-8'))
    served = os.path.join(APPDIR, rec['app']['file'])
    state = 'present' if os.path.exists(served) else 'MISSING'
    print(f"lockouts: repo not found, keeping the committed copy "
          f"({rec['app']['file']}, {state})")
    return 0


def main():
    repo = find_repo()
    if repo is None:
        return keep_committed()

    src, named = source_build(repo)
    if src is None:
        print(f'lockouts: {repo} holds no built app yet')
        return keep_committed()

    blob = open(src, 'rb').read()
    sha256 = hashlib.sha256(blob).hexdigest()
    short = sha256[:8]
    name = f'{PREFIX}.{short}.html'

    # The pointer is a claim about these bytes. Where it disagrees, something
    # upstream is stale and copying either one would publish a lie about which
    # build this is.
    if name != named:
        sys.exit(f"lockouts: {named} hashes to {short}, so the Lockouts repo's "
                 f"own filename does not describe its contents. Rebuild it "
                 f"there; do not copy a build whose name is already wrong")

    os.makedirs(APPDIR, exist_ok=True)
    # A hashed URL only defeats a stale cache if the stale FILE stops being
    # served. Otherwise every build accumulates and an old link works forever.
    dropped = []
    for old in sorted(glob.glob(os.path.join(APPDIR, f'{PREFIX}.*.html'))):
        base = os.path.basename(old)
        if base != name and NAME_RE.match(base):
            os.remove(old)
            dropped.append(base)

    # Bytes, verbatim. Re-encoding would change the hash the name promises.
    with open(os.path.join(APPDIR, name), 'wb') as fh:
        fh.write(blob)

    rec = dict(
        read=datetime.date.today().isoformat(),
        source=f'public/app/{named}',
        pointer='latest.txt',
        # No package.json in that repo, so there is no version to record. It is
        # null rather than absent, and null rather than invented: a version
        # string typed here would be the exact fault this file exists to avoid.
        version=None,
        # PROMOTED 26 AUG 2026. This was false for one day by order, while the
        # app sat copied and unlinked pending Session D.
        #
        # It stays a field rather than becoming an assumption because check.py
        # reads it: with promoted true, an unlinked served app is a build
        # FAILURE, and a page linking it while this said false would also fail.
        # Flipping it and flipping the check are one act - a gate that only
        # warns after promotion is the dead-check class, and a dead check looks
        # exactly like a passing one.
        promoted=True,
        app=dict(file=name, hash=short, sha256=sha256, bytes=len(blob),
                 kb=round(len(blob) / 1024)),
    )
    json.dump(rec, open(OUT, 'w', encoding='utf-8', newline='\n'),
              indent=1, sort_keys=True)

    # Read off the record, not typed beside it. This line said "unpromoted"
    # literally, and went on saying it after the flag flipped - a caption
    # disagreeing with the data one line above it, which is the fault this file
    # already documents twice.
    print(f"lockouts: {name} ({rec['app']['kb']} KB, "
          f"{'promoted' if rec['promoted'] else 'unpromoted'})"
          + (f", dropped {', '.join(dropped)}" if dropped else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
