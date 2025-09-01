
FROM python:3.13.6-slim-bookworm AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 jail.py /srv/app/run
COPY --chmod=444 flag.txt /srv/app/flag.txt
ENV JAIL_MEM=25M JAIL_TIME=180 JAIL_CONNS_PER_IP=2