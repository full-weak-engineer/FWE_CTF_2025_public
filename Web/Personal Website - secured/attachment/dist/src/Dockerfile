FROM python:3.13.6-slim-bookworm

RUN groupadd -g 1001 app && \
    useradd -m -s /bin/bash -u 1001 -g 1001 app

RUN apt-get update && apt-get install -y gcc

COPY readflag.c readflag.c
RUN gcc -o readflag readflag.c && rm readflag.c
RUN chmod 4555 readflag

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod -R 777 /app

ENTRYPOINT ["/app/entrypoint.sh"]
CMD flask run --host=0.0.0.0 --port=${PORT}