#!/usr/bin/env python3
"""
Test script to verify file download functionality
"""

import requests
import urllib.parse

def test_file_download():
    """Test file download functionality"""
    base_url = "https://your-app.railway.app"
    
    # Test with a file that has spaces in the name
    filename = "PA-10183 CELESTRAN.pdf"
    encoded_filename = urllib.parse.quote(filename)
    
    print("Testing File Download")
    print("=" * 50)
    print(f"Original filename: {filename}")
    print(f"URL encoded filename: {encoded_filename}")
    
    # Test OPTIONS request
    print(f"\n1. Testing OPTIONS request:")
    try:
        options_response = requests.options(
            f"{base_url}/api/files/download/{encoded_filename}",
            headers={
                "Origin": "https://preview-vxc8dzbt--ai-procure-optimize-4.deploypad.app"
            }
        )
        print(f"   Status: {options_response.status_code}")
        print(f"   CORS Headers:")
        for header, value in options_response.headers.items():
            if header.lower().startswith('access-control'):
                print(f"     {header}: {value}")
    except Exception as e:
        print(f"   ❌ OPTIONS request failed: {e}")
    
    # Test GET request
    print(f"\n2. Testing GET request:")
    try:
        get_response = requests.get(
            f"{base_url}/api/files/download/{encoded_filename}",
            headers={
                "Origin": "https://preview-vxc8dzbt--ai-procure-optimize-4.deploypad.app"
            }
        )
        print(f"   Status: {get_response.status_code}")
        print(f"   Content-Type: {get_response.headers.get('Content-Type', 'Not set')}")
        print(f"   Content-Length: {get_response.headers.get('Content-Length', 'Not set')}")
        print(f"   Content-Disposition: {get_response.headers.get('Content-Disposition', 'Not set')}")
        
        if get_response.status_code == 200:
            print(f"   ✅ File download successful!")
            print(f"   File size: {len(get_response.content)} bytes")
            
            # Save the file to verify it's correct
            with open("test_download.pdf", "wb") as f:
                f.write(get_response.content)
            print(f"   File saved as 'test_download.pdf' for verification")
        else:
            print(f"   ❌ File download failed")
            print(f"   Response: {get_response.text}")
            
    except Exception as e:
        print(f"   ❌ GET request failed: {e}")
    
    # Test with a file that doesn't exist
    print(f"\n3. Testing with non-existent file:")
    try:
        response = requests.get(f"{base_url}/api/files/download/nonexistent.pdf")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Request failed: {e}")

def test_available_parts():
    """Test the available parts endpoint"""
    base_url = "https://your-app.railway.app"
    
    print(f"\n4. Testing available parts:")
    try:
        response = requests.get(f"{base_url}/api/parts/available")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Available parts: {data.get('count', 0)}")
            parts = data.get('parts', [])
            for part in parts[:5]:  # Show first 5 parts
                print(f"     - {part}")
            if len(parts) > 5:
                print(f"     ... and {len(parts) - 5} more")
        else:
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Request failed: {e}")

if __name__ == "__main__":
    print("Starting file download test...")
    test_file_download()
    test_available_parts()
    print("\nFile download test completed!") 