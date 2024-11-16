FROM --platform=linux/arm/v8 node:20-alpine
WORKDIR /overlord-web/

COPY public /overlord-web/public
COPY src /overlord-web/src
COPY package.json /overlord-web

RUN npm install
CMD ["npm", "start"]