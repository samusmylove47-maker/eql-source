/* mediadefer.js — the deferred trailers are still deferred, and still arrive.
 *
 * Hand-run, like conformance.js and toolrender.js. NOT part of build.sh: it
 * needs a browser installed and a rebuild must work on a machine without one.
 *
 * WHY THIS EXISTS AT ALL, since three checks already run over these pages and
 * none of them can see this property:
 *
 *   - conformance.js ABORTS every non-file request by design, and its own
 *     header forbids extending it to judge what it cannot fetch.
 *   - toolsmoke.js runs scripts under a stub DOM. There is no viewport, so
 *     there is no intersection, so there is nothing to observe.
 *   - check.py reads the HTML a page ships. The attachment happens at runtime.
 *
 * An IntersectionObserver that sets a src when a band is approached is
 * invisible to all three, and 2,191,073 bytes of trailer now depend on it.
 *
 * TWO HALVES, AND THE FIRST ONE NEEDS NO BROWSER.
 *
 *   STATIC   No built page may carry an eager src= or poster= pointing at
 *            media. This is the regression that costs the most and it is
 *            decidable from the file: if the attribute is not there, a
 *            parse-time fetch cannot happen. Always runs.
 *
 *   RUNTIME  Every video holding a data-src must actually attach it when
 *            scrolled to. Needs Chrome; WARNs and exits 0 without one.
 *
 * THE SECOND HALF IS NOT OPTIONAL POLISH. Deferring is trivial to prove and
 * worthless on its own: a trailer that defers and never attaches is a blank box,
 * which is worse than the bytes it saved. Both arms are taken on ONE load of the
 * SAME page, differing only in whether the element has been scrolled to.
 *
 * IT HAS ALREADY DISTINGUISHED A BROKEN HARNESS FROM A BROKEN FEATURE. The
 * in-app browser pane snapshots local files into a context where innerHeight is
 * 0, so nothing can intersect anything and a freshly-created observer times out.
 * That reads exactly like a dead feature. Being able to tell those apart is half
 * the value here.
 *
 * WHAT IT CANNOT SEE, stated in the header for the same reason conformance.js
 * states its own blindness: it does not judge whether the trailer looks right,
 * whether the poster matches the video, whether playback is smooth, or how long
 * any of it took. It answers exactly two questions — was it absent before, and
 * was it present after.
 *
 *   node scripts/mediadefer.js           the two halves, summary only
 *   node scripts/mediadefer.js --show    every measurement, because a silent
 *                                        pass and a dead check read the same
 */
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawn } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const PUBLIC = path.join(ROOT, 'public');
const SHOW = process.argv.includes('--show');

const CANDIDATES = [
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
  (process.env.LOCALAPPDATA || '') + '\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
];

const MEDIA_EXT = /\.(mp4|webm|m4v|jpg|jpeg|png|webp|avif)$/i;

function walk(dir, out) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (e.name.endsWith('.html')) out.push(p);
  }
  return out;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/* ---- half one: nothing eager, decided from the file --------------------- */

/* SCOPED TO <video>, AND THE FIRST RUN IS WHY.
 *
 * This began as "no eager src or poster pointing at media, anywhere". Run
 * against the real tree it immediately flagged two screenshots on
 * tools/sky-ledger.html — both of which carry loading="lazy" and are deferred by
 * the browser natively. The rule was wrong, not the page.
 *
 * A <video> is the case that needs a check, because there is no native lazy
 * attribute for one and `autoplay` overrides `preload` to pull the whole file
 * during first paint. That is the 2,191,073 bytes this exists to hold down.
 * Images are counted and reported, never failed: an <img> without
 * loading="lazy" is worth seeing and is not this file's subject.
 *
 * The negative lookbehind is what separates `src=` from `data-src=`: the whole
 * change under test is that the second exists and the first does not.
 */
const EAGER = /(?<![\w-])(src|poster)="([^"]*)"/g;

