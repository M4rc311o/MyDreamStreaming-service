FROM tiangolo/nginx-rtmp:latest-2024-11-11

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*
    
RUN  wget -O jq https://github.com/stedolan/jq/releases/download/jq-1.5/jq-linux64 && \
     chmod +x ./jq && \
     mv ./jq /usr/bin/jq

RUN mkdir -p /etc/nginx/mdss/site
RUN mkdir -p /var/hls/tmp_hls 
RUN mkdir -p /var/hls/recordings
RUN mkdir -p /var/hls/screenshots

COPY ./ffmpeg.sh /etc/nginx/ffmpeg.sh
RUN chmod +x /etc/nginx/ffmpeg.sh

EXPOSE 80
