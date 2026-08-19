"""search.html — one box that searches the whole site.

WHY
---
721 pages, and the only search was The Index, which searches items and named
mobs. You could not find "Screaming Terror", "charm cap", "mote", "voidling" or
"backstab" anywhere on this site, including on the pages that explain it.

WHAT IT INDEXES, AND WHAT IT LEAVES OUT
---------------------------------------
Every published page except the 671 item and named-mob pages, which The Index
already covers far better - it filters by class, slot and zone, and this cannot.
Sending someone to a generic text search for an item when a purpose-built filter
exists would be a worse answer, so the two are kept apart and each says so.

That leaves roughly fifty pages: surveys, raids, tools, Learn, Accuracy, the
change log, credits. The index carries each page's title, its section headings
and a trimmed body, which is enough to find a concept rather than an item.

WHY IT IS NOT A LIBRARY
-----------------------
No stemming, no fuzzy matching, no ranking model. Terms are matched as
substrings, scored by where they hit - title beats heading beats body - and the
whole index is about 120KB, which is smaller than one of the survey pages it
searches. A dependency would cost more than it returns at this size.
"""
import os, re, sys, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, '_build'))
from _partials import head, bar, foot

# public/app/ holds the Sky Ledger browser build verbatim — a 176 KB
# application, not a page of ours. Indexing it would put its whole UI into the
# site search under a hashed URL that changes with every release.
SKIP_DIRS = ('public/items/', 'public/named/', 'public/app/')
SKIP_FILES = {'public/404.html', 'public/search.html'}
STRIP = re.compile(r'<(script|style|svg)\b.*?</\1>', re.S | re.I)


