from flask import Flask, render_template, jsonify, request
import asyncio
import json
from agents.data_generator import DataGeneratorAgent
from agents.agent_core import AgentCore

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/generate-demo-data')
def generate_demo_data():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    data_generator = DataGeneratorAgent()
    result = loop.run_until_complete(data_generator.execute({
        'suppliers': 10, 'routes': 15, 'products': 8
    }))
    
    return jsonify(result)

@app.route('/api/analyze', methods=['POST'])
def analyze_sustainability():
    data = request.json
    
    agent_core = AgentCore()
    result = agent_core.orchestrate_sustainability_analysis(data)
    
    return jsonify(result)

@app.route('/api/quick-demo')
def quick_demo():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Generate demo data
    data_generator = DataGeneratorAgent()
    supply_data = loop.run_until_complete(data_generator.execute({
        'suppliers': 8, 'routes': 12, 'products': 6
    }))
    
    # Run analysis
    agent_core = AgentCore()
    analysis = agent_core.orchestrate_sustainability_analysis(supply_data)
    
    return jsonify({
        'supply_data': supply_data,
        'analysis': analysis
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)