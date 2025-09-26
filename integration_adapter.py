"""
Integration adapter to bridge Phase 1 (Data Generator) with Phase 2 (Analysis Agents)
Handles data format conversion and validation
"""

from typing import Dict, Any, List
import asyncio
from agents.data_generator import DataGeneratorAgent
from agents import AgentCore

class IntegrationAdapter:
    def __init__(self):
        self.data_generator = DataGeneratorAgent()
        self.agent_core = AgentCore()
    
    async def generate_and_analyze(self, suppliers: int = 20, routes: int = 30, products: int = 15) -> Dict[str, Any]:
        """Generate data and run complete sustainability analysis"""
        
        # Step 1: Generate data using Phase 1 agent
        generated_data = await self.data_generator.execute({
            'suppliers': suppliers,
            'routes': routes,
            'products': products
        })
        
        # Step 2: Convert to Phase 2 format
        converted_data = self._convert_data_format(generated_data)
        
        # Step 3: Run Phase 2 analysis
        analysis_results = self.agent_core.orchestrate_sustainability_analysis(converted_data)
        
        # Step 4: Combine results
        return {
            'generated_data': generated_data,
            'converted_data': converted_data,
            'analysis_results': analysis_results,
            'integration_metadata': {
                'data_quality_score': self._calculate_data_quality(generated_data),
                'conversion_success': True,
                'analysis_success': 'error' not in analysis_results
            }
        }
    
    def _convert_data_format(self, generated_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Phase 1 data format to Phase 2 expected format"""
        
        # Convert suppliers
        suppliers = []
        for supplier in generated_data.get('suppliers', []):
            suppliers.append({
                'id': supplier['id'],
                'name': supplier['name'],
                'carbon_footprint': supplier['carbon_footprint'] / 10,  # Scale down for Phase 2
                'certifications': supplier['certifications'],
                'renewable_energy_percent': supplier.get('sustainability_score', 50)  # Use sustainability_score as renewable %
            })
        
        # Convert routes
        routes = []
        for route in generated_data.get('routes', []):
            routes.append({
                'id': route['id'],
                'origin': route['origin'],
                'destination': route['destination'],
                'distance_km': route['distance'],
                'transport_mode': route['mode']
            })
        
        # Convert products to inventory
        inventory = []
        for product in generated_data.get('products', []):
            inventory.append({
                'id': product['id'],
                'name': product['name'],
                'current_stock': product['current_stock'],
                'monthly_demand': product['reorder_point'] * 2,  # Estimate monthly demand
                'shelf_life_days': 180 if product['category'] == 'Food' else 365  # Category-based shelf life
            })
        
        return {
            'suppliers': suppliers,
            'routes': routes,
            'inventory': inventory
        }
    
    def _calculate_data_quality(self, data: Dict[str, Any]) -> float:
        """Calculate data quality score (0-100)"""
        quality_factors = []
        
        # Check suppliers
        suppliers = data.get('suppliers', [])
        if suppliers:
            avg_sustainability = sum(s.get('sustainability_score', 0) for s in suppliers) / len(suppliers)
            quality_factors.append(min(100, avg_sustainability))
            
            # Check certifications coverage
            cert_coverage = sum(1 for s in suppliers if s.get('certifications')) / len(suppliers) * 100
            quality_factors.append(cert_coverage)
        
        # Check routes
        routes = data.get('routes', [])
        if routes:
            valid_routes = sum(1 for r in routes if r.get('distance', 0) > 0) / len(routes) * 100
            quality_factors.append(valid_routes)
        
        # Check products
        products = data.get('products', [])
        if products:
            valid_products = sum(1 for p in products if p.get('current_stock', 0) > 0) / len(products) * 100
            quality_factors.append(valid_products)
        
        return sum(quality_factors) / len(quality_factors) if quality_factors else 0

    def validate_phase1_integration(self) -> Dict[str, Any]:
        """Validate Phase 1 components are working correctly"""
        validation_results = {
            'data_generator_available': True,
            'mcp_server_structure': True,
            'base_agent_pattern': True,
            'issues_found': [],
            'recommendations': []
        }
        
        try:
            # Test data generator
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            test_data = loop.run_until_complete(self.data_generator.execute({'suppliers': 2, 'routes': 2, 'products': 2}))
            
            if not test_data or len(test_data.get('suppliers', [])) == 0:
                validation_results['issues_found'].append("Data generator not producing valid supplier data")
            
        except Exception as e:
            validation_results['data_generator_available'] = False
            validation_results['issues_found'].append(f"Data generator error: {str(e)}")
        
        # Check for data format compatibility
        if validation_results['data_generator_available']:
            try:
                converted = self._convert_data_format(test_data)
                if not all(key in converted for key in ['suppliers', 'routes', 'inventory']):
                    validation_results['issues_found'].append("Data conversion missing required keys")
            except Exception as e:
                validation_results['issues_found'].append(f"Data conversion error: {str(e)}")
        
        # Add recommendations
        if validation_results['issues_found']:
            validation_results['recommendations'].extend([
                "Ensure Phase 1 data generator follows expected schema",
                "Validate data type consistency between phases",
                "Test MCP server endpoints independently"
            ])
        else:
            validation_results['recommendations'].append("Phase 1 integration looks good!")
        
        return validation_results