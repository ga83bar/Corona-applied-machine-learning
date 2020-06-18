FROM debian:buster-slim
LABEL maintainer "n.landerer@tum.de"

ENV JOBT jobtype
ENV IDX file_id
ENV ACTIVATION_CODE Code
ENV LOCATION smart

ARG APP=expressvpn_2.4.5.2-1_amd64.deb

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates wget python3 expect iproute2 curl \
    && rm -rf /var/lib/apt/lists/* \
    && wget -q "https://download.expressvpn.xyz/clients/linux/${APP}" -O /tmp/${APP} \
    && dpkg -i /tmp/${APP} \
    && rm -rf /tmp/*.deb \
    && apt-get purge -y --auto-remove wget

RUN apt-get update && apt-get install python3-pip -y

RUN pip3 install cloudscraper pandas

COPY initializer.sh /tmp/initializer.sh
COPY expressvpnActivate.sh /tmp/expressvpnActivate.sh
COPY docker_scraper.py /tmp/docker_scraper.py

ENTRYPOINT ["/bin/bash", "/tmp/initializer.sh"]
