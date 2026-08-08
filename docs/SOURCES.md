# Sources and watchlist

The pages the automation checks twice a day, why each matters, and what to do
when one changes.

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
| Blackburrow | Plate 05 | Plate is missing its reading key |
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

## Verification standard

A zone counts as **verified** only when all three are true:

1. Its wiki page was fetched in full.
2. **Its edit history was fetched** — not just the footer date.
3. Its coordinates were re-derived and collision-checked against the room list.

Anything short of that is `partial`, and which gate is open is recorded on the
plate. Do not upgrade a zone's status without doing all three.
