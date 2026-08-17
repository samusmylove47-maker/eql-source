# Blind reader analysis — 17 August 2026

Six readers with no knowledge of the project, forbidden from reading CLAUDE.md,
docs/, HANDOFF.md or _build/. Each arrived with a different question.

## Verdict: **NOT PUBLISHABLE**

Not today — but it is days of work away, not months, and none of what stops it is coverage. Judged as a product it does three of four things well: the writing is unusually good, the sourcing method is better than anything else in this corner of the web, and check.py passes 722 pages green. What fails is the fourth: things on it are broken and, in four places, embarrassing in exactly the way that costs an accuracy site its argument. It publishes a superlative its own dataset refutes, on three pages and inside an Open Graph card that travels off-site. It headlines a trust score ("10 fully verified") that its own change log demoted on 14 August, while the live score sits in a hover tooltip no touch device can open. It ships 13 named-mob pages cut off mid-word, one of them mid-number, on a site whose first hard rule is never to publish a number it did not read. And one CSS line strips the Type and Date off all 69 change-log entries on phones — deleting, on the "Accuracy" page, the precise mechanism the home page promises. Any of these, found by a reader who came to check the site's rigour, undoes more trust than the rigour earns. Second reason, softer but real: the item corpus is the front door's headline credential ("Search 435 items") and roughly a quarter of those pages are a name and three blanks, while the fields that decide anything — no drop, lore, damage, delay — are dropped in the build and appear nowhere. That is a promise the product cannot meet. Fix the four defects and qualify the two overstated numbers and I would call it publishable with the coverage gaps openly stated, because the readers who trusted it trusted it for the right reasons.

## Headline

An answer layer. The site is filed by how it was built — surveys, sources, tiers — not by what readers arrive asking, so five of the six had to assemble their own answer by hand; and on the four questions the site does answer directly, it answers some of them more than one way.

## Ranked gaps

### 1. [MISSING — factual defect] The site contradicts itself on its own headline facts, and prints the contradictions bare

**BLOCKER** · hit 4 of 6 readers

**Why it matters:** This is the one failure mode the site exists to prevent, so it costs more here than it would anywhere else. Verified: data/zones.v1.json gives Kedge Keep ZEM 139 against The Hole, Splitpaw and Warrens at 128, yet thehole.html's H1, its meta description and its Open Graph card all say "highest zone experience modifier in the game", splitpaw.html says "joint highest", sources.html says the Warrens shares the top — and kedgekeep.html quietly says 139 is "the highest figure on this site". That is the single question a grind-zone reader arrives with, answered four ways, and the wrong version is baked into a share card that travels off-site. The same shape recurs: najena.html asserts a Journeyman's Boots quest that learn/still-true.html flatly denies exists, three days later, with a different date and a Tier C grade — while the survey note prints bare, which on this site means tier 2 or better. planeoffear.html and planeofhate.html both say "which class kits attach to which raid boss at D3 and above is unpublished by anyone, and it is the largest gap on this site" while sources.html#gaps says it is no longer the gap and learn/difficulty.html prints 100 parsed boss fights. reading-the-plans.html says the 28 July patch cleared placeholders from eleven dungeons; sources.html names six, five times, identically. plane-of-sky.html says eight islands in its meta description, nine in its hero and asks about a tenth. check.py passes all 722 pages, so none of this is caught.

