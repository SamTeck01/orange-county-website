#!/bin/bash
# per shot: temporal anti-flicker (no blending across cuts), 1080p upscale, light sharpen
cd "$(dirname "$0")"; FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
mkdir -p film_v2_df; s=1
for n in $(cat v2_shots.txt); do
  $FF -y -v error -start_number $s -i film_v2_hq/f_%04d.png -frames:v $n \
   -vf "deflicker=mode=pm:size=7,atadenoise=0a=0.04:0b=0.08:1a=0.04:1b=0.08:2a=0.04:2b=0.08:s=9,hqdn3d=0:0:5:5,scale=1920:1080:flags=lanczos,unsharp=5:5:0.7:5:5:0" \
   -start_number $s film_v2_df/f_%04d.png
  s=$((s+n))
done
echo DF_DONE
