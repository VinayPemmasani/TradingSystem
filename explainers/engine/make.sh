#!/bin/bash
# make.sh SLUG [workers]  -> /mnt/project-files/videos/explainers/SLUG.mp4 (voice, data, frames, mux)
set -e; S=$1; N=${2:-3}; E=/mnt/project-files/videos/explainers/engine; W=/tmp/claude-0/vx/$S
mkdir -p $W; cd $W
[ -f $W/audio/timing.json ] || python3 $E/tts.py $S
python3 $E/build_data.py $S
for ((i=0;i<N;i++)); do node $E/render.js $S frames $i $N > $W/render_$i.log 2>&1 & done; wait
grep -h "PAGE ERROR\|CONSOLE" $W/render_*.log && exit 1 || true
: > $W/segs.txt; for ((i=0;i<N;i++)); do echo "file '$W/seg_$i.mp4'" >> $W/segs.txt; done
ffmpeg -y -loglevel error -f concat -safe 0 -i $W/segs.txt -i $W/narration.wav -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $W/$S.mp4
cp $W/$S.mp4 /mnt/project-files/videos/explainers/$S.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 $W/$S.mp4
