#!/bin/bash
# load_test.sh - Simple load testing

BASE_URL=${BASE_URL:-http://localhost:8000}
REQUESTS=${REQUESTS:-10}
CONCURRENT=${CONCURRENT:-2}

echo "=== Load Testing ==="
echo "URL: $BASE_URL"
echo "Requests: $REQUESTS"
echo "Concurrent: $CONCURRENT"

# Function to test with curl if ab is not available
curl_load_test() {
  local endpoint="$1"
  local method="$2"
  local data_file="$3"
  
  echo "Testing $endpoint with curl..."
  for i in $(seq 1 $REQUESTS); do
    if [ "$method" = "POST" ] && [ -n "$data_file" ]; then
      curl -s -w "Request $i: %{time_total}s (HTTP %{http_code})\n" \
        -X POST -H "Content-Type: application/json" \
        -d @"$data_file" "$BASE_URL$endpoint" -o /dev/null
    else
      curl -s -w "Request $i: %{time_total}s (HTTP %{http_code})\n" \
        "$BASE_URL$endpoint" -o /dev/null
    fi
  done
}

# Test health endpoint
echo "Testing health endpoint..."
curl_load_test "/api/health" "GET" ""

# Test job creation with POST data
echo "Testing job creation endpoint..."
cat > /tmp/job_data.json << EOF
{
  "title": "Load Test Job $(date +%s)",
  "company": "Load Test Corp",
  "url": "https://loadtest.com/job/$(date +%s)"
}
EOF

curl_load_test "/api/jobs" "POST" "/tmp/job_data.json"

echo "=== Load Testing Complete ==="