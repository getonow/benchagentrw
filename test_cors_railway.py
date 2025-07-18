#!/usr/bin/env python3
"""
Test script to verify CORS configuration with Railway deployment
"""

import requests
import json

def test_cors_with_railway():
    """Test CORS configuration with Railway deployment"""
    base_url = "https://web-production-b5bc8.up.railway.app"
    
    # Test endpoints
    endpoints = [
        "/health",
        "/api/health",
        "/api/cors-test",
        "/api/analyze-part"
    ]
    
    print("Testing CORS Configuration with Railway")
    print("=" * 60)
    print(f"Base URL: {base_url}")
    
    for endpoint in endpoints:
        print(f"\n{'='*50}")
        print(f"Testing: {endpoint}")
        print(f"{'='*50}")
        
        # Test OPTIONS request (CORS preflight)
        try:
            print(f"1. Testing OPTIONS request...")
            options_response = requests.options(
                f"{base_url}{endpoint}",
                headers={
                    "Origin": "http://localhost:3000",
                    "Access-Control-Request-Method": "GET" if "analyze-part" not in endpoint else "POST",
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
            
        except requests.exceptions.RequestException as e:
            print(f"   ❌ OPTIONS request failed: {e}")
        
        # Test actual request
        try:
            print(f"\n2. Testing actual request...")
            if "analyze-part" in endpoint:
                # POST request for analyze-part
                response = requests.post(
                    f"{base_url}{endpoint}",
                    headers={
                        "Origin": "http://localhost:3000",
                        "Content-Type": "application/json"
                    },
                    json={"part_number": "PA-10183"}
                )
            else:
                # GET request for other endpoints
                response = requests.get(
                    f"{base_url}{endpoint}",
                    headers={"Origin": "http://localhost:3000"}
                )
            
            print(f"   Status: {response.status_code}")
            print(f"   Response Headers:")
            for header, value in response.headers.items():
                if header.lower().startswith('access-control'):
                    print(f"     {header}: {value}")
            
            if response.status_code == 200:
                print(f"   ✅ Request successful")
                try:
                    data = response.json()
                    print(f"   Response: {json.dumps(data, indent=2)[:200]}...")
                except:
                    print(f"   Response: {response.text[:200]}...")
            else:
                print(f"   ❌ Request failed")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request failed: {e}")

def test_frontend_simulation():
    """Simulate frontend requests"""
    base_url = "https://web-production-b5bc8.up.railway.app"
    
    print(f"\n{'='*60}")
    print("Frontend Simulation Test")
    print(f"{'='*60}")
    
    # Simulate React frontend request
    frontend_headers = {
        "Origin": "http://localhost:3000",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    try:
        print("Testing analyze-part endpoint with frontend headers...")
        response = requests.post(
            f"{base_url}/api/analyze-part",
            headers=frontend_headers,
            json={"part_number": "PA-10183"}
        )
        
        print(f"Status: {response.status_code}")
        print(f"CORS Headers:")
        for header, value in response.headers.items():
            if header.lower().startswith('access-control'):
                print(f"  {header}: {value}")
        
        if response.status_code == 200:
            print("✅ Frontend request successful!")
        else:
            print(f"❌ Frontend request failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Frontend simulation failed: {e}")

if __name__ == "__main__":
    test_cors_with_railway()
    test_frontend_simulation()
    print("\n" + "="*60)
    print("CORS Test Completed!")
    print("="*60) 