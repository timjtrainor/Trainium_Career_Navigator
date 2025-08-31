#!/bin/bash
# e2e_workflow_test.sh

BASE_URL=${BASE_URL:-http://localhost:8000}
TEST_ID=$(date +%s)

echo "=== End-to-End Workflow Test ==="
echo "Test ID: $TEST_ID"

# Step 1: Health check
echo "Step 1: Health verification..."
health_response=$(curl -s "$BASE_URL/api/health")
echo "$health_response" | grep -q '"status":"ok"' || {
  echo "❌ Health check failed"
  exit 1
}
echo "✅ System healthy"

# Step 2: Create job
echo "Step 2: Creating test job..."
job_response=$(curl -s -X POST "$BASE_URL/api/jobs" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"E2E Test Job $TEST_ID\",
    \"company\": \"Test Corp $TEST_ID\",
    \"url\": \"https://test.com/job/$TEST_ID\"
  }")

job_id=$(echo "$job_response" | grep -o '"job_id":"[^"]*' | sed 's/"job_id":"//')
if [ -n "$job_id" ]; then
  echo "✅ Job created: $job_id"
else
  echo "❌ Job creation failed: $job_response"
  exit 1
fi

# Step 3: Retrieve job
echo "Step 3: Retrieving job..."
get_response=$(curl -s "$BASE_URL/api/jobs/$job_id")
echo "$get_response" | grep -q "$job_id" || {
  echo "❌ Job retrieval failed"
  exit 1
}
echo "✅ Job retrieved successfully"

# Step 4: List jobs
echo "Step 4: Listing jobs..."
list_response=$(curl -s "$BASE_URL/api/jobs/unique?page=1")
echo "$list_response" | grep -q '"data"' || {
  echo "❌ Job listing failed"
  exit 1
}
echo "✅ Job listing successful"

echo "🎉 End-to-End test completed successfully!"