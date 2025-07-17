import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from typing import List, Dict, Optional
import time
import re
from config import config
from schemas import SupplierInfo
import os
import PyPDF2

B2B_SITES = [
    "alibaba.com", "thomasnet.com", "europages.com", "kompass.com", "made-in-china.com", "campusplastics.com"
]

class WebScraper:
    def __init__(self):
        self.max_suppliers = config.MAX_ALTERNATIVE_SUPPLIERS
        self.timeout = config.WEB_SCRAPING_TIMEOUT
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def extract_keywords_from_spec(self, spec_path: str) -> Dict[str, str]:
        # Extract material, grade, process, and application from spec
        keywords = {"material": "", "grade": "", "process": "", "application": ""}
        if not spec_path or not os.path.exists(spec_path):
            return keywords
        ext = os.path.splitext(spec_path)[1].lower()
        text = ""
        try:
            if ext == '.txt':
                with open(spec_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
            elif ext == '.pdf':
                with open(spec_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    text = " ".join(page.extract_text() or '' for page in reader.pages)
            else:
                return keywords
            # Material (look for PPS, PA6, Celstran, etc.)
            material_match = re.search(r'(PPS|PA6|PA-6|Polyamide|Polypropylene|Polycarbonate|Celstran|Celanese|[A-Z]{2,10}-[A-Z0-9\-]+)', text)
            if material_match:
                keywords["material"] = material_match.group(0)
            # Grade (look for e.g. "CF40", "BKV30", "GF30", "PPS-CF40-01")
            grade_match = re.search(r'([A-Z]{2,10}-[A-Z0-9\-]+|CF\d{2}|GF\d{2}|BKV\d{2})', text)
            if grade_match:
                keywords["grade"] = grade_match.group(0)
            # Process (look for "injection molding", "extrusion", etc.)
            process_match = re.search(r'(injection molding|extrusion|blow molding|compression molding)', text, re.I)
            if process_match:
                keywords["process"] = process_match.group(0)
            # Application (look for "automotive", "electrical", etc.)
            app_match = re.search(r'(automotive|electrical|connector|housing|base|module|gear|bearing)', text, re.I)
            if app_match:
                keywords["application"] = app_match.group(0)
            return keywords
        except Exception as e:
            print(f"[WebScraper] Error extracting keywords from spec: {e}")
            return keywords

    def search_alternative_suppliers(self, part_number: str, part_name: str, material: Optional[str] = None, spec_path: Optional[str] = None, region: str = "Europe") -> List[SupplierInfo]:
        log = {"queries": [], "sources": []}
        suppliers = []
        # Extract keywords from spec
        spec_keywords = self.extract_keywords_from_spec(spec_path) if spec_path else {"material": material or "", "grade": "", "process": "", "application": ""}
        material_kw = spec_keywords.get("material") or material or ""
        grade_kw = spec_keywords.get("grade", "")
        process_kw = spec_keywords.get("process", "injection molding")
        app_kw = spec_keywords.get("application", "")
        # Generate queries
        queries = [
            f"{material_kw} {grade_kw} {process_kw} supplier {region}",
            f"{material_kw} {grade_kw} custom part manufacturer {region}",
            f"{material_kw} {grade_kw} component supplier {region}",
            f"engineering plastics supplier {material_kw} {grade_kw} {region}",
            f"{material_kw} {grade_kw} distributor {region}",
            f"{material_kw} {grade_kw} {process_kw} company {region}",
        ]
        # Add B2B site queries
        for site in B2B_SITES:
            queries.append(f"{material_kw} {grade_kw} {process_kw} site:{site}")
        # Remove duplicates
        queries = [q.strip() for q in list(dict.fromkeys(queries)) if q.strip()]
        # Search Google and B2B
        for query in queries:
            log["queries"].append(query)
            print(f"[WebScraper] Searching Google for: {query}")
            results = self._search_google(query, log)
            print(f"[WebScraper] Found {len(results)} suppliers for query: {query}")
            suppliers.extend(results)
            if len(suppliers) >= self.max_suppliers:
                break
        unique_suppliers = self._remove_duplicates(suppliers)
        print(f"[WebScraper] Returning {len(unique_suppliers)} unique web suppliers.")
        # Return only SupplierInfo objects (not dicts)
        return unique_suppliers[:self.max_suppliers]

    def _search_google(self, query: str, log: Optional[Dict] = None) -> List[SupplierInfo]:
        suppliers = []
        api_key = config.GOOGLE_API_KEY
        cse_id = config.GOOGLE_CSE_ID
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": cse_id,
            "q": query,
            "num": 8,
        }
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                for item in data.get("items", []):
                    title = item.get("title")
                    link = item.get("link")
                    desc = item.get("snippet", "")
                    if self._is_supplier_website(title, link):
                        suppliers.append(SupplierInfo(
                            supplier_number=f"WEB_{len(suppliers) + 1}",
                            supplier_name=title,
                            website=link,
                            description=desc,
                            is_web_found=True
                        ))
            else:
                print(f"[WebScraper] Google API error: {response.status_code} {response.text}")
        except Exception as e:
            print(f"[WebScraper] Error in Google Custom Search API: {e}")
        return suppliers

    def _is_supplier_website(self, title: str, url: str) -> bool:
        supplier_keywords = [
            'supplier', 'manufacturer', 'distributor', 'wholesale',
            'industrial', 'components', 'parts', 'machinery',
            'engineering', 'manufacturing', 'factory', 'plastics', 'polymer', 'company'
        ]
        title_lower = title.lower()
        if any(keyword in title_lower for keyword in supplier_keywords):
            return True
        url_lower = url.lower()
        if any(keyword in url_lower for keyword in supplier_keywords):
            return True
        return False

    def _remove_duplicates(self, suppliers: List[SupplierInfo]) -> List[SupplierInfo]:
        unique_suppliers = []
        seen_names = set()
        for supplier in suppliers:
            normalized_name = supplier.supplier_name.lower().replace(' ', '').replace('.', '')
            if normalized_name not in seen_names:
                seen_names.add(normalized_name)
                unique_suppliers.append(supplier)
        return unique_suppliers
    
    def get_supplier_details(self, supplier: SupplierInfo) -> Optional[Dict]:
        """
        Get additional details for a supplier by visiting their website.
        This is a basic implementation - you may want to enhance it.
        """
        if not supplier.website:
            return None
        
        try:
            response = self.session.get(supplier.website, timeout=self.timeout)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Try to extract contact information
                contact_info = {}
                
                # Look for email addresses
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                emails = re.findall(email_pattern, response.text)
                if emails:
                    contact_info['emails'] = emails[:3]  # Limit to first 3
                
                # Look for phone numbers
                phone_pattern = r'[\+]?[1-9][\d]{0,15}'
                phones = re.findall(phone_pattern, response.text)
                if phones:
                    contact_info['phones'] = phones[:3]  # Limit to first 3
                
                # Look for address information
                address_keywords = ['address', 'location', 'contact']
                for keyword in address_keywords:
                    elements = soup.find_all(text=re.compile(keyword, re.I))
                    if elements:
                        contact_info['address_hints'] = [elem.strip() for elem in elements[:2]]
                        break
                
                return contact_info
        
        except Exception as e:
            print(f"Error getting supplier details for {supplier.supplier_name}: {e}")
        
        return None 