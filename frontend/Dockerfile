FROM nginx:alpine

# Build output is committed to the repo so the image only needs static files.
ARG FRONTEND_PORT=80
ENV FRONTEND_PORT=${FRONTEND_PORT}

COPY dist/ /usr/share/nginx/html/

EXPOSE ${FRONTEND_PORT}
