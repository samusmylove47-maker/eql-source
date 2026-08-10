# The three planes — research dossier and sourcing rulings

Research for the Plane of Fear and Plane of Hate guides, and for the Plane of
Sky material already on the site. Compiled 10 August 2026.

**Read the rulings in section 1 before writing a word of either guide.** They
decide what may be stated plainly, what must be badged, and what we must refuse.

---

## 1. The ruling: the boss pages are classic EverQuest

Every Plane of Fear and Plane of Hate **boss** page on eqlwiki is a Project 1999
import carrying classic stats, and one of them says so out loud. Checked against
the MediaWiki revision API on 10 Aug 2026, not against page footers.

| Page | Oldest revision | Author | Verdict |
|---|---|---|---|
| Plane of Fear | 2026-03-09 | `P99Wiki>RibbonRMX` | Import. Prose T5 |
| Plane of Hate | 2026-03-27 | `P99Wiki>Permahoo` | Import. Prose T5 |
| Cazic Thule (God) | 2026-03-29 | `imported>CrazyPro` | Import. T5 |
| Innoruuk (God) | 2025-04-11 | `imported>CrazyPro` | Import. T5 base |

`Plane of Fear` carries `{{Classic Era}}`; the boss pages carry `{{Fear Era}}`
and `{{Hate Era}}`. None of that changes the answer — the revision history does.

### The tell that settles it

The Cazic Thule strategy section reads, verbatim:

> "It's recommended to have several dozen melee and a dozen+ healers."

**Legends caps a raid at 8.** It also references "the Velious era revamp",
chain-CH healing rotations, and Temple of Veeshan loot comparisons. This is
classic EverQuest raid text, word for word, and following it in Legends is not
possible. It is not "slightly stale" — it describes a different game.

### The boss stat corpus, and what is wrong with it

Pulled verbatim from the infoboxes on 10 Aug 2026:

| Boss | Level | AC | HP | Respawn as published |
|---|---|---|---|---|
| Cazic Thule | 70 | 400 | 450,000 | not recorded |
| Innoruuk | 60 | 600 | **156,000 (D2 Raid), 235,000 (D4 Raid)** | 7 days ±8h |
| a dracoliche | 58 | 600 | 175,000 | 7 days ±8h |
| Dread | 55 | 376 | 32,500 | 72h ±8h |
| Terror | 55 | 397 | 32,000 | 72h ±8h |
| Fright | 55 | ? | ? | 72h ±8h |
| Maestro of Rancor | 52–53 | 363 | ~16k? | 3 days ±8h |

Two things are wrong with this table as Legends fact.

**The respawn timers cannot be true.** Tier 1, patch notes 16 June 2026:

> "Maestro of Rancor, Innoruuk, the Prince of Hate, Cazic Thule, Fright, Terror,
> Dread, and a dracoliche no longer spawn in the open world & personal instances
> of Planes of Hate and Fear."

These bosses are raid-instance only. A 7-day open-world respawn describes a
spawn that no longer happens. Every timer in that column is stale.

**The HP figures are single-difficulty.** Legends runs D0–D4. One number cannot
describe a boss across five tiers, and `Fright` and `Maestro of Rancor` are
question marks even in classic terms.

### The one Legends-era exception, and why it still is not tier 2

Innoruuk alone carries difficulty-tiered hit points, verbatim:

```
| HP = 156000 (D2 Raid), 235000 (D4 Raid)
```

That is the **first published D4 raid figure we have found anywhere**, and
`CLAUDE.md` records D3 and D4 as pinned by nobody. It is worth having.

It is **not** tier 2. The provenance test asks for a named editor changing the
field *after launch* with a comment describing measurement. The edits that
carried it — Mandlz 10 July, Aursan 16 July ×3 — are pre-launch beta, and not
one comment states a method. The page's last edit, Mazirian on 28 July, cut it
by 1,577 bytes with no comment at all.

**Ruling: publish it as T3, labelled beta-era, explicitly not confirmed since
launch.** Say what would settle it: one raid log from a D2 or D4 Innoruuk.

The 1.51× ratio between D2 and D4 is *not* a scaling law. It is two numbers from
one boss. Do not extrapolate it to any other encounter, and do not print it as a
rule.

### Cross-validation that did work

