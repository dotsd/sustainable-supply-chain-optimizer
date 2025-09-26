#!/usr/bin/env python3
"""
Test Lambda function directly without Bedrock Agent
"""

import boto3
import json

def test_lambda_function():
    """Test the deployed Lambda function directly"""
    
    print("🧪 Testing Lambda Function Directly")
    print("=" * 40)
    
    lambda_client = boto3.client('lambda')
    
    # Test 1: Simple test
    print("\n📋 Test 1: Simple Function Test")
    print("-" * 30)
    
    try:
        test_event = {
            'test': True,
            'message': 'Testing sustainability agents'
        }
        
        response = lambda_client.invoke(
            FunctionName='sustainability-agents-orchestrator',
            Payload=json.dumps(test_event)
        )
        
        result = json.loads(response['Payload'].read())
        print(f"✅ Simple test result: {result}")
        
    except Exception as e:
        print(f"❌ Simple test failed: {e}")
        return
    
    # Test 2: Sustainability Analysis
    print(f"\n📊 Test 2: Sustainability Analysis")
    print("-" * 30)
    
    try:
        analysis_event = {
            'supply_chain_data': {
                'suppliers': [
                    {
                        'id': 'SUP001',
                        'name': 'EcoTech Solutions',
                        'carbon_footprint': 25,
                        'certifications': ['ISO14001'],
                        'renewable_energy_percent': 60
                    }
                ],
                'routes': [
                    {
                        'id': 'RT001',
                        'origin': 'Factory A',
                        'destination': 'Warehouse B',
                        'distance_km': 200,
                        'transport_mode': 'truck'
                    }
                ],
                'inventory': [
                    {
                        'id': 'PRD001',
                        'name': 'Sustainable Widget',
                        'current_stock': 500,
                        'monthly_demand': 100,
                        'shelf_life_days': 180
                    }
                ]
            }
        }
        
        response = lambda_client.invoke(
            FunctionName='sustainability-agents-orchestrator',
            Payload=json.dumps(analysis_event)
        )
        
        result = json.loads(response['Payload'].read())
        
        if result.get('statusCode') == 200:
            body = json.loads(result['body'])
            analysis_results = body.get('results', {})
            
            print(f"✅ Analysis completed successfully!")
            
            # Show summary
            summary = analysis_results.get('summary', {})
            if summary:
                print(f"   - Sustainability Score: {summary.get('overall_sustainability_score', 0):.1f}/100")
                print(f"   - Grade: {summary.get('key_metrics', {}).get('sustainability_grade', 'N/A')}")
                print(f"   - Carbon Footprint: {summary.get('total_carbon_footprint', 0):.1f} tons")
                
                recommendations = summary.get('top_recommendations', [])
                if recommendations:
                    print(f"   - Top Recommendation: {recommendations[0]}")
            else:
                print(f"   - Raw results available")
        else:
            print(f"❌ Analysis failed: {result}")
            
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
    
    print(f"\n🎉 Lambda Testing Complete!")
    print(f"💡 Lambda function can be used independently of Bedrock Agent")

if __name__ == "__main__":
    test_lambda_function()