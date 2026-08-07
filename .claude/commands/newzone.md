---
description: Add a new dungeon survey plate to the site
---

Add a new dungeon to the survey. The zone is: $ARGUMENTS

Follow this exactly:

1. Confirm you have the source plate HTML. If it is not in `_build/source/`,
   stop and ask for it. Do not write a plate from scratch without being asked.
2. Read `assets/zones-index.json`. Work out the next plate number and pick an
   accent colour that is **not already used** — check every existing entry.
3. Add the zone entry: plate, slug, title, accent, levels, zem, zem_pct,
   respawn, who, adjacent, verified. Use `null` for anything you do not have a
   source for. Do not guess.
4. Update `.spec-bars{grid-template-columns:repeat(N,1fr)}` in `assets/site.css`
   so N matches the new zone count.
5. Add the zone's top level to `TOPLV` in `_build/build1.py` — that sets its
   spectrum bar height.
6. Run `./build.sh`, then `python3 scripts/check.py`.
7. Add a Change log row to `sources.html`, typed **Addition**.
8. Show me the diff and tell me what is unverified about this zone before you
   commit anything.
