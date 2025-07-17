from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
import mimetypes

from supabase_client import SupabaseClient
from data_service import DataService
from file_service import FileService
from web_scraper import WebScraper
from ai_agent import AIAgent
from schemas import (
    PartAnalysisRequest, 
    PartAnalysisResponse, 
    ErrorResponse,
    SupplierInfo,
    SearchAlternativesRequest,
    PartInfo
)
from config import config

# Initialize FastAPI app
app = FastAPI(
    title="BENCHEXTRACT API",
    description="AI Negotiation & Benchmarking Agent Service",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "http://localhost:5173",  # Vite dev server
        "https://preview-vxc8dzbt--ai-procure-optimize-4.deploypad.app",  # Deployed frontend
        "https://*.deploypad.app",  # All deploypad subdomains
        "https://*.railway.app",  # Railway deployments
        "https://*.vercel.app",  # Vercel deployments
        "https://*.netlify.app",  # Netlify deployments
        "*"  # Allow all origins (for development only - remove in production)
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Initialize services
file_service = FileService()
web_scraper = WebScraper()
ai_agent = AIAgent()

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    # Test Supabase connection
    supabase = SupabaseClient()
    if supabase.test_connection():
        print("✅ Supabase connection successful")
    else:
        print("⚠️  Supabase connection failed - some features may not work")

# Global exception handler with CORS headers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "BENCHEXTRACT API - AI Negotiation & Benchmarking Agent Service",
        "version": "1.0.0",
        "status": "running"
    }

@app.options("/")
async def options_root():
    """Handle OPTIONS requests for root endpoint"""
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "86400",
        }
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "BENCHEXTRACT"}

@app.options("/health")
async def options_health():
    """Handle OPTIONS requests for health check"""
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "86400",
        }
    )

@app.get("/api/health")
async def api_health_check():
    """API health check endpoint for frontend"""
    return {"status": "healthy", "message": "BENCHEXTRACT API is running"}

@app.options("/api/health")
async def options_api_health():
    """Handle OPTIONS requests for API health check"""
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "86400",
        }
    )

@app.get("/api/database/test")
async def test_database_connection():
    """Test database connection via Supabase"""
    try:
        supabase = SupabaseClient()
        if supabase.test_connection():
            tables = supabase.list_tables()
            return {
                "success": True,
                "message": "Database connection successful",
                "available_tables": tables
            }
        else:
            return {
                "success": False,
                "message": "Database connection failed"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Database connection error: {str(e)}"
        }

@app.options("/api/database/test")
async def options_test_database():
    """Handle OPTIONS requests for database test"""
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "86400",
        }
    )

@app.options("/api/analyze-part")
async def options_analyze_part():
    """Handle OPTIONS requests for analyze-part endpoint"""
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Max-Age": "86400",
        }
    )

@app.post("/api/analyze-part", response_model=PartAnalysisResponse)
async def analyze_part(
    request: PartAnalysisRequest
):
    """
    Main endpoint to analyze a part and generate benchmark recommendations.
    
    This endpoint:
    1. Retrieves part information from MASTER_FILE
    2. Gets technical specification file
    3. Retrieves benchmark supplier data
    4. Searches for alternative suppliers on the web
    5. Generates AI-powered analysis and recommendations
    """
    
    try:
        # Initialize data service
        data_service = DataService()
        
        # Step 1: Get part information
        part_info = data_service.get_part_info(request.part_number)
        if not part_info:
            # Create demo part info for testing when not found in database
            part_info = PartInfo(
                part_number=request.part_number,
                part_name=f"Demo Part {request.part_number}",
                material="Demo Material",
                material2="Demo Material 2",
                currency="EUR",
                current_supplier="Demo Supplier GmbH",
                current_price=4.36,
                annual_volume=416580,
                annual_total_spend=1816291
            )
        
        # Step 2: Get technical specification file
        technical_spec = file_service.find_technical_spec(request.part_number)
        
        # Step 3: Get benchmark suppliers
        panel_suppliers = data_service.get_benchmark_suppliers(request.part_number)
        
        # Add demo suppliers if none found
        if not panel_suppliers:
            panel_suppliers = [
                SupplierInfo(
                    supplier_number="SUP999",
                    supplier_name="Global Parts Ltd",
                    supplier_contact_name="John Smith",
                    supplier_contact_email="john@globalparts.com",
                    supplier_manufacturing_location="Munich, Germany",
                    website="https://globalparts.com",
                    description="Leading supplier of industrial components",
                    price=3.71,
                    currency="EUR",
                    is_panel_supplier=True,
                    is_current_supplier=False
                ),
                SupplierInfo(
                    supplier_number="SUP001",
                    supplier_name="Euro Components GmbH",
                    supplier_contact_name="Maria Schmidt",
                    supplier_contact_email="maria@eurocomponents.de",
                    supplier_manufacturing_location="Berlin, Germany",
                    website="https://eurocomponents.de",
                    description="Specialized in precision engineering",
                    price=4.15,
                    currency="EUR",
                    is_panel_supplier=True,
                    is_current_supplier=False
                )
            ]
        
        # Step 4: Search for web alternatives
        web_suppliers = web_scraper.search_alternative_suppliers(
            part_number=request.part_number,
            part_name=part_info.part_name,
            material=part_info.material
        )
        
        # Combine all suppliers
        all_suppliers = panel_suppliers + web_suppliers
        
        # Step 5: Generate AI analysis
        benchmark_summary = ai_agent.generate_benchmark_analysis(
            part_info=part_info,
            suppliers=all_suppliers
        )
        
        # Prepare response
        response = PartAnalysisResponse(
            benchmark_summary=benchmark_summary,
            technical_spec=technical_spec,
            suppliers=all_suppliers,
            success=True,
            message=f"Successfully analyzed part {request.part_number}"
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error analyzing part {request.part_number}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.options("/api/files/download/{filename:path}")
async def options_download_file(filename: str):
    """Handle OPTIONS requests for file download"""
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "86400",
        }
    )

