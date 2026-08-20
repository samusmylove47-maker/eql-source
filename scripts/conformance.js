#!/usr/bin/env node
/* Load every built page in a real browser and report what it does.
 *
 * WHY THIS EXISTS
 * ---------------
 * check.py reads the HTML a page ships. toolsmoke.js runs each tool's script
 * under a stub DOM. Neither of them lays a page out, so neither can see a page
 * that overflows its viewport, throws in the console on load, or renders to an
 * empty body. Those are failures of the built page rather than of its markup,
 * and nothing here has ever looked for them.
 *
 * WHAT IT MEASURES, AND WHAT IT DELIBERATELY DOES NOT
 * ---------------------------------------------------
 * Per page, per viewport: console errors, page exceptions,
 * document.documentElement.scrollWidth against window.innerWidth, and
 * document.body.innerText.length.
 *
 * WHY mobile:false ON A MOBILE VIEWPORT — READ BEFORE CHANGING IT
 * ---------------------------------------------------------------
 * Emulation.setDeviceMetricsOverride with mobile:true makes the overflow check
 * structurally dead, and it fails in the direction that looks like a pass.
 *
 * Under mobile emulation the layout viewport is elastic: give a page a 900px
 * child at a 390px device width and window.innerWidth reports 900, because the
 * layout viewport grew to contain it. scrollWidth grows with it, the two are
 * equal on every page ever tested, and `scrollWidth > innerWidth` cannot fire.
 * A control page built to overflow reported 900 / 900 and no finding.
 *
 * With mobile:false the layout viewport stays pinned at the width asked for.
 * The same control reports 900 / 390 and the finding fires. That is the whole
 * reason this flag is off: the cost is touch emulation and a desktop UA, which
 * this script does not measure, and the gain is a check that is alive.
 *
 * It makes NO typography or aesthetic judgement, and it must not be extended to
 * make one. Every page links three Google-hosted faces, this script aborts
 * every non-file: request, and the fonts therefore render as system fallbacks —
 * so line length, rhythm, and whether a label fits its box are all measured
 * against a page that is not the page which ships. Overflow at 390px is
 * reported because CLAUDE.md sets it as a hard rule and a fallback face is
 * wider than the real one, which makes this the conservative direction: a
 * measurement here is a lower bound on the real page's fit.
 *
 * WHY EVERY REQUEST IS ABORTED
 * ----------------------------
 * The browser in this environment has no network egress. Left alone, each
 * page's font requests hang until they time out, at roughly twelve seconds a
 * page, which is four hours for the site. Aborting them costs a fallback face
 * and buys the whole sweep in about a minute.
 *
 * ZERO DEPENDENCIES, BY CONSTRAINT AND BY CHOICE
 * ----------------------------------------------
 * This repo has no package.json and no node_modules, and adding puppeteer to
 * run a check is a large dependency for a small job. Node 24 ships a global
 * WebSocket, so it can drive Chrome over the DevTools Protocol directly.
 *
 * Hand-run, like scripts/contamination.py and _build/geometry.py — a rebuild
 * must work on a machine with no browser. Follows toolsmoke.js: serial, every
 * entry accounted for even when skipped, and WARN-and-continue where the binary
 * is absent rather than failing a build over a missing tool.
 *
 *     node scripts/conformance.js            # both viewports, whole site
 *     node scripts/conformance.js --desktop  # 1440x900 only
 *     node scripts/conformance.js public/learn/difficulty.html   # one page
 */
'use strict';
const { spawn, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

const ROOT = path.dirname(__dirname);
process.chdir(ROOT);

const VIEWPORTS = [
  { name: 'desktop', width: 1440, height: 900 },
  { name: 'mobile', width: 390, height: 844 },
];

// The two grounds. Torchlight is the default and sets no attribute at all -
// asking for it explicitly would test a state most readers never reach.
//
// TRAP, and it cost a wrong answer while this was written: the attribute has to
// be set AFTER Page.navigate, not before. Navigating replaces the document and
// takes any attribute with it, so a theme applied up front measures the default
// twice and reports a clean daylight sweep without ever having rendered
// daylight. That is the same shape as mobile:true above - a check that cannot
// fail rather than one that passes.
const THEMES = [
  { name: 'torchlight', attr: null },
  { name: 'daylight', attr: 'light' },
];

const CANDIDATES = [
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
];

function findBrowser() {
  for (const c of CANDIDATES) if (fs.existsSync(c)) return c;
  return null;
}

/* ---- the smallest CDP client that does this job ------------------------- */

class CDP {
  constructor(ws) {
    this.ws = ws;
    this.id = 0;
    this.pending = new Map();
    this.handlers = new Map();
    ws.addEventListener('message', (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id !== undefined) {
        const p = this.pending.get(msg.id);
        if (!p) return;
        this.pending.delete(msg.id);
        msg.error ? p.reject(new Error(msg.error.message)) : p.resolve(msg.result);
      } else {
        const hs = this.handlers.get(msg.method) || [];
        for (const h of hs) h(msg.params, msg.sessionId);
      }
    });
  }
  on(method, fn) {
    if (!this.handlers.has(method)) this.handlers.set(method, []);
    this.handlers.get(method).push(fn);
  }
  send(method, params = {}, sessionId) {
    const id = ++this.id;
    const payload = { id, method, params };
    if (sessionId) payload.sessionId = sessionId;
    this.ws.send(JSON.stringify(payload));
    return new Promise((resolve, reject) => this.pending.set(id, { resolve, reject }));
  }
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function getJSON(url, tries = 60) {
  for (let i = 0; i < tries; i++) {
    try {
      const r = await fetch(url);
      if (r.ok) return await r.json();
    } catch (e) { /* browser not up yet */ }
    await sleep(200);
  }
  throw new Error(`devtools endpoint never answered: ${url}`);
}

/* ---- the page set: exactly what check.py checks -------------------------- */

function sitePages() {
  const out = [];
  const walk = (dir, depth) => {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      const p = path.join(dir, e.name).replace(/\\/g, '/');
      if (e.isDirectory()) {
        if (depth === 0 && e.name !== 'app') walk(p, depth + 1);
      } else if (e.name.endsWith('.html') && !e.name.startsWith('_')) {
        out.push(p);
      }
    }
  };
  walk('public', 0);
  return out.sort();
}

