# The change log, in one place. sources.html renders all of it; the home page
# shows the most recent few. Typed by what changed, so a correction is never
# mistaken for an addition.
#
# kind: "Correction" | "Addition" | "Source refresh"
ENTRIES = [
    dict(kind="Correction", date="14 Aug 2026", title="The item count disagreed with itself again",
         body="An audit raised this on 11 August as <em>452 items against 446</em>. We fixed the numbers and not the cause, so it came back as <strong>451 against 441</strong> &mdash; and both were wrong. The home page counted every row, including families and elided fragments that are not items at all; The Index filtered the fragments but not the families; the A&ndash;Z counted the pages it had just written. <strong>There are 435 items</strong>, in 440 rows because a few drop in two zones, plus <strong>6 families</strong> the surveys name as a line rather than piece by piece. A <code>kind</code> field has existed since 11 August to say which is which and not one of the three counts read it. It is counted once now, where the data is made, and <strong>the build refuses to finish if the pages written disagree with the count declared</strong> &mdash; which it did, on the first run, by exactly the six families"),
    dict(kind="Addition", date="14 Aug 2026", title="The plane gods, measured",
         body="The largest gap this site has listed: <em>which kits attach to the plane bosses at D3 and above is recorded nowhere</em>. <strong>Cazic-Thule killed at Adaptive, Fused and Refined; Innoruuk at Fused and Refined</strong>, with ten of Innoruuk&rsquo;s court beside them, and every spell each cast is now on record. <strong>Cazic-Thule runs a shadow knight&rsquo;s kit</strong> &mdash; Harm Touch, Life Leech, Dooming Darkness, Shadow Vortex &mdash; and hits for 38 to 492. <strong>Innoruuk mixes three</strong>: wizard (Ice Comet, Wrath of Al`Kabor), shaman (Malosi, Plague, Gale of Poison) and priest (Superior Healing). That is the published triple-class claim appearing in a log for the first time. Damage to kill: Cazic-Thule 94,941 at Adaptive, 316,488 at Fused, 382,035 at Refined; Innoruuk 333,054 and 345,385. <strong>Every Fear and Hate boss page on the wiki is a Project 1999 import</strong> written before this game existed, so until today nobody had measured any of it"),
    dict(kind="Addition", date="14 Aug 2026", title="Which boss drops which planar set",
         body="The gear tool ranks 116 planar pieces against your trio and could never say where a single one comes from. Now it can: <strong>86 pieces watched dropping, and every one of the eighteen sets names the mobs we saw drop it</strong>. Seven bosses gave up exactly one set each in our sample &mdash; Magi P`tasa drops Apothic, Master of Spite drops Rune Etched, Mistress of Scorn drops Imbrued Platemail, Coercer T`vala drops Insidious, Grandmaster R`tal and Innoruuk&rsquo;s Chosen drop Indicolite, and phoboplasm drops Midnight Clad. <strong>Counts from our own kills, never a rate.</strong> Two faults had been hiding all of it: the drop join only read the dungeon catalogue, which contains no planar piece at all, and it discarded any drop from a mob missing from a hand-written roster &mdash; so measured evidence could only ever confirm what we had already typed. Sightings went from 171 to 524"),
    dict(kind="Correction", date="14 Aug 2026", title="Two gods we never recorded, because we spelled them wrong",
         body="The raid parser has carried a list of boss names since it was written, and two entries on it were guesses: <em>Cazic Thule</em> and <em>Innoruuk</em>. The game writes <strong>Cazic-Thule</strong> with a hyphen and <strong>Innoruuk, the Prince of Hate</strong> in full, so neither ever matched a line. Both gods were killed repeatedly on 12 and 13 August and the file recorded nothing, because <strong>a boss whose name is wrong is indistinguishable from a boss nobody fought</strong>. Also fixed: two separate kills of the same boss at the same tier on one night were merged into a single fight with an invented range &mdash; Lord of Ire published as &ldquo;61,014 to 401,708, two clients 84.8% apart&rdquo; on an evening when only one character was logging at all"),
    dict(kind="Correction", date="11 Aug 2026", title="Those raid kills were never ours alone",
         body="We published Master Yael at five difficulties as <em>&ldquo;killed once at every difficulty by one trio in one session&rdquo;</em>. <strong>Every raid-boss fight in every log we hold is a public pick-up raid of five to seven players</strong>, and our own characters dealt <strong>13&ndash;44% of the damage</strong>. The damage totals are unaffected &mdash; damage to kill counts everyone, and the D4 figure re-checks to 242,060 exactly &mdash; but the sentence beside them was wrong in the direction that misleads hardest. Anyone reading &ldquo;one trio did this&rdquo; and taking a duo into The Hole at Refined would have been badly served. The parser now records how many attackers a fight had and what share was ours; <strong>the other players are counted and their names discarded</strong>, because nobody is named on this site outside the credits"),
    dict(kind="Correction", date="11 Aug 2026", title="A boss self-heal is not gated at D3",
         body="Beside the same table we said <strong>the kit widens at D3</strong> and <strong>he healed himself never at D0, D1 and D2</strong>. Both were read off one session and later kills contradict the second. <strong>The same boss healed itself at D2 on a separate kill</strong> &mdash; Superior Healing, 210 hit points &mdash; and <strong>Lady Vox heals itself at D0</strong>, in the open world. What difficulty raises is how much of the kit turns up, not whether a heal is in it. <strong>And &ldquo;ten times at D4&rdquo; was ten log lines, not ten decisions:</strong> one effect ticking every six seconds for the same 22 hit points. The same shape appears on Lady Vox at her top tier. Counting a recurring drain as ten separate heals overstated what the boss did"),
    dict(kind="Addition", date="11 Aug 2026", title="Lady Vox and Lord Nagafen, at four tiers and two",
         body="Seven more boss kills parsed: <strong>Lady Vox at Base, Awakened, Adaptive and Fused</strong>, and <strong>Lord Nagafen at Awakened and Adaptive</strong>. All public raids, all recorded as such. Damage to kill rises with the tier as it does for Master Yael, but <strong>one of these is a fifth of what it should be and is published as a floor rather than a total</strong>: our character reached the fight five minutes after the boss had already engaged, so the log simply never saw the opening. That is what a client log is &mdash; a record of what one character witnessed &mdash; and a figure from a fight you joined late is a lower bound and nothing more"),
    dict(kind="Addition", date="11 Aug 2026", title="Paste your inventory, and the site reads it back",
         body="<code>/outputfile inventory</code> writes a wall of tab-separated text &mdash; more than half of it empty sockets &mdash; and nobody reads it. <a href=\"tools/inventory.html\">The reader</a> turns it into a list of what you carry with everything we know attached: the item&rsquo;s page, its zone, its planar set, and where we have <strong>watched the thing drop ourselves</strong>, naming the mob and the count. <strong>Nothing is uploaded.</strong> The parse happens in the page; an inventory names your character and lists what you own, and that stays yours. It refuses to score your gear: the file carries names, IDs and counts and <strong>no stats at all</strong>, so any rating would be invented. An item we do not recognise is reported as a gap in our catalogue, not in your bags"),
    dict(kind="Correction", date="11 Aug 2026", title="Six item names, and four we could finally spell",
         body="The dump is the game&rsquo;s own record of an item name, which beats any reading of a wiki. Six were wrong here: <em>A Dark Cauldron</em>, <em>Djarns Amethyst Ring</em>, <em>An Elven Charm Necklace</em>, <em>An Executioners Axe</em>, <em>Skull-shaped Barbute</em> and <em>Slaver&rsquo;s Lash</em> are Dark Cauldron, Djarn&rsquo;s Amethyst Ring, Elven Charm Necklace, Executioner&rsquo;s Axe, Skull-Shaped Barbute and Slaver`s Lash. <strong>And four items that had no page now have one.</strong> Where a loot cell elides a shared prefix we refused to guess the full name, so <em>Fire</em>, <em>Water</em>, <em>Greaves</em> and <em>Sleeves</em> sat as fragments. They are <strong>Torn Page of Mastery Fire</strong>, <strong>Torn Page of Mastery Water</strong>, <strong>Mithril Greaves</strong> and <strong>Embroidered Black Sleeves</strong>. The caution earned itself twice over: the format has no colon, and &ldquo;Sleeves&rdquo; beside an Embroidered Black Cape is a different garment, not the cape. Earth and Wind stay unnamed &mdash; we know the format now, but applying it to them would be a pattern inference rather than a reading"),
    dict(kind="Correction", date="11 Aug 2026", title="We counted one player&rsquo;s loot against the whole group&rsquo;s kills",
         body="Published this morning: <em>Efreeti Lord Djarn dropped Golden Efreeti Boots on 9 of 11 kills</em>. The 11 is right and the 9 is not. <strong>A log records what its own character picked up</strong>, not what the corpse held &mdash; nine boots went to one player and two went to the other, from the same eleven kills. The figure is <strong>11 boots across 11 kills</strong>. The <em>data</em> was never wrong &mdash; the sightings join has always counted every log, and the item pages have said 11 all along. The mistake was in a sentence typed beside it, which is the same fault as every other one this register records: a figure re-derived by hand next to a figure printed from data"),
    dict(kind="Correction", date="11 Aug 2026", title="Difficulty is the lowest tier that drops, not the commonest",
         body="We read a session&rsquo;s difficulty from the <code>+N</code> most items arrived at. It is the <strong>lowest</strong> <code>+N</code>, and the difference is not academic. Across <strong>1,742 upgradeable drops</strong> in sessions where the zone line stated the tier independently, <strong>not one item dropped below it</strong> &mdash; difficulty is a floor, and about an eighth of drops roll above it. The floor identified the tier in 52 of 52 sessions; the commonest value got 50. It is a roll and not a property of the item: <em>Fine Steel Rapier</em> dropped +1 forty-three times, +2 eleven times and +3 once, all at Awakened. <strong>The practical gain is small samples</strong> &mdash; three drops settle it, where a commonest value needs an evening. One session of ours dropped four items, three rolled up, and the commonest value said Adaptive while the zone line said Awakened. A bare item with no suffix had to start counting as <code>+0</code> for any of this to work, or every open-world session read as Awakened. <strong>No difficulty already published changed</strong>"),
    dict(kind="Correction", date="11 Aug 2026", title="Two names on the Nagafen&rsquo;s Lair roster",
         body="<strong>Magi Rokyl is Magus Rokyl.</strong> Our log names him on both combat and loot lines, dropping the same Polished Mithril Mask the survey attributes to him, so a measured source corrects a read one. <strong>And we withdraw a merge made on 10 August.</strong> That day&rsquo;s note said we had &ldquo;merged one dragon spelled two ways&rdquo;: <em>Zordak Ragefire</em> and <em>Zordakalicus Ragefire</em>. They are not one entry spelled two ways. The survey gives them different levels, races, locations and behaviour &mdash; a level 60 non-aggressive human merchant, and a level 54 triggered lava dragon. One character in the Cleric epic, two things in the game. The merge pointed both rows at a single page, so whichever built last erased the other, and the merchant had no address for a day. He has one again. A shared surname is not a spelling variant"),
    dict(kind="Addition", date="11 Aug 2026", title="Sol B and The Hole, measured",
         body="Three sessions parsed from logs due to be deleted: <strong>Nagafen&rsquo;s Lair at Awakened</strong> (166 kills) and <strong>The Ruins of Old Paineel at Base and Awakened</strong> (94). Both surveys carried rosters and neither carried a measured section. <strong>Efreeti Lord Djarn produced 11 Golden Efreeti Boots across 11 kills</strong>, and his Amethyst Ring twice &mdash; counts, not rates. The multiclass-trash finding from Castle Mistmoore <strong>replicates in a second zone</strong>: <em>an imp protector</em> backstabbed 103 times while casting Dry Bone Fire Burst 379 times, plus heals and a charm. Nearly three times the Mistmoore sample. Its melee averages 45 and its backstab 175, max 405, which is why we never print one average for a mob that backstabs. <strong>At Base the same zone runs one kit per mob</strong>, not two &mdash; the capturer backstabs and never casts, the channeler heals and never backstabs. Class kits reach trash at Base; a mob carrying two of them remains an Awakened observation"),
    dict(kind="Addition", date="11 Aug 2026", title="A Learn hub, and search for everything else",
         body="Six Learn pages existed and the header&rsquo;s <em>Learn</em> link went to one of them, with the breadcrumb on every Learn page pointing back at that same article. There is a <a href=\"learn/index.html\">hub</a> now, driven by the same registry as the footer so the two cannot disagree. <strong>And the site is searchable.</strong> The only search covered items and named mobs &mdash; you could not find <em>Screaming Terror</em>, <em>voidling</em>, <em>mote</em> or <em>tier C</em> anywhere, including on the pages that explain them. <a href=\"search.html\">Search</a> covers the other 41 pages. The first build indexed 1,400 characters a page and still could not find Screaming Terror, which was the whole point; it indexes whole-page tokens now. Header and footer also lead with the same section for the first time"),
    dict(kind="Addition", date="11 Aug 2026", title="What we have actually watched drop",
         body="Every item page on this site &mdash; and on every competitor&rsquo;s &mdash; is a transcription of what a wiki says drops. Our parsed logs are the one thing nobody else has, and until now they lived at the bottom of one zone page and flowed nowhere. <strong>112 named-to-item sightings across 50 mobs and 89 items</strong> now print on both pages: &ldquo;seen 23&times;, 04 Aug 2026 D3&rdquo;. <strong>A count, never a rate</strong> &mdash; a drop seen once is seen once. Of 501 distinct items observed dropping, 121 match a survey loot table; the other 380 are vendor trash and +N gear lines, which fall off anything and are not a gap in the catalogue. Joining the two estates needed a canonical name key that strips the +N tier and the leading article, because the roster writes <em>A Fallen Noble</em> and a log writes <em>a fallen noble</em>"),
    dict(kind="Correction", date="11 Aug 2026", title="One respawn ceiling was printing bare",
         body="Four zones mark their respawn with <code>&le;</code> because the 28 July patch lowered the maximum without publishing a figure. Crushbone&rsquo;s own note said to treat 9:00 as a pre-patch ceiling and it printed bare. Marked. <strong>And a contradiction is now recorded rather than carried:</strong> our Blackburrow note says the zone is not in that patch list, the register says it is, and the two renderings of the note we have seen name six dungeons and eleven. We do not know which, so the page says so"),
    dict(kind="Correction", date="11 Aug 2026", title="The retraction reached the header and not the row",
         body="An outside audit found the defect this site is most prone to, in its worst form yet. The placeholder question was settled at tier 1 and every affected survey grew a header saying <em>no placeholders here</em> &mdash; while the roster three lines below still read <strong>&ldquo;Placeholder is an earth elemental&rdquo;</strong> in bold, present tense. The header is authored; the rows are generated; nothing connected them. <strong>18 claims across 5 surveys are now struck as historical by the renderer</strong>, reading <code>placeholders_removed</code>, which already existed in the data and which nothing had ever read. One analysis paragraph built on the retracted model &mdash; a camp called &ldquo;the most frustrating&rdquo; because of a 10% spawn off two placeholders &mdash; has been corrected too"),
    dict(kind="Correction", date="11 Aug 2026", title="Eight items were never items",
         body="A loot cell reading <em>Mithril Vambraces</em> then <em>Greaves</em> means two pieces sharing a prefix; one reading <em>Torn Page of Mastery</em> then <em>Earth &middot; Water &middot; Fire &middot; Wind</em> means one item with four variants. Our splitter treated both separators the same, so <strong>Earth, Fire, Water, Wind, Skin, Sleeves, Greaves and &ldquo;pg. 3&rdquo; each got a page, a canonical URL and a share card.</strong> They are suppressed now and printed on their parent instead. We have not reconstructed the full names: the row elides a prefix and guessing it would invent an item. Also merged one dragon spelled two ways, and split a slash-joined pair of guards"),
    dict(kind="Correction", date="11 Aug 2026", title="Metadata was the last place hand-typed facts lived",
         body="Body counts were made to print from data on 10 August. The <code>&lt;head&gt;</code> was not, so four pages still advertised <em>ten surveyed dungeons</em> to Discord and to search results &mdash; which is the only text most readers ever see. Descriptions now derive from the same registry as the body, and <strong>the gate reads the head</strong>. The tools page also printed seven trackers over a grid of six, because the count came from the registry and the cards were hand-written; the seventh card exists now"),
    dict(kind="Addition", date="11 Aug 2026", title="Motes: spells scale doubled, items scale flat",
         body="A mote is worth <strong>2<sup>rank&minus;1</sup></strong> to a spell and <strong>exactly its rank</strong> to an item, and that one difference decides every mote decision. It means <strong>converting motes upward destroys item XP</strong> &mdash; two rank 5s are 10 item XP and the rank 6 they become is 6. Convert for spells, never to feed an item. From an infographic supplied as a developer release; <strong>the artefact is branded by a creator</strong>, so it is published T3 until someone shows otherwise. Three of its four testable claims match patch notes we hold. The fourth does not: it shows ten mote ranks where the 21 June note says the conversion construct accepts ranks 1 to 8"),
    dict(kind="Correction", date="11 Aug 2026", title="Every raid figure was logged twice",
         body="A second client&rsquo;s log of the same seven fights arrived, so every number on the difficulty ramp is now a measured range rather than a point. Two parses of one kill disagree by however much each client was out of range to see &mdash; <strong>between nothing and 3.2% here, with two fights matching exactly</strong>. That spread is the method&rsquo;s error bar. It also corrected us: <strong>we published ten self-heals at D4 and the second log shows one</strong>. The pattern &mdash; no healing below D3, healing at and above it &mdash; is in both logs independently, so the finding stands and the count does not"),
    dict(kind="Addition", date="11 Aug 2026", title="The difficulty ramp, measured on one boss at all five tiers",
         body="Master Yael killed at D0, D1, D2, D3 and D4 in a single session by one trio, in the group instance of The Hole. <strong>The class kit widens at D3</strong> &mdash; direct damage and control up to D2, then healing, fear and damage over time from D3. He healed himself <strong>never at D0, D1 and D2, once at D3 and ten times at D4</strong>, which needs no inference about spell names: the log says <em>healed itself</em>. That is the largest gap this site has listed, and it lands exactly where the published claim said it would. Damage to kill ran 75,369 / 85,415 / 139,117 / 227,690 / 242,060 &mdash; <strong>an upper bound on hit points, not a measurement of them</strong>, because he heals"),
    dict(kind="Correction", date="11 Aug 2026", title="One sentence was on 446 pages",
         body="A site-wide sweep for repeated text found <strong>12,195 words of it</strong>, and almost all of it was boilerplate on the item and named-mob pages. One fifteen-word sourcing sentence appeared on all 446 item pages &mdash; 6,690 words of the same line, the largest single block of repeated text on the site &mdash; and two more ran to 2,400 between them. All three are now short lines that say the same thing, and the survey they point at was already linked directly above. <strong>9,386 words gone, not one fact with them.</strong> Repetition across three or more pages is down to 1,880 words, nearly all of it single lines that have to exist on each page"),
    dict(kind="Correction", date="11 Aug 2026", title="Accuracy said the same thing twice",
         body="The per-zone provenance section rendered a summary table <em>and</em> the ten prose blocks that table was built to replace, so four zones restated their own row in a paragraph underneath it. Those are gone and the rule they shared &mdash; infobox live, narrative prose imported &mdash; is stated once above the table. Eight blocks also carried survey markup pasted in, rendering a meaningless section number and putting an <code>h2</code> inside the zone&rsquo;s own <code>h3</code>. Both fixed. The rest of that section stays: it reads as repetitive but the ten blocks are only 8 to 30% alike, and the difference is the evidence"),
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
