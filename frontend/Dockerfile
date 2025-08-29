FROM node:18 AS build
WORKDIR /app
# Install dependencies separately for better caching
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
ARG FRONTEND_PORT=80
ENV FRONTEND_PORT=${FRONTEND_PORT}
COPY --from=build /app/dist /usr/share/nginx/html
# keep health endpoint accessible at /health
COPY --from=build /app/public/health /usr/share/nginx/html/health
EXPOSE ${FRONTEND_PORT}

