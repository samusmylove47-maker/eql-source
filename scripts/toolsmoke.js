/* scripts/toolsmoke.js — run every tool's JavaScript and see whether it works.
 *
 *     node scripts/toolsmoke.js            # all tools
 *     node scripts/toolsmoke.js sky        # one, by substring
 *
 * WHY THIS EXISTS
 * ---------------
 * On 14 August 2026 the Plane of Sky tracker shipped with its class picker
 * rendering nothing. A constant had gone missing in a refactor, so the very
 * first statement of the render threw, no buttons were built, a trio could
 * never reach three, and the Build button was disabled forever.
 *
 * check.py passed all 721 pages that day. Every check it runs reads the HTML a
 * page SHIPS; not one of them runs the page's JavaScript. A tool can be
 * structurally perfect and completely dead, and nothing we had could tell.
 *
 * So this runs it. Two assertions per tool, and the second is the useful one:
 *
 *   1. the script executes on load without throwing
 *   2. where a tool renders something on load, that container is not empty
 *
 * A tool that only renders after input — the inventory reader waits for a
 * paste — gets assertion 1 only, and says so rather than pretending.
 *
 * WHY THE DOM IS HAND-ROLLED
 * --------------------------
 * jsdom would be more faithful and would add a node_modules tree to a static
 * site that has none. This project vendors three.js rather than call a CDN;
 * the same instinct applies. The surveyed API surface across all seven tools is
 * small — getElementById, querySelector, classList, dataset, addEventListener,
 * localStorage, location — and none of it needs layout. About ninety lines.
 *
 * The stub is deliberately shallow. It CANNOT tell you a tool looks right, or
 * that a click does the correct thing. It tells you the script runs and the
 * page fills. That is the gap that let a dead tool ship, and it is all this
 * claims to close.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');

/* What each tool must have done by the time its script has run. `fills` is a
 * DOM id that must contain `expect` afterwards. Omit `fills` for a tool that
 * legitimately renders nothing until the reader does something. */
const TOOLS = [
  { file: 'plane-of-sky.html', fills: 'classgrid', expect: '<button',
    note: 'the class picker — the control that broke' },
  { file: 'planar-gear.html', fills: 'cls', expect: '<button',
    note: 'the class chooser' },
  { file: 'index-search.html', fills: 'results', expect: '<',
    note: 'the result list renders unfiltered on load' },
  { file: 'faction-impact.html', fills: null,
    note: 'zone cards are server-rendered; the script only filters' },
  { file: 'character.html', fills: null,
    note: 'renders from saved state, empty on a first visit' },
  /* These two boot straight onto a tab and fill its pane from the race data,
   * with no saved state needed. Listed as load-only until 14 Aug 2026, which
   * meant the migration of their dataset out of the markup was covered by no
   * assertion at all - the weakest moment to be running blind. */
  { file: 'race-unlocks.html', fills: 'pane-track', expect: '<',
    note: 'the tracker pane, filled from the race data on boot' },
  { file: 'combo-calculator.html', fills: 'pane-calc', expect: '<',
    note: 'same app, boots onto the calculator tab' },
  { file: 'inventory.html', fills: null,
    note: 'waits for a paste; nothing renders on load by design' },
];

