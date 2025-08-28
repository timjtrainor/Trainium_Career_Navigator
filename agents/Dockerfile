FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Build deps for wheels & Postgres client
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential gcc git libpq-dev pkg-config ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install -U pip setuptools wheel

WORKDIR /app
COPY requirements.txt .
COPY constraints.txt .

# Make pip resilient and honor constraints to avoid resolver thrash
ARG PIP_OPTS="--disable-pip-version-check --prefer-binary --timeout 120 --retries 5"
RUN python -m pip install $PIP_OPTS -r requirements.txt -c constraints.txt

COPY app ./app
EXPOSE 8000
CMD ["uvicorn","app.main:app","--host=0.0.0.0","--port=8000","--workers=2","--proxy-headers"]