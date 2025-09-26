import requests
import json

def test_api_endpoint():
    """Test the sustainability API endpoint"""
    
    base_url = "http://localhost:5000"
    
    # Test data
    test_data = {
        "supply_chain_data": {
            "suppliers": [
                {
                    "id": "SUP001",
                    "name": "GreenTech Materials",
                    "carbon_footprint": 35,
                    "certifications": ["ISO14001", "FSC"],
                    "renewable_energy_percent": 75
                },
                {
                    "id": "SUP002", 
                    "name": "EcoSupplier Corp",
                    "carbon_footprint": 50,
                    "certifications": ["ISO14001"],
                    "renewable_energy_percent": 40
                }
            ],
            "routes": [
                {
                    "id": "RT001",
                    "origin": "Supplier A",
                    "destination": "Factory B",
                    "distance_km": 150,
                    "transport_mode": "truck"
                },
                {
                    "id": "RT002",
                    "origin": "Factory B", 
                    "destination": "Distribution Center",
                    "distance_km": 600,
                    "transport_mode": "truck"
                }
            ],
            "inventory": [
                {
                    "id": "PRD001",
                    "name": "Eco Widget Pro",
                    "current_stock": 800,
                    "monthly_demand": 120,
                    "shelf_life_days": 90
                },
                {
                    "id": "PRD002",
                    "name": "Sustainable Component X",
                    "current_stock": 300,
                    "monthly_demand": 80,
                    "shelf_life_days": 365
                }
            ]
        }
    }
    
    print("🧪 Testing Sustainability API...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health Check: {response.json()}")
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
        return
    
    # Test sample endpoint
    try:
        response = requests.get(f"{base_url}/api/sustainability/test")
        print("✅ Test Endpoint: Success")
        print(f"Sample Analysis Score: {response.json()['test_results']['summary']['overall_sustainability_score']:.1f}")
    except Exception as e:
        print(f"❌ Test Endpoint Failed: {e}")
    
    # Test main analysis endpoint
    try:
        response = requests.post(
            f"{base_url}/api/sustainability/analyze",
            json=test_data,
            headers={
                'Content-Type': 'application/json',
                'X-API-Key': 'strands_api_key_ai_hackathon'
            }
        )
        
        if response.status_code == 200:
            results = response.json()['results']
            print("✅ Main Analysis: Success")
            print(f"📊 Results Summary:")
            print(f"   - Suppliers Analyzed: {results['summary']['total_suppliers_analyzed']}")
            print(f"   - Routes Optimized: {results['summary']['total_routes_optimized']}")
            print(f"   - Sustainability Score: {results['summary']['overall_sustainability_score']:.1f}/100")
            print(f"   - Carbon Footprint: {results['summary']['total_carbon_footprint']:.1f} tons")
            print(f"   - Grade: {results['summary']['key_metrics']['sustainability_grade']}")
            
            print(f"\n🎯 Top Recommendations:")
            for i, rec in enumerate(results['summary']['top_recommendations'][:3], 1):
                print(f"   {i}. {rec}")
                
        else:
            print(f"❌ Analysis Failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Analysis Endpoint Failed: {e}")

if __name__ == "__main__":
    test_api_endpoint()