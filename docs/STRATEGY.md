# Where this site wins

Written 9 August 2026, from our own analysis of the four live EQ Legends
reference sites. This is the answer to "why us and not them", and it is meant to
be argued with rather than admired. If a competitor closes the gap described
here, this document is wrong and should be rewritten.

---

## 1. The market, read honestly

| | What it is | Its real strength | Its structural weakness |
|---|---|---|---|
| **eqlwiki** | MediaWiki, hundreds of editors | Total coverage. Every mob has a crawlable URL. Wins every long-tail search, permanently | **It cannot tell you what it got wrong.** Large parts are Project 1999 text describing a different game, and a 2019 import and a measurement taken last night render identically |
| **eqlegendstools** | One maintainer, item and gear tools | Inventory import — you drag your `/outputfile` in and it knows your character. The strongest single feature anyone ships | No provenance at all. "Curated, audited" is an assertion. No dates, no sources, no change log |
| **eqltools** | Client-mined, automated | 3D zone atlas, log parser, hourly recomputation from wiki edits, confidence labels | Confidence is not provenance. It tells you how sure it is, not *where the number came from* or *when it was last true* |
| **eqlsource** | Ten plates, one raid, five tools | Mesh geometry, measured logs, tiered provenance | Small. Slow. One author. No inbound channel |

**We are not going to out-cover eqlwiki.** They have the whole game and hundreds
of editors. We are not going to out-tool eqlegendstools on gear, or out-automate
eqltools. Competing on any of those is choosing a fight we lose on arithmetic.

## 2. What we actually own that nobody can copy quickly

1. **The game's own geometry.** `_build/geometry.py` reads Daybreak's `.s3d`
   mesh archives and derives walkable floor. Every coordinate we publish is
   tested against it — 176 of 176 land on drawn floor, and six impossible Najena
   coordinates were caught and withheld that way. eqltools plots `/loc` data
   from the wiki; **they cannot tell you when the wiki's `/loc` is wrong.** We
   can, and have.
2. **First-hand instrument data.** Tier M. Our own combat logs, published with
   trio, level, zone, difficulty, date and sample size. It produced the
   difficulty tier names read off the zone line, two class kits on *trash* at
   D1, and the living/undead faction split in Old Guk. Nobody else publishes
   measurement with its conditions attached.
3. **The tier discipline itself.** It is the only reason we can look at an
   eqlwiki page and say "infobox current, prose is 1999" — which is the single
   most useful sentence in this ecosystem and nobody else says it.

Note what these have in common: **all three require having read the classic text
carefully.** Being downstream of eqlwiki is not our ceiling. It is the
precondition for the only job nobody else is doing.

## 3. The niche, in one sentence

> **Every EQ Legends player is a returning EverQuest player carrying twenty-five
> years of muscle memory, and a large amount of what they know is now wrong. We
> are the site that tells them which parts.**

eqlwiki cannot do this — it *is* the classic text. eqltools computes what is
currently true but never contrasts it with what people expect. eqlegendstools
does items. Nobody is answering the question every returning player actually
has, which is not "what is the respawn timer" but **"is what I remember still
true?"**

We have already been doing this without naming it. Multiclass. D0–D4 not raising
mob levels. "You need a full group of level 50s" being from a game where neither
multiclass nor difficulty tiers existed. The Per-Level Hunting Guide being a
P99 import that predates both. Those are all the same product, written four
times without a home.

### The Changed-from-Classic register

One page, one entry per mechanic, each carrying:

- **What classic did** — with a source, marked plainly as historical.
- **What Legends does** — with its tier and its date.
- **How we know** — patch note, structured wiki record, our own logs, or a
  named player's report.
- **What would settle it**, when it is not settled.
- **Who found it.**

Why this is the right bet:

- **It is search-shaped.** People type "is X still true in Legends". Nothing
  currently answers that.
- **It is Discord-shaped.** It settles arguments, and being the link people
  paste into a disagreement is how a reference becomes canonical.
- **It is community-fed.** Players trip over these constantly and enjoy being
  the one who noticed. Annalise found one on 9 August without being asked.
- **It compounds.** Every entry makes the next one easier to spot, because the
  register itself becomes the list of things worth re-testing.
- **It is cheap.** Most entries are one observation plus one confirmation.

### The tier this needs: Tier C, community report

Our scale runs M, 1, 2, 3, 4, 5. A named player reporting first-hand play is
none of those. It is not measured by us, so it is not M. It is not a read of a
document, so it is not 3–5.

