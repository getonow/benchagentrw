import requests
import json

def test_search_alternatives():
    """Test the search alternatives endpoint"""
    url = "http://localhost:8099/api/search-alternatives"
    
    # Test data
    test_data = {
        "part_number": "PA-10183",
        "part_name": "Control Module Base",
        "material": "CELESTRAN"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("Testing search alternatives endpoint...")
        print(f"URL: {url}")
        print(f"Data being sent: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(url, json=test_data, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 422:
            print("422 Error - Validation Error Details:")
            try:
                error_details = response.json()
                print(json.dumps(error_details, indent=2))
            except:
                print("Raw response:", response.text)
        else:
            print("Response Body:")
            try:
                response_json = response.json()
                print(json.dumps(response_json, indent=2))
            except:
                print("Raw response:", response.text)
                
    except Exception as e:
        print(f"Error: {e}")

def test_health():
    """Test the health endpoint"""
    url = "http://localhost:8099/health"
    
    try:
        print("\nTesting health endpoint...")
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_database():
    """Test the database connection"""
    url = "http://localhost:8099/api/database/test"
    
    try:
        print("\nTesting database connection...")
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_health()
    test_database()
    test_search_alternatives() 