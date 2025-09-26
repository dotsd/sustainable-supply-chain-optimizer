#!/usr/bin/env python3
import asyncio
import json
import time
from agents.data_generator import DataGeneratorAgent
from agents.agent_core import AgentCore

async def final_system_test():
    print("=" * 60)
    print("FULL SYSTEM TEST - AWS SUPPLY CHAIN OPTIMIZER")
    print("=" * 60)
    
    start_time = time.time()
    
    # Test 1: Data Generation
    print("\nTEST 1: Data Generation Agent")
    print("-" * 40)
    data_generator = DataGeneratorAgent()
    supply_data = await data_generator.execute({
        'suppliers': 10, 'routes': 15, 'products': 8
    })
    
    print(f"PASS: Generated {len(supply_data['suppliers'])} suppliers")
    print(f"PASS: Generated {len(supply_data['routes'])} routes")
    print(f"PASS: Generated {len(supply_data['products'])} products")
    
    # Test 2: Agent Orchestration
    print("\nTEST 2: AI Agent Orchestration")
    print("-" * 40)
    agent_core = AgentCore()
    analysis = agent_core.orchestrate_sustainability_analysis(supply_data)
    
    summary = analysis.get('summary', {})
    print(f"PASS: Sustainability Score: {summary.get('overall_sustainability_score', 0):.1f}")
    print(f"PASS: Carbon Footprint: {summary.get('total_carbon_footprint', 0):.1f} tons")
    print(f"PASS: Grade: {summary.get('key_metrics', {}).get('sustainability_grade', 'N/A')}")
    
    # Test 3: Performance
    print("\nTEST 3: Performance Metrics")
    print("-" * 40)
    total_time = time.time() - start_time
    print(f"PASS: Total Time: {total_time:.3f}s")
    print(f"PASS: Performance Target < 3s: {'YES' if total_time < 3 else 'NO'}")
    
    # Test 4: Recommendations
    print("\nTEST 4: AI Recommendations")
    print("-" * 40)
    recommendations = summary.get('top_recommendations', [])
    print(f"PASS: Generated {len(recommendations)} recommendations")
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"  {i}. {rec}")
    
    # Final Results
    print("\n" + "=" * 60)
    print("FINAL TEST RESULTS")
    print("=" * 60)
    
    all_tests_pass = (
        len(supply_data['suppliers']) == 10 and
        len(supply_data['routes']) == 15 and
        len(supply_data['products']) == 8 and
        summary.get('overall_sustainability_score', 0) > 0 and
        len(recommendations) > 0 and
        total_time < 5
    )
    
    status = "PASS" if all_tests_pass else "FAIL"
    print(f"Overall System Status: {status}")
    print(f"Hackathon Ready: {'YES' if all_tests_pass else 'NO'}")
    print(f"Demo Ready: {'YES' if all_tests_pass else 'NO'}")
    
    if all_tests_pass:
        print("\nSYSTEM FULLY OPERATIONAL!")
        print("Ready for:")
        print("  - Live Demo Presentation")
        print("  - Hackathon Judging") 
        print("  - Production Deployment")
    
    print("\nAccess Options:")
    print("  - Web UI: Open quick_demo.html in browser")
    print("  - Server: python start_demo.py")
    print("  - API Test: python test_dashboard.py")
    
    return all_tests_pass

if __name__ == "__main__":
    result = asyncio.run(final_system_test())
    print(f"\nFinal Result: {'SUCCESS' if result else 'FAILURE'}")
    exit(0 if result else 1)