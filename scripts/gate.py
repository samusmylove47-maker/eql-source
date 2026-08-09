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
