# What counts as done — a correction to the verification standard

**Date:** 14 August 2026
**Status:** proposed by Claude, awaiting the collaborator's decision
**Supersedes:** the three-gate standard in `docs/SOURCES.md` as the *headline*
grade. It does not remove those gates; it demotes them.

---

## The problem, stated by the person who owns the site

> *Few people playing EQ Legends care about plot coordinates. Few players have
> cared about `/loc` for 20+ years… trash monsters are irrelevant. Players only
> care about bosses, unless it's for farming experience, in which case that is
> a different set of data. What our site needs to carry is only data that
> players care about.*

That is correct, and the site's own grade proves it.

**Plane of Fear and Plane of Hate are marked `verify_level: none`.** The site
holds, for those two zones: Cazic-Thule killed at Adaptive, Fused and Refined;
Innoruuk at Fused and Refined; ten of Innoruuk's court; every spell each of them
cast; damage to kill; which named mob drops which planar armour set; and 262
measured kills across 100 mob types.

They score zero because **gate 3 asks whether plotted coordinates land on drawn
floor**, and neither zone has plotted coordinates. The gate cannot be passed
there by any amount of play. Meanwhile Kedge Keep, where we have never logged a
single session, scores the same zero — so the grade cannot tell the difference
between *no coordinates* and *no evidence at all*.

**A standard that cannot distinguish those two is not measuring the thing.**

## What the old gates actually are

They are **sourcing hygiene**, and they are good at that:

1. wiki page fetched in full, roster re-compared
2. edit history fetched, not just the footer date
3. every coordinate within 120 units of walkable floor

Gates 1 and 2 are how the provenance test gets applied. Gate 3 is how the map
gets proved. All three are worth keeping — as **properties of a claim**, which
is exactly where the per-field provenance model already puts them.

What they are not is a measure of whether a page is useful to somebody playing
the game tonight.

## What players actually need, in order

Taken from the collaborator, who plays this game:

1. **Bosses.** Which ones, what they do, how the difficulty tier changes them.
2. **Loot.** What drops, from which boss, at which tier.
3. **Difficulty.** How D0–D4 changes the fight, the kit and the drops.
4. **What is new in Legends** versus EQ Live and Project 1999 — the inherited
   advice that is now wrong.
5. **Farming value**, for the zones people grind: ZEM, density, respawn.
6. **Their own progression**: unlocks, quests, what to chase next.

Trash matters only where it feeds 3 or 5. Coordinates matter to *us*, for
drawing the floor plans — they are a build input, not a reader's need.

## The proposed grade

Score a zone on **coverage of what a player needs**, and keep the tier of each
claim beside it. Something like:

| Facet | Counts as covered when |
|---|---|
| Bosses | every named raid target has its behaviour recorded, measured where we have logs |
| Loot | the drops are listed with their source, and measured counts where we have them |
| Difficulty | the zone's behaviour is recorded at more than one tier |
| Inherited | the classic advice that is wrong here is named and marked |
| Farming | ZEM, density and respawn stated, for zones people grind |

Each facet carries its best evidence tier, exactly as `sky.json` does per claim.
The headline becomes **"what do we know about this zone that you need"**, not
"did a coordinate land on a polygon".

Under that grade, on today's data: **Fear and Hate go from the bottom of the
table to near the top**, because we have killed both gods across three
difficulty tiers and recorded what they do. Kedge Keep stays at the bottom,
correctly, because we have never played it.

## What this costs

Almost nothing structural. The machinery is already right:

- per-claim provenance exists (`sky.json`, and the model is documented)
- measured data exists and is joined (`measured.json`, `sightings.json`)
- the public contract exists and can carry a new field
- `check.py` already refuses to let a count disagree with its data

What changes is **the criteria and the field**, not the architecture. This is a
config-and-copy change, not a rebuild.

## What I got wrong, and why it matters beyond this file

I built increasingly precise machinery for verifying things, and stopped asking
whether the things were worth verifying. Then I used the output of that
machinery — `verify_level: none` — as evidence in a critique of the site's own
quality, without noticing that the metric had drifted from the mission.

The site's stated failure mode is *"a correct decision reaches the authored
layer and stops at the boundary with the generated layer."* This is the same
fault one level up: **a correct standard was written, the project's purpose
moved, and the standard did not follow.**
