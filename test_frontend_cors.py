#!/usr/bin/env python3
"""
Test CORS with the specific frontend domain
"""

import requests
import json

def test_frontend_cors():
    """Test CORS with the specific frontend domain"""
    base_url = "https://web-production-b5bc8.up.railway.app"
    frontend_origin = "https://preview-4uxubwa7--ai-procure-optimize-5.deploypad.app"
    
    print("Testing CORS with Frontend Domain")
    print("=" * 60)
    print(f"API URL: {base_url}")
    print(f"Frontend Origin: {frontend_origin}")
    
    # Test OPTIONS preflight
    print(f"\n1. Testing OPTIONS preflight...")
    try:
        options_response = requests.options(
            f"{base_url}/api/analyze-part",
            headers={
                "Origin": frontend_origin,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type, Authorization, X-Requested-With"
            }
        )
        
        print(f"   Status: {options_response.status_code}")
        print(f"   CORS Headers:")
        cors_headers = [
            "Access-Control-Allow-Origin",
            "Access-Control-Allow-Methods", 
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Credentials",
            "Access-Control-Max-Age"
        ]
        
        for header in cors_headers:
            value = options_response.headers.get(header)
            if value:
                print(f"     {header}: {value}")
            else:
                print(f"     {header}: ❌ Missing")
                
    except Exception as e:
        print(f"   ❌ OPTIONS request failed: {e}")
    
    # Test actual POST request
    print(f"\n2. Testing POST request...")
    try:
        response = requests.post(
            f"{base_url}/api/analyze-part",
            headers={
                "Origin": frontend_origin,
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest"
            },
            json={"part_number": "PA-10116"}
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response Headers:")
        for header, value in response.headers.items():
            if header.lower().startswith('access-control'):
                print(f"     {header}: {value}")
        
        if response.status_code == 200:
            print(f"   ✅ Request successful!")
            try:
                data = response.json()
                print(f"   Response: {json.dumps(data, indent=2)[:300]}...")
            except:
                print(f"   Response: {response.text[:300]}...")
        else:
            print(f"   ❌ Request failed")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ POST request failed: {e}")

def test_simple_get():
    """Test a simple GET request"""
    base_url = "https://web-production-b5bc8.up.railway.app"
    frontend_origin = "https://preview-4uxubwa7--ai-procure-optimize-5.deploypad.app"
    
    print(f"\n3. Testing simple GET request...")
    try:
        response = requests.get(
            f"{base_url}/api/health",
            headers={"Origin": frontend_origin}
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   CORS Headers:")
        for header, value in response.headers.items():
            if header.lower().startswith('access-control'):
                print(f"     {header}: {value}")
        
        if response.status_code == 200:
            print(f"   ✅ GET request successful!")
        else:
            print(f"   ❌ GET request failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ GET request failed: {e}")

if __name__ == "__main__":
    test_frontend_cors()
    test_simple_get()
    print("\n" + "="*60)
    print("Frontend CORS Test Completed!")
    print("="*60) 