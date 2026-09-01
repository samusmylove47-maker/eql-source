# The owner capture census — 1 September 2026

**Produced by a five-agent survey of Director, eql-source, EQL50ups, EQLSLockouts
and sky-ledger.** All five agents verified their own tooling with a probe before
analysing and all five reported working tools; every item carries a file:line
from the repository that recorded it.

**Session C's repo was NOT surveyed** and is the known gap in coverage.

**40 reported items dedupe to 28 distinct captures.** Trips 0 to 3 total about 75
minutes and clear 15 of the 28, including four of the five highest-value.

*Read section 8 before asking the owner for anything: it lists five defects in
the records that would send them to the wrong capture.*

---

## Coverage

**Five of five agents had working tools.** Every one verified its tooling with an explicit probe before analysing, and none reported a failure that could masquerade as an empty result. One qualification: the Director agent's first Bash call (a compound `cd && rm -rf && git clone`) was denied by the permission system; it retried as a single `git clone` and every subsequent call worked. That is a retry, not a gap.

So the list below covers the five surveyed repos in full: **Director, eql-source, EQL50ups, EQLSLockouts, sky-ledger.** Two things it does *not* cover, stated so the list is not read as exhaustive:

- **Session C's repo, if it is one.** sky-ledger's single-digit-day item names a cheaper partial route through "Session C's corpus" (HANDOFF.md:50.2). C was not in the survey set.
- **Director's own two blind spots** — it could not read EQL50ups' `CAPTURE-REQUESTS.md` §2 or E's definition of item `35.5`. This survey resolves both by cross-reference (see #4 and #5), so Director's items 3 and 4 are no longer under-specified.

I verified three things directly rather than taking them on report: today's date and weekday, and the contents of `CAPTURE-REQUESTS.md` in the clone at `/tmp/claude-0/-home-user-eql-source/62da951e-34c6-5377-8786-8bc68b47bbca/scratchpad/bpeek/research/validation/CAPTURE-REQUESTS.md`.

---

## The headline

**40 reported items dedupe to 28 distinct captures.** The count flatters the problem. The real shape:

- **Five captures carry most of the value**, and four of the five are item/stat windows taken standing still, with nothing to farm and no zone to travel to. They fit in one 45-minute login.
- **Eleven of the 28 cost under five minutes.**
- **Two expire.** One is calendar-locked to a Tuesday and **today, 1 September 2026, is a Tuesday** (verified: `date` returns `Tue Sep 1 01:07 UTC 2026`). The other needs a log written on a day 1–9 of a month, and today opens a nine-day window that then shuts until 1 October.
- Only six captures require a raid, a trip, or other players.

Deduplication removed 12 duplicate asks. The heaviest overlaps: **dual wield wanted by three repos, haste by four, the level-gate question by two under two different protocols, the "weapon with base damage 1–9" window by two under two different names** (Director calls it `35.5`; sky-ledger calls it the upgrade floor — same single screenshot).

---

## 1. The five that matter

**#1 — The haste bench.** 15–20 min; **the first two readings are 5 min and already decisive for three of the four repos.**
*Wanted by: eql-source, Director, EQL50ups, sky-ledger (adjacent).*
Capture: the item window of each hasted item showing its haste line, then four Attack Speed readings from the Stats window with the state and **the character's level** noted beside each — (a) nothing hasted at all, (b) one hasted item, (c) a second hasted item with a different figure, (d) a haste song or spell running with both worn. Stop and report at whichever step stops moving the number; a number that stops moving *is* the finding.
Unblocks: eql-source's open finding at `_build/build13.py:65-88` and the six Sky reward tooltips carrying percentage haste — five of them the identical +41%, a copied constant rather than five readings — cleared or condemned as classic imports in one shot. Director's audit finding F-05 (whether haste is a capped current/maximum value rather than a divisor on weapon delay), which the record says the patch-note fetch explicitly does *not* close. EQL50ups' `HASTE_PROVENANCE` (step b), `HASTE_STACKING` (step c) and the haste cap (step d): 23 catalogue items carry haste, a haste belt at +10 is the largest single EP any item can earn under Melee DPS — larger than the best weapon in the game — and all 23 are currently ranked as though their full figure lands. Attack Speed is the only capped stat on the panel printing a bare number with no denominator. sky-ledger's Berserker Stance reading (stance off, then on, at cap) rides along in the same window.

