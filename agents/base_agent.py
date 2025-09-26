from abc import ABC, abstractmethod
from typing import Dict, Any
import boto3
import json

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        self.context = {}
    
    async def execute(self, parameters: Dict[str, Any], shared_context: Dict[str, Any] = None) -> Dict[str, Any]:
        if shared_context:
            self.context.update(shared_context)
        return await self.process(parameters)
    
    @abstractmethod
    async def process(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    async def invoke_bedrock(self, prompt: str, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0") -> str:
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}]
        })
        
        response = self.bedrock.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )
        
        response_body = json.loads(response.get('body').read())
        return response_body['content'][0]['text']