#!/usr/bin/env bash
set -euo pipefail

# Load variables from .env if available
if [ -f ".env" ]; then
  set -o allexport
  source .env
  set +o allexport
fi

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

# === Agents layer smoke tests ===

# Validate /api/personas returns a JSON array with at least one persona
echo "Checking personas catalog"
personas_resp=$(curl -fsS "$BASE_URL/api/personas")
echo "$personas_resp"
echo "$personas_resp" | python -m json.tool >/dev/null
echo "$personas_resp" | grep -q '"id"'

# Validate /api/agent/{persona} returns JSON on POST
echo "Checking agent endpoint"
agent_resp=$(curl -fsS -H 'Content-Type: application/json' \
  -d '{"input":"ping"}' "$BASE_URL/api/agent/test")
echo "$agent_resp"
echo "$agent_resp" | python -m json.tool >/dev/null

# Validate /feedback persists data to Postgres via Agents service
echo "Checking feedback persistence"
payload='{ "persona": "smoke", "input": "hi", "output": "hello", "feedback": "ok" }'
post_resp=$(curl -fsS -H 'Content-Type: application/json' -d "$payload" "$BASE_URL/api/feedback")
echo "$post_resp" | python -m json.tool >/dev/null
feedback_list=$(curl -fsS "$BASE_URL/api/feedback")
echo "$feedback_list" | grep -q '"persona"[[:space:]]*:[[:space:]]*"smoke"'

echo "All smoke tests passed."
