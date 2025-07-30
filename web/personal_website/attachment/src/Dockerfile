FROM python:3.13.2-slim-bookworm

ARG PORT="8080"
ARG FLAG="fwectf{fake_flag}"
ENV PORT=${PORT}

WORKDIR /app

RUN echo ${FLAG} > flag.txt
RUN mv flag.txt /flag-$(md5sum flag.txt | cut -c-32).txt

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD flask run --host=0.0.0.0 --port=${PORT}