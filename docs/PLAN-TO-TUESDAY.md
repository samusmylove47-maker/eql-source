# Plan to Tuesday morning

**Written Sunday 16 August 2026, evening.** Target: professional, publishable,
and fronted by a Castle Mistmoore guide good enough to push the site on.

---

## Phase 0 — new logs. DONE

Two Shara logs added, 14 and 16 August, no overlap with the four already held.
Corpus 1,918,093 → 2,098,441 lines. Raid fights 104 → 122.

Six boss/tier combinations we had never measured, all Plane of Hate at D1,
including **Innoruuk at D1** — so a plane boss now has a D1/D3/D4 ramp rather
than two points at the top. Four new Plane of Sky sessions feed the Sky work.

## Phase 1 — the things that cost us the argument

These come first because they are cheap, and because Mistmoore inherits them:
the item-field fix is what puts **no drop** on Mistmoore's loot.

1. **The ZEM superlative.** Kedge Keep is 139. The Hole is 128, tied with
   Warrens and Splitpaw, and calls itself the highest in the game in its H1,
   its meta description, its Open Graph card and its Twitter card. Derive the
   phrase from `zones.v1.json`; regenerate the share card; add a `gate.py` rule
   that fails the build when a superlative sits beside a rankable field.
2. **Item pages drop the deciding fields.** `no drop` appears 159 times across
   19 surveys and 0 times across 442 item pages; not one carries Damage or
   Delay. The extractor splits the "Slot / type" cell and keeps the first token.
3. **Raids is a top-level section containing no raids**, while the raid data is
   the best material on the site — and it just grew by 18 fights.
4. **Voidling locations** supplied by the collaborator that never reached a page.
5. **Four smaller contradictions**: Najena's Journeyman's Boots quest against
   `still-true.html`; Fear and Hate both calling a closed gap "the largest gap
   on this site"; eleven dungeons against six; eight islands against nine.

## Phase 2 — Castle Mistmoore. The headline.

The most time, and the work the site gets judged on.

- **Refine the map.** Push the cartographer idiom hard — storeys, routes,
  named at their measured positions, legible at a glance.
- **Cut without mercy.** Anything a player standing in Mistmoore already knows
  comes out. What stays is what they cannot get anywhere else: measured
  backstab evidence, the two-kit trash finding at D1, camp value, loot.
- **Best foot forward.** This page is the argument for the whole site.

## Phase 3 — Sky Ledger

Landing-page promotion above the plates, its own page, the reskin, and the
retirement of our weaker tracker. Now with four more Sky sessions behind it.

## Phase 4 — the majors from the blind read

Mobile deleting the change log's Type and Date; the hover-only quality score;
search reaching 44 of 722 pages; unexpanded abbreviations; nobody named as
running the site.

---

## Order, and why

Phase 1 before Phase 2 because Mistmoore's loot table is downstream of the item
fix, and because a beautiful page on a site that contradicts itself is a
beautiful page nobody trusts. Phase 3 before Phase 4 because the Ledger is a
front door and the majors are polish. If time runs short, Phase 4 is what gives.
