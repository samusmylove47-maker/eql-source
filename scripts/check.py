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
pages = [p for p in glob.glob("public/*.html") + glob.glob("public/*/*.html")
         if not os.path.basename(p).startswith("_")]
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
# three typefaces. A fourth is the usual way a considered site starts to drift.
FACES = {"Saira Condensed", "IBM Plex Mono", "Public Sans"}
declared = set(re.findall(r'font-family:\s*"([^"]+)"', css))
extra = declared - FACES
if extra:
    warn(f"assets/site.css uses {sorted(extra)} beyond the three site faces")
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
               if f_.endswith(".py") and f_ not in ("_partials.py", "changelog.py",
                                                    "geometry.py", "logstats.py",
                                                    "extract_faction.py", "withheld.py")}
    for g in sorted(on_disk - set(gens)):
        warn(f"{g} exists but build.sh never runs it")

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

print(f"checked {len(pages)} pages")
for w in warns: print(f"  WARN  {w}")
for f in fails: print(f"  FAIL  {f}")
if fails:
    print(f"\n{len(fails)} blocker(s). Do not commit until these are fixed.")
    sys.exit(1)
print(f"\nAll checks passed" + (f" with {len(warns)} warning(s)." if warns else "."))