**Tier C sits below M and above 3.** First-hand, named, dated, unconfirmed. It
publishes with the reporter's name, the date, and the line *what would confirm
it*. It is never laundered into fact by repetition — an entry either gets
confirmed and moves tier, or stays C indefinitely, visibly.

This gives the contact route we are building somewhere to land, and it gives a
contributor something better than thanks: **a credited entry they can point at.**

---

## 4. Ruling on the two user reports, 9 August 2026

### 4.1 Annalise — underwater combat, Kedge Keep

> "back in OG EQ underwater combat you needed a pierce weapon as slash and blunt
> were nerfed. it seems like that in Legends that isnt the case as i am under
> water slapping things in kedge keep with a sword"

**Merit: high. This is exactly the product described above, and it is entry
one.** Not because it is confirmed — it is not — but because it is the shape.

Checked 9 Aug 2026:

- eqlwiki's **Kedge Keep** page carries `{{Classic Era}}`, describes the zone as
  entirely underwater, warns about breathing — and **says nothing whatever about
  weapon types or damage underwater.**
- eqlwiki search returns **zero results for "underwater"**, on a wiki whose
  Kedge Keep page contains the word repeatedly. **Their search index is not
  reliable and absence of results there is not evidence of anything.** Worth
  remembering the next time a search comes back empty.

So the wiki neither confirms nor denies. It has no position.

**Published as Tier C, credited to Annalise, dated, with the confirmation
condition stated: a combat log showing a slashing or blunt weapon landing normal
damage on a mob while submerged in Kedge Keep.** One log settles it. Kedge Keep
is not one of our ten plates, which does not matter — the register is about
mechanics, not zones, and this is the first argument for the register existing
independently of the plates.

**Do not state the classic rule as fact without a citation.** It is widely
believed and we have not sourced it; the entry says so.

### 4.2 The five-plus plate recommendations

| # | Ask | Ruling |
|---|---|---|
| 1 | **Toggle names on the plate plans** to cut clutter | **Accept.** Cheap, obviously right. The plots are dense by design and a reader orienting does not need 18 labels at once |
| 2 | **Show the stairs and ramps** that connect layers | **Accept, and it is better than asked.** We do not have to hand-place them: a ramp is a mesh triangle whose normal is neither floor-flat nor wall-vertical. `geometry.py` already classifies by normal to find floors. The same pass can emit connections. Derived from the game, not guessed |
| 3 | **Optimal named farming route**, toggleable overlay, described when on | **Accept, with an honesty constraint.** Order the named by a real route solve, draw it, and **say plainly that segments are straight lines between spawn points, not walked paths**. We hold floor geometry, so a segment crossing a wall can be flagged. Publishing a route that walks through a wall unmarked would be exactly the sin this site exists to avoid |
| 4 | **Layer selection should filter the named** to that layer | **Accept.** Most coordinates are two-value with no Z, so the layer is inferred from which floor the position lands on. Where two floors overlap, the mob shows on both, and the plate says that is why |
| 5 | **Loot list for a selected named** on the route view | **Accept.** `index-data.json` already ties every item to its dropping mob. This is a join we already hold and have never surfaced on the map |
| 6 | **Exaltations tool** — list all, filter by type, source weapons, removal level, drop locations | **Split ruling.** *Reject* building an exaltation planner: eqlegendstools ships one and `CLAUDE.md` forbids shipping a worse copy of an existing tool. *Accept* the half nobody else can build — **exaltation → source item → which named drops it → which plate and which coordinate.** That join needs our plate data and their planner cannot make it. **Blocked on data: we hold no exaltation records at all**, so this starts with a sourcing pass, not a build |

**Items 1, 3, 4 and 5 are all the same surface** — the floor plan on each plate —
and should ship together as one coherent map upgrade rather than four patches.

---

## 5. Order of work

1. **The map upgrade** — name toggle, layer-filtered named, named detail with
   its drops, route overlay. Recommendations 1, 3, 4, 5.
2. **The Changed-from-Classic register**, with Tier C, seeded with the
   underwater entry and the multiclass and difficulty findings already written
   elsewhere on the site.
3. **Ramp and stair extraction** in `geometry.py`. Recommendation 2.
4. **Exaltation sourcing pass**, then the drop-source join. Recommendation 6.
5. Item and named-mob pages — the long-tail surface we do not have.

## 6. What would prove this strategy wrong

- If eqlwiki starts marking its own imports, the tier discipline stops being
  differentiating overnight. Watch `Category:Classic Era` adoption.
- If eqltools adds provenance to its confidence labels, the register is
  reproducible by someone with more data and more automation.
- If the register cannot reach thirty entries, it is a page and not a product.
