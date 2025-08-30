FROM node:18 AS base
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .

FROM base AS dev
CMD ["npm", "run", "dev"]

FROM base AS build
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
