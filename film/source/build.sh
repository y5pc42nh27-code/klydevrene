#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p ../delivery
python3 captions.py
python3 animate.py --render ../delivery/animation-silent.mp4
ffmpeg -v error -y -i ../delivery/animation-silent.mp4 -i assets/narration.mp3 -map 0:v -map 1:a -c:v copy -af 'loudnorm=I=-16:TP=-1.5:LRA=9:measured_I=-25.13:measured_TP=-5.93:measured_LRA=3.60:measured_thresh=-35.57:offset=0.87:linear=false' -ar 48000 -c:a aac -b:a 192k -movflags +faststart ../delivery/Klyde-Vrene-bez-napisow.mp4
ffmpeg -v error -y -i ../delivery/Klyde-Vrene-bez-napisow.mp4 -vf "ass=captions.ass" -c:v libx264 -preset fast -crf 18 -threads 4 -pix_fmt yuv420p -c:a copy -movflags +faststart ../delivery/Klyde-Vrene-TikTok.mp4
