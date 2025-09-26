import boto3
import json
from typing import Dict, Any, List

class CarbonAccountingAgent:
    def __init__(self):
        self.bedrock_client = boto3.client('bedrock-runtime')
        
    def calculate_overall_footprint(self, supply_chain_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall carbon footprint across supply chain"""
        
        # Extract data from other agents
        sourcing_data = supply_chain_data.get('sourcing', {})
        logistics_data = supply_chain_data.get('logistics', {})
        inventory_data = supply_chain_data.get('inventory', {})
        
        footprint_breakdown = self._calculate_footprint_breakdown(
            sourcing_data, logistics_data, inventory_data
        )
        
        total_footprint = sum(footprint_breakdown.values())
        
        return {
            'agent': 'carbon_accounting',
            'total_carbon_footprint_tons': total_footprint,
            'footprint_breakdown': footprint_breakdown,
            'footprint_percentage': self._calculate_percentages(footprint_breakdown, total_footprint),
            'reduction_opportunities': self._identify_reduction_opportunities(footprint_breakdown),
            'sustainability_score': self._calculate_overall_sustainability_score(supply_chain_data),
            'benchmarking': self._benchmark_performance(total_footprint)
        }
    
    def _calculate_footprint_breakdown(self, sourcing: Dict, logistics: Dict, inventory: Dict) -> Dict[str, float]:
        """Calculate carbon footprint by category"""
        
        # Sourcing emissions (from suppliers)
        sourcing_emissions = 0
        if 'analysis' in sourcing:
            sourcing_emissions = sum(
                supplier.get('carbon_footprint', 0) 
                for supplier in sourcing['analysis']
            )
        
        # Logistics emissions (from transportation)
        logistics_emissions = 0
        if 'optimized_routes' in logistics:
            logistics_emissions = sum(
                route.get('current_emissions', 0) 
                for route in logistics['optimized_routes']
            )
        
        # Inventory emissions (waste-related)
        inventory_emissions = 0
        if 'waste_analysis' in inventory:
            inventory_emissions = sum(
                item.get('waste_percentage', 0) * 0.1  # Convert waste % to emissions
                for item in inventory['waste_analysis']
            )
        
        return {
            'sourcing': sourcing_emissions,
            'logistics': logistics_emissions,
            'inventory_waste': inventory_emissions,
            'operations': sourcing_emissions * 0.2  # Estimate operational emissions
        }
    
    def _calculate_percentages(self, breakdown: Dict[str, float], total: float) -> Dict[str, float]:
        """Calculate percentage breakdown of emissions"""
        if total == 0:
            return {key: 0 for key in breakdown.keys()}
        
        return {
            key: round((value / total) * 100, 2) 
            for key, value in breakdown.items()
        }
    
    def _identify_reduction_opportunities(self, breakdown: Dict[str, float]) -> List[Dict[str, Any]]:
        """Identify top carbon reduction opportunities"""
        opportunities = []
        
        # Sort by emission amount to prioritize
        sorted_categories = sorted(breakdown.items(), key=lambda x: x[1], reverse=True)
        
        for category, emissions in sorted_categories[:3]:  # Top 3 categories
            if category == 'sourcing':
                opportunities.append({
                    'category': 'Supplier Management',
                    'potential_reduction_tons': emissions * 0.3,
                    'action': 'Switch to low-carbon suppliers and implement supplier sustainability programs'
                })
            elif category == 'logistics':
                opportunities.append({
                    'category': 'Transportation',
                    'potential_reduction_tons': emissions * 0.4,
                    'action': 'Optimize routes and switch to lower-emission transport modes'
                })
            elif category == 'inventory_waste':
                opportunities.append({
                    'category': 'Waste Reduction',
                    'potential_reduction_tons': emissions * 0.6,
                    'action': 'Implement demand forecasting and inventory optimization'
                })
        
        return opportunities
    
    def _calculate_overall_sustainability_score(self, supply_chain_data: Dict) -> float:
        """Calculate overall sustainability score (0-100)"""
        scores = []
        
        # Sourcing score
        sourcing_data = supply_chain_data.get('sourcing', {})
        if 'analysis' in sourcing_data:
            avg_supplier_score = sum(
                supplier.get('sustainability_score', 0) 
                for supplier in sourcing_data['analysis']
            ) / len(sourcing_data['analysis'])
            scores.append(avg_supplier_score)
        
        # Logistics score (based on emission reduction potential)
        logistics_data = supply_chain_data.get('logistics', {})
        if 'total_emission_reduction' in logistics_data:
            logistics_score = min(100, logistics_data['total_emission_reduction'] * 2)
            scores.append(logistics_score)
        
        # Inventory score (inverse of waste)
        inventory_data = supply_chain_data.get('inventory', {})
        if 'total_waste_reduction_potential' in inventory_data:
            inventory_score = min(100, 100 - inventory_data['total_waste_reduction_potential'])
            scores.append(inventory_score)
        
        return sum(scores) / len(scores) if scores else 50
    
    def _benchmark_performance(self, total_footprint: float) -> Dict[str, str]:
        """Benchmark performance against industry standards"""
        if total_footprint < 100:
            performance = 'Excellent'
            percentile = '90th'
        elif total_footprint < 300:
            performance = 'Good'
            percentile = '70th'
        elif total_footprint < 500:
            performance = 'Average'
            percentile = '50th'
        else:
            performance = 'Needs Improvement'
            percentile = '25th'
        
        return {
            'performance_rating': performance,
            'industry_percentile': percentile,
            'comparison': f'Your footprint is in the {percentile} percentile of similar companies'
        }