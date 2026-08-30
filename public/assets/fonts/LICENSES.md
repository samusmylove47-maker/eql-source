# The four faces, and the licence each ships under

Every file in this directory is served from this origin so that reading a page on
this site does not disclose your IP address to a third party. Until 30 August
2026 they were fetched from Google on every page load.

All four families are licensed under the **SIL Open Font License, Version 1.1**.
The full licence text is at <https://scripts.sil.org/OFL>.

| Family | Copyright | Weights served |
|---|---|---|
| **Cinzel** | Copyright (c) Natanael Gama | 500, 600, 700 |
| **IBM Plex Mono** | Copyright (c) IBM Corp. | 400, 500, 600 |
| **Public Sans** | Copyright (c) United States Government | 400, 600 |
| **Saira Condensed** | Copyright (c) Omnibus-Type | 600, 700 |

## Why the files are unmodified, and why that matters

They are **byte-identical copies** of what Google's font service served, fetched
once by `_build/fetchfonts.py` and committed. The `@font-face` blocks and their
`unicode-range` values in `fonts.css` are Google's, unchanged; only the `src`
URLs were rewritten to point here.

That is deliberate on two counts.

**Rendering.** Reproducing Google's own subsetting exactly means a glyph that
rendered yesterday renders today. A hand-rolled subset would differ, and the
difference would stay invisible until some page needed a character the subset had
dropped. `U+2212 MINUS SIGN` is the specific hazard on this site — it appears in
every published coordinate — and it sits in Google's `latin` range, which is
carried over intact.

**Naming.** OFL 1.1 clause 3 reserves a font's name for its author, and forbids a
**Modified Version** from using it. Subsetting a font produces a Modified
Version. Because these files are unmodified, the restriction does not apply and
they are served under their real names.

This is why the EQLS Lockouts application, which *does* subset its embedded
faces, ships two of them renamed to **EQLS Mono** and **EQLS Condensed**. Same
licence, different obligation, because it took a step we did not.

## Regenerating

```bash
python3 _build/fetchfonts.py
```

Hand-run, never part of `build.sh` — it needs the network, and a rebuild must
work on a machine that has none. Its output is committed. The same rule governs
`_build/geometry.py` and `_build/ogcards.py`.
