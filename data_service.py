from typing import List, Optional, Dict, Any
from schemas import PartInfo, SupplierInfo
from supabase_client import SupabaseClient

class DataService:
    def __init__(self):
        self.supabase = SupabaseClient()
    
    def get_part_info(self, part_number: str) -> Optional[PartInfo]:
        """
        Retrieve part information from MASTER_FILE table via Supabase.
        """
        master_record = self.supabase.get_part_info(part_number)
        
        if not master_record:
            return None
        
        # Calculate annual volume for 2025
        volume_columns_2025 = [
            'voljan2025', 'volfeb2025', 'volmar2025', 'volapr2025',
            'volmay2025', 'voljun2025', 'voljul2025', 'volaug2025',
            'volsep2025', 'voloct2025', 'volnov2025', 'voldec2025'
        ]
        
        annual_volume = sum(
            master_record.get(col, 0) or 0 
            for col in volume_columns_2025
        )
        
        # Calculate average price for 2025
        price_columns_2025 = [
            'pricejan2025', 'pricefeb2025', 'pricemar2025', 'priceapr2025',
            'pricemay2025', 'pricejun2025', 'pricejul2025', 'priceaug2025',
            'pricesep2025', 'priceoct2025', 'pricenov2025', 'pricedec2025'
        ]
        
        prices = [master_record.get(col) for col in price_columns_2025]
        prices = [p for p in prices if p is not None]
        current_price = sum(prices) / len(prices) if prices else 0
        
        annual_total_spend = annual_volume * current_price
        
        return PartInfo(
            part_number=str(master_record.get('partnumber', '')),
            part_name=str(master_record.get('partname', '')),
            material=str(master_record.get('material', '')) if master_record.get('material') else None,
            material2=str(master_record.get('material2', '')) if master_record.get('material2') else None,
            currency=str(master_record.get('currency', '')),
            current_supplier=str(master_record.get('suppliername', '')),
            current_price=current_price,
            annual_volume=annual_volume,
            annual_total_spend=annual_total_spend
        )
    
    def get_benchmark_suppliers(self, part_number: str) -> List[SupplierInfo]:
        """
        Retrieve benchmark supplier information from PARTS_BENCHMARKS and SUPPLIER_PANEL_CATALOG via Supabase.
        """
        suppliers_data = self.supabase.get_benchmark_suppliers(part_number)
        suppliers = []
        
        for supplier_data in suppliers_data:
            supplier = SupplierInfo(
                supplier_number=str(supplier_data.get('suppliernumber', '')),
                supplier_name=str(supplier_data.get('suppliername', '')),
                supplier_contact_name=str(supplier_data.get('suppliercontactname', '')) if supplier_data.get('suppliercontactname') else None,
                supplier_contact_email=str(supplier_data.get('suppliercontactemail', '')) if supplier_data.get('suppliercontactemail') else None,
                supplier_manufacturing_location=str(supplier_data.get('suppliermanufacturinglocation', '')) if supplier_data.get('suppliermanufacturinglocation') else None,
                website=str(supplier_data.get('website', '')) if supplier_data.get('website') else None,
                description=str(supplier_data.get('description', '')) if supplier_data.get('description') else None,
                price=supplier_data.get('price'),
                currency=supplier_data.get('currency'),
                is_current_supplier=supplier_data.get('is_current_supplier', False),
                is_panel_supplier=supplier_data.get('is_panel_supplier', False)
            )
            suppliers.append(supplier)
        
        return suppliers
    
    def get_all_suppliers_for_part(self, part_number: str) -> List[SupplierInfo]:
        """
        Get all suppliers (current + benchmark) for a part.
        """
        part_info = self.get_part_info(part_number)
        if not part_info:
            return []
        
        suppliers = self.get_benchmark_suppliers(part_number)
        
        # Add current supplier if not already in the list
        current_supplier_exists = any(s.is_current_supplier for s in suppliers)
        if not current_supplier_exists and part_info:
            suppliers.append(SupplierInfo(
                supplier_number="CURRENT",
                supplier_name=part_info.current_supplier,
                price=part_info.current_price,
                currency=part_info.currency,
                is_current_supplier=True
            ))
        
        return suppliers
    
    def get_supplier_details(self, supplier_number: str) -> Optional[SupplierInfo]:
        """
        Get detailed supplier information from SUPPLIER_PANEL_CATALOG via Supabase.
        """
        supplier_data = self.supabase.get_supplier_details(supplier_number)
        
        if not supplier_data:
            return None
        
        return SupplierInfo(
            supplier_number=str(supplier_data.get('suppliernumber', '')),
            supplier_name=str(supplier_data.get('suppliername', '')),
            supplier_contact_name=str(supplier_data.get('suppliercontactname', '')) if supplier_data.get('suppliercontactname') else None,
            supplier_contact_email=str(supplier_data.get('suppliercontactemail', '')) if supplier_data.get('suppliercontactemail') else None,
            supplier_manufacturing_location=str(supplier_data.get('suppliermanufacturinglocation', '')) if supplier_data.get('suppliermanufacturinglocation') else None,
            website=str(supplier_data.get('website', '')) if supplier_data.get('website') else None,
            description=str(supplier_data.get('description', '')) if supplier_data.get('description') else None,
            is_panel_supplier=True
        ) 