import requests
import json

def test_single_endpoint():
    """Test the single analyze-part endpoint that does everything"""
    url = "http://localhost:8099/api/analyze-part"
    
    # Only part number needed
    test_data = {
        "part_number": "PA-10183"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("Testing single endpoint that does everything...")
        print(f"URL: {url}")
        print(f"Input (only part number): {json.dumps(test_data, indent=2)}")
        print("\n" + "="*60)
        
        response = requests.post(url, json=test_data, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS! Single endpoint working perfectly!")
            response_json = response.json()
            
            print("\n📊 RESPONSE STRUCTURE:")
            print("1. ✅ Success status")
            print("2. ✅ Benchmark Summary (Part info + Analysis)")
            print("3. ✅ Technical Specification (File info)")
            print("4. ✅ Suppliers List (All suppliers)")
            
            print("\n📋 DETAILED RESPONSE:")
            print(json.dumps(response_json, indent=2))
            
            # Verify all required sections are present
            required_sections = ['benchmark_summary', 'technical_spec', 'suppliers']
            missing_sections = []
            
            for section in required_sections:
                if section in response_json:
                    print(f"✅ {section.upper()} section present")
                else:
                    missing_sections.append(section)
                    print(f"❌ {section.upper()} section missing")
            
            if not missing_sections:
                print("\n🎉 ALL SECTIONS PRESENT! Ready for frontend!")
            else:
                print(f"\n⚠️  Missing sections: {missing_sections}")
                
        elif response.status_code == 422:
            print("❌ 422 Error - Validation Error Details:")
            try:
                error_details = response.json()
                print(json.dumps(error_details, indent=2))
            except:
                print("Raw response:", response.text)
        else:
            print(f"❌ Error {response.status_code}:")
            try:
                error_details = response.json()
                print(json.dumps(error_details, indent=2))
            except:
                print("Raw response:", response.text)
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_single_endpoint() 