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
# The two quantities that used to share the word "items" with N_ITEMS. Read from
# the same files the gate reads, so a dataset change moves the case and the rule
# together rather than leaving one of them asserting a stale figure.
N_TURNIN = json.load(open("assets/sky-ledger.json", encoding="utf-8"))["dataset"]["items"]
N_CATALOGUE = json.load(open("assets/50-upgrades.json", encoding="utf-8"))["figures"]["counts.items"]


# THE OTHER HALF OF THE SAME PROBLEM: THIS FILE'S OWN OUTPUT.
#
# Reading check.py's pipe as utf-8 fixed the silent loss and immediately turned
# it into a crash, because a Windows console is cp1252 and cannot ENCODE what
# had just been correctly decoded. A harness that dies while reporting a caught
# failure is no better than one that loses it.
#
# Both directions are utf-8 now. Windows is the platform this project builds on,
# and CLAUDE.md already records that every open() here needs an explicit
# encoding; a pipe and a console are the two that are easy to forget because
# nothing declares them.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):        # not a real stream, e.g. under a pipe wrapper
    pass


def check():
    # ENCODING IS LOAD-BEARING, AND ITS ABSENCE HID A REAL FAILURE.
    #
    # `text=True` with no encoding decodes the pipe with the platform default,
    # which on Windows is cp1252. check.py's messages carry U+2212 MINUS SIGN
    # and em dashes, and 141 of the site's recorded coordinates use U+2212
    # rather than an ASCII hyphen — so the failure lines most likely to matter
    # are exactly the ones cp1252 cannot represent.
    #
    # On 27 Aug 2026 a new case reported WRONG CHECK with an EMPTY detail: the
    # check had fired, the process had exited 1, and the line saying so was
    # lost in decoding. A harness that exists to prove checks are alive was
    # dropping their evidence on the floor, and reported that as the case being
    # wrong rather than as itself being broken.
    #
    # utf-8 with errors="replace" so a decode problem degrades to a visible
    # replacement character in a line that still matches, never to silence.
    r = subprocess.run([sys.executable, "scripts/check.py"],
                       capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.returncode, r.stdout


def failures(out):
    """Every assertion check.py printed, in order, stripped of its prefix.

    All of them, not the first. Reading only the first is how two cases came to
    be proved by the staleness check and the link checker.

    WARN AS WELL AS FAIL, AND THAT WAS A BLIND SPOT IN THE INSTRUMENT ITSELF.
    This collected only lines beginning "FAIL". gate.py holds 35 `fail(` and 7
    `warn(` assertions, so SEVEN of its checks could not be proved by the
    harness that exists to prove them — and a warn firing correctly was
    indistinguishable from a warn that had gone dead, which is the exact fault
    this whole file was written to catch, sitting inside the catcher.

    Session B reached the identical conclusion in their own instrument
    independently, which is the strongest evidence available that it is the
    shape and not the repository.

    A case may now assert against either, so a warn-only check is reachable.
    The prefix is stripped in both cases and the caller matches on the message,
    so no existing case changes meaning.
    """
    out_lines = []
    for line in out.splitlines():
        s = line.strip()
        for prefix in ("FAIL", "WARN"):
            if s.startswith(prefix):
                out_lines.append(s[len(prefix):].strip())
                break
    return out_lines


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


def _shrink_dataset(text, key, keep):
    """Drop a published dataset to `keep` entries without breaking its shape.

    The point is that it stays valid JSON with every declared field present —
    which is exactly why the emptiness rule could not see this failure and the
    floor had to be added.
    """
    d = json.loads(text)
    items = d["data"][key]
    d["data"][key] = dict(list(items.items())[:keep])
    return json.dumps(d)


def _json_poke(text):
    """Change a published dataset's PAYLOAD, keeping valid JSON and every
    contracted field. A scalar so the emptiness and floor rules do not fire
    instead and prove the wrong check."""
    d = json.loads(text)
    d["data"]["__selftest__"] = 1
    return json.dumps(d)


def _media_poke(text):
    """Make one media entry's recorded byte count disagree with the file."""
    d = json.loads(text)
    k = sorted(d)[0]
    d[k]["bytes"] = int(d[k]["bytes"]) + 1
    return json.dumps(d, indent=1, sort_keys=True)


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
     "claims 8 zones past all three gates; the ledger says",
     "public/index.html",
     lambda t: re.sub(r"(\d+) past all three gates", "8 past all three gates", t, count=1)),

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
     # Derived, not typed. This pinned the literal "Four of the 13 surveys" and
     # went TEST BROKEN the moment Mistmoore returned to full and the sentence
     # read "Three" - a self-test that hard-codes the value it mutates rots
     # exactly like the pages it is guarding. It now rewrites whatever word is
     # there into one that is certainly wrong.
     lambda t: re.sub(r'\b(One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|Eleven|Twelve|Thirteen)'
                      r'( of the \d+ surveys have not cleared)',
                      r'Thirteen\2', t, count=1)),

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
     "footer does not link tools/faction-impact",
     "public/index.html",
     lambda t: re.sub(r'\s*<li><a href="[^"]*tools/faction-impact">[^<]*</a></li>', "", t)),

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

    # A WITHHELD COORDINATE ON A PAGE THAT IS NOT A PLATE.
    #
    # Rule 4 hardcoded its scan to public/dungeons/{slug}.html, so it proved 13
    # pages and all six withheld Najena coordinates shipped on their named-mob
    # pages anyway - "Position −670, −119" on rathyl.html - and all six were
    # embedded in The Index's search bundle too, one per mob. The rule was right
    # and its reach was one directory wide. This case exists so the widened scan
    # cannot quietly narrow again.
    #
    # THAT COUNT SAID FOUR UNTIL 30 AUG 2026, AND THE WAY IT WAS WRONG IS THE
    # POINT. The bundle is JSON, so a coordinate's minus sign is stored as the
    # six-character escape − - 245 of them, and zero literal ones. The scan
    # that produced "four" matched on a character class, [-−], which cannot
    # match an escape sequence; it counted the mobs whose digits happened to
    # parse anyway and missed the rest. A wrong figure inside the comment
    # explaining why this rule exists, in the file whose whole job is catching
    # wrong figures, is worth measuring twice.
    ("a withheld coordinate on a named-mob page",
     "whose coordinate is withheld",
     "public/named/rathyl.html",
     lambda t: t.replace('<dt>Position</dt><dd><span class="wh">withheld</span></dd>',
                         '<dt>Position</dt><dd>−670, −119</dd>', 1)),

    # NO CASE HERE FOR A SERVED APPLICATION FETCHING FROM ANOTHER ORIGIN, AND
    # THE REASON IS A LIMIT OF THIS HARNESS RATHER THAN OF THE CHECK.
    #
    # The egress rule now covers public/app/ — it did not until 31 August, when
    # `pages` excluded those two bundles and they were the only files under
    # public/ it could not see. I proved the fix with a matched pair by hand:
    # a stylesheet link injected into the Sky Ledger bundle is caught, and the
    # restored file passes.
    #
    # I then wrote it as a case here and it CORRUPTED THE BUNDLE. This runner
    # reads with `open(path, encoding="utf-8")` and restores with
    # `newline="\n"`, which is a lossless round-trip for pages this repository
    # generates and is NOT one for a 182 KB artifact built in another repository:
    # the restored file hashed to cae880e4 against a recorded dad68d2b, and
    # check.py caught it because the served hash is verified.
    #
    # So the constraint, for whoever adds the next case: THE MUTATION PATH HERE
    # IS TEXT. Do not point it at anything whose bytes are load-bearing —
    # anything under public/app/, anything hashed, anything vendored. Fixing the
    # runner to round-trip binary would be the real repair and it is not a 2am
    # change to the file that proves every other check is alive.

    # A PAGE THAT FETCHES FROM ANOTHER ORIGIN ON LOAD.
    #
    # 715 of 717 pages fetched their typefaces from Google until 30 August 2026,
    # disclosing every reader's IP before anything rendered, on pages that said
    # "Nothing transmitted". The faces are self-hosted now. This case exists
    # because one CDN link added in six months would restore the fault in
    # silence — and because nothing was watching for it the first time:
    # conformance.js aborts every non-file: request, so it had always measured a
    # page whose remote fetches never happened.
    ("a page fetching a stylesheet from another origin",
     "from another origin",
     "public/index.html",
     lambda t: t.replace('<link rel="stylesheet"',
                         '<link rel="stylesheet" href="https://cdn.example.com/x.css">'
                         '<link rel="stylesheet"', 1)),

    # THE PROMOTION GATE, BOTH DIRECTIONS.
    #
    # The lockout tracker was copied into public/app/ on 25 Aug 2026 and left
    # deliberately unlinked, guarded by a warn(). Promotion on the 26th flipped
    # `promoted` in the manifest and turned that warn into a fail() derived from
    # the flag. These two cases exist because that is exactly the moment a check
    # goes dead: it was written for a state that no longer holds, it stops
    # firing, and a silent check and a passing one read the same.
    #
    # Both mutate the manifest rather than the pages, because two pages link the
    # app - the band and the tool page - so no single-page edit can make it
    # unlinked. The first case necessarily trips the "not in public/app/" check
    # as well; what it proves is that the promoted-and-unlinked branch is
    # reachable and that its sentence still appears.
    ("an app that is promoted but that no page links",
     "is served and promoted, but no page links it",
     "assets/lockouts.json",
     lambda t: json.dumps({**json.loads(t),
                           "app": {**json.loads(t)["app"],
                                   "file": "eqls-lockouts.00000000.html"}},
                          indent=1, sort_keys=True)),

    ("a linked app whose manifest still says it is not promoted",
     "records promoted:false",
     "assets/lockouts.json",
     lambda t: json.dumps({**json.loads(t), "promoted": False},
                          indent=1, sort_keys=True)),

    # A registered tool with no card on the hub that lists the tools. This
    # shipped twice: once when the inventory reader was built, registered and
    # footer-linked with no card, and again on 18 Aug 2026 when 50 Upgrades —
    # the tool actually being posted — was missing from the grid all day while
    # a band announced it on the home page. Rule 6 only ever proved the footer.
    ("a registered tool with no card on the tools hub",
     "has no card for",
     "public/tools/index.html",
     lambda t: t.replace('<a class="card" href="50-upgrades"',
                         '<a class="card" href="50-upgrades-x"', 1)),

    # A published dataset that lost most of itself and stayed green. The
    # emptiness rule beside the floor catches a dataset that lost EVERYTHING;
    # it is blind to one that lost a third, which is the shape the consolidation
    # had waiting. assets/planar.json feeds sightings.py's match table, the two
    # catalogues share a hundred names, and removing the planar generator would
    # have taken data.items from 277 to 177 — valid JSON, right shape, not
    # empty. This proves the floor sees what emptiness cannot.
    ("a published dataset that lost a large fraction of itself",
     "below its recorded floor",
     "public/data/sightings.v1.json",
     lambda t: _shrink_dataset(t, "items", 150)),

    # The sitemap and the canonical tags disagreed on every page until 18 Aug
    # 2026 and nothing noticed, because each was internally consistent and only
    # wrong against the other. Both derive from _partials.public_path() now, and
    # this proves the comparison between them is alive: reverting one entry to
    # the .html form it used to carry must fail the build.
    ("a sitemap entry that contradicts the page's own canonical",
     "the sitemap does not list that address",
     "public/sitemap.xml",
     lambda t: t.replace("<loc>https://eqlsource.com/dungeons/najena</loc>",
                         "<loc>https://eqlsource.com/dungeons/najena.html</loc>")),

    # A count typed as a word rather than printed from the ledger. The dungeon
    # index headline read "Ten zones, surveyed" while the ledger held thirteen,
    # and nothing caught it because every count check matched digits only.
    ("a zone count spelled out and left behind",
     f"says 'Ten' for 'zones surveyed' but the data holds {N_ZONES}",
     "public/dungeons/index.html",
     lambda t: t.replace(f"{N_ZONES} zones,", "Ten zones,")),

    # The two counts that were unreachable while everything was called "items".
    # Both live on the tools hub, which printed three different quantities under
    # that one word; the gate could only ever check the first of them. These are
    # the positive half of the pair - the negative half is that check.py passes
    # on the unmutated tree, where all three counts are correct and differently
    # named, so neither rule is matching by accident.
    ("a Sky turn-in count drifting from its dataset",
     f"for 'turn-in items' but the data holds {N_TURNIN}",
     "public/tools/index.html",
     lambda t: t.replace(f"{N_TURNIN} turn-in items", f"{N_TURNIN + 1} turn-in items")),

    ("a planner catalogue count drifting from its snapshot",
     f"for 'catalogue items' but the data holds {N_CATALOGUE}",
     "public/tools/index.html",
     lambda t: t.replace(f"{N_CATALOGUE:,} catalogue items",
                         f"{N_CATALOGUE + 1:,} catalogue items")),

    # The stamp present but UNREADABLE - the other half of the same asymmetry.
    # A bare `except Exception` used to swallow this, so corrupt JSON, a KeyError
    # on "inputs", a permission error or a syntax error in stamp.py all read
    # green and the freshness detector could die completely without saying so.
    ("the build stamp is unreadable, so freshness cannot be checked",
     "could not be verified",
     "state/last-build.json",
     lambda t: t.replace('"inputs"', '"inputs_renamed"', 1)),

    # A TIER BADGE THAT RENDERS WITH NO SELECTOR TO STYLE IT.
    #
    # `class="tier tC"` shipped against a stylesheet defining `.tc`. CSS class
    # selectors are case-sensitive, so one letter was the entire defect, and it
    # was invisible: an unstyled badge still reads as text, so the page looks
    # merely plain rather than broken.
    #
    # The old check listed four classes somebody had typed. It could not notice
    # a class nobody listed, which is what tC was. The replacement derives the
    # set from the pages that actually render badges, so this case mutates the
    # STYLESHEET rather than the list.
    ("a tier badge renders with no selector to style it",
     "defines no .tC",
     "public/assets/site.css",
     lambda t: t.replace(".tC{", ".tc{", 1)),

    # ---- content hashes are SENSITIVE, not merely stable ---------------------
    #
    # R93. A hash exists so that different content produces a different value. A
    # test asserting only that a hash is STABLE across rebuilds is satisfied by
    # the literal "deadbeef"; only the sensitivity direction is load-bearing,
    # and on 31 Aug 2026 four of this repo's six hashed things had nobody
    # testing it. Each case below mutates content and requires the check to
    # notice.
    #
    # The two served apps are absent from this list on purpose. Their checks are
    # alive and were proved by hand, but they are foreign binaries and this
    # harness restores through a utf-8 text round-trip - which is lossless for
    # our own pages and NOT for a 182 KB bundle. A case of mine corrupted the
    # Sky Ledger that way once. Same reason the hashed media is reached through
    # its manifest below rather than by touching the .jpg.

    # public/assets/site.css is hand-edited and _partials.py hashes it into the
    # stylesheet URL of every page. Before this input was added to stamp.py,
    # editing it and not rebuilding left check.py at exit 0 - so the cache-
    # busting hash silently stopped being recomputed, which is the exact
    # incident _asset_v was written after.
    ("the stylesheet changed and nothing rebuilt",
     "public/ is stale",
     "public/assets/site.css",
     lambda t: t + "/* selftest */"),

    # The same input, separately, so that dropping either one from stamp.py's
    # INPUTS fails a case. One case covering both would pass on either.
    ("the webfont stylesheet changed and nothing rebuilt",
     "public/ is stale",
     "public/assets/fonts/fonts.css",
     lambda t: t + "/* selftest */"),

    # THE ENUMERATION FALLING BEHIND WHAT THE GENERATORS READ.
    #
    # This mutation removes the glob that covers _build/planar_raw.txt, which
    # _build/planardata.py opens by a literal path. That is the same condition
    # someone creates by adding a generator that reads a new kind of file, and
    # it is the condition scripts/inputscover.py exists to notice. The case is
    # built this way because there is currently NO uncovered file to point at -
    # so the only honest way to exercise the check is to re-create the gap.
    ("stamp.py stopped covering an input a generator reads",
     "does not fingerprint it",
     "scripts/stamp.py",
     lambda t: t.replace(chr(34) + "_build/*.txt" + chr(34) + ", ", "", 1)),

    # A raw build input whose EXTENSION no glob covered. stamp.py's INPUTS are
    # extension-specific, so a file in a covered directory with an uncovered
    # suffix is invisible - which is how site.css was missed, one directory
    # over. _build/planar_raw.txt is read by planardata.py, which build.sh runs
    # to write assets/planar.json.
    ("a raw build input changed and nothing rebuilt",
     "public/ is stale",
     "_build/planar_raw.txt",
     lambda t: t + "# selftest"),

    # A published dataset drifting from its own content hash. `hash` was in the
    # contract's required top-level fields, so a MISSING one failed and a WRONG
    # one passed. We tell consumers to cache on that value.
    ("a published dataset drifted from its own content hash",
     "but its data hashes to",
     "public/data/zones.v1.json",
     lambda t: _json_poke(t)),

    # The hashed media, reached through assets/media.json because the files
    # themselves are binary. Changing the recorded byte count must be caught;
    # nothing verified this manifest at all until 31 Aug 2026.
    ("hashed media disagreeing with its manifest",
     "recorded in assets/media.json",
     "assets/media.json",
     lambda t: _media_poke(t)),

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

    # named/najena.html published "the NPC record says 3" where the source says
    # 35, because a hard 190-character slice landed between the digits. Every
    # other truncation is a rough edge a reader can see; that one was a false
    # figure they could not, since a severed number looks like a whole smaller
    # one. The mutation puts a digit back in front of an existing ellipsis, so
    # it stays correct however the underlying notes change.
    ("a truncation that ends on a digit, publishing a severed number as a whole one",
     "the cut lands on a digit",
     "assets/index-data.json",
     lambda t: t.replace("\\u2026", "5\\u2026", 1)),

    # _build/build3.py copies the FIRST :root block out of site.css into the
    # fifteen self-contained pages - the thirteen surveys and two imported
    # tools - and those stay dark in both themes by design. Put a light block
    # first and fifteen pages take parchment tokens over hard-coded dark
    # backgrounds, with every other check still green: the CSS is valid, every
    # page builds, and nothing lays a page out at this stage. A cascade that
    # depends on source order needs something asserting that order.
    #
    # The mutation makes the first block define the daylight ground, which is
    # what "a light block came first" looks like from the regex's side.
    ("the first :root in site.css defining the daylight ground",
     "the first :root in site.css defines the daylight ground",
     "public/assets/site.css",
     lambda t: t.replace("--surface-0:#0B0704", "--surface-0:#EFE6D4", 1)),

    # Both daylight blocks ship now - one for the system setting, one for the
    # toggle - and they are byte-identical on purpose, because CSS has no mixin
    # and a media query cannot be combined with an attribute selector. Drift
    # between them is close to invisible: it takes a reader who uses BOTH the
    # system setting and the toggle to meet it, so it would sit there.
    #
    # The generated block is written FROM the authored one, so they cannot
    # differ at birth. This catches them being edited apart afterwards.
    ("the two daylight token blocks drifting apart",
     "daylight token blocks in site.css have drifted apart",
     "public/assets/site.css",
     lambda t: t.replace(':root[data-theme="light"]{\n  --surface-0:#EFE6D4;',
                         ':root[data-theme="light"]{\n  --surface-0:#EFE6D5;', 1)),

    # THE TIER SCALE, AND THE REASON THIS CASE EXISTS AT ALL.
    #
    # check.py guarded this block with `if os.path.exists("index.html")` and the
    # site moved to public/ long ago, so it had never run - including the
    # assertion whose own message says the scale "is the reason the site exists
    # and must stay published on the home page". Session B proved it by deleting
    # a tier name from the home page and watching check.py stay green.
    #
    # This case is that mutation, kept. It also stands as the general guard the
    # directive asked for: `if os.path.exists(X)` wrapped round an assertion
    # turns a moved file into a silent skip, and a skipped check reads exactly
    # like a passing one. If the path ever moves again, this goes TEST BROKEN
    # loudly instead of going quiet.
    ("a source tier missing from the home page's published scale",
     "names only 4 of the 5 source tiers",
     "public/index.html",
     lambda t: t.replace("Aggregator", "Aggreg&#97;tor", 1)),
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