The wiki's boss roster and the 16 June patch note name **exactly the same seven
bosses** — Hate's two (Maestro of Rancor, Innoruuk) and Fear's five (Cazic
Thule, Fright, Terror, Dread, a dracoliche). The patch note's "Innoruuk, the
Prince of Hate" is one boss, not two; that is Innoruuk's classic epithet, and
2 + 5 = 7 accounts for the list exactly.

So the *roster* is confirmed by tier 1. Only the *stats and strategy* are
classic.

---

## 2. Tier 1 — what the patch notes actually establish

From eqlwiki.com/Patch_notes, which is a dated archive of the developers' notes.
Everything here outranks everything in section 3.

### Instances, and how many kinds there are

| Date | Note |
|---|---|
| 2026-06-16 | "Personal instances for Plane of Hate and Plane of Fear are now available!" |
| 2026-06-16 | The seven raid bosses "no longer spawn in the open world & personal instances" |
| 2026-06-23 | "Personal instances of the Plane of Sky are now operational." |
| 2026-06-11 | "Enabled Personal Instances of Nagafen's Lair, Permafrost, The Hole, and Kedge Keep." |
| 2026-06-02 | "Balance changes to Solo Raid versions of Innoruuk, Cazic-Thule, Maestro of Rancor, and Lord of Loathing." |

So at least four contexts exist: **open world**, **personal instance**, **solo
raid instance**, and **raid instance**. A boss can be absent from the first two
and present in the others. The distinction is load-bearing for both guides and
we should not blur it.

The Plane of Hate page describes the door mechanism, and it matches:

> "interacting with the black sword at the top of the tower for the public
> instance, or **the voidling for the raid instance**."

### Loot lockouts

| Date | Note |
|---|---|
| 2026-06-23 | "if you are in that lockout you will only receive 1 piece of loot per named raid creature that has its own lockout. The raid bonus loot lockouts reset every Tuesday at 8AM PST." |
| 2026-07-28 | "Killing a raid boss while you have a loot lockout will now give one guaranteed drop from that boss's unique treasure tables." |
| 2026-07-29 | "Loot drops will correspond to the difficulty tier you're in, plus a diminishing chance to roll higher tiers." |

The 28 July note is a meaningful improvement and reads as under-reported: a
lockout kill is no longer worthless, it is one guaranteed unique-table drop.

### Motes and the token

| Date | Note |
|---|---|
| 2026-06-29 | "Players can now upgrade spells using motes… through inspecting spells (via right-click hold) and adding motes." |
| 2026-06-29 | Upgrades give reduced mana cost, reduced cast/recovery/reuse, increased durations, better resist rates |
| 2026-06-21 | A construct "can condense your motes into stronger versions, at a two-to-one rate! NOTE: For the moment, he can only accept ranks 1-8." |
| 2026-07-28 | "Introducing Void-touched Potential, a new token that can be earned up to 3 times per week from raid activities through voidlings." |

### ZEM — and Hate is the best of the three

| Date | Note |
|---|---|
| 2026-06-23 | "Boosted the ZEM on instanced versions of Hate, Fear and Sky to match that of the open world version." |

Per the zone infoboxes, each showing a struck-through classic 75:

| Zone | ZEM | vs base |
|---|---|---|
| Plane of Hate | **86** | 115% |
| Plane of Fear | 82.5 | 110% |
| Plane of Sky | 82.5 | 110% |

That combination — a 115% ZEM, no open-world boss risk since the raid bosses
were moved out, and instances that match open-world rates — is the mechanical
basis for the 46+ levelling and farming reputation. It is sourced, and it is
worth stating plainly in both guides.

### Fear-specific

| Date | Note |
|---|---|
| 2026-06-24 | "Cazic-Thule now properly calls for his minions when he is engaged in an instance of the Plane of Fear." |

That corroborates the zone-wide social aggro the wiki describes, in a Legends
instance, from a tier 1 source. It is the one boss mechanic we can state flatly.

---

## 3. Zone facts — tier 2 candidates, from the infoboxes

The infobox fields below sit on imported pages but were maintained through July
2026 by named editors. Treat as **T3**, badged, until a post-launch measured
edit or our own log confirms them.

| | Plane of Fear | Plane of Hate |
|---|---|---|
| `/who` name | `fearplane` | `hateplane` / `hateplaneb` |
| Monster level | 48+ | 48+ |
| Minimum player level | 46 | 46 |
| Adjacent | The Feerrott | Oasis of Marr (one-way), wizard port |
| Succor / evacuate | −1139, 1282 | −375, −354 |
| ZEM | 82.5 (110%) | 86 (115%) |

