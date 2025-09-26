"""
Bedrock Agent endpoint with API key authentication
"""

from flask import Flask, request, jsonify
from bedrock_auth import BedrockAuthenticator
import json

app = Flask(__name__)
auth = BedrockAuthenticator(api_key="strands_api_key_ai_hackathon")

@app.route('/bedrock/agent/invoke', methods=['POST'])
def invoke_bedrock_agent():
    """Invoke Bedrock agent with authentication"""
    try:
        data = request.get_json()
        
        # Extract parameters
        agent_id = data.get('agent_id')
        input_text = data.get('input_text')
        api_key = request.headers.get('X-API-Key') or data.get('api_key')
        
        # Validate required parameters
        if not all([agent_id, input_text, api_key]):
            return jsonify({
                'error': 'Missing required parameters: agent_id, input_text, api_key',
                'status': 'bad_request'
            }), 400
        
        # Generate session ID
        session_id = auth.generate_session_id()
        
        # Invoke agent with authentication
        result = auth.invoke_agent_with_auth(
            agent_id=agent_id,
            session_id=session_id,
            input_text=input_text,
            api_key=api_key
        )
        
        return jsonify(result), result.get('code', 200)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/bedrock/agent/chat', methods=['POST'])
def chat_with_agent():
    """Chat interface for Bedrock agent"""
    try:
        data = request.get_json()
        
        # Extract parameters
        message = data.get('message')
        api_key = request.headers.get('X-API-Key') or data.get('api_key')
        agent_id = data.get('agent_id', 'sustainability-supply-chain-optimizer')
        
        if not message or not api_key:
            return jsonify({
                'error': 'Missing message or api_key',
                'status': 'bad_request'
            }), 400
        
        # Generate session ID
        session_id = auth.generate_session_id()
        
        # Invoke agent
        result = auth.invoke_agent_with_auth(
            agent_id=agent_id,
            session_id=session_id,
            input_text=message,
            api_key=api_key
        )
        
        if result.get('status') == 'success':
            return jsonify({
                'response': result.get('result'),
                'session_id': result.get('session_id'),
                'authenticated': True
            })
        else:
            return jsonify(result), result.get('code', 500)
            
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/bedrock/auth/validate', methods=['POST'])
def validate_api_key():
    """Validate API key"""
    try:
        data = request.get_json()
        api_key = request.headers.get('X-API-Key') or data.get('api_key')
        
        is_valid = auth.authenticate_request({'api_key': api_key})
        
        return jsonify({
            'valid': is_valid,
            'message': 'API key is valid' if is_valid else 'Invalid API key'
        }), 200 if is_valid else 401
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)