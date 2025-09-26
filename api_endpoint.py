from flask import Flask, request, jsonify
from agents import AgentCore
from bedrock_auth import BedrockAuthenticator
import json
import os

app = Flask(__name__)
agent_core = AgentCore()
auth = BedrockAuthenticator(api_key="strands_api_key_ai_hackathon")

@app.route('/api/sustainability/analyze', methods=['POST'])
def analyze_sustainability():
    """API endpoint for sustainability analysis with authentication"""
    try:
        data = request.get_json()
        
        # Check API key authentication
        api_key = request.headers.get('X-API-Key') or data.get('api_key')
        if not auth.authenticate_request({'api_key': api_key}):
            return jsonify({
                'error': 'Invalid or missing API key',
                'status': 'unauthorized'
            }), 401
        
        # Validate required data
        if not data or 'supply_chain_data' not in data:
            return jsonify({'error': 'supply_chain_data required'}), 400
        
        # Run analysis
        results = agent_core.orchestrate_sustainability_analysis(data['supply_chain_data'])
        
        return jsonify({
            'status': 'success',
            'results': results,
            'authenticated': True
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/sustainability/test', methods=['GET'])
def test_endpoint():
    """Test endpoint with sample data"""
    sample_data = {
        'suppliers': [
            {
                'id': 'SUP001',
                'name': 'EcoSupplier Inc',
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
                'distance_km': 250,
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
    
    results = agent_core.orchestrate_sustainability_analysis(sample_data)
    
    return jsonify({
        'status': 'success',
        'test_results': results
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)