FROM ubuntu
LABEL maintainer "n.landerer@tum.de"

RUN apt-get update && apt-get install -y --no-install-recommends
RUN apt install python3 -y

RUN apt-get update && apt-get install python3-pip -y

RUN pip3 install --upgrade setuptools
COPY dependencies/requirements.txt /usr/bin
RUN pip3 install -r /usr/bin/requirements.txt

ENTRYPOINT python3 asdf.py