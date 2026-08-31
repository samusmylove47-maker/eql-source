"""EQLS_SKIP_APPS — build the site without republishing anyone else's app.

WHAT THIS FIXES, MEASURED RATHER THAN PREDICTED
-----------------------------------------------
`_build/skyledger.py` and `_build/lockouts.py` copy a browser build out of a
sibling repository into `public/app/` under a content hash. That is correct and
it is how those tools reach a reader.

The cost is that they run on EVERY `./build.sh`, on every branch. A session
working on something else entirely picks up whatever the sibling repos have
built since the branch point, and cannot avoid it — the copiers find the repo by
walking up from ROOT, so being in a worktree does not help.

On 31 August 2026 one branch about copy edits hit this THREE TIMES in a night,
dragging in a 17 KB lockout rebuild each time. And reverting the copy is not
enough on its own: four generators embed the build hash in the pages they
write, so after a revert the site goes on naming a file that no longer exists,
which is the one hard constraint here — an existing public URL must not 404.
The full recovery each time was: revert `assets/lockouts.json` and `public/app/`,
re-run build1, build2, build30 and build23, then re-stamp.

With three tools shipping this way, every unrelated branch makes three publish
decisions nobody made.

WHAT IT DOES NOT DO
-------------------
It does not change what is served. The committed copy stays exactly as it is,
which is the point: a branch about the home page should publish the same app it
found. Set it when you are NOT working on an app, unset it when you are.

Default is unset, and unset means the existing behaviour. A guard that silently
stopped a real publish from happening would be worse than the problem — the
Sky Ledger served a build three releases old for a day, to testers, because a
copier no-opped quietly.

AND THE SKIP IS ANNOUNCED, NEVER SILENT
---------------------------------------
Both copiers already have a `keep_committed(reason)` path that names why nothing
was copied, written after that stale-build incident. The skip reuses it with its
own reason rather than pretending the repo was missing, because "not found" and
"deliberately skipped" are different facts and a build log that confuses them is
how the next stale build gets served.

    EQLS_SKIP_APPS=1 ./build.sh
"""
import os

VAR = 'EQLS_SKIP_APPS'

# The reason string both copiers pass to keep_committed(), so the two cannot
# describe the same condition two different ways.
REASON = f'{VAR} is set'


def skipping():
    """True when this build must not copy an app in from a sibling repo.

    Any non-empty value except the ones that conventionally mean "off". Written
    permissively on purpose: someone reaching for this has already decided they
    do not want the copy, and `EQLS_SKIP_APPS=true` failing silently because it
    was not the literal string `1` would be its own small version of the fault
    this file exists to fix.
    """
    v = os.environ.get(VAR, '').strip().lower()
    return bool(v) and v not in ('0', 'false', 'no', 'off')
