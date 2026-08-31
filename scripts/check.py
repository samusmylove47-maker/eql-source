#!/usr/bin/env python3
"""EQL Source — pre-commit validation.

Run before every commit:  python3 scripts/check.py
Exit code 0 = safe to commit. Anything else is a blocker, not a warning.
"""
import json, os, re, sys, glob

# THIS FILE COULD CRASH WHILE PRINTING A FAILURE, AND EXIT 1 WITH NO REASON.
#
# On Windows a piped stdout is encoded with the locale default, cp1252, which
# cannot represent U+2212 MINUS SIGN. 141 of the site's recorded coordinates use
# U+2212 rather than an ASCII hyphen, and the withheld-coordinate rule quotes
# the coordinate it found — so the failure most worth reporting was the one that
# killed the reporter. The caller saw a non-zero exit and an empty explanation,
# which reads exactly like a check that fired for no stated reason.
#
# Found 27 Aug 2026 when gate_selftest.py reported WRONG CHECK with an empty
# detail for a rule that was working perfectly. It reproduced only without
# PYTHONIOENCODING set, which is how it survived every run made from a terminal
# that happened to have it.
#
# A validator must be able to print any failure it can detect.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
fails, warns = [], []

def fail(m): fails.append(m)
def warn(m): warns.append(m)

# Everything published lives under public/. Nothing outside it is deployed,
# so nothing outside it is a page.
#
# public/app/ is the exception and is not a page at all: it holds the Sky Ledger
# browser build, copied in verbatim by _build/skyledger.py under a content hash.
# It is a self-contained application with its own chrome, its own stylesheet and
# no favicon of ours, so every check below would fail it for not being one of
# our pages. Excluding it is only safe because it is checked on its own terms
# further down — an exclusion with nothing behind it is how a blind spot starts.
pages = [p for p in glob.glob("public/*.html") + glob.glob("public/*/*.html")
         if not os.path.basename(p).startswith("_")
         and not p.replace(os.sep, "/").startswith("public/app/")]
if len(pages) < 20:
    fail(f"only {len(pages)} pages found — expected 20 or more. Did a build fail?")

# 1. every internal href/src resolves
SCRIPTS = re.compile(r"<script\b.*?</script>", re.S | re.I)
for p in pages:
    h = open(p, encoding="utf-8", errors="replace").read()
    markup = SCRIPTS.sub("", h)   # href/src inside JS strings are not links
    base = os.path.dirname(p)
    for ref in re.findall(r'(?:href|src)="([^"]+)"', markup):
        if ref.startswith(("http", "#", "mailto:", "data:", "javascript:")):
            continue
        tgt = os.path.normpath(os.path.join(base, ref.split("#")[0].split("?")[0]))
        if tgt and not os.path.exists(tgt):
            fail(f"{p} -> broken link: {ref}")

    for ref in re.findall(r'<script[^>]+src="([^"]+)"', h):
        if ref.startswith(("http", "//")): continue
        tgt = os.path.normpath(os.path.join(base, ref))
        if tgt and not os.path.exists(tgt):
            fail(f"{p} -> missing script: {ref}")

# 2. chrome, favicon and styling present on every page
for p in pages:
    h = open(p, encoding="utf-8", errors="replace").read()
    if "favicon.svg" not in h:
        fail(f"{p} is missing its favicon link")
    if "site-bar" not in h and "ns-bar" not in h:
        fail(f"{p} has no site navigation bar")
    if "site.css" not in h and "<style>" not in h:
        fail(f"{p} has no stylesheet at all")
    if not re.search(r"<title>.+?</title>", h, re.S):
        fail(f"{p} has no title")

# 3. zones-index drives navigation — it must match what is on disk
zi = "assets/zones-index.json"
if not os.path.exists(zi):
    fail("assets/zones-index.json is missing — navigation cannot build")
else:
    Z = json.load(open(zi, encoding="utf-8"))
    accents, plates = {}, {}
    for z in Z:
        s = z["slug"]
        if not os.path.exists(f"public/dungeons/{s}.html"):
            fail(f"zones-index lists '{s}' but dungeons/{s}.html does not exist")
        if not os.path.exists(f"_build/source/{s}.html"):
            warn(f"no source file for '{s}' — ./build.sh cannot regenerate it")
        a = z["accent"].upper()
        if a in accents:
            fail(f"accent {a} used by both {accents[a]} and {s} — accents must be unique")
        accents[a] = s
        if z["plate"] in plates:
            fail(f"plate number {z['plate']} used twice: {plates[z['plate']]} and {s}")
        plates[z["plate"]] = s
    # verification level must be explicit, valid, and match what the pages claim
    VALID = {"full", "partial", "none"}
    counts = {"full": 0, "partial": 0, "none": 0}
    for z in Z:
        lv = z.get("verify_level")
        if lv not in VALID:
            fail(f"{z['slug']}: verify_level is {lv!r} — must be one of {sorted(VALID)}")
        else:
            counts[lv] += 1
        if lv in ("partial", "none") and not z.get("verify_gate"):
            fail(f"{z['slug']} is {lv} but does not say which gate is open — name it in verify_gate")
    for page in ("public/index.html", "public/dungeons/index.html"):
        if os.path.exists(page):
            h = open(page, encoding="utf-8").read()
            claim = re.search(r"(\d+) verified to the full three-gate standard", h)
            if claim and int(claim.group(1)) != counts["full"]:
                fail(f"{page} claims {claim.group(1)} verified but zones-index says {counts['full']} "
                     f"— never publish a higher number than the data supports")

    # Every zone must be reachable from the dungeon index. This lives here rather
    # than on the home page: the home page deliberately does not enumerate the
    # plates — that is what the index is for — so requiring it to link all ten
    # would force the page back into being a table of contents for itself.
    if os.path.exists("public/dungeons/index.html"):
        h = open("public/dungeons/index.html", encoding="utf-8").read()
        missing = [z["slug"] for z in Z if f'{z["slug"]}.html' not in h]
        if missing:
            fail(f"dungeons/index.html does not link {len(missing)} zone(s): {', '.join(missing)}")

# 4. the 3D viewer must not depend on a CDN
for p in glob.glob("public/raids/*.html"):
    h = open(p, encoding="utf-8").read()
    if "cdnjs" in h or "unpkg" in h or "jsdelivr" in h:
        fail(f"{p} loads a script from a CDN — vendor it into assets/vendor/ instead")