**Smallest fix:** Derive every superlative from the dataset instead of typing it. One pass: replace the four "highest ZEM" sentences with a generated phrase from zones.v1.json (and regenerate The Hole's OG card, which is the copy that leaves the site). Then add a gate.py rule that fails the build when a superlative string appears in prose next to a field the data can rank — the propagation gate already exists for exactly this class of fault and simply has no rule for it. Separately, reconcile the four named contradictions by hand and put the boots note behind the still-true.html grade.

### 2. [MISSING] Item pages drop the fields that make an item decidable — no drop, lore, damage, delay, effect magnitude

**BLOCKER** · hit 3 of 6 readers

**Why it matters:** "Search 435 items" is the first of the three front doors and the credential the home page leads with, and item pages are the deep-link surface a search engine lands people on. Verified: "no drop" appears 59 times across dungeons/*.html and 0 times across all 442 item pages; grep for <dt>Damage or <dt>Delay across items/ returns 0, though 15 survey rows carry a damage/delay pair. The extractor is splitting the survey's "Slot / type" cell on the middle dot and keeping the first token, so the tradeability flag — the one fact that decides whether a guildmate can hand you the item — is not hedged or marked "not recorded", it is gone without trace. blued-two-handed-hammer.html tells you the slot is Primary and nothing about how hard it hits, so two weapons cannot be compared anywhere on this site. Journeyman's Boots, the item the flagship survey calls its headline, never states the run-speed percentage, duration or stacking — the only reason anyone wants them. Silent field loss is worse than a stated gap on a site that elsewhere prints "source not recorded" in red, because it teaches readers the absence means the fact does not exist.

**Smallest fix:** One change in _build/extract.py: keep the whole slot cell rather than the first dot-token, and carry damage, delay, weapon type and the flag words through to the item record. Then add the four fields to the item page template, printing "not recorded" where absent. Add a check.py assertion that the count of "no drop" strings in items/ is not zero while it is 59 in dungeons/ — the mismatch is what makes this silent.

### 3. [MISSING] No way to ask the site a question by level — no filter, no sort, no progression statement, no beginner door

**BLOCKER** · hit 3 of 6 readers

**Why it matters:** Level is the only currency a player has, and the site is priced in nothing else. Verified: dungeons/index.html contains one button and it is the mobile burger — thirteen cards in plate-number order, so "which of these takes a 12" is a manual sweep of thirteen bands. The Index tool filters by class, slot and zone; not level. raids/plane-of-sky.html and learn/raid-access.html mention a level exactly once each, and it is the level 11 class lock, so the entire endgame is unpriced. tools/character.html has a Level input that is serialised into the share URL and never read again — the one page that knows the reader's level declines to use it. And the flagship mechanic is nowhere on a page: the clearest explanation of the multiclass trio and the permanent level-11 primary lock lives inside a JavaScript template literal in the combo calculator, rendering only after the reader picks options. Learn's seven pages are all corrections to knowledge a new player does not have, opening with "Every EverQuest Legends player is a returning EverQuest player" — the site tells its newest reader they are the wrong reader on the first page they open.

**Smallest fix:** Two things, both small. Add a level input to dungeons/index.html that dims cards outside the band — the data is already in zones-index.json and the page is generated. Then promote the multiclass explanation already written inside combo-calculator.html into an eighth Learn page, "How classes work", and add it as a fourth door labelled "I just started". That is a copy-paste of existing prose plus one card.

### 4. [BURIED] Raids is a top-level section containing no raids, while the raid data sits under Learn

**BLOCKER** · hit 2 of 6 readers

**Why it matters:** The severity is entirely misfiling — the data is superb and unreachable. Verified: raids/index.html links exactly one content page, plane-of-sky.html, whose own text says "Sky is not a raid zone". It writes "The most expensive boss in the zone costs about a 15th of Cazic-Thule at Refined" and does not link Cazic-Thule. Meanwhile 100+ parsed boss fights including Cazic-Thule and Innoruuk at D2–D4 sit in learn/difficulty.html, a page about difficulty settings, in a 97-row table with no zone column, no attacker count and no sort — so the raider clicked Raids first, as anyone planning a raid would, and called it the least useful page on the site for the job. Compounding it: the table's "floor" rows make the hardest bosses look the cheapest (Ashenbone Broodmaster reads seven times cheaper at D4 than D3), and attacker counts — the number that decides whether six people can do it — are published for Sky bosses and withheld for everything else. Lady Vox exists on this site as four table rows and no page at all.

**Smallest fix:** Rebuild raids/index.html as a boss table generated from raids-measured.json: boss, zone, tiers measured, damage to kill, attacker count, link to its named page. The generator, the data and the named pages all already exist; this is a new build target reading committed JSON, not new research. Add an attacker column to the difficulty table and sort by zone rather than boss name.

### 5. [MISSING] Voidling locations — the contributor supplied every one and the site published one

**BLOCKER** · hit 1 of 6 readers

**Why it matters:** Only one reader hit it, but it stopped them completely and it is the cheapest fix on this list. learn/raid-access.html is titled "How raid access actually works", says raid instances are created by hailing a voidling, and never says where one stands. Verified: exactly one page on the site gives a location — planeofhate.html, "Oasis of Marr, top of the tower" — which the raider called the single most useful paragraph on the site. And credits.html thanks a contributor for "Every voidling location, and the confirmation that raid bosses live only in raid instances." The site is sitting on the answer, credits itself for having it, and publishes a tenth of it. Without it no raid instance can be entered, so every raid page downstream is unusable regardless of how good it is.

**Smallest fix:** Add the location column to the existing three-instance table on learn/raid-access.html and repeat each zone's voidling location in that zone's "Getting in" section. The data is in hand; this is typing.

### 6. [MISSING — defect] Mobile deletes information rather than reflowing it, on the two tables that carry the site's promise

**MAJOR** · hit 1 of 6 readers

**Why it matters:** Desktop is the stated primary target and that is a legitimate call, but this is not a layout compromise — it is silent data loss, and it lands on the exact promise the home page makes. Verified: assets/site.css:292, @media(max-width:900px){.zrow .cell:nth-of-type(n+2),.zrow .zonesub{display:none}}. sources.html carries 138 .cell spans across 69 change-log entries; on a phone every Type and every Date disappears, on the page whose whole job is that "a correction never reads as new content" and that "every claim names the date its source was read". The same rule strips Entry, Charges and Raid-boss from the three-instance table on learn/raid-access.html — a page whose lede is "getting that wrong costs you a charge and an evening", with the charge figure in a hidden cell that appears in no other file on the site. The home page's own "What changed" block uses different markup and displays correctly, so the full log is worse than its summary. A reader who checks the site on a phone concludes nobody has read it on one.

**Smallest fix:** Change the rule to restack rather than hide: at ≤900px make .zrow a two-row grid and let the cells wrap under the title, keeping the <em> labels that are already in the markup. One media query, no template change.

### 7. [BURIED] The site's live quality score is hover-only, undefined, and contradicted by the retired one on the front page

**MAJOR** · hit 3 of 6 readers

**Why it matters:** This is the site's most decision-useful number and its most misleading one at the same time. index.html:52 headlines "10 fully verified" and dungeons/index.html:52 repeats it — a grade the site's own change log demoted on 14 August to "sourcing hygiene", noting that four of those ten zones score 4/10 on the metric that replaced it "because nobody has played them with logging on". The live score renders as a bare "4/10" whose entire meaning lives in a title attribute: "bosses: 17 named on the roster, none fought by us; loot: 65 items listed, none seen by us; difficulty: never played at a recorded difficulty". Three separate readers independently identified that string as the most useful text on the page, and it is invisible to touch, to keyboard, and to anyone who does not rest a cursor on a small grey fraction. Nothing anywhere says what /10 means. So Najena shows a green "all gates cleared" dot beside a silent 4/10, and the loudest trust signal on the site is one it privately withdrew.

**Smallest fix:** Replace the hero count with the live metric ("3 zones measured in play, 10 sourced only") and print the coverage breakdown as visible text under each card instead of a title attribute — five short labels per card, all already generated by coverage.py. Add one line defining the score on dungeons/index.html.

### 8. [MISSING — defect] Truncated text ships on 15 pages, including two headline bosses and two provenance blocks

**MAJOR** · hit 3 of 6 readers

**Why it matters:** Small, cheap, and disproportionately damaging because of where it lands. Verified: 13 named-mob pages cut their Notes mid-word at roughly 194 characters. named/cazic-thule.html ends "2 attacks a round, 223–603 a hit. Zone-wide social agg" — a figure severed from its context on a site whose first hard rule is never to publish a number it did not read. named/drelzna.html opens with a bare "20%" that has no label, points the reader to "the note under this table" on a page that has no such note, and closes an unopened bracket at "alway". Separately, two of the ten "Sources & confidence" blocks on sources.html — Crushbone and Blackburrow — end at "Compiled from the EverQuest Legends community wiki (eqlwiki.", unclosed bracket and all, on the page that is the site's proof of rigour. There is also one empty <span class="tag warn"></span> in najena.html's chase-item table that paints a small blank red rectangle where every sibling row prints a rarity, and it is on the item that page calls its headline. Every reader who found one of these went looking for what else had been silently dropped.

**Smallest fix:** Remove the 194-character truncation in build17.py and let the note run, or cut on a sentence boundary with a link to the survey. Find the two sources.html blocks' lost sentences in _build/source/ and restore them. Add a check.py rule that fails on any rendered field ending mid-word or on an unclosed bracket — cheap, and it would have caught all 15.

### 9. [BURIED] Search reaches 44 of about 722 pages, and neither of the two search boxes says so

**MAJOR** · hit 3 of 6 readers

**Why it matters:** Verified: window.__S__ holds 44 records — 19 dungeons, 9 tools, 8 learn, 3 root, 2 raids, 1 each archive/data/sets — and zero beginning items/ or named/. So searching "Journeyman's Boots" in the box labelled Search never returns items/journeymans-boots.html, and searching a damage figure returns nothing because difficulty.html is indexed as its intro. Roughly 675 pages are unfindable by the site's own search and reachable only through a separate nav item with a different name. The scoring is also an unstemmed AND across terms, so a beginner's phrasing falls into the empty state: "leveling" returns 0 because the site only writes "levelling", "starting city" returns 0. Two nav items called Search and The Index, each covering what the other does not, with nothing telling anyone which is which.

**Smallest fix:** Either merge the two indexes — the item and named records already exist in index-data.json, so it is a concatenation in the search generator — or, minimum viable, put one line under the Search box saying it covers guides and explainers and linking The Index for items and mobs. Add a handful of spelling aliases (leveling/levelling, armor/armour) to the tokeniser.

### 10. [MISSING] No expansion of the abbreviations the site prints on every card and header

**MAJOR** · hit 3 of 6 readers

**Why it matters:** Verified: "zone experience modifier" appears in exactly two files, dungeons/thehole.html and search.html, neither on any skim path. "ZEM 119" is printed thirteen times on the home page as the headline stat of every zone card, with no unit, no direction and no scale — one reader spent a full minute comparing 119 against 139 without ever confirming higher was better, and another worked out that percent = ZEM ÷ 75 by opening six zone pages one at a time. The legible percentage form exists only inside individual surveys. Same silence for "Succor −644, 158" on every zone header and the "/who name crushbone" line under every title. This is a small fix that three of six readers hit, because the abbreviations sit on the most-viewed surface on the site.

**Smallest fix:** Print the percentage beside the raw ZEM on the cards, as the surveys already do, and wrap the three abbreviations in <abbr title>. Optionally one short glossary in Learn. All three live in generated templates, so it is one edit each.

### 11. [MISSING] Nobody says who runs the site, and there is no site-wide 'as of' date

**MAJOR** · hit 2 of 6 readers

**Why it matters:** The site's entire argument is that a claim is worth what its named source is worth, and it does not apply that to itself. credits.html names eight contributors and no operator; there is no About page; the change log refers to "the site's owner" in the third person. The sceptic — the reader most inclined to recommend it — could not do the thing they normally do before recommending a wiki to a guild. Compounding it, for a site whose pitch is being current against a stale wiki, the home page carries no build date at all, and the newest change-log entry is dated 17 August when today is 16 August. Dating the site meant reading 69 entries and the first date found was in the future.

**Smallest fix:** One line in the footer template — a maintainer name or handle, plus a build date generated by stamp.py, which already fingerprints the build. Fix the future-dated entry.

### 12. [MISSING] No statement of what three multiclass characters can actually handle, while classic group-size advice still prints

**MAJOR** · hit 2 of 6 readers

**Why it matters:** The site dismantles inherited group-size advice and puts nothing in its place. sources.html says of Nagafen's Lair "treat every group-size claim on this page as a P99 artefact, not a requirement", while najena.html still prints "Full group or leave it" and splitpaw.html "Almost nothing is solo. Bring a group from the entrance." Because the site's own framing removes the reader's classic intuition — three classes per character, raids capped at 8 — a reader cannot fall back on anything. And measured danger exists for exactly one zone out of thirteen (mistmoore.html's "fights broken off"), where the page immediately says the deaths may record a client crash rather than the fight. So the honest answer is that danger is unmeasured, which is fine, but the pages print the classic answer instead of saying so.

**Smallest fix:** Either badge the inherited group-size sentences where they appear, or replace each with the measured line the site can support — "no trio has played this zone with logging on" — which coverage.py already computes per zone.

### 13. [BURIED] The item graph is one-directional and every item page prints a floor plan that locates nothing

**MINOR** · hit 2 of 6 readers

**Why it matters:** Verified: all 442 ../named/ hrefs in items/ point at the index — not one item links the mob that drops it, though all 234 named pages link back to their items, and named/drelzna.html is exactly the page the item page should be sending readers to. Separately, 441 item pages ship the .loc-mark CSS with the comment "The mark is the point of the whole thing" and 0 use it, so each renders an unannotated whole-zone plan captioned with the zone name — telling the reader nothing the line above it did not. On a site whose stated rule is that a drawing is an assertion, that is a drawing asserting nothing, 441 times. Cheap to fix and it converts the weakest generated page into the second-strongest.

**Smallest fix:** In build17.py, link the drop-source name to its named-page slug — extract.py already assigns both slugs precisely so the two cannot disagree — and reuse the named page's loc-mark span when the source mob has a recorded /loc.

### 14. [MISSING] Raid boss loot for the Plane of Fear and Plane of Hate bosses

**MINOR** · hit 1 of 6 readers

**Why it matters:** Listed low deliberately, because this is coverage rather than a defect and the site handles it honestly — named/cazic-thule.html says "No drops recorded — a gap, not an empty mob." But it is the reason anyone books an evening for a boss, the site has killed Cazic-Thule at three tiers, and zero items name him, Innoruuk, Maestro of Rancor, Fright, Terror, Dread, the dracoliche or Lady Vox. Worth flagging because HANDOFF.md already identifies the mechanism: sightings.py discards every measured drop whose item is not in the catalogue mined from the surveys, which threw away all 148 Plane of Sky loot lines. So some of this loot may already be in the logs and losing silently rather than being genuinely unobserved.

**Smallest fix:** Finish the sightings.py migration already sitting at P0 in docs/BACKLOG.md, then check whether Fear and Hate drops reappear before treating this as a play gap. Run scripts/toolrender.js before and after, as the backlog requires.

### 15. [MISSING] The front page promises a badge convention that 7 of 13 surveys do not follow

**MINOR** · hit 1 of 6 readers

**Why it matters:** Ranked low and framed narrowly, because the ungraded plates are a deliberate project decision, not a defect. The problem is only that the home page does not say so. index.html states "Tiers 1 and 2 print plain; anything weaker carries its badge wherever it appears — T3 T4 T5", and verified badge counts are: najena 5, lowerguk 4, kedgekeep 4, nagafenslair 1, planeoffear 6, planeofhate 5, and zero in splitpaw, crushbone, befallen, blackburrow, thehole, warrens, mistmoore. The site's own coverage data agrees, reading "0 inherited claims badged" for those seven, and sources.html says of The Hole that its narrative sections are classic EverQuest text. So a reader told they can scan a page for weak claims cannot, and finds out by comparing pages. The inconsistency — six surveys badged, seven not — is what makes the promise read as broken rather than pending.

**Smallest fix:** Qualify the sentence on index.html to say badging is complete on the surveys that carry it and name the phase that finishes the rest, or link the coverage field that already reports it per zone. One sentence; no badges added.

## What worked

- The sourcing method is genuinely novel and it survived a hostile read. sources.html gives per-zone revision ids, editor names and read dates, then a prose block per zone explaining what would not fit in a cell. The sceptic said they had never seen a fan wiki do this, and every count they spot-checked reconciled.
- The site retracts its own best work in public. The change log withdrawing the Eye of Veeshan 3D guide — "a 3D model is an assertion with production values, and we built one on top of a sentence from 1999" — bought more trust from the sceptic than any green tick would have.
- Provenance is computed per claim, not per page. tools/plane-of-sky.html derives "verified" and publicly refuses to let Warrior qualify, naming the reason. That is the correct failure mode and it is shipped.
- learn/still-true.html was named the best page on the site by two independent readers. Classic claim, Legends claim, tiered evidence with read dates, and a literal "What would settle it" line.
- Gaps are named rather than smoothed. planeoffear.html refusing to print a plat-per-hour figure until one is measured, kedgekeep.html's "We are not going to fill those in for them", Kedge's card admitting "Nothing here is ours yet" — readers trusted the printed numbers more because of the withheld ones.
- The measured combat-log output is the best raw material on the site and has no equivalent elsewhere: Master Yael's 74,915→242,060 damage ramp across five tiers with fight length and spell names, the stun tables that read as a kill order, and the published method error bar (two clients parsing one kill differ by up to 3.2%).
- Individual surveys hit the target when they try. Splitpaw's Dangers section ("If you hear chains rattling, turn and run", then calibrating with "Beyond that, Splitpaw is a fair zone"), Lower Guk's clan ladder, Crushbone's per-level camp table, and Najena's "01 Why you come here" opener were each singled out unprompted.
- Named-mob pages are the strongest generated template: level, race, class, /loc plotted as a real marker on a mesh-derived floor plan, and every drop linked with a sighting count and the tier it dropped at.
- Item pages are the best mobile experience on the site — 10KB, question answered in eight lines, 442 of them the same shape.
- The home page skims well: 824 words, three doors phrased as reader intents, and a hook two readers retained verbatim (classic EverQuest text "in a Legends-shaped hole").
- learn/contamination.html points the scanner only at eqlsource, and says why: "A scanner that only finds someone else's rot is an attack ad."