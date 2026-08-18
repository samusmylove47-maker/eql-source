# EQLS Auras — the asset spec

Session C encoded these and recorded the reasoning in their handoff note. It is
collected here because a handoff note is read once and a spec is read whenever
someone re-encodes, and the next person to touch this video needs the frame
numbers rather than the summary.

Both files live in `_media/` and are committed. `_build/media.py` hashes them
into `public/assets/media/` and writes `assets/media.json`; **no build change was
needed to add them**, because that script globs the directory.

| File | Size | Shipped as |
|---|---|---|
| `_media/auras-trailer.mp4` | 839 KB | `auras-trailer.5fc3fbbc.mp4` |
| `_media/auras-poster.jpg` | 175 KB | `auras-poster.5c861299.jpg` |

Both 1600x900. The trailer is 8.9s at 24fps and carries **no audio stream at
all** — `ffprobe` reports a single stream, index 0, video.

---

## The encode

Cut from `EQ AURAS BURST.mp4` (35.8s, 1920x1080, 42.8 MB) and encoded once by
hand at **CRF 28, no audio**, which is the Sky Ledger recipe unchanged.

**The one departure is 24fps rather than 30.** At 30 the particle burst came out
at 1,112 KB — heavier than the Sky Ledger trailer despite being half as long. At
24 it is 839 KB, under that trailer's 949 KB, with the documented CRF intact.

`media.py` will not re-encode and must not be made to. A rebuild has to work on
a machine with no ffmpeg, the same rule that keeps `geometry.py` out of
`build.sh`.

## Why it is 8.9 seconds

**The source constrains it; it was not trimmed for weight.** The clip runs from
2.0s to 10.9s in the capture: the Quick Buff cast, then fourteen buff tiles
filling the top of the screen, each counting down.

At **t=11.25 the Windows Start menu opens** in the capture, showing the desktop —
Discord, Outlook, Battle.net, "Update and shut down". At **t=13 the application
window opens** over the game. Session C verified frame by frame that the onset
falls between t=11.0 (clean) and t=11.25 (open), and cut at 10.9. The encoded
file's own first and last frames were checked after encoding, not only the
source.

**Do not extend the out-point** without re-checking those frames. There is a
desktop, with named third-party applications on it, one third of a second past
the end.

## The poster

A frame from inside the clip at **t=10.8**, with the full buff row up.

It is what shows below 700px and under `prefers-reduced-motion`, so it has to
carry the message on its own rather than be a neutral first frame. Verified in
a real browser at 1440x900, 390x844, and at 1440x900 with reduced motion: the
band's script removes `autoplay` in the latter two and the poster is what
renders.

## What the video deliberately does not show

**The application window never appears.** That is incidental to the cut but
useful: the application calls itself *EQ Buff Tracker* — window title, taskbar,
`package.json` — while the site announces **EQLS Auras**. The clash is
invisible in this band and will be obvious on any page carrying a screenshot of
the app. Settle the name before a tool page ships, not before this band does.

---

## Serving it

No iframe, ever. An embed would make the home page issue a third-party request
on load. It is served from our own origin under a content hash.

No control implying sound. There is no audio stream, so a mute button would
offer to silence something that does not exist. The band carries a Pause button
and a caption reading "9s, silent".
