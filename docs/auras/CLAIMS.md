# EQL Auras band — the claim set

Every factual assertion in the band copy, and what backs it. For the Director to
adjudicate before it ships.

> **⚠ RE-READ 3 September 2026 against `LoxyBee/EQLS-Auras@3a4d119c` (version
> 1.0.0). Two claims below went stale, and both went stale in the direction that
> flatters the tool — see §5 and §9.** That direction is the finding: a staleness
> that makes a product look worse gets caught by whoever is proud of it; one that
> makes it look cleaner has nobody hunting for it.
>
> **The original read was against a delivered zip; this one is against the live
> repository at a named ref.** A zip cannot be re-read by anyone else — which is
> why the corrections below name a commit instead.

Line references are to the Auras project source as delivered in `EQ tracker.zip`
(`EQ Buff Tracker`, version 0.1.0), read 18 August 2026. Video references are to
`EQ AURAS BURST.mp4` as delivered.

**Three things are flagged and need your decision: §7, §11, and the caveats
under §5 and §6. Everything else is backed by the source.**

---

## Backed by the source

**1. "It reads your combat log."**
`src/main/logWatcher.js:7` tails files matching the pattern `eqlog_*.txt`,
polling every 200ms, always following whichever matching file was modified most
recently. The project describes itself the same way at `package.json:5`.

**2. "draws your buffs over the game as icons that count down"**
Overlay windows are `frame: false`, `transparent: true`, `alwaysOnTop: true`
(`src/main/widgetManager.js:84-88`) and click-through when locked (`:104`,
`:356`). Icon-grid mode with per-icon countdown text is
`src/renderer/overlay/overlay.js:471`, `:681`. Visible in the video: fourteen
buff tiles across the top of the screen, each showing its own remaining time.

**3. "so you can see what is about to drop off without opening a window"**
The overlay is always-on-top and click-through, so it needs no interaction. A
per-widget expiring-soon flash turns a tile red under a set threshold — the
setting is on screen in the tutorial video, described there as "when a buff's
remaining time drops under this, its tile flashes red".

**4. "It reads files the client already has: the log it writes as you play,
your spellbook, and the game's own spell icons."**
Three sources, all read-only: the log (§1); the character's spellbook text file
in the install root, re-read every 30s (`src/main/spellbookService.js:5-14`,
`:52`, `:69`); and the game's real spell icon art under `Textures/`, decoded by
a hand-rolled TGA reader (`src/main/iconExtractor.js:64-68`, `:83-85`).

**This sentence replaced a draft that said "the log file, and nothing else".**
That would have been false. It is exactly the kind of clean line that survives
review because nobody thinks to check a claim that flatters the tool.

**5. "It does not read or alter the game's memory, inject code into it, or send
it input."**
A negative, so here is what was searched for and **not** found anywhere in the
first-party source: `ReadProcessMemory`, `WriteProcessMemory`, `OpenProcess`,
`VirtualAlloc`, `CreateRemoteThread`, `LoadLibrary`, `SetWindowsHookEx`,
`SendInput`, `keybd_event`, `mouse_event`, `node-ffi`, `ffi-napi`, `memoryjs`,
`robotjs`, `iohook`, `nut-js`, DLL loading, native `.node` bindings, `node-gyp`,
`desktopCapturer`, ~~`globalShortcut`~~.

> **⚠ CORRECTED 3 Sep 2026: `globalShortcut` is now PRESENT** at
> `src/main/main.js:182-193`, and it is on this list as absent. **The claim it
> supports nevertheless survives, and the reason is the point:** it registers a
> *hide-auras* hotkey — **it receives a key press, it never sends one.** Sending
> input to the game would be `SendInput` / `keybd_event` / `mouse_event`, and all
> three remain absent. **So "does not send it input" is still true.**
>
> Kept here with its reason rather than quietly deleted, because a correction that
> drops the reason invites the next reader to re-open it. Every other token on this
> list was re-run against `3a4d119c` and remains absent.

It is also structurally hard for any of those to be present: `package.json:11-14`
declares **no runtime dependencies at all**, only `electron` and
`electron-builder` for development. Every import in the tree is a Node builtin
or `electron` itself.

