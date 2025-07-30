FROM mitmproxy/mitmproxy:12.1.1

ARG FLAG

RUN echo ${FLAG} > flag.txt
RUN mv flag.txt /flag-$(md5sum flag.txt | cut -c-32).txt

CMD ["mitmweb", "--set", "web_password=this_is_the_same_in_remote"]