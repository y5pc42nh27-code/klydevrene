#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-/workspace/klydevrene-cache}"
mkdir -p "$XDG_CACHE_HOME"
bash build.sh
python3 qa.py
cp ../delivery/Klyde-Vrene-TikTok.mp4 ../Klyde-Vrene-dynamiczny.mp4
cp ../delivery/Klyde-Vrene-bez-napisow.mp4 ../Klyde-Vrene-dynamiczny-bez-napisow.mp4
cp captions.srt ../dynamiczny.srt
cp captions.ass ../dynamiczny.ass
cp ../delivery/qa-metrics.json ../qa-dynamiczny.json
cp ../delivery/audio-check.json ../audio-check-dynamiczny.json
# The accepted original MP4, original SRT, reports and ZIP are preserved.
