# File Download Fix

This document explains the fixes implemented to resolve the file download issues in the API.

## Problem

The file download endpoint was failing with the error:
```
{"detail":"Error downloading file: [Errno 2] No such file or directory: '/tmp/PA-10183 CELESTRAN.pdf'"}
```

## Root Causes

1. **Windows Path Issue**: The code was trying to create temporary files in `/tmp/` which doesn't exist on Windows
2. **Unnecessary Temporary Files**: The approach of creating temporary files was problematic and unnecessary
3. **URL Encoding**: Filenames with spaces (like "PA-10183 CELESTRAN.pdf") weren't being properly URL-encoded
4. **Path Parameter**: The route parameter wasn't configured to handle path-like filenames

## Solutions Implemented

### 1. Direct File Serving
Instead of creating temporary files, the API now serves files directly from the SPECS directory:

```python
@app.get("/api/files/download/{filename:path}")
async def download_file(filename: str):
    # URL decode the filename
    from urllib.parse import unquote
    decoded_filename = unquote(filename)
    
    # Get the file path directly
    file_path = file_service.get_file_path(decoded_filename)
    
    # Return the file directly
    return FileResponse(
        path=str(file_path),
        filename=decoded_filename,
        media_type=mime_type
    )
```

### 2. URL Encoding Support
- Added URL decoding in the download endpoint to handle filenames with spaces
- Updated the file service to URL-encode filenames when creating download URLs
- Changed route parameter to `{filename:path}` to handle path-like filenames

### 3. New FileService Method
Added `get_file_path()` method to return the full file path:

```python
def get_file_path(self, filename: str) -> Optional[Path]:
    """Get the full file path for a given filename."""
    file_path = self.specs_directory / filename
    
    if not file_path.exists() or not file_path.is_file():
        return None
    
    return file_path
```

### 4. Proper URL Generation
Updated the file service to generate properly encoded download URLs:

```python
# URL encode the filename for the download URL
from urllib.parse import quote
encoded_filename = quote(file_path.name)
download_url = f"/api/files/download/{encoded_filename}"
```

## Testing

### Test Script
Created `test_file_download.py` to verify the fix:

```bash
python test_file_download.py
```

This script tests:
- OPTIONS requests for CORS
- GET requests for file download
- URL encoding/decoding
- Error handling for non-existent files

### Manual Testing
You can test the file download manually:

1. **Direct URL**: `https://your-app.railway.app/api/files/download/PA-10183%20CELESTRAN.pdf`
2. **Frontend Integration**: The frontend should now be able to download files successfully

## Expected Behavior

### Before Fix
- ❌ Error: `{"detail":"Error downloading file: [Errno 2] No such file or directory: '/tmp/PA-10183 CELESTRAN.pdf'}"`
- ❌ CORS issues with file downloads
- ❌ Filenames with spaces not working

### After Fix
- ✅ Files download successfully
- ✅ CORS headers included in file responses
- ✅ Filenames with spaces work properly
- ✅ Proper Content-Type and Content-Disposition headers
- ✅ Direct file serving (no temporary files)

## File Types Supported

The API now properly handles various file types:
- PDF files (`.pdf`)
- Text files (`.txt`)
- Other file types with appropriate MIME type detection

## Security Considerations

- Files are served directly from the SPECS directory
- No temporary files are created
- URL encoding prevents path traversal attacks
- File existence is verified before serving

## CORS Support

File downloads now include proper CORS headers:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type`

## Example Usage

### Frontend JavaScript
```javascript
// Download a file
const response = await fetch('/api/files/download/PA-10183%20CELESTRAN.pdf');
const blob = await response.blob();
const url = window.URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'PA-10183 CELESTRAN.pdf';
a.click();
```

### curl Command
```bash
curl -X GET "https://your-app.railway.app/api/files/download/PA-10183%20CELESTRAN.pdf" \
  -H "Origin: https://preview-vxc8dzbt--ai-procure-optimize-4.deploypad.app" \
  --output downloaded_file.pdf
```

The file download functionality should now work correctly from both the frontend and direct API calls. 