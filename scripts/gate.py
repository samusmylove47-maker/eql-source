"""The propagation gate — checks that a fact cannot disagree with itself.

WHY THIS FILE EXISTS
--------------------
An external audit on 9 August 2026 found seven faults and every one was the same
fault: a correction had been found, reasoned about, written up in the change log,
and then applied in one place instead of all the places. The site said "Three
trackers" and "Five trackers" on one page. It said 209 named everywhere and 208
on the tools index, four days after a change log entry promised every count would
be printed rather than typed. It withheld six coordinates from the plot and kept
printing them in the roster. It retracted the Eye of Veeshan's hit points in the
body and left them asserted in the meta description.

`check.py` caught none of it, because it validates that pages are well-formed
rather than that they agree.

The standard was being enforced by the author's attention. This enforces it with
the build. Each check below traces to a specific fault that actually shipped —
none of them are hypothetical, and none should be removed without the fault they
prevent becoming acceptable again.

Imported and run by scripts/check.py.
"""
import json, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_build"))

STRIP = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")


def text_of(html):
    return WS.sub(" ", STRIP.sub(" ", html))


SCRIPT_TAG = re.compile(r"<(script|style)\b.*?</\1>", re.S | re.I)


def page_words(path, key):
    """Words of readable prose on a built page.

    Lives here, and is imported by scripts/prose_budget.py, because a ceiling
    measured one way and enforced another is not a ceiling. Two counts that
    agree today would drift the first time either side changed what it strips.
    """
    h = open(path, encoding="utf-8", errors="replace").read()
    # The change log is a ledger, not prose. It gains a row every time a
    # correction is published and it is meant to: the whole reason pages were
    # stripped of their revision histories was to move that record here. A
    # ceiling this side of it would eventually forbid recording a correction,
    # which is the opposite of what the ratchet is for. Only the rows after the
    # anchor are exempt — `zrow` is the site's row class generally, so an
    # unscoped strip would blind the ratchet on the home and dungeon indexes.
    if key == "sources.html":
        cut = h.find('id="changelog"')
        if cut > 0:
            h = h[:cut] + re.sub(r'<div class="zrow".*?</div>', " ",
                                 h[cut:], flags=re.S)
    t = re.sub(r"&[a-z]+;", " ", re.sub(r"<[^>]+>", " ", SCRIPT_TAG.sub(" ", h)))
    return len([w for w in t.split() if any(c.isalpha() for c in w)])


