---
description: Scaffold a new tool following the house patterns
---

Build a new tool: $ARGUMENTS

Check it belongs here first. `docs/BACKLOG.md` has a "deliberately not doing"
section — our layer is quests, factions, routes and tactics. If this duplicates
something EQL Tools already does well, say so and stop.

Follow the established patterns exactly:

1. **Generator in `_build/`**, numbered next in sequence, added to `build.sh`.
   Output goes to `tools/<slug>.html`.
2. **Use `head()`, `bar("../")` and `foot("../")`** from `_build/_partials.py` so
   it gets site chrome, the favicon and the correct nav.
3. **Data inline, not fetched.** `fetch()` fails on `file://`, which breaks local
   testing. Mine source data into JSON in the generator and embed it.
4. **State in the URL fragment**, mirrored to browser storage, exactly as the
   other tools do: bitfield packed to base64url, a mode flag so a reload returns
   you where you were, and a share link. Copy the pattern from
   `_build/source/eql-sky-tracker.html`.
5. **Two reset actions, not one** — clear progress, and start over. The single
   ambiguous "Reset" was a real bug we fixed.
6. **Add it to** the tools index (`_build/build2.py`), the homepage tools band
   (`_build/build1.py`), the nav in `_partials.py`, and the footer.
7. **Test with a browser**, not just by reading the HTML. Filters, empty states,
   share-link round trip, 390px overflow.

Then `./build.sh`, `python3 scripts/check.py`, and show me before committing.
