// React CORS Test Script
// Copy and paste this into your React app's browser console

const API_BASE = 'https://web-production-b5bc8.up.railway.app';

// Test 1: Simple GET request
async function testGetRequest() {
    console.log('🔍 Testing GET request...');
    try {
        const response = await fetch(`${API_BASE}/health`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
        
        console.log('✅ GET Response Status:', response.status);
        console.log('✅ GET Response Headers:', Object.fromEntries(response.headers.entries()));
        
        const data = await response.json();
        console.log('✅ GET Response Data:', data);
        return true;
    } catch (error) {
        console.error('❌ GET Request Failed:', error);
        return false;
    }
}

// Test 2: POST request with JSON body
async function testPostRequest() {
    console.log('🔍 Testing POST request...');
    try {
        const response = await fetch(`${API_BASE}/api/analyze-part`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({
                part_number: 'PA-10116'
            })
        });
        
        console.log('✅ POST Response Status:', response.status);
        console.log('✅ POST Response Headers:', Object.fromEntries(response.headers.entries()));
        
        const data = await response.json();
        console.log('✅ POST Response Data:', data);
        return true;
    } catch (error) {
        console.error('❌ POST Request Failed:', error);
        return false;
    }
}

// Test 3: OPTIONS preflight request
async function testOptionsRequest() {
    console.log('🔍 Testing OPTIONS preflight...');
    try {
        const response = await fetch(`${API_BASE}/api/analyze-part`, {
            method: 'OPTIONS',
            headers: {
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type, Authorization, X-Requested-With'
            }
        });
        
        console.log('✅ OPTIONS Response Status:', response.status);
        console.log('✅ OPTIONS Response Headers:', Object.fromEntries(response.headers.entries()));
        return true;
    } catch (error) {
        console.error('❌ OPTIONS Request Failed:', error);
        return false;
    }
}

// Test 4: CORS debug endpoint
async function testCorsDebug() {
    console.log('🔍 Testing CORS debug endpoint...');
    try {
        const response = await fetch(`${API_BASE}/api/cors-debug`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
        
        console.log('✅ CORS Debug Response Status:', response.status);
        console.log('✅ CORS Debug Response Headers:', Object.fromEntries(response.headers.entries()));
        
        const data = await response.json();
        console.log('✅ CORS Debug Response Data:', data);
        return true;
    } catch (error) {
        console.error('❌ CORS Debug Request Failed:', error);
        return false;
    }
}

// Test 5: Simulate React fetch with credentials
async function testReactFetch() {
    console.log('🔍 Testing React-style fetch...');
    try {
        const response = await fetch(`${API_BASE}/api/analyze-part`, {
            method: 'POST',
            credentials: 'include', // This is important for React apps
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({
                part_number: 'PA-10116'
            })
        });
        
        console.log('✅ React Fetch Response Status:', response.status);
        console.log('✅ React Fetch Response Headers:', Object.fromEntries(response.headers.entries()));
        
        const data = await response.json();
        console.log('✅ React Fetch Response Data:', data);
        return true;
    } catch (error) {
        console.error('❌ React Fetch Failed:', error);
        return false;
    }
}

// Run all tests
async function runAllTests() {
    console.log('🚀 Starting comprehensive CORS tests...');
    console.log('📍 Current Origin:', window.location.origin);
    console.log('🌐 API Base URL:', API_BASE);
    
    const results = {
        get: await testGetRequest(),
        post: await testPostRequest(),
        options: await testOptionsRequest(),
        corsDebug: await testCorsDebug(),
        reactFetch: await testReactFetch()
    };
    
    console.log('📊 Test Results:', results);
    
    const allPassed = Object.values(results).every(result => result);
    if (allPassed) {
        console.log('🎉 All tests passed! CORS is working correctly.');
    } else {
        console.log('⚠️ Some tests failed. Check the errors above.');
    }
    
    return results;
}

// Export functions for manual testing
window.corsTests = {
    testGetRequest,
    testPostRequest,
    testOptionsRequest,
    testCorsDebug,
    testReactFetch,
    runAllTests
};

console.log('🔧 CORS test functions loaded. Run corsTests.runAllTests() to start testing.'); 