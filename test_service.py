#!/usr/bin/env python3
"""
Test script for BENCHEXTRACT service
This script demonstrates how to use the API endpoints
"""

import requests
import json
import time
from typing import Dict, Any

class BenchExtractClient:
    def __init__(self, base_url: str = "https://your-app.railway.app"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the service is running"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_available_parts(self) -> Dict[str, Any]:
        """Get list of available parts"""
        try:
            response = self.session.get(f"{self.base_url}/api/parts/available")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_part(self, part_number: str) -> Dict[str, Any]:
        """Analyze a specific part"""
        try:
            payload = {"part_number": part_number}
            response = self.session.post(
                f"{self.base_url}/api/analyze-part",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_suppliers_for_part(self, part_number: str) -> Dict[str, Any]:
        """Get suppliers for a specific part"""
        try:
            response = self.session.get(f"{self.base_url}/api/suppliers/{part_number}")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def search_alternatives(self, part_number: str, part_name: str, material: str | None = None) -> Dict[str, Any]:
        """Search for alternative suppliers"""
        try:
            payload = {
                "part_number": part_number,
                "part_name": part_name
            }
            if material:
                payload["material"] = material
            
            response = self.session.post(
                f"{self.base_url}/api/search-alternatives",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}

def print_json(data: Dict[str, Any], title: str = ""):
    """Pretty print JSON data"""
    if title:
        print(f"\n{'='*50}")
        print(f"{title}")
        print(f"{'='*50}")
    print(json.dumps(data, indent=2))

def main():
    """Main test function"""
    print("BENCHEXTRACT Service Test")
    print("=" * 50)
    
    # Initialize client
    client = BenchExtractClient()
    
    # Test 1: Health check
    print_json(client.health_check(), "1. Health Check")
    
    # Test 2: Get available parts
    print_json(client.get_available_parts(), "2. Available Parts")
    
    # Test 3: Analyze a specific part (using a part that exists in SPECS)
    part_number = "PA-10183"
    print_json(client.analyze_part(part_number), f"3. Part Analysis for {part_number}")
    
    # Test 4: Get suppliers for the part
    print_json(client.get_suppliers_for_part(part_number), f"4. Suppliers for {part_number}")
    
    # Test 5: Search for alternatives
    print_json(
        client.search_alternatives(part_number, "Control Module Base", "CELESTRAN"),
        f"5. Alternative Suppliers for {part_number}"
    )
    
    print("\n" + "="*50)
    print("Test completed!")

def test_without_database():
    """Test the service without database connection (file operations only)"""
    print("BENCHEXTRACT Service Test (File Operations Only)")
    print("=" * 50)
    
    client = BenchExtractClient()
    
    # Test 1: Health check
    print_json(client.health_check(), "1. Health Check")
    
    # Test 2: Get available parts (this should work without database)
    print_json(client.get_available_parts(), "2. Available Parts")
    
    print("\n" + "="*50)
    print("File operations test completed!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--file-only":
        test_without_database()
    else:
        main() 