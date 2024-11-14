FROM tiangolo/nginx-rtmp:latest-2024-11-11

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /etc/nginx/mdss/site

EXPOSE 80