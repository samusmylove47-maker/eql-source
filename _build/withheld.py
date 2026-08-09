"""Coordinates we hold but will not publish as positions, and why.

WHY THIS MODULE EXISTS
On 8 August 2026 six Najena coordinates were found sitting 57 to 513 units
outside the zone's own drawn floor. They were withheld from the survey plot and
the reason was written up in the change log — and then they carried on printing
as bare coordinates in the named roster on the plate, which is the table a
reader actually navigates by. The withholding existed in the change log and in
the plot. It did not exist where the reader was.

So the set lives here, one place, and:

  - _build/build6.py skips these when plotting,
  - _build/build3.py rewrites their coordinate cells as the plate is built,
  - scripts/check.py fails the build if a withheld coordinate reaches a page.

A withheld coordinate is not deleted. The mob keeps its row, its level, its
class and its notes; only the position is replaced, by a statement that we do
not have one we trust. Deleting the row would be the dishonest version.
"""

# (zone slug, mob name as it appears on the plate)
WITHHELD = {
    ('najena', 'Rathyl'),
    ('najena', 'Ekeros'),
    ('najena', 'BoneCracker'),
    ('najena', 'Officer Grush'),
    ('najena', 'Trazdon'),
    ('najena', 'A Visiting Priestess'),
}

# One reason per zone, printed under the table it affects.
REASON = {
    'najena': (
        'Six coordinates on this plate are withheld. Every recorded position on the '
        'site is checked against the walkable floor extracted from the game’s own '
        'mesh files, and these six land 57 to 513 units outside it — outside the '
        'zone, not merely off a walkway. The mobs are real and the rest of their '
        'records stand; the positions are not ones we are willing to send anyone to. '
        'A <code>/loc</code> reading taken standing on any of them would close this.'),
}

# What replaces the coordinate in a roster cell.
MARK = '<span class="wh">withheld</span>'