# Vendored libraries must resolve where a page actually asks for one. This
# asserted unconditionally that three.min.js exists, "or the 3D viewer will not
# load" — a viewer withdrawn on 17 Aug 2026 whose generator was deleted with it.
# It failed the build to protect a dependency that no shipped page has requested
# since, and told whoever hit it that a nonexistent feature was about to break.
#
# The real invariant is CLAUDE.md's no-CDN rule: a page that loads a vendored
# library must find it on disk. Where nothing loads it, there is nothing to
# check and nothing to assert.
# page_key IS gate.py's, AND THIS FILE CALLED IT WITHOUT HAVING IT.
#
# Line 151 below called `page_key(p)` bare. check.py imports json, os, re, sys,
# glob and subprocess — and never defines or imports page_key, which exists only
# at gate.py:157. So the one branch that reports a missing vendored script would
# have raised `NameError` at module scope: no message, no accumulated failures
# printed, just a traceback and exit 1. **The check would fire and report
# nothing.** A session shipping a page that loads a vendored library would have
# debugged check.py instead of their own missing file.
#
# It has never been taken because no page under public/ references
# assets/vendor/ at all — `_vendor_refs` is 0 — which is exactly how a dead
# branch survives review.
#
# Line 567 calls the same name behind `if 'page_key' in dir()`, which at module
# scope is permanently false, so that site has silently been printing the raw
# path all along. Somebody met this once, guarded one site and left the other.
#
# Imported from gate rather than redefined: two implementations of one string
# transform is how the counts in this repository used to disagree. gate.py
# imports only stdlib, so moving the path insert above the first use is safe.
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from gate import page_key

_vendor_refs = 0
for p in pages:
    h = open(p, encoding="utf-8", errors="replace").read()
    for m in re.finditer(r'src="[^"]*?(?:\.\./)*assets/vendor/([^"?]+)', h):
        _vendor_refs += 1
        if not os.path.exists(os.path.join("public/assets/vendor", m.group(1))):
            fail(f"{page_key(p)} loads assets/vendor/{m.group(1)}, which is not on disk")
print(f"  vendored script references checked: {_vendor_refs}")

# 4a2. NO PAGE MAY FETCH FROM ANOTHER ORIGIN ON LOAD.
#
# On 30 August 2026, 715 of 717 published pages preconnected to
# fonts.googleapis.com and loaded a stylesheet from it, disclosing every reader's
# IP address to Google before anything rendered. Several of those pages printed
# "Nothing transmitted" while doing it, and the site had published that exact
# criticism about a collaborator's application.
#
# The faces are self-hosted now, which makes the disclosure stop existing rather
# than be disclosed better. THIS IS THE CHECK THAT KEEPS IT THAT WAY. One CDN
# link added in six months would restore the fault silently, and the reason it
# went unseen for so long is that nothing was looking: conformance.js aborts
# every non-file: request, so it has always measured a page whose remote fetches
# never happened.
#
# WHAT IT DOES NOT COVER, deliberately. A canonical URL, an og:image and a
# Twitter card all name https://eqlsource.com and are metadata rather than
# fetches — the reader's browser requests none of them. Only constructs the
# browser acts on at load are checked.
_EGRESS = [
    (re.compile(r'<link[^>]+rel=["\'][^"\']*(?:preconnect|dns-prefetch|preload|prefetch)', re.I),
     "a preconnect or prefetch hint"),
    # Only link types the browser FETCHES. rel="canonical" and rel="alternate"
    # name a URL without requesting it, and every page carries a canonical — the
    # first draft of this rule failed all 714 pages on exactly that.
    (re.compile(r'<link[^>]+rel=["\'](?:stylesheet|icon|apple-touch-icon|manifest)["\'][^>]*href=["\'](?:https?:)?//', re.I),
     "a stylesheet, icon or manifest from another origin"),
    (re.compile(r'<link[^>]+href=["\'](?:https?:)?//[^>]*rel=["\'](?:stylesheet|icon|apple-touch-icon|manifest)["\']', re.I),
     "a stylesheet, icon or manifest from another origin"),
    (re.compile(r'<script[^>]+src=["\'](?:https?:)?//', re.I), "a script from another origin"),
    (re.compile(r'<(?:img|iframe|video|audio|source|embed)[^>]+src=["\'](?:https?:)?//', re.I),
     "media from another origin"),
    (re.compile(r'@import\s+(?:url\()?["\']?(?:https?:)?//', re.I), "a CSS @import from another origin"),
    (re.compile(r'url\(\s*["\']?(?:https?:)?//', re.I), "a CSS url() pointing at another origin"),
]
# AND IT COVERS public/app/, WHICH `pages` DELIBERATELY EXCLUDES.
#
# `pages` drops public/app/ at line 47 because those files are applications
# rather than pages and none of the chrome rules apply to them. That exclusion
# is right for chrome and WRONG HERE, and I shipped it wrong: the two served
# bundles are the artifacts most likely to fetch something, and they were the
# only two files under public/ this rule could not see.
#
# Found 31 August by testing it rather than reading it — a stylesheet link
# injected into the Sky Ledger bundle produced no finding at all. This is the
# same shape as conformance.js skipping public/app/ for three shipped render
# failures, and it is the fourth check this month whose documented exclusion
# turned out to cover something it should not have.
#
# It matters now rather than in principle: docs/BUNDLE-CONTRACT.md tells Session
# E that "no fetch, no XHR, no WebSocket" is checkable and that I will check it.
# Until this loop included them, that sentence was a promise rather than a gate.
_APPS = sorted(p.replace(os.sep, "/") for p in glob.glob("public/app/*.html"))
_egress_hits = 0
for p in pages + _APPS:
    h = open(p, encoding="utf-8", errors="replace").read()
    for rx, what in _EGRESS:
        m = rx.search(h)
        if m:
            _egress_hits += 1
            fail(f"{p} loads {what}: {m.group(0)[:110]!r}. Published pages and "
                 f"served applications carry their own assets — see "
                 f"public/assets/fonts/LICENSES.md and docs/BUNDLE-CONTRACT.md")
            break
