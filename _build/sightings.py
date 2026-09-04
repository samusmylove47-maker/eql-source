"""assets/sightings.json — what we have actually watched drop.

    python3 _build/sightings.py        # run from build.sh; reads assets/measured.json

WHY THIS IS THE POINT OF THE PARSER
-----------------------------------
Every item page on this site is a transcription of what eqlwiki says drops. So
is every competitor's. The one thing we hold that nobody else does is a parsed
record of what we *saw* drop, and until now it lived in one section at the
bottom of one zone page and flowed nowhere.

This joins it. Where a mob in our logs matches a named mob in a survey roster,
and an item it dropped matches that survey's loot table, the pairing becomes a
tier M sighting printed on both pages: "seen dropping, 2 sessions, 8 Aug 2026."

A SIGHTING IS NOT A RATE
------------------------
One session is a sample. A drop seen once is seen once. Nothing here divides by
kills, and nothing here is a percentage - the count is how many times we watched
it happen, which is strictly more than the wiki offers and is not the same claim
as "how often it happens".

WHAT IS DELIBERATELY NOT PUBLISHED
----------------------------------
Of 501 distinct items observed dropping, 121 match a survey loot table. The rest
are vendor trash and `+N` gear lines - Rusty Long Sword, Ringmail Pants, Amber,
Pearl, Topaz - which fall off anything, exist to be sold, and are not tracked by
anyone for good reason. They are not published, not counted on the pages, and
not treated as a gap in the catalogue: the catalogue is right to omit them.

TWO NORMALISATIONS, BOTH LOAD-BEARING
-------------------------------------
`+N` is an upgrade tier, not part of the name: "Fine Steel Rapier +2" and "Fine
Steel Rapier" are one item. And a leading article is noise between data estates:
the roster writes "A Fallen Noble", a log writes "a fallen noble". Matching on a
key that strips both is the canonical name key an outside audit correctly said
had to exist before any of this could be joined.
"""
import os, re, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)


def key(s):
    """The canonical name key shared by the roster, the log tables and the catalogue."""
    s = re.sub(r'\s*\+\d+\s*$', '', s or '')
    s = re.sub(r'^(a|an|the)\s+', '', s.strip(), flags=re.I)
    return re.sub(r'[^a-z0-9]+', '', s.lower())