def text_of(h):
    h = STRIP.sub(' ', h)
    h = re.sub(r'<footer\b.*?</footer>', ' ', h, flags=re.S | re.I)
    h = re.sub(r'<header class="site-bar".*?</header>', ' ', h, flags=re.S | re.I)
    h = re.sub(r'<div class="ns-bar".*?</div>', ' ', h, flags=re.S | re.I)
    t = re.sub(r'<[^>]+>', ' ', h)
    t = re.sub(r'&[a-z]+;', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()


# Matching runs against a deduplicated token blob rather than the snippet body.
# The first version indexed 1,400 characters per page and could not find
# "Screaming Terror" — which is the exact term the audit named as unfindable,
# on a site that documents it. Whole-page tokens cost 121KB and fix it.
STOP = set(
    "the a an and or of to in on for with is are was were be been it its this that "
    "as at by from not no you your we our they their he she his her but if then "
    "than so such can will would could should may might have has had do does did "
    "one two three all any each every more most other some what which who when "
    "where how why here there them these those into out up down over under only "
    "also just now still yet both either neither because while about after before".split())


def tokens(t):
    return sorted({w for w in re.findall(r"[a-z][a-z0-9'`-]{2,}", t.lower())
                   if w not in STOP})


def build():
    docs = []
    for p in sorted(glob.glob('public/**/*.html', recursive=True)):
        key = p.replace(os.sep, '/')
        if key in SKIP_FILES or any(key.startswith(d) for d in SKIP_DIRS):
            continue
        h = open(p, encoding='utf-8', errors='replace').read()
        title = re.search(r'<title>(.*?)</title>', h, re.S)
        title = re.sub(r'\s*&mdash;.*$|\s*—.*$', '', title.group(1)).strip() if title else key
        heads = [re.sub(r'<[^>]+>', ' ', m).strip()
                 for m in re.findall(r'<h[23][^>]*>(.*?)</h[23]>', h, re.S)]
        heads = [re.sub(r'\s+', ' ', x) for x in heads if x.strip()]
        desc = re.search(r'<meta name="description" content="([^"]*)"', h)
        body = text_of(h)
        docs.append({
            'u': key.replace('public/', ''),
            't': title,
            'h': heads[:24],
            'd': (desc.group(1) if desc else '')[:180],
            'b': body[:1400],
            'k': ' '.join(tokens(body)),
        })
    return docs


DOCS = build()

CSS = '''<style>
.sf{width:100%;font-family:"IBM Plex Mono",monospace;font-size:17px;padding:15px 17px;
  background:var(--panel2);border:1px solid var(--rule2);color:var(--bone);margin-top:var(--s-5)}
.sf:focus{outline:2px solid var(--bone);outline-offset:-1px}
.sf::placeholder{color:var(--dim);opacity:1}
.scount{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--faint);margin:var(--s-4) 0 0}
.sres{list-style:none;margin:var(--s-4) 0 0;padding:0;display:grid;gap:1px;
  background:var(--rule);border:1px solid var(--rule);border-radius:var(--r);overflow:hidden}
.sres li{background:var(--panel)}
.sres a{display:block;padding:15px 18px;text-decoration:none}
.sres a:hover{background:var(--panel2)}
.sres .st{font-family:"Saira Condensed",sans-serif;font-size:19px;font-weight:600;
  color:var(--bone);display:block}
.sres .su{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.1em;
  color:var(--faint);display:block;margin-top:2px}
.sres .sx{display:block;margin-top:6px;color:var(--dim);font-size:14px;line-height:1.55}
.sres mark{background:rgba(230,233,228,.22);color:var(--bone);padding:0 2px}
.sempty{border:1px dashed var(--rule);padding:30px;text-align:center;color:var(--mut);
  margin-top:var(--s-5)}
</style>'''

BODY = f'''
<main id="main">
<section class="hero page">
  <div class="shell">
    <p class="crumb"><a href="index.html">EQL Source</a> &nbsp;/&nbsp; Search</p>
    <h1 class="display">Search<br><em>everything else.</em></h1>
    <p class="hero-lede">Surveys, raid guides, tools, explainers and the change log &mdash;
      {len(DOCS)} pages. Looking for an item or a named mob?
      <a href="tools/index-search.html">The Index</a> does that properly, with filters for class,
      slot and zone.</p>
    <input class="sf" id="q" type="search" autocomplete="off" spellcheck="false"
      placeholder="Screaming Terror, voidling, mote, backstab, placeholder&hellip;">
    <p class="scount" id="c"></p>
  </div>
</section>
<div class="shell"><ul class="sres" id="r"></ul><div id="e"></div></div>
</main>
'''

SCRIPT = ('<script>window.__S__=' + json.dumps(DOCS, separators=(',', ':')) + ';</script>'
          + '''<script>
(function(){
  var D=window.__S__, q=document.getElementById('q'), R=document.getElementById('r'),
      C=document.getElementById('c'), E=document.getElementById('e');
  function esc(s){return String(s).replace(/[&<>"]/g,function(m){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]})}
  function mark(s,terms){
    s=esc(s);
    terms.forEach(function(t){
      if(!t)return;
      s=s.replace(new RegExp('('+t.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&')+')','ig'),'<mark>$1</mark>');
    });
    return s;
  }
  function snippet(d,terms){
    var b=d.b, low=b.toLowerCase(), at=-1;
    for(var i=0;i<terms.length&&at<0;i++) at=low.indexOf(terms[i]);
    if(at<0) return d.d||b.slice(0,150);
    var s=Math.max(0,at-70);
    return (s?'…':'')+b.slice(s,s+190)+'…';
  }
  function run(){
    var raw=q.value.trim().toLowerCase();
    if(raw.length<2){ R.innerHTML=''; E.innerHTML=''; C.textContent=''; return; }
    var terms=raw.split(/\\s+/);
    var hits=[];
    D.forEach(function(d){
      var t=d.t.toLowerCase(), hs=d.h.join(' ').toLowerCase(), b=(d.k||d.b).toLowerCase(),
          dd=(d.d||'').toLowerCase(), score=0, all=true;
      terms.forEach(function(x){
        var s=0;
        if(t.indexOf(x)>-1) s+=60;
        if(hs.indexOf(x)>-1) s+=25;
        if(dd.indexOf(x)>-1) s+=12;
        if(b.indexOf(x)>-1) s+=6;
        if(!s) all=false; else score+=s;
      });
      if(all&&score) hits.push({d:d,s:score});
    });
    hits.sort(function(a,b){return b.s-a.s||a.d.t.localeCompare(b.d.t)});
    C.textContent=hits.length+' page'+(hits.length===1?'':'s');
    E.innerHTML = hits.length ? '' :
      '<div class="sempty">Nothing matches. Items and named mobs live in '+
      '<a href="tools/index-search.html">The Index</a>.</div>';
    R.innerHTML=hits.slice(0,40).map(function(h){
      return '<li><a href="'+h.d.u+'"><span class="st">'+mark(h.d.t,terms)+'</span>'+
             '<span class="su">'+esc(h.d.u)+'</span>'+
             '<span class="sx">'+mark(snippet(h.d,terms),terms)+'</span></a></li>';
    }).join('');
  }
  var t; q.addEventListener('input',function(){clearTimeout(t);t=setTimeout(run,110)});
  // arriving with ?q= or #q runs the search immediately, so a link can carry one
  var pre=(location.search.match(/[?&]q=([^&]*)/)||[])[1]||location.hash.slice(1);
  if(pre){ q.value=decodeURIComponent(pre.replace(/\\+/g,' ')); run(); }
  q.focus();
})();
</script>''')

page = (head("Search", f"Search {len(DOCS)} pages of EverQuest Legends surveys, raid guides, "
                       f"explainers and change log. Items and named mobs have their own index.",
             rel="", extra=CSS, og="home", canon="search")
        + bar("") + BODY + foot("").replace('</body>', SCRIPT + '\n</body>'))

open('public/search.html', 'w', encoding='utf-8', newline='\n').write(page)
kb = len(json.dumps(DOCS, separators=(',', ':'))) / 1024
print(f"search.html written: {len(DOCS)} pages indexed, {kb:.0f} KB index")
