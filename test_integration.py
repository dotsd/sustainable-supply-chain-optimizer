#!/usr/bin/env python3
import asyncio
import json
from agents.data_generator import DataGeneratorAgent
from agents.agent_core import AgentCore

async def test_phase1_phase2_integration():
    print("Testing Phase 1 + Phase 2 Integration...\n")
    
    # Step 1: Generate data with Phase 1 agent
    print("Step 1: Generating supply chain data...")
    data_generator = DataGeneratorAgent()
    supply_chain_data = await data_generator.execute({
        'suppliers': 5,
        'routes': 8,
        'products': 6
    })
    
    print(f"Generated: {len(supply_chain_data['suppliers'])} suppliers, {len(supply_chain_data['routes'])} routes, {len(supply_chain_data['products'])} inventory items")
    
    # Step 2: Run full orchestration with Phase 2 agents
    print("\nStep 2: Running orchestrated sustainability analysis...")
    agent_core = AgentCore()
    analysis_result = agent_core.orchestrate_sustainability_analysis(supply_chain_data)
    
    # Step 3: Display results
    print("\n=== INTEGRATION TEST RESULTS ===")
    print(f"Overall Sustainability Score: {analysis_result.get('summary', {}).get('overall_sustainability_score', 0):.1f}")
    print(f"Total Carbon Footprint: {analysis_result.get('summary', {}).get('total_carbon_footprint', 0):.1f} tons")
    print(f"Sustainability Grade: {analysis_result.get('summary', {}).get('key_metrics', {}).get('sustainability_grade', 'N/A')}")
    
    print(f"\nTop Recommendations:")
    for i, rec in enumerate(analysis_result.get('summary', {}).get('top_recommendations', [])[:3], 1):
        print(f"{i}. {rec}")
    
    print(f"\nOrchestration Metadata:")
    metadata = analysis_result.get('orchestration_metadata', {})
    print(f"- Execution Time: {metadata.get('execution_time', 0):.2f}s")
    print(f"- Successful Agents: {metadata.get('agent_execution_summary', {}).get('successful_agents', 0)}")
    
    print("\n✅ Phase 1 + Phase 2 Integration Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_phase1_phase2_integration())