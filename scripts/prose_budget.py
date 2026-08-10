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

Run it after a deliberate trim, then commit the new ceilings with the trim:

    python3 scripts/prose_budget.py

Deliberately not part of ./build.sh. A build that re-baselined its own ceilings
every time would never fail check 6 at all.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from gate import page_words                              # one measurement, shared

BUDGET = "assets/prose-budget.json"


def main():
    budget = json.load(open(BUDGET, encoding="utf-8"))
    new, moved, gone = {}, [], []
    for key, cap in sorted(budget.items()):
        path = os.path.join("public", key)
        if not os.path.exists(path):
            gone.append(key)
            continue
        n = page_words(path, key)
        new[key] = min(n, cap)
        if new[key] != cap:
            moved.append((key, cap, new[key]))

    for key in gone:
        print(f"  dropped   {key} — no longer on disk")
    for key, was, now in moved:
        print(f"  {key:42} {was:>6,} -> {now:>6,}  ({was - now:,} freed)")
    if not moved and not gone:
        print("  no ceiling moved — every page is already at its budget")

    json.dump(new, open(BUDGET, "w", encoding="utf-8", newline="\n"),
              indent=1, sort_keys=True)
    total = sum(new.values())
    print(f"\n{len(new)} ceilings, {total:,} words allowed in total"
          f"{f', {sum(w - n for _, w, n in moved):,} words of slack removed' if moved else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
