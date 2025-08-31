#!/bin/bash
# curl-debug.sh - Advanced API debugging with cURL

BASE_URL=${BASE_URL:-http://localhost:8000}

# Function for detailed HTTP debugging
debug_request() {
  local method="$1"
  local endpoint="$2"
  local data="$3"
  local headers="$4"
  
  echo "=== Debug Request: $method $endpoint ==="
  echo "URL: $BASE_URL$endpoint"
  echo "Data: $data"
  echo "Headers: $headers"
  echo ""
  
  # Make request with detailed output
  if [ "$method" = "POST" ]; then
    curl -v -X POST "$BASE_URL$endpoint" \
      -H "Content-Type: application/json" \
      -H "$headers" \
      -d "$data" \
      -w "\n\nResponse Time: %{time_total}s\nHTTP Code: %{http_code}\nSize: %{size_download} bytes\n"
  else
    curl -v "$BASE_URL$endpoint" \
      -H "$headers" \
      -w "\n\nResponse Time: %{time_total}s\nHTTP Code: %{http_code}\nSize: %{size_download} bytes\n"
  fi
  echo ""
}

# Example usage
debug_request "GET" "/api/health" "" ""
debug_request "POST" "/api/jobs" '{
  "title": "Debug Job",
  "company": "Debug Corp", 
  "url": "https://debug.com/job"
}' ""