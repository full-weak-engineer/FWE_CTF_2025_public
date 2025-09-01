FROM python@sha256:60d9996b6a8a3689d36db740b49f4327be3be09a21122bd02fb8895abb38b50d AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 jail.py /srv/app/run
COPY --chmod=444 flag.txt /srv/app/flag.txt
ENV JAIL_MEM=25M JAIL_TIME=180 JAIL_CONNS_PER_IP=2