def mutate_missing_stamp():
    """Delete the build stamp, so freshness cannot be checked at all.

    Until 31 Aug 2026 this was a warn(): the comparison FAILING blocked the
    build and the comparison being IMPOSSIBLE did not, which is backwards. An
    impossible comparison is worse than a failed one, because a failed one told
    you something true.

    The runner restores by writing `orig` back, so deleting the file here is
    safe - and it is only safe to round-trip at all because stamp.py was fixed
    the same day to write LF. It had been writing CRLF on Windows, which this
    harness would have converted while claiming to leave the tree as it found
    it.
    """
    p = "state/last-build.json"
    orig = open(p, encoding="utf-8").read()
    os.remove(p)
    return p, orig


def mutate_media_name():
    """Rename a hashed media file so its NAME no longer describes its CONTENT.

    THE BRANCH THIS REACHES WAS GUARDED BY NOTHING. check.py's media block has
    two failures: a sha1-vs-name comparison, and a byte-count comparison. The
    case written for it in #159 mutates the recorded BYTE COUNT, so it exercised
    the second and left the first - the only line that makes the media check
    content-sensitive, and the whole reason #159 touched media at all - untested.
    Proved by disabling that branch outright: the suite still reported every case
    caught.

    Reaching it from the manifest alone is not possible, and I measured that
    rather than assuming: changing the recorded filename makes the file MISSING
    and trips a third branch instead. The content cannot be edited either,
    because this harness restores through a utf-8 text round-trip and media files
    are binary - the limit stated when the media check was written.

    So the file is RENAMED, which preserves every byte, and the manifest is
    updated to match. The runner restores the manifest; the cleanup returned here
    renames the file back.
    """
    p = "assets/media.json"
    orig = open(p, encoding="utf-8").read()
    d = json.loads(orig)
    k = sorted(d)[0]
    old = d[k]["file"]
    parts = old.rsplit(".", 2)
    parts[1] = "deadbeef"
    new = ".".join(parts)
    src = os.path.join("public", "assets", "media", old)
    dst = os.path.join("public", "assets", "media", new)
    os.rename(src, dst)
    d[k]["file"] = new
    open(p, "w", encoding="utf-8", newline=chr(10)).write(
        json.dumps(d, indent=1, sort_keys=True))
    return p, orig, lambda: os.rename(dst, src)


SPECIAL = [
    ("hashed media whose name no longer describes its content",
     "a cache would serve the wrong file",
     mutate_media_name),
    ("the build stamp is gone, so freshness cannot be checked at all",
     "is missing, so build freshness could not be checked",
     mutate_missing_stamp),
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
        # A SPECIAL may return a third element: a callable that undoes side
        # effects the single-file restore below cannot reach. Added 31 Aug 2026
        # for the media-hash case, which has to RENAME a file - the only way to
        # make a name disagree with its own content without editing a binary.
        _got = fn()
        path, orig = _got[0], _got[1]
        _cleanup = _got[2] if len(_got) > 2 else None
        try:
            rc, out = check()
            results.append((label,) + judge(expect, rc, out))
        finally:
            open(path, "w", encoding="utf-8", newline="\n").write(orig)
            if _cleanup:
                _cleanup()

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
