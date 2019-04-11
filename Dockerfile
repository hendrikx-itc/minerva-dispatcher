FROM python:3.6
MAINTAINER HENDRIKX-ITC

RUN pip3 install minerva-dispatcher

RUN mkdir /etc/minerva -p
COPY dispatcher.yml /etc/minerva/dispatcher.yml

VOLUME /data

CMD ["dispatcher"]
