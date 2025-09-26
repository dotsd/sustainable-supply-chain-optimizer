import boto3
import os
from botocore.config import Config

# AWS Configuration for Supply Chain Optimizer
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
AWS_PROFILE = os.getenv('AWS_PROFILE', 'default')

# Bedrock configuration for AI agents
BEDROCK_CONFIG = Config(
    region_name=AWS_REGION,
    retries={'max_attempts': 3, 'mode': 'adaptive'}
)

# Model configurations
MODELS = {
    'claude': 'anthropic.claude-3-sonnet-20240229-v1:0',
    'titan': 'amazon.titan-text-express-v1',
    'llama': 'meta.llama2-70b-chat-v1'
}

def get_bedrock_client():
    """Initialize Bedrock client with proper configuration"""
    return boto3.client('bedrock-runtime', config=BEDROCK_CONFIG)

def get_s3_client():
    """Initialize S3 client for data storage"""
    return boto3.client('s3', config=BEDROCK_CONFIG)

# MCP Server configuration
MCP_CONFIG = {
    'name': 'supply-chain-optimizer',
    'version': '1.0.0',
    'description': 'Sustainable Supply Chain Optimizer with AI Agents'
}