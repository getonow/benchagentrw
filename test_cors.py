#!/usr/bin/env python3
"""
Test script to verify CORS configuration
"""

import requests
import json

def test_cors_configuration():
    """Test CORS configuration for the API"""
    base_url = "http://localhost:8099"
    
    # Test endpoints
    endpoints = [
        "/",
        "/health",
        "/api/health",
        "/api/database/test",
        "/api/parts/available"
    ]
    
    print("Testing CORS Configuration")
    print("=" * 50)
    
    for endpoint in endpoints:
        print(f"\nTesting {endpoint}:")
        
        # Test OPTIONS request (CORS preflight)
        try:
            options_response = requests.options(
                f"{base_url}{endpoint}",
                headers={
                    "Origin": "https://preview-vxc8dzbt--ai-procure-optimize-4.deploypad.app",
                    "Access-Control-Request-Method": "GET",
                    "Access-Control-Request-Headers": "Content-Type"
                }
            )
            
            print(f"  OPTIONS Status: {options_response.status_code}")
            print(f"  CORS Headers:")
            for header, value in options_response.headers.items():
                if header.lower().startswith('access-control'):
                    print(f"    {header}: {value}")
            
        except requests.exceptions.RequestException as e:
            print(f"  ❌ OPTIONS request failed: {e}")
        
        # Test GET request
        try:
            get_response = requests.get(f"{base_url}{endpoint}")
            print(f"  GET Status: {get_response.status_code}")
            
        except requests.exceptions.RequestException as e:
            print(f"  ❌ GET request failed: {e}")
    
    # Test POST endpoint
    print(f"\nTesting /api/analyze-part:")
    try:
        options_response = requests.options(
            f"{base_url}/api/analyze-part",
            headers={
                "Origin": "https://preview-vxc8dzbt--ai-procure-optimize-4.deploypad.app",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )
        
        print(f"  OPTIONS Status: {options_response.status_code}")
        print(f"  CORS Headers:")
        for header, value in options_response.headers.items():
            if header.lower().startswith('access-control'):
                print(f"    {header}: {value}")
        
    except requests.exceptions.RequestException as e:
        print(f"  ❌ OPTIONS request failed: {e}")

def test_frontend_origin():
    """Test with actual frontend origin"""
    base_url = "http://localhost:8099"
    frontend_origin = "https://preview-vxc8dzbt--ai-procure-optimize-4.deploypad.app"
    
    print(f"\nTesting with frontend origin: {frontend_origin}")
    print("=" * 60)
    
    # Test health endpoint
    try:
        response = requests.get(
            f"{base_url}/api/health",
            headers={"Origin": frontend_origin}
        )
        
        print(f"Health check status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Check CORS headers
        print(f"CORS Headers:")
        for header, value in response.headers.items():
            if header.lower().startswith('access-control'):
                print(f"  {header}: {value}")
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    print("Starting CORS test...")
    test_cors_configuration()
    test_frontend_origin()
    print("\nCORS test completed!") 