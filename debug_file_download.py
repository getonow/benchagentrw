#!/usr/bin/env python3
"""
Debug script to examine file download response in detail
"""

import requests
import urllib.parse
import os

def debug_file_download():
    """Debug file download response"""
    base_url = "https://your-app.railway.app"
    filename = "PA-10183 CELESTRAN.pdf"
    encoded_filename = urllib.parse.quote(filename)
    
    print("Debugging File Download Response")
    print("=" * 50)
    print(f"Filename: {filename}")
    print(f"Encoded: {encoded_filename}")
    print(f"URL: {base_url}/api/files/download/{encoded_filename}")
    
    try:
        response = requests.get(
            f"{base_url}/api/files/download/{encoded_filename}",
            headers={
                "Origin": "https://preview-vxc8dzbt--ai-procure-optimize-4.deploypad.app"
            }
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers:")
        for header, value in response.headers.items():
            print(f"  {header}: {value}")
        
        print(f"\nContent Length: {len(response.content)} bytes")
        print(f"Content Type: {response.headers.get('Content-Type', 'Not set')}")
        print(f"Content Disposition: {response.headers.get('Content-Disposition', 'Not set')}")
        
        # Check if content looks like a PDF
        content = response.content
        if content.startswith(b'%PDF'):
            print("✅ Content starts with PDF signature (%PDF)")
        else:
            print("❌ Content does not start with PDF signature")
            print(f"First 20 bytes: {content[:20]}")
        
        # Save the file and check its properties
        debug_filename = "debug_download.pdf"
        with open(debug_filename, "wb") as f:
            f.write(content)
        
        print(f"\nFile saved as: {debug_filename}")
        print(f"File size: {os.path.getsize(debug_filename)} bytes")
        
        # Try to open and read the first few lines
        try:
            with open(debug_filename, "rb") as f:
                first_line = f.readline().decode('utf-8', errors='ignore').strip()
                print(f"First line: {first_line}")
        except Exception as e:
            print(f"Error reading first line: {e}")
        
    except Exception as e:
        print(f"❌ Request failed: {e}")

def test_browser_simulation():
    """Simulate browser behavior"""
    base_url = "https://your-app.railway.app"
    filename = "PA-10183 CELESTRAN.pdf"
    encoded_filename = urllib.parse.quote(filename)
    
    print(f"\nBrowser Simulation Test")
    print("=" * 30)
    
    # Simulate browser headers
    browser_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0"
    }
    
    try:
        response = requests.get(
            f"{base_url}/api/files/download/{encoded_filename}",
            headers=browser_headers
        )
        
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        print(f"Content-Disposition: {response.headers.get('Content-Disposition')}")
        print(f"Content-Length: {response.headers.get('Content-Length')}")
        
        # Check if it's a valid PDF
        if response.content.startswith(b'%PDF'):
            print("✅ Valid PDF content detected")
        else:
            print("❌ Invalid PDF content")
            
    except Exception as e:
        print(f"❌ Browser simulation failed: {e}")

if __name__ == "__main__":
    debug_file_download()
    test_browser_simulation()
    print("\nDebug completed!") 