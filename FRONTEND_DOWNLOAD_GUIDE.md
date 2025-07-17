# Frontend File Download Guide

This guide explains how to properly handle file downloads from the API to avoid the black screen issue.

## Problem Description

When clicking download in the frontend, users see a black screen instead of downloading the file. This happens because:

1. **Browser Behavior**: Modern browsers try to display PDFs inline when opened in a new tab
2. **Content-Disposition**: Even with `attachment` header, some browsers may still try to display the content
3. **Frontend Implementation**: The frontend might be using `window.open()` or direct links instead of proper download handling

## Root Cause

The black screen appears when the browser tries to display the PDF inline instead of downloading it. This happens when:

- Using `window.open()` with PDF URLs
- Using `<a href="..." target="_blank">` for PDF files
- Not setting the `download` attribute on links

## Solutions

### ✅ **Recommended Solution: Programmatic Download**

Use JavaScript to create a download link and trigger it programmatically:

```javascript
function downloadFile(filename, downloadUrl) {
    // Create a temporary link element
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = filename; // This forces download instead of display
    link.style.display = 'none';
    
    // Add to DOM, click, and remove
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Usage
downloadFile('PA-10183 CELESTRAN.pdf', '/api/files/download/PA-10183%20CELESTRAN.pdf');
```

### ✅ **Alternative Solution: Fetch and Blob Download**

For more control over the download process:

```javascript
async function fetchAndDownload(filename, downloadUrl) {
    try {
        const response = await fetch(downloadUrl);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        
        // Create download link
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        
        // Trigger download
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        // Clean up
        window.URL.revokeObjectURL(url);
        
        console.log('File downloaded successfully!');
    } catch (error) {
        console.error('Download failed:', error);
    }
}

// Usage
fetchAndDownload('PA-10183 CELESTRAN.pdf', '/api/files/download/PA-10183%20CELESTRAN.pdf');
```

### ✅ **React Component Example**

```jsx
import React from 'react';

const DownloadButton = ({ filename, downloadUrl }) => {
    const handleDownload = () => {
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = filename;
        link.style.display = 'none';
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <button onClick={handleDownload}>
            Download {filename}
        </button>
    );
};

// Usage
<DownloadButton 
    filename="PA-10183 CELESTRAN.pdf"
    downloadUrl="/api/files/download/PA-10183%20CELESTRAN.pdf"
/>
```

## ❌ **What NOT to Do**

### Don't use `window.open()`
```javascript
// ❌ This will show black screen
window.open('/api/files/download/PA-10183%20CELESTRAN.pdf', '_blank');
```

### Don't use direct links without download attribute
```html
<!-- ❌ This will show black screen -->
<a href="/api/files/download/PA-10183%20CELESTRAN.pdf" target="_blank">
    Download PDF
</a>
```

### Don't use iframe
```html
<!-- ❌ This will show black screen -->
<iframe src="/api/files/download/PA-10183%20CELESTRAN.pdf"></iframe>
```

## ✅ **What TO Do**

### Use download attribute
```html
<!-- ✅ This will download the file -->
<a href="/api/files/download/PA-10183%20CELESTRAN.pdf" download>
    Download PDF
</a>
```

### Use programmatic download
```javascript
// ✅ This will download the file
const link = document.createElement('a');
link.href = '/api/files/download/PA-10183%20CELESTRAN.pdf';
link.download = 'PA-10183 CELESTRAN.pdf';
link.click();
```

## API Response Details

The API returns files with these headers:
- `Content-Type: application/pdf`
- `Content-Disposition: attachment; filename="PA-10183 CELESTRAN.pdf"`
- `Content-Length: 86756`

## Testing

You can test the download functionality using the provided test page:

1. Open `test_download.html` in your browser
2. Try each download method
3. Verify that files download correctly instead of showing black screens

## Browser Compatibility

| Method | Chrome | Firefox | Safari | Edge |
|--------|--------|---------|--------|------|
| Programmatic Download | ✅ | ✅ | ✅ | ✅ |
| Fetch and Blob | ✅ | ✅ | ✅ | ✅ |
| Download Attribute | ✅ | ✅ | ✅ | ✅ |
| Window.open() | ❌ | ❌ | ❌ | ❌ |

## Error Handling

Always include error handling in your download functions:

```javascript
async function downloadFileWithErrorHandling(filename, downloadUrl) {
    try {
        const response = await fetch(downloadUrl);
        
        if (!response.ok) {
            throw new Error(`Download failed: ${response.status} ${response.statusText}`);
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        window.URL.revokeObjectURL(url);
        
        // Show success message
        console.log('Download completed successfully');
        
    } catch (error) {
        console.error('Download failed:', error);
        // Show error message to user
        alert(`Download failed: ${error.message}`);
    }
}
```

## Summary

To fix the black screen issue:

1. **Use programmatic downloads** instead of `window.open()`
2. **Set the `download` attribute** on links
3. **Use fetch + blob** for more control
4. **Include proper error handling**
5. **Test with the provided test page**

The key is to force the browser to download the file instead of trying to display it inline. 