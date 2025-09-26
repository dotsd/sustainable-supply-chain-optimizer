#!/usr/bin/env python3
import asyncio
import json
from agents.data_generator import DataGeneratorAgent

async def test_data_generation():
    print("Testing Data Generator Agent...\n")
    
    agent = DataGeneratorAgent()
    result = await agent.execute({
        'suppliers': 20,
        'routes': 30,
        'products': 15
    })
    
    print("Generated Data Summary:")
    print(f"- Suppliers: {len(result['suppliers'])}")
    print(f"- Routes: {len(result['routes'])}")
    print(f"- Products: {len(result['products'])}")
    
    print("\nSample Supplier:")
    print(json.dumps(result['suppliers'][0], indent=2))
    
    print("\nSample Route:")
    print(json.dumps(result['routes'][0], indent=2))
    
    print("\nSample Product:")
    print(json.dumps(result['products'][0], indent=2))
    
    # Data quality validation
    avg_sustainability = sum(s['sustainability_score'] for s in result['suppliers']) / len(result['suppliers'])
    print(f"\nData Quality Check:")
    print(f"- Average Sustainability Score: {avg_sustainability:.1f}")
    print(f"- All suppliers have certifications: {all(len(s['certifications']) > 0 for s in result['suppliers'])}")
    print(f"- All routes have valid emissions: {all(r['emissions_per_mile'] > 0 for r in result['routes'])}")

if __name__ == "__main__":
    asyncio.run(test_data_generation())