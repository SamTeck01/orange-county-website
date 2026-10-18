#!/bin/bash
cd /tmp/claude-0/-home-user-orange-county-website/79bc8f36-fcdf-57d9-86dc-616179bddea7/scratchpad/epe2
until grep -q "ALL_DONE video" video.log 2>/dev/null; do python3 f_render.py -- video >> video.log 2>&1; sleep 2; done
FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
$FF -y -framerate 24 -i frames/f_%04d.png -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -movflags +faststart final/Orange_County_Epe_Flythrough.mp4 > encode.log 2>&1
echo ENCODED >> video.log
until grep -q "ALL_DONE stills" stills.log 2>/dev/null; do python3 f_render.py -- stills >> stills.log 2>&1; sleep 2; done
