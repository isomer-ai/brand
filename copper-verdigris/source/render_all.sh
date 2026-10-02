#!/usr/bin/env bash
# Rebuild every plate, animation, poster frame and the page. Needs: python3, cairosvg, ffmpeg,
# and Fustat + IBM Plex Mono installed as system fonts (for PNG and video text).
set -euo pipefail
cd "$(dirname "$0")"
python3 export.py
python3 anim.py
python3 anim2.py
python3 anim3.py
cd ../animations
ffmpeg -y -loglevel error -framerate 30 -i _frames/point-of-receipt-16x9/f%04d.png \
  -vf "fps=15,scale=960:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse=dither=none" point-of-receipt-16x9.gif
for f in *.mp4; do ffmpeg -y -loglevel error -sseof -0.5 -i "$f" -frames:v 1 -vf scale=720:-1 "${f%.mp4}-poster.png"; done
rm -rf _frames
cd ../source && python3 build_page.py && python3 build_logos.py