**Hate has two zone names.** `hateplaneb` is a second Hate zone, and it is not
a typo: a patch note refers to a "Plane of Hate B" achievement trigger. What
`hateplaneb` is in Legends — the second floor, a separate instance, or the
revamped zone — **we do not know, and neither guide may guess.** One `/who`
while standing upstairs settles it.

### Access

**Fear.** One-way portal in the spectre caves of The Feerrott. Level 46 gate.
No conventional exit — gate, port, or the exit portal deep in the Temple, which
the page advises against. A race line runs at the portal.

**Hate.** Wizard spell `Alter Plane: Hate`, reagent `Fuligan Soulstone of
Innoruuk` at 62.5pp from wizard spell vendors; or the one-way Oasis of Marr
portal. At the Oasis tower: **black sword for the public instance, voidling for
the raid instance.** No conventional exit.

### Hate's layout — the reason a 3D model is on the table

The page numbers 30 map locations across **two floors**:

- 1 — port-in
- 2–19 — various buildings
- 20 — The Church
- 21–28 — various buildings
- **29 — the Organ Hall, Maestro of Rancor. This building has a second floor**
- **30 — spiral staircase to the second level. The Fountain is immediately east**

Three map images exist, including `HateSecondFloorWithFirstOverlay.jpg` — the
second floor drawn over the first in grey. That someone needed to build that
overlay is the argument for a 3D or layered treatment in one sentence.

Innoruuk's location field reads "Wanders Upstairs".

---

## 4. The armour sets

Both planes drop planar armour split into two groups by class. Same two groups
in both zones; different slots.

- **Fear drops** Chest, Wrist, Hands, Feet
- **Hate drops** Head, Arms, Wrist, Legs

Wrist drops in both. Seven distinct slots between them.

**Group 1** — wisdom casters, Berserkers, Monks, plus all of Lustrous Russet:
Ethereal Mist (CLR), Vermiculated (DRU), Rune Etched (SHM), Anthemion (BST),
Thorny Vine (RNG), Valorium (PAL), Shadow Rage (BER), Shiverback-hide (MNK).

**Group 2** — intelligence casters, Rogues, Warriors, plus all of Midnight Clad:
Insidious (ENC), Apothic (MAG), Blighted (NEC), Carmine (WIZ), Imbrued (BRD),
Umbral Platemail (SHD), Woven Shadow (ROG), Indicolite (WAR).

**Beastlord and Berserker sets are listed.** Neither class exists on Project
1999. Their presence is real evidence that the armour tables specifically were
rebuilt for a 16-class game, which is why these tables are the strongest
material on either page — and why they are worth more than the boss stats.

### Fear — slot to mob

| Slot | Group 1 | Group 2 |
|---|---|---|
| Chest | a glare lord, a tentacle tormentor | amygdalan knight, amygdalan warrior |
| Wrist | a decrepit warder, a samhain | a fetid fiend, a spinechiller spider |
| Hands | a scareling, a shiverback | a frightfinger, a turmoil toad, a worry wraith |
| Feet | a boogeyman, a phantasm | a gorgon, a nightmare |

`Phoboplasm` drops any planar armour, **including Hate-only pieces**.

### Hate — slot to mob

| Slot | Group 1 | Group 2 |
|---|---|---|
| Head | Cleric of Innoruuk | a spite golem |
| Arms | a forsaken revenant (f), an ire ghast | a forsaken revenant (m), an ashenbone drake |
| Wrist | an abhorrent, a scorn banshee | a kiraikuei, a loathling lich, a revultant rat |
| Legs | an elite dragoon (m), Innoruuk's Chosen (m), a Disciple of Innoruuk, a Knight of Innoruuk | an elite dragoon (f), Innoruuk's Chosen (f), an Agent of Innoruuk, a Champion of Innoruuk, a Sage of Innoruuk |

`a haunted chest` drops any planar armour, **including Fear-only pieces**.

Gender splits the group on three Hate mob types — forsaken revenant, elite
dragoon, Innoruuk's Chosen. Male and female drop for *different* groups. That is
a genuinely useful, easily-missed fact and belongs high in the Hate guide.

### Hate's minibosses map one-to-one onto trash