const groupOf = (p) => {
  const rel = p.replace('public/', '');
  return rel.includes('/') ? rel.split('/')[0] : '(root)';
};

/* ---- main --------------------------------------------------------------- */

(async () => {
  const args = process.argv.slice(2);
  const only = args.filter((a) => !a.startsWith('--'));
  const themes = process.argv.includes('--one-theme') ? [THEMES[0]] : THEMES;
const showAll = args.includes('--show');
  const viewports = args.includes('--desktop')
    ? VIEWPORTS.filter((v) => v.name === 'desktop')
    : args.includes('--mobile')
      ? VIEWPORTS.filter((v) => v.name === 'mobile')
      : VIEWPORTS;

  const bin = findBrowser();
  if (!bin) {
    console.log('WARN  no Chrome or Edge binary found — conformance sweep skipped.');
    console.log('      This is not a build failure. check.py and toolsmoke.js still');
    console.log('      cover the markup and the tools; nothing lays a page out.');
    process.exit(0);
  }

  const pages = only.length ? only.map((p) => p.replace(/\\/g, '/')) : sitePages();
  if (!pages.length) {
    console.log('WARN  no built pages found. Run ./build.sh first.');
    process.exit(0);
  }

  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'eql-conf-'));
  const port = 9222 + (process.pid % 500);
  const child = spawn(bin, [
    '--headless=new',
    `--remote-debugging-port=${port}`,
    `--user-data-dir=${profile}`,
    '--no-first-run', '--no-default-browser-check', '--disable-gpu',
    '--disable-extensions', '--disable-background-networking',
    '--disable-sync', '--mute-audio', '--hide-scrollbars',
    'about:blank',
  ], { stdio: 'ignore' });

  let cleanedUp = false;
  const cleanup = () => {
    if (cleanedUp) return;
    cleanedUp = true;
    try { child.kill(); } catch (e) { /* already gone */ }
    try { fs.rmSync(profile, { recursive: true, force: true }); } catch (e) { /* locked */ }
  };
  process.on('exit', cleanup);
  process.on('SIGINT', () => { cleanup(); process.exit(130); });

  const version = await getJSON(`http://127.0.0.1:${port}/json/version`);
  const ws = new WebSocket(version.webSocketDebuggerUrl);
  await new Promise((res, rej) => {
    ws.addEventListener('open', res);
    ws.addEventListener('error', rej);
  });
  const cdp = new CDP(ws);

  const { targetId } = await cdp.send('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await cdp.send('Target.attachToTarget', { targetId, flatten: true });

  await cdp.send('Page.enable', {}, sessionId);
  await cdp.send('Runtime.enable', {}, sessionId);
  await cdp.send('Fetch.enable', { patterns: [{ urlPattern: '*' }] }, sessionId);

  // Everything that is not the local file is aborted. See the header: with no
  // egress these hang for twelve seconds a page, and the fonts they fetch are
  // the one thing this script is forbidden to have an opinion about anyway.
  let blocked = 0;
  cdp.on('Fetch.requestPaused', async (p, sid) => {
    const isLocal = p.request.url.startsWith('file://');
    if (!isLocal) blocked++;
    try {
      await cdp.send(isLocal ? 'Fetch.continueRequest' : 'Fetch.failRequest',
        isLocal ? { requestId: p.requestId }
                : { requestId: p.requestId, errorReason: 'Aborted' }, sid);
    } catch (e) { /* navigation moved on */ }
  });

  let consoleErrors = [];
  cdp.on('Runtime.consoleAPICalled', (p) => {
    if (p.type === 'error') {
      consoleErrors.push((p.args || []).map((a) => a.value ?? a.description ?? a.type).join(' '));
    }
  });
  cdp.on('Runtime.exceptionThrown', (p) => {
    const d = p.exceptionDetails || {};
    consoleErrors.push(d.exception?.description || d.text || 'exception');
  });

  let loaded = false;
  cdp.on('Page.loadEventFired', () => { loaded = true; });

  const findings = [];
  const groups = new Map();
  const t0 = Date.now();

  for (const page of pages) {
    const url = 'file:///' + path.resolve(page).replace(/\\/g, '/');
    for (const vp of viewports) {
      await cdp.send('Emulation.setDeviceMetricsOverride', {
        width: vp.width, height: vp.height, deviceScaleFactor: 1,
        mobile: false,   // NOT a simplification — see the header. mobile:true
                         // makes the layout viewport elastic and the overflow
                         // check can then never fire.
      }, sessionId);

     for (const theme of themes) {
      consoleErrors = [];
      loaded = false;
      await cdp.send('Page.navigate', { url }, sessionId);
      for (let i = 0; i < 100 && !loaded; i++) await sleep(20);

      // After navigate, never before - see THEMES.
      await cdp.send('Runtime.evaluate', {
        expression: theme.attr
          ? `document.documentElement.setAttribute('data-theme','${theme.attr}')`
          : `document.documentElement.removeAttribute('data-theme')`,
      }, sessionId);
      await sleep(30);   // let the cascade settle before measuring

      let m;
      try {
        const r = await cdp.send('Runtime.evaluate', {
          expression: `(() => ({
            scrollWidth: document.documentElement.scrollWidth,
            innerWidth: window.innerWidth,
            textLength: (document.body && document.body.innerText || '').length,
            title: document.title || ''
          }))()`,
          returnByValue: true,
        }, sessionId);
        m = r.result.value;
      } catch (e) {
        findings.push({ page, vp: vp.name, theme: theme.name, kind: 'evaluate failed', detail: e.message });
        continue;
      }

      // A silent pass and a broken measurement look identical, which is the
      // fault gate_selftest.py exists to prevent one level up. --show prints
      // every number so a clean sweep can be read rather than trusted.
      if (showAll) {
        console.log(`  ${page} @ ${vp.name}/${theme.name}: scrollWidth ${m.scrollWidth} / innerWidth `
                  + `${m.innerWidth}, innerText ${m.textLength} chars, `
                  + `${consoleErrors.length} console error(s)`);
      }

      const g = groupOf(page);
      if (!groups.has(g)) groups.set(g, { n: 0, overflow: 0, errors: 0, empty: 0 });
      const gs = groups.get(g);
      gs.n++;

      if (m.scrollWidth > m.innerWidth) {
        gs.overflow++;
        findings.push({
          page, vp: vp.name, theme: theme.name, kind: 'overflow',
          detail: `scrollWidth ${m.scrollWidth} > innerWidth ${m.innerWidth} (+${m.scrollWidth - m.innerWidth}px)`,
        });
      }
      if (consoleErrors.length) {
        gs.errors++;
        findings.push({
          page, vp: vp.name, theme: theme.name, kind: 'console',
          detail: consoleErrors.slice(0, 3).join(' | ').slice(0, 300),
        });
      }
      if (m.textLength < 40) {
        gs.empty++;
        findings.push({
          page, vp: vp.name, theme: theme.name, kind: 'empty',
          detail: `body.innerText is ${m.textLength} chars`,
        });
      }
     }
    }
  }

  const secs = ((Date.now() - t0) / 1000).toFixed(1);

  console.log(`Conformance sweep — ${pages.length} pages x ${viewports.length} viewport(s) `
            + `in ${secs}s, ${blocked} non-file request(s) aborted\n`);

  console.log('  group          pages  overflow  console  empty');
  for (const [g, s] of [...groups].sort()) {
    console.log(`  ${g.padEnd(14)} ${String(s.n).padStart(5)} ${String(s.overflow).padStart(9)} `
              + `${String(s.errors).padStart(8)} ${String(s.empty).padStart(6)}`);
  }

  if (!findings.length) {
    console.log('\nNo page overflowed its viewport, logged a console error, or rendered empty.');
    console.log('This says nothing about how any of it looks: the webfonts were aborted.');
    cleanup();
    process.exit(0);
  }

  console.log(`\n${findings.length} finding(s):\n`);
  for (const f of findings) {
    console.log(`  [${f.kind.padEnd(9)}] ${f.page} @ ${f.vp}`);
    console.log(`               ${f.detail}`);
  }
  console.log('\nReported, not judged. The webfonts were aborted, so nothing above is a');
  console.log('statement about type, rhythm or whether a label fits its box.');
  cleanup();
  process.exit(0);
})().catch((e) => {
  console.error('conformance sweep failed:', e.message);
  process.exit(1);
});
