FROM node:lts-bookworm as node
WORKDIR /app
COPY package*.json ./
COPY ./dist ./
RUN npm install
CMD ["node", "."]