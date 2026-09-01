#!/usr/bin/env python3
"""The local preview server, serving addresses the way the host serves them.

WHY THIS EXISTS
---------------
`.claude/launch.json` ran `python -m http.server --directory public`, which maps
a URL to a file path and does no guessing. That was fine while every internal
link ended in `.html`. Internal links went extensionless on 1 September 2026, and
measured against that server immediately afterwards:

    /tools/lockouts        404
    /tools/lockouts.html   200
    /dungeons/             200   (a directory, so index.html is served)
    /dungeons              200   (redirected to /dungeons/)

23,140 of 35,848 internal links - 64% - answered 404 locally while every one of
them worked in production. The site was fine and the preview of it was broken,
which is the worse way round: it trains you to distrust the preview.

The mapping this adds is the one Cloudflare's `html_handling` already performs on
the live host, and NOTHING LOCAL REPRODUCED IT. That is the actual defect. A
preview server that resolves addresses differently from the host is not
previewing the site; it is previewing a different site that happens to share its
files, and every difference between them is a bug you cannot see and a bug you
see that is not there.

WHAT IT DOES, and deliberately nothing more:

  /x            ->  x.html            the extensionless form the site now links
  /dir/         ->  dir/index.html    inherited from SimpleHTTPRequestHandler
  /x.html       ->  x.html            still served, because the host still serves
                                      it - old links and bookmarks are the whole
                                      reason the redirect stays
  anything else ->  404.html, with a real 404 status, matching
                    wrangler.jsonc's not_found_handling: "404-page"

It does NOT emulate the host's 307 from /x.html to /x. Production sends one and
this does not, and that difference is deliberate: the redirect exists for links
already in the wild, no page on this site emits a `.html` link any more, and a
local redirect would only make the preview slower at reproducing a hop no reader
takes. If that ever needs testing, test it against a preview deploy, which is the
only place the real status code lives.

Run it through the Browser pane's preview, not by hand:
`.claude/launch.json` names it, so `preview_start` with the name "site" is the
supported way in. Serving is all it does - it never builds, so a stale public/
looks exactly like a fresh one and `./build.sh` is still what makes it current.
"""
import functools
import http.server
import os
import posixpath
import sys
import urllib.parse

ROOT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public")


class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        """Map a URL to a file the way the host does.

        The base class resolves the path and gives up. This adds one rule: when
        the resolved path is neither a file nor a directory, try it with `.html`
        before failing. That single line is the whole difference between this and
        `python -m http.server`, and it is the whole difference between a preview
        where 64% of links 404 and one where none do.
        """
        local = super().translate_path(path)
        if os.path.isfile(local) or os.path.isdir(local):
            return local
        if os.path.isfile(local + ".html"):
            return local + ".html"
        return local

    def send_error(self, code, message=None, explain=None):
        """Serve the site's own 404 page, as wrangler.jsonc's 404-page does.

        A bare "Error 404" from the standard library looks nothing like what a
        reader gets, so a broken link in the preview would not look the way the
        same broken link looks in production - which is the whole point of this
        file.
        """
        page = os.path.join(ROOT, "404.html")
        if code == 404 and os.path.isfile(page):
            with open(page, "rb") as fh:
                body = fh.read()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)
            return
        super().send_error(code, message, explain)

    def log_message(self, fmt, *args):
        # One line per request, without the date noise, so preview_logs reads
        # as a list of what was asked for.
        sys.stderr.write("  %s\n" % (fmt % args))


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8731
    if not os.path.isdir(ROOT):
        sys.exit(f"no {ROOT} to serve - run ./build.sh first")
    handler = functools.partial(Handler, directory=ROOT)
    # THREADING, NOT TCPServer. `python -m http.server` uses ThreadingHTTPServer
    # and a plain single-threaded TCPServer looks identical until a browser opens
    # a keep-alive connection - then the server holds that socket and every later
    # request hangs rather than failing. The first version of this file did that:
    # it answered one HEAD request, served the home page, and then stopped
    # answering, which reads as a hung browser rather than as a broken server.
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    with http.server.ThreadingHTTPServer(("", port), handler) as httpd:
        print(f"serving {ROOT} on http://localhost:{port}", flush=True)
        print("extensionless addresses resolve here the way they do on the host",
              flush=True)
        httpd.serve_forever()


if __name__ == "__main__":
    main()
