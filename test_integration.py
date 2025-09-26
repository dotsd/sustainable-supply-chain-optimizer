#!/usr/bin/env python3
"""
Complete integration test for Phase 1 + Phase 2
Tests data generation, conversion, and analysis pipeline
"""

import asyncio
import json
from integration_adapter import IntegrationAdapter

async def test_complete_integration():
    """Test complete Phase 1 + Phase 2 integration"""
    
    print("🔄 Testing Complete Phase 1 + Phase 2 Integration")
    print("=" * 60)
    
    adapter = IntegrationAdapter()
    
    # Test 1: Validate Phase 1 components
    print("\n📋 Test 1: Phase 1 Validation")
    print("-" * 40)
    
    validation = adapter.validate_phase1_integration()
    
    print(f"✅ Data Generator Available: {validation['data_generator_available']}")
    print(f"✅ MCP Server Structure: {validation['mcp_server_structure']}")
    print(f"✅ Base Agent Pattern: {validation['base_agent_pattern']}")
    
    if validation['issues_found']:
        print(f"\n⚠️ Issues Found:")
        for issue in validation['issues_found']:
            print(f"   - {issue}")
    
    if validation['recommendations']:
        print(f"\n💡 Recommendations:")
        for rec in validation['recommendations']:
            print(f"   - {rec}")
    
    # Test 2: Data Generation and Conversion
    print(f"\n📊 Test 2: Data Generation & Format Conversion")
    print("-" * 40)
    
    try:
        # Generate smaller dataset for testing
        results = await adapter.generate_and_analyze(suppliers=3, routes=5, products=4)
        
        generated = results['generated_data']
        converted = results['converted_data']
        
        print(f"✅ Generated Data:")
        print(f"   - Suppliers: {len(generated['suppliers'])}")
        print(f"   - Routes: {len(generated['routes'])}")
        print(f"   - Products: {len(generated['products'])}")
        
        print(f"\n✅ Converted Data:")
        print(f"   - Suppliers: {len(converted['suppliers'])}")
        print(f"   - Routes: {len(converted['routes'])}")
        print(f"   - Inventory: {len(converted['inventory'])}")
        
        # Show sample conversion
        if generated['suppliers'] and converted['suppliers']:
            orig_supplier = generated['suppliers'][0]
            conv_supplier = converted['suppliers'][0]
            
            print(f"\n🔄 Sample Data Conversion:")
            print(f"   Original: {orig_supplier['name']} (Score: {orig_supplier['sustainability_score']})")
            print(f"   Converted: {conv_supplier['name']} (Carbon: {conv_supplier['carbon_footprint']})")
        
    except Exception as e:
        print(f"❌ Data generation/conversion failed: {str(e)}")
        return
    
    # Test 3: Complete Analysis Pipeline
    print(f"\n🧠 Test 3: Complete Analysis Pipeline")
    print("-" * 40)
    
    analysis = results['analysis_results']
    
    if 'error' in analysis:
        print(f"❌ Analysis failed: {analysis['error']}")
        return
    
    summary = analysis.get('summary', {})
    
    print(f"✅ Analysis Results:")
    print(f"   - Sustainability Score: {summary.get('overall_sustainability_score', 0):.1f}/100")
    print(f"   - Grade: {summary.get('key_metrics', {}).get('sustainability_grade', 'N/A')}")
    print(f"   - Carbon Footprint: {summary.get('total_carbon_footprint', 0):.1f} tons")
    
    # Test 4: Integration Quality Assessment
    print(f"\n📈 Test 4: Integration Quality Assessment")
    print("-" * 40)
    
    metadata = results['integration_metadata']
    
    print(f"✅ Integration Quality:")
    print(f"   - Data Quality Score: {metadata['data_quality_score']:.1f}/100")
    print(f"   - Conversion Success: {metadata['conversion_success']}")
    print(f"   - Analysis Success: {metadata['analysis_success']}")
    
    # Show top recommendations from integrated analysis
    recommendations = summary.get('top_recommendations', [])
    if recommendations:
        print(f"\n🎯 Top Integrated Recommendations:")
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"   {i}. {rec}")
    
    # Test 5: Orchestration Metadata
    orch_metadata = analysis.get('orchestration_metadata', {})
    if orch_metadata:
        print(f"\n🔧 Orchestration Performance:")
        print(f"   - Execution Time: {orch_metadata.get('execution_time', 0):.2f}s")
        print(f"   - Context Flow Steps: {len(orch_metadata.get('context_flow', []))}")
    
    print(f"\n🎉 Integration Test Complete!")
    
    # Final assessment
    if (metadata['conversion_success'] and 
        metadata['analysis_success'] and 
        metadata['data_quality_score'] > 70):
        print("✅ PHASE 1 + PHASE 2 INTEGRATION: SUCCESS")
    else:
        print("⚠️ PHASE 1 + PHASE 2 INTEGRATION: NEEDS ATTENTION")
    
    return results

async def test_mcp_compatibility():
    """Test MCP server compatibility"""
    
    print(f"\n🔌 Testing MCP Server Compatibility")
    print("-" * 40)
    
    try:
        # Test if MCP components are importable
        from mcp.server import Server
        from mcp.types import Tool
        print("✅ MCP dependencies available")
        
        # Test data generator with MCP pattern
        from agents.data_generator import DataGeneratorAgent
        agent = DataGeneratorAgent()
        
        # Test async execution
        result = await agent.execute({'suppliers': 1, 'routes': 1, 'products': 1})
        
        if result and 'suppliers' in result:
            print("✅ MCP agent pattern working")
        else:
            print("❌ MCP agent pattern failed")
            
    except ImportError as e:
        print(f"⚠️ MCP dependencies missing: {e}")
        print("   Run: pip install mcp")
    except Exception as e:
        print(f"❌ MCP compatibility issue: {e}")

if __name__ == "__main__":
    async def main():
        await test_complete_integration()
        await test_mcp_compatibility()
    
    asyncio.run(main())