# Cutting the text, and the ruling on generated maps

Two guildmates tried the site and both said the same thing: too much text, too
many paragraphs, not enough shown. That is the most useful feedback the project
has had, and it is correct. This is the plan, and the ruling on the alternative
that was proposed alongside it.

---

## 1. Ruling: we do not publish generated maps. We extract real ones.

Four AI-generated maps of the Temple of Cazic-Thule were put forward as a model
for what the site could look like. **The instinct behind them is right and the
artefact is not**, and it took one command to show why, because we already own
the tool that settles it.

The generated map prints the Avatar of Fear's position twice, as
`approx 1085, 590, -98`, beside a scale bar and a compass rose. We read the
zone's own mesh out of `cazicthule.s3d`:

| | |
|---|---|
| Zone extent, all geometry | X −112..1392, Y −597..875, Z −305..168 |
| Claimed position | Y **1085**, X 590, Z −98 |
| Distance to nearest walkable floor | **476 units** |
| Distance to nearest geometry of any kind | **458 units** |
| Y extent overshoot | **210 units outside the zone entirely** |

That coordinate does not point at the wrong room. It points at empty space
beyond the edge of the zone. Everything else on the image — the maze, the two
pyramids, the pond network, the plank crossings, the four guard positions, the
"1 square = 10 meters" scale — carries exactly the same amount of evidence,
which is none. It is a picture of what an EverQuest dungeon map looks like.

Three further problems, each fatal on its own:

1. **It is titled "EverQuest Classic Map."** Publishing it would import classic
   layout into a Legends site, which is the single thing this project exists to
   fight.
2. **A generated image cannot be sourced, dated, corrected or tiered.** Every
   other claim we publish names where it came from. An image makes several
   hundred spatial claims at once and can cite none of them.
3. **It reads as authoritative to exactly the reader it misleads.** Someone who
   already knows the zone recognises it and thinks "close enough". Someone who
   does not know the zone is the person the guide is for, and they cannot tell
   the invented parts from the real ones. That is backwards.

**We do not need to imagine these maps. We can read them.** `cazicthule.s3d` is
on the disk. Thirty seconds of extraction gives 29,320 triangles, 6,673 walkable,
and four separated elevation bands — the real thing, with the storeys already
apart. Anything we would have asked an image model to draw, we can derive.

### Where generated imagery could still be used, and why we are not

Purely decorative headers carry no factual claims, so the accuracy objection
does not apply. We are still not doing it: the design direction is to strip the
signs the site was AI-built, and the chrome is deliberately monochrome with all
colour coming from the material. Decorative AI art fights both.

---

## 2. Where the words actually are

The complaint was "too many paragraphs". The measurement says otherwise, and the
difference matters because it changes what to cut.

**13 surveys, 34,812 words.**

| Where | Words |
|---|---|
| Inside tables | 15,928 |
| Inside paragraphs | ~9,100 |
| Inside list items | ~3,400 |

Tables hold nearly half the text. **Our tables are prose wearing a table's
clothes** — the roster's notes column is a paragraph per mob, 671 of them. The
median notes cell is a healthy 4 words; the mean is 8, dragged up by a long
tail, and the six worst cells are 40 to 76 words each.

Four of the six worst are on the three surveys written this week. Those are
mine, and they are the clearest example of the problem: a raid boss row carrying
a 76-word essay about hit points instead of a figure and a badge.

A 30% cut is **10,443 words**. It does not come from deleting facts.

---

## 3. The plan

### Phase A — stop saying the same thing on every page

The provenance explanation — what an import is, why the boss pages are classic
text, what the tier badges mean — is written out on Plane of Fear, Plane of Hate
and Kedge Keep in three near-identical passes. That is one explanation printed
three times, and it will be printed thirteen times if we keep going.

It moves to one page under `learn/`, and each survey keeps a single sentence and
a link. **Largest single win, deletes no facts.**

### Phase B — replace words with structure

1. **An icon vocabulary for the roster.** Sees invis, summons, undead, caster,
   backstab, see-through-invis-undead. Six glyphs replace the recurring phrases
   in 671 notes cells, leaving the notes column for what is genuinely unique to
   that mob.
2. **An elevation strip per zone.** A side view of the storeys with their z
   ranges and the descent marked. Vertical structure is the hardest thing to
   write and the easiest thing to draw, and the one panel of the generated set
   that was genuinely well judged was its Z-drop diagram. We can draw that from
   real band data.
3. **Step lists instead of route paragraphs.** Three-word imperative steps
   beside the plan, not a paragraph describing them.
4. **Facts into columns.** A boss row gets Level, AC, HP, Tier as columns with
   badges, and the notes cell keeps only the sentence that is actually about
   that boss.

### Phase C — the honest version of what the generated map was reaching for

The images drew a *path*. Our floor plan draws floor and points, and the
existing route feature draws straight lines between named mobs while disclaiming
at length that it knows nothing about walls.

We have the walkable floor as triangles. Triangles that share an edge are
adjacent. **That is a graph, and A\* over it produces a real path that stays on
real floor.** It would be derived from the game's own geometry, checkable the
same way every coordinate on this site is checked, and it is exactly the thing
the generated image was faking.

Bigger and riskier than A and B. Scoped last, and only after the cut lands.

---

## 4. The rule this produces

**Show geometry, say meaning.**

A picture earns its place when it carries spatial or numeric structure — where a
thing is, how far, how deep, in what order. Prose earns its place when it
carries judgement — what is disputed, what is unsourced, what changed and who
says so. The site has been using paragraphs for both, and paragraphs are only
good at the second.
