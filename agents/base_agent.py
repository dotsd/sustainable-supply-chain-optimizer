from abc import ABC, abstractmethod
from typing import Dict, Any
import json
import os

try:
    import boto3  # type: ignore
    _BOTO3_AVAILABLE = True
except Exception:  # ImportError or other issues
    _BOTO3_AVAILABLE = False

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.bedrock = None
        self.context = {}
        # Lazy / safe bedrock client initialization
        if _BOTO3_AVAILABLE and not bool(int(os.getenv('DISABLE_BEDROCK', '0'))):
            try:
                import boto3  # local scope
                self.bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
            except Exception:
                # Graceful fallback: operate without bedrock
                self.bedrock = None
    
    async def execute(self, parameters: Dict[str, Any], shared_context: Dict[str, Any] = None) -> Dict[str, Any]:
        if shared_context:
            self.context.update(shared_context)
        return await self.process(parameters)
    
    @abstractmethod
    async def process(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    async def invoke_bedrock(self, prompt: str, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0") -> str:
        """Invoke Bedrock model or return a deterministic fallback if unavailable."""
        if not self.bedrock:
            return f"[Fallback LLM] Prompt received: {prompt[:120]}..."

        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 600,
            "messages": [{"role": "user", "content": prompt}]
        })
        try:
            response = self.bedrock.invoke_model(
                body=body,
                modelId=model_id,
                accept="application/json",
                contentType="application/json"
            )
            response_body = json.loads(response.get('body').read())
            return response_body.get('content', [{}])[0].get('text', '').strip() or "[Empty response]"
        except Exception as e:
            return f"[Bedrock error fallback] {e.__class__.__name__}: {e}" 