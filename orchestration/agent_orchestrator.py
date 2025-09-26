import json
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

class AgentStatus(Enum):
    PENDING = "pending"
    RUNNING = "running" 
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class AgentResult:
    agent_name: str
    status: AgentStatus
    data: Dict[str, Any]
    execution_time: float
    error_message: Optional[str] = None

class AgentOrchestrator:
    def __init__(self):
        self.execution_history = []
        self.context_store = {}
        
    def orchestrate_agents(self, supply_chain_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced orchestration with proper flow control and context passing"""
        
        orchestration_result = {
            'orchestration_id': f"orch_{int(time.time())}",
            'start_time': time.time(),
            'agent_results': {},
            'context_flow': [],
            'final_results': {},
            'execution_summary': {}
        }
        
        try:
            # Step 1: Initialize context
            self._initialize_context(supply_chain_data)
            
            # Step 2: Execute agents in sequence with context passing
            agent_sequence = [
                ('sourcing', self._execute_sourcing_agent),
                ('logistics', self._execute_logistics_agent), 
                ('inventory', self._execute_inventory_agent),
                ('carbon_accounting', self._execute_carbon_agent)
            ]
            
            for agent_name, agent_func in agent_sequence:
                result = self._execute_with_retry(agent_name, agent_func)
                orchestration_result['agent_results'][agent_name] = result
                
                if result.status == AgentStatus.COMPLETED:
                    self._update_context(agent_name, result.data)
                    orchestration_result['context_flow'].append({
                        'agent': agent_name,
                        'context_keys_added': list(result.data.keys()),
                        'timestamp': time.time()
                    })
                else:
                    self._handle_agent_failure(agent_name, result)
            
            # Step 3: Generate final aggregated results
            orchestration_result['final_results'] = self._aggregate_results()
            orchestration_result['execution_summary'] = self._generate_execution_summary(orchestration_result)
            
        except Exception as e:
            orchestration_result['orchestration_error'] = str(e)
            
        orchestration_result['end_time'] = time.time()
        orchestration_result['total_execution_time'] = orchestration_result['end_time'] - orchestration_result['start_time']
        
        return orchestration_result
    
    def _initialize_context(self, supply_chain_data: Dict[str, Any]):
        """Initialize shared context for all agents"""
        self.context_store = {
            'original_data': supply_chain_data,
            'suppliers': supply_chain_data.get('suppliers', []),
            'routes': supply_chain_data.get('routes', []),
            'inventory': supply_chain_data.get('inventory', []),
            'metadata': {
                'total_suppliers': len(supply_chain_data.get('suppliers', [])),
                'total_routes': len(supply_chain_data.get('routes', [])),
                'total_inventory_items': len(supply_chain_data.get('inventory', []))
            }
        }
    
    def _execute_with_retry(self, agent_name: str, agent_func, max_retries: int = 2) -> AgentResult:
        """Execute agent with retry logic"""
        
        for attempt in range(max_retries + 1):
            try:
                start_time = time.time()
                result_data = agent_func(self.context_store)
                execution_time = time.time() - start_time
                
                return AgentResult(
                    agent_name=agent_name,
                    status=AgentStatus.COMPLETED,
                    data=result_data,
                    execution_time=execution_time
                )
                
            except Exception as e:
                if attempt == max_retries:
                    return AgentResult(
                        agent_name=agent_name,
                        status=AgentStatus.FAILED,
                        data={},
                        execution_time=time.time() - start_time,
                        error_message=str(e)
                    )
                time.sleep(0.5)
    
    def _execute_sourcing_agent(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute sourcing agent with context"""
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from agents import SourcingAgent
        
        agent = SourcingAgent()
        suppliers = context.get('suppliers', [])
        
        if not suppliers:
            return {'analysis': [], 'top_suppliers': [], 'message': 'No suppliers to analyze'}
        
        result = agent.analyze_supplier_sustainability(suppliers)
        result['context_metadata'] = {
            'suppliers_processed': len(suppliers),
            'avg_sustainability_score': sum(s.get('sustainability_score', 0) for s in result.get('analysis', [])) / max(len(result.get('analysis', [])), 1)
        }
        
        return result
    
    def _execute_logistics_agent(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute logistics agent with context from sourcing"""
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from agents import LogisticsAgent
        
        agent = LogisticsAgent()
        routes = context.get('routes', [])
        
        if not routes:
            return {'optimized_routes': [], 'total_emission_reduction': 0, 'message': 'No routes to optimize'}
        
        result = agent.optimize_routes_for_emissions(routes)
        
        # Enhance with sourcing context
        sourcing_data = context.get('sourcing_results', {})
        if sourcing_data and 'top_suppliers' in sourcing_data:
            result['supplier_route_correlation'] = {
                'high_sustainability_suppliers': len(sourcing_data.get('top_suppliers', [])),
                'recommendation': 'Prioritize routes connecting to top sustainability suppliers'
            }
        
        return result
    
    def _execute_inventory_agent(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute inventory agent with context from previous agents"""
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from agents import InventoryAgent
        
        agent = InventoryAgent()
        inventory = context.get('inventory', [])
        
        if not inventory:
            return {'waste_analysis': [], 'total_waste_reduction_potential': 0, 'message': 'No inventory to analyze'}
        
        result = agent.generate_waste_reduction_recommendations(inventory)
        
        # Enhance with logistics context
        logistics_data = context.get('logistics_results', {})
        if logistics_data:
            result['logistics_inventory_insights'] = {
                'combined_efficiency_score': (logistics_data.get('total_emission_reduction', 0) + result.get('total_waste_reduction_potential', 0)) / 2,
                'recommendation': 'Coordinate route optimization with inventory turnover rates'
            }
        
        return result
    
    def _execute_carbon_agent(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute carbon accounting agent with all previous context"""
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from agents import CarbonAccountingAgent
        
        agent = CarbonAccountingAgent()
        
        supply_chain_data = {
            'sourcing': context.get('sourcing_results', {}),
            'logistics': context.get('logistics_results', {}),
            'inventory': context.get('inventory_results', {})
        }
        
        result = agent.calculate_overall_footprint(supply_chain_data)
        result['orchestration_insights'] = {
            'data_completeness': {
                'suppliers': len(context.get('suppliers', [])) > 0,
                'routes': len(context.get('routes', [])) > 0,
                'inventory': len(context.get('inventory', [])) > 0
            },
            'orchestration_quality_score': self._calculate_orchestration_quality(context)
        }
        
        return result
    
    def _update_context(self, agent_name: str, result_data: Dict[str, Any]):
        """Update shared context with agent results"""
        self.context_store[f'{agent_name}_results'] = result_data
        
        if agent_name == 'sourcing':
            self.context_store['supplier_scores'] = {
                s.get('supplier_id'): s.get('sustainability_score', 0) 
                for s in result_data.get('analysis', [])
            }
        elif agent_name == 'logistics':
            self.context_store['route_emissions'] = {
                r.get('route_id'): r.get('current_emissions', 0)
                for r in result_data.get('optimized_routes', [])
            }
    
    def _calculate_orchestration_quality(self, context: Dict[str, Any]) -> float:
        """Calculate quality of orchestration based on data flow"""
        quality_factors = []
        
        if context.get('suppliers'): quality_factors.append(25)
        if context.get('routes'): quality_factors.append(25)  
        if context.get('inventory'): quality_factors.append(25)
        if context.get('sourcing_results'): quality_factors.append(25)
        
        return sum(quality_factors)
    
    def _handle_agent_failure(self, agent_name: str, result: AgentResult):
        """Handle agent failure gracefully"""
        fallback_data = {
            'sourcing': {'analysis': [], 'top_suppliers': []},
            'logistics': {'optimized_routes': [], 'total_emission_reduction': 0},
            'inventory': {'waste_analysis': [], 'total_waste_reduction_potential': 0},
            'carbon_accounting': {'total_carbon_footprint_tons': 0, 'sustainability_score': 0}
        }
        
        self.context_store[f'{agent_name}_results'] = fallback_data.get(agent_name, {})
    
    def _aggregate_results(self) -> Dict[str, Any]:
        """Aggregate all agent results with orchestration metadata"""
        return {
            'sourcing': self.context_store.get('sourcing_results', {}),
            'logistics': self.context_store.get('logistics_results', {}),
            'inventory': self.context_store.get('inventory_results', {}),
            'carbon_accounting': self.context_store.get('carbon_accounting_results', {}),
            'orchestration_metadata': {
                'successful_agents': len([k for k in self.context_store.keys() if k.endswith('_results')]),
                'data_flow_integrity': len([k for k in self.context_store.keys() if k.endswith('_results')]) >= 3
            }
        }
    
    def _generate_execution_summary(self, orchestration_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate execution summary"""
        agent_results = orchestration_result.get('agent_results', {})
        
        return {
            'total_agents': len(agent_results),
            'successful_agents': len([r for r in agent_results.values() if r.status == AgentStatus.COMPLETED]),
            'failed_agents': len([r for r in agent_results.values() if r.status == AgentStatus.FAILED]),
            'context_flow_steps': len(orchestration_result.get('context_flow', [])),
            'orchestration_success': orchestration_result.get('orchestration_error') is None
        }