/* ---------------------------------------------------------------- the stub */
function makeEl(tag, id) {
  const el = {
    tagName: (tag || 'div').toUpperCase(), id: id || '', innerHTML: '',
    textContent: '', value: '', disabled: false, checked: false, hidden: false,
    children: [], dataset: {}, attributes: {},
    style: { _p: {},
      setProperty(k, v) { this._p[k] = v; },
      getPropertyValue(k) { return this._p[k] || ''; },
      removeProperty(k) { delete this._p[k]; } },
    classList: { _s: new Set(),
      add(...c) { c.forEach(x => this._s.add(x)); },
      remove(...c) { c.forEach(x => this._s.delete(x)); },
      toggle(c, f) { const on = f === undefined ? !this._s.has(c) : f;
                     on ? this._s.add(c) : this._s.delete(c); return on; },
      contains(c) { return this._s.has(c); } },
    addEventListener() {}, removeEventListener() {},
    setAttribute(k, v) { this.attributes[k] = String(v); },
    getAttribute(k) { return k in this.attributes ? this.attributes[k] : null; },
    removeAttribute(k) { delete this.attributes[k]; },
    appendChild(c) { this.children.push(c); return c; },
    insertAdjacentHTML(_pos, html) { this.innerHTML += html; },
    remove() {}, focus() {}, blur() {}, click() {}, scrollIntoView() {},
    closest() { return null; }, matches() { return false; },
    cloneNode() { return makeEl(tag, id); },
    querySelector() { return null; }, querySelectorAll() { return []; },
    getBoundingClientRect() { return { top: 0, left: 0, width: 0, height: 0 }; },
  };
  return el;
}

function makeDocument() {
  const byId = new Map();
  const doc = {
    /* Every id the script asks for exists. A stub that returned null would
     * fail on `$("#x").onclick=` and report a fault the browser does not have,
     * which is worse than no test. */
    getElementById(id) {
      if (!byId.has(id)) byId.set(id, makeEl('div', id));
      return byId.get(id);
    },
    querySelector(sel) {
      const m = /^#([\w-]+)$/.exec(sel);
      return m ? doc.getElementById(m[1]) : makeEl('div');
    },
    querySelectorAll() { return []; },
    createElement(tag) { return makeEl(tag); },
    createDocumentFragment() { return makeEl('fragment'); },
    addEventListener() {}, removeEventListener() {},
    execCommand() { return true; },
    documentElement: makeEl('html'), head: makeEl('head'), body: makeEl('body'),
    readyState: 'complete', title: '', cookie: '',
    _byId: byId,
  };
  return doc;
}

function makeStore() {
  const m = new Map();
  return { getItem: k => (m.has(k) ? m.get(k) : null),
           setItem: (k, v) => m.set(k, String(v)),
           removeItem: k => m.delete(k), clear: () => m.clear(),
           get length() { return m.size; }, key: i => [...m.keys()][i] ?? null };
}

/* ------------------------------------------------------------------ runner */
function scriptsOf(html) {
  const out = [];
  const re = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
  let m;
  while ((m = re.exec(html))) {
    if (/\bsrc\s*=/.test(m[1])) continue;      // external file, not ours to run
    out.push(m[2]);
  }
  return out;
}

