#!/usr/bin/env python3
"""Lower the prose ceilings to what the pages now weigh.

WHY
---
The ratchet in scripts/gate.py refuses a page that has grown past its ceiling.
Its docstring said the ceiling follows a page down when it shrinks — but nothing
did that, so every ceiling stayed at the number it was first set to. A page cut
from 6,000 words to 3,000 kept a 6,000-word allowance and could quietly double
again without tripping anything. A ratchet that only turns one way in the
documentation is not a ratchet.

This runs the other half. It rewrites assets/prose-budget.json with, for each
page, the lower of what it weighs now and what it was allowed before. Ceilings
only ever fall. Growing one takes editing the file by hand and saying why in the
commit, which is the point: it should be a decision, not a side effect.

IT ALSO ENROLS, AS OF 18 AUGUST 2026
------------------------------------
It used to iterate the keys already in the file, which meant it could lower a
ceiling and could never create one. The gate's other half matched: a page with
no key hit `if cap is None: continue` and was skipped in silence. Between them
a page could ship ungoverned forever, and fourteen did — including three of the
thirteen dungeon surveys and tools/sky-ledger.html at 1,233 words.

Enrolment is free, because the ratchet only falls: seeding a page at what it
weighs today forbids nothing that is already there and forbids growth from
tomorrow. The page set and the exemption both come from gate.py, so what this
script enrols and what the gate enforces cannot drift apart.

Run it after a deliberate trim, then commit the new ceilings with the trim:

    python3 scripts/prose_budget.py

Deliberately not part of ./build.sh. A build that re-baselined its own ceilings
every time would never fail check 6 at all.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
# One measurement, one page set and one exemption, all shared with the gate that
# enforces them. Three imports rather than three reimplementations.
from gate import page_key, page_words, governed, site_pages

BUDGET = "assets/prose-budget.json"


def main():
    budget = json.load(open(BUDGET, encoding="utf-8"))
    keys = [k for k in (page_key(p) for p in site_pages()) if governed(k)]

    new, moved, added = {}, [], []
    for key in sorted(keys):
        n = page_words("public/" + key, key)
        cap = budget.get(key)
        if cap is None:
            new[key] = n
            added.append((key, n))
            continue
        new[key] = min(n, cap)
        if new[key] != cap:
            moved.append((key, cap, new[key]))
    gone = [k for k in sorted(budget) if k not in new]

    for key in gone:
        print(f"  dropped   {key} — not a governed page on disk")
    for key, n in added:
        print(f"  ENROLLED  {key:40} at {n:>6,}")
    for key, was, now in moved:
        print(f"  {key:42} {was:>6,} -> {now:>6,}  ({was - now:,} freed)")
    if not moved and not gone and not added:
        print("  no ceiling moved — every page is already at its budget")

    json.dump(new, open(BUDGET, "w", encoding="utf-8", newline="\n"),
              indent=1, sort_keys=True)
    total = sum(new.values())
    print(f"\n{len(new)} ceilings, {total:,} words allowed in total"
          f"{f', {sum(w - n for _, w, n in moved):,} words of slack removed' if moved else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