Each is the upgraded version of a common mob and drops a named armour set. This
is the cleanest structure on either page and should drive the Hate guide's loot
section.

| Miniboss | Upgrade of | Set it drops |
|---|---|---|
| High Priest M`kari | Cleric of Innoruuk | Ethereal Mist |
| Master of Spite | a spite golem | Rune Etched |
| Coercer T`vala | a forsaken revenant (f) | Insidious |
| Magi P`Tasa | a forsaken revenant (m) | Apothic |
| Avatar of Abhorrence | an abhorrent | Woven Shadow |
| Grandmaster R`Tal | a kiraikuei | Indicolite |
| Mistress of Scorn | a scorn banshee | Imbrued Platemail |
| Ashenbone Broodmaster | an ashenbone drake | not recorded |
| Lord of Ire | an ire ghast | not recorded |
| Lord of Loathing | a loathling lich | not recorded |

`Lord of Loathing` is named in the 2 June patch note among bosses given Solo
Raid balance changes, alongside Innoruuk, Cazic-Thule and Maestro of Rancor.
So it is a real Legends encounter, not just an imported name.

---

## 5. Errors found in the sources

Recorded because we correct rather than copy, and because these are what a
reader hits if they use the wiki directly.

1. **`a scorn banshee` is filed under "Group a"** in Hate's common-mob table — a
   typo. The armour table puts it in Group 1, and Mistress of Scorn dropping
   Imbrued (a Group 2 set) makes the row internally inconsistent. Flag, do not
   silently pick one.
2. **`Imbrued Armor` and `Imbrued Platemail Armor`** are used for what appears
   to be one set, on the same page.
3. **`Wraith of a Shissir` and `Wraith of a Shissar`** — both spellings on the
   Fear page, table against prose.
4. **`a decrepit warder` appears in Fear's armour table but not its mob table.**
   A whole mob is missing its row.
5. **"Non-raid mobs in fear are level 48(49?)-51"** — the source hedges its own
   level range in place. We inherit the hedge; we do not resolve it by picking.
6. **`Fright` has no AC, no HP and no attacks per round**, and its damage is
   "437?". One of the five Fear raid targets is essentially unrecorded.

---

## 5b. Tier C — the first genuinely Legends-era account we have found

**Source.** "EverQuest Legends | Guide To Quickly Farming Lustrous Russet Armor
| Plane Of Hate", channel **Classic XP** (4.87K subscribers), published
**9 August 2026**, 3,261 views, 21 minutes. Transcript read in full 10 Aug 2026.

**Tier C, not tier M.** It is a named player describing his own play, on a dated
session, in a D4 instance. Nothing is parsed and nothing is counted. It outranks
the imported wiki prose and it does not outrank a log.

The channel's own tags are `#p99 #project1999 #ProjectQuarm`, so it covers
classic emulators generally — but the content is unmistakably Legends: D3/D4
instances, merging, AA gain, non-respawning instance options.

### What it establishes, and what it only suggests

| Claim | Standing |
|---|---|
| Haunted chests sit **in the small houses**, never the big buildings or streets, usually in a corner | First-hand, repeated, and he navigates by it for 21 minutes |
| He believes chests are **static spawns in fixed spots** | He says so and then says he is not sure, and asks commenters. Publish as open |
| Roughly **one piece per three chests** | **He says "I feel like". Nothing was counted. Do not publish as a rate** |
| **Rats see through invisibility** | Contradicts the wiki. See below |
| Haunted chests **drop only Lustrous Russet** | Contradicts the wiki. See below |
| A trash kill gave **9% of an AA**; he has 229 AAs | One reading, no level or difficulty stated for the AA figure |
| Open-world Hate is **contested**; he moved to instances to avoid competition | Practical, and it matches the instance system existing at all |
| Sky is where weapons come from; Hate and Fear are where armour comes from | Consistent with the Sky island/boss structure |

### Two contradictions with the wiki, and how they resolve

**1. Do haunted chests drop anything but Russet?**

- eqlwiki: "a haunted chest can drop any planar armor, including pieces that
  normally drop only in Plane of Fear!" — **T5, imported prose**
- Classic XP: "all they drop is the russet gear. That's all they drop." — **Tier C**

C outranks 5, so the Legends-era reading leads. The likeliest reconciliation is
that this is a Legends change from classic behaviour, which is exactly the kind
of thing this site exists to catch. **Publish as: the imported text says any
planar piece; the only Legends-era account says Russet only; unresolved.** One
logged session of chest kills settles it outright.

