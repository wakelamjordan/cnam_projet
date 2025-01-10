# syntax=docker/dockerfile:1.4
FROM node:18-alpine

WORKDIR /frontend

COPY package.json package-lock.json ./
RUN npm install

COPY . .
EXPOSE 3000

# uniquement pour le dev du coup
CMD ["npm", "run", "dev"]