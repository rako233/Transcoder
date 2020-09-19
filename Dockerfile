FROM python:3-slim

WORKDIR /watcher

ENV PYTHONIOENCODING="UTF-8"
ENV PUID=1000
ENV PGID=1000

ADD python/watcher.ini .
ADD python/watcher.py .
ADD python/transcode.py .
ADD startup .

RUN chmod +x startup && \
    mkdir -p /.local && \
    mkdir -p /source && \
    mkdir -p /config && \
    mkdir -p /destination && \
    pip --no-cache-dir install pyinotify && \
    chown -R $PUID:$PGID /watcher && \
    chown -R $PUID:$PGID /source && \
    chown -R $PUID:$PGID /destination && \
    chown -R $PUID:$PGID /config && \
    apt update && \
    apt install -y ffmpeg && \
    apt clean -y 

VOLUME /config
VOLUME /source
VOLUME /destination

USER $PUID:$PGID
CMD [ "/watcher/startup" ]

