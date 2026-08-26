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
  /* tools/plane-of-sky.html was withdrawn on 17 Aug 2026 — Sky Ledger replaced
   * it. Its page here is a description with no application in it, and the
   * application itself lives in public/app/ with its own test suite in its own
   * repository. Listed so this file stays parallel to the TOOLS registry in
   * _build/_partials.py; it reports as skipped, which is the honest answer. */
  { file: 'sky-ledger.html', fills: null,
    note: 'a description page — the app it links is tested in its own repo' },
  /* Same shape: a description page for an application hosted in its own
   * repository. Listed rather than omitted because nothing else forces a new
   * tool to appear here, and a page that ships unsmoked is one nobody notices
   * is unsmoked. */
  { file: '50-upgrades.html', fills: null,
    note: 'a description page — the app it links is hosted and tested in its own repo' },
  /* Third of the same shape. Promoted 26 Aug 2026; the page describes the
   * application and the application itself is smoked below, out of
   * public/app/, along with the Sky Ledger's. */
  { file: 'lockouts.html', fills: null,
    note: 'a description page — the app it links is tested in its own repo' },
  { file: 'index-search.html', fills: 'results', expect: '<',
    note: 'the result list renders unfiltered on load' },
  { file: 'faction-impact.html', fills: null,
    note: 'zone cards are server-rendered; the script only filters' },
  /* These two boot straight onto a tab and fill its pane from the race data,
   * with no saved state needed. Listed as load-only until 14 Aug 2026, which
   * meant the migration of their dataset out of the markup was covered by no
   * assertion at all - the weakest moment to be running blind. */
  { file: 'race-unlocks.html', fills: 'pane-track', expect: '<',
    note: 'the tracker pane, filled from the race data on boot' },
  { file: 'combo-calculator.html', fills: 'pane-calc', expect: '<',
    note: 'same app, boots onto the calculator tab' },
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

/* THE LIST ABOVE IS A SECOND COPY OF THE REGISTRY, SO IT IS PINNED TO THE FIRST.
 *
 * Its own comment said a tool is listed here "because nothing else forces a new
 * tool to appear", and on 26 Aug 2026 that came true: the lockout tracker was
 * registered in _build/_partials.py, shipped a page, reached the footer and the
 * hub, and this file went on reporting "All 6 tools ran" — a green line for a
 * set that had grown underneath it. A hand-maintained parallel list with nothing
 * comparing it to its original is the drift this project keeps finding.
 *
 * So: read the slugs out of _partials.py and refuse to run if the two disagree.
 * A tool missing here is unsmoked; a tool here that no longer exists is a test
 * pointing at nothing. Both are failures, and neither is silent any more. */
function pinToRegistry() {
  const py = path.join(__dirname, '..', '_build', '_partials.py');
  let src;
  try {
    src = fs.readFileSync(py, 'utf8');
  } catch {
    console.error(`toolsmoke: cannot read ${py} to pin the tool list`);
    process.exit(2);
  }
  const block = src.slice(src.indexOf('TOOLS = ['));
  const registry = [...block.slice(0, block.indexOf('\n]')).matchAll(/slug="([^"]+)"/g)]
    .map((m) => `${m[1]}.html`);
  const listed = TOOLS.map((t) => t.file);
  const missing = registry.filter((f) => !listed.includes(f));
  const extra = listed.filter((f) => !registry.includes(f));
  if (missing.length || extra.length) {
    console.error('toolsmoke: this file has drifted from _build/_partials.py TOOLS');
    if (missing.length) {
      console.error(`  registered but unsmoked: ${missing.join(', ')}`);
    }
    if (extra.length) {
      console.error(`  smoked but not registered: ${extra.join(', ')}`);
    }
    console.error('  Add or remove the entry above; the registry is the truth.');
    process.exit(2);
  }
  console.log(`  [pinned     ] ${registry.length} tools, matching _partials.TOOLS`);
}

/* -------------------------------------------------------------------- main */
pinToRegistry();
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
/* ── served applications: does the bundle even parse? ──────────────────────
 * On 17 August a fix written through a shell heredoc turned an escaped newline
 * escape into two REAL line breaks inside a JavaScript string literal. The
 * bundle raised SyntaxError on load and the whole tool rendered nothing — empty
 * class picker, empty rune list — while 196 dataset assertions still passed,
 * because they exercise the engine and the data rather than the built page. A
 * green suite and a dead page look identical from a terminal.
 *
 * This is SYNTAX ONLY. No DOM, no execution. The served bundles are whole
 * applications with their own suites, and running one under a stub DOM fails
 * for a dozen unrelated reasons — which is how a check like this gets switched
 * off within a week. Parsing is the part that catches the fault above, and it
 * costs milliseconds. */
const appDir = path.join(ROOT, 'public', 'app');
let appsChecked = 0;
if (fs.existsSync(appDir)) {
  for (const f of fs.readdirSync(appDir).filter((n) => n.endsWith('.html'))) {
    const html = fs.readFileSync(path.join(appDir, f), 'utf8');
    const bodies = [...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)]
      .map((m) => m[1])
      .filter((b) => b.trim().length);
    let i = 0;
    for (const body of bodies) {
      i += 1;
      try {
        new vm.Script(body);
      } catch (e) {
        bad += 1;
        console.log(`  [SYNTAX     ] app/${f} script ${i} — ${e.message}`);
      }
    }
    appsChecked += 1;
    console.log(`  [parses     ] app/${f} — ${bodies.length} inline script(s)`);
  }
}

console.log(bad
  ? `\n${bad} failure(s). A tool that throws on load is dead in the browser.`
  : `\nAll ${picked.length} tools ran${appsChecked ? `, ${appsChecked} served app(s) parse` : ''}. `
    + `Loading is not working: this proves the script executes and the page `
    + `fills, and nothing more.`);
process.exit(bad ? 1 : 0);
})();
