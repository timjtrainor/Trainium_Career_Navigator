# API Debugging Plan for Trainium Career Navigator

This document provides a comprehensive debugging plan for the Trainium Career Navigator API system, designed to help developers and AI agents systematically troubleshoot API issues.

## Quick Reference Card

| Issue | Quick Check | Solution |
|-------|-------------|----------|
| Connection refused | `docker compose ps` | `docker compose up -d` |
| 502 Bad Gateway | `docker compose logs kong` | Check Kong config, restart Kong |
| 500 Internal Error | `curl http://localhost:8000/api/health` | Check service logs, DB connections |
| Slow responses | `docker stats` | Check resource usage, optimize queries |
| 409 Duplicate | Expected behavior | Handle gracefully in client code |
| 422 Validation | Check request format | Validate required fields |

**Emergency Reset:** `docker compose down && docker compose up -d --build`

## System Architecture Overview

The Trainium Career Navigator consists of multiple microservices:
- **Kong Gateway** (Port 8000) - API Gateway and proxy
- **Agents Service** - AI agents and LLM integration
- **JobSpy Service** - Job scraping and search functionality
- **PostgreSQL** - Primary database for job data and feedback
- **MongoDB** - Document storage for unstructured data
- **Frontend** - React-based user interface

## Quick Debug Checklist

When facing API issues, follow this systematic approach:

### 1. System Health Verification
```bash
# Check overall system health
curl http://localhost:8000/api/health

# Check individual service health
curl http://localhost:8000/api/health/postgres
curl http://localhost:8000/api/health/mongo
curl http://localhost:8000/api/health/db
```

**Expected Results:**
- HTTP 200 status code
- JSON response with `"status": "ok"`
- No error fields in the response

### 2. Service Status Check
```bash
# Verify all containers are running
docker compose ps

# Check container logs for errors
docker compose logs kong
docker compose logs agents
docker compose logs jobspy_service
docker compose logs postgres
docker compose logs mongo
```

### 3. Network Connectivity Test
```bash
# Test Kong gateway is accessible
curl -v http://localhost:8000/

# Test individual service endpoints through Kong
curl -v http://localhost:8000/api/
```

## Service-Specific Debugging

### Kong Gateway Debugging

**Common Issues:**
- Kong configuration errors
- Route misconfigurations
- Service discovery failures

**Debug Steps:**
```bash
# Check Kong admin API
curl http://localhost:8001/services
curl http://localhost:8001/routes

# Validate Kong configuration
python -c 'import yaml,sys; yaml.safe_load(open("gateway/kong.yml"))'

# Check Kong logs
docker compose logs kong --tail=50
```

**Configuration Validation:**
```bash
# Test Kong configuration syntax
docker run --rm -v "$(pwd)/gateway/kong.yml:/tmp/kong.yml" kong:3.6 kong config -c /tmp/kong.yml check
```

### Agents Service Debugging

**Health Check Endpoints:**
```bash
# Agent service health
curl http://localhost:8000/api/health

# Database connectivity
curl http://localhost:8000/api/health/postgres
curl http://localhost:8000/api/health/mongo
```

**Common Issues:**
- Database connection failures
- Missing environment variables
- LLM provider API key issues

**Debug Steps:**
```bash
# Check agent service logs
docker compose logs agents --tail=50

# Test database connections
docker exec -it trainium-postgres-1 psql -U trainium -d trainium -c "SELECT 1;"
docker exec -it trainium-mongo-1 mongosh trainium --eval "db.runCommand('ping')"

# Validate environment variables
docker compose exec agents env | grep -E "(POSTGRES|MONGO|OPENAI|ANTHROPIC|GOOGLE)"
```

**Python Module Validation:**
```bash
# Compile check for agents service
python -m py_compile agents/app/main.py
python -m py_compile agents/app/config.py
```

### JobSpy Service Debugging

**Service Health:**
```bash
# Test JobSpy service directly
curl http://localhost:8000/api/jobspy/health
```

**Common Issues:**
- Job scraping failures
- Cache issues
- External API rate limiting