if not _egress_hits:
    print(f"  fetching another origin on load: 0 of {len(pages)} page(s) "
          f"and 0 of {len(_APPS)} served app(s)")

# 4a3. EVERY SELF-HOSTED FACE MUST RESOLVE, FROM EVERY PAGE THAT LINKS IT.
#
# Session B hit this exact failure self-hosting their own faces and named it
# better than I would have: root-absolute font paths 404 under a subdirectory,
# and "every page silently fell back to the local stacks — the one failure state
# that looks like a design choice rather than a bug."
#
# That is the whole hazard. A missing typeface does not throw, does not warn, and
# does not look broken; it looks like a slightly different design. Nothing in
# this repository would have caught it: conformance.js aborts non-file: requests
# so it never loaded a webfont in its life, and a page with no font renders
# perfectly well.
#
# So both halves are checked, and BY RESOLVING FILES rather than by reading the
# stylesheet — B's other instruction, which is the same lesson as "open the page"
# one layer down. A stylesheet that looks right and points at nothing is the
# failure being prevented.
_fcss = "public/assets/fonts/fonts.css"
if not os.path.exists(_fcss):
    fail(f"{_fcss} is missing — run python3 _build/fetchfonts.py")
else:
    _ftext = open(_fcss, encoding="utf-8").read()
    _fdir = os.path.dirname(_fcss)
    _urls = re.findall(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", _ftext)
    _missing = [u for u in _urls
                if not u.startswith("data:")
                and not os.path.exists(os.path.normpath(os.path.join(_fdir, u)))]
    if _missing:
        fail(f"{_fcss} names {len(_missing)} font file(s) that are not on disk: "
             f"{', '.join(_missing[:4])}. Every page would fall back silently")
    elif not _urls:
        fail(f"{_fcss} declares no font files at all — every page would fall "
             f"back to system stacks and look like a design choice")
    # And the link itself, resolved per page, because the href is relative and
    # its depth differs. One wrong `rel` and a whole directory loses its faces.
    _badlink = []
    for p in pages:
        h = open(p, encoding="utf-8", errors="replace").read()
        m = re.search(r'<link[^>]+href="([^"]*fonts/fonts\.css)(?:\?[^"]*)?"', h)
        if not m:
            continue
        if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(p), m.group(1)))):
            _badlink.append(p)
    if _badlink:
        fail(f"{len(_badlink)} page(s) link a fonts.css that does not resolve "
             f"from their own directory, e.g. {_badlink[0]}")
    else:
        print(f"  self-hosted faces: {len(_urls)} file(s), all resolving")

# 4b. tier discipline: the badge CSS must exist and the scale must be published
css = open("public/assets/site.css", encoding="utf-8").read()
for cls in (".tier", ".t1", ".t3", ".t5"):
    if cls not in css:
        fail(f"assets/site.css has lost {cls} — the source-tier badge system is load-bearing")
# THE PATH IS public/index.html AND HAS BEEN SINCE THE SITE MOVED THERE.
#
# This read a root index.html that has not existed for the life of this layout,
# so the whole block below — including the assertion whose own message says "the
# scale is the reason the site exists and must stay published on the home page"
# — has never once executed. Session B proved it by mutation: deleting
# "Aggregator" from the home page entirely left check.py green.
#
# `if os.path.exists(...)` around an assertion is the shape to distrust. A
# missing file silently skips the check instead of failing it, so a guard that
# stops matching reads exactly like a guard that passes. gate_selftest.py now
# carries a case for precisely this, because the only reason this was found is
# that somebody went looking.
#
# Repointing it turns it GREEN, not red: all five tier names are on the page
# and the badge count is 3. The check was right and had simply been unplugged.
if not os.path.exists("public/index.html"):
    fail("public/index.html is missing — the home page is the site's front door "
         "and the tier-scale assertions below cannot run without it")
else:
    h = open("public/index.html", encoding="utf-8").read()
    # What matters is that the scale is published and legible on the home page,
    # not which markup renders it. This used to require a literal "tier-scale"
    # class, which broke the moment the scale was redesigned even though every
    # tier was still on the page.
    named = sum(1 for t in ("Developer", "wiki data", "community guides",
                            "Aggregator", "classic prose") if t.lower() in h.lower())
    if named < 5:
        fail(f"index.html names only {named} of the 5 source tiers — the scale is "
             f"the reason the site exists and must stay published on the home page")
    if h.count('class="tier') < 3:
        warn("the home page shows fewer than three example tier badges")

# 4c. the design system's real constraints
#
# This used to warn on any border-radius or box-shadow. That was a previous
# session's taste encoded as validation, and docs/DESIGN.md now permits both in
# service of hierarchy. Removed: a checker should catch breakage, not opinions.
#
# What is checked instead is the constraint that is actually load-bearing — the
# typeface count. A face too many is the usual way a considered site drifts.
#
# Cinzel was added on 16 Aug 2026 and the count went from three to four. That is
# a decision, not drift: it is an inscriptional Roman capital, it holds the top
# two display levels only, and Saira Condensed stays underneath it as the
# workhorse. The site read as documentation rather than as a reference for this
# game, and a display face with an actual point of view is most of the fix.
FACES = {"Cinzel", "Saira Condensed", "IBM Plex Mono", "Public Sans"}
declared = set(re.findall(r'font-family:\s*"([^"]+)"', css))
extra = declared - FACES
if extra:
    warn(f"assets/site.css uses {sorted(extra)} beyond the four site faces")
if "cdnjs" in css or "unpkg" in css:
    fail("assets/site.css references a CDN")

# 5. house style
for p in pages:
    h = open(p, encoding="utf-8", errors="replace").read()
    for word in ("Lorem ipsum", "TODO", "FIXME", "PLACEHOLDER", "XXX"):
        if word in h:
            fail(f"{p} contains '{word}' — placeholder text must not ship")
    if "REPLACE-ME" in h:
        warn(f"{p} still contains REPLACE-ME")
if not os.path.exists("site.config.json"):
    fail("site.config.json is missing — site name and URL have no source of truth")
