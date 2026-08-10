# The change log, in one place. sources.html renders all of it; the home page
# shows the most recent few. Typed by what changed, so a correction is never
# mistaken for an addition.
#
# kind: "Correction" | "Addition" | "Source refresh"
ENTRIES = [
    dict(kind="Addition", date="11 Aug 2026", title="The Plane of Sky, measured and redrawn",
         body="Sky's teleporters form a <strong>ring</strong> &mdash; island 8 returns you to island 1 &mdash; so the six-boss circuit everyone runs is not a list to memorise, it is one and a half laps. The page is built on that, on the key chain, and on a thing nobody has published: <strong>the zone read from its own mesh</strong>. 21 separate bodies of walkable floor across <strong>2,878 units of height</strong>, drawn as a side elevation. It is deliberately unlabelled &mdash; the mesh says where every piece of floor is and cannot say which piece is island 4, and ten <code>/loc</code> readings would fix that permanently. The old page was one player's solo route framed by their trio and gear, which is a fact about a player rather than about the zone"),
    dict(kind="Addition", date="11 Aug 2026", title="Contributors are credited in one place now",
         body="Findings used to be credited inline, so a survey read a player's name in the middle of a sentence about loot. That buried the thanks and gave creators nothing back. Claims now carry what a reader needs to weigh them &mdash; the kind of source, the date, the tier badge &mdash; and <a href=\"credits.html\">every contributor is named once</a>, with a link to their own work where they have one. Wiki editor usernames stay inline: those are citations rather than credits, and the provenance test needs them"),
    dict(kind="Addition", date="11 Aug 2026", title="A planar gear tool, and 116 item records behind it",
         body="Your trio can wear planar armour from all three of its classes plus the two shared "
              "sets, so <strong>five sets compete for every slot</strong>. The tool shows that pool, "
              "ranks it by a named preset &mdash; highest AC, mana and casting, most total stats, "
              "clicky effects, resistances &mdash; and lets you lock a target per slot, two for "
              "wrist. <strong>No weights to configure.</strong> Built on 116 pieces mined from the "
              "item records, with 1,219 blank fields kept blank rather than filled with zeroes. "
              "The idea came from a guild member who did it by hand with an AI first &mdash; "
              "<a href=\"credits.html\">credited here</a>"),
    dict(kind="Correction", date="11 Aug 2026", title="The planar class-group split is gone",
         body="Our Fear and Hate surveys divided every drop into two class groups, following the "
              "imported wiki tables. <strong>A guild loot guide lists them merged</strong> &mdash; "
              "slot-specific, not group-specific &mdash; and adds that any of those mobs can drop "
              "the matching Lustrous Russet or Midnight Clad piece. It also moves a turmoil toad "
              "from Hands to Wrist. Both surveys corrected and flagged as one pre-launch source. <strong>The haunted chest question is now settled:</strong> two "
              "independent Legends-era accounts seven weeks apart, one post-launch, both say "
              "Lustrous Russet only, against the imported claim of any planar piece"),
    dict(kind="Addition", date="10 Aug 2026", title="Kedge Keep surveyed",
         body="Survey 13, and the highest experience rate we have recorded &mdash; <strong>ZEM 139, "
              "or 185%</strong>, which the 23 June patch note singles out as deliberate: "
              "&ldquo;Kedge has retained its original modifier for those willing to brave the "
              "depths.&rdquo; <strong>Four class epics converge on Phinigel Autropos</strong> "
              "&mdash; Wizard, Bard, Rogue and Magician &mdash; which makes it the place to test "
              "whether the Fiery Avenger result generalises. The floor plan carries a "
              "caveat we have not needed before: our plans draw walkable floor, and this is a zone "
              "you swim through, so it under-draws where you can actually go"),
    dict(kind="Correction", date="10 Aug 2026", title="Two counts were typed instead of printed",
         body="The dungeon index headline read &ldquo;Ten zones, surveyed&rdquo; with thirteen in "
              "the ledger, and the 404 page offered &ldquo;Five trackers&rdquo; against a six-tool "
              "registry. Both were spelled out as words in templates, and every count check the "
              "build had matched digits only. Both now print from the data, and the gate reads "
              "words as well as numerals"),
    dict(kind="Addition", date="10 Aug 2026", title="Plane of Fear and Plane of Hate surveyed",
         body="Surveys 11 and 12, and the first two written knowing that almost everything "
              "published about them is Project 1999 text. Both carry armour tables by slot and "
              "class group, and Hate carries the ten minibosses mapped onto the trash each one "
              "upgrades. <strong>The floor plans are read from the game&rsquo;s own meshes.</strong> "
              "Hate separates into three levels and the middle one &mdash; ten units deep, 367 "
              "disconnected pieces &mdash; is the rooftops players cross with levitate to avoid "
              "ground aggro. No flattened map can show that, and no one else publishes it. "
              "Four published boss coordinates were checked against our own geometry and all four "
              "land on drawn floor"),
    dict(kind="Correction", date="10 Aug 2026", title="The plane boss pages are classic EverQuest",
         body="Checked against the wiki&rsquo;s revision API rather than its page footers. Every "
              "Fear and Hate boss page is a Project 1999 import &mdash; Cazic Thule and Innoruuk "
              "both from <code>imported&gt;CrazyPro</code>. The Cazic Thule strategy recommends "
              "&ldquo;several dozen melee and a dozen+ healers&rdquo; in a game that caps raids at "
              "8, and every published respawn timer describes an open-world spawn the 16 June patch "
              "note removed. One exception: Innoruuk carries 156,000 HP at D2 and 235,000 at D4, "
              "the only difficulty-tiered plane-boss figure published anywhere. It is a pre-launch "
              "beta edit with no stated method, so it prints badged and nothing is built on it"),
    dict(kind="Addition", date="10 Aug 2026", title="Every item and every named mob now has its own page",
         body="655 new addresses &mdash; <a href=\"items/index.html\">446 items</a> and "
              "<a href=\"named/index.html\">209 named mobs</a>, each carrying what we hold on it and "
              "linking back to the survey it was mined from. Until now all of it lived inside one "
              "search box, so there was nothing to bookmark, paste into guild chat or link to. "
              "The Index is unchanged and still the fastest way to filter"),
    dict(kind="Correction", date="10 Aug 2026", title="Item stats read off a shared table row",
         body="27 loot rows list several items behind a single stats cell, and splitting those rows "
              "copied the one stats line onto each item &mdash; so <em>Red Dragon Scales</em> "
              "carried a description of a tooth and a book of prayers. 90 items were affected. The "
              "stats now say they describe the row rather than the item"),
    dict(kind="Correction", date="10 Aug 2026", title="Two gaps closed, and neither was still open",
         body="<strong>Placeholder removals</strong> was answered by the developers&rsquo; own patch "
              "note, which names all eleven zones placeholders were removed from; it had been carried "
              "as unresolved since launch. <strong>Five missing maps</strong> was closed when "
              "<code>geometry.py</code> replaced the hand plots &mdash; all ten surveys have had a "
              "floor plan read from the game meshes since 10 August. What the plans still lack is "
              "room names, and that is what the gap says now"),
    dict(kind="Correction", date="10 Aug 2026", title="A third of the item catalogue had no class data",
         body="Building the levelling route surfaced it: <strong>160 of 452 items carried no class "
              "list</strong>, and every item in Castle Mistmoore and The Hole was affected. Three "
              "faults, all in the extractor. Some surveys head that column &ldquo;Classes&rdquo; "
              "and others &ldquo;Classes &amp; races&rdquo;, and an exact-match lookup returned "
              "nothing for the second kind. A <code>&lt;br&gt;</code> between the classes and the "
              "races was flattened away, turning &ldquo;WAR PAL RNG SHD&rdquo; into "
              "&ldquo;SHDall&rdquo; and hiding the last class on every such row. And worst, "
              "<strong>a cell the parser could not read defaulted to ALL</strong> &mdash; inventing "
              "permission for every class to use an item whenever the parse failed. Earthshaker "
              "read as usable by everyone; it is WAR PAL RNG SHD. The Index&rsquo;s class filter "
              "was silently dropping a third of the catalogue. 157 items still have no class list "
              "and now say so: they come from quest-component tables that carry no class column at "
              "all, which is a real absence rather than a parse failure"),
    dict(kind="Addition", date="10 Aug 2026", title="One character sheet, one link",
         body="The site had three save states &mdash; the race tracker, the Plane of Sky tracker, "
              "and the calculator sharing the race tracker&rsquo;s key. Three links to keep, three "
              "things to lose, and <strong>nobody keeps three links</strong>. The character sheet "
              "carries all of it in one address: name, race, primary class, trio, level, race "
              "unlock progress and Sky progress. Open that link on another machine and the sheet "
              "rebuilds &mdash; <strong>and so do both trackers</strong>, because the sheet writes "
              "their state back for them. Still no account and still nothing transmitted: "
              "everything after the <code>#</code> stays in the browser and is never sent here. "
              "<strong>What it deliberately does not do is decode the Sky bitfield.</strong> "
              "Parsing that structure out of the tracker gave 200 components where the tool itself "
              "reports 222, and a count that might be wrong is worse than no count, so the sheet "
              "shows the trio and links out for the detail. Epic progress is absent for the same "
              "reason &mdash; the site holds no structured epic data, and a checklist invented from "
              "loot tables would be a guess"),
    dict(kind="Addition", date="10 Aug 2026", title="Every page now has a share card and a canonical address",
         body="Zero of the site&rsquo;s 33 pages carried an <code>og:image</code>. EverQuest "
              "communities coordinate in Discord, and <strong>a link with no card is a link nobody "
              "opens</strong> &mdash; so every page we wrote was invisible at the exact moment "
              "somebody tried to share it. There are 17 cards now, drawn from the zone data itself: "
              "name, level band, ZEM, respawn and verification state, so a card cannot drift from "
              "the page it represents. <strong>Also fixed: no page had a canonical address.</strong> "
              "Every internal link ends in <code>.html</code> and the host redirects it to the "
              "extensionless form, which gave every page two addresses and let a search engine pick. "
              "32 of 33 now name the right one &mdash; the 404 page deliberately does not. And "
              "fifteen standalone pages had no description at all, so their embeds would have "
              "carried a title and an image and no sentence; they take their subtitle now, with the "
              "level band and respawn appended"),
    dict(kind="Correction", date="10 Aug 2026", title="Placeholders: the answer was in the patch notes the whole time",
         body="The developer patch note removes placeholders by name from <strong>eleven "
              "dungeons</strong> &mdash; The Hole, Nagafen&rsquo;s Lair, Lower Guk, Lair of the "
              "Splitpaw, The Warrens, Castle Mistmoore, Upper Guk, Crushbone, Befallen, Blackburrow "
              "and Najena. That is every zone this site surveys, plus Upper Guk. <strong>Named spawn "
              "every cycle and every inherited spawn percentage on the site is historical.</strong> "
              "We carried this as an open question for a day, weighing a wiki category page against "
              "our own play, while the answer sat in a tier 1 source nobody had gone back to read. "
              "The percentages stay printed rather than deleted &mdash; deleting what a source says "
              "is how a record stops being checkable &mdash; but every survey now says plainly that "
              "they describe nothing about the zone now. <strong>The same patch note lowers maximum "
              "respawn times and publishes no figures</strong>, so every respawn here remains a "
              "pre-patch ceiling and is labelled as one"),
    dict(kind="Correction", date="10 Aug 2026", title="Ten source warnings become one table",
         body="The Accuracy page carried ten near-identical prose blocks, each stating the same "
              "four facts about a wiki page in a different order. They are one sorted table now, "
              "with a revision column: zone, last edited, revision id, editor, whether the page "
              "began as a Project 1999 import, and what that means for the survey. <strong>Where a "
              "field was never established the cell says &ldquo;not recorded&rdquo;</strong> rather "
              "than sitting empty, because an empty cell reads as nothing to report and that is a "
              "different claim. Thirteen cells say it. Also removed: 355 words arguing that the "
              "hand-drawn plots were internally consistent, which was a defence of drawings retired "
              "the same day"),
    dict(kind="Correction", date="10 Aug 2026", title="The plates are retired, and kept",
         body="This site began as ten hand-built coordinate plots. Every named mob&rsquo;s "
              "<code>/loc</code> read off the wiki, transformed into page space and drawn by hand "
              "with a numbered legend beside it. The pages were called <em>plates</em> because that "
              "is what they were. <strong>They are redundant now.</strong> The floor plans derived "
              "from the game&rsquo;s own mesh archives are better in every direction that matters: "
              "the walls are the game&rsquo;s walls rather than an outline drawn around some dots, "
              "the storeys separate, the named filter by storey, and every coordinate is checked "
              "against walkable floor at build time &mdash; which is how six impossible Najena "
              "positions were caught and withheld. The hand plots could not have caught them, "
              "because they had nothing to check against. So the guides are <strong>Dungeon "
              "surveys</strong> from today, and the ten original plates move whole to "
              "<a href=\"archive/index.html\">the archive</a>, stored exactly as they last "
              "shipped. Not deleted and not tidied: they are the record of how the survey was done "
              "before it could be done properly, and anyone who wants to judge whether we improved "
              "or merely changed can put the two side by side"),
    dict(kind="Addition", date="10 Aug 2026", title="Is it still true? &mdash; the register of inherited advice",
         body="Almost everyone playing Legends played EverQuest, and arrives carrying twenty-five "
              "years of habit. Some of it holds and some was quietly replaced, and <strong>the wiki "
              "cannot tell you which is which, because large parts of the wiki are the old "
              "text</strong>. One entry per piece of inherited advice, each with its evidence, its "
              "date, and what it would take to settle it. Six to start: multiclass, difficulty not "
              "raising mob levels, placeholders in the revamped dungeons, the Per-Level Hunting "
              "Guide, underwater weapon types, and whether Paragon of Spirit stacks with Clarity. "
              "<strong>Three are open, and that is the normal state rather than a failure.</strong> "
              "The last of those exists because an AI assistant answered the stacking question by "
              "citing eqlwiki's Buff Lines page for &ldquo;slots nine, ten and eleven&rdquo;. That "
              "page describes slots 1&ndash;8 and a Layer 2, never mentions Paragon of Spirit, and "
              "the spell has no wiki page at all &mdash; the URL returns 404. Asked to be more "
              "certain, the same tool returned more sources and more specific detail: confidence "
              "rose, evidence did not. That pattern is worth more than the spell"),
    dict(kind="Correction", date="10 Aug 2026", title="Najena's spawn percentages, and a T5 number in a structured field",
         body="Two faults on the flagship plate, both found by an outside reader and both worse than "
              "reported. <strong>The header carried a 19:00 zone respawn and argued it was "
              "current.</strong> It is not a zone figure: it comes from the wiki zone page's prose, "
              "on a page carrying <code>{{Classic Era}}</code>, so by our own standard it is import "
              "text. The infobox on that same page gives the zone spawn timer as <strong>4:50</strong>, "
              "corrected there on 4 August. The ~19 minute figure is a per-mob cycle and is now "
              "labelled as one. Publishing a tier 5 prose number in a structured field and then "
              "reasoning about whether it was current is the exact mistake this site exists to "
              "catch. <strong>Separately, the spawn percentages are almost certainly meaningless.</strong> "
              "Four sources say the revamped dungeons have no placeholders &mdash; the 23 June patch "
              "note promising &ldquo;a striking lack of placeholders&rdquo;, eqlwiki's Named Mobs "
              "category, and Avenrae's own play across ten or more consecutive cycles at The "
              "Tenderizer with no placeholder seen, plus hours in Befallen and Blackburrow. Only "
              "individual wiki mob pages still describe placeholders, in classic text nobody has "
              "revisited. The figures stay printed and struck through: deleting them would hide what "
              "the source says. A log across several cycles at one camp settles it outright. "
              "<strong>Drelzna also gained three drops</strong> her wiki record carries and this "
              "plate never did &mdash; Dark Elf Parts, Bronze Greaves and Tentacle Whip"),
    dict(kind="Addition", date="10 Aug 2026", title="Tier C, for a first-hand report that is not a log",
         body="The source scale ran M, 1, 2, 3, 4, 5, and a named player saying &ldquo;I did this last "
              "night and it did not work the way the wiki says&rdquo; fitted none of them. It is not "
              "tier M &mdash; nothing was parsed, and recollection is not a log. It is not 3 to 5, "
              "which are readings of documents. <strong>Tier C sits below M and above 3: first-hand, "
              "named, dated, unconfirmed</strong>, and every claim carrying it publishes who reported "
              "it, when, what would confirm it, and that it has not been. A Tier C claim never becomes "
              "fact by repetition &mdash; it is confirmed and moves, or it stays C visibly. "
              "<strong>This applies to us as well:</strong> our logs are tier M because a parser read "
              "them; our memories are not, and exempting ourselves would be the fastest way to corrupt "
              "the scale"),
    dict(kind="Correction", date="9 Aug 2026", title="A verification gate that could not be passed",
         body="Gate 3 of the verification standard asked that coordinates be collision-checked "
              "against the room list. <strong>There is no room list.</strong> Across the five zones "
              "then held at <em>partial</em>, not one room carried a coordinate and 9 of 209 named "
              "mobs named a room or floor at all &mdash; so the check had no left-hand side and "
              "could not be failed, passed or attempted. Five zones sat waiting on it, which read as "
              "work remaining when the truth was that the test did not fit our data. <strong>Gate 3 "
              "is now the geometry check</strong>: every coordinate must land within 120 units of "
              "the walkable floor extracted from the game's own mesh files, counted at build time "
              "rather than typed. It is the stronger test for whether a position is real &mdash; it "
              "is how six impossible Najena coordinates were found and withheld &mdash; and the "
              "weaker one for whether a position matches the room its note names. That trade is "
              "stated in the standard rather than buried. Closing the change, <strong>The Warrens "
              "cleared gate 1</strong>: its page was fetched in full for the first time and all 17 "
              "named mobs, the 6:40 respawn and the 4&ndash;25 level range all agree; and "
              "<strong>Blackburrow gained the reading key</strong> it was the only plate of ten to "
              "lack. All ten zones are now fully verified, 176 of 176 coordinates on drawn floor"),
    dict(kind="Source refresh", date="9 Aug 2026", title="The Hole, three weeks behind its own source",
         body="The plate cited the wiki as last edited 15 July. Taken from the API rather than the "
              "page footer, it had been edited <strong>six times on 8 August</strong>, the last at "
              "21:25. Re-compared in full: every named mob the wiki lists is on the plate and the "
              "respawn still agrees at 7:48, so nothing was wrong &mdash; but <strong>Slizik the "
              "Mighty gained a coordinate</strong>, 372, &minus;88, where the plate had only "
              "&ldquo;back of the Ratman Jail&rdquo;. It lands 10 units from drawn floor, so it "
              "checks out against the zone geometry as well as against the source"),
    dict(kind="Correction", date="8 Aug 2026", title="Befallen's respawn, and a source two months stale",
         body="Two faults on one plate, both found by taking the wiki's edit history from the API "
              "instead of its page footer. <strong>The plate said its source was last edited 7 June "
              "2026. It was last edited 5 August</strong>, revision 166594 &mdash; and the plate "
              "reasoned from the wrong date, telling readers the page &ldquo;cannot reflect anything "
              "after 7 June&rdquo; when it postdates launch and gained the Ebon Scythe on 5 August. "
              "Separately, <strong>the prose still gave the respawn as 4:27 in four places while "
              "the zone data said 4:30</strong>, corrected from the wiki on 1 August &mdash; the "
              "page and the data driving it disagreed. The roster itself checks out: all 15 named "
              "mobs on the wiki are on the plate"),
    dict(kind="Addition", date="8 Aug 2026", title="Kelynn, missing from the Crushbone roster",
         body="A named mob the plate never carried. Found by comparing our roster against the "
              "eqlwiki Crushbone page line by line during a verification pass: 16 named on the "
              "wiki, 18 on our plate, and <strong>Kelynn was on theirs and not ours</strong>. "
              "Level 9, 12% spawn, at 3, 387. The same comparison found <strong>no coordinate "
              "mismatches at all</strong> across the fifteen named mobs both sources carry, and "
              "the zone respawn agreeing at 9:00"),
    dict(kind="Correction", date="8 Aug 2026", title="Six Najena coordinates that sit outside Najena",
         body="Rathyl, Ekeros, BoneCracker, Officer Grush, Trazdon and A Visiting Priestess are "
              "recorded on eqlwiki at positions south of the zone&rsquo;s own extent, by between 57 and "
              "513 units &mdash; outside the dungeon. Najena&rsquo;s geometry runs from &minus;168 to "
              "546 on the north&ndash;south axis, measured from the map file EverQuest Legends installs "
              "with the game; two community map sets drawn independently agree to within two units. "
              "The east&ndash;west value is right in every case and only the north&ndash;south value is "
              "out, which points at a single column rather than at noise. Our transcription matches the "
              "source exactly, so this is the source being wrong rather than us misreading it. The six "
              "are withheld from the survey plot and listed with the reason instead. <strong>No "
              "replacement figure is published, because none is sourced</strong> &mdash; the official "
              "map carries no mob positions, so one <code>/loc</code> reading per mob closes it"),
    dict(kind="Correction", date="8 Aug 2026", title="A coordinate range read as a coordinate",
         body="A hiding gnoll in Lair of the Splitpaw is recorded as &ldquo;718&ndash;800, "
              "212&ndash;236&rdquo; &mdash; a span it appears across, not a point. The survey plot read "
              "the two ends as a north&ndash;south and east&ndash;west pair and drew it 464 units "
              "outside the zone. Ranges now join the list of mobs that vary by spawn point rather than "
              "being placed"),
    dict(kind="Correction", date="8 Aug 2026", title="The Eye of Veeshan's stat block",
         body="We published 32,000 hit points and 865 damage a swing as though they were EverQuest "
              "Legends figures. They are not. The hit points come from an eqlwiki page whose oldest "
              "revision is 25 March 2026 by an account named <code>imported&gt;Kistraxx</code> &mdash; "
              "four months before the game launched. The melee figure is contradicted inside eqlwiki "
              "itself, which gives 865 on one page and 200 on another. And the stat block lists the "
              "Eye as a single class at level 70, where Legends raid bosses run three classes from D3. "
              "Both figures now carry a T5 badge and the tanking section no longer reasons from either"),
    dict(kind="Correction", date="8 Aug 2026", title="Four respawn timers",
         body="The Hole read 21:30; eqlwiki replaced that with 7:48 on 14 July, two weeks before we "
              "captured the older value &mdash; it was stale on arrival. Befallen 4:27 to 4:30, Najena "
              "19:00 to 4:50, and Crushbone and Blackburrow gain figures they previously lacked. Each "
              "now records the revision, date, editor and comment behind it. Lower Guk's change was "
              "deliberately not adopted: the wiki raised it to 11:00, but the 28 July patch says that "
              "zone's respawn was <em>lowered</em>, and that contradiction is unresolved"),
    dict(kind="Correction", date="7 Aug 2026", title="Item count on The Index",
         body="The page described itself as holding &ldquo;389 items&rdquo; while the index it shipped "
              "held 452, and its own counter said 452 on screen. 389 was never correct at any point. "
              "Every count on the site is now printed from the mined data rather than typed by hand, "
              "so the sentence and the tool cannot disagree again"),
    dict(kind="Correction", date="6 Aug 2026", title="Verification counting",
         body="Front page claimed 8 of 10 plates verified. By the project&rsquo;s own three-gate "
              "standard it is 5. Corrected, and the open gate is now named per zone"),
    dict(kind="Correction", date="6 Aug 2026", title="Tracker state handling",
         body="Changes made in the trio builder were never saved, so reloading restored the previous "
              "trio. Reset also left the trio and the calculator selections untouched. Both trackers "
              "now have separate <em>Clear ticks</em> and <em>Start over</em> actions"),
    dict(kind="Correction", date="6 Aug 2026", title="Primary-slot logic",
         body="Calculator no longer suggests demoting a class you require in the primary slot"),
    dict(kind="Source refresh", date="5 Aug 2026", title="Race unlock data",
         body="Rebuilt against Alanna&rsquo;s guide revision 166686"),
    dict(kind="Addition", date="6 Aug 2026", title="Site launch",
         body="Ten plates, five maps, three tools, first raid encounter"),
]

TONE = {"Correction": "var(--ok)", "Addition": "var(--bone)", "Source refresh": "var(--instr)"}

# The three-letter stamp on the change log rows.
TAG = {"Correction": "FIX", "Addition": "NEW", "Source refresh": "DAT"}
