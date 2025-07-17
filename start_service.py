#!/usr/bin/env python3
"""
Startup script for BENCHEXTRACT service
This script helps users start the service with proper configuration
"""

import os
import sys
import subprocess
import uvicorn
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'psycopg2-binary',
        'pydantic',
        'openai',
        'requests',
        'beautifulsoup4',
        'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nPlease install missing packages:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def check_environment():
    """Check if environment variables are set"""
    required_vars = ['OPENAI_API_KEY']
    optional_vars = ['DATABASE_URL', 'SPECS_DIRECTORY']
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
    
    for var in optional_vars:
        if not os.getenv(var):
            missing_optional.append(var)
    
    if missing_required:
        print("❌ Missing required environment variables:")
        for var in missing_required:
            print(f"   - {var}")
        print("\nPlease set these variables in your .env file")
        return False
    
    if missing_optional:
        print("⚠️  Missing optional environment variables:")
        for var in missing_optional:
            print(f"   - {var}")
        print("These will use default values")
    
    print("✅ Environment configuration is valid")
    return True

def check_specs_directory():
    """Check if SPECS directory exists and contains files"""
    specs_dir = os.getenv('SPECS_DIRECTORY', 'C:/Development/benchagent/SPECS')
    specs_path = Path(specs_dir)
    
    if not specs_path.exists():
        print(f"❌ SPECS directory not found: {specs_dir}")
        print("Please create the directory and add technical specification files")
        return False
    
    files = list(specs_path.glob('*'))
    if not files:
        print(f"⚠️  SPECS directory is empty: {specs_dir}")
        print("Please add technical specification files")
        return False
    
    print(f"✅ SPECS directory found with {len(files)} files")
    return True

def check_database_connection():
    """Check database connection (optional)"""
    try:
        from database import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"⚠️  Database connection failed: {e}")
        print("The service will work with limited functionality")
        return False

def start_service():
    """Start the BENCHEXTRACT service"""
    print("\n🚀 Starting BENCHEXTRACT service...")
    
    # Get configuration
    host = os.getenv('API_HOST', '0.0.0.0')
    port = int(os.getenv('API_PORT', '8000'))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Debug: {debug}")
    print(f"   API URL: http://{host}:{port}")
    print(f"   Docs: http://{host}:{port}/docs")
    
    try:
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=debug,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Service stopped by user")
    except Exception as e:
        print(f"\n❌ Failed to start service: {e}")

def main():
    """Main function"""
    print("BENCHEXTRACT Service Startup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ main.py not found. Please run this script from the benchagent directory")
        sys.exit(1)
    
    # Run checks
    checks_passed = True
    
    print("\n1. Checking dependencies...")
    if not check_dependencies():
        checks_passed = False
    
    print("\n2. Checking environment...")
    if not check_environment():
        checks_passed = False
    
    print("\n3. Checking SPECS directory...")
    if not check_specs_directory():
        checks_passed = False
    
    print("\n4. Checking database connection...")
    check_database_connection()  # This is optional
    
    if not checks_passed:
        print("\n❌ Some checks failed. Please fix the issues above before starting the service.")
        sys.exit(1)
    
    print("\n✅ All checks passed!")
    
    # Ask user if they want to start the service
    response = input("\nDo you want to start the service now? (y/n): ")
    if response.lower() in ['y', 'yes']:
        start_service()
    else:
        print("Service startup cancelled")

if __name__ == "__main__":
    main() 