else:
    cfg = json.load(open("site.config.json", encoding="utf-8"))
    if not cfg.get("site_url") or "REPLACE-ME" in cfg["site_url"]:
        fail("site.config.json has no real site_url — the sitemap will be wrong")
    if os.path.exists("public/sitemap.xml") and cfg["site_url"].rstrip("/") not in open("public/sitemap.xml", encoding="utf-8").read():
        fail("sitemap.xml does not match site_url in site.config.json — run ./build.sh")
    for p_ in pages:
        h = open(p_, encoding="utf-8", errors="replace").read()
        if cfg["site_name"] not in h and "ns-bar" not in h:
            warn(f"{p_} does not carry the site name")

# ---------------------------------------------------------------- source integrity
# check.py validates the generated site, which means a broken *generator* passes
# it. build.sh was once committed with merge conflict markers still in it and
# this script reported all clear, because the HTML it had produced earlier was
# still fine. The site was healthy; the thing that builds it was not.
#
# So: no tracked source file may carry conflict markers, and build.sh must at
# least parse. Neither is expensive and both catch a class of fault that is
# invisible to every other check here.
import subprocess
CONFLICT = ("<" * 7, "=" * 7, ">" * 7)
tracked = subprocess.run(["git", "ls-files"], capture_output=True, text=True).stdout.split()
for f_ in tracked:
    if not os.path.isfile(f_) or f_.endswith((".png", ".jpg", ".svg", ".ico", ".woff2")):
        continue
    try:
        txt = open(f_, encoding="utf-8", errors="replace").read()
    except OSError:
        continue
    for line in txt.splitlines():
        if line.startswith(CONFLICT[0]) or line.startswith(CONFLICT[2]) or line.rstrip() == CONFLICT[1]:
            fail(f"{f_} still contains merge conflict markers")
            break

if os.path.exists("build.sh"):
    r = subprocess.run(["bash", "-n", "build.sh"], capture_output=True, text=True)
    if r.returncode != 0:
        fail(f"build.sh does not parse: {r.stderr.strip().splitlines()[0] if r.stderr.strip() else 'syntax error'}")
    gens = [ln.split()[-1] for ln in open("build.sh", encoding="utf-8")
            if ln.startswith("python3 _build/")]
    for g in gens:
        if not os.path.exists(g):
            fail(f"build.sh runs {g}, which does not exist")
    on_disk = {f"_build/{f_}" for f_ in os.listdir("_build")
               if f_.endswith(".py") and f_ not in (
                   "_partials.py", "changelog.py", "logstats.py",
                   "extract_faction.py", "withheld.py", "ogcards.py",
                   # Imported by the page generators rather than run: it turns
                   # the committed zone geometry into drawable SVG. Nothing to
                   # schedule, so an orphan warning here would be permanent.
                   "heroart.py",
                   # Also imported, not run: it reads the Mistmoore backstab
                   # evidence out of measured.json so four pages cannot carry a
                   # stale copy of it again.
                   "backstab.py",
                   # The same idea asked of a zone rather than of one claim:
                   # rate, roster, hazards and loot read out of the measured
                   # sessions at build time. backstab.py answers "is this
                   # sentence still true"; this answers "what is this zone
                   # worth", and both are imported by the pages that cite them.
                   "zonestats.py",
                   # Substituted into every survey by build3.py: the
                   # experience ranking and the measured-boss counts, so a
                   # page cannot type an ordinal that goes stale in silence.
                   "derived.py",
                   # Derives each zone accent's text variant for both grounds
                   # and refuses any that cannot clear 4.5:1. Imported by the
                   # generators that emit per-card tokens rather than run on
                   # its own; run it directly to print the table.
                   "accents.py",
                   # Rewrites _build/source/*.html in place, so it is hand-run
                   # like prose_budget.py. A script that rewrites its own
                   # inputs on every build eventually rewrites something it
                   # should not.
                   "warmshift.py",
                   # Draws the Mistmoore chart from zone-geometry.json and the
                   # recorded /loc values, and writes it back into
                   # _build/source/mistmoore-map.html between sentinels. Same
                   # reason as warmshift.py: build3.py imports that page
                   # verbatim and takes no substitutions, so the drawing has to
                   # live in the authored file — but a build step that rewrote
                   # an authored page every run would fight its author. Re-run
                   # it after any change to the geometry or the coordinates and
                   # diff; if the page moves, the page was stale.
                   "mistmoorecarto.py",
                   # Read the game's .s3d archives, so they are run by hand and
                   # their output is committed. A rebuild has to work on a
                   # machine with no EverQuest Legends install.
                   "geometry.py", "skyislands.py", "palette.py",
                   # Fetches the four faces from Google once so no reader ever
                   # fetches them again. Needs the network, and a rebuild must
                   # work on a machine that has none. Its output —
                   # public/assets/fonts/ and the stylesheet beside it — is
                   # committed. Same rule as geometry.py and ogcards.py.
                   "fetchfonts.py",
                   # Reads combat logs out of state/logs/, which are
                   # gitignored because they can carry private chat. Run
                   # by hand; only the derived counts are committed.
                   "raidstats.py",
                   # Reads inventory dumps out of state/inventory/, gitignored
                   # because they are a named person's account contents. Run
                   # by hand; only name-to-item-ID is committed.
                   "inventory.py")}
    for g in sorted(on_disk - set(gens)):
        warn(f"{g} exists but build.sh never runs it")

# ---- is public/ actually what the sources would produce? --------------------
# A generator that crashes leaves the previous output in place, and every check
# below passes against it. build.sh stamps a fingerprint of its inputs; if the
# stamp does not match, the tree is stale and nothing else here means anything.
try:
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import stamp
    want = stamp.fingerprint()
    got = json.load(open("state/last-build.json", encoding="utf-8"))["inputs"]
    if want != got:
        fail("public/ is stale — a source changed since the last successful "
             "./build.sh, or a generator crashed part way. Re-run ./build.sh")
except FileNotFoundError:
    warn("state/last-build.json is missing — run ./build.sh to stamp the tree")
except Exception as e:
    warn(f"could not verify build freshness: {type(e).__name__}: {e}")

# ---- stray control characters in source ------------------------------------
# Three separate times a regex has shipped with a literal backspace (0x08) where
# a word-boundary escape was meant. It compiles, it matches nothing, and every check built on it
# reports success exactly as it does when the site is clean. That is the worst
# failure mode available, so it is caught here rather than remembered.
CTRL = {8: "backspace, probably a word-boundary escape that lost its backslash",
        1: "SOH, probably a group backreference that lost its backslash",
        2: "STX, probably a group backreference that lost its backslash",
        12: "formfeed", 7: "bell", 11: "vertical tab"}
