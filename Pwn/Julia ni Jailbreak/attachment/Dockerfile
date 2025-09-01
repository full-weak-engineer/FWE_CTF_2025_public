FROM julia@sha256:84c25e8c04e15936d1c5b68b0928ca8d6478947524a8817829a36345cbb3dc39 as app

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=755 run.sh /srv/app/run
COPY --chmod=755 jail.jl /srv/app/jail.jl
COPY --chmod=444 flag.txt /srv/app/flag.txt
ENV JAIL_MEM=800M JAIL_TIME=180 JAIL_CONNS_PER_IP=2 JAIL_ENV_HOME=/srv/app