@app.get("/api/files/download/{filename:path}")
async def download_file(filename: str):
    """
    Download technical specification file.
    """
    try:
        # URL decode the filename in case it contains spaces or special characters
        from urllib.parse import unquote
        decoded_filename = unquote(filename)
        
        # Get the file path from the file service
        file_path = file_service.get_file_path(decoded_filename)
        if not file_path or not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"File {decoded_filename} not found"
            )
        
        # Determine MIME type
        mime_type, _ = mimetypes.guess_type(decoded_filename)
        if not mime_type:
            mime_type = "application/octet-stream"
        
        # Return the file directly from the SPECS directory
        return FileResponse(
            path=str(file_path),
            filename=decoded_filename,
            media_type=mime_type
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error downloading file {filename}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error downloading file: {str(e)}"
        )

@app.options("/api/parts/available")
async def options_available_parts():
    """Handle OPTIONS requests for available parts"""
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "86400",
        }
    )

@app.get("/api/parts/available")
async def get_available_parts():
    """
    Get list of available part numbers based on files in SPECS directory.
    """
    try:
        parts = file_service.list_available_parts()
        return {
            "success": True,
            "parts": parts,
            "count": len(parts)
        }
    except Exception as e:
        print(f"Error getting available parts: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving available parts: {str(e)}"
        )

@app.options("/api/suppliers/{part_number}")
async def options_suppliers_for_part(part_number: str):
    """Handle OPTIONS requests for suppliers endpoint"""
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "86400",
        }
    )

@app.get("/api/suppliers/{part_number}")
async def get_suppliers_for_part(
    part_number: str
):
    """
    Get all suppliers (current + benchmark) for a specific part.
    """
    try:
        data_service = DataService()
        suppliers = data_service.get_all_suppliers_for_part(part_number)
        
        return {
            "success": True,
            "part_number": part_number,
            "suppliers": suppliers,
            "count": len(suppliers)
        }
    except Exception as e:
        print(f"Error getting suppliers for part {part_number}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving suppliers: {str(e)}"
        )

@app.options("/api/supplier/{supplier_number}")
async def options_supplier_details(supplier_number: str):
    """Handle OPTIONS requests for supplier details"""
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "86400",
        }
    )

@app.get("/api/supplier/{supplier_number}")
async def get_supplier_details(
    supplier_number: str
):
    """
    Get detailed information for a specific supplier.
    """
    try:
        data_service = DataService()
        supplier = data_service.get_supplier_details(supplier_number)
        
        if not supplier:
            raise HTTPException(
                status_code=404,
                detail=f"Supplier {supplier_number} not found"
            )
        
        return {
            "success": True,
            "supplier": supplier
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting supplier details for {supplier_number}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving supplier details: {str(e)}"
        )

@app.options("/api/search-alternatives")
async def options_search_alternatives():
    """Handle OPTIONS requests for search alternatives"""
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Max-Age": "86400",
        }
    )

@app.post("/api/search-alternatives")
async def search_alternative_suppliers(
    request: SearchAlternativesRequest
):
    """
    Search for alternative suppliers on the web.
    """
    try:
        suppliers = web_scraper.search_alternative_suppliers(
            part_number=request.part_number,
            part_name=request.part_name,
            material=request.material
        )
        
        return {
            "success": True,
            "part_number": request.part_number,
            "suppliers": suppliers,
            "count": len(suppliers)
        }
    except Exception as e:
        print(f"Error searching alternatives for {request.part_number}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error searching alternatives: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=config.DEBUG
    ) 