/* What does every heading on a page actually LOOK like? Dump it, change something,
 * dump it again, and diff. The pair is the measurement; neither half is one alone.
 *
 * WHY THIS EXISTS
 *
 * On 1 Sep 2026 the shared footer's five <h4> column labels became <nav aria-label>
 * groups, because they are navigation and were never document sections. That fixed
 * a skipped heading level on 703 of 717 pages. Promoting the ten pages underneath
 * it - card titles sitting directly under the <h1> with no <h2> anywhere - fixed
 * the rest.
 *
 * Every one of those promotions moved an element out from under a bare `h3{}`
 * element rule. site.css has a bare `h3{}` and NO bare `h2{}`, so a promoted
 * heading that carried no class silently lost its entire appearance: Saira
 * Condensed 22px uppercase became browser-default Public Sans, mixed case. Seven
 * pages did that at once.
 *
 * check.py passed. toolsmoke.js passed. conformance.js passed. Nothing overflowed,
 * nothing threw, no body was empty, every link resolved. The defect is invisible
 * to every check this repo owns, and it is invisible in the diff too - the diff
 * says `<h3>` became `<h2>`, which is what was intended.
 *
 * THE FONTS OBJECTION, AND WHY IT DOES NOT APPLY
 *
 * CLAUDE.md forbids extending conformance.js to judge type, and it is right:
 * that script aborts every non-file request, so the three Google-hosted faces
 * fall back and it would be measuring a page which does not ship.
 *
 * This script aborts them too. It gets away with it because it never judges a
 * measurement - it only compares two of them. Both builds fall back identically,
 * so the handicap cancels and any surviving difference is real. An absolute read
 * would be worthless here; a differential one is sound. Do not add a threshold,
 * a target value, or a pass/fail to this file. The moment it judges a single
 * build on its own it inherits the objection and becomes wrong.
 *
 * It also reports font-family, which IS affected by the fallback - the name will
 * read as the fallback, not the shipped face. That is fine for a diff and a lie
 * as an absolute. Same rule.
 *
 * USE
 *
 *   git archive origin/main public | tar -x -C /tmp/before
 *   node scripts/headstyle.js /tmp/before index.html learn/index.html > before.txt
 *   node scripts/headstyle.js .          index.html learn/index.html > after.txt
 *   diff before.txt after.txt
 *
 * A change that only moves heading LEVELS should diff in the element column and
 * nowhere else. Compare with the element column dropped to see that directly.
 *
 * scripts/toolrender.js is the same idea for what a tool renders. This is the one
 * for how a page reads.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawn } = require('child_process');

const CANDIDATES = [
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
  (process.env.LOCALAPPDATA || '') + '\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
];
const bin = CANDIDATES.find((c) => c && fs.existsSync(c));
if (!bin) {
  console.log('WARN  no browser installed; cannot read computed type. Skipped.');
  process.exit(0);
}

const root = process.argv[2];
const pages = process.argv.slice(3);
if (!root || !pages.length) {
  console.log('usage: node scripts/headstyle.js <build-root> <page> [<page> ...]');
  console.log('  <build-root> contains public/. Use "." for this tree.');
  process.exit(2);
}

class CDP {
  constructor(ws) {
    this.ws = ws; this.id = 0; this.pending = new Map();
    ws.addEventListener('message', (ev) => {
      const m = JSON.parse(ev.data);
      if (m.id === undefined) return;
      const p = this.pending.get(m.id); if (!p) return;
      this.pending.delete(m.id);
      m.error ? p.reject(new Error(m.error.message)) : p.resolve(m.result);
    });
  }
  send(method, params, sessionId) {
    const id = ++this.id;
    return new Promise((res, rej) => {
      this.pending.set(id, { resolve: res, reject: rej });
      this.ws.send(JSON.stringify({ id, method, params, sessionId }));
    });
  }
}
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function getJSON(url, tries = 60) {
  for (let i = 0; i < tries; i++) {
    try { return await (await fetch(url)).json(); } catch (e) { await sleep(100); }
  }
  throw new Error('no debugging port');
}

/* p.fh is in the selector because the footer labels are no longer headings and a
 * diff that lost sight of them would call their removal a clean pass. */
const PROBE = `(function(){
  var out = [];
  document.querySelectorAll('h1,h2,h3,h4,h5,h6,p.fh').forEach(function(e){
    var s = getComputedStyle(e);
    var t = (e.textContent || '').replace(/\\s+/g, ' ').trim().slice(0, 34);
    out.push([t, e.tagName.toLowerCase(), s.fontFamily.split(',')[0].replace(/"/g, ''),
              s.fontSize, s.fontWeight, s.letterSpacing, s.textTransform,
              s.color, s.marginBottom].join(' | '));
  });
  return JSON.stringify(out);
})()`;

(async () => {
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'eql-head-'));
  const port = 9800 + (process.pid % 90);
  const child = spawn(bin, ['--headless=new', `--remote-debugging-port=${port}`,
    `--user-data-dir=${profile}`, '--no-first-run', '--disable-gpu', 'about:blank'],
    { stdio: 'ignore' });
  const done = () => {
    try { child.kill(); } catch (e) {}
    try { fs.rmSync(profile, { recursive: true, force: true }); } catch (e) {}
  };
  process.on('exit', done);

  const v = await getJSON(`http://127.0.0.1:${port}/json/version`);
  const ws = new WebSocket(v.webSocketDebuggerUrl);
  await new Promise((r, j) => { ws.addEventListener('open', r); ws.addEventListener('error', j); });
  const cdp = new CDP(ws);
  const { targetId } = await cdp.send('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await cdp.send('Target.attachToTarget', { targetId, flatten: true });
  await cdp.send('Page.enable', {}, sessionId);

  let n = 0;
  for (const rel of pages) {
    const file = path.resolve(root, 'public', rel);
    console.log(`### ${rel}`);
    if (!fs.existsSync(file)) { console.log('  (absent in this build)'); continue; }
    const url = 'file:///' + file.split(path.sep).join('/');
    await cdp.send('Page.navigate', { url }, sessionId);
    await sleep(900);
    const r = await cdp.send('Runtime.evaluate',
      { expression: PROBE, returnByValue: true }, sessionId);
    const lines = JSON.parse(r.result.value);
    // A page with no headings and a page that failed to load read the same in a
    // diff. Say which one it was.
    if (!lines.length) console.log('  (no headings on this page)');
    for (const line of lines) { console.log('  ' + line); n++; }
  }
  console.log(`\n${n} heading(s) measured across ${pages.length} page(s).`);
  console.log('This is one half of a measurement. Diff it against the other build.');
  done();
  process.exit(0);
})().catch((e) => { console.log('probe error: ' + e.message); process.exit(1); });