> **Caveat, flagged.** There is exactly one Windows-API path, at
> `src/main/foregroundWatcher.js`. Every two seconds it runs a PowerShell
> P/Invoke calling `GetForegroundWindow` and `GetWindowThreadProcessId`
> (`:21-34`), then reads that process's **name** and compares it to `eqgame`
> (`:12`, `:68`), so the overlay can hide itself when you alt-tab away.
>
> It never opens a handle to the game, never targets the game process and never
> reads its memory, so the sentence as written stays true. But "it never uses a
> Windows API in relation to the game" would be false, and I have deliberately
> not written that. **Your decision:** the band omits this nuance for space. I
> think that is right for a band and wrong for the tool page, which should state
> it plainly.

**6. "It makes no network requests of its own — no telemetry, no analytics, no
update check."**
Zero matches under `src/` for `fetch`, `axios`, the `http` and `https` modules,
`XMLHttpRequest`, `WebSocket`, `net`, `dgram`, `autoUpdater`, `electron-updater`,
`telemetry`, `analytics`, `sentry`, `posthog`, `mixpanel`, `crashReporter`.

> **⚠ CORRECTED 3 Sep 2026. The sentence below is FALSE as of `3a4d119c`, and it
> was false within hours of being written.** The font link landed **18 Aug at
> 12:11** in `1fe8fb49` — the same day this file was written, shortly after.
>
> **There ARE URLs in the shipped source.** `src/renderer/main-window/index.html`
> lines 19–21 preconnect to `fonts.googleapis.com` and `fonts.gstatic.com` and
> fetch Poppins as a stylesheet. **So the main window discloses the user's IP to
> Google at launch.**
>
> **The precision matters and `public/auras.html:111` already has it right:** nine
> renderer windows *permit* Google Fonts in their CSP; **exactly one *requests* it.**
> Permitting and requesting are different facts and only one of them discloses an
> IP. The overlay drawn over the game requests nothing at all. **No change to
> `auras.html` is needed — it is the accurate page.**
>
> **What survives unchanged, re-run against `3a4d119c` rather than inherited:**
> `fetch`, `XMLHttpRequest`, `WebSocket`, the `http`/`https` modules, `autoUpdater`,
> `electron-updater`, `telemetry`, `analytics`, `sentry`, `crashReporter` are **all
> still absent**, and renderer CSP sets `connect-src 'none'`. **"No telemetry, no
> analytics, no update check" is still true.** Only "makes no network requests of
> its own" is not, and it has been struck from the band copy.

~~Stronger than that: a search of the entire `src/` tree — including the
86,511-line bundled buff roster — for `http://`, `https://`, `www.`, `.com`,
`.net`, `.org` and `ws://` returns **nothing**. There is not one URL in the
shipped source.~~ All three window types run `contextIsolation: true`,
`nodeIntegration: false`, `sandbox: true`. Widget sharing is an offline
`EQBT2-` string the user copies to their clipboard, not a service
(`src/main/widgetStore.js:225`, `:516-526`).

> **Caveat, flagged, and the reason the copy says "of its own".** This is a
> statement about the application's code, not about the Electron/Chromium
> runtime beneath it. The project's own handoff records a Windows
> location-access prompt that was traced to routine Electron behaviour, with
> nothing in the app requesting geolocation. **"of its own" is load-bearing and
> should not be edited out.**

**8. "The code is not [WeakAuras']: a from-scratch implementation for EverQuest
Legends, sharing no code and no trigger format with it."**
Strongly backed. No Lua anywhere. No WeakAuras code, data or format. Its only
import format is its own — an `EQBT2-` prefix over compressed JSON, rejecting
any unrecognised prefix (`src/main/widgetStore.js:225`, `:512-533`). A
WeakAuras string would be refused. The detection engine is built on
EverQuest-specific log grammar with no WoW analogue: EQ publishes no universal
"buff landed" message, so each spell's own flavour text was mined and is matched
exactly (`src/main/buffParser.js:1-9`, `:15-45`).

**9. "neither affiliated with nor endorsed by its authors."**
Ours to assert, and true: nothing in the project claims any relationship, and
there is none. A disclaimer about our own standing needs no external source.

