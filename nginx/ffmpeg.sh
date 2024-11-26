#!/bin/bash


STREAM_NAME="$1"
RTMP_INPUT="rtmp://127.0.0.1:1935/live/$STREAM_NAME"
OUTPUT_DIR="/var/hls/tmp_hls"
SCREENSHOT_DIR="/var/hls/screenshots"
RECORDINGS_DIR="/var/hls/recordings"

# Create master playlist
MASTER_PLAYLIST="$OUTPUT_DIR/${STREAM_NAME}_master.m3u8"
echo "#EXTM3U" > "$MASTER_PLAYLIST"
echo "#EXT-X-STREAM-INF:BANDWIDTH=400000,RESOLUTION=640x360" >> "$MASTER_PLAYLIST"
echo "${STREAM_NAME}_360.m3u8" >> "$MASTER_PLAYLIST"
echo "#EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=854x480" >> "$MASTER_PLAYLIST"
echo "${STREAM_NAME}_480.m3u8" >> "$MASTER_PLAYLIST"
echo "#EXT-X-STREAM-INF:BANDWIDTH=2048000,RESOLUTION=1280x720" >> "$MASTER_PLAYLIST"
echo "${STREAM_NAME}_720.m3u8" >> "$MASTER_PLAYLIST"

# Start processing the stream
/usr/bin/ffmpeg -i "$RTMP_INPUT" \
    -map 0:v? -vf "fps=1/10,scale=400:-1" -q:v 2 "$SCREENSHOT_DIR/screenshot_%04d.jpg" \
    -map 0:v? -vf "scale=640:360" -b:v 400k -preset fast -f hls -hls_time 2 -hls_playlist_type event -hls_flags append_list+discont_start -hls_list_size 300 "$OUTPUT_DIR/${STREAM_NAME}_360.m3u8" \
    -map 0:v? -vf "scale=854:480" -b:v 800k -preset fast -f hls -hls_time 2 -hls_playlist_type event -hls_flags append_list+discont_start -hls_list_size 300 "$OUTPUT_DIR/${STREAM_NAME}_480.m3u8" \
    -map 0:v? -vf "scale=1280:720" -b:v 2048k -preset fast -f hls -hls_time 2 -hls_playlist_type event -hls_flags append_list+discont_start -hls_list_size 300 "$OUTPUT_DIR/${STREAM_NAME}_720.m3u8" 