#!/usr/bin/env python3
"""Prove the propagation gate still catches the faults it was built for.

WHY THIS EXISTS
---------------
While writing the gate, check 5 was dead. Its regex contained two literal
backspace bytes where `\\b` was intended — the pattern compiled fine, matched
nothing, and the gate reported "All checks passed" exactly as it does when the
site is clean. **A dead check is indistinguishable from a passing one**, and the
whole point of the gate is that it fails when the site is wrong.

So each check is exercised against the real fault it was written for. Most of
these mutations are faults that actually shipped and were found by an outside
reader on 9 August 2026. The catalogue-fixes cases at the end trace to a
different miss: a guard that file claimed to have and did not.

WHY EVERY CASE NAMES THE MESSAGE IT EXPECTS
-------------------------------------------
Until 11 August 2026 a case passed when check.py failed *at all*. That is the
same weakness one level up: a mutation that trips some other check reads exactly
like a mutation the intended check caught, and this file would report it as
proof.

It was not hypothetical. Two of the eleven cases were proving the wrong thing:

  - The open-gate case mutates assets/zones-index.json, which is a build input,
    so the staleness check fires and sorts first. The case reported
    "public/ is stale — a source changed since the last successful ./build.sh"
    as its evidence that a full zone may not name an open gate.
  - Removing an item page trips two ordinary broken-link failures, because the
    A–Z hub links it with a real href. The slug check it was written for — the
    one that catches the links The Index writes in the browser, which no link
    checker can see — fired third and was never read.

Both checks turned out to be alive. Nothing here had shown that, which is this
file's only job.

So each case carries `expect`: a distinctive fragment of the message its check
prints. A case passes only when some failure line contains that fragment. Other
failures alongside it are fine and ignored — the staleness one above cannot be
avoided, because proving that check requires changing a build input. What is no
longer possible is a case passing on someone else's failure.

`expect` is matched against check.py's output rather than gate.py being made to
tag each failure with a check id, because half these cases exercise checks that
live in check.py, not in the gate. One mechanism covers both.

Run by hand before trusting the gate, and after touching scripts/gate.py:

    python3 scripts/gate_selftest.py

It edits files under public/ and assets/ and restores them in a finally block,
so an interrupt still leaves the tree as it found it. It is deliberately NOT
wired into check.py: a pre-commit check should not write to the working tree.
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)


_IX = json.load(open("assets/index-data.json", encoding="utf-8"))
# Declared by extract.py, matching what the pages print. Typed as
# len(_IX["items"]) until 17 Aug 2026, which is 451 raw rows including groups
# and fragments; the pages print 435 item pages, so the mutation below silently
# matched nothing.
N_ITEMS, N_NAMED = _IX["counts"]["item_pages"], _IX["counts"]["named_pages"]
N_ZONES = len(json.load(open("assets/zones-index.json", encoding="utf-8")))


def check():
    r = subprocess.run([sys.executable, "scripts/check.py"], capture_output=True, text=True)
    return r.returncode, r.stdout


def failures(out):
    """Every blocker check.py printed, in order, stripped of the FAIL prefix.

    All of them, not the first. Reading only the first is how two cases came to
    be proved by the staleness check and the link checker.
    """
    return [l.strip()[6:].strip() for l in out.splitlines() if l.strip().startswith("FAIL")]


def judge(expect, rc, out):
    """Did the check this case is about fire? Not: did anything fire.

    `expect` is kept ASCII on purpose. check.py's messages carry em dashes, and
    a pipe on Windows round-trips through cp1252 — a fragment that spans one
    would match or not depending on the console encoding, which is a worse
    failure than the one this file exists to prevent.
    """
    got = failures(out)
    for line in got:
        if expect in line:
            return "caught", line
    if rc == 0:
        return "MISSED", f"nothing failed at all; expected {expect!r}"
    return "WRONG CHECK", (f"expected {expect!r}, but what failed was: "
                           + " | ".join(got))


def _sub_first_number(text, placeholder):
    """Swap the first comma-formatted figure on a page for an unrendered token.

    These two cases used to name a literal - "26,158", the biggest Plane of Sky
    boss damage on the day they were written. Four more Sky sessions were parsed
    on 17 August, the figure moved, and both mutations silently stopped applying.
    A self-test that cannot apply its mutation reports the check as broken, which
    is the correct alarm, but the cause was the test pinning itself to data that
    was always going to change.

    So it targets the SHAPE instead. Any page rendering a measured figure has
    one, and the check under test is about placeholders reaching a page rather
    than about any particular number.

    Anchored inside <b>, which is how the measured figures render. A bare
    number pattern matched SVG path coordinates first — "0,150" in a polyline —
    and a placeholder buried in path data is not what the check looks at.
    """
    m = re.search(r"<b>\d{1,3},\d{3}</b>", text)
    if not m:
        return text
    return text[:m.start()] + "<b>" + placeholder + "</b>" + text[m.end():]


CASES = [
    # A tool whose data constant went missing. The Sky tracker shipped on 14
    # August with ORDER undefined: the class picker rendered nothing, the trio
    # could never reach three, the Build button was permanently disabled, and
    # check.py passed all 721 pages because nothing here runs a page's
    # JavaScript. The check that catches it is narrow on purpose; this proves
    # it is alive.
    # Retargeted 17 Aug 2026: the case used tools/plane-of-sky.html, which was
    # withdrawn when Sky Ledger replaced it. RORDER is the same shape of
    # constant in the same shape of tool — a top-level display order the render
    # reads on its first statement — so removing it reproduces the fault
    # exactly. The check is about a tool's data constants, not about that page.
    ("a tool's data constant is undefined",
     "script uses 1 undefined constant(s)",
     "public/tools/race-unlocks.html",
     lambda t: t.replace('const RORDER=["DEF"', 'const RORDER_UNUSED=["DEF"', 1)),

    # The counts are read from the data, not typed, because this file typed them
    # once and the case silently became a no-op the next time a zone was added —
    # reported as TEST BROKEN rather than caught, which is the good failure, but
    # it is still the same fault the gate exists to prevent.
    ("count contradiction — one fewer named than the data holds",
     f"says {N_NAMED - 1} for 'named recorded' but the data holds {N_NAMED}",
     "public/tools/index.html",
     lambda t: t.replace(f"{N_ITEMS} items, {N_NAMED} named",
                         f"{N_ITEMS} items, {N_NAMED - 1} named")),

    ("verification count off the ledger",
     "claims 8 fully verified; the ledger says",
     "public/index.html",
     lambda t: re.sub(r"(\d+) fully verified", "8 fully verified", t, count=1)),

    # The other half of check 2, revived 18 Aug 2026. It had read "of the ten
    # plates have not cleared" since the plates became surveys on 10 August, so
    # it matched nothing for eight days and reported clean throughout — and it
    # compared against npart rather than every survey short of the full
    # standard, so the day it began matching it would have failed a correct
    # page. Dead and wrong at once, which is why the sibling case above could
    # not stand in for it: that one exercises the "fully verified" regex, and
    # this sentence is counted from a different number on a different page.
    ("the count of surveys short of the full standard, off by one",
     "surveys have not cleared the full standard",
     "public/sources.html",
     lambda t: t.replace("Four of the 13 surveys have not cleared",
                         "Five of the 13 surveys have not cleared")),

    ("a withheld coordinate reprinted in the roster",
     "prints a coordinate for 'Rathyl', which is withheld",
     "public/dungeons/najena.html",
     lambda t: t.replace('<td class="nmob">Rathyl</td><td class="loc"><span class="wh">withheld</span></td>',
                         '<td class="nmob">Rathyl</td><td class="loc">&minus;670, &minus;119</td>')),

    # Retargeted 17 Aug 2026: this case used raids/eye-of-veeshan.html, which was
    # withdrawn. Plane of Hate carries a badged figure in its body and so
    # exercises the same rule — the check is about the badge and the metadata,
    # not about that one page.
    ("metadata asserting a figure the body hedges",
     "asserts 375 flatly in its meta description",
     "public/dungeons/planeofhate.html",
     lambda t: re.sub(r'(<meta name="description" content=")', r'\g<1>375 damage. ', t, count=1)),

    # Rule 5's blind spot, proved separately because rule 5 cannot prove it.
    # Castle Mistmoore was revamped on 18 Aug 2026 with the note in its body and
    # its share card still ending "Every figure sourced and dated" — the copy a
    # Discord embed keeps, and the one a reader cannot correct. Rule 5 only
    # inspects numbers of three digits or more and this description has none, so
    # the case above would pass on this page no matter how stale the card got.
    ("a revamped zone whose share card does not say so",
     "share description does not say so",
     "public/dungeons/mistmoore.html",
     lambda t: t.replace("Measured before the 18 August 2026 revamp and not "
                         "re-measured since.",
                         "Every figure sourced and dated.")),

    # The bug this shipped with. _build/plans.py parsed /loc with a plain
    # `-?\d+`, and 141 recorded coordinates use U+2212 MINUS SIGN, so every
    # negative one read as positive and the mark landed in the opposite corner.
    # Nothing looked wrong: a dot on a dungeon plan looks right wherever it is.
    # Mutating a plotted circle away from its /loc proves the agreement check
    # is alive.
    ("a plotted position that disagrees with its floor plan",
     "the page locator and the floor plan disagree",
     "public/dungeons/najena.html",
     lambda t: re.sub(r'(<g class="mk"[^>]*>.*?<circle[^>]*cx=")(-?[\d.]+)',
                      lambda m: m.group(1) + str(float(m.group(2)) + 300),
                      t, count=1, flags=re.S)),

    # The stored percentage that disagreed with its own ZEM. Splitpaw shipped
    # 170 where 128/75 rounds to 171, and the survey built a "highest of the
    # set" claim on it while another zone published 185%.
    ("a derived percentage that disagrees with its ZEM",
     "a derived figure may not disagree with what it derives from",
     "assets/zones-index.json",
     lambda t: t.replace('"zem_pct": 171', '"zem_pct": 170', 1)),

    ("a tool dropped from the footer",
     "footer does not link tools/faction-impact.html",
     "public/index.html",
     lambda t: re.sub(r'\s*<li><a href="[^"]*tools/faction-impact\.html">[^<]*</a></li>', "", t)),

    # This one shipped. the withdrawn build4.py's BODY carried the 3D engine's JavaScript, so
    # it can never be an f-string, and f-string syntax written into it renders as
    # itself: the Eye's stat block published the literal text "{EYE_FULL:,}" on
    # 15 August 2026 and all 723 checks passed. Every other check reads what a
    # page says; none asked whether it had finished rendering.
    ("an f-string placeholder left unrendered",
     "shipped an unrendered placeholder",
     "public/raids/plane-of-sky.html",
     lambda t: _sub_first_number(t, "{BIGGEST:,}")),

    # The same fault in the other notation that generator used. Two shapes, two
    # cases: a check that caught only the one we happened to hit last would go
    # dead the first time a generator picked the other convention.
    ("an @@TOKEN@@ placeholder left unrendered",
     "shipped an unrendered placeholder",
     "public/raids/plane-of-sky.html",
     lambda t: _sub_first_number(t, "@@BIGGEST@@")),

    # A dataset figure typed into the metadata. The Sky Ledger tool page said 95
    # in its description while its body read the same quantity from the data, so
    # the two were free to drift on the next dataset change. Metadata is the
    # only text a reader gets uncaveated, and it is what a share card carries.
    ("a figure in the metadata that is nowhere on the page",
     "in its meta description and never on the page",
     "public/tools/sky-ledger.html",
     lambda t: t.replace('name="description" content="',
                         'name="description" content="4242 tests. ', 1)),

    # The change log is exempt from the prose ceiling, and that exemption is
    # exactly the kind of hole that quietly turns a check off. This proves the
    # rest of the page is still governed.
    ("prose growing on the page that hosts the change log",
     "sources.html has grown to",
     "public/sources.html",
     lambda t: t.replace('<section class="band" id="changelog"',
                         "<p>" + " ".join(["ballast"] * 100)
                         + '</p><section class="band" id="changelog"')),

    # Same hole, second ledger. The register's entries are exempt; its prose
    # is not, and each exemption has to be proved separately or the list in
    # gate.py becomes a place to hide growth.
    ("prose growing on the findings register",
     "learn/still-true.html has grown to",
     "public/learn/still-true.html",
     lambda t: t.replace('<article class="st-entry"',
                         "<p>" + " ".join(["ballast"] * 100)
                         + '</p><article class="st-entry"', 1)),

    # Third ledger, same proof.
    ("prose growing on the dungeon index",
     "dungeons/index.html has grown to",
     "public/dungeons/index.html",
     lambda t: t.replace('class="plates"',
                         'class="x">' + " ".join(["ballast"] * 90)
                         + '</div><div class="plates"', 1)),

    # Not growth this time — absence. The three cases above all prove that a
    # page WITH a ceiling cannot grow past it. None of them could prove anything
    # about a page with no ceiling at all, and until 18 Aug 2026 that page was
    # skipped in silence: `cap = budget.get(key)` then `if cap is None:
    # continue`. Fourteen pages were in that state, three of them dungeon
    # surveys, and the ratchet reported clean the whole time.
    #
    # A hole that swallows every page nobody thought to enrol is worse than a
    # ceiling set too high, because a ceiling set too high is at least visible
    # in the file. This case deletes a key and requires the build to notice.
    ("a governed page with no prose ceiling at all",
     "tools/sky-ledger.html ships with no ceiling",
     "assets/prose-budget.json",
     lambda t: json.dumps({k: v for k, v in json.loads(t).items()
                           if k != "tools/sky-ledger.html"},
                          indent=1, sort_keys=True)),

    # A count typed as a word rather than printed from the ledger. The dungeon
    # index headline read "Ten zones, surveyed" while the ledger held thirteen,
    # and nothing caught it because every count check matched digits only.
    ("a zone count spelled out and left behind",
     f"says 'Ten' for 'zones surveyed' but the data holds {N_ZONES}",
     "public/dungeons/index.html",
     lambda t: t.replace(f"{N_ZONES} zones,", "Ten zones,")),

    # ---- the curated corrections have not gone stale -------------------------
    #
    # assets/catalogue-fixes.json ends by saying "scripts/check.py fails if a
    # name here no longer appears in the data, so this file cannot rot quietly."
    # For a long time no such check existed, so the file was free to rot in
    # exactly the silence it claimed to be protected from. The check arrived on
    # 11 August 2026. These cases are what stop it going the same way, and the
    # sequence — a guard asserted, absent, then added unproven — is the reason
    # to be strict about it.
    #
    # A CASE PER LABEL, NOT PER CODE PATH.
    #
    # The five labels share two lookups: fragments, groups and resolved
    # fragments are checked against the mined data, aliases and splits against
    # the survey sources. Two cases would cover both lookups. But each label
    # reads a different key out of the file, so one mistyped .get() would empty
    # one label's key set and leave that label reporting success for ever while
    # the other four still worked. An empty set is the dead check in its purest
    # form: nothing to iterate, nothing to fail, nothing to see.
    #
    # Mutating this file also makes public/ stale, since it is a build input and
    # extract.py reads it. That failure is collateral and ignored, the same as
    # the open-gate case below.
    #
    # `expect` carries the stale name rather than just the label, because
    # "1 fragment(s)" and "1 resolved fragment(s)" are one word apart and a
    # count away from matching each other.
    ("a fragment fix keyed to a name the survey has since re-worded",
     "fragment(s) that no longer appear in the mined data, so the correction "
     "does nothing: 'Skin of the Gnoll'",
     "assets/catalogue-fixes.json",
     lambda t: t.replace('"Skin": "Blackburrow Gnoll Pelt"',
                         '"Skin of the Gnoll": "Blackburrow Gnoll Pelt"')),

    ("a group heading fix keyed to a name the survey has since re-worded",
     "group(s) that no longer appear in the mined data, so the correction "
     "does nothing: 'Bronze weapon range'",
     "assets/catalogue-fixes.json",
     # The prose above the data spells this one in single quotes, so the
     # double-quoted form only ever matches the entry itself.
     lambda t: t.replace('"Bronze weapon line"', '"Bronze weapon range"')),

    # The resolved fragments are the newest entries and the ones most likely to
    # move: each retires a fragment on the strength of one inventory dump, and
    # the name it retires it to is the game's, not ours.
    ("a resolved fragment whose full name is not in the data",
     "resolved fragment(s) that no longer appear in the mined data, so the "
     "correction does nothing: 'Torn Page of Mastery Flame'",
     "assets/catalogue-fixes.json",
     lambda t: t.replace('"name": "Torn Page of Mastery Fire"',
                         '"name": "Torn Page of Mastery Flame"')),

    ("a split fix keyed to a row no survey source holds",
     "split(s) that no longer appear in any survey source, so the correction "
     "does nothing: 'A Nisch / Tesch Val Sentry'",
     "assets/catalogue-fixes.json",
     lambda t: t.replace('"A Nisch / Tesch Val Guard": [',
                         '"A Nisch / Tesch Val Sentry": [')),

    # This one ADDS a key rather than re-wording one, because `aliases` is empty:
    # its only entry, Zordak Ragefire aliased to Zordakalicus Ragefire, was
    # withdrawn on 11 August 2026 as a wrong merge.
    #
    # An empty dict is why the case is worth having rather than why it should be
    # skipped. While the dict is empty a mistyped .get("aliases") reports success
    # and looks identical to a working check, so the branch would be found broken
    # only by whoever adds the first real alias — and they would find it by the
    # correction silently doing nothing, which is the fault this check exists to
    # prevent.
    ("an alias fix naming a mob no survey source mentions",
     "alias(s) that no longer appear in any survey source, so the correction "
     "does nothing: 'A Ghoul That No Survey Names'",
     "assets/catalogue-fixes.json",
     lambda t: t.replace('"aliases": {},',
                         '"aliases": {"A Ghoul That No Survey Names": "A Ghoul"},')),
]


def mutate_zone_gate():
    """A zone marked full while its gate text still names an open gate.

    This also makes public/ stale, because zones-index.json is a build input and
    build.sh stamps its inputs. That staleness failure is collateral and is
    ignored; `expect` names the open-gate message instead. For two months it was
    the only thing this case actually proved.
    """
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

    The A–Z hub does link this one with a real href, so the ordinary link check
    fails first and twice. Those are collateral: `expect` names the slug check,
    which is the one that would still fire for an item reachable only through
    The Index.
    """
    p = "public/items/journeymans-boots.html"
    orig = open(p, encoding="utf-8").read()
    os.remove(p)
    return p, orig


