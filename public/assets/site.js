/* Norrath Survey — shared chrome behaviour. Kept deliberately small. */
(function(){
  var b=document.querySelector('.burger'), n=document.querySelector('.site-nav');
  if(b&&n){b.addEventListener('click',function(){
    var open=n.classList.toggle('open');
    b.setAttribute('aria-expanded',String(open));
  });}
  var here=location.pathname.replace(/\/index\.html$/,'/').replace(/\/$/,'')||'/';
  document.querySelectorAll('.site-nav a').forEach(function(a){
    var p=a.getAttribute('href')||'';
    var seg=p.split('/').filter(Boolean)[p.startsWith('..')?1:0];
    if(seg&&here.indexOf(seg)>-1)a.setAttribute('aria-current','page');
  });

  function paint(theme){
    if(theme==='dungeon') document.documentElement.setAttribute('data-theme','dungeon');
    else document.documentElement.setAttribute('data-theme','atlas');
    try{localStorage.setItem('eql-theme', theme==='dungeon'?'dungeon':'atlas');}catch(e){}
    document.querySelectorAll('.theme-toggle').forEach(function(btn){
      var dungeon=theme==='dungeon';
      btn.setAttribute('aria-pressed', String(dungeon));
      btn.setAttribute('aria-label', dungeon?'Switch to daylight atlas':'Switch to torchlit reading');
      btn.textContent=dungeon?'Daylight':'Torchlight';
    });
  }
  function apply(theme){
    var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches;
    if(!reduce&&document.startViewTransition) document.startViewTransition(function(){paint(theme);});
    else paint(theme);
  }
  var stored=null;
  try{stored=localStorage.getItem('eql-theme');}catch(e){}
  var start=stored==='dungeon'||stored==='atlas'?stored
    :(window.matchMedia&&matchMedia('(prefers-color-scheme:dark)').matches?'dungeon':'atlas');
  apply(start);
  document.querySelectorAll('.theme-toggle').forEach(function(btn){
    btn.addEventListener('click',function(){
      var now=document.documentElement.getAttribute('data-theme')==='dungeon'?'atlas':'dungeon';
      apply(now);
    });
  });
})();
