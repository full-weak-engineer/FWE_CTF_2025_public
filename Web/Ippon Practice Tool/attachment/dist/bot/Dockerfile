FROM mcr.microsoft.com/playwright:v1.54.2-noble

WORKDIR /app

COPY package*.json .
RUN npm i --omit=dev

COPY . .

CMD [ "node", "index.js" ]