**Debug Steps:**
```bash
# Check JobSpy service logs
docker compose logs jobspy_service --tail=50

# Test job search functionality
curl "http://localhost:8000/api/jobs/search?source=indeed&search_term=python"

# Check ingestion status
curl http://localhost:8000/api/ingest/status
```

### Database Debugging

**PostgreSQL Debugging:**
```bash
# Connect to PostgreSQL
docker exec -it trainium-postgres-1 psql -U trainium -d trainium

# Check database connectivity
docker exec -it trainium-postgres-1 pg_isready -U trainium

# View database tables
docker exec -it trainium-postgres-1 psql -U trainium -d trainium -c "\dt"

# Check recent jobs
docker exec -it trainium-postgres-1 psql -U trainium -d trainium -c "SELECT COUNT(*) FROM jobs;"
```

**MongoDB Debugging:**
```bash
# Connect to MongoDB
docker exec -it trainium-mongo-1 mongosh trainium

# Check MongoDB status
docker exec -it trainium-mongo-1 mongosh --eval "db.adminCommand('ping')"

# List collections
docker exec -it trainium-mongo-1 mongosh trainium --eval "db.listCollections()"
```

## API Testing and Validation

### Job Management API Testing

**Create Job Test:**
```bash
# Test job creation
curl -X POST http://localhost:8000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Debug Test Job",
    "company": "Debug Corp",
    "url": "https://debug.com/job/test",
    "location": "Remote",
    "description": "Test job for debugging",
    "job_type": "Full-time"
  }'
```

**Expected Result:**
- HTTP 201 status
- Response with `job_id` and `message`

**Get Job Test:**
```bash
# Replace JOB_ID with actual ID from creation response
curl http://localhost:8000/api/jobs/JOB_ID
```

**List Jobs Test:**
```bash
curl http://localhost:8000/api/jobs/unique?page=1
```

### Error Response Testing

**Duplicate Job Test:**
```bash
# Create the same job twice - second should return 409
curl -X POST http://localhost:8000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Duplicate Test",
    "company": "Test Corp",
    "url": "https://test.com/duplicate"
  }'
```

**Invalid Request Test:**
```bash
# Missing required fields - should return 422
curl -X POST http://localhost:8000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{"title": "Incomplete Job"}'
```

## Error Analysis and Resolution

### HTTP Status Code Guide

| Status | Description | Common Causes | Resolution |
|--------|-------------|---------------|------------|
| 200 | OK | - | Request successful |
| 201 | Created | - | Resource created successfully |
| 400 | Bad Request | Invalid JSON, malformed request | Check request format and data |
| 404 | Not Found | Invalid endpoint, missing resource | Verify URL and resource existence |
| 409 | Conflict | Duplicate resource | Handle duplicates gracefully |
| 422 | Validation Error | Missing required fields, invalid data | Validate request data |
| 500 | Internal Server Error | Database connection, service errors | Check logs and service health |
| 502 | Bad Gateway | Kong proxy issues | Check Kong configuration |
| 503 | Service Unavailable | Service down or overloaded | Check service status |

## Common Error Scenarios

**Connection Refused (Port 8000):**
```bash
# Symptoms: "Connection refused", "Failed to establish connection"
# This indicates services are not running

# Resolution steps:
1. Check if services are running: docker compose ps
2. Start services: docker compose up -d
3. Wait for services to be healthy: sleep 30
4. Re-run health check: curl http://localhost:8000/api/health
```

**Database Connection Failures:**
```bash
# Symptoms: 500 errors, "database unavailable" in logs
# Resolution steps:
1. Check database health: curl http://localhost:8000/api/health/postgres
2. Verify containers running: docker compose ps
3. Check database logs: docker compose logs postgres
4. Restart database: docker compose restart postgres
```

**Kong Gateway Issues:**
```bash
# Symptoms: 502 errors, gateway timeouts
# Resolution steps:
1. Check Kong logs: docker compose logs kong
2. Verify Kong admin API: curl http://localhost:8001/
3. Validate Kong config: python -c 'import yaml,sys; yaml.safe_load(open("gateway/kong.yml"))'
4. Restart Kong: docker compose restart kong
```

