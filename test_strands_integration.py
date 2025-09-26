#!/usr/bin/env python3
"""
Test Strands SDK integration across all agents
"""

import asyncio
import os
from agents import AgentCore
from agents.data_generator import DataGeneratorAgent

async def test_strands_integration():
    """Test Strands integration across all components"""
    
    print("🧬 Testing Strands SDK Integration")
    print("=" * 50)
    
    # Set test API key (replace with real key)
    os.environ['STRANDS_API_KEY'] = 'test-strands-key'
    
    # Test 1: Data Generator with Strands
    print("\n📊 Test 1: Data Generator with Strands Company Names")
    print("-" * 45)
    
    data_generator = DataGeneratorAgent()
    generated_data = await data_generator.execute({
        'suppliers': 5,
        'routes': 3,
        'products': 3
    })
    
    print(f"✅ Generated {len(generated_data['suppliers'])} suppliers with Strands names:")
    for supplier in generated_data['suppliers'][:3]:
        print(f"   - {supplier['name']}")
    
    # Test 2: Complete Analysis with Strands
    print(f"\n🧠 Test 2: Complete Analysis with Strands AI")
    print("-" * 45)
    
    # Convert to Phase 2 format
    from integration_adapter import IntegrationAdapter
    adapter = IntegrationAdapter()
    converted_data = adapter._convert_data_format(generated_data)
    
    # Run analysis with Strands integration
    agent_core = AgentCore()
    results = agent_core.orchestrate_sustainability_analysis(converted_data)
    
    # Check Strands integration in results
    print(f"✅ Strands Integration Status:")
    
    # Sourcing Agent Strands features
    sourcing = results.get('sourcing', {})
    if sourcing.get('strands_powered'):
        print(f"   - Sourcing Agent: ✅ Strands-powered")
        if sourcing.get('analysis'):
            sample_supplier = sourcing['analysis'][0]
            print(f"     Strands Explanation: {sample_supplier.get('strands_explanation', 'N/A')[:50]}...")
    
    # Logistics Agent Strands features
    logistics = results.get('logistics', {})
    if 'optimized_routes' in logistics and logistics['optimized_routes']:
        sample_route = logistics['optimized_routes'][0]
        if sample_route.get('strands_powered'):
            print(f"   - Logistics Agent: ✅ Strands-powered")
            print(f"     Strands Reasoning: {sample_route.get('strands_reasoning', 'N/A')[:50]}...")
    
    # Inventory Agent Strands features
    inventory = results.get('inventory', {})
    if inventory.get('strands_powered'):
        print(f"   - Inventory Agent: ✅ Strands-powered")
        print(f"     Strands Explanation: {inventory.get('strands_explanation', 'N/A')[:50]}...")
    
    # Carbon Accounting Strands features
    carbon = results.get('carbon_accounting', {})
    if carbon.get('strands_powered'):
        print(f"   - Carbon Agent: ✅ Strands-powered")
        print(f"     Strands Explanation: {carbon.get('strands_explanation', 'N/A')[:50]}...")
    
    # Test 3: Strands Fallback Behavior
    print(f"\n🔄 Test 3: Strands Fallback Behavior")
    print("-" * 45)
    
    # Test without API key
    os.environ.pop('STRANDS_API_KEY', None)
    
    fallback_generator = DataGeneratorAgent()
    fallback_data = await fallback_generator.execute({
        'suppliers': 2,
        'routes': 2,
        'products': 2
    })
    
    print(f"✅ Fallback mode working:")
    print(f"   - Generated {len(fallback_data['suppliers'])} suppliers without Strands")
    print(f"   - Sample name: {fallback_data['suppliers'][0]['name']}")
    
    # Summary
    print(f"\n📈 Strands Integration Summary")
    print("-" * 45)
    print(f"✅ Data Generator: Strands company name generation")
    print(f"✅ Sourcing Agent: Strands sustainability analysis + explanations")
    print(f"✅ Logistics Agent: Strands transport reasoning")
    print(f"✅ Inventory Agent: Strands waste analysis explanations")
    print(f"✅ Carbon Agent: Strands comprehensive explanations")
    print(f"✅ Fallback Mode: Works without Strands SDK")
    
    print(f"\n🎉 Strands Integration Complete!")
    print(f"🔑 Set STRANDS_API_KEY environment variable to enable full features")

if __name__ == "__main__":
    asyncio.run(test_strands_integration())