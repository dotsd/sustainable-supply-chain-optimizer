from agents import AgentCore
import json

def test_sustainability_agents():
    """Test all sustainability agents with sample data"""
    
    # Sample supply chain data
    sample_data = {
        'suppliers': [
            {
                'id': 'SUP001',
                'name': 'EcoSupplier Inc',
                'carbon_footprint': 25,
                'certifications': ['ISO14001', 'FSC'],
                'renewable_energy_percent': 60
            },
            {
                'id': 'SUP002', 
                'name': 'GreenTech Materials',
                'carbon_footprint': 45,
                'certifications': ['ISO14001'],
                'renewable_energy_percent': 30
            }
        ],
        'routes': [
            {
                'id': 'RT001',
                'origin': 'Factory A',
                'destination': 'Warehouse B',
                'distance_km': 250,
                'transport_mode': 'truck'
            },
            {
                'id': 'RT002',
                'origin': 'Supplier C',
                'destination': 'Factory A', 
                'distance_km': 800,
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
            },
            {
                'id': 'PRD002',
                'name': 'Eco Component',
                'current_stock': 1200,
                'monthly_demand': 150,
                'shelf_life_days': 365
            }
        ]
    }
    
    # Initialize agent orchestrator
    agent_core = AgentCore()
    
    # Run complete analysis
    results = agent_core.orchestrate_sustainability_analysis(sample_data)
    
    # Print results
    print("=== SUSTAINABILITY ANALYSIS RESULTS ===")
    print(json.dumps(results, indent=2))
    
    return results

if __name__ == "__main__":
    test_sustainability_agents()