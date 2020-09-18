FROM python:3-slim

WORKDIR /watcher

ENV PYTHONIOENCODING="UTF-8"
ENV PUID=1000
ENV PGID=1000

VOLUME /config

ADD startwatcher .
ADD watcher.py .
ADD watcher.ini .
CMD ls -al /config

RUN mkdir -p /.local
RUN pip --no-cache-dir install pyinotify

RUN mkdir -p /source
RUN mkdir -p /destination

RUN chown -R $PUID:$PGID /config
RUN chown $PUID:$PGID /source
RUN chown $PUID:$PGID /destination

RUN chown -R $PUID:$PGID /watcher

VOLUME /source
VOLUME /destination

USER $PUID:$PGID


CMD [ "bash" , "startwatcher" ]



