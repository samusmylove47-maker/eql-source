/* Norrath Survey — shared chrome behaviour. Kept deliberately small. */
(function(){
  var b=document.querySelector('.burger'), n=document.querySelector('.site-nav');
  if(b&&n){b.addEventListener('click',function(){
    var open=n.classList.toggle('open');
    b.setAttribute('aria-expanded',String(open));
  });}
  // mark the current section in the nav
  var here=location.pathname.replace(/\/index\.html$/,'/').replace(/\/$/,'')||'/';
  document.querySelectorAll('.site-nav a').forEach(function(a){
    var p=a.getAttribute('href')||'';
    var seg=p.split('/').filter(Boolean)[p.startsWith('..')?1:0];
    if(seg&&here.indexOf(seg)>-1)a.setAttribute('aria-current','page');
  });
})();
