FROM node:14.4.0-alpine


RUN mkdir /app

RUN npm install -g @vue/cli

COPY package*.json ./

RUN npm install

WORKDIR /app

COPY . /app/

CMD npm run serve
