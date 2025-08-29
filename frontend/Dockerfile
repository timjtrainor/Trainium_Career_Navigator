FROM node:18 AS build
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
ARG FRONTEND_PORT=80
ENV FRONTEND_PORT=${FRONTEND_PORT}
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE ${FRONTEND_PORT}