for src in sorted(glob.glob("_build/**/*.py", recursive=True) + glob.glob("scripts/*.py")):
    try:
        body = open(src, encoding="utf-8").read()
    except OSError:
        continue
    for code, why in CTRL.items():
        n = body.count(chr(code))
        if n:
            fail(f"{src} contains {n} literal control character(s) 0x{code:02x} — {why}")

# ---- every slug in the data has a page ---------------------------------------
# The Index writes its links in the browser, from the `u` field, so the link
# checker above never sees them: a missing item page would be a 404 nothing on
# this site could detect. The slug is generated once in extract.py precisely so
# the two sides cannot drift, and this proves they have not.
try:
    _ix = json.load(open("assets/index-data.json", encoding="utf-8"))
except Exception as e:
    fail(f"index-data.json unreadable: {e}")
    _ix = {"items": [], "named": []}
for _folder, _key in (("items", "items"), ("named", "named")):
    # Fragments are deliberately page-less: they are not items. See
    # assets/catalogue-fixes.json for why, and build17.py for where they print.
    _missing = sorted({r["u"] for r in _ix[_key]
                       if r.get("kind") != "fragment"
                       and not os.path.exists(f"public/{_folder}/{r['u']}.html")})
    if _missing:
        fail(f"The Index links {len(_missing)} {_folder} page(s) that do not "
             f"exist: {', '.join(_missing[:4])}")
    _orphan = sorted(set(os.path.basename(p)[:-5]
                         for p in glob.glob(f"public/{_folder}/*.html"))
                     - {r["u"] for r in _ix[_key] if r.get("kind") != "fragment"}
                     - {"index"})
    if _orphan:
        fail(f"public/{_folder}/ holds {len(_orphan)} page(s) no longer in the "
             f"data — a rename left them behind: {', '.join(_orphan[:4])}")

# ---- a tool's data constants are all defined --------------------------------
# On 14 August the Sky tracker's dataset moved out of the page into sky.json.
# ORDER - the class picker's display order - was a separate top-level constant
# sitting just past the block that moved, and it went with it. `ORDER.map(...)`
# on an undefined ORDER throws before a single button is built, so the picker
# rendered nothing, the trio could never reach three, and the Build button was
# permanently disabled. **check.py passed all 721 pages while the tool was
# unusable**, because every check here reads the DOM the page ships and none of
# them run its JavaScript.
#
# This is the cheap 90%: the data constants in these tools are ALL CAPS by
# convention, so every all-caps identifier the script uses must be declared
# somewhere in that script. It would have caught ORDER instantly. It does not
# replace opening the page, and nothing here should be read as proof a tool
# works - only that it cannot fail this particular way again.
_JS_GLOBALS = {"JSON", "Math", "Object", "Array", "String", "Number", "Boolean",
               "Date", "RegExp", "Map", "Set", "Promise", "URL", "URLSearchParams",
               "Error", "TypeError", "NaN", "Infinity", "IDBKeyRange", "DOMParser",
               "TextEncoder", "TextDecoder", "Intl", "BigInt", "Symbol", "Proxy",
               "Reflect", "WeakMap", "WeakSet", "ArrayBuffer", "Uint8Array"}
_DECL = re.compile(r"\b(?:const|let|var|function|class)\s+([A-Z][A-Z0-9_]{1,})\b")
# `const EF=[...],EFM="..."` declares two. The second has no keyword in front of
# it, so it has to be matched separately or it reads as an undefined reference.
_DECL2 = re.compile(r"[,;]\s*([A-Z][A-Z0-9_]{1,})\s*=")
_USE = re.compile(r"(?<![.\w$'\"])([A-Z][A-Z0-9_]{1,})\b")


def _strip_js(js):
    """Comments and string literals are not code. Section banners like
    /* ===== DATA ===== */ and hex colours inside strings were read as
    references by the first version, which reported 54 faults and zero real
    ones."""
    js = re.sub(r"/\*.*?\*/", " ", js, flags=re.S)
    js = re.sub(r"(?m)//[^\n]*$", " ", js)
    # Escaped quotes matter: a single \" inside an embedded JSON blob desyncs a
    # naive "[^"]*" and exposes the whole rest of the line as if it were code,
    # which reported nineteen faults in a page that had none.
    js = re.sub(r'"(?:[^"\\\n]|\\.)*"', '""', js)
    js = re.sub(r"'(?:[^'\\\n]|\\.)*'", '""', js)
    js = re.sub(r"`(?:[^`\\]|\\.)*`", '""', js, flags=re.S)
    js = re.sub(r"#[0-9A-Fa-f]{3,8}\b", " ", js)
    return js


for _p in sorted(glob.glob("public/tools/*.html")):
    _h = open(_p, encoding="utf-8").read()
    for _m in re.finditer(r"<script\b[^>]*>(.*?)</script>", _h, re.S | re.I):
        _js = _strip_js(_m.group(1))
        if len(_js) < 400:
            continue
        _declared = set(_DECL.findall(_js)) | set(_DECL2.findall(_js)) | _JS_GLOBALS
        # a key inside an object literal is not a reference to anything
        _stripped = re.sub(r"\b([A-Z][A-Z0-9_]{1,})\s*:", "", _js)
        _used = set(_USE.findall(_stripped))
        _missing = sorted(_used - _declared)
        if _missing:
            # Was `page_key(_p) if 'page_key' in dir() else _p`. At module scope
            # dir() is the globals and page_key was never among them, so that
            # guard was constant-false and this printed the raw path every time.
            # It is imported properly now, so the label is the one intended.
            fail(f"{page_key(_p)}: script uses "
                 f"{len(_missing)} undefined constant(s) — the tool will throw "
                 f"before it renders: {', '.join(_missing[:5])}")

# ---- the curated corrections have not gone stale ----------------------------
# assets/catalogue-fixes.json says of itself: "check.py fails if a name here no
# longer appears in the data, so this file cannot rot quietly." It did not.
# There was no such check, so the file could have rotted in exactly the silence
# it claimed to be protected from - and a fix keyed to a name that a survey has
# since re-worded does nothing at all, invisibly.
#
# Every left-hand key must still be reachable: a fragment or group by that name
# in the mined data, an alias or split by the name it renames FROM, and a
# resolved fragment by the name it renames TO.
try:
    _fx = json.load(open("assets/catalogue-fixes.json", encoding="utf-8"))