SPECIAL = [
    ("a full zone still naming an open gate",
     "is marked full but its verify_gate still names an open gate",
     mutate_zone_gate),
    ("an item page The Index links but that is not on disk",
     "items page(s) that do not exist: journeymans-boots",
     mutate_missing_item_page),
]


def main():
    code, out = check()
    if code != 0:
        print("The tree does not pass before mutation. Fix that first — the "
              "self-test cannot tell a real failure from a caught one.")
        for f in failures(out):
            print(f"    {f}")
        return 1

    results = []
    for name, expect, path, fn in CASES:
        orig = open(path, encoding="utf-8").read()
        try:
            new = fn(orig)
            if new == orig:
                results.append((name, "TEST BROKEN", "the mutation did not apply — "
                                "the markup it targets has changed"))
                continue
            open(path, "w", encoding="utf-8", newline="\n").write(new)
            rc, out = check()
            results.append((name,) + judge(expect, rc, out))
        finally:
            open(path, "w", encoding="utf-8", newline="\n").write(orig)

    for label, expect, fn in SPECIAL:
        path, orig = fn()
        try:
            rc, out = check()
            results.append((label,) + judge(expect, rc, out))
        finally:
            open(path, "w", encoding="utf-8", newline="\n").write(orig)

    bad = 0
    for name, status, detail in results:
        print(f"  [{status:11}] {name}")
        if detail:
            print(f"                {detail[:200]}")
        if status != "caught":
            bad += 1

    rc, _ = check()
    if rc != 0:
        print("\nThe tree does not pass after restoring. Something was left mutated.")
        return 1
    if bad:
        print(f"\n{bad} case(s) did not see the check they were written for fail. "
              f"Either that check is dead, or this file is now testing something "
              f"else — both are blockers.")
        return 1
    print(f"\nAll {len(results)} cases saw the check they were written for fail, "
          f"and the tree is clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
