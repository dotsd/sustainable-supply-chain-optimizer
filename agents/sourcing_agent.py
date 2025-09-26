import boto3
import json
from typing import Dict, Any, List

class SourcingAgent:
    def __init__(self):
        self.bedrock_client = boto3.client('bedrock-runtime')
        
    def analyze_supplier_sustainability(self, suppliers: List[Dict]) -> Dict[str, Any]:
        """Analyze supplier sustainability profiles"""
        results = []
        
        for supplier in suppliers:
            score = self._calculate_sustainability_score(supplier)
            recommendations = self._generate_recommendations(supplier, score)
            
            results.append({
                'supplier_id': supplier.get('id'),
                'name': supplier.get('name'),
                'sustainability_score': score,
                'carbon_footprint': supplier.get('carbon_footprint', 0),
                'certifications': supplier.get('certifications', []),
                'recommendations': recommendations,
                'risk_level': self._assess_risk_level(score)
            })
        
        return {
            'agent': 'sourcing',
            'analysis': results,
            'top_suppliers': sorted(results, key=lambda x: x['sustainability_score'], reverse=True)[:5]
        }
    
    def _calculate_sustainability_score(self, supplier: Dict) -> float:
        """Calculate sustainability score (0-100)"""
        base_score = 50
        carbon_impact = max(0, 30 - (supplier.get('carbon_footprint', 50) / 10))
        cert_bonus = len(supplier.get('certifications', [])) * 5
        renewable_bonus = supplier.get('renewable_energy_percent', 0) * 0.2
        
        return min(100, base_score + carbon_impact + cert_bonus + renewable_bonus)
    
    def _assess_risk_level(self, score: float) -> str:
        if score >= 80: return 'Low'
        elif score >= 60: return 'Medium'
        else: return 'High'
    
    def _generate_recommendations(self, supplier: Dict, score: float) -> List[str]:
        recommendations = []
        
        if score < 70:
            recommendations.append("Implement supplier sustainability training program")
        if supplier.get('carbon_footprint', 0) > 40:
            recommendations.append("Request carbon reduction plan from supplier")
        if not supplier.get('certifications'):
            recommendations.append("Encourage ISO 14001 or similar certification")
        
        return recommendations