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
3. **Re-derive the coordinates** and collision-check them against the room list.

Then:

- Compare every figure on our plate against the page. List every difference.
- Check the patch notes for anything dated after the page's last edit. Patch
  notes win.
- Update `verified` in `assets/zones-index.json` **only if all three gates
  passed.** Otherwise leave it and tell me which gate is still open.
- Report what you found as: confirmed / changed / still unknown. Do not smooth
  over the third category.
