# EQL Auras band — the claim set

Every factual assertion in the band copy, and what backs it. For the Director to
adjudicate before it ships.

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
`desktopCapturer`, `globalShortcut`.

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

Stronger than that: a search of the entire `src/` tree — including the
86,511-line bundled buff roster — for `http://`, `https://`, `www.`, `.com`,
`.net`, `.org` and `ws://` returns **nothing**. There is not one URL in the
shipped source. All three window types run `contextIsolation: true`,
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

**No licence.** There is no LICENSE file, no `license` field, and
`"private": true` (`package.json:6`). The first-party code is unlicensed — all
rights reserved by default. **Do not describe it as open source, free, or
redistributable anywhere.** The site withdrew an unsourceable licence claim
about eqlwiki this week; this is the same shape of mistake waiting to happen.

**No roster figure.** The bundled data file holds 11,337 buff entries, 11,190 of
them with landing text. The app's own About page says roughly 3,300 and is stale
by more than a factor of three. It is a good figure and it is deliberately
absent here: a number like that should be printed from the data at build time,
not typed beside it, and the band has no build step of its own. Worth telling
the author their About page understates their work threefold.

**No feature that is only planned.** Sound is synthesised tones, not sound
files; user-supplied audio, the dispel notification and the bard-song widget are
unbuilt, with disabled placeholders visible in the app. The band claims none of
them. Two controls in the tutorial video are visibly labelled "planned", which
is a reason not to cut promotional stills from the settings screens.
