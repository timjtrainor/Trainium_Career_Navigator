# Trainium – Local Dev Guide

This repository contains the Trainium Career Navigator application, a multi-service platform for job discovery and evaluation using AI-powered analysis.

> **📋 For detailed architecture information**, see [architecture_proposal.md](./architecture_proposal.md)

## Architecture Overview

The application consists of several services orchestrated via **Docker Compose** and routed through **Kong API Gateway**:

- **Frontend**: React application served via Kong at `/`
- **Agents**: FastAPI service that includes backend routes, served via Kong at `/api`
- **JobSpy Service**: Job scraping service, served via Kong at `/jobs`
- **PostgreSQL**: Primary database for job data and evaluations
- **MongoDB**: Document store for additional data
- **Kong**: API Gateway for routing and CORS handling

Persistent data for Postgres and Mongo is stored in named Docker volumes (`pgdata`, `mongodata`) so database contents survive restarts.

---

## 1) Environment Variables (.env)

**⚠️ Security Notice**: All sensitive data (passwords, API keys, secrets) are managed through environment variables and **must never be hardcoded in the source code**. The application uses `python-dotenv` to securely load these variables.

Copy `.env.example` to `.env` in the repo root and update as needed. **Do not commit real secrets** - the `.env` file is already excluded in `.gitignore`.

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
# Admin API bound to localhost; change to 0.0.0.0:8001 for host access in dev
KONG_ADMIN_LISTEN=127.0.0.1:8001
KONG_PROXY_PORT=8000
KONG_ADMIN_PORT=8001

# === App ===
ENVIRONMENT=local
FRONTEND_PORT=80
FRONTEND_DEV_PORT=5173

# === JobSpy ===
JOBSPY_DELAY_SECONDS=2
```

### Environment Variable Loading

The application automatically loads environment variables through:
- **Agents service**: Uses `load_dotenv()` in `agents/app/config.py`
- **Backend services**: Centralized loading via `backend/app/config.py`
- **Docker services**: Environment variables passed via `env_file: - .env` in `docker-compose.yml`

> **Tip**: Keep a private `.env.local` for real secrets and `source` it in your shell before running Docker.

### Variable reference
- **OPENAI_API_KEY / ANTHROPIC_API_KEY / GOOGLE_API_KEY**: Optional for now; used by Agents when hitting LLMs.
- **POSTGRES_HOST / POSTGRES_PORT / POSTGRES_DB / POSTGRES_USER / POSTGRES_PASSWORD**: Connection settings for the Postgres container.
- **MONGO_HOST / MONGO_PORT / MONGO_DB**: Connection settings for the Mongo container.
- **KONG_LOG_LEVEL**: Kong log verbosity (`info`, `debug`, etc.).
- **KONG_ADMIN_LISTEN**: Admin API bind. Defaults to `127.0.0.1:8001` for safety; set to `0.0.0.0:8001` if you need host access in development.
- **KONG_PROXY_PORT / KONG_ADMIN_PORT**: Host ports for Kong's proxy and admin interfaces.
- **FRONTEND_PORT**: Port exposed for the frontend service.
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

## 8) Job Posting Functionality

### Via UI (Frontend)
1. Navigate to `/jobs/discover` in the frontend
2. Click the "Add Job" button (positioned on the same row as the page heading)
3. Fill in the required fields:
   - **Job Title** (required)
   - **Company Name** (required)
   - **URL for Original Posting** (required)
   - Location (optional)
   - Job Description (optional)
   - Salary Range (optional)
   - Job Type (optional)
4. Click "Submit" - you should see a success message if the job is saved

### Via curl (API Testing)
```bash
# Test job posting via API
curl -X POST http://localhost:8000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Python Developer",
    "company": "Example Corp",
    "url": "https://example.com/jobs/python-dev",
    "location": "Remote",
    "description": "Looking for an experienced Python developer...",
    "salary_min": 80000,
    "salary_max": 120000,
    "job_type": "Full-time"
  }'
```

**Expected Response** (HTTP 201):
```json
{
  "job_id": "uuid-here",
  "message": "Job created successfully"
}
```

**Error Response** (HTTP 409 for duplicates):
```json
{
  "detail": "duplicate job"
}
```

### Required Fields for Job Posting
- `title`: String (job title)
- `company`: String (company name)
- `url`: String (URL to original job posting)

### Optional Fields
- `location`: String
- `description`: String
- `salary_min`: Integer (minimum salary)
- `salary_max`: Integer (maximum salary)
- `job_type`: String (e.g., "Full-time", "Part-time", "Contract")

---

## 9) Next Steps
- Add jobspy_service microservice and route via Kong at `/jobs`.
- Introduce auth (JWT/OIDC) and rate limiting in Kong for staging.
- Add observability (structured logs, metrics) once the stack is stable.

---

## 🔮 Optional: Adding a GUI for Kong

Right now this stack runs **Kong in DB-less mode** with a declarative `gateway/kong.yml`.  
This is lean, Git-driven, and works great for CI/CD.

If in the future you need a **GUI for Kong**:

- **Konga (open source):** Community UI for managing Kong.  
  ⚠️ Requires running Kong in **Postgres DB mode** instead of DB-less.  
  You can then connect Konga at `http://localhost:1337` and view/manage routes, services, and plugins.  
- **Kong Manager (Enterprise):** Official paid UI from Kong Inc.  
- **deck (CLI tool):** Use `deck sync` to push `kong.yml` into a DB-backed Kong, or `deck dump` to export GUI-made changes back into Git.
👉 Recommendation: keep `kong.yml` as the **source of truth** in Git, and only use a GUI for inspection or quick experiments.  
