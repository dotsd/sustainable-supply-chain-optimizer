"""
Bedrock Agent authentication using API key
"""

import boto3
import json
import hashlib
import time
from typing import Dict, Any, Optional

class BedrockAuthenticator:
    def __init__(self, api_key: str = "strands_api_key_ai_hackathon"):
        self.api_key = api_key
        self.bedrock_agent = boto3.client('bedrock-agent-runtime')
        
    def authenticate_request(self, request_data: Dict[str, Any]) -> bool:
        """Authenticate request using API key"""
        provided_key = request_data.get('api_key') or request_data.get('headers', {}).get('x-api-key')
        return provided_key == self.api_key
    
    def invoke_agent_with_auth(self, agent_id: str, session_id: str, input_text: str, api_key: str) -> Dict[str, Any]:
        """Invoke Bedrock agent with authentication"""
        
        # Validate API key
        if api_key != self.api_key:
            return {
                'error': 'Invalid API key',
                'status': 'unauthorized',
                'code': 401
            }
        
        try:
            # Invoke Bedrock agent
            response = self.bedrock_agent.invoke_agent(
                agentId=agent_id,
                agentAliasId='TSTALIASID',  # Test alias
                sessionId=session_id,
                inputText=input_text
            )
            
            # Process response
            result = ""
            for event in response.get('completion', []):
                if 'chunk' in event:
                    chunk = event['chunk']
                    if 'bytes' in chunk:
                        result += chunk['bytes'].decode('utf-8')
            
            return {
                'status': 'success',
                'result': result,
                'session_id': session_id,
                'authenticated': True
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'status': 'error',
                'code': 500
            }
    
    def generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = str(int(time.time()))
        hash_input = f"{self.api_key}_{timestamp}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:16]