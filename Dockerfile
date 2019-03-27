FROM python:3.6
MAINTAINER HENDRIKX-ITC

RUN pip3 install minerva-dispatcher

COPY docker-dispatcher.yml /etc/minerva/dispatcher.yml

VOLUME /data

CMD ["dispatcher"]