except Exception as e:
    fail(f"catalogue-fixes.json unreadable: {e}")
    _fx = {}
_item_names = {r["n"] for r in _ix["items"]}
_named_names = {r["n"] for r in _ix["named"]}
_resolved = {k: v["name"] for k, v in _fx.get("fragment_resolved", {}).items()}
# A fix that RENAMES is checked against the survey sources, not the mined data:
# by the time the data exists the old name has already been replaced, so
# looking for it downstream would fail every rename that is working correctly.
# A fix that only LABELS - fragments, groups - survives into the data and is
# checked there.
_srctext = ""
for _p in glob.glob("_build/source/*.html"):
    _srctext += open(_p, encoding="utf-8").read()
for _label, _keys, _pool, _where in (
        ("fragment", set(_fx.get("fragments", {})), _item_names, "the mined data"),
        ("group", set(_fx.get("groups", [])), _item_names, "the mined data"),
        ("resolved fragment", set(_resolved.values()), _item_names, "the mined data"),
        ("alias", set(_fx.get("aliases", {})), None, "any survey source"),
        ("split", set(_fx.get("split_named", {})), None, "any survey source")):
    if _pool is not None:
        _stale = sorted(k for k in _keys if k not in _pool)
    else:
        _stale = sorted(k for k in _keys if k not in _srctext)
    if _stale:
        fail(f"catalogue-fixes.json lists {len(_stale)} {_label}(s) that no "
             f"longer appear in {_where}, so the correction does nothing: "
             f"{', '.join(repr(s) for s in _stale[:4])}")

# ---- the served application is the one we say it is -------------------------
# public/app/ is excluded from the page checks above because it is not a page.
# This is what stands in their place, and it is the check the stylesheet needed
# and did not have on 16 Aug 2026: an asset served under a stable URL goes stale
# in a reader's cache silently, and a stale copy of a log parser is not visibly
# stale — it runs, it fills the page, and it is simply the old build.
#
# So: the record must exist, the file it names must be on disk, its name must
# still be a hash of its own contents, no earlier build may still be sitting
# there, and some page must link it. A hashed URL that nothing points at is a
# 176 KB file nobody can reach.
try:
    _sl = json.load(open("assets/sky-ledger.json", encoding="utf-8"))
except Exception as e:
    fail(f"assets/sky-ledger.json unreadable: {e} — the Sky Ledger pages "
         f"print every figure from it and cannot build without it")
    _sl = None
if _sl:
    import hashlib
    _app = _sl["app"]
    _served = os.path.join("public", "app", _app["file"])
    if not os.path.exists(_served):
        fail(f"assets/sky-ledger.json names {_app['file']}, which is not in "
             f"public/app/. Run python3 _build/skyledger.py")
    else:
        _blob = open(_served, "rb").read()
        _got = hashlib.sha1(_blob).hexdigest()
        if not _app["file"].endswith(f".{_got[:8]}.html"):
            fail(f"public/app/{_app['file']} hashes to {_got[:8]}, so its URL "
                 f"no longer describes its contents — a cache would serve the "
                 f"wrong build. Re-run python3 _build/skyledger.py")
        if _got != _app["sha1"] or len(_blob) != _app["bytes"]:
            fail(f"public/app/{_app['file']} does not match the sha1 or the "
                 f"byte count recorded in assets/sky-ledger.json")
    _stale = sorted(os.path.basename(p) for p in glob.glob("public/app/sky-ledger.*.html")
                    if os.path.basename(p) != _app["file"])
    if _stale:
        fail(f"public/app/ still holds {len(_stale)} earlier Sky Ledger "
             f"build(s): {', '.join(_stale)}. A hashed URL only stops a stale "
             f"cache if the stale file stops being served")
    _linked = any(_app["file"] in open(p, encoding="utf-8", errors="replace").read()
                  for p in pages)
    if not _linked:
        fail(f"public/app/{_app['file']} is served but no page links it")

# ---- the EQLS Lockouts app, copied but deliberately not promoted ------------
# Same guard as the Sky Ledger's, with one clause deliberately different.
#
# The record must exist, the file it names must be on disk, its name must still
# be a hash of its own contents, and no earlier build may still be sitting
# there. All of that is identical, and all of it catches the same fault: an
# asset served under a stable URL going stale in a reader's cache in silence.
#
# WHAT IS DIFFERENT, AND WHY IT IS A WARN
# The Sky Ledger block ends by FAILING when no page links the hashed file. That
# is right for a promoted tool and wrong here: by the Director's order of
# 25 August 2026 this app is copied without a tools/ page or a landing band,
# pending a report from Session D. So an unlinked file is the intended state.
#
# It is a WARN rather than nothing at all, because a check that quietly permits
# an interim state permits it forever. The warning names the promotion that is
# owed, appears in every build, and goes away by itself the moment a page links
# the file. When that happens, turn this into the same fail() the Ledger uses.
try:
    _lk = json.load(open("assets/lockouts.json", encoding="utf-8"))
except FileNotFoundError:
    _lk = None                              # not copied yet, which is allowed
except Exception as e:
    fail(f"assets/lockouts.json unreadable: {e}")
    _lk = None
