# The change log, in one place. sources.html renders all of it; the home page
# shows the most recent few. Typed by what changed, so a correction is never
# mistaken for an addition.
#
# kind: "Correction" | "Addition" | "Source refresh"
ENTRIES = [
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
