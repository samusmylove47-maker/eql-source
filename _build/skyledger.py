"""public/app/ — the Sky Ledger browser build, copied in and content-hashed.

WHAT THIS DOES
--------------
Sky Ledger is a separate project. Its browser build is one self-contained HTML
file with no server, no upload and no external request, so this site can serve
it directly: a reader clicks a link and the tool runs, with nothing to install.

This copies that file into `public/app/sky-ledger.<hash>.html`, where `<hash>`
is the first eight hex characters of its SHA-1, deletes any earlier copy, and
records what it copied in `assets/sky-ledger.json`.

WHY THE HASH IS NOT OPTIONAL
----------------------------
`assets/site.css` was one stable URL with no version on it, and on 16 Aug 2026
a browser that had seen the old file kept serving it: an entire redesign was
invisible to every returning reader. The fix there was `?v=<hash>` in
`_partials.py`. An application is worse than a stylesheet in the same failure,
because a stale copy of a log parser is not obviously stale — it runs, it fills
the page, and it is simply the old one. A different build is a different URL
here, so a cache can never serve the wrong version of it.

WHY IT MUST NOT FAIL WITHOUT THE LEDGER REPO
--------------------------------------------
Same rule as `_build/geometry.py` and the game's `.s3d` archives: a rebuild has
to work on a machine that does not have the source. So the copied file and
`assets/sky-ledger.json` are both committed, and when the Ledger repo is absent
this prints what it skipped and leaves the committed pair alone.

WHY THE DATASET COUNTS ARE READ RATHER THAN TYPED
-------------------------------------------------
CLAUDE.md: a figure that cites a dataset must be read out of that dataset at
build time. The tool page prints how many turn-in items are wanted by more than
one test, and that is the whole argument for promoting it — so it is counted
here, from the Ledger's own `sky.json`, and the page prints the count.

It has already earned that. The Ledger's README says "Holding one Djinni War
Blade does not make three quests ready"; the dataset says that blade is wanted
by two tests, not three. The claim is right and the example was stale, which is
exactly the fault a typed figure makes.

Run by build.sh before anything that links or quotes the app.
"""
import hashlib, json, os, sys, datetime, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

OUT = 'assets/sky-ledger.json'
APPDIR = 'public/app'

# Where the Ledger repo might be. An env var wins, so a machine that keeps it
# somewhere else needs no edit here.
CANDIDATES = [os.environ.get('SKY_LEDGER_REPO', ''),
              os.path.join(ROOT, '..', '..', 'ClaSkyApp'),
              os.path.join(ROOT, '..', 'ClaSkyApp')]


def find_repo():
    for c in CANDIDATES:
        if c and os.path.exists(os.path.join(c, 'SkyLedger.html')):
            return os.path.abspath(c)
    return None


def dataset_counts(repo):
    """The invariants the Ledger's own test suite asserts, counted here.

    `demand` maps a turn-in item to the list of tests that want it, so an item
    wanted by more than one test is contested — which is the property no other
    Sky tracker has, and the reason this one is promoted.
    """
    with open(os.path.join(repo, 'sky.json'), encoding='utf-8') as fh:
        d = json.load(fh)
    demand = d['demand']
    contested = {k: len(v) for k, v in demand.items() if len(v) > 1}
    runes = [k for k in demand if k.lower().startswith('wind rune')]
    top = sorted(contested.items(), key=lambda kv: (-kv[1], kv[0]))[:3]
    return dict(
        classes=len(d['classes']),
        quests=sum(len(c['quests']) for c in d['classes'].values()),
        turnin_slots=sum(len(q['items']) for c in d['classes'].values()
                         for q in c['quests']),
        items=len(demand),
        contested=len(contested),
        runes=len(runes),
        runes_contested=sum(1 for k in runes if len(demand[k]) > 1),
        most_contested_item=top[0][0] if top else None,
        most_contested_tests=top[0][1] if top else None,
        contested_top=[[k, n] for k, n in top],
    )