**2. Do rats see through invisibility?**

- eqlwiki common-mob table: `a revultant rat` — Sees invis: **NO**
- Classic XP: "Rats see through invis. They're annoying."

Same ruling, and this one is cheap to check — a single invis'd approach.

### Where the video *confirms* the wiki

He kills a haunted chest and a rat together and reports "that dropped a mage
wrist". Apothic is the Magician set and sits in **Group 2**; the wiki puts
`a revultant rat` at **Wrist, Group 2**. The drop matches the rat, not the
chest — which both explains the apparent contradiction with his own "chests only
drop Russet" claim *and* independently confirms the wiki's armour table.

**The armour tables are the strongest material on those wiki pages, and this is
the first outside evidence for them.**

### The multiclass sets, and a wearability rule the wiki does not state

He describes the two shared sets by who can wear them, which is orthogonal to
the wiki's Group 1 / Group 2 split by which mobs drop them:

> "there's two sets of stuff like lustrous russet. There's like a leather cloth
> one and then there's a plate male one. This is the plate mail one."

So **Lustrous Russet is the plate-and-mail multiclass set** and Midnight Clad is
the leather-and-cloth one. Unconfirmed, and worth confirming: it is the single
most useful sentence for a reader deciding which plane to farm.

He also states a multiclass consequence worth chasing: **"The bard is our plate
class. The bard is what gives us plate."** Armour access appears to come from
the trio, not the character. If that is right it belongs in `learn/`, not only
in these guides.

### The `+N` ceiling is a merge ceiling, not a drop ceiling

He refers to a "woo fist **plus 10** from sky". `CLAUDE.md` records drops at
`+N` where the modal `N` is the difficulty, which caps at `+4` at D4. Both are
true: `+10` is reached by **merging**, and the difficulty governs what a merge
is worth. The rule in `CLAUDE.md` is about *dropped* values and should say so
rather than reading as a ceiling on the item.

### The strongest available argument for a 3D or layered Hate map

Unprompted, from someone farming the zone daily:

> "hate could be very confusing. You know, there's the upper level, there's the
> bottom level… you can memorize the upstairs or whatever pretty easily, but
> down here it's just a lot of houses with a lot of little dots on the map."

He asks his own viewers whether the chest spawns are fixed, because he cannot
hold the ground floor in his head. That is a named user, with an audience,
describing precisely the problem a separated-storey map solves. It is a better
argument for the 3D treatment than any reasoning of our own.

---

## 6. Sources that look authoritative and are not

There are at least three of these, and the family resemblance is the tell:
`eqlegends.wiki`, `everquestlegends-wiki.wiki` and `everquestlegendswiki.wiki`.

`eqlegends.wiki` and `everquestlegends-wiki.wiki` rank well for Legends queries
and are **not** community wikis. Checked 10 Aug 2026: no named authors, no
dates, no revision history, no citations, no API. `eqlegends.wiki` attributes a
claim about Beastlord and Berserker Sky quest lines to unnamed "developer
comments" that cannot be checked.

Where its Sky access claim could be tested it was roughly right — East Freeport,
which eqlwiki puts at an orb near −425, −1200 — so this is not a fabrication
farm. It is worse for our purposes: **plausible, unattributable, and
uncheckable.** Treat as tier 4 at the absolute best, and prefer never to cite
it. It must never be the only source for a claim.

---

## 7. What we cannot answer, and what would settle it

Each of these is one log, one screenshot or one `/who` away.

| Open question | What settles it |
|---|---|
| What is `hateplaneb`? | One `/who` from the second floor |
| Boss HP at D0–D4, for all seven | Raid logs. Innoruuk D2/D4 is a beta claim by one editor |
| Do raid bosses run triple-class from D3 here? | A raid log at D3+. **The site's biggest gap** |
| Real respawn or lockout behaviour | The published timers describe a spawn that was removed |
| Fright's stats | Unrecorded by anyone, including classic sources |
| Plat per hour, motes per hour, AA per hour | Nobody publishes these. Our own logs could |
| Which armour pieces actually drop at which difficulty | The 29 July note ties loot tier to difficulty tier |

The last two are the opening. **No source we have found publishes measured rates
for Fear or Hate at any difficulty.** Our logs can, and that would be the first
tier M data on either zone anywhere.
