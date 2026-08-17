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
import fnmatch, glob, json, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_build"))

STRIP = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")


def text_of(html):
    return WS.sub(" ", STRIP.sub(" ", html))


SCRIPT_TAG = re.compile(r"<(script|style)\b.*?</\1>", re.S | re.I)

# (page, anchor the rows start after, regex matching one row)
LEDGERS = [
    ("sources.html", 'id="changelog"', r'<div class="zrow".*?</div>'),
    ("learn/still-true.html", "", r'<article class="st-entry".*?</article>'),
    # The dungeon index is one card per zone plus a paragraph of introduction.
    # Its word count rises every time a survey is added, so a ceiling over the
    # cards forbids adding a zone — the same shape as the other two. The
    # introduction is still governed.
    ("dungeons/index.html", 'class="plates"', r'<a class="plate[^"]*"[^>]*>.*?</a>'),
    # Same shape again: the tools index is one card per tool. A ceiling over the
    # cards forbids shipping a tool, and the tool that exposed it had been built,
    # registered and footer-linked while its card was never written - so the
    # count printed seven and the grid rendered six.
    ("tools/index.html", 'class="cards c2"', r'<a class="card"[^>]*>.*?</a>'),
    # MEASURED TABLES ARE A LEDGER; THE WORDS AROUND THEM ARE NOT.
    #
    # A survey's "Measured in play" section is a table per thing measured - the
    # mobs fought, the spells that landed, the drops seen. Every new session
    # adds rows, so a word ceiling over them means the ceiling falls every time
    # we play and eventually forbids logging another night in a zone we have
    # already logged. That is backwards: more evidence is the goal.
    #
    # This exempts only the table ROWS, and only inside the measured section.
    # The conditions paragraph above them, the prose explaining what a figure
    # does and does not mean, and the entire survey before it stay governed. So
    # the ceiling still bites on writing more, and never on measuring more.
    # Anchor on the OPENING of the tag, not the whole tag. Adding id="measured"
    # to it broke the match outright and five surveys blew their ceilings at
    # once, because every measured row started counting as prose. An anchor
    # that a new attribute can silently turn off is not an anchor.
    ("dungeons/*.html", '<section class="meas"', r"<tr>.*?</tr>"),
    # The faction tool is one card per zone we have faction data for. Same
    # shape: a ceiling over the cards forbids measuring an eleventh zone.
    ("tools/faction-impact.html", "", r'<article class="fzone">.*?</article>'),
    # The difficulty explainer's measured tables: one row per boss kill at one
    # tier. They grew from five rows to twelve the day we parsed two more
    # bosses, and a ceiling over them means the page can never report a third.
    # Anchored AFTER the ramp heading so the fixed five-row table of tier names
    # higher up stays governed, along with every word of the prose.
    ("learn/difficulty.html", "The ramp, measured", r"<tr>.*?</tr>"),
]


def without_ledger_rows(h, key):
    """Drop the append-only rows from a ledger page.

    A ledger records what was true when the row was written. The change log
    entry for 9 August says "All ten zones are now fully verified" and that was
    correct on the day — rewriting it when the site reached thirteen zones would
    be falsifying the record to satisfy a checker. So the count rules and the
    prose ceiling both read ledger pages with their rows removed, and both still
    govern everything around them.
    """
    for ledger_key, anchor, row in LEDGERS:
        # A glob so one rule can cover every survey. Written as an exact match
        # first, thirteen surveys meant thirteen near-identical entries and the
        # fourteenth zone would have shipped without one.
        if key != ledger_key and not fnmatch.fnmatch(key, ledger_key):
            continue
        cut = h.find(anchor) if anchor else 0
        if cut < 0:
            continue
        # THE EXEMPTION ENDS WHERE ITS SECTION ENDS.
        #
        # It used to run to the end of the file, which was harmless only while
        # every ledger sat last on its page. On 17 August the measured section
        # moved to the top of the Castle Mistmoore survey, and the exemption
        # anchored on it swallowed the nine tables below — the named roster,
        # every loot table, the landmarks. The ceiling went on passing while
        # governing almost nothing, which is the shape of a dead check.
        #
        # A section-scoped strip cannot do that: moving a ledger changes what
        # it exempts by nothing. Where the anchor is not a <section> the end is
        # the end of the file, as before, because those ledgers are the page.
        end = len(h)
        if anchor.startswith('<section'):
            close = h.find('</section>', cut)
            if close >= 0:
                end = close
        h = h[:cut] + re.sub(row, " ", h[cut:end], flags=re.S) + h[end:]
    return h


