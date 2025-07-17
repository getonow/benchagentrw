from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class PartAnalysisRequest(BaseModel):
    part_number: str

class SearchAlternativesRequest(BaseModel):
    part_number: str
    part_name: str
    material: str | None = None

class SupplierInfo(BaseModel):
    supplier_number: str
    supplier_name: str
    supplier_contact_name: Optional[str] = None
    supplier_contact_email: Optional[str] = None
    supplier_manufacturing_location: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    is_current_supplier: bool = False
    is_panel_supplier: bool = False
    is_web_found: bool = False

class PartInfo(BaseModel):
    part_number: str
    part_name: str
    material: Optional[str] = None
    material2: Optional[str] = None
    currency: str
    current_supplier: str
    current_price: float
    annual_volume: float
    annual_total_spend: float

class BenchmarkSummary(BaseModel):
    part_info: PartInfo
    supplier_comparison: str
    geographic_risk_assessment: Optional[str] = None
    strategic_recommendation: str
    potential_savings: Optional[float] = None
    savings_percentage: Optional[float] = None

class TechnicalSpec(BaseModel):
    filename: str
    file_path: str
    file_size: int
    file_type: str
    download_url: str

class PartAnalysisResponse(BaseModel):
    benchmark_summary: BenchmarkSummary
    technical_spec: Optional[TechnicalSpec] = None
    suppliers: List[SupplierInfo]
    success: bool
    message: str

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: Optional[str] = None 