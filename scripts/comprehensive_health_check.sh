#!/bin/bash
# comprehensive_health_check.sh

echo "=== System Health Check ==="
BASE_URL=${BASE_URL:-http://localhost:8000}

# Function to check endpoint
check_endpoint() {
  local path="$1"
  local name="$2"
  echo "Checking $name at $BASE_URL$path"
  
  response=$(curl -s -w "HTTPSTATUS:%{http_code}" "$BASE_URL$path")
  http_code=$(echo $response | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
  body=$(echo $response | sed -e 's/HTTPSTATUS\:.*//g')
  
  if [ "$http_code" -eq 200 ]; then
    echo "✅ $name: OK"
    echo "$body" | python -m json.tool > /dev/null 2>&1 && echo "   Valid JSON response"
  else
    echo "❌ $name: HTTP $http_code"
    echo "   Response: $body"
  fi
  echo ""
}

# Run health checks
check_endpoint "/api/health" "Overall Health"
check_endpoint "/api/health/postgres" "PostgreSQL Health"
check_endpoint "/api/health/mongo" "MongoDB Health"
check_endpoint "/api/health/db" "Database Health"

echo "=== Health Check Complete ==="