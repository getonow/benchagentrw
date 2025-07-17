#!/bin/bash

# Test CORS configuration with curl commands
echo "Testing CORS Configuration with curl"
echo "===================================="

BASE_URL="http://localhost:8099"
FRONTEND_ORIGIN="https://preview-vxc8dzbt--ai-procure-optimize-4.deploypad.app"

echo -e "\n1. Testing OPTIONS request for /api/health:"
curl -X OPTIONS "$BASE_URL/api/health" \
  -H "Origin: $FRONTEND_ORIGIN" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v

echo -e "\n\n2. Testing GET request for /api/health:"
curl -X GET "$BASE_URL/api/health" \
  -H "Origin: $FRONTEND_ORIGIN" \
  -v

echo -e "\n\n3. Testing OPTIONS request for /api/analyze-part:"
curl -X OPTIONS "$BASE_URL/api/analyze-part" \
  -H "Origin: $FRONTEND_ORIGIN" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v

echo -e "\n\n4. Testing POST request for /api/analyze-part:"
curl -X POST "$BASE_URL/api/analyze-part" \
  -H "Origin: $FRONTEND_ORIGIN" \
  -H "Content-Type: application/json" \
  -d '{"part_number": "PA-10183"}' \
  -v

echo -e "\n\n5. Testing OPTIONS request for /api/parts/available:"
curl -X OPTIONS "$BASE_URL/api/parts/available" \
  -H "Origin: $FRONTEND_ORIGIN" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v

echo -e "\n\n6. Testing GET request for /api/parts/available:"
curl -X GET "$BASE_URL/api/parts/available" \
  -H "Origin: $FRONTEND_ORIGIN" \
  -v

echo -e "\n\nCORS test completed!" 