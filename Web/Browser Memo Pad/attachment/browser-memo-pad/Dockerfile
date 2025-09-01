FROM node:23.8.0-slim

WORKDIR /app

ENV PUPPETEER_SKIP_DOWNLOAD=true

RUN apt update && apt install -y chromium
RUN rm -rf /var/lib/apt/lists/*

COPY package*.json .
RUN npm i --omit=dev

COPY . .

EXPOSE 1337

USER node

CMD [ "node", "index.js" ]