if _lk:
    import hashlib
    _lapp = _lk["app"]
    _lserved = os.path.join("public", "app", _lapp["file"])
    if not os.path.exists(_lserved):
        fail(f"assets/lockouts.json names {_lapp['file']}, which is not in "
             f"public/app/. Run python3 _build/lockouts.py")
    else:
        _lblob = open(_lserved, "rb").read()
        # sha256 here, sha1 for the Ledger. Each mirrors its own upstream build
        # so that "are the two repos in sync?" is a string comparison. This is
        # not an inconsistency to tidy away.
        _lgot = hashlib.sha256(_lblob).hexdigest()
        if not _lapp["file"].endswith(f".{_lgot[:8]}.html"):
            fail(f"public/app/{_lapp['file']} hashes to {_lgot[:8]}, so its URL "
                 f"no longer describes its contents. Re-run "
                 f"python3 _build/lockouts.py")
        if _lgot != _lapp["sha256"] or len(_lblob) != _lapp["bytes"]:
            fail(f"public/app/{_lapp['file']} does not match the sha256 or the "
                 f"byte count recorded in assets/lockouts.json")
    _lstale = sorted(os.path.basename(p)
                     for p in glob.glob("public/app/eqls-lockouts.*.html")
                     if os.path.basename(p) != _lapp["file"])
    if _lstale:
        fail(f"public/app/ still holds {len(_lstale)} earlier Lockouts "
             f"build(s): {', '.join(_lstale)}. A hashed URL only stops a stale "
             f"cache if the stale file stops being served")
    _llinked = any(_lapp["file"] in open(p, encoding="utf-8", errors="replace").read()
                   for p in pages)
    # THE GATE IS DERIVED FROM THE FLAG, NOT HAND-EDITED TO MATCH IT.
    #
    # This was a warn() for one day, while the app was copied and deliberately
    # unlinked. Promotion flipped `promoted` in assets/lockouts.json, and the
    # check follows the flag rather than a person remembering to come back:
    #
    #   promoted, not linked  -> FAIL. Exactly the Sky Ledger's rule. A hashed
    #                            URL nothing points at is a file nobody reaches.
    #   linked, not promoted  -> FAIL. The data and the pages disagree.
    #   neither               -> warn. The interim state is still expressible,
    #                            and still says out loud that it is interim.
    #
    # Writing it this way is the point. A check hand-edited to match a state it
    # does not read goes stale the moment the state changes, and a dead check
    # looks exactly like a passing one.
    _lpromoted = bool(_lk.get("promoted"))
    if _lpromoted and not _llinked:
        fail(f"public/app/{_lapp['file']} is served and promoted, but no page "
             f"links it. Run python3 _build/build30.py, or set promoted:false")
    elif _llinked and not _lpromoted:
        fail(f"a page links public/app/{_lapp['file']}, but "
             f"assets/lockouts.json records promoted:false. The tool is "
             f"promoted or it is not; the data and the pages must agree")
    elif not _lpromoted:
        warn(f"public/app/{_lapp['file']} is served and no page links it, and "
             f"assets/lockouts.json records promoted:false, so this is "
             f"deliberate. Promotion flips both together")

# 4a4. THE GAP ENGINE PAGE MUST PUBLISH ITS REFUSALS, AND ALL OF THEM.
#
# The Director's instruction was that refusals render "as prominently as"
# deltas. That is a judgement a later session can shade while believing it is
# complying — trimming one, moving them below the fold, folding them into a
# disclosure — and each step looks reasonable on its own.
#
# So the checkable version: every refusal in the data appears on the page, and
# the page carries as many refusal entries as delta entries at minimum. The
# reason is E's and it is the same as this site's own rule about never deleting
# a flagged gap: a tool that silently omits what it cannot do fails open,
# because a short list of findings reads as "nothing else to improve".
#
# Also guarded here, though the schema makes it nearly impossible: no delta may
# reach the page carrying anything but a difference. build31.py refuses to build
# such a thing; this catches a page edited by hand afterwards.
try:
    _ge = json.load(open("assets/gap-engine.json", encoding="utf-8"))
except FileNotFoundError:
    _ge = None
except Exception as e:
    fail(f"assets/gap-engine.json unreadable: {e}")
    _ge = None
if _ge:
    _gp = "public/tools/gap-engine.html"
    if not _ge.get("_fixture"):
        fail("assets/gap-engine.json is not marked _fixture. That page renders "
             "SYNTHETIC data only — a real report must never be published there")
    if not os.path.exists(_gp):
        fail(f"{_gp} is missing — run python3 _build/build31.py")
    else:
        _gh = open(_gp, encoding="utf-8", errors="replace").read()
        _missing = [r["lane"] for r in _ge.get("refusals", [])
                    if r.get("lane") and r["lane"] not in _gh]
        if _missing:
            fail(f"{_gp} omits {len(_missing)} refusal(s) the data holds: "
                 f"{', '.join(_missing)}. A tool that hides what it declined "
                 f"reads as having found nothing left to improve")
        # ge-r is refusals ONLY. The no-rate rows inside `measured` are
        # ge-nr: they are refusals in spirit and they are not the list this
        # rule is about, and while they shared a class this printed
        # "4 refusal(s)" against 3 in the data and compared the wrong
        # quantity — a dropped refusal could have been masked by a resist row.
        _nr = _gh.count('class="ge-r"')
        _nd = _gh.count('class="ge-d"')
        if _nr < _nd:
            fail(f"{_gp} renders {_nd} delta(s) and only {_nr} refusal(s). "
                 f"Refusals carry equal weight there by instruction")
        for _d in _ge.get("deltas", []):
            if not str(_d.get("unit", "")).startswith("dps_delta"):
                fail(f"{_gp}: delta on lane {_d.get('lane')!r} carries unit "
                     f"{_d.get('unit')!r}, which is not a difference. A modelled "
                     f"absolute must never reach a page")
        if not _missing and _nr >= _nd:
            print(f"  gap engine: {_nd} delta(s), {_nr} refusal(s), all published")

# ---- the propagation gate ---------------------------------------------------
# Everything above checks that a page is well formed. This checks that facts
# agree with each other and with the data they came from, which is the class of
# fault that actually shipped. See scripts/gate.py.
sys.path.insert(0, os.path.join(ROOT, "scripts"))
try:
    import gate
    gate.run(pages, fail, warn)
except Exception as e:                      # a broken gate must not pass silently
    fail(f"the propagation gate did not run: {type(e).__name__}: {e}")