**Service Discovery Failures:**
```bash
# Symptoms: Services not reachable through Kong
# Resolution steps:
1. Check service health directly: curl http://agents:8000/health
2. Verify Docker network: docker network ls
3. Check service exposure: docker compose config
4. Restart affected services: docker compose restart agents jobspy_service
```

## Performance Debugging

### Response Time Analysis
```bash
# Measure API response times
curl -w "@scripts/curl-format.txt" -o /dev/null -s http://localhost:8000/api/health

# Test with multiple requests to get average
for i in {1..5}; do
  echo "Request $i:"
  curl -w "@scripts/curl-format.txt" -o /dev/null -s http://localhost:8000/api/health
  echo ""
done
```

### Load Testing
```bash
#!/bin/bash
# load_test.sh - Simple load testing

BASE_URL=${BASE_URL:-http://localhost:8000}
REQUESTS=${REQUESTS:-10}
CONCURRENT=${CONCURRENT:-2}

echo "=== Load Testing ==="
echo "URL: $BASE_URL"
echo "Requests: $REQUESTS"
echo "Concurrent: $CONCURRENT"

# Install ab (Apache Bench) if not available
command -v ab >/dev/null 2>&1 || {
  echo "Installing Apache Bench..."
  apt-get update && apt-get install -y apache2-utils
}

# Test health endpoint
echo "Testing health endpoint..."
ab -n $REQUESTS -c $CONCURRENT "$BASE_URL/api/health"

# Test job creation with POST data
echo "Testing job creation endpoint..."
cat > /tmp/job_data.json << EOF
{
  "title": "Load Test Job",
  "company": "Load Test Corp",
  "url": "https://loadtest.com/job"
}
EOF

ab -n $REQUESTS -c $CONCURRENT -p /tmp/job_data.json -T application/json "$BASE_URL/api/jobs"
```

### Resource Monitoring
```bash
# Monitor container resource usage
docker stats --no-stream

# Check specific service logs for performance issues
docker compose logs agents | grep -E "(slow|timeout|error)"

# Monitor database performance
docker compose exec postgres psql -U trainium -d trainium -c "
  SELECT query, mean_time, calls, total_time 
  FROM pg_stat_statements 
  ORDER BY mean_time DESC 
  LIMIT 10;"
```

## Logging and Monitoring

### Log Analysis Commands
```bash
# View all service logs
docker compose logs -f

# Filter logs by service
docker compose logs agents --tail=100

# Search for specific errors
docker compose logs | grep -i error

# Monitor real-time logs
docker compose logs -f --tail=50
```

### Log Levels and Configuration
```bash
# Adjust Kong log level in .env file
KONG_LOG_LEVEL=debug  # Options: debug, info, notice, warn, error, crit

# Check current log configuration
docker compose exec kong kong config db_less_entities
```

## Automated Testing Scripts

### Comprehensive Health Check
```bash
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
```

### API Endpoint Testing
```bash
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
```

## Best Practices for API Debugging

### 1. Always Start with Health Checks
Before investigating specific API issues, verify overall system health using the health endpoints.

### 2. Use Structured Logging
When adding debug logs, use structured JSON format for easier parsing:
```python
logger.info("api_request", extra={
    "method": "POST",
    "endpoint": "/api/jobs",
    "user_id": user_id,
    "status_code": 201,
    "response_time": 0.123
})
```

### 3. Implement Request Tracing
Add correlation IDs to track requests across services:
```bash
# Example with correlation ID
curl -H "X-Correlation-ID: debug-$(date +%s)" http://localhost:8000/api/health
```

### 4. Monitor Resource Usage
Keep an eye on container resource consumption during debugging:
```bash
# Monitor memory and CPU usage
docker stats --no-stream
```

### 5. Test Error Scenarios
Always test both success and failure paths:
- Valid requests
- Invalid data
- Missing parameters
- Duplicate resources
- Database connection failures

### 6. Use Version Control for Config
Track configuration changes that might affect API behavior:
```bash
# Check recent config changes
git log --oneline -n 10 gateway/kong.yml
git log --oneline -n 10 .env.example
```

## Troubleshooting Checklist

When facing API issues, work through this checklist systematically:

- [ ] System health check passes
- [ ] All containers are running
- [ ] Kong gateway is accessible
- [ ] Database connections are healthy
- [ ] Service logs show no critical errors
- [ ] Request format is correct
- [ ] Required fields are provided
- [ ] Authentication (if required) is valid
- [ ] Rate limits are not exceeded
- [ ] Network connectivity is stable
- [ ] Configuration files are valid
- [ ] Environment variables are set correctly

## Emergency Procedures

### Complete System Reset
If the system is in an unrecoverable state:
```bash
# Stop all services
docker compose down

# Remove volumes (WARNING: This deletes all data)
docker compose down -v

# Rebuild and restart
docker compose up -d --build

# Wait for services to be healthy
sleep 30

# Run health check
curl http://localhost:8000/api/health
```

### Rollback Configuration
If a configuration change causes issues:
```bash
# Revert to previous configuration
git checkout HEAD~1 -- gateway/kong.yml

# Restart Kong with old config
docker compose restart kong
```

### Database Recovery
If database issues persist:
```bash
# Backup current data (if accessible)
docker compose exec postgres pg_dump -U trainium trainium > backup.sql

# Reset database
docker compose restart postgres

# Restore from backup if needed
docker compose exec -T postgres psql -U trainium trainium < backup.sql
```

## Contact and Escalation

For persistent issues that cannot be resolved using this guide:

1. **Check GitHub Issues**: Review existing issues and create a new one with:
   - System health check results
   - Error logs from affected services
   - Steps to reproduce the issue
   - Expected vs actual behavior

2. **Include Debug Information**:
   - Docker compose logs
   - API response examples
   - Configuration files (sanitized)
   - System resource usage

3. **Environment Information**:
   - Operating system
   - Docker version
   - Service versions
   - Environment variables (without secrets)

## API Response Debugging Tools

### cURL Debugging Template
Create a `curl-debug.sh` script for systematic API testing:
```bash
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
```

### Python API Testing Script
Create `api_debug_test.py` for programmatic API testing:
```python
#!/usr/bin/env python3
"""
API Debug Testing Script for Trainium Career Navigator
"""

import json
import time
import requests
from datetime import datetime
from typing import Dict, Any, Optional

BASE_URL = "http://localhost:8000"

class APIDebugger:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        
    def health_check_full(self) -> Dict[str, Any]:
        """Comprehensive health check of all services."""
        results = {}
        
        endpoints = [
            ("/api/health", "overall"),
            ("/api/health/postgres", "postgres"),
            ("/api/health/mongo", "mongo"),
            ("/api/health/db", "database")
        ]
        
        for endpoint, name in endpoints:
            try:
                start_time = time.time()
                response = self.session.get(f"{self.base_url}{endpoint}")
                duration = time.time() - start_time
                
                results[name] = {
                    "status_code": response.status_code,
                    "response_time": duration,
                    "success": response.status_code == 200,
                    "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
                }
            except Exception as e:
                results[name] = {
                    "status_code": None,
                    "response_time": None,
                    "success": False,
                    "error": str(e)
                }
        
        return results
    
    def test_job_api_flow(self) -> Dict[str, Any]:
        """Test complete job API workflow."""
        results = {}
        
        # Test job creation
        job_data = {
            "title": f"Debug Test Job {datetime.now().isoformat()}",
            "company": "Debug Corp",
            "url": f"https://debug.com/job/{int(time.time())}"
        }
        
        try:
            # Create job
            start_time = time.time()
            create_response = self.session.post(
                f"{self.base_url}/api/jobs",
                json=job_data,
                headers={"Content-Type": "application/json"}
            )
            create_duration = time.time() - start_time
            
            results["create_job"] = {
                "status_code": create_response.status_code,
                "response_time": create_duration,
                "success": create_response.status_code == 201,
                "data": create_response.json() if create_response.headers.get('content-type', '').startswith('application/json') else create_response.text
            }
            
            # If job created successfully, test retrieval
            if create_response.status_code == 201:
                job_id = create_response.json().get("job_id")
                if job_id:
                    # Get job details
                    start_time = time.time()
                    get_response = self.session.get(f"{self.base_url}/api/jobs/{job_id}")
                    get_duration = time.time() - start_time
                    
                    results["get_job"] = {
                        "status_code": get_response.status_code,
                        "response_time": get_duration,
                        "success": get_response.status_code == 200,
                        "data": get_response.json() if get_response.headers.get('content-type', '').startswith('application/json') else get_response.text
                    }
            
            # Test duplicate creation (should fail with 409)
            start_time = time.time()
            dup_response = self.session.post(
                f"{self.base_url}/api/jobs",
                json=job_data,
                headers={"Content-Type": "application/json"}
            )
            dup_duration = time.time() - start_time
            
            results["duplicate_job"] = {
                "status_code": dup_response.status_code,
                "response_time": dup_duration,
                "success": dup_response.status_code == 409,  # Expected duplicate error
                "data": dup_response.json() if dup_response.headers.get('content-type', '').startswith('application/json') else dup_response.text
            }
            
        except Exception as e:
            results["error"] = str(e)
        
        return results
    
    def generate_debug_report(self) -> str:
        """Generate comprehensive debug report."""
        report = ["=== API Debug Report ==="]
        report.append(f"Timestamp: {datetime.now().isoformat()}")
        report.append(f"Base URL: {self.base_url}")
        report.append("")
        
        # Health checks
        report.append("=== Health Check Results ===")
        health_results = self.health_check_full()
        for service, result in health_results.items():
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            report.append(f"{service}: {status} (HTTP {result.get('status_code', 'N/A')})")
            if result.get("response_time"):
                report.append(f"  Response time: {result['response_time']:.3f}s")
            if not result["success"] and result.get("error"):
                report.append(f"  Error: {result['error']}")
        report.append("")
        
        # Job API tests
        report.append("=== Job API Test Results ===")
        job_results = self.test_job_api_flow()
        for test, result in job_results.items():
            if test != "error":
                status = "✅ PASS" if result["success"] else "❌ FAIL"
                report.append(f"{test}: {status} (HTTP {result.get('status_code', 'N/A')})")
                if result.get("response_time"):
                    report.append(f"  Response time: {result['response_time']:.3f}s")
        
        if "error" in job_results:
            report.append(f"Job API Error: {job_results['error']}")
        
        return "\n".join(report)

if __name__ == "__main__":
    debugger = APIDebugger()
    print(debugger.generate_debug_report())
```