function staticHalf(pages) {
  const eager = [];
  const deferred = [];
  let imgLazy = 0;
  let imgEager = 0;
  for (const p of pages) {
    const html = fs.readFileSync(p, 'utf8');

    for (const m of html.matchAll(/<video\b[^>]*>/g)) {
      for (const a of m[0].matchAll(EAGER)) {
        if (MEDIA_EXT.test(a[2])) eager.push([p, a[1], a[2]]);
      }
      for (const a of m[0].matchAll(/data-(src|poster)="([^"]*)"/g)) {
        if (MEDIA_EXT.test(a[2])) deferred.push([p, a[1], a[2]]);
      }
    }

    for (const m of html.matchAll(/<img\b[^>]*>/g)) {
      // The URL, not the whole `src="..."`. Matching the attribute and testing
      // the extension against it counted 0 lazy and 0 eager on a tree holding
      // both, because the trailing quote defeated the anchored extension test -
      // a branch reporting a comfortable zero, which is the fault this whole
      // file exists to argue about.
      const src = (m[0].match(/(?<![\w-])src="([^"]*)"/) || [])[1];
      if (!src || !MEDIA_EXT.test(src)) continue;
      /\bloading="lazy"/.test(m[0]) ? imgLazy++ : imgEager++;
    }
  }
  return { eager, deferred, imgLazy, imgEager };
}

/* ---- half two: it still arrives ---------------------------------------- */

class CDP {
  constructor(ws) {
    this.ws = ws;
    this.id = 0;
    this.pending = new Map();
    ws.addEventListener('message', (ev) => {
      const m = JSON.parse(ev.data);
      if (m.id === undefined) return;
      const p = this.pending.get(m.id);
      if (!p) return;
      this.pending.delete(m.id);
      m.error ? p.reject(new Error(m.error.message)) : p.resolve(m.result);
    });
  }
  send(method, params, sessionId) {
    const id = ++this.id;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params, sessionId }));
    });
  }
}

async function getJSON(url, tries = 60) {
  for (let i = 0; i < tries; i++) {
    try {
      const r = await fetch(url);
      return await r.json();
    } catch (e) { await sleep(100); }
  }
  throw new Error('browser never opened its debugging port');
}

/* Which pages hold a deferred video, and under what ids. Derived from the built
 * HTML rather than listed here: a hand-kept list is how "5 maps" outlived the
 * maps, and a new deferred trailer must be covered without anyone remembering
 * to add it. */
function targets(pages) {
  const byPage = new Map();
  for (const p of pages) {
    const html = fs.readFileSync(p, 'utf8');
    for (const m of html.matchAll(/<video\b[^>]*>/g)) {
      const tag = m[0];
      if (!/\bdata-src="/.test(tag)) continue;
      const id = (tag.match(/\bid="([^"]+)"/) || [])[1];
      if (!id) continue;
      if (!byPage.has(p)) byPage.set(p, []);
      byPage.get(p).push(id);
    }
  }
  return byPage;
}

async function runtimeHalf(bin, byPage) {
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'eql-media-'));
  const port = 9800 + (process.pid % 150);
  const child = spawn(bin, [
    '--headless=new',
    `--remote-debugging-port=${port}`,
    `--user-data-dir=${profile}`,
    '--no-first-run', '--no-default-browser-check', '--disable-gpu',
    '--disable-extensions', '--disable-background-networking', '--disable-sync',
    '--mute-audio', '--hide-scrollbars',
    // Headless refuses to start playback without this, which would look exactly
    // like the observer failing to attach. Autoplay policy is not what is under
    // test here; attachment is.
    '--autoplay-policy=no-user-gesture-required',
    'about:blank',
  ], { stdio: 'ignore' });

  let cleaned = false;
  const cleanup = () => {
    if (cleaned) return;
    cleaned = true;
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
  await cdp.send('Emulation.setDeviceMetricsOverride',
    { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false }, sessionId);
  await cdp.send('Page.enable', {}, sessionId);

  const evaluate = async (expression) => {
    const r = await cdp.send('Runtime.evaluate',
      { expression, returnByValue: true, awaitPromise: true }, sessionId);
    return r.result && r.result.value;
  };

  const results = [];
  for (const [page, ids] of byPage) {
    const url = 'file:///' + page.split(path.sep).join('/');
    await cdp.send('Page.navigate', { url }, sessionId);
    await sleep(2500);

    // A zero-height viewport cannot report an intersection, and that failure is
    // indistinguishable from a broken observer. Say which one it is.
    const innerH = await evaluate('window.innerHeight');
    if (!innerH) {
      results.push({ page, id: '(all)', harness: true });
      continue;
    }

    const state = (id) => `(function(){var v=document.getElementById(${JSON.stringify(id)});
      return v?JSON.stringify({present:true,src:v.hasAttribute('src'),
        poster:v.hasAttribute('poster'),paused:v.paused}):JSON.stringify({present:false});})()`;

    for (const id of ids) {
      const before = JSON.parse(await evaluate(state(id)));
      await evaluate(`(function(){var v=document.getElementById(${JSON.stringify(id)});
        if(v) v.scrollIntoView(); return 1;})()`);
      await sleep(1600);
      const after = JSON.parse(await evaluate(state(id)));
      results.push({ page, id, before, after });
    }
  }
  cleanup();
  return results;
}

