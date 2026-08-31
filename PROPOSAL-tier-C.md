# Proposal: tier C, client-mined — replacement text for CLAUDE.md section 2

**FOR ADOPTION. Proposal only — nobody pushes this.** `CLAUDE.md` lives in
`eql-source`, which is a peer to the Director. **The owner merges, and merging is
what publishes.**

**This row is defensible even if bulk import is declined forever.** It describes
what the project already does. It does not license doing more of it.

---

## The hole, stated as a measurement

**The hierarchy does not describe our own practice.**

`_build/geometry.py` reads the game's own `.s3d` meshes and **used them to
falsify six hand-plotted Najena coordinates.** We let mined data overturn a
published claim. **That is tier-1 behaviour by a source the hierarchy does not
list.**

And it is already recorded in the idiom a tier would use. `assets/sky-islands.json`
carries, today, at its top level:

```json
"source": "airplane.s3d",
"read":   "2026-08-11"
```

**A named source and a read-date. That is a provenance record with no tier
attached to it.** The row below does not invent a practice; it names one.

---

## 1. Where it sits, and the ordering defended rather than asserted

**Insert between M and 1.** But a single linear slot misdescribes the
relationship, so the text says what it actually asserts against tier 1:

> **Client-mined outranks official patch notes for what the game CURRENTLY
> CONTAINS. Patch notes outrank client-mined for WHAT CHANGED AND WHY.**

They are authoritative about different things and neither is a superset:

| | authoritative for | blind to |
|---|---|---|
| **Tier 1, patch notes** | intent, change, dates, the reason a thing moved | what actually shipped — notes are written before release and can be imprecise (*"improved loot tables"*) or silent (the 28 July note lowered respawn maximums **without publishing figures**) |
| **Tier C, client-mined** | the shipped state of a table, mesh or asset, exactly | why anything is the way it is, and everything not in a file we can read |

**The tie-break is the date, not the tier**, and this is the part that must be in
the text or the ordering is meaningless:

> **A client read supersedes any patch note published before that read. A patch
> note published after the read invalidates the read.** Where the two disagree
> and the dates do not settle it, the claim is unresolved and the page says so.

**Why C is a letter and not a number.** `tier` is already overloaded across three
namespaces in `assets/`: source tier in `sky.json` (2, 4, 5), **difficulty D0–D4
in `raids-measured.json`**, and **mote tiers 1–10 in `motes.json`**. A new integer
would collide on sight. **M is already a letter for the same reason** — it names a
kind of source, not a rank in an integer field.

## 2. What qualifies, and the test that stops the badge becoming a fig leaf

**Qualifies:** data read directly out of files shipped by the game client —
`.s3d` archives, item and spell tables, zone meshes, textures, faction tables.
First-hand, structural, re-derivable.

**Does not qualify:** anything obtained from another site, database, export or
scrape, however well made.

> **THE TEST, and it goes in the text verbatim: CAN YOU RE-DERIVE IT FROM A
> SOURCE YOU HOLD?**
>
> Client files: yes — run the extractor again and get the same answer.
> Someone else's database: no. **There you are badging your confidence in THEIR
> pipeline, which is not a quantity this system measures**, and that is precisely
> the moment a badge becomes a fig leaf.

**A second-hand copy of client-mined data is tier 4**, like any other aggregator,
**no matter how certain you are that their extractor is correct.** The tier grades
the reading, not the bytes.

## 3. Staleness is the badge's one real weakness and must be a field

**Client-mined data is stale the moment the game patches**, and that is its only
genuine defect. It must be carried, not written around:

```json
"source":       "airplane.s3d",
"read":         "2026-08-11",
"read_against": "2026-07-28"
```

`read_against` is the patch the extraction was run against. **The page derives
"not re-checked since <patch>" from those fields.** It is never typed.

**This rests on a rule section 2 already holds:** *"Verified is derived and cannot
be typed."* **When that was enforced on the Sky data the verified class count fell
from eleven to five.** A tier C row whose staleness is a sentence beside the data
is the same fault at whatever scale it is applied.