# ---- the public data contract is intact -------------------------------------
# /data/*.vN.json is published as a promise: fields are never removed and never
# change type, because other people's tools read them. That promise is only
# worth anything if something enforces it, so the shape is declared here rather
# than left to whoever next edits _build/publicdata.py.
#
# Adding a key is fine and needs no change here. Removing one, or renaming it,
# should fail loudly and require a deliberate decision to publish a v2.
# `floor` is the smallest each collection may become before the build refuses.
#
# ADDED 18 AUG 2026, BECAUSE EMPTY WAS THE ONLY FAILURE THIS COULD SEE.
# The emptiness rule below catches a dataset that lost everything. It cannot
# catch one that lost most of itself, and the consolidation had exactly that
# waiting: assets/planar.json is read by _build/sightings.py to match planar
# armour, index-data.json contains none of it, and the two catalogues share a
# hundred names. Losing planar.json would have taken data.items from 277 to 177
# — a third of a published dataset gone, still valid JSON, still the right
# shape, still not empty. Green.
#
# The numbers are observations, not targets: each is the count on 18 Aug 2026,
# recorded in the comment beside it, with the floor set low enough that ordinary
# churn does not trip it and far above the failure it exists to catch. Raising a
# floor as a dataset grows is fine. Lowering one is a decision that needs a
# reason in the commit, exactly like raising a prose ceiling.
_CONTRACT = {
    "sky.v1.json": dict(
        top={"name", "version", "title", "description", "source", "schema",
             "terms", "stability", "notes", "data", "hash"},
        data={"sources", "islands", "ladder", "order", "efreeti", "classes"},
        # Fixed sets: the zone has ten islands and the game sixteen classes.
        # These do not churn, so their floors sit at the count itself.
        floor={"sources": 4, "islands": 10, "ladder": 10, "order": 16,
               "efreeti": 2, "classes": 16}),
    "sightings.v1.json": dict(
        top={"name", "version", "title", "description", "source", "schema",
             "terms", "stability", "notes", "data", "hash"},
        data={"items"},
        floor={"items": 220}),        # 277 on 18 Aug 2026
    "zones.v1.json": dict(
        top={"name", "version", "title", "description", "source", "schema",
             "terms", "stability", "notes", "data", "hash"},
        data={"zones"},
        floor={"zones": 13}),         # 13 surveys; a zone is never unsurveyed
    "items.v1.json": dict(
        top={"name", "version", "title", "description", "source", "schema",
             "terms", "stability", "notes", "data", "hash"},
        data={"items"},
        floor={"items": 205}),        # 257 on 18 Aug 2026
}
try:
    _idx = json.load(open("public/data/index.json", encoding="utf-8"))
except Exception as e:
    fail(f"public/data/index.json unreadable: {e}")
    _idx = {"datasets": []}
_listed = set()
for _d in _idx.get("datasets", []):
    _fname = _d["url"].rsplit("/", 1)[-1]
    _listed.add(_fname)
    _p = os.path.join("public", "data", _fname)
    if not os.path.exists(_p):
        fail(f"the data index lists {_fname}, which is not on disk")
        continue
    try:
        _body = json.load(open(_p, encoding="utf-8"))
    except ValueError as e:
        fail(f"public/data/{_fname} is not valid JSON: {e}")
        continue
    _want = _CONTRACT.get(_fname)
    if not _want:
        fail(f"public/data/{_fname} is published with no declared contract in "
             f"check.py — add one before shipping it, or consumers have no "
             f"promise to rely on")
        continue
    _missing = sorted(_want["top"] - set(_body))
    if _missing:
        fail(f"{_fname} has lost top-level field(s) {_missing} — that breaks "
             f"the v1 contract. Publish a v2 instead of changing v1")
    _missing = sorted(_want["data"] - set(_body.get("data") or {}))
    if _missing:
        fail(f"{_fname} data has lost field(s) {_missing} — that breaks the v1 "
             f"contract. Publish a v2 instead of changing v1")
    # An empty dataset is the failure faction-data.json had: still valid JSON,
    # still the right shape, and carrying nothing.
    for _k, _v in (_body.get("data") or {}).items():
        if isinstance(_v, (dict, list)) and len(_v) == 0:
            fail(f"{_fname}: data.{_k} is empty. A published dataset that lost "
                 f"its contents is worse than one that failed to build")
        # And the failure that is not emptiness. See the floors above.
        elif isinstance(_v, (dict, list)):
            _floor = (_want.get("floor") or {}).get(_k)
            if _floor is not None and len(_v) < _floor:
                fail(f"{_fname}: data.{_k} holds {len(_v)}, below its recorded "
                     f"floor of {_floor}. A published dataset does not lose a "
                     f"large fraction of itself by accident — find what stopped "
                     f"feeding it. If the drop is real and intended, lower the "
                     f"floor in check.py and say why in the commit")
for _extra in sorted(set(os.path.basename(p) for p in glob.glob("public/data/*.json"))
                     - _listed - {"index.json"}):
    fail(f"public/data/{_extra} is published but not listed in index.json, so "
         f"nobody can discover it")

# ---- the tools actually run ------------------------------------------------
# Everything above reads the HTML a page ships. None of it runs the page's
# JavaScript, which is how the Sky tracker shipped with an empty class picker
# and a green check. scripts/toolsmoke.js executes each tool under a stub DOM
# and asserts it neither throws nor renders nothing.
#
# Skipped, loudly, where node is absent: this must not become a check that
# quietly does nothing on a machine without a JS runtime.
try:
    _node = subprocess.run(["node", "--version"], capture_output=True, text=True)
    _have_node = _node.returncode == 0
except (OSError, FileNotFoundError):
    _have_node = False
if not _have_node:
    warn("node is not on PATH, so the tool smoke test did not run. The tools "
         "are unverified in this build: run scripts/toolsmoke.js where node is "
         "available before trusting it.")
else:
    _r = subprocess.run(["node", os.path.join(ROOT, "scripts", "toolsmoke.js")],
                        capture_output=True, text=True, cwd=ROOT)
    if _r.returncode != 0:
        for _line in (_r.stdout or "").splitlines():
            _line = _line.strip()
            if _line.startswith("[THREW") or _line.startswith("[RENDERED"):
                fail("tool smoke test: " + _line)
            elif _line and not _line.startswith("[") and "failed" in _line:
                fail("tool smoke test: " + _line)
        if not any("tool smoke test" in f for f in fails):
            fail(f"tool smoke test failed: {(_r.stderr or _r.stdout)[:300]}")

print(f"checked {len(pages)} pages")
for w in warns: print(f"  WARN  {w}")
for f in fails: print(f"  FAIL  {f}")
if fails:
    print(f"\n{len(fails)} blocker(s). Do not commit until these are fixed.")
    sys.exit(1)
print(f"\nAll checks passed" + (f" with {len(warns)} warning(s)." if warns else "."))
