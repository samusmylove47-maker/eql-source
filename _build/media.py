#!/usr/bin/env python3
"""Copy the committed media into public/ under a content hash.

WHY A HASH
----------
Same reason the stylesheet and the Sky Ledger carry one. A reader who has the
trailer cached keeps it until the URL changes, and a silent stale video is
worse than a stale page: it shows the tool behaving in a way it no longer
behaves. The hash makes a changed file a different cache key.

WHY THE SOURCE LIVES IN _media/
-------------------------------
public/ is generated and a rebuild throws away anything edited in place. The
originals sit outside it and are committed, so the build is reproducible on a
machine that never had the raw capture.

WHAT IT WILL NOT DO
-------------------
Re-encode. The 18-second trailer arrived as a 20.4 MB 1920x1080 screen capture
at 8.9 Mbps, which is heavier than every other asset on this site put together
and would have been the first thing a phone downloaded. It was encoded once, by
hand, to 1600x900 at CRF 28 with no audio track, and the result is committed.
Encoding on every build would need ffmpeg present, and CLAUDE.md's rule for
geometry.py applies here too: a rebuild must work on a machine without the
tools that made the input.
"""
import hashlib
import glob
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SRC = '_media'
DST = os.path.join('public', 'assets', 'media')


def main():
    if not os.path.isdir(SRC):
        print('media: no _media/ directory, nothing to copy')
        return
    os.makedirs(DST, exist_ok=True)
    manifest, keep = {}, set()
    for path in sorted(glob.glob(os.path.join(SRC, '*'))):
        if not os.path.isfile(path):
            continue
        blob = open(path, 'rb').read()
        short = hashlib.sha1(blob).hexdigest()[:8]
        stem, ext = os.path.splitext(os.path.basename(path))
        name = f'{stem}.{short}{ext}'
        keep.add(name)
        out = os.path.join(DST, name)
        if not os.path.exists(out):
            # Written as bytes. Re-encoding a video through a text path is the
            # kind of corruption that only shows up in a browser.
            with open(out, 'wb') as fh:
                fh.write(blob)
        manifest[stem] = dict(file=name, bytes=len(blob),
                              kb=round(len(blob) / 1024))
    # An earlier build's copy is dead weight and, worse, still reachable.
    for old in sorted(glob.glob(os.path.join(DST, '*'))):
        if os.path.basename(old) not in keep:
            os.remove(old)
            print('media: dropped', os.path.basename(old))
    import json
    json.dump(manifest, open('assets/media.json', 'w', encoding='utf-8',
                             newline='\n'), indent=1, sort_keys=True)
    for stem, rec in sorted(manifest.items()):
        print(f"media: {rec['file']} ({rec['kb']} KB)")


if __name__ == '__main__':
    main()
