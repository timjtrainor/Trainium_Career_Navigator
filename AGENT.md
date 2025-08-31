# AGENT Instructions for Trainium Career Navigator

This document provides comprehensive guidance for AI agents and automated systems interacting with the Trainium Career Navigator.

## Development Guidelines

- Use conventional commit messages.
- For Python services (agents, backend, jobspy_service), run `python -m py_compile` on changed modules.
- When the Kong configuration is modified, validate it with `python -c 'import yaml,sys; yaml.safe_load(open("gateway/kong.yml"))'`.
- The frontend and documentation currently have no automated checks.

## API Endpoints Overview

### Base URL
- **Local Development**: `http://localhost:8000`
- **API Base Path**: `/api`

### Authentication
Currently no authentication is required for API endpoints in development.

## Job Management API

### Create Job Post
**Endpoint**: `POST /api/jobs`

Creates a new job posting in the system.

**Required Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "string (required)",
  "company": "string (required)", 
  "url": "string (required)",
  "location": "string (optional)",
  "description": "string (optional)",
  "salary_min": "integer (optional)",
  "salary_max": "integer (optional)",
  "job_type": "string (optional)"
}
```

**Success Response** (HTTP 201):
```json
{
  "job_id": "uuid-generated-id",
  "message": "Job created successfully"
}
```

**Error Responses**:
- **HTTP 409**: Duplicate job (same title, company, and URL)
  ```json
  {
    "detail": "duplicate job"
  }
  ```
- **HTTP 422**: Validation error (missing required fields)
  ```json
  {
    "detail": "Field validation error details"
  }
  ```

### Get Job Details
**Endpoint**: `GET /api/jobs/{job_id}`

**Success Response** (HTTP 200):
```json
{
  "job_id": "string",
  "title": "string",
  "company": "string", 
  "url": "string",
  "source": "string",
  "updated_at": "ISO 8601 timestamp",
  "decision": "string",
  "salary_min": "integer",
  "salary_max": "integer",
  "job_type": "string",
  "description": "string",
  "location": "string",
  "evaluation": {
    "yes": "integer",
    "no": "integer", 
    "final_decision_bool": "boolean",
    "confidence": "float"
  }
}
```

### List Jobs
**Endpoint**: `GET /api/jobs/unique`

**Query Parameters**:
- `query`: Search term (optional)
- `company`: Filter by company (optional)
- `source`: Filter by job source (optional, array)
- `since`: Time window filter (optional, e.g., "24h", "7d", "30d")
- `hide`: Hide specific jobs (optional, array)
- `page`: Page number for pagination (default: 1)

**Response**:
```json
{
  "data": [
    {
      "job_id": "string",
      "title": "string",
      "company": "string",
      "url": "string",
      "source": "string",
      "updated_at": "ISO 8601 timestamp",
      "decision": "string",
      "salary_min": "integer",
      "salary_max": "integer", 
      "job_type": "string"
    }
  ],
  "meta": {
    "page": "integer",
    "page_count": "integer", 
    "total": "integer"
  }
}
```

## Health Check API

### Application Health
**Endpoint**: `GET /api/health`

**Response**:
```json
{
  "status": "ok",
  "environment": "local",
  "services": {
    "postgres": {
      "host": "postgres",
      "port": 5432
    },
    "mongo": {
      "host": "mongo", 
      "port": 27017
    }
  },
  "llm_providers": {
    "openai": true,
    "anthropic": false,
    "gemini": true
  },
  "via": "FastAPI behind Kong"
}
```

### Database Health
**Endpoints**: 
- `GET /api/health/postgres`
- `GET /api/health/mongo` 
- `GET /api/health/db`

## Automated Testing Guidelines

### Job Posting Test Scenarios

#### 1. Valid Job Post
```bash
curl -X POST http://localhost:8000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Software Engineer",
    "company": "Tech Corp",
    "url": "https://techcorp.com/jobs/swe",
    "location": "San Francisco, CA",
    "description": "We are looking for a skilled software engineer...",
    "salary_min": 90000,
    "salary_max": 130000,
    "job_type": "Full-time"
  }'
```

#### 2. Minimal Valid Job Post (required fields only)
```bash
curl -X POST http://localhost:8000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Backend Developer",
    "company": "StartupXYZ", 
    "url": "https://startupxyz.com/careers/backend"
  }'
```

#### 3. Duplicate Job Test (should return 409)
```bash
# First create a job, then repeat the same request
curl -X POST http://localhost:8000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Job",
    "company": "Test Company",
    "url": "https://test.com/job"
  }'
```

#### 4. Invalid Request (missing required fields)
```bash
curl -X POST http://localhost:8000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Incomplete Job"
  }'
```

### Test Validation

**Successful Job Creation**:
- HTTP status code: 201
- Response contains `job_id` and `message`
- Job can be retrieved via `GET /api/jobs/{job_id}`

**Error Handling**:
- Duplicate jobs return HTTP 409
- Missing required fields return HTTP 422
- Invalid JSON returns HTTP 422

### Environment Configuration for Testing

Ensure your test environment has:
1. `.env` file with valid database credentials
2. Running PostgreSQL database
3. Running Kong gateway
4. All services up via `docker compose up -d`

### Health Check Validation

Before running job posting tests, verify the system is healthy:
```bash
curl http://localhost:8000/api/health
```

Expected: HTTP 200 with `"status": "ok"`

## Error Handling

All API endpoints return consistent error responses:

**Format**:
```json
{
  "detail": "Error description"
}
```

**Common Error Codes**:
- `400`: Bad Request
- `404`: Not Found  
- `409`: Conflict (duplicate)
- `422`: Validation Error
- `500`: Internal Server Error

## Rate Limiting

Currently no rate limiting is implemented, but consider adding delays between requests in automated testing to avoid overwhelming the system.

## Data Validation

The API performs the following validation:
- **title**: Non-empty string
- **company**: Non-empty string
- **url**: Valid URL format
- **salary_min/max**: Positive integers if provided
- **salary_min** ≤ **salary_max** if both provided

## Notes for AI Agents

1. **Always check health endpoints** before making API calls
2. **Handle duplicate job scenarios** gracefully (409 responses are expected)
3. **Use appropriate delays** between bulk operations 
4. **Validate responses** and check HTTP status codes
5. **Log errors** for debugging when requests fail
6. **Test with minimal payloads** first, then add optional fields
7. **Verify job creation** by retrieving the created job via GET endpoint

