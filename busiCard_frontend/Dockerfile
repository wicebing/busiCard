FROM node:18.16.0

WORKDIR /usr/src/app

COPY . ./
RUN npm install
RUN npm i -D naive-ui
RUN npm i -D vfonts
RUN npm i -D @vicons/ionicons5
RUN npm install -D tailwindcss

EXPOSE 3000

# ENV HOST=0.0.0.0
# ENV PORT=8080

RUN npm run build

# CMD [ "npm", "run", "start" ]
CMD ["node", ".output/server/index.mjs"]