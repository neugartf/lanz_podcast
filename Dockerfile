FROM ubuntu:22.04


RUN apt update && apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
RUN curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
RUN curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list

RUN apt-get update && apt-get install --no-install-recommends -y python3 python3-dev python3-pip python3-lxml libxml2-dev libxslt-dev ffmpeg build-essential cron caddy && \
   apt-get clean && rm -rf /var/lib/apt/lists/*
RUN caddy add-package github.com/caddyserver/transform-encoder

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8080
RUN mkdir /code
WORKDIR code

COPY . .
RUN curl -L -o goatcounter.gz https://github.com/arp242/goatcounter/releases/download/v2.5.0/goatcounter-v2.5.0-linux-amd64.gz && gzip -d goatcounter.gz && chmod +x goatcounter
RUN crontab crontab

CMD ["/bin/bash", "-c", "cron && caddy start && goatcounter import --follow --format=common --site='https://neugartf.goatcounter.com' lanz_access.log"]
