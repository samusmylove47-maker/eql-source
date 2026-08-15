/* scripts/toolrender.js — dump what a tool renders, so a refactor can be proved
 * to change nothing.
 *
 *     node scripts/toolrender.js race-unlocks.html pane-track > before.html
 *     ...make the change, rebuild...
 *     node scripts/toolrender.js race-unlocks.html pane-track > after.html
 *     diff before.html after.html
 *
 * A path works too, so the previous version can be rendered straight out of
 * git:  git show main:_build/source/eql-race-unlocks.html > old.html
 *
 * WHY THIS EXISTS
 * ---------------
 * toolsmoke.js asserts a container is not empty. That is enough to catch a
 * tool that throws or renders nothing, and it is NOT enough to catch a tool
 * that renders the wrong thing.
 *
 * On 14 August 2026 a data migration silently dropped every step note, every
 * race explanation and every hour figure from the race tracker. toolsmoke said
 * "ok, 26857 chars" and meant it — the pane was full, of less. This caught it
 * in one diff.
 *
 * Use it for any change that moves data a tool reads. A migration that alters
 * the rendered output is not a migration.
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const ROOT = process.cwd();

const file = process.argv[2];
const target = process.argv[3];
const html = fs.readFileSync(file.includes('/')||file.includes(String.fromCharCode(92)) ? file : path.join(ROOT,'public','tools',file), 'utf8');

function makeEl(tag, id) {
  const el = { tagName: (tag||'div').toUpperCase(), id: id||'', innerHTML: '',
    textContent:'', value:'', disabled:false, checked:false, hidden:false,
    children: [], dataset:{}, attributes:{},
    style:{ _p:{}, setProperty(k,v){this._p[k]=v;}, getPropertyValue(k){return this._p[k]||'';}, removeProperty(k){delete this._p[k];} },
    classList:{ _s:new Set(), add(...c){c.forEach(x=>this._s.add(x));}, remove(...c){c.forEach(x=>this._s.delete(x));},
      toggle(c,f){const on=f===undefined?!this._s.has(c):f;on?this._s.add(c):this._s.delete(c);return on;},
      contains(c){return this._s.has(c);} },
    addEventListener(){}, removeEventListener(){},
    setAttribute(k,v){this.attributes[k]=String(v);}, getAttribute(k){return k in this.attributes?this.attributes[k]:null;},
    removeAttribute(k){delete this.attributes[k];},
    appendChild(c){this.children.push(c);return c;}, insertAdjacentHTML(_p,h){this.innerHTML+=h;},
    remove(){}, focus(){}, blur(){}, click(){}, scrollIntoView(){},
    closest(){return null;}, matches(){return false;}, cloneNode(){return makeEl(tag,id);},
    querySelector(){return null;}, querySelectorAll(){return [];},
    getBoundingClientRect(){return {top:0,left:0,width:0,height:0};} };
  return el;
}
const byId = new Map();
const doc = {
  getElementById(id){ if(!byId.has(id)) byId.set(id, makeEl('div', id)); return byId.get(id); },
  querySelector(s){ const m=/^#([\w-]+)$/.exec(s); return m?doc.getElementById(m[1]):makeEl('div'); },
  querySelectorAll(){return [];}, createElement(t){return makeEl(t);},
  createDocumentFragment(){return makeEl('fragment');},
  addEventListener(){}, removeEventListener(){}, execCommand(){return true;},
  documentElement:makeEl('html'), head:makeEl('head'), body:makeEl('body'),
  readyState:'complete', title:'', cookie:'' };
const store=()=>{const m=new Map();return{getItem:k=>m.has(k)?m.get(k):null,setItem:(k,v)=>m.set(k,String(v)),removeItem:k=>m.delete(k),clear:()=>m.clear(),get length(){return m.size;},key:i=>[...m.keys()][i]??null};};
const timers=[];
const sb={ document:doc, console, localStorage:store(), sessionStorage:store(),
  location:{href:'https://eqlsource.com/tools/'+file,hash:'',search:'',pathname:'/tools/'+file,origin:'https://eqlsource.com',reload(){},replace(){}},
  history:{replaceState(){},pushState(){},back(){}},
  navigator:{clipboard:{writeText:()=>Promise.resolve()},userAgent:'panedump'},
  setTimeout:fn=>{timers.push(fn);return timers.length;}, clearTimeout(){}, setInterval:()=>0, clearInterval(){},
  requestAnimationFrame:fn=>{timers.push(fn);return 1;}, cancelAnimationFrame(){},
  matchMedia:()=>({matches:false,addEventListener(){},addListener(){}}),
  indexedDB:{open:()=>({addEventListener(){}}),deleteDatabase:()=>({})},
  fetch:()=>Promise.reject(new Error('no network')), URL, URLSearchParams,
  TextEncoder, TextDecoder, JSON, Math, Date,
  btoa:s=>Buffer.from(String(s),'binary').toString('base64'),
  atob:s=>Buffer.from(String(s),'base64').toString('binary'),
  scrollTo(){}, scrollBy(){}, scroll(){}, getComputedStyle:()=>({getPropertyValue:()=>''}),
  alert(){}, confirm:()=>true, prompt:()=>null };
sb.window=sb; sb.globalThis=sb; sb.self=sb;
vm.createContext(sb);
process.on('unhandledRejection',()=>{});

(async () => {
  const re=/<script\b([^>]*)>([\s\S]*?)<\/script>/gi; let m;
  while((m=re.exec(html))){ if(/\bsrc\s*=/.test(m[1])) continue;
    if(m[2].trim().length<200) continue;
    try{ vm.runInContext(m[2], sb, {filename:file, timeout:10000}); }catch(e){ console.error('THREW '+e.message); process.exit(1);} }
  for(let i=0;i<20;i++) await new Promise(r=>setImmediate(r));
  for(const fn of timers.splice(0,50)){ try{fn();}catch(e){} }
  for(let i=0;i<20;i++) await new Promise(r=>setImmediate(r));
  const el=byId.get(target);
  process.stdout.write(el?String(el.innerHTML||''):'');
})();