def run(pages, fail, warn):
    Z = json.load(open("assets/zones-index.json", encoding="utf-8"))
    IX = json.load(open("assets/index-data.json", encoding="utf-8"))

    # ---- 1. counts derived from data may not be contradicted in prose --------
    #
    # The truth is the data file. A page may say a number or not say it, but it
    # may not say a different one. Each pattern is anchored to the words the
    # site actually uses, because "176 named mobs plotted" is a different
    # quantity from "209 named recorded" and conflating them would make this
    # check lie.
    truth = {
        "named recorded": len(IX["named"]),
        "items indexed": len(IX["items"]),
    }
    LABELLED = [
        (re.compile(r"(\d[\d,]*)\s+items?,\s*(\d[\d,]*)\s+named"), ("items indexed", "named recorded")),
    ]
    for p in pages:
        t = text_of(open(p, encoding="utf-8", errors="replace").read())
        for rx, labels in LABELLED:
            for m in rx.finditer(t):
                for got, label in zip(m.groups(), labels):
                    n = int(got.replace(",", ""))
                    if n != truth[label]:
                        fail(f"{p} says {n} for '{label}' but the data holds "
                             f"{truth[label]} — print the count, never type it")

    # ---- 2. verification counts agree with the ledger ------------------------
    nfull = sum(1 for z in Z if z["verify_level"] == "full")
    npart = sum(1 for z in Z if z["verify_level"] == "partial")
    for p in pages:
        t = text_of(open(p, encoding="utf-8", errors="replace").read())
        for m in re.finditer(r"(\d+)\s+fully verified", t):
            if int(m.group(1)) != nfull:
                fail(f"{p} claims {m.group(1)} fully verified; the ledger says {nfull}")
        # The gaps page once said five plates had not cleared the standard on
        # the same page whose change log said all ten had.
        for m in re.finditer(r"(\w+) of the ten plates have not cleared", t):
            words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                     "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
            got = words.get(m.group(1).lower())
            if got is not None and got != npart:
                fail(f"{p} says {m.group(1)} plates have not cleared the standard; "
                     f"the ledger says {npart}")

    # ---- 3. a full zone may not still name an open gate ---------------------
    for z in Z:
        g = (z.get("verify_gate") or "").lower()
        if z["verify_level"] == "full" and ("is still open" in g or "still open:" in g):
            fail(f"{z['slug']} is marked full but its verify_gate still names an open gate")

    # ---- 4. withheld coordinates may not reach a page -----------------------
    #
    # They were withheld from the plot and kept printing in the roster, which is
    # the table a reader navigates by.
    try:
        from withheld import WITHHELD
    except ImportError:
        WITHHELD = set()
        warn("_build/withheld.py could not be imported — withholding is unchecked")
    for slug, name in sorted(WITHHELD):
        path = f"public/dungeons/{slug}.html"
        if not os.path.exists(path):
            continue
        h = open(path, encoding="utf-8", errors="replace").read()
        row = re.search(r'<td class="nmob">' + re.escape(name) + r"</td>\s*<td class=\"loc\">(.*?)</td>",
                        h, re.S)
        if not row:
            warn(f"{path}: no roster row found for withheld mob {name!r} — cannot verify")
            continue
        cell = row.group(1)
        if re.search(r"\d", cell):
            fail(f"{path} prints a coordinate for {name!r}, which is withheld: {text_of(cell).strip()!r}")

    # ---- 5. metadata may not assert what the body will not ------------------
    #
    # The Eye of Veeshan's meta description published 32,000 HP as fact while the
    # body carried it as a T5 pre-launch import. The metadata is the version that
    # reaches search snippets and Discord embeds, so it is the version that
    # matters most and was the only one nobody checked.
    LOW = re.compile(r'class="tier t[45]"')
    # Words the body uses when it will not stand behind a figure. The badge
    # alone is not enough: the Eye of Veeshan page badges the number once and
    # then discusses it twice in prose - "unverified for Legends", "the 32,000
    # hit points come from" - and an all-occurrences rule let it through.
    HEDGE = re.compile(r"unverified|unconfirmed|disputed|retract|pre-launch|"
                       r"import|not confirmed|cannot be confirmed|we do not|"
                       r"no longer|superseded", re.I)
    for p in pages:
        h = open(p, encoding="utf-8", errors="replace").read()
        m = re.search(r'<meta name="description" content="([^"]*)"', h)
        if not m:
            continue
        desc, body = m.group(1), h[m.end():]
        for num in set(re.findall(r"\b\d[\d,]{2,}\b", desc)):
            # If the description qualifies it itself, it is not asserting it.
            near_desc = desc[max(0, desc.find(num) - 120):desc.find(num) + 120]
            if HEDGE.search(near_desc):
                continue
            for i2 in (i3.start() for i3 in re.finditer(re.escape(num), body)):
                ctx = body[max(0, i2 - 260):i2 + 260]
                if LOW.search(ctx) or HEDGE.search(text_of(ctx)):
                    fail(f"{p} asserts {num} flatly in its meta description while the "
                         f"body qualifies it — the metadata is the version that reaches "
                         f"search snippets and Discord embeds")
                    break

    # ---- 5b. a zone's respawn may not be contradicted on its own page --------
    #
    # Befallen shipped "4:27" in four places against a ledger of 4:30, was
    # corrected, and then a spelled-out "4 minute 27 second" survived the fix
    # because it matched no digit pattern. Twice is a class of fault, not an
    # accident, so it is checked in both forms.
    WORDNUM = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
               "seven": 7, "eight": 8, "nine": 9, "ten": 10}
    for z in Z:
        page = f"public/dungeons/{z['slug']}.html"
        want = (z.get("respawn") or "").strip()
        if not want or not os.path.exists(page):
            continue
        m = re.match(r"(?:&le;|<=)?\s*(\d+):(\d\d)$", want)
        if not m:
            continue
        wmin, wsec = int(m.group(1)), int(m.group(2))
        t = text_of(open(page, encoding="utf-8", errors="replace").read())
        seen = set()
        # Only durations the page itself calls a respawn. Without this the check
        # reads "4 min recast" off an item and reports it as a respawn, which is
        # the sort of noise that gets a checker switched off.
        NEAR = re.compile(r"respawn|spawn timer|turns over|repop", re.I)

        def near_respawn(at):
            return bool(NEAR.search(t[max(0, at - 90):at + 90]))

        for mm in re.finditer(r"\b(\d+)\s*(?:minute|min)s?\s*(?:(\d+)\s*(?:second|sec)s?)?", t):
            if near_respawn(mm.start()):
                seen.add((int(mm.group(1)), int(mm.group(2) or 0)))
        for mm in re.finditer(r"\b(\w+)\s+minute\s+(\w+)\s+second", t, re.I):
            a1, b1 = WORDNUM.get(mm.group(1).lower()), WORDNUM.get(mm.group(2).lower())
            if a1 and near_respawn(mm.start()):
                seen.add((a1, b1 or 0))
        for got in seen:
            # only flag values close enough to be the same claim said differently
            if got != (wmin, wsec) and abs(got[0] - wmin) <= 1 and got[0] > 0:
                fail(f"{page} says a respawn of {got[0]}:{got[1]:02d} while the ledger "
                     f"says {want} — the same figure, two values")

    # ---- 5c. every share card must exist and be the right size --------------
    #
    # og:image is an absolute URL, so nothing in the normal link check can see
    # it. A page that points at a card we never generated shows a blank embed in
    # Discord, which is worse than having no card at all: it looks broken rather
    # than plain.
    for p in pages:
        h = open(p, encoding="utf-8", errors="replace").read()
        m = re.search(r'<meta property="og:image" content="([^"]+)"', h)
        if not m:
            fail(f"{p} has no og:image - it will share as a bare link")
            continue
        name = m.group(1).rsplit("/", 1)[-1]
        card = os.path.join("public", "assets", "og", name)
        if not os.path.exists(card):
            fail(f"{p} points at share card {name}, which does not exist. "
                 f"Run python3 _build/ogcards.py")

    # ---- 6. prose may not grow -----------------------------------------------
    #
    # The site reached 67,752 words before anyone measured it. Not one page was
    # written carelessly; every paragraph justified itself at the time, and the
    # total was still four times what a reader wants. Two people who both like
    # writing will not catch that by reading.
    #
    # assets/prose-budget.json holds a per-page ceiling. A page may shrink freely
    # and the ceiling follows it down on the next commit; a page may not grow.
    # Trimming is the only direction this ratchet turns.
    try:
        budget = json.load(open("assets/prose-budget.json", encoding="utf-8"))
    except (OSError, ValueError):
        budget = None
        warn("assets/prose-budget.json is missing — prose growth is unchecked")
    if budget is not None:
        for p in pages:
            key = p.replace(os.sep, "/").replace("public/", "")
            cap = budget.get(key)
            if cap is None:
                continue
            n = page_words(p, key)
            if n > cap + 40:          # a little slack for a genuine new fact
                fail(f"{key} has grown to {n:,} words against a ceiling of {cap:,}. "
                     f"Cut something, or move it to Accuracy, Learn or the change log")

    # ---- 6. no tool may be orphaned from the footer -------------------------
    #
    # The faction impact checker, the most original tool on the site, appeared in
    # no footer on any page and was reachable only from the tools index.
    try:
        from _partials import TOOLS
        listed = {t["slug"] for t in TOOLS}
    except ImportError:
        listed = None
        warn("_build/_partials.py has no TOOLS registry — tool nav is unchecked")
    if listed is not None:
        on_disk = {os.path.basename(f)[:-5] for f in os.listdir("public/tools")
                   if f.endswith(".html") and f != "index.html"}
        for missing in sorted(on_disk - listed):
            fail(f"public/tools/{missing}.html exists but is not in the TOOLS registry, "
                 f"so it is in no footer on any page")
        for ghost in sorted(listed - on_disk):
            fail(f"TOOLS lists {ghost!r} but public/tools/{ghost}.html does not exist")
        for p in pages:
            h = open(p, encoding="utf-8", errors="replace").read()
            if "site-foot" not in h:
                continue
            foot = h[h.rfind("<footer"):]
            for slug in sorted(listed):
                if f"tools/{slug}.html" not in foot:
                    fail(f"{p}: footer does not link tools/{slug}.html")
                    break
