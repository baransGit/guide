#!/usr/bin/env python3
# Test Runner - All Tests
# Tum testleri calistiran ana script

import sys
import os
import subprocess
import asyncio
from pathlib import Path

# Test dizinlerini tanimla
TEST_DIR = Path(__file__).parent
UNIT_TESTS = TEST_DIR / "unit"
INTEGRATION_TESTS = TEST_DIR / "integration"  
SCENARIO_TESTS = TEST_DIR / "scenarios"

def run_command(cmd, description):
    """Komut calistir ve sonucu logla"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print(f"STDERR: {result.stderr}")
        
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            return True
        else:
            print(f"❌ {description} - FAILED (return code: {result.returncode})")
            return False
            
    except Exception as error:
        print(f"💥 {description} - ERROR: {str(error)}")
        return False

async def run_async_scenario(script_path, description):
    """Async scenario testlerini calistir"""
    print(f"\n{'='*60}")
    print(f"🎭 {description}")
    print(f"{'='*60}")
    
    try:
        # Python script'i async olarak calistir
        process = await asyncio.create_subprocess_exec(
            sys.executable, str(script_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if stdout:
            print(stdout.decode())
        
        if stderr:
            print(f"STDERR: {stderr.decode()}")
        
        if process.returncode == 0:
            print(f"✅ {description} - PASSED")
            return True
        else:
            print(f"❌ {description} - FAILED")
            return False
            
    except Exception as error:
        print(f"💥 {description} - ERROR: {str(error)}")
        return False

async def main():
    """Ana test runner"""
    print("🚀 Sydney Guide - Complete Test Suite")
    print("🔧 Running Unit Tests → Integration Tests → Scenario Tests")
    
    results = []
    
    # 1. Unit Tests
    unit_test_files = list(UNIT_TESTS.glob("test_*.py"))
    for test_file in unit_test_files:
        cmd = f"cd {TEST_DIR.parent} && python3 -m pytest {test_file} -v"
        success = run_command(cmd, f"Unit Test: {test_file.name}")
        results.append(("Unit", test_file.name, success))
    
    # 2. Integration Tests  
    integration_test_files = list(INTEGRATION_TESTS.glob("test_*.py"))
    for test_file in integration_test_files:
        cmd = f"cd {TEST_DIR.parent} && python3 -m pytest {test_file} -v"
        success = run_command(cmd, f"Integration Test: {test_file.name}")
        results.append(("Integration", test_file.name, success))
    
    # 3. Scenario Tests
    scenario_test_files = list(SCENARIO_TESTS.glob("*_scenario.py"))
    for test_file in scenario_test_files:
        success = await run_async_scenario(test_file, f"Scenario Test: {test_file.name}")
        results.append(("Scenario", test_file.name, success))
    
    # Test ozeti
    print(f"\n{'='*60}")
    print("📊 TEST RESULTS SUMMARY")
    print(f"{'='*60}")
    
    passed = 0
    failed = 0
    
    for test_type, test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {test_type:12} | {test_name}")
        
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📈 Overall Results:")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📊 Total:  {passed + failed}")
    
    if failed == 0:
        print(f"\n🎉 ALL TESTS PASSED! Sydney Guide is ready for production!")
        return True
    else:
        print(f"\n⚠️  Some tests failed. Please review and fix before deployment.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 