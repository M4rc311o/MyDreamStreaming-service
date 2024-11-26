FROM tiangolo/nginx-rtmp:latest-2024-11-11

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /etc/nginx/mdss/site
RUN mkdir -p /var/hls/tmp_hls 
RUN mkdir -p /var/hls/recordings
RUN mkdir -p /var/hls/screenshots

COPY ./ffmpeg.sh /etc/nginx/ffmpeg.sh
RUN chmod +x /etc/nginx/ffmpeg.sh

EXPOSE 80