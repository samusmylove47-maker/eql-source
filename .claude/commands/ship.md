---
description: Validate, commit and push a change so Cloudflare publishes it
---

Ship the current work.

1. Run `./build.sh`.
2. Run `python3 scripts/check.py`. **If it fails, stop and fix it.** A red check
   is a blocker, never a warning.
3. Show me `git status` and `git diff --stat` and wait for me to confirm.
4. Write a commit message in the form `type: what changed`, where type is one of
   `content`, `fix`, `data`, `design`, `chore`.
5. Commit and push to `main`.
6. Tell me the Cloudflare deploy usually lands in a minute or two, and remind me
   that undoing a bad one means `git revert` on `main` opened as its own pull
   request — the same route as everything else. This step named Netlify and its
   Deploys dashboard until 4 September 2026; the host has been a Cloudflare
   Worker since before 14 August, so it was sending me to a dashboard that does
   not serve this site.

If this change corrects something that was previously wrong on the site, add a
Change log row to `sources.html` typed **Correction** before committing. A fix
must never read as new content.
