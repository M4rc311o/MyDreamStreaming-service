FROM python:3.12.7-slim

WORKDIR /mdss

RUN apt-get update && \
    apt-get install -y curl tzdata && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /mdss/app/static/js && \
    chmod -R 755 /mdss/app/static

RUN mkdir /mdss/app/static/avatar && \
    chmod 755 /mdss/app/static/avatar

RUN curl -L -o /mdss/app/static/js/purify.min.js https://unpkg.com/dompurify@latest/dist/purify.min.js

EXPOSE 80

#ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:80", "wsgi:app"]
ENTRYPOINT ["python", "-u", "wsgi.py"]
