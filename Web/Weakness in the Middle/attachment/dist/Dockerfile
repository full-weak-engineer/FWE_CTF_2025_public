FROM mitmproxy/mitmproxy:12.1.1

RUN groupadd -g 1001 app && \
    useradd -m -s /bin/bash -u 1001 -g 1001 app

RUN apt-get update && apt-get install -y gcc

COPY . .
RUN gcc -o readflag readflag.c && rm readflag.c
RUN chmod 4555 readflag
RUN chmod +x entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD mitmweb --listen-host 0.0.0.0 --set block_global=false --set web_password=$PASS