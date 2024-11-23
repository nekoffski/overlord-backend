FROM node:20-alpine
WORKDIR /overlord-web/

COPY public /overlord-web/public
COPY src /overlord-web/src
COPY dist/*.js /overlord-web/src/dashboard/components/proto
COPY package.json /overlord-web

RUN npm install
CMD ["npm", "start"]