---
description: Work through one stage of the aesthetic uplift
---

Work on the design uplift. Stage: $ARGUMENTS

Before you touch anything:

1. Read `docs/DESIGN.md` in full. The "load-bearing" section lists things you
   must not change — monochrome chrome, the ten zone accents, three faces, the
   spectrum, hairlines, the tier badges.
2. Take a full-page screenshot at 1440px and 390px so we can compare after.
3. Tell me what specifically you intend to change, in which files, and why.
   **Wait for me to agree before editing.**

Then:

- Edit `assets/site.css` and the generators in `_build/`. Never edit generated
  HTML directly — a rebuild will throw it away.
- Run `./build.sh` then `python3 scripts/check.py`. A red check is a blocker.
- Screenshot again at both widths.
- Answer the four verification questions at the end of `docs/DESIGN.md` in
  writing. If question 4 is "no", you have gone too far — pull back.

One stage per commit. Do not do the whole uplift in one pass; I want to react to
each stage before you continue.