**One field is missing today and this proposal exposes it rather than fixing it:**
`sky-islands.json` carries `source` and `read`; **`zone-geometry.json` carries
neither.** Two files produced by two extractors from the same archives, one with
provenance and one without. **Naming the tier is what makes that visible.**

## 4. What re-grading implies — checked, not assumed

**Nothing currently published changes tier, and I verified that rather than
assuming it.**

- **`zone-geometry.json` has no tier or source field at all.** Mesh-derived data
  is currently **ungraded, not mis-graded.** Adding the row grades something that
  had no grade, which cannot lower or raise a published claim.
- **`sky-islands.json` has `source` and `read` and no tier.** Same.
- **The survey plates carry no tier badges by deliberate decision**, recorded in
  section 2. That exception is untouched.
- **No page renders a tier badge on a geometry-derived claim**, because no
  geometry-derived claim carries a tier to render.

**So the honest answer to "what does this re-grade today" is: nothing.**

**And that answer is exactly the shape section 3 warns about** — *"It is true
today and it is the pattern section 3 forbids."* So it is stated as a measurement
with its date, not as a property: **checked 31 August 2026 against `origin/main`
`e6039020`. It stops being true the moment anything is imported.**

**What it does create is one piece of work, and the row should not pretend
otherwise:** `zone-geometry.json` needs `source` and `read` before anything on a
page can claim tier C for a floor plan. **Until it has them, floor plans are
ungraded — which is what they are today, honestly stated.**

## 5. What this does NOT license

**It does not license importing a rival's corpus, and that must be in the text
because the two arguments arrive together and are not the same act.**

- **EQLBase's 9,360 is, by its auditor's own addendum, largely classic-EverQuest
  baseline data imported wholesale**, of which an unpublished fraction has been
  confirmed in Legends. **Importing it is importing classic EverQuest**, which
  section 3's second hard rule forbids outright.
- **A competitor measured that cost on itself.** Gnoll Guard, 12 August 2026:
  502 items that exist in Legends missing entirely, 782 showing no stats when the
  real numbers were on hand, 186 showing stats that disagree with what the game
  reports.
- **It does not license shipping a drawing.** *"A drawing is an assertion"* stands
  unchanged. Tier C grades **where the walls are**. It says nothing about what
  happens in a room, and a badge on geometry does not license an encounter model
  of a fight nobody here has fought.

**And it does not decide whether client data gets imported at all.** That is a
separate decision, it belongs to the owner, and this row is correct whether the
answer is yes or never.

---

# The replacement text

*Insert as a new row after tier M, before tier 1, in section 2's list.*

> **0b. Client-mined — tier C.** Data read directly out of files shipped by the
> game client: `.s3d` archives, item and spell tables, zone meshes, textures.
> First-hand and structural, but not observed in play. **Outranks patch notes for
> what the game currently contains; patch notes outrank it for what changed and
> why.** The tie-break is the date — **a read supersedes any note published
> before it, and any note published after it invalidates the read.**
>
> **The test for what qualifies: can you re-derive it from a source you hold?**
> Run the extractor again and get the same answer. **A copy of someone else's
> extraction is tier 4**, however good their pipeline, because the tier grades the
> reading and not the bytes.
>
> **Every tier C claim carries `source`, `read` and `read_against`** — the file,
> the date it was read, and the patch it was read against. **The page derives
> "not re-checked since" from those fields and never states it in prose.** Client
> data is stale the moment the game patches; that is its one real weakness and
> the badge exists to carry it.
>
> **Tier C prints a badge** — `<span class="tier tC">C</span>` — wherever the
> claim appears. It is below tier 2's bare-printing threshold **because its
> staleness is unbounded between reads**, which is a different risk from being
> wrong and is the one a reader needs told.
>
> **Tier C does not license importing another site's corpus.** That is tier 4 at
> best and classic EverQuest at worst, and the second is forbidden outright.
