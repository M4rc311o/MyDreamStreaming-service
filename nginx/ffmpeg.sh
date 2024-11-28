#!/usr/bin/env bash
set -Eeuo pipefail

on_die ()
{
    pkill -KILL -P $$
}
trap 'on_die' TERM

STREAM_NAME="$1"

USER_ID=$(curl -s "http://flask/api/keys/$STREAM_NAME" | jq -r '.data.user_id')

RTMP_INPUT="rtmp://127.0.0.1:1935/live/$STREAM_NAME"

OUTPUT_DIR="/var/hls/tmp_hls/$USER_ID"
SCREENSHOT_DIR="/var/hls/screenshots"
RECORDINGS_DIR="/var/hls/recordings"

/usr/bin/ffmpeg -y -i "$RTMP_INPUT" \
     -map 0:v? -vf "fps=1/10,scale=400:-1" -q:v 2 -update 1 "$SCREENSHOT_DIR/${USER_ID}.jpg" \
     -map 0:v? -map 0:a? -c:v copy -c:a copy -f mpegts "${RECORDINGS_DIR}/${USER_ID}.ts" \
    -preset fast -g 48 -sc_threshold 0 \
    -map 0:v -map 0:a -map 0:v -map 0:a -map 0:v -map 0:a \
    -s:v:0 640x360 -c:v:0 libx264 -b:v:0 400k -pix_fmt yuv420p -profile:v:0 high -level:v:0 4.0 \
    -s:v:1 854x480 -c:v:1 libx264 -b:v:1 800k -pix_fmt yuv420p -profile:v:1 high -level:v:1 4.0 \
    -s:v:2 1280x720 -c:v:2 libx264 -b:v:2 2048k -pix_fmt yuv420p -profile:v:2 high -level:v:2 4.0 \
    -c:a copy \
    -var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2" \
    -master_pl_name master.m3u8 \
    -f hls -hls_time 2 -hls_list_size 300 \
    -hls_segment_filename "$OUTPUT_DIR/${USER_ID}_v%v/${USER_ID}_sequence%d.ts" \
    "$OUTPUT_DIR/${USER_ID}_v%v/media.m3u8"
wait
