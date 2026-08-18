import os, sys, glob, datetime, json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "_build"))
from _partials import public_path   # one address rule, shared with the canonical tag
CFG=json.load(open("site.config.json", encoding="utf-8")) if os.path.exists("site.config.json") else {}
DOMAIN=os.environ.get("SITE_URL", CFG.get("site_url","")).rstrip("/")
if not DOMAIN or "REPLACE-ME" in DOMAIN:
    raise SystemExit("site_url is not set in site.config.json — set it and rerun")
today=datetime.date.today().isoformat()
pages=[]
# Pages live under public/ and the URL must not contain it: public/ is the
# deploy root, so public/tools/x.html is served at /tools/x.html.
for p in sorted(glob.glob("public/*.html")+glob.glob("public/*/*.html")):
    p=p.replace(os.sep,"/")   # Windows globs return backslashes; URLs must not
    p=p[len("public/"):]
    # public/app/ is the Sky Ledger application, served verbatim under a
    # content hash. The hash changes with every release, so listing it would
    # publish a URL that stops existing - and the page a reader should find is
    # tools/sky-ledger.html, which describes it and links it.
    if p.startswith("app/"):
        continue
    # 404.html is an error page. It was listed here until 18 Aug 2026, which
    # asks a search engine to index the page a reader lands on when nothing
    # matched. It is also the one page with no canonical, deliberately.
    if p=="404.html":
        continue
    pri="1.0" if p=="index.html" else ("0.8" if p.endswith("index.html") else "0.6")
    # THE SAME RULE THE CANONICAL TAG USES, imported rather than repeated.
    # This wrote {DOMAIN}/{p} until 18 Aug 2026, so all 716 entries ended .html
    # and every one of them 307-redirected. A sitemap of redirecting URLs is
    # indexed as redirects rather than as pages, and it contradicted the
    # canonical each of those pages declares. Two files deriving one address two
    # ways is how they came to disagree; there is one way now.
    pages.append(f"  <url><loc>{DOMAIN}/{public_path(p)}</loc><lastmod>{today}</lastmod><priority>{pri}</priority></url>")
open("public/sitemap.xml","w",encoding="utf-8",newline="\n").write(
 '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
 + "\n".join(pages) + "\n</urlset>\n")
open("public/robots.txt","w",encoding="utf-8",newline="\n").write(f"User-agent: *\nAllow: /\nDisallow: /_build/\n\nSitemap: {DOMAIN}/sitemap.xml\n")
print(f"sitemap.xml + robots.txt written for {DOMAIN} ({len(pages)} urls)")
