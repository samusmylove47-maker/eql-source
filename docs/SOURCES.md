# Sources and watchlist

The pages the automation checks twice a day, why each matters, and what to do
when one changes.

---

## Measured combat logs — instrument data, tier M

Every other source on this list is *read*. A combat log is *measured*: it records
what happened, in the live game, on a stated date, to a stated character. It is
the only thing the project has that can close the gaps CLAUDE.md calls the
biggest ones — which class kits attach to which mob, what a fight costs, what a
named mob actually drops.

`_build/logstats.py` turns a log directory into `assets/measured.json`. Logs are
kept out of the repository; the derived counts are committed.

**Tier M outranks every read source for what it directly measures, and
generalises to nothing at all beyond its stated conditions.** A hit rate is a
fact about one trio at one level against one set of mobs on one day. Publish the
conditions with the figure or do not publish the figure:

- character and class trio, and the same for anyone grouped
- level, and the level of what was fought when known
- zone, and the difficulty label from the zone line
- date, and the length of the sample

**One session is a sample, not a rate.** Say how many swings, kills or drops a
figure rests on. A drop seen once is "seen once", never a drop rate.

### Reading a log

- Zone and difficulty arrive together: `You have entered The Castle of Mistmoore
  1 (Awakened).` The parenthesised word is the difficulty tier name:
  **D0 Base/Normal, D1 Awakened, D2 Adaptive, D3 Fused, D4 Refined.** Supplied by
  the collaborator, 8 Aug 2026.
- Difficulty is separately readable from loot: items drop at `+N`, and the modal
  `N` is the difficulty. Read the *dropped* value, not the created one —
  `looted a Keg Mallet +2 ... to create a Keg Mallet +4` is a `+2` drop.
- **Both readings are kept, and reported separately.** They are independent —
  one comes from the zone name, the other from what dropped — so agreement is
  worth something. They agreed on the 8 Aug Mistmoore session: the line said
  `Awakened` and 22 of 27 drops were `+1`, giving D1 twice over. When they
  disagree, the difficulty is unresolved and the page says so rather than
  picking one.
- The collaborator marks context in party chat with `ATTN Claude:`. Those lines
  are captured verbatim as session notes.

### Telling mobs from players, which is where this goes wrong

A first pass recorded **Azuria** as a named mob missing from the Mistmoore plate.
Azuria is a player — they dodge, riposte, parry and carry a thorns shield, and
were fighting the same mobs we were. Published, that would have invented a mob
and given it a fabricated spell list.

A name counts as a mob **only on positive evidence**: the log says we slew it, it
was slain, it attacked us, or it is written with an article. Anything else is
left out. A named mob fought but never killed and never landing a blow gets
missed — the right way round to be wrong.

---

## The game's own map files — first-party geometry, tier 1

EverQuest Legends installs plain-text map files with the game:

```
C:\Users\Public\Daybreak Game Company\Installed Games\EverQuest Legends\maps\
```

194 files on the current install. The format is the long-standing EQ one, one
record per line, comma separated:

```
L x1,y1,z1,x2,y2,z2,r,g,b     one 3D line segment
P x,y,z,r,g,b,size,Label      one labelled point, underscores render as spaces
```

`<zone>.txt` is geometry; `<zone>_1.txt` is labels. **The coordinates share the
`/loc` space**, with the axis convention the project already uses:

```
map_x = −worldX      map_y = −worldY      map_z = worldZ (true elevation)
/loc prints worldY, worldX, worldZ
```

**This is first-party data shipped by the publisher and describing the live
game, so it outranks every wiki page.** Treat it as tier 1.

**What it can and cannot settle.** It is authoritative for geometry: zone
extents, floor plans, elevation, and which zone connects to which. The label
layers carry only zone exits — Najena's has exactly one label — so **there are
no mob positions in it.** It can prove a recorded coordinate impossible without
supplying the right one. It found six such coordinates in Najena on 8 Aug 2026.

Six of the ten plated zones are present (Najena, Splitpaw, Crushbone, Befallen,
Lower Guk, Mistmoore). Blackburrow, Nagafen's Lair, The Hole and The Warrens are
not in the shipped set.

**Do not copy these files into the repository or publish them.** They are
Daybreak's. Reading them to check our own figures is not publishing them; any
geometry the site draws must be our own derivation, not their line work.

---

## The watchlist

Machine-readable copy: `state/watchlist.json`. That file is what the automation
reads; this document explains it.

### eqlwiki.com — MediaWiki, has an API

**Do not scrape these pages on a schedule.** MediaWiki exposes Recent Changes.
Ask which watched pages changed since the last run and read only those. Faster,
cheaper, and it does not hammer a volunteer-run wiki twice a day.

