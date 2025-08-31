#!/usr/bin/env python3
"""
Simple debug test to validate the API debugging plan works with the current system.
"""

import sys
import json
from pathlib import Path

# Add the project root to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

def test_python_compilation():
    """Test that Python modules compile correctly."""
    print("Testing Python module compilation...")
    
    import subprocess
    
    modules_to_test = [
        "agents/app/main.py",
        "jobspy_service/app/main.py",
        "agents/app/config.py"
    ]
    
    for module in modules_to_test:
        try:
            result = subprocess.run(
                ["python", "-m", "py_compile", module],
                cwd=Path(__file__).resolve().parents[1],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"✅ {module} compiles successfully")
            else:
                print(f"❌ {module} compilation failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error testing {module}: {e}")
            return False
    
    return True

def test_configuration_files():
    """Test configuration file validity."""
    print("\nTesting configuration files...")
    
    try:
        import yaml
        with open(Path(__file__).resolve().parents[1] / "gateway/kong.yml") as f:
            yaml.safe_load(f)
        print("✅ Kong configuration is valid YAML")
    except Exception as e:
        print(f"❌ Kong configuration error: {e}")
        return False
    
    # Check .env.example exists
    env_example = Path(__file__).resolve().parents[1] / ".env.example"
    if env_example.exists():
        print("✅ .env.example file exists")
    else:
        print("❌ .env.example file missing")
        return False
    
    return True

def validate_debugging_plan():
    """Validate the debugging plan components."""
    print("\nValidating debugging plan components...")
    
    # Check if debugging scripts exist
    scripts_dir = Path(__file__).resolve().parent
    
    required_scripts = [
        "comprehensive_health_check.sh",
        "api_endpoint_test.sh", 
        "curl-debug.sh",
        "e2e_workflow_test.sh",
        "api_debug_test.py"
    ]
    
    for script in required_scripts:
        script_path = scripts_dir / script
        if script_path.exists():
            print(f"✅ Debug script exists: {script}")
        else:
            print(f"❌ Missing debug script: {script}")
            return False
    
    # Check if main debugging plan exists
    plan_path = Path(__file__).resolve().parents[1] / "api_debugging_plan.md"
    if plan_path.exists():
        print("✅ API debugging plan document exists")
    else:
        print("❌ API debugging plan document missing")
        return False
    
    return True

def main():
    """Run all validation tests."""
    print("=== API Debugging Plan Validation ===")
    
    success = True
    
    # Test Python compilation
    if not test_python_compilation():
        success = False
    
    # Test configuration files
    if not test_configuration_files():
        success = False
    
    # Validate debugging plan
    if not validate_debugging_plan():
        success = False
    
    print(f"\n=== Validation {'PASSED' if success else 'FAILED'} ===")
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())