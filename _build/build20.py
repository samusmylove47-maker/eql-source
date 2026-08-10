"""credits.html — everyone who gave us something, in one place.

WHY THIS IS THE ONLY PLACE NAMES APPEAR
---------------------------------------
Findings used to be credited inline, so a survey read "Skyfox, 18 June 2026"
in the middle of a sentence about loot. That is worse for everyone. It clutters
the page, it buries the thanks where only a reader of that one paragraph sees
it, and it gives a creator no link back.

So: claims carry what a reader needs to weigh them — the kind of source, the
date, and the tier badge — and the person is named here, once, with a link to
their work where they have one. A creator who tells us something gets traffic
back as thanks, which a name in a paragraph never did.

Wiki editor usernames are a separate thing and stay inline. Those are
bibliographic — "revision 158182, editor Mazirian, 16 July" is how a reader
checks the claim themselves, and stripping the name would break the provenance
test that CLAUDE.md runs on every wiki page. They are citations, not credits.
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

# name, link (or None), what they gave us. One line each, newest first-ish.
PEOPLE = [
    ("Cavepig", "https://www.reddit.com/r/EQLegends/comments/1vg8x7l/cavepigs_guide_to_enchanting_in_sky_how_to_key/",
     "Keying and speed-clearing the Plane of Sky. The Key Master, the Overseer of Air, "
     "and the island count our own page was short of."),
    ("Skyfox", None,
     "The planar loot guide that showed the class-group split was gone, and that haunted "
     "chests and phoboplasms drop the two shared sets."),
    ("Annalise", None,
     "Blunt and slashing weapons underwater in Kedge Keep. The Fiery Avenger completed as a "
     "non-paladin. Raid lockouts running per difficulty."),
    ("BarakDur", None,
     "The idea behind the planar gear tool &mdash; comparing all three of a trio&rsquo;s class "
     "sets at once instead of one."),
    ("Classic XP", "https://www.youtube.com/watch?v=92F07fPPBlI",
     "Farming Lustrous Russet in the Plane of Hate, and the rooftop route across the city that "
     "sent us looking for a rooftop layer in the mesh."),
    ("BrutallStatic", "https://www.youtube.com/watch?v=dUWk-kYubKU",
     "Every voidling location, and the confirmation that raid bosses live only in raid "
     "instances."),
    ("Avenrae and Shara", None,
     "The combat logs behind every measured figure on this site."),
]

CSS = '''<style>
.cr{list-style:none;margin:var(--s-6) 0 0;padding:0;display:grid;gap:1px;
  background:var(--rule);border:1px solid var(--rule);border-radius:var(--r);overflow:hidden}
.cr li{background:var(--panel);padding:15px 18px;display:grid;
  grid-template-columns:minmax(0,180px) minmax(0,1fr);gap:6px 22px;align-items:baseline}
.cr .who{font-family:"Saira Condensed",sans-serif;font-size:19px;font-weight:600;
  color:var(--bone);letter-spacing:.02em}
.cr .who a{color:var(--bone);text-decoration:none;border-bottom:1px solid var(--rule2)}
.cr .who a:hover{border-bottom-color:var(--bone)}
.cr .gave{color:var(--dim);font-size:14.5px;line-height:1.6}
.cr .ext{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--faint);display:block;margin-top:3px}
@media(max-width:620px){.cr li{grid-template-columns:1fr}}
</style>'''

rows = "\n".join(
    f'''      <li><span class="who">{
        f'<a href="{url}" rel="noopener">{name}</a><span class="ext">Their work &rarr;</span>'
        if url else name}</span>
        <span class="gave">{gave}</span></li>''' for name, url, gave in PEOPLE)

page = (head("Credits",
             "The players and creators whose findings corrected this site, and where to find "
             "their own work.", rel="", extra=CSS, og="home", canon="credits")
        + bar("") + f'''
<main>
<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="index.html">EQL Source</a> &nbsp;/&nbsp; Credits</p>
    <h1 class="display">People who<br><em>told us things.</em></h1>
    <p class="hero-lede">Almost everything on this site that is genuinely about EverQuest Legends,
      rather than inherited from a wiki that predates it, came from a player who went and looked.
      Several of these findings corrected pages we had already published.</p>
  </div>
</section>

<section class="band" style="border-top:0;padding-top:0">
  <div class="shell">
    <ul class="cr">
{rows}
    </ul>
    <p class="lede" style="margin-top:var(--s-6)">If you found something here that is wrong, or
      something the wiki has wrong, that is the most useful thing anyone can send us.
      <a href="https://github.com/samusmylove47-maker/eql-source/issues/new?template=finding.yml">Send
      a finding</a> and you will end up on this page.
      Please do not attach a combat log to a public issue &mdash; they can carry private chat. Say
      you have one and we will ask.</p>
  </div>
</section>
</main>
''' + foot(""))

open('public/credits.html', 'w', encoding='utf-8', newline='\n').write(page)
print(f"credits.html written: {len(PEOPLE)} contributors, "
      f"{sum(1 for _, u, _ in PEOPLE if u)} linked")
