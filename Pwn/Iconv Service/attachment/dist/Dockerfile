FROM bookworm-slim@sha256:4b50eb66f977b4062683ff434ef18ac191da862dbe966961bc11990cf5791a8d AS app

FROM pwn.red/jail
COPY --from=ubuntu / /srv
COPY --chmod=755 shifty_service /srv/app/run
COPY --chmod=444 flag.txt /srv/app/flag.txt
ENV JAIL_MEM=25M JAIL_TIME=180 JAIL_CONNS_PER_IP=2