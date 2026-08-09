# The change log, in one place. sources.html renders all of it; the home page
# shows the most recent few. Typed by what changed, so a correction is never
# mistaken for an addition.
#
# kind: "Correction" | "Addition" | "Source refresh"
ENTRIES = [
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
