import os, glob, datetime, json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
CFG=json.load(open("site.config.json")) if os.path.exists("site.config.json") else {}
DOMAIN=os.environ.get("SITE_URL", CFG.get("site_url","")).rstrip("/")
if not DOMAIN or "REPLACE-ME" in DOMAIN:
    raise SystemExit("site_url is not set in site.config.json — set it and rerun")
today=datetime.date.today().isoformat()
pages=[]
for p in sorted(glob.glob("*.html")+glob.glob("dungeons/*.html")+glob.glob("raids/*.html")+glob.glob("tools/*.html")):
    pri="1.0" if p=="index.html" else ("0.8" if p.endswith("index.html") else "0.6")
    pages.append(f"  <url><loc>{DOMAIN}/{p}</loc><lastmod>{today}</lastmod><priority>{pri}</priority></url>")
open("sitemap.xml","w").write(
 '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
 + "\n".join(pages) + "\n</urlset>\n")
open("robots.txt","w").write(f"User-agent: *\nAllow: /\nDisallow: /_build/\n\nSitemap: {DOMAIN}/sitemap.xml\n")
print(f"sitemap.xml + robots.txt written for {DOMAIN} ({len(pages)} urls)")
