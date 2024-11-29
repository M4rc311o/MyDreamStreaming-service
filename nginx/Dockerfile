FROM tiangolo/nginx-rtmp:latest-2024-11-11

RUN apt-get update && \
    apt-get install -y ffmpeg gettext-base tzdata && \
    rm -rf /var/lib/apt/lists/*
    
RUN  wget -O jq https://github.com/stedolan/jq/releases/download/jq-1.5/jq-linux64 && \
     chmod +x ./jq && \
     mv ./jq /usr/bin/jq

RUN mkdir -p /etc/nginx/mdss/site
RUN mkdir -p /var/hls/tmp_hls 
RUN mkdir -p /var/hls/recordings
RUN mkdir -p /var/hls/screenshots

COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

COPY ./nginx.conf /etc/nginx/templates/nginx.conf.template

COPY ./ffmpeg.sh /etc/nginx/ffmpeg.sh
RUN chmod +x /etc/nginx/ffmpeg.sh

EXPOSE 80

ENTRYPOINT [ "/docker-entrypoint.sh" ]
CMD [ "nginx", "-g", "daemon off;" ]