**#2 — Six Shadow Rage item windows.** 5 min. Nothing to farm.
*Wanted by: Director (R82), EQL50ups.*
Capture: the full item window of each Shadow Rage piece — the Helm (id 55601) is on the owner's head; Gloves 55605, Sleeves 55603, Wristguard 55604 and Boots 55607 are in bank slot 15 per the existing inventory export. Full window, not the inventory line.
Unblocks: **R82 — does Legends gate equipping by level at all.** A `Required Level` line on a *wearable* row settles it yes; the only Tier M sighting anywhere in the project is on a click effect, not on wearing. And six items the player demonstrably wears are currently refused by `rankSlotItems`, never placed by Auto-fill even into a slot with no other candidate, printed with `—` in the item browser's EP column, and skipped by the importer — they ship `statsUnknown: true` with no stats, weight, size, flags or icon. It is the only Tier 0 evidence the project holds for a class whose planar armour the wiki never recorded.

**#3 — One below-level equip attempt.** 10 min if a low-level character exists; 15 if one must be made.
*Wanted by: EQL50ups (`levelCheck`), Director (R82's decisive form).*
Capture: on a character below the required level, try to equip one of the three catalogue records carrying `rl` — Baton of the Sky (49), Azarack Skin Wristwraps (46), Refugee Shroud (15) — and screenshot whatever the client does. **If it goes on, note all three of the trio's class levels**, because that distinguishes gating on the highest qualifying class from gating on the lowest.
Unblocks: R82 in the direction #2 cannot (an absent line is not proof of an absent rule). `levelCheck` sits inside `canUse`, which gates every ranking, auto-fill, the item browser and the planar sets; it costs 3 of 3,663 records today and is dormant, and the record's own point is that a patch populating `rl` turns a dormant unsourced choice into a wrong answer on every list at once with no code change to notice. Director R71 ruled it stays on "highest" and documented — this is what would let it be *settled* rather than ruled. If the item goes on, the three class levels also bear directly on R55/R65/R71.

**#4 — The dual-wield secondary test.** 15 min including making the character.
*Wanted by: Director, EQL50ups §2, sky-ledger. Three repos, and the widest single-question spread in the survey.*
Capture: a character whose classes are all non-dual-wield under the classic table — a brand-new level-1 character with two caster classes is the cheapest and needs no levelling. Equip a main hand, then try to place a weapon listing `Secondary` into Secondary. Screenshot the class line, the item's slot line, and the outcome. If it goes in, check the log for offhand swings after a zone or relog. **If the test could not be assembled at all, say that in those words** — "I could not equip it" and "the game refused it" are the same English sentence and opposite findings.
Unblocks: EQL50ups' `DUAL_WIELD_STANDING` (Tier 5), which today shows every offhand weapon to every trio; sky-ledger's `model4.py:50`, which applies the class set as a **hard gate its own audit says not to use**, so every ranking in E moves either way; Director's own item. There is no outcome that leaves the project where it started: a refusal licenses a gate B currently declines to build, an allow retires a rule everyone carries over from 1999.

**#5 — One item window of a weapon with base damage 1–9, at tier ≥1.** 3 min.
*Wanted by: sky-ledger (the ungraded floor), Director (its item 3, "35.5"). **These are the same capture** — Director could not read E's item list and so could not say so.*
Capture: the client item window of any such weapon. Worked example: `Efreeti Standard`, base 3 — at +1 the percentage rule says 3 and the floor rule says 4; at +5, 4 against 8. A +5 or better is easiest to read.
Unblocks: the +1-per-tier floor against the +10%/tier percentage term — stated as worth **62% of the weapon catalogue**, with damage swings up to 5.50× on affected rows. Retires the acknowledged "choice, not a finding" at `model4.py:82`, regrades the term in SOURCING.md from UNGRADED, and closes a term ungraded in *both* E's repo and B's. It is also the project's only measurement of what one owner capture costs (~16 h round trip), which is one of the three measurements behind R30's decision to decline the Concordance.

---

## 2. Time-locked — today, or wait

**#6 — Tuesday Voidling pair.** 5 min + 5 min. *EQLSLockouts.*
Hail a Voidling **before 10:00 Eastern (14:00 UTC)** and again **after 12:00 Eastern (16:00 UTC)**, saying `danger` each time, writing the wall clock beside each — on a day the weekly has not already been taken, or the capture reads REFUSED for the wrong reason.
Unblocks: halves the measured 26.06-hour reset bracket per pair and upgrades `RESET_RULE` from `provenance: 'stated'` to measured — the weekday itself has never been observed (`lockoutCore.js:900`: *"NOT 'measured'. We did not observe this."*). One Tuesday done properly already beats every published source.
**Today is Tuesday 1 September 2026.** Missing it costs a week; the next windows are 8, 15 and 22 September.

**#7 — Any log written on a day 1–9.** 0 min — just have logging on. *sky-ledger.*
Unblocks: whether the client space-pads a single-digit day (`Sun Sep  1`). The corpus is 4 logs and 189,460 lines with **zero single-digit days**, so it cannot answer it; the `[ \d]\d` widening has shipped, is provably inert on the current corpus, and stays marked unverified in both engines until one such log exists. The stake is whether both engines were silently discarding every line on a third of the calendar before any parse.
This rides free on #6 and on any login between now and 9 September. After that: 1–9 October.

---

## 3. Cheap, unlocked, do them at the bench

**#8 — Wall clock on the alt+Z screenshots already sent.** 2 min at a desk; 10 min for the fresh version. *EQLSLockouts (its own #1, "the one that unblocks the grid"), Director.*
The screenshots exist; only the moment they were taken is missing. **Director's amendment must be carried into the ask**: a fresh alt+Z reading with a **positive control** — a boss not killed this week shown beside one that was, in the same window — plus a second character or a second week. The earlier bare wall-clock request was measured against the wrong object (the six-day instance lockout), which is why the control is now part of it.
Unblocks: the reset hour, which is `hour: null // not recorded` at `lockoutCore.js:899`. It is a one-constant edit, and `test/grid.test.js:1365` already proves the `conditional` cell state collapses to `0` the moment the hour is known — **every boundary-day `unsure` cell in the tracker, for every user, permanently.** The record notes this has been "one sentence away for nine days" with a 1 September deadline, which is today.

**#9 — alt+Z within one minute of entering a fresh instance.** 3 min, free on any raid night. *EQLSLockouts.* Fixes R and therefore B with no assumption: `B − R` is exactly 5d23h, and the absolute period is undetermined among 6d / 6d0h30m / 6d1h / 6d2h — the difference between "available Monday evening" and "available Monday night".

**#10 — `/say café — naïve "quotes" résumé` with logging on.** 1 min. *EQLSLockouts.* Settles the decoder permanently: bytes `C3 A9` for the é means UTF-8, `E9` alone means Windows-1252. Cannot be settled from the corpus, whose only non-ASCII content is U+FFFD — the residue of a decode that already threw the byte away. Also makes the multi-byte read-boundary hazard testable for the first time.

**#11 — Two Equipment-tab captures with different gear worn.** 5 min. *EQL50ups.* What the third figure in `AC 20/350 | 110` is, and whether it responds to worn AC. One capture cannot distinguish a constant from a function. Would put a third client constant on Tier M as `Strength 70/510` and `SV Magic 25/1000` already did for `ATTRIBUTE_CAP` and `RESIST_CAP`.

**#12 — One item window showing the flag line, on an item whose wiki page uses the modern Title Case convention.** 3 min. *EQL50ups.* `meta.dataReliability.flags.doNotUseAsAuthoritativeFilter` is `true`, so the app refuses to offer a "No Trade only" filter a player could trust. Collapsing `NO_DROP`/`NO_TRADE` would rewrite 3,355 items on a two-item client sample; the same screenshot bears on the unresolved `MAGIC` and `Placeable` findings.

**#13 — One two-hander tooltip, delay above 50, showing its damage-bonus field.** 5 min. *sky-ledger.* Two open questions on one screenshot: whether the bonus applies above 50 delay, and whether the `max(Level, Damage)` branch is real — the record states the 50-delay cap and the observation cannot both be true unless that weapon's DMG exceeds the character's level. 124 two-handers in the corpus. Take a 1H `Dmg Bon` reading at known level and DMG while you are there; it closes a 3.75% spread on that term.

**#14 — Heirloom Ring worn-effect test on an all-class character.** 10 min. *Director.* We hold one screenshot, not a test. Releases the strongest first-hand item finding the site holds — a ring that lowers two resistances to raise regeneration on an all-class finger slot — which currently may not be published with *or* without the "No eligible class" restriction stated.

**#15 — Call of Flame spell-description window on a level-49 Ranger, plus one measured cast time under the named stance.** 10 min if such a Ranger exists. *sky-ledger, recorded as one of its two hard BLOCKs.* Converts the entire non-gear (quested spell) ranking axis from Tier 5 classic import to Tier M. The wiki page is a P99 `{{Classic Era}}` import whose figures match the recalled ones to the digit, so it cannot corroborate itself.

---

## 4. Rides free on a raid you were running anyway

**#16 — Plane of Hate instrumentation.** ~5 min of extra actions. *eql-source + EQLSLockouts.* A `/who` from the upper level (what `hateplaneb` is — a second, much larger archive, open in the zone's `verify_gate` and as a comment at `_build/geometry.py:52`); **record the exact zone-line shape on entry**, `Zone N (Label)` against `Zone - Group N (Label)` (the whole archive has every roster-boss kill in the `- Group` shape and none bare, so the shared-lock question is unanswerable from disk, and it decides which instance the grid's 25 cells describe); loot Ashenbone Broodmaster, Lord of Ire and Lord of Loathing, whose set columns read "not recorded".

**#17 — Make an instance at D2 or higher on a day that boss's weekly is not yet taken.** 5 min. *EQLSLockouts.* Breaks a perfect confound: every observed refusal happened *after* the weekly was already taken, so "difficulty too high" and "already locked out" are indistinguishable in the corpus. If the task is not granted, every weekly count we hold is measuring something else.

**#18 — alt+Z after a partial clear of Nagafen's Lair or The Permafrost Caverns.** Needs the run, ~45–60 min. *EQLSLockouts.* Whether several bosses in one zone share one lock or hold separate locks that merely started together — the current window is consistent with both. Releases the `alsoDies` decision, which can only fail dangerously: a group that kills King Tranix then wipes on Nagafen would be told the raid is done.

**#19 — Enter a Solo instance with logging on.** 10 min. *EQLSLockouts.* `" - Solo"` returns 0 across all 16 log files — no entry line, no invite line — while the alt+Z window shows a `Solo 3` lock, so the shape is real and the logs have simply never seen one. Bare `- Solo` currently keeps `difficulty: null` and degrades those cells to `unknown`.

**#20 — A FearHateRevamp sighting outside the Shadow Rage set.** Opportunistic, 0 dedicated minutes — a Legionnaire Scale or Greenmist piece on a vendor, a corpse or another player counts. *EQL50ups.* 53 items are quarantined out of the payload entirely, with `verify.mjs` failing the build if one reaches it. Either they are withheld for no reason, or the quarantine is correct and can be *stated* rather than assumed.

**#21–#23 — bard measurements, if a bard is present.** *sky-ledger.* Buff-bar screenshots during a 3,177 DDD run and a 2,659 run (20 min) — every single-valued DDD figure is currently a figure for one of two unnamed states, **including the 2,659 the entire Amplification measurement of ×1.6797 rests on**. One DDD cast into 12+ distinctly-named mobs (15 min) — the AE lane models bard AE with no measured target ceiling. One logged fight with the stance known from a screenshot rather than inferred (20 min) — `STANCE_EVEN_SHARE_OFFENSIVE = 0.93` against a careful re-read giving 99.3%, and E will not retune it from its own inference because that is indistinguishable from tuning to force a result.

---

## 5. Real trips

**#24 — The Sky circuit.** 60–90 min. *eql-source; three of its eight items plus the tenth-island question.*
Attempt to make the Plane of Sky at D1 — **a client that will not offer a tier is itself the answer, and must be reported as such**. Then one `/loc` standing on each island of the ring, taking **every island reachable, including any Efreeti island**. Then kill and loot the Thunder Spirit Princess on island 1.
Unblocks: labels the Sky side elevation permanently — 21 measured bodies of walkable floor, none identified, the geometry gap half-open since 11 Aug; the seventh of seven ring keys (`Key of Swords` is the only one missing from `sky-loot.json`) and the last ring boss with no measurement of any kind; and whether difficulty touches a raid zone at all — all ~78 Sky fights in the corpus are D0.

**#25 — The Kedge Keep circuit.** 45–60 min. *eql-source.*
`/con` and `/loc` on the thirteen named other than Phinigel Autropos, and one log of a slashing or blunt weapon landing normal damage while submerged — ideally against a mob type also fought on land, so averages compare.
Unblocks: 13 of 14 named carry `lv='?'` and `loc='not recorded'`; Kedge is one of three zones at `verify_level: "none"` and the `/loc` half closes Gate 3 for it; and it promotes Annalise's (AnnaWulf) 9 Aug first-hand underwater report to tier M — one of the two findings `docs/FINISH.md` calls "one session of play away from settled".

**#26 — Paragon of Spirit stacking.** 15 min plus a bard and an enchanter, the most expensive dependency in the survey. *eql-source.* Cast Paragon, then Cantata of Replenishment and Clarity on the same target; a buff bar showing all three settles it outright. Nobody has published an answer for Legends — no eqlwiki page (404), and the Buff Lines page never mentions it. The other of `FINISH.md`'s two "one session away" findings.

---

## 6. Desk work — owner-only, but no client

**#27 — Read the Producer's Letter of 8 July 2026.** 10 min. *Director; settles a live disagreement in eql-source.* Nobody has read it. If it or any T1 source states which class's level the active trio uses, it settles R55/R65/R71 in one read and either earns or splits the live T1 badge at `public/learn/still-true.html:222`, which currently spans three claims on evidence for one. It also adjudicates `CLAUDE.md:122-124` ("lowest") against B's test-pinned `levelCheck` ("highest").

**#28 — Does the 23 June 2026 revamp note exist?** 5–10 min, or one sentence of memory. *Director, eql-source F-06.* A screenshot, an archive link, or the owner's own recollection of reading it. A session already probed and found the archive's oldest note is 7 July 2026 (Beta), and Director's session is egress-blocked from that host. It is Najena's re-citation target after 28 July was found to name only six dungeons, and it is the **only** source the site's prose credits for the Najena 130→119 and Warrens 150→128 ZEM movements. Until settled, it may not be cited at all.

---

## 7. Batching order

**Trip 0 — desk, 15 min, do before anything else.** #8 (wall clock on the screenshots already sent), #27, #28. No client needed, and #8 is the highest-value item in the survey per minute spent.

**Trip 1 — today, Tuesday 1 September, and it expires.** Log in with logging on: #6 before 14:00 UTC, #10 (one minute), then #6's second hail after 16:00 UTC. #7 is free the moment the log is written. If an instance gets made, #9 and #17 come free with it.

**Trip 2 — the item bench. One login, no travel, ~45 min, and it is the single highest-yield trip in the list: four repos and roughly twelve questions.** Everything here is an item or stat window taken standing still. Order: #2 (Shadow Rage ×6) → #1 steps a–b (decisive alone) → #5 (base-damage 1–9 weapon) → #13 (two-hander >50 delay, plus the 1H `Dmg Bon`) → #11 (AC pair) → #12 (flag line) → #1 steps c–d (needs a second hasted item and a haste song) → #14 (Heirloom Ring) → #15 (Call of Flame, if the Ranger exists).

**Trip 3 — 15 min, append to trip 2.** #4: make a level-1 two-caster character, buy a vendor weapon listing Secondary, try it.

**Trip 4 — the next raid night, near-zero extra time.** #16 (Hate: `/who`, zone-line shape, three miniboss corpses), #9 and #17 if trip 1 did not catch them, #20 (keep eyes open), #21–#23 if a bard is in the group. #18 if the raid is Nagafen or Permafrost.

**Trip 5 — Sky, 60–90 min.** #24 as one circuit; run it at D1 if the client allows, because the same lap then answers all three questions.

**Trip 6 — Kedge Keep, 45–60 min.** #25.

**Trip 7 — whenever a bard and an enchanter are both around.** #26.

Everything in trips 0–3 is 75 minutes of total effort and clears 15 of the 28 captures, including four of the five that matter.

---

## 8. Five things to fix in the records before the owner is asked

1. **The level-gate capture is in no capture list.** I checked the file: `CAPTURE-REQUESTS.md` §1 is exaltation stacking, §2 is dual wield, §3 is haste, and the "Queued, not yet written up" section holds only haste. Both Director's HANDOFF ("the capture list, item 2, **six Shadow Rage item windows**") and EQL50ups' HANDOFF ("blocked on the capture in `CAPTURE-REQUESTS.md` §2") point at §2, which is the dual-wield request. **An owner working the list would never take the Shadow Rage windows.** Write #2 and #3 up as §4 first.
2. **`Solo 3` is recorded as answered in one repo and open in another.** Director dropped it as ANSWERED (R96); EQLSLockouts has it open at `lockoutCore.js:439`. Both are right about different things: the lock's *existence* is answered, the *entry line* has never been logged. Ask for the log line, not the lock.
3. **The reset-hour ask must carry the positive control.** EQLSLockouts' wording asks only for the wall clock; Director's records why that is not enough. Send the merged version.
4. **`CAPTURE-REQUESTS.md` exists only in EQL50ups.** EQLSLockouts uses `docs/CAPTURE-PROTOCOL.md`; eql-source and Director have no such file, and their asks are scattered across `CLAUDE.md` §9, `docs/FINISH.md`, `verify_gate` strings, `settle=` fields in `_build/build13.py` and per-zone "Still open" tables. Any brief that assumes one file per repo will come back short.
5. **Two known-stale statements bear on what to ask for.** `CLAUDE.md` says ten `/loc` for Sky; `_build/build8.py` computes nine from `len(RING)` — asking for every island reachable answers the tenth-island question as a by-product. And the Fear and Hate `verify_gate` strings claim "no named coordinate is recorded for this zone", which is overstated: `index-data.json` already holds coordinates for Dread, Terror, Fright and Maestro of Rancor. Gate 3 is genuinely open in both zones, but the gate text is wrong about there being none at all.
