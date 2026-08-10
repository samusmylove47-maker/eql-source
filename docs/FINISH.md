# The plan to finish

Written 10 August 2026. The question this answers is not "what could we build"
but **"what is between here and people using it"**, and the answer is shorter
than the backlog suggests.

---

## The honest starting position

**The site works.** Ten surveys, five tools, a raid model, a register, a
sourcing standard, a build that refuses eight classes of fault. It is accurate
and it is usable today.

**Two things stop it being used.** Nobody can find it, and nothing brings anyone
back. Everything below is aimed at those two, in that order. Anything that
serves neither is cut, however good it is.

---

## Phase 1 — Arrival · half a day

Nothing here is clever. All of it is the difference between a link that works
and a link nobody clicks.

| | Why | Size |
|---|---|---|
| **OG images**, one per page type | 0 of 33 pages have one. EQ communities live in Discord, and a link with no card is a link nobody opens. Generated from page data — zone name, level band, respawn — so they cannot go stale | 2h |
| **Canonical tags** | 0 of 33. Every internal link is `.html` and 301s to the extensionless path, so every page has two URLs and search engines pick | 1h |
| **Drop `.html` from internal links** | Same fault, other half. 33 of 33 pages | 30m |
| **`twitter:card`** | Rides along with the OG work | 15m |

**Done when:** a survey link pasted into Discord shows a card with the zone
name, level band and verification state.

## Phase 2 — The reason to come back · three to four days

This is the differentiator and it is one build, not two. The character sheet is
the data layer; the route planner is the thing people arrive for.

### 2a. The unified character sheet · 1 day

One sheet, one URL fragment, replacing three separate tracker save-states.
Holds: trio and levels, race unlocks, Plane of Sky quest progress, faction
standings we can derive, epic progress.

- **Zero hosting cost, zero accounts.** The existing trackers already do this —
  a compressed bitfield in the hash, never sent to a server. A unified sheet is
  roughly 400–600 bits, about 140 characters of URL.
- Plus a **downloadable JSON** for anyone who does not trust a bookmark, and
  `localStorage` for day to day, both of which already exist per tool.
- **Do not build a database.** It would cost money, create a privacy surface,
  and contradict the site's own promise of no account and nothing transmitted —
  which is a real differentiator against every site that wants a sign-up.

### 2b. The route planner — **built, then cut, 10 August 2026**

It worked and it was still wrong, and the reason is worth keeping.

Ranking zones by level band and experience modifier is deterministic, and the
three highest-modifier zones happen to tile levels 4 to 50 between them. So
**every trio, from every starting level, got the same three stops**: The
Warrens, Lair of the Splitpaw, The Hole. Adding "what else is open" alongside
each window made it honest but did not make it different.

The only way to make the output vary usefully is to encode nuance the data does
not hold — which class combinations struggle where, what is worth a detour for
whom, where a band is survivable in practice. **None of that can be derived;
all of it would be hand-tuned, and hand-tuning is the collaborator's hours.**

That is the test this project should apply to any tool: *does making it good
cost the human time on an ongoing basis?* If yes, it is the wrong tool however
well it is built. Automation that needs constant human correction is not
automation.

**Do not rebuild it** without new data that makes the output genuinely differ by
trio — measured kill rates per class combination, or per-class difficulty
ratings per zone. Neither exists today.

What survived: the item class-data correction the build exposed. 160 of 452
items had no usable class list and the parser was defaulting unreadable cells to
"every class". That fix stands on its own.

## Phase 3 — The long tail · 2 days

**661 item and named-mob pages** — `/items/journeymans-boots`, `/named/drelzna`
— generated from `index-data.json`, cross-linked to their survey, with the
client-side search kept on top.

This is the single highest-leverage reach change available: it creates 661
crawlable URLs where there are currently zero, and eqlwiki wins every long-tail
item search today purely because it has a page per item and we do not.

Deliberately after Phase 2, because a route planner over ten sharp surveys is a
product and 661 thin item pages are not.

---

## Cut, and why

Each of these is defensible work. None of them gets someone using the site
sooner, so none of them happens before Phase 3 is done.

- **Discord bot and Worker.** The GitHub issue form already gives inbound a
  door. The bot is convenience on a channel that has almost no traffic yet.
- **Provenance dashboards** — staleness tracker, contradiction registry,
  automated import detection. Genuinely our best long-term position, and it
  serves nobody until there is an audience to serve.
- **Log ingestion as a browser tool.** Changes the growth curve, costs a week.
  After there is growth to change.
- **Five missing navigation maps.** The geometry floor plans replaced their job.
  This backlog item predates the retirement and should be struck.
- **More raid encounters.** One good 3D model is enough to prove the format.
- **Compressing Accuracy further.** It is 8,561 words and it is the designated
  home for exactly this material. Shrinking it further means deciding which
  caveats have expired, which is judgement work, not editing.

---

## Stale entries to strike while passing

- `docs/BACKLOG.md` **P4 — Five missing navigation maps.** Superseded.
- `CLAUDE.md` known gaps: **Placeholder removals** — settled 10 Aug by the
  developer patch note.
- `CLAUDE.md` known gaps: **Navigation maps** — reframed, the plates it refers
  to no longer exist.

---

## Sequence and what it needs from the collaborator

| Phase | Days | Needs |
|---|---|---|
| 1 Arrival | 0.5 | Nothing |
| 2a Character sheet | 1 | Nothing |
| 2b Route planner | 2–3 | A sanity read on one generated route before the other nine |
| 3 Long tail | 2 | Nothing |

**About a week of working days, four pull requests.** Nothing in it is blocked
on anything outside the repository.

The one thing that would genuinely accelerate the result is play data for zones
we have not measured, because the route planner is only as good as the surveys
underneath it. That is not on the critical path — it makes the same product
better rather than making it arrive sooner.