def page_key(path):
    return path.replace(os.sep, "/").replace("public/", "")


def page_words(path, key):
    """Words of readable prose on a built page.

    Lives here, and is imported by scripts/prose_budget.py, because a ceiling
    measured one way and enforced another is not a ceiling. Two counts that
    agree today would drift the first time either side changed what it strips.
    """
    h = open(path, encoding="utf-8", errors="replace").read()
    # Ledgers are not prose. Two pages on this site exist to accumulate a record
    # — the change log holds every correction, the register holds every finding
    # — and both were given that job when the pages were stripped of their own
    # revision histories. A word ceiling over a ledger eventually forbids
    # recording a correction or a finding, which is the opposite of what the
    # ratchet is for.
    #
    # So the ledger's rows are exempt and the rest of each page is not. Each
    # entry names the anchor its rows start after, because these row classes are
    # used elsewhere on the site and an unscoped strip would blind the ratchet on
    # the home page and the dungeon index.
    #
    # This is the whole list. Adding to it means arguing that a third page is a
    # ledger, which should be hard.
    h = without_ledger_rows(h, key)
    # Chrome is not this page's prose. The footer and the nav are identical on
    # every one of 700-odd pages, so counting them meant adding a single footer
    # link raised the word count of the entire site at once — and the page that
    # tripped its ceiling was whichever happened to be closest to it, which is
    # a ratchet measuring the wrong thing and blaming the wrong page.
    # A DRAWING IS NOT PROSE, AND ITS LABELS ARE PART OF THE DRAWING.
    #
    # The floor plans name every mob they plot, inside <svg> as <text>. Counting
    # those made the ratchet fall every time a named mob's position was
    # recorded — so plotting an eighteenth mob on Crushbone spent 18 words of a
    # budget meant to govern writing, and a zone with more named mobs was
    # penalised for having more evidence. Crushbone's plan section read 700
    # words, of which the map's own labels were most.
    #
    # Same reasoning as the ledger rows above: the ceiling must bite on writing
    # more and never on measuring or drawing more. Everything outside the <svg>
    # — the lede, the legend, the caveats under it — stays governed.
    h = re.sub(r"<svg\b.*?</svg>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<footer\b.*?</footer>", " ", h, flags=re.S | re.I)
    h = re.sub(r'<header class="site-bar".*?</header>', " ", h, flags=re.S | re.I)
    h = re.sub(r'<div class="ns-bar".*?</div>', " ", h, flags=re.S | re.I)
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
        "named recorded": IX["counts"]["named_pages"],
        # THE GATE'S OWN TRUTH WAS THE WRONG NUMBER. len(IX["items"]) is 451:
        # the raw row count, which includes the 6 groups and 4 fragments that
        # are not items and get no page. extract.py declares the real figure as
        # counts.item_pages = 435, and the home page and The Index both print
        # that. So the check that exists to stop a count drifting was holding a
        # value no page should ever print, and would have failed a correct page
        # while passing tools/index.html, which printed 451 for months.
        "items indexed": IX["counts"]["item_pages"],
        "zones surveyed": len(Z),
        "tools listed": None,          # filled below, once _partials is importable
    }
    try:
        from _partials import TOOLS as _T
        truth["tools listed"] = len(_T)
    except Exception:
        truth.pop("tools listed")

    # Spelled-out counts are how this one got through. The dungeon index headline
    # read "Ten zones, surveyed" with thirteen in the ledger, and the 404 offered
    # "Five trackers" against a six-tool registry, because both were typed into a
    # template while every other count on the page was printed from data. Words
    # and digits are both checked now.
    WORDNUM = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
               "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
               "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15}

    def as_int(tok):
        tok = tok.replace(",", "").strip().lower()
        return int(tok) if tok.isdigit() else WORDNUM.get(tok)

    LABELLED = [
        (re.compile(r"(\d[\d,]*)\s+items?,\s*(\d[\d,]*)\s+named"), ("items indexed", "named recorded")),
    ]
    # "N trackers" was a rule here for one commit and was withdrawn. The tools
    # index legitimately writes "including the two trackers" meaning the other
    # two, not the total, and no regex tells that apart from a headline count.
    # A check that blocks correct prose gets switched off, which is worse than
    # not having it: the tool count is printed from the TOOLS registry
    # everywhere it means a total, and check 6 already fails a registry that
    # disagrees with the footers.
    SINGLE = [
        (re.compile(r"\b([\w,]+)\s+(?:zones?|surveys?)\s*,?\s*surveyed\b", re.I), "zones surveyed"),
    ]
    # The <head> is where hand-typed facts survived longest. Body counts were
    # made to print from data on 10 Aug; the meta descriptions beside them still
    # said "ten surveyed dungeons" the next day, and metadata is the only text
    # most readers ever see - it is the Discord embed and the search snippet.
    META = re.compile(r'<meta[^>]+(?:name|property)="(?:description|og:description|'
                      r'twitter:description)"[^>]+content="([^"]*)"')
    for p in pages:
        raw = open(p, encoding="utf-8", errors="replace").read()
        t = text_of(without_ledger_rows(raw, page_key(p)))
        for m in META.finditer(raw):
            t += " " + m.group(1)
        for rx, label in SINGLE:
            if label not in truth:
                continue
            for m in rx.finditer(t):
                n = as_int(m.group(1))
                if n is not None and n != truth[label]:
                    fail(f"{p} says {m.group(1)!r} for '{label}' but the data holds "
                         f"{truth[label]} — print the count, never type it")
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

    # ---- 3b. a derived figure must equal what it derives from ---------------
    #
    # zem_pct is ZEM/75 as a percentage and is stored rather than computed, so
    # it can drift from the number it comes from. Lair of the Splitpaw carried
    # 170 for a ZEM of 128 while The Hole and The Warrens carried 171 for the
    # identical 128 — and the survey then claimed 170% was "highest of the set"
    # when Kedge Keep publishes 185%. One stored figure, two published errors.
    for z in Z:
        want = round(z["zem"] / 75 * 100)
        if z.get("zem_pct") != want:
            fail(f"{z['slug']}: zem_pct is {z.get('zem_pct')} but ZEM {z['zem']} gives {want} "
                 f"— a derived figure may not disagree with what it derives from")

    # ---- 3c. a ranking claim may not be typed beside the data it ranks ------
    #
    # A cold reader found The Ruins of Old Paineel calling itself "the highest
    # zone experience modifier in the game" in its H1, its meta description and
    # both share cards. Kedge Keep is 139; The Hole is 128, level with two
    # others. Rule 3b above was already guarding zem_pct against zem and could
    # not see this, because the fault was in prose rather than in a field.
    #
    # The first repair replaced one typed superlative with four typed ordinals
    # — the same fault with better arithmetic. So the ordinals are derived now
    # (_build/derived.py, substituted by build3.py), and this refuses a survey
    # SOURCE that types one by hand again.
    #
    # It reads the sources rather than the built pages on purpose: the built
    # page is supposed to contain the phrase, having had the token filled in.
    # Deliberately narrow. The first draft flagged "the highest camp in the
    # dungeon" (about depth) and "highest of the three planes" (true, and
    # bounded to a named set it does rank). A gate that cries wolf gets its
    # exemptions widened until it catches nothing, so it only fires on an
    # unbounded ordinal sitting within 60 characters of the modifier itself.
    RANK_WORD = re.compile(
        r'\b(?:joint\s+)?(?:highest|second[- ]highest|third[- ]highest|second|third)\b',
        re.I)
    ZEM_NEAR = re.compile(r'\b(?:ZEM|experience (?:modifier|rate))\b', re.I)
    # A claim that names the set it ranks over is answerable and may stay.
    BOUNDED = re.compile(
        r'\bon this site\b|\bwe have (?:recorded|measured)\b|\bof the \w+ planes?\b'
        r'|\bof our \d+ surveys\b|\bof the (?:three|four|five)\b|\bin the dungeon\b',
        re.I)
    for src in sorted(glob.glob('_build/source/*.html')):
        raw = open(src, encoding='utf-8').read()
        for m in RANK_WORD.finditer(raw):
            window = raw[max(0, m.start() - 60):m.end() + 60]
            if not ZEM_NEAR.search(window):
                continue
            if BOUNDED.search(raw[max(0, m.start() - 90):m.end() + 90]):
                continue
            fail(f"{src} types {m.group(0)!r} beside an experience figure. "
                 f"Use @@ZEM_RANK@@ — the ranking is derived in "
                 f"_build/derived.py so it cannot go stale silently")

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

        # THE ROSTER WAS NOT THE ONLY TABLE. This checked the roster row and
        # nothing else, so Najena shipped "BoneCracker L24 · −262, 167" in its
        # key-chain list while the roster three sections below said "withheld".
        # Withholding a coordinate means withholding it from the PAGE, so the
        # whole page is checked: any "<name> ... <number>, <number>" within a
        # short span of the name is a coordinate that escaped.
        #
        # Both minus signs are matched. 141 recorded coordinates use U+2212
        # rather than ASCII hyphen, and a pattern that knows only one of them
        # would pass exactly the coordinates most likely to be missed.
        body = text_of(h)
        for m in re.finditer(re.escape(name), body):
            near = body[m.end(): m.end() + 90]
            hit = re.search(r"[-−]?\d{2,4}\s*,\s*[-−]?\d{2,4}", near)
            if hit:
                fail(f"{path} prints {hit.group(0)!r} beside {name!r}, whose coordinate is "
                     f"withheld — withholding applies to the whole page, not just the roster")
                break

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

    # ---- 5d. a template placeholder may not reach a reader -------------------
    #
    # raids/eye-of-veeshan.html shipped the literal text "{EYE_FULL:,}" in its
    # stat block on 15 Aug 2026 and passed all 723 checks. Its BODY is a plain
    # triple-quoted string - it carries the 3D engine's JavaScript, so it can
    # never be an f-string - and f-string syntax written into it is not a syntax
    # error anywhere. It renders as itself.
    #
    # Nothing here looked for that, because every other check reads what a page
    # SAYS rather than whether it finished rendering. The shapes below are the
    # ones a generator on this site can leak: an f-string field, a str.format
    # slot, and the @@TOKEN@@ convention build4.py now uses instead. Scripts and
    # styles are stripped first - a CSS rule and a JS object are full of braces
    # and none of them are placeholders.
    LEAKED = re.compile(
        r"@@[A-Z][A-Z0-9_]*@@"                      # @@EYE_FULL@@
        r"|\{[A-Za-z_]\w*(?:\[[^\]{}]*\]|\.\w+)*(?::[^{}]*)?\}")   # {EYE_FULL:,}
    for p in pages:
        h = open(p, encoding="utf-8", errors="replace").read()
        t = text_of(SCRIPT_TAG.sub(" ", h))
        for m in LEAKED.finditer(t):
            fail(f"{p} shipped an unrendered placeholder {m.group(0)!r} - the "
                 f"generator wrote template syntax into a plain string")
            break

    # ---- 5e. a plotted position must agree with the zone's own floor plan ----
    #
    # The locator on the item and named pages and the floor plan on the survey
    # pages describe the same mob from the same /loc, through two different code
    # paths. They must land in the same place.
    #
    # They did not. _build/plans.py parsed coordinates with a plain `-?\d+`,
    # and 141 of the recorded /locs use U+2212 MINUS SIGN rather than ASCII
    # hyphen, so every negative coordinate read as positive: 46 of 60 checked
    # marks disagreed with the floor plan by up to 1,508 units. Nothing looked
    # wrong — a dot on a dungeon plan looks correct wherever it is. build6.py
    # had already found and documented this hazard, which is exactly why the
    # agreement needs a check rather than a comment.
    try:
        sys.path.insert(0, os.path.join(os.getcwd(), "_build"))
        from plans import locate as _loc
        PB = json.load(open("assets/zone-plan-bounds.json", encoding="utf-8"))["zones"]
        named = {(n["z"], n["n"]): n for n in IX["named"]}
        checked = off = 0
        for p in pages:
            slug = os.path.basename(p)[:-5]
            if os.path.dirname(p).replace("\\", "/").split("/")[-1] != "dungeons":
                continue
            if slug not in PB:
                continue
            h = open(p, encoding="utf-8", errors="replace").read()
            for blk in re.findall(r'<g class="mk"[^>]*>(.*?)</g>', h, re.S):
                c = re.search(r'cx="(-?[\d.]+)"\s+cy="(-?[\d.]+)"', blk)
                t = re.search(r">([^<]+)</text>", blk)
                if not c or not t:
                    continue
                n = named.get((slug, t.group(1).strip()))
                if not n:
                    continue
                pos = _loc(PB[slug], n.get("loc") or "")
                if not pos:
                    continue
                b = PB[slug]
                dx = b["x0"] + pos[0] / 100 * b["w"] - float(c.group(1))
                dy = b["y0"] + pos[1] / 100 * b["h"] - float(c.group(2))
                checked += 1
                if (dx * dx + dy * dy) ** .5 > 1.0:
                    off += 1
                    if off <= 3:
                        fail(f"{slug}/{t.group(1).strip()}: the page locator and the floor "
                             f"plan disagree by {(dx*dx+dy*dy)**.5:.0f} game units — "
                             f"check the coordinate parser, not the drawing")
        if checked and off > 3:
            fail(f"{off} plotted positions disagree with their floor plan in total")
    except (OSError, ValueError, KeyError, ImportError):
        pass          # no plans yet is not a failure; a wrong plan is

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
