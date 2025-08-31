# Debugging Scripts for Trainium Career Navigator

This directory contains debugging and testing scripts for the Trainium Career Navigator API system.

## Available Scripts

### Health Check Scripts
- **`comprehensive_health_check.sh`** - Comprehensive health check of all services
- **`smoke_test.sh`** - Existing smoke test for basic functionality

### API Testing Scripts
- **`api_endpoint_test.sh`** - Test job API endpoints (create, get, list)
- **`api_debug_test.py`** - Python-based comprehensive API testing and reporting
- **`curl-debug.sh`** - Advanced cURL debugging with detailed output
- **`e2e_workflow_test.sh`** - End-to-end workflow testing

### Performance Testing
- **`load_test.sh`** - Simple load testing for API endpoints

### Validation Scripts
- **`validate_debug_plan.py`** - Validates the debugging plan implementation

## Usage

### Prerequisites
Ensure you have the following installed:
- Docker and Docker Compose
- curl
- Python 3.11+ with required packages (requests, pyyaml)

### Basic Health Check
```bash
# Start services first
docker compose up -d

# Wait for services to initialize
sleep 30

# Run health check
./scripts/comprehensive_health_check.sh
```

### Complete API Testing
```bash
# Run comprehensive API tests
python scripts/api_debug_test.py

# Or run bash-based endpoint tests
./scripts/api_endpoint_test.sh
```

### End-to-End Testing
```bash
# Test complete workflow
./scripts/e2e_workflow_test.sh
```

### Performance Testing
```bash
# Run load tests
./scripts/load_test.sh
```

## Debugging Workflow

1. **Start with health checks** - Always verify system health first
2. **Check service status** - Ensure all containers are running
3. **Test individual endpoints** - Isolate issues to specific services
4. **Review logs** - Check container logs for detailed error information
5. **Test end-to-end** - Verify complete workflows function correctly

## Integration with Main Debugging Plan

These scripts implement the debugging procedures outlined in the main `api_debugging_plan.md` document. Refer to that document for:
- Detailed troubleshooting procedures
- Error code explanations
- Service-specific debugging steps
- Configuration validation methods

## Contributing

When adding new debugging scripts:
1. Make them executable: `chmod +x script_name.sh`
2. Follow the existing naming convention
3. Include comprehensive error handling
4. Add usage documentation to this README
5. Test scripts against both working and broken scenarios