---
description: Re-verify a zone against its wiki page to the full standard
---

Re-verify this zone: $ARGUMENTS

The verification standard has three gates and all three must pass:

1. **Fetch the wiki page in full.** Check the `oldid` in the footer against the
   current revision from the API. If they differ you were served a cache —
   re-request with `diff=cur&oldid=<what you got>`. If the page comes back
   empty, that is a failed fetch, not an empty page.
2. **Fetch the edit history**, not just the footer date. Record when the page
   was created, by whom, and whether it is a Project 1999 import.
3. **Check every coordinate against drawn floor.** Each must land within 120
   units of the walkable geometry in `assets/zone-geometry.json`. `build6.py`
   counts this at build time and prints the total, so a regression shows up in
   the build output — do not retype the number. This gate replaced a collision
   check against a room list on 9 Aug 2026, because no room in the project
   carries an extent to check against. See `docs/SOURCES.md`.

Then:

- Compare every figure on our plate against the page, and compare the full named
  roster both ways. List every difference.
- Where a mob's note names a room, check that mobs sharing a room land close
  together on the plot. That is the qualitative version of the old gate 3 and it
  is the strongest room evidence available without room extents.
- Check the patch notes for anything dated after the page's last edit. Patch
  notes win.
- Update `verified` in `assets/zones-index.json` **only if all three gates
  passed.** Otherwise leave it and tell me which gate is still open.
- Report what you found as: confirmed / changed / still unknown. Do not smooth
  over the third category.