```
https://eqlwiki.com/api.php?action=query&list=recentchanges
  &rcprop=title|ids|timestamp|comment|user&rclimit=200&format=json
```

Compare titles against the watchlist, compare `revid` against
`state/last-check.json`, read the full page only on a match.

| Page | Feeds | Why it matters |
|---|---|---|
| Najena | Plate 01 | Actively maintained; freshest zone page in the project |
| Lair of the Splitpaw | Plate 02 | Revamped, 4 named and 13 items added |
| Crushbone | Plate 03 | Revamped 14 Jul, touched 28 Jul; plate not fully verified |
| Befallen | Plate 04 | Import provenance inferred, not confirmed |
| Blackburrow | Plate 05 | Content dates from 4 Jul; Aug edits were images only |
| Lower Guk | Plate 06 | Respawn corrected 28:00 to 9:28 |
| Nagafen's Lair | Plate 07 | |
| The Hole | Plate 08 | Rebuilt after a fabrication was found. Watch closely |
| The Warrens | Plate 09 | Also the Kerra Isle faction source |
| Castle Mistmoore | Plate 10 | |
| Plane of Sky | Sky tracker, raid guides | Class quest tables and boss mechanics |
| Character Races | Race tools | Race to primary class matrix |
| Newbie Guide | Race tools | Lock rules, unlock mechanics |
| Alanna's Race Unlock Guide | Race tracker | The definitive race unlock source |
| Rituals | Najena plate, travel notes | The disputed druid/wizard port levels live here |

### Other sources — no API, fetch politely

| Source | Cadence | Notes |
|---|---|---|
| everquestlegends.com/news | Every run | **Tier 1.** Patch notes override everything |
| eqprogression.com Sky quests page | Weekly | Sky turn-in structure |
| eqltools.com | Weekly | **Confirmed 8 Aug 2026.** Zone Atlas, Trio Builder, AA Planner, Spellmaster, Log Parser, Gear Upgrade Finder, Where to Level, and the Learn primers. This is the site `CLAUDE.md` and `docs/BACKLOG.md` mean. Client-mined; we link rather than duplicate |
| eqlegendstools.com | Weekly | **A different site**, also real. Weapon and gear search, proc lookup, Plane of Sky quest reward tracker, focus and clicky lookup, Exaltation planner. The two were previously conflated in this file |
| eqlbuildforge.com/items | Weekly | Item stat snapshot, dated in the footer |

**Known blocked:** necrotalk.com (bot detection), gnollguard.com (blocks
automated requests, paginates hard) and eqprogression.com (returns 403 to
automated fetch, confirmed 8 Aug 2026). Do not retry these on a schedule. If
their content is needed, ask the human to fetch it by hand.

**Lookalike domains — do not cite.** `eqlegends.wiki`, `everquestlegends.wiki`,
`everquestlegends-wiki.wiki` and `everquest-legends-wiki.wiki` rank highly and
look authoritative. They carry no bylines, no edit history and no citations, and
they reference "developer updates" without linking any. Tier 5 at best. They will
keep surfacing in searches; skip them.

**Patch notes live at two addresses.** The full list is at
`everquestlegends.com/patch-notes`, which is JS-rendered; `/news` is a separate,
shorter feed and lags behind. Check the former. As of 8 Aug 2026 the complete set
is 7-7, 7-14, 7-28, 7-29 and 8-4 — probing intermediate dates returns redirects
to `/home`, so gaps in that sequence are real rather than missed.

**Some hotfixes are Discord-only.** A 5 Aug 2026 hotfix was never posted to the
website; eqlwiki transcribed it. Tier 1 in origin, tier 2 as received — badge it
accordingly and say where it came from.

---

## What to do when a page changes

1. **Get the diff, not the page.** MediaWiki gives you both at once:
   `?title=PAGE&diff=cur&oldid=<the revid you last saw>` returns the changes
   *and* the full current text in a single request.
2. **Classify it.**
   - **Green** — a single-source factual field with no interpretation: a ZEM
     value, a respawn timer, a level band, a coordinate, an item stat.
   - **Red** — everything else: new prose, a new named mob, a changed mechanic,
     a conflict with an existing claim, or anything touching a flagged gap.
3. **Green** may be applied directly. State old and new value in the proposal.
4. **Red** must be written up with reasoning, not applied silently. If it
   contradicts something already published, say which claim, where it is, which
   source you are trusting, and why.
5. **Both go in the same pull request.** The human merges. Nothing publishes
   without that.

---

## A tier 5 page worth naming in public

