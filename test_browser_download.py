#!/usr/bin/env python3
"""
Test to simulate browser download behavior
"""

import requests
import urllib.parse

def test_direct_browser_access():
    """Test how browser would handle direct access"""
    base_url = "https://your-app.railway.app"
    filename = "PA-10183 CELESTRAN.pdf"
    encoded_filename = urllib.parse.quote(filename)
    
    print("Testing Direct Browser Access")
    print("=" * 40)
    print(f"URL to test in browser: {base_url}/api/files/download/{encoded_filename}")
    
    # Test with Accept header that includes PDF
    headers = {
        "Accept": "application/pdf,application/x-pdf,*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(
            f"{base_url}/api/files/download/{encoded_filename}",
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        print(f"Content-Disposition: {response.headers.get('Content-Disposition')}")
        
        # Check if browser would try to display inline
        content_disposition = response.headers.get('Content-Disposition', '')
        if 'inline' in content_disposition.lower():
            print("⚠️  Browser will try to display inline")
        elif 'attachment' in content_disposition.lower():
            print("✅ Browser will download as attachment")
        else:
            print("❓ Unknown disposition behavior")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

def test_with_different_accept_headers():
    """Test with different Accept headers"""
    base_url = "https://your-app.railway.app"
    filename = "PA-10183 CELESTRAN.pdf"
    encoded_filename = urllib.parse.quote(filename)
    
    print(f"\nTesting Different Accept Headers")
    print("=" * 40)
    
    test_headers = [
        {"Accept": "application/pdf"},
        {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"},
        {"Accept": "*/*"},
        {"Accept": "application/pdf,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
    ]
    
    for i, headers in enumerate(test_headers, 1):
        print(f"\nTest {i}: Accept: {headers['Accept']}")
        try:
            response = requests.get(
                f"{base_url}/api/files/download/{encoded_filename}",
                headers=headers
            )
            print(f"  Status: {response.status_code}")
            print(f"  Content-Type: {response.headers.get('Content-Type')}")
            print(f"  Content-Disposition: {response.headers.get('Content-Disposition')}")
        except Exception as e:
            print(f"  ❌ Failed: {e}")

if __name__ == "__main__":
    test_direct_browser_access()
    test_with_different_accept_headers()
    print("\nBrowser simulation tests completed!") 