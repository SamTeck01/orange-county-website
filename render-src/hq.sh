#!/bin/bash
cd /tmp/claude-0/-home-user-orange-county-website/79bc8f36-fcdf-57d9-86dc-616179bddea7/scratchpad/epe2
until grep -q "FILM_DONE v2" hq_v2.log 2>/dev/null; do python3 film.py -- v2 render >> hq_v2.log 2>&1; done
python3 -c "
from PIL import Image; import glob, os
for f in sorted(glob.glob('film_v2_hq/f_*.png')):
  try: Image.open(f).verify()
  except Exception: os.remove(f)"
python3 film.py -- v2 render >> hq_v2.log 2>&1
python3 dissolve.py film_v2_hq v2_hq_out >> hq_v2.log 2>&1
FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
$FF -y -framerate 24 -i v2_hq_out/o_%05d.png -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -movflags +faststart -an Orange_County_Epe_Film_720p.mp4 > /dev/null 2>&1
echo HQ_DONE >> hq_v2.log
