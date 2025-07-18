# CORS Configuration Setup

This document explains the CORS (Cross-Origin Resource Sharing) configuration that has been implemented to allow the frontend application to communicate with the backend API.

## What was implemented

### 1. CORS Middleware
Added FastAPI CORS middleware to `main.py` with the following configuration:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Local development URLs removed for cloud deployment
        "https://preview-vxc8dzbt--ai-procure-optimize-4.deploypad.app",  # Deployed frontend
        "https://*.deploypad.app",  # All deploypad subdomains
        "*"  # Allow all origins (for development only - remove in production)
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
```

### 2. OPTIONS Handlers
Added explicit OPTIONS handlers for all endpoints to handle CORS preflight requests:

- `/` - Root endpoint
- `/health` - Health check
- `/api/health` - API health check
- `/api/database/test` - Database test
- `/api/analyze-part` - Part analysis
- `/api/files/download/{filename}` - File download
- `/api/parts/available` - Available parts
- `/api/suppliers/{part_number}` - Suppliers for part
- `/api/supplier/{supplier_number}` - Supplier details
- `/api/search-alternatives` - Search alternatives

### 3. Global Exception Handler
Added a global exception handler that includes CORS headers in error responses.

### 4. Port Configuration
Updated the default API port from 8000 to 8099 in `config.py` to match the frontend's expected port.

## Testing the CORS Configuration

### Method 1: Using the Python test script
```bash
python test_cors.py
```

### Method 2: Using curl commands
```bash
# On Windows PowerShell:
bash test_cors_curl.sh

# Or run individual commands:
curl -X OPTIONS "https://your-app.railway.app/api/health" \
  -H "Origin: https://preview-vxc8dzbt--ai-procure-optimize-4.deploypad.app" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v
```

### Method 3: Browser Developer Tools
1. Open your frontend application
2. Open browser developer tools (F12)
3. Go to the Network tab
4. Try to make a request to the API
5. Check if the request succeeds and look for CORS headers in the response

## Expected CORS Headers

When CORS is working correctly, you should see these headers in the response:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: *
Access-Control-Max-Age: 86400
```

## Troubleshooting

### 1. "Failed to fetch" error
- Make sure the backend is running on port 8099
- Check that the CORS middleware is properly configured
- Verify that the frontend origin is in the `allow_origins` list

### 2. CORS preflight fails
- Ensure OPTIONS handlers are implemented for all endpoints
- Check that the `Access-Control-Request-Method` and `Access-Control-Request-Headers` are properly handled

### 3. Port mismatch
- Verify that the backend is running on the correct port (8099)
- Check the `config.py` file for the correct port configuration

### 4. HTTPS to HTTP issues
- Modern browsers block HTTPS frontend to HTTP backend requests
- Consider using a local development setup where both frontend and backend run on HTTP
- Or deploy the backend to HTTPS

## Security Notes

⚠️ **Important**: The current configuration includes `"*"` in `allow_origins` which allows all origins. This should be removed in production for security reasons.

For production, use specific origins:
```python
allow_origins=[
    "https://your-production-domain.com",
    "https://your-staging-domain.com"
]
```

## Restart Required

After making these changes, you need to restart your FastAPI backend server for the CORS configuration to take effect:

```bash
# Stop the current server (Ctrl+C)
# Then restart it:
python main.py
# or
python start_service.py
```

## Verification

To verify that CORS is working:

1. Start your backend server on port 8099
2. Open your frontend application
3. Try to make a request to the API
4. Check the browser's Network tab for successful requests
5. Look for CORS headers in the response

The frontend should now be able to successfully communicate with your backend API without CORS errors. 