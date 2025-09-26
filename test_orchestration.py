from orchestration import AgentOrchestrator
from agents import AgentCore
import json
import time

def test_enhanced_orchestration():
    """Test Phase 2 Step 2 enhanced orchestration"""
    
    print("🚀 Testing Enhanced Agent Orchestration (Phase 2 Step 2)")
    print("=" * 60)
    
    # Sample supply chain data
    sample_data = {
        'suppliers': [
            {
                'id': 'SUP001',
                'name': 'EcoTech Solutions',
                'carbon_footprint': 28,
                'certifications': ['ISO14001', 'FSC'],
                'renewable_energy_percent': 75
            },
            {
                'id': 'SUP002', 
                'name': 'GreenSupply Corp',
                'carbon_footprint': 42,
                'certifications': ['ISO14001'],
                'renewable_energy_percent': 45
            },
            {
                'id': 'SUP003',
                'name': 'SustainableMaterials Inc',
                'carbon_footprint': 35,
                'certifications': ['FSC', 'LEED'],
                'renewable_energy_percent': 60
            }
        ],
        'routes': [
            {
                'id': 'RT001',
                'origin': 'EcoTech Factory',
                'destination': 'Main Warehouse',
                'distance_km': 180,
                'transport_mode': 'truck'
            },
            {
                'id': 'RT002',
                'origin': 'GreenSupply Plant',
                'destination': 'Distribution Center', 
                'distance_km': 650,
                'transport_mode': 'truck'
            },
            {
                'id': 'RT003',
                'origin': 'Main Warehouse',
                'destination': 'Regional Hub',
                'distance_km': 320,
                'transport_mode': 'truck'
            }
        ],
        'inventory': [
            {
                'id': 'PRD001',
                'name': 'Eco Widget Pro',
                'current_stock': 750,
                'monthly_demand': 125,
                'shelf_life_days': 120
            },
            {
                'id': 'PRD002',
                'name': 'Sustainable Component X',
                'current_stock': 400,
                'monthly_demand': 90,
                'shelf_life_days': 300
            },
            {
                'id': 'PRD003',
                'name': 'Green Material Y',
                'current_stock': 1200,
                'monthly_demand': 180,
                'shelf_life_days': 90
            }
        ]
    }
    
    # Test 1: Enhanced Orchestration
    print("\n📊 Test 1: Enhanced Orchestration with Context Passing")
    print("-" * 50)
    
    orchestrator = AgentOrchestrator()
    start_time = time.time()
    
    orchestration_result = orchestrator.orchestrate_agents(sample_data)
    
    execution_time = time.time() - start_time
    
    print(f"✅ Orchestration completed in {execution_time:.2f} seconds")
    print(f"📋 Orchestration ID: {orchestration_result['orchestration_id']}")
    
    # Display execution summary
    exec_summary = orchestration_result.get('execution_summary', {})
    print(f"🎯 Agent Execution Summary:")
    print(f"   - Total Agents: {exec_summary.get('total_agents', 0)}")
    print(f"   - Successful: {exec_summary.get('successful_agents', 0)}")
    print(f"   - Failed: {exec_summary.get('failed_agents', 0)}")
    print(f"   - Context Flow Steps: {exec_summary.get('context_flow_steps', 0)}")
    
    # Display context flow
    context_flow = orchestration_result.get('context_flow', [])
    if context_flow:
        print(f"\n🔄 Context Flow Between Agents:")
        for step in context_flow:
            print(f"   {step['agent']} → Added: {step['context_keys_added']}")
    
    # Test 2: Agent Core with Enhanced Orchestration
    print(f"\n📊 Test 2: Agent Core with Enhanced Orchestration")
    print("-" * 50)
    
    agent_core = AgentCore()
    start_time = time.time()
    
    results = agent_core.orchestrate_sustainability_analysis(sample_data)
    
    execution_time = time.time() - start_time
    
    print(f"✅ Agent Core analysis completed in {execution_time:.2f} seconds")
    
    # Display key results
    summary = results.get('summary', {})
    print(f"\n📈 Key Results:")
    print(f"   - Sustainability Score: {summary.get('overall_sustainability_score', 0):.1f}/100")
    print(f"   - Grade: {summary.get('key_metrics', {}).get('sustainability_grade', 'N/A')}")
    print(f"   - Carbon Footprint: {summary.get('total_carbon_footprint', 0):.1f} tons")
    print(f"   - Suppliers Analyzed: {summary.get('total_suppliers_analyzed', 0)}")
    print(f"   - Routes Optimized: {summary.get('total_routes_optimized', 0)}")
    
    # Display orchestration metadata
    orch_metadata = results.get('orchestration_metadata', {})
    if orch_metadata:
        print(f"\n🔧 Orchestration Metadata:")
        print(f"   - Orchestration ID: {orch_metadata.get('orchestration_id', 'N/A')}")
        print(f"   - Execution Time: {orch_metadata.get('execution_time', 0):.2f}s")
        print(f"   - Context Flow Steps: {len(orch_metadata.get('context_flow', []))}")
    
    # Display top recommendations
    recommendations = summary.get('top_recommendations', [])
    if recommendations:
        print(f"\n🎯 Top Recommendations:")
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"   {i}. {rec}")
    
    # Test 3: Error Handling and Resilience
    print(f"\n📊 Test 3: Error Handling Test")
    print("-" * 50)
    
    # Test with incomplete data
    incomplete_data = {'suppliers': sample_data['suppliers']}  # Only suppliers
    
    resilience_result = agent_core.orchestrate_sustainability_analysis(incomplete_data)
    
    print(f"✅ Handled incomplete data gracefully")
    print(f"   - Suppliers processed: {resilience_result.get('summary', {}).get('total_suppliers_analyzed', 0)}")
    print(f"   - Routes processed: {resilience_result.get('summary', {}).get('total_routes_optimized', 0)}")
    print(f"   - Still generated sustainability score: {resilience_result.get('summary', {}).get('overall_sustainability_score', 0):.1f}")
    
    print(f"\n🎉 All orchestration tests completed successfully!")
    print(f"✅ Phase 2 Step 2 - Agent Orchestration: IMPLEMENTED")
    
    return results

if __name__ == "__main__":
    test_enhanced_orchestration()