#!/usr/bin/env python3
"""Prove the propagation gate still catches the faults it was built for.

WHY THIS EXISTS
---------------
While writing the gate, check 5 was dead. Its regex contained two literal
backspace bytes where `\\b` was intended — the pattern compiled fine, matched
nothing, and the gate reported "All checks passed" exactly as it does when the
site is clean. **A dead check is indistinguishable from a passing one**, and the
whole point of the gate is that it fails when the site is wrong.

So each check is exercised against the real fault it was written for. Every one
of these mutations is a fault that actually shipped and was found by an outside
reader on 9 August 2026.

Run by hand before trusting the gate, and after touching scripts/gate.py:

    python3 scripts/gate_selftest.py

It edits files under public/ and assets/ and restores them in a finally block,
so an interrupt still leaves the tree as it found it. It is deliberately NOT
wired into check.py: a pre-commit check should not write to the working tree.
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)


def check():
    r = subprocess.run([sys.executable, "scripts/check.py"], capture_output=True, text=True)
    return r.returncode, r.stdout


CASES = [
    ("count contradiction — 208 named against 209 in the data",
     "public/tools/index.html",
     lambda t: t.replace("452 items, 209 named", "452 items, 208 named")),

    ("verification count off the ledger",
     "public/index.html",
     lambda t: re.sub(r"(\d+) fully verified", "8 fully verified", t, count=1)),

    ("a withheld coordinate reprinted in the roster",
     "public/dungeons/najena.html",
     lambda t: t.replace('<td class="nmob">Rathyl</td><td class="loc"><span class="wh">withheld</span></td>',
                         '<td class="nmob">Rathyl</td><td class="loc">&minus;670, &minus;119</td>')),

    ("metadata asserting a figure the body hedges",
     "public/raids/eye-of-veeshan.html",
     lambda t: t.replace('content="Interactive 3D raid guide for the Eye of Veeshan',
                         'content="32,000 HP. Interactive 3D raid guide for the Eye of Veeshan')),

    ("a tool dropped from the footer",
     "public/index.html",
     lambda t: re.sub(r'\s*<li><a href="[^"]*tools/faction-impact\.html">[^<]*</a></li>', "", t)),

    # The change log is exempt from the prose ceiling, and that exemption is
    # exactly the kind of hole that quietly turns a check off. This proves the
    # rest of the page is still governed.
    ("prose growing on the page that hosts the change log",
     "public/sources.html",
     lambda t: t.replace('<section class="band" id="changelog"',
                         "<p>" + " ".join(["ballast"] * 100)
                         + '</p><section class="band" id="changelog"')),

    # Same hole, second ledger. The register's entries are exempt; its prose
    # is not, and each exemption has to be proved separately or the list in
    # gate.py becomes a place to hide growth.
    ("prose growing on the findings register",
     "public/learn/still-true.html",
     lambda t: t.replace('<article class="st-entry"',
                         "<p>" + " ".join(["ballast"] * 100)
                         + '</p><article class="st-entry"', 1)),
]


def mutate_zone_gate():
    """A zone marked full while its gate text still names an open gate."""
    p = "assets/zones-index.json"
    orig = open(p, encoding="utf-8").read()
    Z = json.loads(orig)
    Z[0]["verify_gate"] = "Gate 3, the room-list collision check, is still open"
    open(p, "w", encoding="utf-8", newline="\n").write(
        json.dumps(Z, indent=1, ensure_ascii=False) + "\n")
    return p, orig


def mutate_missing_item_page():
    """An item page the data links to but that is not on disk.

    The Index writes its links in the browser, so the link checker never sees
    them and this is the only thing standing between a renamed item and 452
    silent 404s. Moved rather than deleted, and put back in the finally.
    """
    p = "public/items/journeymans-boots.html"
    orig = open(p, encoding="utf-8").read()
    os.remove(p)
    return p, orig


def main():
    code, _ = check()
    if code != 0:
        print("The tree does not pass before mutation. Fix that first — the "
              "self-test cannot tell a real failure from a caught one.")
        return 1

    results = []
    for name, path, fn in CASES:
        orig = open(path, encoding="utf-8").read()
        try:
            new = fn(orig)
            if new == orig:
                results.append((name, "TEST BROKEN", "the mutation did not apply — "
                                "the markup it targets has changed"))
                continue
            open(path, "w", encoding="utf-8", newline="\n").write(new)
            rc, out = check()
            hit = next((l.strip()[6:] for l in out.splitlines() if "FAIL" in l), "")
            results.append((name, "caught" if rc != 0 else "MISSED", hit[:110]))
        finally:
            open(path, "w", encoding="utf-8", newline="\n").write(orig)

    for label, fn in (("a full zone still naming an open gate", mutate_zone_gate),
                      ("an item page The Index links but that is not on disk",
                       mutate_missing_item_page)):
        path, orig = fn()
        try:
            rc, out = check()
            hit = next((l.strip()[6:] for l in out.splitlines() if "FAIL" in l), "")
            results.append((label, "caught" if rc != 0 else "MISSED", hit[:110]))
        finally:
            open(path, "w", encoding="utf-8", newline="\n").write(orig)

    bad = 0
    for name, status, detail in results:
        print(f"  [{status:11}] {name}")
        if detail and status == "caught":
            print(f"                {detail}")
        if status != "caught":
            bad += 1

    rc, _ = check()
    if rc != 0:
        print("\nThe tree does not pass after restoring. Something was left mutated.")
        return 1
    if bad:
        print(f"\n{bad} check(s) did not catch their fault. The gate is not doing its job.")
        return 1
    print(f"\nAll {len(results)} gate checks caught their fault, and the tree is clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
