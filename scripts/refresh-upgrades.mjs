#!/usr/bin/env node
/* Rewrite assets/50-upgrades.json from the 50 Upgrades planner's live meta.json.
 *
 * WHY THIS EXISTS
 * ---------------
 * The planner is built and refreshed in its own repository. We vendor a
 * snapshot of its meta.json so the description page can print the planner's own
 * accounting rather than our summary of it, and so a rebuild here does not
 * depend on that site being up.
 *
 * Vendoring is the right call and it has a failure mode of its own, which this
 * file exists to close.
 *
 * THE FAULT, WHICH ACTUALLY HAPPENED
 * ----------------------------------
 * The snapshot recorded `counts.items: 3653`. Upstream, `counts.items` was
 * 3663; 3653 is `counts.purge.shipped` — the number of items that survived the
 * era purge, not the number of items the planner holds. The two were equal
 * while `counts.purge.admittedOutsideScrape` was 0, so a figure copied out of
 * the wrong field looked exactly like a figure copied out of the right one, and
 * the page printed the purge-survivor count under the label "Items shipped" for
 * as long as the coincidence held.
 *
 * Nothing was done carelessly to produce that. The number was read from a real
 * field of a real snapshot recording its own source and read-date. What was
 * missing is the one thing that would have caught it: the snapshot never said
 * WHICH FIELD each figure came from.
 *
 * THE FIX IS STRUCTURAL, NOT DILIGENCE
 * ------------------------------------
 * Every figure in the snapshot is keyed by its dotted path in the upstream
 * file, and _build/build29.py looks figures up by that path. So the generator
 * names the upstream field at the point of use, a mismatch between label and
 * field is visible in the source rather than invisible in a number, and a path
 * that no longer exists upstream is a KeyError at build time instead of a
 * plausible wrong quantity on a published page.
 *
 * It is the argument assets/sky.json already makes about truth — a claim names
 * its source rather than inheriting a badge — applied to field selection.
 *
 * HAND-RUN, LIKE geometry.py AND ogcards.py
 * -----------------------------------------
 * It needs the network, and a rebuild must work on a machine that has none.
 * Never wire it into build.sh: a build that silently re-fetches its own
 * vendored inputs is not vendoring them.
 *
 *     node scripts/refresh-upgrades.mjs 2026-08-18
 *
 * The read-date is passed in rather than taken from the clock, because it is
 * the date a person stood behind this snapshot, not the date a script ran.
 */
import { writeFileSync } from 'node:fs';

const SOURCE = 'https://samusmylove47-maker.github.io/EQL50ups/data/meta.json';
const SITE = 'https://samusmylove47-maker.github.io/EQL50ups/';
const OUT = 'assets/50-upgrades.json';

/* The whole contract, and the only place it is written down. Each entry is a
 * path INTO the planner's meta.json, and it becomes the key in the snapshot.
 * A ".length" suffix means the length of the array at that path.
 *
 * Adding a figure to the page means adding its path here. There is deliberately
 * no way to vendor a number without naming where it came from. */
const PATHS = [
  'counts.items',                        // everything the planner holds
  'counts.withSlot',
  'counts.withStats',
  'counts.withEffects',
  'counts.withAcquisition',
  'counts.withNumericId',
  'counts.eraUnknown',
  'counts.statsUnknown',
  'counts.standing.tier-M',
  'counts.standing.tier-2',
  'counts.standing.tier-5',
  'counts.standing.unattributed',
  'counts.purge.before',                 // rows before the era purge
  'counts.purge.shipped',                // survived the era purge — NOT the catalogue size
  'counts.purge.quarantined',
  'counts.purge.catalog',                // agrees with counts.items; kept so the two can be compared
  'counts.purge.admittedOutsideScrape',  // the difference between the two above
  'classes.length',
  'races.length',
  'slots.worn.length',
  'era.current',
  'license.content',
  'license.checked',
  'license.contentSource',
  'attribution',
];

const read = process.argv[2];
if (!/^\d{4}-\d{2}-\d{2}$/.test(read || '')) {
  console.error('usage: node scripts/refresh-upgrades.mjs <YYYY-MM-DD>');
  console.error('       the read-date is the day a person stood behind this snapshot.');
  process.exit(2);
}

const dig = (obj, path) => {
  let cur = obj;
  for (const part of path.split('.')) {
    if (part === 'length' && Array.isArray(cur)) return cur.length;
    if (cur === null || cur === undefined) return undefined;
    cur = cur[part];
  }
  return cur;
};

const res = await fetch(SOURCE);
if (!res.ok) {
  console.error(`fetch failed: ${res.status} ${SOURCE}`);
  process.exit(1);
}
const meta = await res.json();

const figures = {};
const missing = [];
for (const p of PATHS) {
  const v = dig(meta, p);
  if (v === undefined) { missing.push(p); continue; }
  figures[p] = v;
}

/* A path that has vanished upstream is a schema change, and a schema change is
 * exactly the moment a figure quietly becomes a different quantity. Refuse
 * rather than write a snapshot with a hole in it and let the build discover it
 * as a missing key on a page. */
if (missing.length) {
  console.error('MISSING upstream paths — refusing to write:\n  ' + missing.join('\n  '));
  console.error('\nThe planner changed its meta.json shape. Re-read it and update PATHS');
  console.error('deliberately; do not delete the figure to make this pass.');
  process.exit(1);
}

const out = {
  _comment:
    'Vendored snapshot of the 50 Upgrades planner’s own meta.json. EVERY FIGURE IS '
    + 'KEYED BY THE DOTTED PATH IT WAS READ FROM in that file, and _build/build29.py looks '
    + 'them up by that path. A vendored number that does not say which field it is gets read '
    + 'as the wrong quantity eventually, and did: this file carried 3,653 as counts.items '
    + 'until 18 Aug 2026, but 3,653 is counts.purge.shipped. They were equal while '
    + 'counts.purge.admittedOutsideScrape was 0, so the page printed the era-purge survivor '
    + 'count under a catalogue label and nothing could tell. A ".length" suffix is the length '
    + 'of the array at that path.',
  _regenerate: 'node scripts/refresh-upgrades.mjs <YYYY-MM-DD>. Never hand-edit a figure.',
  read,
  source: SOURCE,
  url: SITE,
  built_at: meta.builtAt,
  figures,
};

writeFileSync(OUT, JSON.stringify(out, null, 1) + '\n', { encoding: 'utf8' });
console.log(`${OUT} written: ${Object.keys(figures).length} figures, `
  + `catalogue ${figures['counts.items']}, purge survivors ${figures['counts.purge.shipped']}, `
  + `snapshot built ${meta.builtAt}, read ${read}`);
