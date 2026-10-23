#!/bin/sh
# Linux / macOS:  sh build.sh [your_song.py]
set -e
echo '免费分享 · 禁止售卖 · 禁止以任何名义收费（CC BY-NC-SA 4.0，创作者 reaesteve）'
echo 'Shared free · Not for sale · No paid access of any kind (CC BY-NC-SA 4.0, creator: reaesteve)'
cd "$(dirname "$0")"
SONG=${1:-example_song.py}
SF2=../sound_library/GeneralUser-GS/GeneralUser-GS.sf2
[ -f "$SF2" ] || cat ../sound_library/GeneralUser-GS/GeneralUser-GS.sf2.part_* > "$SF2"
python3 -c "import numpy, scipy" 2>/dev/null || python3 -m pip install -r requirements.txt
[ -x render ] || cc -O2 -o render render.c -lm
rm -f events_ch*.txt stems/*.raw
python3 "$SONG"
mkdir -p stems
TOT=$(python3 -c "import json;print(json.load(open('mix.json'))['total'])")
for f in events_ch*.txt; do c=$(echo "$f" | sed 's/events_ch\([0-9]*\).txt/\1/'); ./render "$SF2" "$f" "stems/ch$c.raw" "$TOT"; done
python3 mix_kit.py