**10. "Windows."**
`package.json:17-21` builds one target, Windows NSIS. The code is Windows-only
regardless: PowerShell, `C:\` install paths, `eqgame.exe`.

**12. Caption: "9s, silent."**
The encoded file is 8.916s and carries **no audio stream at all** — `ffprobe`
reports a single stream, index 0, video. "9s" rounds 8.9 up.

**13. The `aria-label` describing the video.**
"A Quick Buff cast landing on screen, and the overlay filling with fourteen buff
icons." The casting bar reads Quick Buff and its tooltip is on screen: it "will
cast all currently memorized beneficial spells on all valid group and raid
targets in range". Fourteen tiles are countable in the frame — Resist Magic,
Guard of Druzzil, Blessing of Faith, Symbol of Naltron, Blessing of the…,
Stamina, Strength, Dexterity, Agility, Charisma, Resolution, Infusion, Talisman,
Shield of Words.

---

## Flagged — not backed by the source

**7. "The idea is WeakAuras'."** — **needs your word. It is the one claim in the
band I cannot source.**

The source does not mention WeakAuras anywhere. Every first-party file was
searched, case-insensitively, for `weakaura`, `weak aura`, `wago`, `warcraft`,
`wow`, `lua`, `addon` and the bare word `aura`: **zero matches** in code,
comments, docs, naming or file formats.

So "modelled on WeakAuras" is a claim about **design intent**, and the only
person who can source it is the author. Your brief states it as fact, and I have
taken your instruction as the author's statement rather than inventing a
citation — but you asked me to flag what I cannot back, and this is it.

The wording puts the weight on the half that *is* backed. "The idea is
WeakAuras'" credits an influence; it does not assert that any WeakAuras artefact
is present. The sentence after it, which is the load-bearing one for accuracy,
is fully evidenced (§8).

**If the author confirms the influence, ship as written.** If they will not, cut
four words to "A from-scratch implementation for EverQuest Legends…" and the
paragraph still works — though the site then loses a credit it would normally
give, which is why I would rather you got the confirmation.

**11. "Targeting next Tuesday's maintenance."** — **the date's only source is
you.**

Nothing in the project backs a date: no changelog, no release notes, no tags, no
roadmap. What the source does say cuts the other way — the project's own handoff
records **"Status: dev build only, nothing shipped"**, the version is `0.1.0`, a
full main-window redesign is marked "planning only, nothing implemented yet",
and one open bug is documented at length with no code written against it.

That is not an argument against the band. It is the argument for the qualifier.
**"Targeting" is doing real work here and must not be softened to "releasing".**
The video is the evidence; the date is an intention. Written this way the claim
is honest, because it claims an intention rather than an event.

---

## Not in the copy, and why

**Licence. ⚠ CORRECTED 3 Sep 2026 — this reversed, and the old text forbids
something now permitted.**

~~There is no LICENSE file, no `license` field... Do not describe it as open
source, free, or redistributable anywhere.~~

At `3a4d119c` there **is** a `LICENSE` file — **MIT** — and `package.json`
carries `"license": "MIT"`. It is also in `build.files`, so it ships with the
installer. **The code is MIT licensed: open source, and redistributable under
those terms.**

`"private": true` is still set, but that is npm's publish guard, not a statement
about rights, and it was doing no work in the original conclusion.

**The band's "Free." is safe on both readings** — free of charge, and now free as
in licence. The original caution was right for 18 August and would be wrong to
carry forward.

**No roster figure. ⚠ CORRECTED 3 Sep 2026 — every number in the struck text
below is wrong, and so is the direction of the error.**

~~The bundled data file holds 11,337 buff entries... the About page understates
their work threefold.~~

At `3a4d119c`: the roster the app loads is `src/shared/data/buffs.json`,
**1,067 entries**, loaded at `src/main/buffStore.js:43`. The 11,337 file is
`archive/buffs-legacy-11337.json`, referenced by **no shipped code** and **not
inside the installer** — `build.files` is
`['src/**/*','package.json','build/icon.ico','LICENSE']` and `archive/` is not in
it. **And the About page states no roster count at all**; `~3300` is a code
comment at `buffStore.js:285`.

**So the advice inverted: the figure did not understate the work threefold, it
overstated it by 10.6×.** The original reasoning was still right — print it from
the data at build time rather than typing it beside the copy. **A hand-typed
figure goes stale silently, which is what happened here.** The printable figure
is **1,067**.

**No feature that is only planned. ⚠ PARTLY CORRECTED 3 Sep 2026 — sound
shipped.**

~~Sound is synthesised tones, not sound files; user-supplied audio... unbuilt.~~
At `3a4d119c` the installer ships **15 real audio files** under `sounds/` (via
`build.extraFiles`), and `docs/HIGHLIGHTS.md` lists user-supplied audio as built:
*"Use your own sound files. Any audio file on your PC."* **The band's "15 sounds"
is counted from the shipped directory, not from that claim.**

The dispel notification and bard-song widget were **not** re-checked; treat them
as unverified rather than as still-unbuilt. The band claims none of
them. Two controls in the tutorial video are visibly labelled "planned", which
is a reason not to cut promotional stills from the settings screens.
