import os, sys, glob, datetime, json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "_build"))
from _partials import public_path   # one address rule, shared with the canonical tag
CFG=json.load(open("site.config.json", encoding="utf-8")) if os.path.exists("site.config.json") else {}
DOMAIN=os.environ.get("SITE_URL", CFG.get("site_url","")).rstrip("/")
if not DOMAIN or "REPLACE-ME" in DOMAIN:
    raise SystemExit("site_url is not set in site.config.json — set it and rerun")
today=datetime.date.today().isoformat()

# LASTMOD IS A MODIFICATION DATE, NOT A BUILD DATE.
#
# Until 1 Sep 2026 every one of the 715 entries carried date.today(). Two costs:
#
#   1. It told crawlers every page on the site was modified today, every day
#      anyone rebuilt. That is a figure asserting something the data does not
#      support, on 715 pages, and it is this project's oldest rule.
#   2. Any rebuild on a new day rewrote all 715 lines, so a pull request opened
#      after one carried a 715-line diff nobody made and a real one-line change
#      to this file would be invisible inside it. That is how a change hides.
#
# A FILESYSTEM MTIME WOULD NOT HAVE FIXED IT, which is what docs/BACKLOG.md
# warned: every build rewrites every page, so the mtime is the build date again
# with extra steps. The honest source is git - the last commit that actually
# changed the file.
#
# A page modified in the working tree and not yet committed gets today, because
# it is being changed now and its git date would be one commit stale. So an
# unchanged page keeps its date and a changed page moves, which is the whole
# property wanted.
#
# WITH NO GIT, OR A CLONE TOO SHALLOW TO CARRY HISTORY, this falls back to
# today for every page AND SAYS SO. A silent fallback here would reproduce the
# exact fault being fixed while looking like the fix.
def _page_dates():
    import subprocess
    try:
        log = subprocess.run(["git", "log", "--format=%cs", "--name-only", "--", "public/"],
                             capture_output=True, text=True, encoding="utf-8",
                             errors="replace", timeout=120)
        if log.returncode != 0:
            return {}, "git log failed"
        seen, date = {}, None
        for line in log.stdout.splitlines():
            line = line.strip()
            if len(line) == 10 and line[4] == "-" and line[7] == "-":
                date = line
            elif line and date and line not in seen:
                seen[line] = date
        if not seen:
            return {}, "git history carries no public/ paths (shallow clone?)"
        dirty = subprocess.run(["git", "status", "--porcelain", "--", "public/"],
                               capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=120)
        for line in dirty.stdout.splitlines():
            path = line[3:].strip()
            if path:
                seen[path] = today          # changed now, so today is the truth
        return seen, ""
    except (OSError, subprocess.SubprocessError) as e:
        return {}, f"{type(e).__name__}: {e}"


PAGE_DATE, _date_why = _page_dates()
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
    pages.append(f"  <url><loc>{DOMAIN}/{public_path(p)}</loc><lastmod>{PAGE_DATE.get("public/" + p, today)}</lastmod><priority>{pri}</priority></url>")
open("public/sitemap.xml","w",encoding="utf-8",newline="\n").write(
 '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
 + "\n".join(pages) + "\n</urlset>\n")
# WE DISALLOW NOTHING, AND THAT IS A DECISION RATHER THAN AN OVERSIGHT.
#
# Ruled 2 Sep 2026 by the Director and this session jointly, on the owner's
# instruction to settle what we withhold from OpenAI, ClaudeBot and other
# reputable crawlers. The answer is: nothing.
#
# THE DECIDING ARGUMENT IS ABOUT THIS SITE, not about openness in general.
# CLAUDE.md's founding premise is that this community repeats classic EverQuest
# text as though it were Legends fact, and the site exists to displace it. AI
# assistants are now a principal channel carrying that error. Blocking reputable
# AI crawlers would remove the correction from the channel doing the damage. For
# another site that is a trade-off; here it is self-defeating.
#
# Three supporting reasons, kept because a rule resting on one is fragile:
#   * robots.txt binds only the compliant. The real choice is "present in AI
#     answers or absent from them", with the scrapers unaffected either way.
#   * eqprogression.com refuses us, and docs/SOURCES.md tells us to ask a human
#     to fetch it by hand. Their Disallow did not protect the content; it turned
#     automated access into manual access. Ours would do the same.
#   * public/data/*.vN.json is a PUBLIC CONTRACT that check.py defends. Telling
#     machines not to read the thing built for machines to read deters a tool
#     author and not one scraper.
#
# THE OWNER WAS TOLD IT IS NOT SYMMETRICALLY REVERSIBLE. Removing a rule later
# costs one line; material already ingested cannot be un-ingested. The ruling
# stands because the content is already fetched wholesale by every visitor's
# browser and already reachable by every non-compliant actor, so the marginal
# ingestion a Disallow would prevent is small and the correction it would
# suppress is the site's whole purpose.
#
# `Disallow: /_build/` WAS REMOVED, NOT FORGOTTEN. public/_build has never
# existed, so the origin has never served that path: our only exclusion rule
# named nothing. A robots.txt carrying a decorative rule is worse than one
# carrying none, because it reads as a policy somebody thought about.
#
# No per-bot stanzas, no ai.txt, no llms.txt. A stanza naming GPTBot and
# ClaudeBot would be the most visible statement on the site about a thing we are
# choosing not to enforce.
open("public/robots.txt","w",encoding="utf-8",newline="\n").write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
_dates = len(set(PAGE_DATE.values()))
print(f"sitemap.xml + robots.txt written for {DOMAIN} ({len(pages)} urls, "
      + (f"{_dates} distinct modification date(s) from git)" if PAGE_DATE
         else f"ALL STAMPED TODAY - no per-page dates: {_date_why})"))
