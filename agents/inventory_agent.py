import boto3
import json
import os
from typing import Dict, Any, List
from strands_client import StrandsWrapper

class InventoryAgent:
    def __init__(self):
        self.bedrock_client = boto3.client('bedrock-runtime')
        self.strands = StrandsWrapper(api_key=os.getenv('STRANDS_API_KEY'))
        
    def generate_waste_reduction_recommendations(self, inventory_data: List[Dict]) -> Dict[str, Any]:
        """Generate waste reduction recommendations for inventory"""
        recommendations = []
        waste_analysis = []
        
        for item in inventory_data:
            waste_metrics = self._analyze_waste_metrics(item)
            item_recommendations = self._generate_item_recommendations(item, waste_metrics)
            
            waste_analysis.append({
                'product_id': item.get('id'),
                'name': item.get('name'),
                'current_stock': item.get('current_stock', 0),
                'waste_percentage': waste_metrics['waste_percentage'],
                'expiry_risk': waste_metrics['expiry_risk'],
                'overstock_risk': waste_metrics['overstock_risk'],
                'recommendations': item_recommendations
            })
            
            recommendations.extend(item_recommendations)
        
        # Generate Strands-powered explanation
        strands_explanation = self.strands.generate_explanation({
            'waste_analysis': waste_analysis,
            'total_items': len(inventory_data)
        })
        
        return {
            'agent': 'inventory',
            'waste_analysis': waste_analysis,
            'total_waste_reduction_potential': self._calculate_total_waste_reduction(waste_analysis),
            'priority_actions': self._prioritize_recommendations(recommendations),
            'high_risk_items': [item for item in waste_analysis if item['waste_percentage'] > 15],
            'strands_explanation': strands_explanation,
            'strands_powered': True
        }
    
    def _analyze_waste_metrics(self, item: Dict) -> Dict[str, float]:
        """Analyze waste metrics for inventory item"""
        current_stock = item.get('current_stock', 0)
        demand_rate = item.get('monthly_demand', 1)
        shelf_life_days = item.get('shelf_life_days', 365)
        
        # Calculate waste percentage
        months_of_stock = current_stock / max(demand_rate, 1)
        waste_percentage = min(50, max(0, (months_of_stock - 3) * 5))
        
        # Expiry risk based on shelf life
        expiry_risk = 'High' if shelf_life_days < 30 else 'Medium' if shelf_life_days < 90 else 'Low'
        
        # Overstock risk
        overstock_risk = 'High' if months_of_stock > 6 else 'Medium' if months_of_stock > 3 else 'Low'
        
        return {
            'waste_percentage': waste_percentage,
            'expiry_risk': expiry_risk,
            'overstock_risk': overstock_risk,
            'months_of_stock': months_of_stock
        }
    
    def _generate_item_recommendations(self, item: Dict, metrics: Dict) -> List[str]:
        """Generate recommendations for specific inventory item"""
        recommendations = []
        
        if metrics['waste_percentage'] > 20:
            recommendations.append(f"Reduce order quantity for {item.get('name')} by 30%")
        
        if metrics['expiry_risk'] == 'High':
            recommendations.append(f"Implement FIFO system for {item.get('name')}")
        
        if metrics['overstock_risk'] == 'High':
            recommendations.append(f"Consider promotional pricing for {item.get('name')}")
        
        if metrics['months_of_stock'] > 6:
            recommendations.append(f"Halt new orders for {item.get('name')} until stock normalizes")
        
        return recommendations
    
    def _calculate_total_waste_reduction(self, analysis: List[Dict]) -> float:
        """Calculate total waste reduction potential"""
        total_current_waste = sum(item['waste_percentage'] for item in analysis)
        potential_reduction = min(80, total_current_waste * 0.6)  # Assume 60% reduction possible
        return potential_reduction
    
    def _prioritize_recommendations(self, recommendations: List[str]) -> List[str]:
        """Prioritize recommendations by impact"""
        priority_keywords = ['Halt', 'Reduce order', 'promotional pricing', 'FIFO']
        prioritized = []
        
        for keyword in priority_keywords:
            prioritized.extend([rec for rec in recommendations if keyword in rec])
        
        return list(dict.fromkeys(prioritized))  # Remove duplicates while preserving order