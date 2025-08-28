#!/usr/bin/env bash
set -euo pipefail

BASE_URL=${BASE_URL:-http://localhost:8000}

check() {
  local path="$1"
  local name="$2"
  echo "Checking $name at $BASE_URL$path"
  resp=$(curl -fsS "$BASE_URL$path")
  echo "$resp"
  echo "$resp" | grep -q '"status"[[:space:]]*:[[:space:]]*"ok"'
}

check /health frontend
check /api/health agents
check /api/health/postgres postgres
check /api/health/mongo mongo

echo "All health checks passed."
