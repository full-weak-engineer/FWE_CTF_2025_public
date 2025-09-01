FROM node:24.5.0-slim

WORKDIR /app

COPY package*.json .
RUN npm i --omit=dev

COPY . .

USER node

CMD [ "node", "index.ts" ]