/* ------------------------------------------------------------------------ */

(async () => {
  if (!fs.existsSync(PUBLIC)) {
    console.log('WARN  no public/ directory. Run ./build.sh first.');
    process.exit(0);
  }
  const pages = walk(PUBLIC, []);
  const rel = (p) => path.relative(ROOT, p).split(path.sep).join('/');

  const { eager, deferred, imgLazy, imgEager } = staticHalf(pages);
  console.log(`  ${pages.length} built page(s) read`);

  let failed = 0;
  if (eager.length) {
    failed += eager.length;
    console.log(`\n  ${eager.length} EAGER <video> media reference(s) — fetched before`
      + ' a reader has seen anything:');
    for (const [p, attr, url] of eager) console.log(`    ${rel(p)}  ${attr}="${url}"`);
  } else {
    console.log('  eager src/poster on a <video>: none');
  }
  console.log(`  images: ${imgLazy} lazy, ${imgEager} eager (reported, not failed)`);

  if (SHOW) {
    for (const [p, attr, url] of deferred) console.log(`    deferred  ${rel(p)}  data-${attr}="${url}"`);
  }

  const byPage = targets(pages);
  const nvid = [...byPage.values()].reduce((a, b) => a + b.length, 0);

  // Zero examined is not a pass. If every deferred video disappeared, that is
  // either a deliberate removal or the regression this file exists to catch,
  // and the two must not print the same way.
  if (!nvid) {
    console.log('\nWARN  no deferred <video> found in any built page, so the runtime half'
      + ' examined nothing.\n      If the trailers were removed deliberately this file has'
      + ' no subject left and should go.');
    process.exit(failed ? 1 : 0);
  }
  console.log(`  ${nvid} deferred video(s) across ${byPage.size} page(s)`);

  const bin = CANDIDATES.find((c) => c && fs.existsSync(c));
  if (!bin) {
    console.log('\nWARN  no browser installed, so the runtime half did not run. The static'
      + ' half passed.\n      Nothing here says the trailers still arrive when scrolled to.');
    process.exit(failed ? 1 : 0);
  }

  const results = await runtimeHalf(bin, byPage);
  console.log('');
  for (const r of results) {
    if (r.harness) {
      console.log(`  [harness    ] ${rel(r.page)} — viewport height 0, so nothing can`
        + ' intersect. This is the harness failing, not the page.');
      failed++;
      continue;
    }
    const ok = r.before.present && !r.before.src && !r.before.poster
      && r.after.src && r.after.poster;
    if (!ok) failed++;
    if (ok && !SHOW) {
      console.log(`  [deferred+attached] ${r.id}`);
    } else {
      console.log(`  ${ok ? '[deferred+attached]' : '[FAIL             ]'} ${r.id}`
        + `  ${rel(r.page)}\n      before: present=${r.before.present} src=${r.before.src}`
        + ` poster=${r.before.poster}\n      after:  src=${r.after.src}`
        + ` poster=${r.after.poster} paused=${r.after.paused}`);
    }
  }

  if (failed) {
    console.log(`\n${failed} problem(s). Either media is fetched eagerly again, or it is`
      + ' deferred and never arrives.\nA blank box is worse than the bytes it saved.');
    process.exit(1);
  }
  console.log('\nNo media is fetched before first paint, and every deferred trailer'
    + ' attached when scrolled to.\nThis says nothing about how any of it looks, or how long'
    + ' it took.');
  process.exit(0);
})().catch((e) => {
  console.log('mediadefer: ' + e.message);
  process.exit(1);
});
