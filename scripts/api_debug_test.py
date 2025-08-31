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