---
description: Validate, commit and push a change so Netlify publishes it
---

Ship the current work.

1. Run `./build.sh`.
2. Run `python3 scripts/check.py`. **If it fails, stop and fix it.** A red check
   is a blocker, never a warning.
3. Show me `git status` and `git diff --stat` and wait for me to confirm.
4. Write a commit message in the form `type: what changed`, where type is one of
   `content`, `fix`, `data`, `design`, `chore`.
5. Commit and push to `main`.
6. Tell me the Netlify deploy usually lands in about thirty seconds, and remind
   me the rollback is under Deploys in the Netlify dashboard.

If this change corrects something that was previously wrong on the site, add a
Change log row to `sources.html` typed **Correction** before committing. A fix
must never read as new content.
