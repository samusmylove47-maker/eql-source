# EQL Auras — landing-page band

Material for Session A, who owns `_build/build1.py` and lands this. Nothing here
was built or rebuilt in this worktree.

`docs/auras/band.html` beside this file is the exact markup the word count was
measured from. Lift the text out of it rather than retyping from the prose
below, so what ships is what was counted.

---

## The copy

**Eyebrow:** Next &middot; **reads your own log**

**Heading:** EQL Auras

> It reads your combat log and draws your buffs over the game as icons that
> count down, so you can see what is about to drop off without opening a window.

> It reads files the client already has: the log it writes as you play, your
> spellbook, and the game's own spell icons. It does not read or alter the
> game's memory, inject code into it, or send it input. It makes no network
> requests of its own &mdash; no telemetry, no analytics, no update check.

> The idea is WeakAuras'. The code is not: a from-scratch implementation for
> EverQuest Legends, sharing no code and no trigger format with it, and neither
> affiliated with nor endorsed by its authors.

**Foot:** Windows. Targeting next Tuesday's maintenance.

**Figure caption:** The overlay in play &middot; 9s, silent

---

## Word count, and the ceiling raise it needs

Measured with `gate.py`'s own `page_words` against `docs/auras/band.html`, so it
is counted the way the ratchet counts rather than by eye.

| Variant | Words | `index.html` becomes | Ceiling must become |
|---|---|---|---|
| **A &mdash; as written above** | **136** | **785** | **785** |
| B &mdash; drop "no telemetry, no analytics, no update check" | 129 | 778 | 778 |
| C &mdash; B, and drop the eyebrow | 124 | 773 | 773 |
| D &mdash; C, and drop the figure caption | 118 | 767 | 767 |

`index.html` is at **649 of 649**. There is no headroom whatsoever, so every one
of these needs a hand edit to `assets/prose-budget.json` with the reason in the
commit message. `prose_budget.py` only ever lowers ceilings, so raising one is a
decision, which is what `CLAUDE.md` requires it to be.

**A is the recommendation.** The trims are listed in the order I would take
them, but B gives up the clause that does the most work per word: an overlay
that reads your log is exactly the thing a reader suspects of phoning home, and
naming the three things it does not do settles that in eight words. D gives up
the caption saying the video is silent, which is worth keeping beside a video
that starts moving on its own.

I would not cut the second paragraph at all. It is the paragraph the reader came
for, and answering it before it is asked is the reason the band can be this short.

---

## Markup

Follow the Sky Ledger band in `_build/build1.py` exactly: same
`<section class="band feat">`, same pause button, same reduced-motion and
narrow-screen script. Only the media keys and the text differ.

    MEDIA['auras-trailer']   _media/auras-trailer.mp4   839 KB   1600x900, 8.9s, 24fps
    MEDIA['auras-poster']    _media/auras-poster.jpg    174 KB   1600x900

`_build/media.py` hashes both on the next build and writes them into
`assets/media.json`. No build change is needed &mdash; the band reads the
manifest exactly as the Sky Ledger band already does.

The file carries **no audio stream at all**, so `muted` is honest rather than
load-bearing. Give it the same `autoplay muted loop playsinline
preload="metadata"` and the same pause control, and the same script that takes
motion away under `prefers-reduced-motion` and below 700px.

---

## Three gate rules this was written around

- **A number in a meta description must appear literally on the page.** This
  copy contains no numerals at all, so it cannot violate this. Do not add a
  figure to `index.html`'s meta description when the band lands.
- **A flat figure within ~260 characters of a hedge word fails.** No figures, so
  it cannot fire. For later: `gate.py`'s `HEDGE` vocabulary contains the bare
  word `import`, so a future Auras page describing how to import a share code
  will trip this if a number sits near it.
- **Any `{token}` reaching visible text fails.** There are no braces in this copy.

---

## Two things for a later page, not for this band

**The name.** The application calls itself **EQ Buff Tracker** &mdash; window
title, taskbar, `package.json`. The band calls it **EQL Auras**. The band's
video never shows the application window, so the clash is invisible here, but it
will be obvious on any page carrying a screenshot of the app.

**The roster figure.** The app's own About page says it knows roughly 3,300
buffs. Its data file holds **11,337** entries, 11,190 of them with landing text.
The About page understates the work by more than a factor of three. That is a
good promotional figure and it is not in this band, because a figure like that
should be printed from the data at build time rather than typed beside it.
