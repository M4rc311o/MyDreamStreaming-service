#!/bin/bash
set -e

on_die ()
{
    pkill -KILL -P $$
}




STREAM_NAME="$1"
# echo "Stream Name: $STREAM_NAME" > /tmp/debug.txt 

# API_RESPONSE=$(curl -s "http://flask/api/keys/$1") 
# echo "API Response: $API_RESPONSE" > /tmp/check_user_id.txt

USER_ID=$(curl -s "http://flask/api/keys/$STREAM_NAME" | jq -r '.data.user_id')
# echo "User ID: $USER_ID" > /tmp/check_user_id2.txt 

trap 'on_die' TERM





RTMP_INPUT="rtmp://127.0.0.1:1935/live/$STREAM_NAME"
# echo "$RTMP_INPUT" > /tmp/input.txt

OUTPUT_DIR="/var/hls/tmp_hls/$USER_ID"
# echo "$OUTPUT_DIR" > /tmp/output.txt
SCREENSHOT_DIR="/var/hls/screenshots"
RECORDINGS_DIR="/var/hls/recordings"



 /usr/bin/ffmpeg -y -i "$RTMP_INPUT" \
     -map 0:v? -vf "fps=1/10,scale=400:-1" -q:v 2 -update 1 "$SCREENSHOT_DIR/${USER_ID}.jpg" \
     -map 0:v? -map 0:a? -c:v copy -c:a copy -f mpegts "${RECORDINGS_DIR}/${USER_ID}.ts" \
    -preset fast -g 48 -sc_threshold 0 \
    -map 0:v -map 0:a -map 0:v -map 0:a -map 0:v -map 0:a \
    -s:v:0 640x360 -c:v:0 libx264 -b:v:0 400k \
    -s:v:1 854x480 -c:v:1 libx264 -b:v:1 800k \
    -s:v:2 1280x720 -c:v:2 libx264 -b:v:2 2048k \
    -c:a copy \
    -var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2" \
    -master_pl_name master.m3u8 \
    -f hls -hls_time 2 -hls_list_size 300 \
    -hls_segment_filename "$OUTPUT_DIR/${USER_ID}_v%v/${USER_ID}_sequence%d.ts" \
    "$OUTPUT_DIR/${USER_ID}_v%v/media.m3u8"   



wait
