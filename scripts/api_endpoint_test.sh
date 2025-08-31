#!/bin/bash
# api_endpoint_test.sh

BASE_URL=${BASE_URL:-http://localhost:8000}

echo "=== API Endpoint Testing ==="

# Test job creation
echo "Testing job creation..."
job_response=$(curl -s -X POST "$BASE_URL/api/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "API Test Job",
    "company": "Test Company",
    "url": "https://test.com/api-job"
  }')

echo "Job creation response: $job_response"

# Extract job ID if creation was successful
job_id=$(echo "$job_response" | grep -o '"job_id":"[^"]*' | sed 's/"job_id":"//')

if [ -n "$job_id" ]; then
  echo "✅ Job created successfully: $job_id"
  
  # Test job retrieval
  echo "Testing job retrieval..."
  get_response=$(curl -s "$BASE_URL/api/jobs/$job_id")
  echo "Job retrieval response: $get_response"
  
  # Test job listing
  echo "Testing job listing..."
  list_response=$(curl -s "$BASE_URL/api/jobs/unique?page=1")
  echo "Job listing response (truncated): $(echo "$list_response" | head -c 200)..."
else
  echo "❌ Job creation failed"
fi

echo "=== API Testing Complete ==="