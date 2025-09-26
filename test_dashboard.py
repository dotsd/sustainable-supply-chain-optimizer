#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(__file__))

from dashboard.app import app
import json

def test_dashboard_api():
    print("=== TESTING DASHBOARD API ===")
    
    with app.test_client() as client:
        # Test quick demo endpoint
        print("\n1. Testing quick demo endpoint...")
        response = client.get('/api/quick-demo')
        
        if response.status_code == 200:
            data = response.get_json()
            print("   SUCCESS: Quick demo API working")
            print(f"   - Generated {len(data['supply_data']['suppliers'])} suppliers")
            print(f"   - Analysis score: {data['analysis']['summary']['overall_sustainability_score']:.1f}")
            print(f"   - Grade: {data['analysis']['summary']['key_metrics']['sustainability_grade']}")
        else:
            print(f"   ERROR: API returned status {response.status_code}")
    
    print("\n=== DASHBOARD API TEST COMPLETE ===")
    print("Ready for web demo at: http://localhost:5000")

if __name__ == "__main__":
    test_dashboard_api()