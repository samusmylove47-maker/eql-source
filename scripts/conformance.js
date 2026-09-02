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
// prefers-color-scheme is EMULATED rather than left to the host, and that is
// load-bearing now that the site honours it. With the media query shipping, a
// torchlight case that merely removes the attribute renders DAYLIGHT on a
// machine set to light - so the sweep would measure daylight twice and report
// a clean torchlight run having never rendered it. The third instance of the
// same shape in this file, after mobile:true and set-the-theme-before-navigate:
// a check that cannot fail rather than one that passes.
//
// Each ground is therefore pinned twice over - the media feature AND the
// attribute - so neither the host's setting nor a stored choice can move it.
const THEMES = [
  { name: 'torchlight', attr: 'dark', media: 'dark' },
  { name: 'daylight', attr: 'light', media: 'light' },
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

/* A page that looks blank is given this long to fill before it is called empty.
 * Only a page that currently measures empty spends it, so the static site pays
 * nothing. 20 x 100ms = two seconds, on top of the load wait. */
const EMPTY_CHARS = 40;
const SETTLE_TRIES = 20;
const SETTLE_MS = 100;

/* WHY public/app/ WAS EXCLUDED, AND WHY IT IS NOT ANY MORE.
 *
 * This walk read `if (depth === 0 && e.name !== 'app')`, so the only instrument
 * that opens a page in a real browser skipped the two files a reader opens AS
 * APPLICATIONS. toolsmoke.js skips them for the same stated reason: the
 * applications live in their own repositories and have their own test suites.
 *
 * That reasoning is wrong in one specific way, and it took three shipped
 * failures to see it. Those suites run under Node. **A Node suite does not lay
 * out a page.** It can prove an engine computes the right answer and tell you
 * nothing about whether anything appeared on screen:
 *
 *   - The Sky Ledger's escaped `\n\n` raised a SyntaxError in the browser while
 *     196 dataset assertions passed. It was public for six minutes.
 *   - The lockout tracker's shortDay() temporal dead zone: the page loaded, the
 *     engine ran, the grid never appeared, and the tests were green.
 *
 * So the exclusion was documented, deliberate, and load-bearing in the worst
 * way - being written down is what stopped anyone re-examining it. It is the
 * third check in ten days to name its own hole and be trusted anyway, after
 * check.py's dead root guard and toolsmoke.js's second copy of the tool
 * registry. If you are reading this because you want to exclude something from
 * a check again: write down what would go unseen, then go and look at whether
 * anything else would actually see it.
 */
function sitePages() {
  const out = [];
  const walk = (dir, depth) => {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      const p = path.join(dir, e.name).replace(/\\/g, '/');
      if (e.isDirectory()) {
        if (depth === 0) walk(p, depth + 1);
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

  // A NAMED PAGE THAT DOES NOT EXIST USED TO SWEEP CLEAN.
  //
  // The positional argument is a path, not a filter, and nothing checked it.
  // Chrome answers a missing file:// URL with its own error page, that page
  // carries well over the 40 characters the empty check wants, and the run
  // finished with "No page overflowed its viewport, logged a console error, or
  // rendered empty." A mistyped path - the normal way anyone narrows a run
  // while iterating - produced a green sweep of nothing at all.
  //
  // Found 27 Aug 2026 while mutation-testing this file, and it is the fourth
  // instrument in ten days whose green light could mean nothing: after
  // check.py's dead root guard, toolsmoke.js's second copy of the tool
  // registry, and this file's own public/app/ exclusion.
  const missing = pages.filter((p) => !fs.existsSync(p));
  if (missing.length) {
    console.error(`conformance: ${missing.length} named page(s) do not exist:`);
    for (const p of missing) console.error(`  ${p}`);
    console.error('Refusing to run. A missing page loads Chrome\'s error page, '
                + 'which is not empty and would sweep clean.');
    process.exit(2);
  }
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
  let contrastChecked = 0, contrastUnmeasurable = 0;
  let themeScriptId = null;
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
      // THE GROUND IS SET BEFORE THE DOCUMENT EXISTS, NOT AFTER IT LOADS.
      //
      // This used to set data-theme with Runtime.evaluate after navigation and
      // it reported the previous ground: the theme switch at 1.52:1 and the
      // plate cards at 1.31:1, both of which measure 13.91 and 10.76 on a page
      // that was actually LOADED in that ground. Custom properties update on a
      // late mutation; resolved colours do not reliably follow within the tick,
      // and forcing a reflow did not fix it either.
      //
      // addScriptToEvaluateOnNewDocument runs before the page's own scripts, so
      // the attribute is on <html> at first paint and every style is computed
      // once, in the ground being measured. That is also what a reader gets,
      // because the site's own no-flash script does exactly this.
      if (themeScriptId) {
        await cdp.send('Page.removeScriptToEvaluateOnNewDocument',
          { identifier: themeScriptId }, sessionId);
        themeScriptId = null;
      }
      await cdp.send('Emulation.setEmulatedMedia', {
        features: [{ name: 'prefers-color-scheme', value: theme.media }],
      }, sessionId);
      const ins = await cdp.send('Page.addScriptToEvaluateOnNewDocument', {
        // A new-document script runs at document CREATION, before the parser
        // has made <html> - documentElement is null and a bare setAttribute
        // throws, which the sweep then reports as a console error on every
        // page. The observer applies it the instant the element appears, which
        // is still before any style is resolved for paint.
        source: `(function(){
          var want = ${JSON.stringify(theme.attr)};
          function set(){
            var d = document.documentElement;
            if (!d) return false;
            if (want) d.setAttribute('data-theme', want); else d.removeAttribute('data-theme');
            return true;
          }
          if (!set()) {
            var o = new MutationObserver(function(){ if (set()) o.disconnect(); });
            o.observe(document, { childList: true, subtree: true });
          }
        })();`,
      }, sessionId);
      themeScriptId = ins.identifier;

      consoleErrors = [];
      loaded = false;
      await cdp.send('Page.navigate', { url }, sessionId);
      for (let i = 0; i < 100 && !loaded; i++) await sleep(20);


      const readMetrics = async () => {
        const r = await cdp.send('Runtime.evaluate', {
          expression: `(() => ({
            scrollWidth: document.documentElement.scrollWidth,
            innerWidth: window.innerWidth,
            textLength: (document.body && document.body.innerText || '').length,
            title: document.title || ''
          }))()`,
          returnByValue: true,
        }, sessionId);
        return r.result.value;
      };

      let m;
      try {
        m = await readMetrics();
        // THE APPS IN public/app/ RENDER AFTER LOAD, so one read at
        // loadEventFired would call a working application empty. This is the
        // thing that made excluding them look reasonable, and it is a couple of
        // lines to solve instead.
        //
        // The grace period is spent ONLY on a page that currently looks empty,
        // so the 715 static pages measure exactly as before and pay nothing: a
        // page with text leaves the loop without ever sleeping. A page that is
        // still blank after the full wait is reported empty, which is the
        // failure we want and the one that shipped twice.
        for (let i = 0; i < SETTLE_TRIES && m && m.textLength < EMPTY_CHARS; i++) {
          await sleep(SETTLE_MS);
          m = await readMetrics();
        }
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
      if (!groups.has(g)) groups.set(g, { n: 0, overflow: 0, errors: 0, empty: 0, contrast: 0 });
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
      if (m.textLength < EMPTY_CHARS) {
        gs.empty++;
        findings.push({
          page, vp: vp.name, theme: theme.name, kind: 'empty',
          detail: `body.innerText is ${m.textLength} chars`,
        });
      }

      // ── CONTRAST ────────────────────────────────────────────────────────
      // Added 20 Aug 2026, after .site-bar shipped a torchlight literal with no
      // daylight partner and left the masthead at 1.06:1 on 699 pages. The
      // wordmark was invisible in daylight and every check in this repository
      // was green, because this file's own header said it reads overflow and
      // errors and never colour. That was true and it is the gap this closes.
      //
      // Three things it does that a naive version gets wrong, each learned by
      // getting it wrong first:
      //
      //   1. ALPHA IS COMPOSITED. .foot-contact carries rgba(255,255,255,.02);
      //      read as an opaque near-white ground it reports 1.97 on a link that
      //      actually measures 8.96.
      //   2. A BACKGROUND IMAGE IS NOT A COLOUR. The plate cards are painted by
      //      a gradient, so walking for a background-COLOUR sails past them to
      //      the page and reports dark-on-dark for light-on-dark text. Those
      //      elements are counted as UNMEASURABLE and reported, never guessed
      //      at and never silently skipped.
      //   3. IT MEASURES A FRESH LOAD. Flipping data-theme in place and reading
      //      getComputedStyle reports the previous ground, because style
      //      recalculation lags the attribute. The sweep navigates per theme,
      //      so every reading here is of a page that was laid out in the ground
      //      it claims to be.
      //
      // Large text takes the 3:1 bar, as WCAG allows: >=24px, or >=18.66px bold.
      let c;
      try {
        const rc = await cdp.send('Runtime.evaluate', {
          expression: `(() => {
            // Force style + layout before reading anything. Setting data-theme
            // and reading getComputedStyle in the same task returns the
            // PREVIOUS ground: custom properties update, resolved colours lag.
            // It reported the theme switch at 1.52:1 and the plate cards at
            // 1.31:1, both of which measure fine on a fresh load. Fourth
            // instance of the same shape in this file.
            void document.body.offsetHeight;
            const lin = v => { v /= 255; return v <= 0.04045 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); };
            const px = s => {
              const n = (String(s).match(/[\\d.]+/g) || ['0','0','0']).map(Number);
              if (String(s).indexOf('color(') === 0) return { rgb: n.slice(0,3).map(v => v*255), a: 1 };
              return { rgb: n.slice(0,3), a: n.length > 3 ? n[3] : 1 };
            };
            const lum = c => 0.2126*lin(c[0]) + 0.7152*lin(c[1]) + 0.0722*lin(c[2]);
            const ground = el => {
              const stack = [];
              for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
                const cs = getComputedStyle(n);
                const { rgb, a } = px(cs.backgroundColor);
                const painted = cs.backgroundImage && cs.backgroundImage !== 'none';
                // An image OVER an opaque colour still has a defined ground: the
                // page carries decorative gradients at 3-12% alpha above
                // --surface-0, and bailing on those made 856 of 1,076 elements
                // unmeasurable - the check would have reported almost nothing
                // and looked thorough doing it. An image over TRANSPARENT is a
                // different thing: that is the plate cards, painted entirely by
                // a gradient, and there is no colour to read.
                if (painted && a < 1) return null;
                if (a > 0) { stack.push({ rgb, a }); if (a >= 1) break; }
              }
              if (!stack.length) return null;
              let out = stack[stack.length-1].rgb;
              for (let i = stack.length-2; i >= 0; i--) {
                const L = stack[i];
                out = out.map((v,j) => L.rgb[j]*L.a + v*(1-L.a));
              }
              return out;
            };
            let checked = 0, unmeasurable = 0;
            const bad = [];
            const all = document.querySelectorAll('body *');
            for (const el of all) {
              let own = '';
              for (const n of el.childNodes) if (n.nodeType === 3) own += n.textContent.trim();
              if (own.length < 2) continue;
              const box = el.getBoundingClientRect();
              // A 1x1 box shows no readable text, so its contrast measures
              // nothing. The bound was < 1 and a visually-hidden label is
              // exactly 1px, so the .sr-only spans added on 1 Sep 2026 arrived
              // as dozens of findings about text no eye will ever meet - and a
              // report full of those is one nobody reads, which is how a real
              // finding gets lost.
              if (box.width <= 1 || box.height <= 1) continue;
              const cs = getComputedStyle(el);
              if (cs.visibility === 'hidden' || cs.opacity === '0') continue;
              // Belt and braces: a larger box clipped away to nothing is just
              // as invisible as a 1px one.
              if (/rect\(0px,? 0px,? 0px,? 0px\)/.test(cs.clip)) continue;
              const bg = ground(el);
              if (!bg) { unmeasurable++; continue; }
              checked++;
              const size = parseFloat(cs.fontSize) || 16;
              const weight = parseInt(cs.fontWeight, 10) || 400;
              const bar = (size >= 24 || (size >= 18.66 && weight >= 700)) ? 3 : 4.5;
              const f = lum(px(cs.color).rgb), b = lum(bg);
              const ratio = (Math.max(f,b) + 0.05) / (Math.min(f,b) + 0.05);
              if (ratio < bar) bad.push({
                sel: el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className
                       ? '.' + el.className.trim().split(/\\s+/).join('.') : ''),
                ratio: Math.round(ratio*100)/100, bar,
                text: own.slice(0,28),
              });
            }
            bad.sort((x,y) => x.ratio - y.ratio);
            return { checked, unmeasurable, bad: bad.slice(0,6) };
          })()`,
          returnByValue: true,
        }, sessionId);
        c = rc.result.value;
      } catch (e) {
        findings.push({ page, vp: vp.name, theme: theme.name, kind: 'contrast probe failed', detail: e.message });
        c = null;
      }
      if (c) {
        contrastChecked += c.checked;
        contrastUnmeasurable += c.unmeasurable;
        // Zero examined is a failure, not a pass: "no element is below the bar"
        // is satisfied for free by an empty collection. Same rule gate.py uses.
        if (c.checked === 0 && m.textLength > 200) {
          findings.push({
            page, vp: vp.name, theme: theme.name, kind: 'contrast',
            detail: `examined 0 elements on a page with ${m.textLength} chars of text — the probe is not reading this page`,
          });
        }
        for (const b of c.bad) {
          gs.contrast++;
          findings.push({
            page, vp: vp.name, theme: theme.name, kind: 'contrast',
            detail: `${b.sel} ${b.ratio}:1 against a ${b.bar}:1 bar — ${JSON.stringify(b.text)}`,
          });
        }
      }
     }
    }
  }

  const secs = ((Date.now() - t0) / 1000).toFixed(1);

  console.log(`  contrast: ${contrastChecked.toLocaleString()} element(s) measured, `
            + `${contrastUnmeasurable.toLocaleString()} unmeasurable (painted by an image, `
            + `not a colour) — reported rather than skipped
`);

  console.log(`Conformance sweep — ${pages.length} pages x ${viewports.length} viewport(s) `
            + `in ${secs}s, ${blocked} non-file request(s) aborted\n`);

  console.log('  group          pages  overflow  console  empty  contrast');
  for (const [g, s] of [...groups].sort()) {
    console.log(`  ${g.padEnd(14)} ${String(s.n).padStart(5)} ${String(s.overflow).padStart(9)} `
              + `${String(s.errors).padStart(8)} ${String(s.empty).padStart(6)} `
              + `${String(s.contrast).padStart(9)}`);
  }

  if (!findings.length) {
    console.log('\nNo page overflowed its viewport, logged a console error, or rendered empty.');
    console.log(`Type IS what ships: ${blocked} remote request(s) aborted, and the faces`);
    console.log('are self-hosted - so these pages were laid out in the real type.');
    cleanup();
    process.exit(0);
  }

  console.log(`\n${findings.length} finding(s):\n`);
  for (const f of findings) {
    console.log(`  [${f.kind.padEnd(9)}] ${f.page} @ ${f.vp}${f.theme ? '/' + f.theme : ''}`);
    console.log(`               ${f.detail}`);
  }
  console.log(`
Reported, not judged. ${blocked} remote request(s) were aborted and the faces`);
  console.log('are self-hosted, so this WAS laid out in the type that ships.');
  console.log('statement about type, rhythm or whether a label fits its box.');
  cleanup();
  process.exit(0);
})().catch((e) => {
  console.error('conformance sweep failed:', e.message);
  process.exit(1);
});
