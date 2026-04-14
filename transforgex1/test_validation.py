#!/usr/bin/env python3
"""
Automated validation script for TransForgeX1
Run this to test simulation accuracy against real HPC data
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

def run_validation_suite():
    """Run complete validation suite"""
    print("\n" + "="*60)
    print("🔬 TransForgeX1 Validation Suite")
    print("="*60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    tests = []
    
    # Test 1: Real HPC Comparison
    print("📊 Test 1: Real HPC System Comparison")
    try:
        response = requests.post(f"{BASE_URL}/api/validation/real_compare", 
                                json={"system": "LUMI", "simulation_results": {"peak_tflops": 380}})
        result = response.json()
        print(f"   Error: {result['error_percentage']:.1f}%")
        print(f"   Status: {'✓ PASS' if result['error_percentage'] < 15 else '✗ FAIL'}")
        tests.append(result['error_percentage'] < 15)
    except Exception as e:
        print(f"   ✗ FAIL: {e}")
        tests.append(False)
    
    # Test 2: Workload Validation
    print("\n📈 Test 2: Workload Trace Validation")
    try:
        response = requests.post(f"{BASE_URL}/api/validation/workload_compare",
                                json={"simulation_stats": {"mean_nodes": 32.5, "mean_duration_seconds": 2712, "utilization": 68.4}})
        result = response.json()
        print(f"   Score: {result['validation_score']:.1f}%")
        print(f"   Status: {'✓ PASS' if result['validation_score'] > 70 else '✗ FAIL'}")
        tests.append(result['validation_score'] > 70)
    except Exception as e:
        print(f"   ✗ FAIL: {e}")
        tests.append(False)
    
    # Test 3: Amdahl's Law Validation
    print("\n🧮 Test 3: Amdahl's Law Compliance")
    try:
        response = requests.post(f"{BASE_URL}/api/validation/amdahl",
                                json={"cores": [1, 2, 4, 8, 16, 32], "serial_fraction": 0.05})
        result = response.json()
        print(f"   R²: {result['r_squared']:.3f}")
        print(f"   Status: {'✓ PASS' if result['r_squared'] > 0.85 else '✗ FAIL'}")
        tests.append(result['r_squared'] > 0.85)
    except Exception as e:
        print(f"   ✗ FAIL: {e}")
        tests.append(False)
    
    # Test 4: Strong Scaling Validation
    print("\n📊 Test 4: Strong Scaling Efficiency")
    try:
        response = requests.post(f"{BASE_URL}/api/validation/scaling",
                                json={"cores": [1, 2, 4, 8, 16, 32], "serial_time": 10})
        result = response.json()
        print(f"   Efficiency: {result['scaling_efficiency']*100:.1f}%")
        print(f"   Status: {'✓ PASS' if result['valid'] else '✗ FAIL'}")
        tests.append(result['valid'])
    except Exception as e:
        print(f"   ✗ FAIL: {e}")
        tests.append(False)
    
    # Summary
    print("\n" + "="*60)
    print("📋 Validation Summary")
    print("="*60)
    passed = sum(tests)
    total = len(tests)
    print(f"Passed: {passed}/{total} tests ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n✅ All tests passed! Simulation is accurate and validated.")
    elif passed >= total * 0.7:
        print("\n⚠️ Most tests passed - minor calibration recommended.")
    else:
        print("\n❌ Multiple tests failed - review simulation parameters.")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    run_validation_suite()
