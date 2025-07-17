import openai
from typing import List, Dict, Any, Optional
from config import config
from schemas import PartInfo, SupplierInfo, BenchmarkSummary

class AIAgent:
    def __init__(self):
        self.client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.OPENAI_MODEL
    
    def generate_benchmark_analysis(
        self,
        part_info: PartInfo,
        suppliers: List[SupplierInfo]
    ) -> BenchmarkSummary:
        """
        Generate AI-powered benchmark analysis and recommendations.
        """
        
        # Prepare data for AI analysis
        analysis_data = self._prepare_analysis_data(part_info, suppliers)
        
        # Generate AI analysis
        prompt = self._create_analysis_prompt(analysis_data)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are BENCHEXTRACT, an expert AI agent specializing in supplier negotiations and benchmarking. 
                        Your role is to analyze supplier pricing data and provide strategic recommendations for cost optimization and risk mitigation.
                        
                        You should:
                        1. Compare supplier prices objectively
                        2. Identify cost-saving opportunities
                        3. Assess supply chain risks
                        4. Provide actionable recommendations
                        5. Consider geographic and quality factors
                        
                        Be concise, professional, and data-driven in your analysis."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            ai_response = response.choices[0].message.content
            
            # Parse AI response and create structured summary
            if ai_response:
                return self._parse_ai_response(ai_response, part_info, suppliers)
            else:
                return self._generate_fallback_analysis(part_info, suppliers)
            
        except Exception as e:
            print(f"Error generating AI analysis: {e}")
            # Fallback to basic analysis
            return self._generate_fallback_analysis(part_info, suppliers)
    
    def _prepare_analysis_data(self, part_info: PartInfo, suppliers: List[SupplierInfo]) -> Dict[str, Any]:
        """Prepare structured data for AI analysis"""
        
        # Separate current, panel, and web suppliers
        current_suppliers = [s for s in suppliers if s.is_current_supplier]
        panel_suppliers = [s for s in suppliers if s.is_panel_supplier and not s.is_current_supplier]
        web_suppliers = [s for s in suppliers if s.is_web_found]
        
        # Calculate price statistics
        prices = [s.price for s in suppliers if s.price is not None]
        min_price = min(prices) if prices else part_info.current_price
        max_price = max(prices) if prices else part_info.current_price
        avg_price = sum(prices) / len(prices) if prices else part_info.current_price
        
        return {
            "part_info": {
                "part_number": part_info.part_number,
                "part_name": part_info.part_name,
                "material": part_info.material,
                "current_price": part_info.current_price,
                "annual_volume": part_info.annual_volume,
                "annual_spend": part_info.annual_total_spend,
                "currency": part_info.currency
            },
            "suppliers": {
                "current": [{"name": s.supplier_name, "price": s.price, "location": s.supplier_manufacturing_location} for s in current_suppliers],
                "panel": [{"name": s.supplier_name, "price": s.price, "location": s.supplier_manufacturing_location} for s in panel_suppliers],
                "web": [{"name": s.supplier_name, "website": s.website, "description": s.description} for s in web_suppliers]
            },
            "price_analysis": {
                "min_price": min_price,
                "max_price": max_price,
                "avg_price": avg_price,
                "price_range": max_price - min_price if prices else 0,
                "price_variance": ((max_price - min_price) / avg_price * 100) if avg_price > 0 else 0
            }
        }
    
    def _create_analysis_prompt(self, data: Dict[str, Any]) -> str:
        """Create a detailed prompt for AI analysis"""
        
        prompt = f"""
        Please analyze the following supplier benchmarking data and provide strategic recommendations:

        PART INFORMATION:
        - Part Number: {data['part_info']['part_number']}
        - Part Name: {data['part_info']['part_name']}
        - Material: {data['part_info']['material']}
        - Current Price: {data['part_info']['current_price']} {data['part_info']['currency']}
        - Annual Volume: {data['part_info']['annual_volume']:,.0f}
        - Annual Spend: {data['part_info']['annual_spend']:,.0f} {data['part_info']['currency']}

        CURRENT SUPPLIER:
        {self._format_suppliers(data['suppliers']['current'])}

        PANEL SUPPLIERS (Benchmarked):
        {self._format_suppliers(data['suppliers']['panel'])}

        WEB-FOUND ALTERNATIVES:
        {self._format_web_suppliers(data['suppliers']['web'])}

        PRICE ANALYSIS:
        - Price Range: {data['price_analysis']['price_range']:.2f} {data['part_info']['currency']}
        - Price Variance: {data['price_analysis']['price_variance']:.1f}%
        - Lowest Price: {data['price_analysis']['min_price']:.2f} {data['part_info']['currency']}
        - Highest Price: {data['price_analysis']['max_price']:.2f} {data['part_info']['currency']}

        Please provide:
        1. Supplier Comparison: Compare current vs benchmark suppliers
        2. Geographic Risk Assessment: Evaluate supply chain diversification
        3. Strategic Recommendation: Actionable next steps for negotiation or supplier selection
        4. Potential Savings: Calculate potential cost savings if switching to best alternative
        5. Risk Considerations: Any risks or factors to consider

        Format your response as a structured analysis with clear sections.
        """
        
        return prompt
    
    def _format_suppliers(self, suppliers: List[Dict]) -> str:
        """Format supplier list for prompt"""
        if not suppliers:
            return "None available"
        
        formatted = []
        for s in suppliers:
            price_info = f"Price: {s['price']:.2f}" if s.get('price') else "Price: Not available"
            location_info = f"Location: {s['location']}" if s.get('location') else ""
            formatted.append(f"- {s['name']} | {price_info} | {location_info}")
        
        return "\n".join(formatted)
    
    def _format_web_suppliers(self, suppliers: List[Dict]) -> str:
        """Format web suppliers for prompt"""
        if not suppliers:
            return "None found"
        
        formatted = []
        for s in suppliers:
            website_info = f"Website: {s['website']}" if s.get('website') else ""
            desc_info = f"Description: {s['description']}" if s.get('description') else ""
            formatted.append(f"- {s['name']} | {website_info} | {desc_info}")
        
        return "\n".join(formatted)
    
    def _parse_ai_response(self, ai_response: str, part_info: PartInfo, suppliers: List[SupplierInfo]) -> BenchmarkSummary:
        """Parse AI response and extract structured information"""
        
        # Extract potential savings
        potential_savings = 0
        savings_percentage = 0
        
        # Find the best alternative price
        alternative_prices = [s.price for s in suppliers if s.price and not s.is_current_supplier]
        if alternative_prices:
            best_price = min(alternative_prices)
            potential_savings = (part_info.current_price - best_price) * part_info.annual_volume
            savings_percentage = ((part_info.current_price - best_price) / part_info.current_price) * 100
        
        return BenchmarkSummary(
            part_info=part_info,
            supplier_comparison=self._extract_section(ai_response, "Supplier Comparison"),
            geographic_risk_assessment=self._extract_section(ai_response, "Geographic Risk Assessment"),
            strategic_recommendation=self._extract_section(ai_response, "Strategic Recommendation"),
            potential_savings=potential_savings,
            savings_percentage=savings_percentage
        )
    
    def _extract_section(self, text: str, section_name: str) -> str:
        """Extract a specific section from AI response"""
        try:
            # Look for section headers
            lines = text.split('\n')
            section_start = -1
            section_end = -1
            
            for i, line in enumerate(lines):
                if section_name.lower() in line.lower():
                    section_start = i + 1
                    break
            
            if section_start >= 0:
                # Find next section or end
                for i in range(section_start, len(lines)):
                    if any(keyword in lines[i].lower() for keyword in ['assessment', 'recommendation', 'consideration', 'summary']):
                        section_end = i
                        break
                
                if section_end == -1:
                    section_end = len(lines)
                
                return '\n'.join(lines[section_start:section_end]).strip()
        
        except Exception as e:
            print(f"Error extracting section {section_name}: {e}")
        
        return "Analysis not available"
    
    def _generate_fallback_analysis(self, part_info: PartInfo, suppliers: List[SupplierInfo]) -> BenchmarkSummary:
        """Generate basic analysis when AI is not available"""
        
        # Basic price comparison
        alternative_prices = [s.price for s in suppliers if s.price and not s.is_current_supplier]
        potential_savings = 0
        savings_percentage = 0
        
        if alternative_prices:
            best_price = min(alternative_prices)
            potential_savings = (part_info.current_price - best_price) * part_info.annual_volume
            savings_percentage = ((part_info.current_price - best_price) / part_info.current_price) * 100
        
        supplier_comparison = f"Found {len(alternative_prices)} alternative suppliers with prices ranging from {min(alternative_prices):.2f} to {max(alternative_prices):.2f} {part_info.currency}."
        
        strategic_recommendation = "Consider requesting quotes from alternative suppliers to validate pricing and explore cost-saving opportunities."
        
        return BenchmarkSummary(
            part_info=part_info,
            supplier_comparison=supplier_comparison,
            strategic_recommendation=strategic_recommendation,
            potential_savings=potential_savings,
            savings_percentage=savings_percentage
        ) 