### Docker Compose Debugging Commands
```bash
# Check service status
docker compose ps

# View service configuration
docker compose config

# Check container resources
docker compose top

# Inspect specific service
docker compose exec agents env

# Restart services in order
docker compose restart postgres mongo
sleep 10
docker compose restart agents jobspy_service
sleep 5
docker compose restart kong
```

## Integration Testing Scenarios

### End-to-End Workflow Test
```bash
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
```

## Debugging FAQ

### Q: API returns "Connection refused" or cannot reach localhost:8000
**A:** The services are not running or Kong gateway is not accessible.
- Check service status: `docker compose ps`
- Start services: `docker compose up -d`
- Wait for services to initialize: `sleep 30`
- Check Kong logs: `docker compose logs kong`

### Q: API returns 502 Bad Gateway
**A:** Kong cannot reach the backend service.
- Check service health: `docker compose ps`
- Verify Kong configuration: `curl http://localhost:8001/services`
- Check service logs: `docker compose logs kong agents jobspy_service`

### Q: Database connection errors
**A:** Database service is not accessible.
- Check database health: `curl http://localhost:8000/api/health/postgres`
- Verify containers: `docker compose ps postgres mongo`
- Check database logs: `docker compose logs postgres mongo`

### Q: Slow API responses
**A:** Performance issue with service or database.
- Monitor resources: `docker stats`
- Check for slow queries in database logs
- Verify network connectivity between containers

### Q: JSON parsing errors
**A:** Invalid request format or response corruption.
- Validate JSON with: `echo "$response" | python -m json.tool`
- Check Content-Type headers
- Verify request encoding

### Q: Service discovery failures
**A:** Services cannot find each other.
- Check Docker network: `docker network inspect trainium_trainium-net`
- Verify service names in docker-compose.yml
- Test internal connectivity: `docker compose exec kong ping agents`

---

*This debugging plan should be updated as the system evolves and new issues are discovered.*