# THE PUBLISHED DOWNLOADS.
#
# The tool page offered no download until 17 August 2026, because nothing was
# published anywhere linkable and a button going nowhere is worse than a
# sentence saying so. A GitHub release exists now, and the page prints its
# sizes rather than describing them.
#
# The sizes are read off the packages in the Ledger's dist/ rather than typed,
# so they cannot drift from what a reader actually downloads. The URL is a
# constant because it is an address, not a measurement. On a machine without
# the Ledger repo the sizes fall back to whatever the committed record already
# holds, the same way the app copy does.
RELEASE_BASE = ('https://github.com/samusmylove47-maker/sky-ledger/'
                'releases/download')
ASSETS = (('overlay', 'SkyLedger-v{v}-windows.zip'),
          ('browser', 'SkyLedger-v{v}-browser-only.zip'))


def release_info(repo, version):
    if not version:
        return None
    out = dict(tag=f'v{version}',
               page=('https://github.com/samusmylove47-maker/sky-ledger/'
                     f'releases/tag/v{version}'))
    prev = {}
    try:
        prev = (json.load(open(OUT, encoding='utf-8')).get('release') or {})
    except (OSError, ValueError):
        pass
    for key, pattern in ASSETS:
        fname = pattern.format(v=version)
        out[key] = dict(url=f'{RELEASE_BASE}/v{version}/{fname}', file=fname)
        path = os.path.join(repo, 'dist', fname) if repo else None
        if path and os.path.exists(path):
            out[key]['bytes'] = os.path.getsize(path)
        elif prev.get(key, {}).get('bytes'):
            out[key]['bytes'] = prev[key]['bytes']
        if out[key].get('bytes'):
            out[key]['mb'] = round(out[key]['bytes'] / 1e6, 1)
    return out



def main():
    repo = find_repo()
    if repo is None:
        if os.path.exists(OUT):
            rec = json.load(open(OUT, encoding='utf-8'))
            served = os.path.join(APPDIR, rec['app']['file'])
            state = 'present' if os.path.exists(served) else 'MISSING'
            print(f"sky ledger: repo not found, keeping the committed copy "
                  f"({rec['app']['file']}, {state})")
        else:
            print("sky ledger: repo not found and no committed record — "
                  "the tool page will not build")
        return 0

    src = os.path.join(repo, 'SkyLedger.html')
    blob = open(src, 'rb').read()
    sha1 = hashlib.sha1(blob).hexdigest()
    short = sha1[:8]
    name = f'sky-ledger.{short}.html'

    os.makedirs(APPDIR, exist_ok=True)
    # One build at a time. A hashed URL only stops a stale cache if the stale
    # FILE also stops being served — otherwise every old build accumulates and
    # an old link keeps working forever, which is a slower version of the same
    # fault.
    dropped = []
    for old in sorted(glob.glob(os.path.join(APPDIR, 'sky-ledger.*.html'))):
        if os.path.basename(old) != name:
            os.remove(old)
            dropped.append(os.path.basename(old))

    dst = os.path.join(APPDIR, name)
    # Written as bytes: the file is the application, verbatim, and re-encoding
    # it would change the hash this page promises.
    with open(dst, 'wb') as fh:
        fh.write(blob)

    try:
        version = json.load(open(os.path.join(repo, 'package.json'),
                                 encoding='utf-8'))['version']
    except (OSError, ValueError, KeyError):
        version = None

    rec = dict(
        read=datetime.date.today().isoformat(),
        source='SkyLedger.html',
        version=version,
        app=dict(file=name, hash=short, sha1=sha1, bytes=len(blob),
                 kb=round(len(blob) / 1024)),
        dataset=dataset_counts(repo),
        release=release_info(repo, version),
    )
    json.dump(rec, open(OUT, 'w', encoding='utf-8', newline='\n'),
              indent=1, sort_keys=True)

    print(f"sky ledger: {name} ({rec['app']['kb']} KB, v{version})"
          + (f", dropped {', '.join(dropped)}" if dropped else ""))
    return 0


if __name__ == '__main__':
    sys.exit(main())
