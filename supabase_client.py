import requests
from typing import List, Dict, Any, Optional
from config import config
import json

class SupabaseClient:
    def __init__(self):
        self.supabase_url = config.SUPABASE_URL
        self.supabase_key = config.SUPABASE_ANON_KEY
        self.headers = {
            'apikey': self.supabase_key,
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': 'application/json'
        }
    
    def _make_request(self, method: str, endpoint: str, data: Dict | None = None) -> Dict:
        """Make a request to Supabase API"""
        url = f"{self.supabase_url}/rest/v1/{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=self.headers, json=data)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Supabase API error: {e}")
            return {}
    
    def get_part_info(self, part_number: str) -> Optional[Dict]:
        """Get part information from MASTER_FILE table"""
        try:
            # Query MASTER_FILE table for the part (case-sensitive column name)
            endpoint = f'MASTER_FILE?"PartNumber"=eq.{part_number}'
            result = self._make_request('GET', endpoint)
            
            if result and len(result) > 0:
                return result[0]  # Return first match
            return None
            
        except Exception as e:
            print(f"Error getting part info: {e}")
            return None
    
    def get_benchmark_suppliers(self, part_number: str) -> List[Dict]:
        """Get benchmark supplier information from PARTS_BENCHMARKS table"""
        try:
            # Query PARTS_BENCHMARKS table (update column name if needed)
            endpoint = f'PARTS_BENCHMARKS?"partnumber"=eq.{part_number}'
            result = self._make_request('GET', endpoint)
            
            if not result or len(result) == 0:
                return []
            
            benchmark_record = result[0]
            suppliers = []
            
            # Get current supplier details
            if benchmark_record.get('currentsuppliernumber'):
                current_supplier = self.get_supplier_details(benchmark_record['currentsuppliernumber'])
                if current_supplier:
                    current_supplier['is_current_supplier'] = True
                    current_supplier['is_panel_supplier'] = True
                    suppliers.append(current_supplier)
            
            # Get benchmark supplier prices and details
            # This is a simplified approach - you may need to adjust based on actual schema
            supplier_columns = ['SUP999', 'SUP001', 'SUP017', 'SUP012']
            
            for col in supplier_columns:
                if col in benchmark_record and benchmark_record[col] is not None:
                    supplier = self.get_supplier_details(col)
                    if supplier:
                        supplier['price'] = benchmark_record[col]
                        supplier['currency'] = benchmark_record.get('currency')
                        supplier['is_panel_supplier'] = True
                        suppliers.append(supplier)
            
            return suppliers
            
        except Exception as e:
            print(f"Error getting benchmark suppliers: {e}")
            return []
    
    def get_supplier_details(self, supplier_number: str) -> Optional[Dict]:
        """Get supplier details from SUPPLIER_PANEL_CATALOG table"""
        try:
            endpoint = f'SUPPLIER_PANEL_CATALOG?suppliernumber=eq.{supplier_number}'
            result = self._make_request('GET', endpoint)
            
            if result and len(result) > 0:
                return result[0]
            return None
            
        except Exception as e:
            print(f"Error getting supplier details: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Test the Supabase connection"""
        try:
            # Try to query a simple endpoint to test connection
            endpoint = 'MASTER_FILE?limit=1'
            result = self._make_request('GET', endpoint)
            return True
        except Exception as e:
            print(f"Supabase connection test failed: {e}")
            return False
    
    def list_tables(self) -> List[str]:
        """List available tables in the database"""
        try:
            # This is a simplified approach - you might need to adjust based on your Supabase setup
            tables = ['MASTER_FILE', 'PARTS_BENCHMARKS', 'SUPPLIER_PANEL_CATALOG']
            available_tables = []
            
            for table in tables:
                try:
                    endpoint = f"{table}?limit=1"
                    result = self._make_request('GET', endpoint)
                    if result is not None:
                        available_tables.append(table)
                except:
                    continue
            
            return available_tables
            
        except Exception as e:
            print(f"Error listing tables: {e}")
            return [] 