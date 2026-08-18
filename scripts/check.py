#!/usr/bin/env python3
"""EQL Source — pre-commit validation.

Run before every commit:  python3 scripts/check.py
Exit code 0 = safe to commit. Anything else is a blocker, not a warning.
"""
import json, os, re, sys, glob

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
if not os.path.exists("public/assets/vendor/three.min.js"):
    fail("assets/vendor/three.min.js is missing — the 3D viewer will not load")

# 4b. tier discipline: the badge CSS must exist and the scale must be published
css = open("public/assets/site.css", encoding="utf-8").read()
for cls in (".tier", ".t1", ".t3", ".t5"):
    if cls not in css:
        fail(f"assets/site.css has lost {cls} — the source-tier badge system is load-bearing")
if os.path.exists("index.html"):
    h = open("index.html", encoding="utf-8").read()
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
            fail(f"{page_key(_p) if 'page_key' in dir() else _p}: script uses "
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