def main():
    try:
        M = json.load(open('assets/measured.json', encoding='utf-8'))
    except (OSError, ValueError):
        print('sightings: no assets/measured.json, skipped')
        return
    IX = json.load(open('assets/index-data.json', encoding='utf-8'))

    items = {}
    for i in IX['items']:
        if i.get('kind') != 'fragment':
            items.setdefault(key(i['n']), i['n'])

    # THE PLANAR SETS ARE A SECOND CATALOGUE.
    # index-data.json is mined from the dungeon surveys, so it does not contain
    # a single planar armour piece - those live in planar.json and are rendered
    # by the gear tool and /sets/. Matching against the surveys alone threw all
    # 86 measured planar set drops away as "trash", including the first
    # evidence anyone has of WHICH boss drops which set. The gear tool could
    # say what to chase and never where.
    try:
        for i in json.load(open('assets/planar.json', encoding='utf-8'))['items']:
            items.setdefault(key(i['n']), i['n'])
    except (OSError, ValueError, KeyError):
        pass
    named = {}
    for n in IX['named']:
        named.setdefault(key(n['n']), n['n'])

    pair = collections.defaultdict(lambda: {'n': 0, 'sessions': []})
    unmatched = 0
    discards_by_zone = collections.Counter()
    for s in M:
        stamp = {'date': s.get('date'), 'zone': s.get('zone'),
                 'difficulty': s.get('difficulty'),
                 'label': s.get('difficulty_label'),
                 'character': s.get('character')}
        for mob, rec in (s.get('mobs') or {}).items():
            mk = key(mob)
            for item, count in (rec.get('loot') or {}).items():
                ik = key(item)
                # AN ITEM WE HAVE NOT CATALOGUED STILL DROPPED, AND FROM A MOB WE
                # NAME IT IS EVIDENCE RATHER THAN NOISE.
                #
                # The paragraph below fixed exactly this asymmetry on the MOB
                # side and the item side kept discarding: a drop whose item was
                # not in the catalogue was thrown away before the pairing, so
                # measured evidence could only ever confirm the catalogue and
                # never extend it. That is the same sentence, one column over.
                #
                # It has already cost us once. The planar block above exists
                # because matching against the surveys alone threw away all 86
                # planar set drops - "including the first evidence anyone has of
                # WHICH boss drops which set". That was patched by adding a
                # second catalogue, which fixes the instance and leaves the rule.
                #
                # Measured 4 Sep 2026: of 5,360 discarded drops, 930 came from a
                # mob our own roster NAMES - 94 mobs, 265 distinct items,
                # including Mote of Major Potential on a site that publishes a
                # page about motes. Those are kept now and marked.
                #
                # THE REST STILL GO. A drop from an unnamed mob whose item is
                # uncatalogued is the vendor-trash case this file was built to
                # exclude, and keeping it would bury the evidence in 4,430 rows
                # of gnoll fur. The discards are reported per zone instead of
                # vanishing into one total.
                if ik not in items:
                    if mk not in named:
                        unmatched += count
                        discards_by_zone[s.get('zone') or '(no zone)'] += count
                        continue
                    off_catalogue = True
                    item_name = item
                else:
                    off_catalogue = False
                    item_name = items[ik]
                # A MOB WE HAVE NOT SURVEYED STILL DROPPED THE THING.
                # This required the mob to already appear in a survey roster,
                # which meant measured evidence could only ever confirm what we
                # had typed and never add to it. Every Plane of Fear and Plane
                # of Hate boss failed that test - we have rosters for nine of
                # them and killed twenty - so the first measured drops anyone
                # has for Innoruuk's court were discarded on the way past.
                #
                # measured.json's mob table has already applied the "is it a
                # mob" test, so a name here is evidence, not a guess. Where we
                # have a roster the roster's spelling wins, for consistency
                # with the rest of the site; otherwise the log names it and the
                # pair is marked so a page can say where the name came from.
                off_roster = mk not in named
                p = pair[(named.get(mk, mob), item_name)]
                p['off_roster'] = off_roster
                p['off_catalogue'] = off_catalogue
                p['n'] += count
                if stamp not in p['sessions']:
                    p['sessions'].append(stamp)

    by_named = collections.defaultdict(list)
    by_item = collections.defaultdict(list)
    for (mob, item), v in sorted(pair.items(), key=lambda kv: (-kv[1]['n'], kv[0])):
        rec = {'n': v['n'], 'sessions': v['sessions']}
        if v.get('off_roster'):
            rec['off_roster'] = True     # named by the log, not by a survey
        if v.get('off_catalogue'):
            rec['off_catalogue'] = True  # the item has no page; the drop is real
        by_named[mob].append(dict(item=item, **rec))
        by_item[item].append(dict(mob=mob, **rec))

    out = {
        '_comment': [
            'Observed drops, joined to the surveys. A count, never a rate.',
            'Vendor trash and +N gear lines are excluded and are not a catalogue gap.',
            'Generated by _build/sightings.py - do not hand-edit.',
        ],
        'by_named': dict(by_named),
        'by_item': dict(by_item),
        'pairs': len(pair),
        # THE OLD NAME FOR THIS WAS `excluded_trash_drops`, AND IT ASSERTED
        # SOMETHING THE CODE NEVER TESTED. Nothing here establishes that a drop
        # is vendor trash; what it establishes is that the item is not in our
        # catalogue, which is a fact about OUR coverage rather than about the
        # item. Until 4 Sep 2026 that label covered 930 drops from mobs our own
        # roster names, and calling those trash is the exact shape of fault this
        # project keeps finding elsewhere - a label is where a number stops
        # saying which quantity it is.
        #
        # Nothing read the old field. It was written once and consumed nowhere,
        # so the name was a claim made to no one and checked by nothing.
        'uncatalogued_drops_excluded': unmatched,
        # PER ZONE, BECAUSE ONE TOTAL CANNOT BE ACTED ON. A zone contributing
        # most of the discards is a zone whose catalogue is thin, which is a
        # survey lead rather than a rounding error.
        'uncatalogued_by_zone': dict(discards_by_zone.most_common()),
    }
    json.dump(out, open('assets/sightings.json', 'w', encoding='utf-8',
                        newline='\n'), indent=1)
    _oc = sum(1 for rows in by_item.values() for r in rows if r.get('off_catalogue'))
    print(f"sightings.json: {len(pair)} named-to-item pairs across {len(by_named)} mobs "
          f"and {len(by_item)} items ({_oc} of them off-catalogue; "
          f"{unmatched:,} uncatalogued drops from unnamed mobs excluded)")


if __name__ == '__main__':
    main()
