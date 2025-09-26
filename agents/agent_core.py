import json
import sys
import os
from typing import Dict, Any, List
from .sourcing_agent import SourcingAgent
from .logistics_agent import LogisticsAgent
from .inventory_agent import InventoryAgent
from .carbon_accounting_agent import CarbonAccountingAgent

# Import enhanced orchestrator
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from orchestration import AgentOrchestrator

class AgentCore:
    def __init__(self):
        self.sourcing_agent = SourcingAgent()
        self.logistics_agent = LogisticsAgent()
        self.inventory_agent = InventoryAgent()
        self.carbon_agent = CarbonAccountingAgent()
        self.orchestrator = AgentOrchestrator()
        
    def orchestrate_sustainability_analysis(self, supply_chain_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced orchestration with proper flow control and context passing"""
        
        # Use enhanced orchestrator for Phase 2 Step 2 requirements
        orchestration_result = self.orchestrator.orchestrate_agents(supply_chain_data)
        
        # Extract final results and add legacy summary for compatibility
        final_results = orchestration_result.get('final_results', {})
        final_results['summary'] = self._generate_executive_summary(final_results)
        
        # Add orchestration metadata
        final_results['orchestration_metadata'] = {
            'orchestration_id': orchestration_result.get('orchestration_id'),
            'execution_time': orchestration_result.get('total_execution_time', 0),
            'agent_execution_summary': orchestration_result.get('execution_summary', {}),
            'context_flow': orchestration_result.get('context_flow', [])
        }
        
        return final_results
    
    def _generate_executive_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary of all analyses"""
        
        summary = {
            'total_suppliers_analyzed': 0,
            'total_routes_optimized': 0,
            'total_inventory_items': 0,
            'overall_sustainability_score': 0,
            'total_carbon_footprint': 0,
            'top_recommendations': [],
            'key_metrics': {}
        }
        
        # Aggregate metrics
        if 'sourcing' in results:
            summary['total_suppliers_analyzed'] = len(results['sourcing'].get('analysis', []))
            
        if 'logistics' in results:
            summary['total_routes_optimized'] = len(results['logistics'].get('optimized_routes', []))
            
        if 'inventory' in results:
            summary['total_inventory_items'] = len(results['inventory'].get('waste_analysis', []))
            
        if 'carbon_accounting' in results:
            carbon_data = results['carbon_accounting']
            summary['overall_sustainability_score'] = carbon_data.get('sustainability_score', 0)
            summary['total_carbon_footprint'] = carbon_data.get('total_carbon_footprint_tons', 0)
        
        # Collect top recommendations from all agents
        recommendations = []
        
        if 'sourcing' in results and 'top_suppliers' in results['sourcing']:
            for supplier in results['sourcing']['top_suppliers'][:2]:
                recommendations.extend(supplier.get('recommendations', []))
        
        if 'logistics' in results and 'best_routes' in results['logistics']:
            for route in results['logistics']['best_routes'][:2]:
                recommendations.extend(route.get('recommendations', []))
        
        if 'inventory' in results and 'priority_actions' in results['inventory']:
            recommendations.extend(results['inventory']['priority_actions'][:3])
        
        summary['top_recommendations'] = recommendations[:5]
        
        # Key performance metrics
        summary['key_metrics'] = {
            'sustainability_grade': self._calculate_grade(summary['overall_sustainability_score']),
            'carbon_intensity': summary['total_carbon_footprint'] / max(summary['total_suppliers_analyzed'], 1),
            'improvement_potential': self._calculate_improvement_potential(results)
        }
        
        return summary
    
    def _calculate_grade(self, score: float) -> str:
        """Convert sustainability score to letter grade"""
        if score >= 90: return 'A+'
        elif score >= 80: return 'A'
        elif score >= 70: return 'B'
        elif score >= 60: return 'C'
        else: return 'D'
    
    def _calculate_improvement_potential(self, results: Dict[str, Any]) -> float:
        """Calculate overall improvement potential percentage"""
        potential_improvements = []
        
        if 'logistics' in results:
            potential_improvements.append(results['logistics'].get('total_emission_reduction', 0))
        
        if 'inventory' in results:
            potential_improvements.append(results['inventory'].get('total_waste_reduction_potential', 0))
        
        return sum(potential_improvements) / len(potential_improvements) if potential_improvements else 0