eqlwiki's **Per-Level Hunting Guide** is one of the most-linked pages on the wiki
and is a Project 1999 import. It cites P1999 forums, carries the phrase "As of
June 2020", and repeats the P99-specific claim that characters "generally perform
like characters three or more levels higher" - a statement about a single-class
server at fixed difficulty. It predates both multiclass and D0-D4, so it is wrong
in both directions for Legends.

Publishing that finding costs nothing and is exactly what the tier scale is for.

---

## The stale-revision trap

**A wiki fetch can silently return an old revision.** This has happened in this
project more than once and it is the most dangerous failure mode available,
because it looks exactly like success.

Always compare the `oldid` in the fetched page footer against the current
revision id from the API. If they differ you were served a cache. Re-request
with `diff=cur&oldid=<what you got>`.

A fetch has also returned an entirely **empty** page while reporting success. If
a page comes back with no content, treat it as a failed fetch, not as a page
with nothing on it. The Hole's plate was once built from an empty fetch and had
to be rebuilt from scratch.

---

## Tier C — a first-hand report, not yet an instrument reading

Added 10 August 2026. The scale ran M, 1, 2, 3, 4, 5, and a named player saying
*"I did this last night and it did not work the way the wiki says"* fits none of
them. It is not Tier M: nothing was parsed, and recollection is not a log. It is
not tiers 3 to 5: those are readings of documents, and this is not a document.

**Tier C sits below M and above 3.** First-hand, named, dated, unconfirmed.

Every Tier C claim publishes four things:

1. **Who reported it**, by name. Credit is the whole point — it is the only
   currency we have for the people who find these.
2. **When**, and under what conditions they saw it.
3. **What would confirm it** — usually one log line or one screenshot.
4. **That it is unconfirmed**, in a badge, wherever the claim appears.

**A Tier C claim never becomes fact by repetition.** It either gets confirmed
and moves tier, with the confirming evidence named, or it stays C indefinitely
and visibly. Watch for the failure mode where a C claim is cited so often that
someone quietly drops the badge.

**This applies to us too.** The collaborator's own play reports are Tier C, not
Tier M. Our logs are Tier M because a parser read them; our memories are not.
Exempting ourselves would be the most obvious way to corrupt the scale.

---

## Verification standard

A zone counts as **verified** only when all three are true:

1. Its wiki page was fetched in full, and its roster re-compared against the plate.
2. **Its edit history was fetched** — not just the footer date.
3. **Every coordinate lands on drawn floor** — within 120 units of the walkable
   geometry extracted from the game's own mesh files, checked by
   `_build/build6.py` at build time and counted rather than typed.

Anything short of that is `partial`, and which gate is open is recorded on the
plate. Do not upgrade a zone's status without doing all three.

### Gate 3 used to say something else, and it could not be done

Until 9 August 2026 gate 3 read *"coordinates were re-derived and
collision-checked against the room list"*. **There is no room list to check
against.** Measured 9 Aug 2026:

- Rooms are named 46 times across 8 of the 10 plates, and **25 of 209 named mobs
  have a room in their note** — so room knowledge exists.
- **Exactly one room anywhere carries a coordinate** — Splitpaw's safe room, at
  1150, −180. It is a single point, not an extent.
- **No room anywhere carries a boundary.** Every other room mention attaches a
  room *name* to a *mob's* coordinate, which is the opposite of what a collision
  check needs.

A collision test needs room extents to test against. Nothing in the project has
one, so the gate could not be failed, passed, or attempted — and five zones were
held at `partial` waiting on it. That read as *work remains* when the honest
statement was *this test does not fit the data we hold*.

The geometry check replaces it, by the owner's decision on 9 August 2026.
**It is stronger in one direction and weaker in another, and the difference is
worth keeping in mind:**

- **Stronger.** It proves a coordinate is somewhere a player can actually stand
  inside that zone, which a room-list comparison cannot. It is how the six
  impossible Najena coordinates were found and withheld.
- **Weaker.** It does not prove a coordinate matches the room its note names. A
  mob recorded in "Room 7" whose coordinate sits on solid floor in Room 3 passes
  this and would have failed the old gate.

**176 of 176 plotted positions across the ten zones land on drawn floor.** Two
independent things have to be right for a point to land close — the recorded
coordinate and the extracted geometry — so the check tests both at once.

**What the old gate was reaching for is not lost.** Where a plate has enough
room knowledge, the qualitative version of the check is already being done and
is worth repeating: Mistmoore and The Warrens both verify their transforms by
showing that mobs whose coordinates land together are documented as sharing a
room — six such pairs in The Warrens, three independent agreements in Mistmoore.
That is a room check without a room list, and it is the strongest corroboration
available short of surveying the rooms themselves.

If room extents are ever derived from the zone geometry — the meshes that give
us the floors could in principle give us the walls — the original comparison
becomes possible and should return as a fourth gate.