async function run(tool) {
  const file = path.join(ROOT, 'public', 'tools', tool.file);
  const html = fs.readFileSync(file, 'utf8');
  const doc = makeDocument();
  const timers = [];
  const sandbox = {
    document: doc, console,
    localStorage: makeStore(), sessionStorage: makeStore(),
    location: { href: 'https://eqlsource.com/tools/' + tool.file, hash: '',
                search: '', pathname: '/tools/' + tool.file,
                origin: 'https://eqlsource.com', reload() {}, replace() {} },
    history: { replaceState() {}, pushState() {}, back() {} },
    navigator: { clipboard: { writeText: () => Promise.resolve() },
                 userAgent: 'toolsmoke' },
    setTimeout: (fn) => { timers.push(fn); return timers.length; },
    clearTimeout() {}, setInterval: () => 0, clearInterval() {},
    requestAnimationFrame: (fn) => { timers.push(fn); return 1 },
    cancelAnimationFrame() {},
    matchMedia: () => ({ matches: false, addEventListener() {}, addListener() {} }),
    indexedDB: { open: () => ({ addEventListener() {}, onsuccess: null,
                                onerror: null, onupgradeneeded: null }),
                 deleteDatabase: () => ({}) },
    fetch: () => Promise.reject(new Error('network is not available in smoke test')),
    URL, URLSearchParams, TextEncoder, TextDecoder, JSON, Math, Date,
    btoa: s => Buffer.from(String(s), 'binary').toString('base64'),
    atob: s => Buffer.from(String(s), 'base64').toString('binary'),
  };
  sandbox.scrollTo = () => {};
  sandbox.scrollBy = () => {};
  sandbox.scroll = () => {};
  sandbox.getComputedStyle = () => ({ getPropertyValue: () => '' });
  sandbox.alert = () => {};
  sandbox.confirm = () => true;
  sandbox.prompt = () => null;
  sandbox.print = () => {};
  sandbox.window = sandbox;
  sandbox.globalThis = sandbox;
  sandbox.self = sandbox;
  vm.createContext(sandbox);

  /* A throw inside an async boot surfaces as an unhandled rejection, not as an
   * exception from runInContext. Without this the process died with a stack
   * trace instead of reporting which tool failed and why. */
  let asyncFail = null;
  const onRejection = (e) => { asyncFail = asyncFail
    || `${(e && e.name) || 'Error'}: ${(e && e.message) || e}`; };
  process.on('unhandledRejection', onRejection);
  process.on('uncaughtException', onRejection);
  const done = () => {
    process.off('unhandledRejection', onRejection);
    process.off('uncaughtException', onRejection);
  };

  const bodies = scriptsOf(html).filter(s => s.trim().length > 200);
  if (!bodies.length) { done(); return { skip: 'no inline script over 200 chars' }; }

  for (const body of bodies) {
    try {
      vm.runInContext(body, sandbox, { filename: tool.file, timeout: 10000 });
    } catch (e) {
      done();
      return { threw: `${e && e.name}: ${e && e.message}` };
    }
  }
  /* Boot is usually an async IIFE — it reads saved state with await before it
   * renders anything. Asserting straight after runInContext looked at the page
   * before a single microtask had run, and reported two working tools dead. */
  for (let i = 0; i < 20; i++) await new Promise(r => setImmediate(r));

  /* anything the page deferred with setTimeout(...,0) is part of load */
  for (const fn of timers.splice(0, 50)) {
    try { fn(); } catch (e) { done(); return { threw: `deferred: ${e && e.message}` }; }
  }
  for (let i = 0; i < 20; i++) await new Promise(r => setImmediate(r));
  done();
  if (asyncFail) return { threw: `during async boot — ${asyncFail}` };

  if (!tool.fills) return { ok: true, rendered: null };
  const el = doc._byId.get(tool.fills);
  const html_ = el ? String(el.innerHTML || '') : '';
  if (!html_.includes(tool.expect)) {
    return { empty: `#${tool.fills} does not contain ${JSON.stringify(tool.expect)} `
                    + `after load (length ${html_.length})` };
  }
  return { ok: true, rendered: `#${tool.fills}, ${html_.length} chars` };
}

/* -------------------------------------------------------------------- main */
const only = process.argv[2];
const picked = only ? TOOLS.filter(t => t.file.includes(only)) : TOOLS;
if (!picked.length) {
  console.error(`no tool matching ${JSON.stringify(only)}`);
  process.exit(2);
}

(async () => {
let bad = 0;
for (const tool of picked) {
  const r = await run(tool);
  const name = tool.file.replace('.html', '');
  if (r.threw) {
    console.log(`  [THREW      ] ${name}\n                ${r.threw}`);
    bad++;
  } else if (r.empty) {
    console.log(`  [RENDERED NOTHING] ${name}\n                ${r.empty}`);
    bad++;
  } else if (r.skip) {
    console.log(`  [skipped    ] ${name} — ${r.skip}`);
  } else if (r.rendered) {
    console.log(`  [ok         ] ${name} — ${r.rendered}`);
  } else {
    console.log(`  [loads      ] ${name} — ${tool.note}`);
  }
}
console.log(bad
  ? `\n${bad} tool(s) failed. A tool that throws on load is dead in the browser.`
  : `\nAll ${picked.length} tools ran. Loading is not working: this proves the `
    + `script executes and the page fills, and nothing more.`);
process.exit(bad ? 1 : 0);
})();
