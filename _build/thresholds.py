"""Numbers a check enforces AND a page states, in one place.

WHY THIS EXISTS
---------------
`ON_FLOOR` decides gate 3: a recorded coordinate counts as landing on drawn
floor if it sits within this many world units of a floor edge extracted from
the game's own mesh files. `_build/build6.py` enforces it.

Three pages also STATE it, in prose, as a literal:

  - dungeons/index.html  "within 120 units of geometry extracted from the
                          game's own mesh files"
  - the dormant "all gates cleared" copy in build1.py, which will publish on
    the day the last gate clears and has never been rendered since
  - the withheld-coordinate note, indirectly, by describing what the check did

Until 6 September 2026 the number the build ENFORCED and the number the pages
STATED were independent literals in separate files. Nothing compared them, and
the failure is silent in the direction that matters: loosen the constant and
every page carries on advertising the old, stricter promise. A reader has no
way to tell, and neither did check.py.

This is the same shape as the prose-versus-data faults `scripts/gate.py` exists
for, with one difference that is why it is fixed here instead of there: a gate
can only catch a disagreement between two things that both already exist. A
single shared constant means there is no second copy to disagree.

WHY NOT IMPORT IT FROM build6
-----------------------------
Importing a generator runs it. CLAUDE.md records an agent doing exactly that to
`raidstats.py` "read-only" and truncating a committed dataset to 0 bytes. A
constant lives in a module with no side effects, or it does not get shared.
"""

# World units. A mob this close to drawn floor is on the map.
#
# Gate 3 asked for a collision check against a room list that does not exist
# until 9 Aug 2026; this replaced it. docs/SOURCES.md carries the reasoning and
# what the new gate is weaker at. Changing this number changes what "verified"
# means on the home page, the dungeon index and every survey - which is the
# whole reason it is not typed in four places any more.
ON_FLOOR = 120
