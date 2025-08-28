# Trainium – Local Dev Guide

This guide explains required **environment variables** and **startup steps** for the Phase 1 stack:

- Kong API Gateway (DB-less)
- Frontend (static placeholder via Nginx)
- Agents API (FastAPI)
- PostgreSQL (relational)
- MongoDB (document)

---

## 1) Environment Variables (.env)
Copy `.env.example` to `.env` in the repo root and update as needed. Do **not** commit real secrets.

```bash
# === LLM providers ===
OPENAI_API_KEY= # sk-...
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=   # for Gemini (google-generativeai)

# === Databases ===
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=trainium
POSTGRES_USER=trainium
POSTGRES_PASSWORD=changeme

MONGO_HOST=mongo
MONGO_PORT=27017
MONGO_DB=trainium

# === Kong (DB-less mode) ===
KONG_LOG_LEVEL=info
KONG_ADMIN_LISTEN=0.0.0.0:8001   # dev only; lock down in staging

# === App ===
ENVIRONMENT=local
```

> **Tip**: Keep a private `.env.local` for real secrets and `source` it in your shell before running Docker.

### Variable reference
- **OPENAI_API_KEY / ANTHROPIC_API_KEY / GOOGLE_API_KEY**: Optional for now; used by Agents when hitting LLMs.
- **POSTGRES_HOST / POSTGRES_PORT / POSTGRES_DB / POSTGRES_USER / POSTGRES_PASSWORD**: Connection settings for the Postgres container.
- **MONGO_HOST / MONGO_PORT / MONGO_DB**: Connection settings for the Mongo container.
- **KONG_LOG_LEVEL**: Kong log verbosity (`info`, `debug`, etc.).
- **KONG_ADMIN_LISTEN**: Admin API bind (enabled only in dev).
- **ENVIRONMENT**: Passed to the Agents service for environment-aware behavior.

An **`.env.example`** is checked in with safe placeholders so others can copy it to `.env` quickly.

---

## 2) Startup Steps

1. **Build and start**
   ```bash
   docker compose up -d --build
   ```

2. **Verify containers**
   ```bash
   docker compose ps
   docker compose logs -f kong
   ```

3. **Open services (via Kong)**
   - Frontend: http://localhost:8000/
   - Agents API health: http://localhost:8000/api/health

4. **(Dev only) Kong admin status**
   - http://localhost:8001/status

---

## 3) Health Checks
- Frontend: Served through Kong at `/` (static Nginx placeholder page).
- Agents: `GET /api/health` returns JSON with environment, DB hosts/ports, and detected LLM keys.
- Databases: the Agents health payload echoes Postgres & Mongo host/port; you can also connect using your local client to verify.

---

## 4) Common Issues & Fixes

### Kong keeps restarting with `unknown field: priority`
Remove `priority` from your `gateway/kong.yml` route definitions. Example working route:
```yaml
services:
  - name: agents
    url: http://agents:8000
    routes:
      - name: agents-api
        paths: ["/api"]
        strip_path: true
        methods: ["GET","POST","OPTIONS"]
```

### Agents image fails during `pip install`
- Ensure the `agents/Dockerfile` installs build tools before `pip install`:
  ```dockerfile
  RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential gcc git libpq-dev pkg-config ca-certificates \
    && rm -rf /var/lib/apt/lists/*
  RUN python -m pip install -U pip setuptools wheel
  ```
- If using CrewAI only (no crewai-tools), keep `requirements.txt` minimal and rebuild with `--no-cache`.

### Can’t fetch packages from PyPI inside Docker
Add DNS for the `agents` service in `docker-compose.yml`:
```yaml
services:
  agents:
    dns:
      - 8.8.8.8
      - 1.1.1.1
```

---

## 5) Tear Down / Rebuild
- Stop containers: `docker compose down`
- Remove volumes (⚠️ deletes DB data): `docker compose down -v`
- Full rebuild: `docker compose build --no-cache && docker compose up -d`

---

## 6) Project Structure (Phase 1)
```
trainium/
├─ .env
├─ docker-compose.yml
├─ gateway/
│  └─ kong.yml
├─ frontend/
│  ├─ Dockerfile
│  └─ public/index.html
├─ agents/
│  ├─ Dockerfile
│  ├─ requirements.txt
│  └─ app/
│     ├─ main.py
│     └─ config.py
```

---

## 7) Quick Verification Steps
- Visit the frontend root → should show "Trainium Stack is Running".
- Call `GET /api/health` → should return `{ "status": "ok", ... }`.
- Check Kong admin `/status` (dev) → should show OK and your route/services.

---

## 8) Next
- Add JobSpy microservice and route via Kong at `/jobs`.
- Introduce auth (JWT/OIDC) and rate limiting in Kong for staging.
- Add observability (structured logs, metrics) once the stack is stable.
