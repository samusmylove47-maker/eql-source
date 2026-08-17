import os, glob, datetime, json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
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
    pri="1.0" if p=="index.html" else ("0.8" if p.endswith("index.html") else "0.6")
    pages.append(f"  <url><loc>{DOMAIN}/{p}</loc><lastmod>{today}</lastmod><priority>{pri}</priority></url>")
open("public/sitemap.xml","w",encoding="utf-8",newline="\n").write(
 '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
 + "\n".join(pages) + "\n</urlset>\n")
open("public/robots.txt","w",encoding="utf-8",newline="\n").write(f"User-agent: *\nAllow: /\nDisallow: /_build/\n\nSitemap: {DOMAIN}/sitemap.xml\n")
print(f"sitemap.xml + robots.txt written for {DOMAIN} ({len(pages)} urls)")
