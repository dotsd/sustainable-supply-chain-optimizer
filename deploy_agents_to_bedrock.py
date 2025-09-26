import boto3
import json
import zipfile
import os
import time

class BedrockAgentDeployer:
    def __init__(self):
        self.bedrock_agent = boto3.client('bedrock-agent')
        self.lambda_client = boto3.client('lambda')
        self.iam_client = boto3.client('iam')
        
    def deploy_complete_solution(self):
        """Deploy all sustainability agents to Bedrock"""
        
        # Step 1: Create Lambda function for agent orchestration
        lambda_arn = self._create_lambda_function()
        
        # Step 2: Create Bedrock Agent
        agent_id = self._create_bedrock_agent(lambda_arn)
        
        # Step 3: Create action groups for each agent
        self._create_action_groups(agent_id, lambda_arn)
        
        # Step 4: Prepare agent
        self._prepare_agent(agent_id)
        
        print(f"✅ Complete sustainability solution deployed!")
        print(f"Agent ID: {agent_id}")
        print(f"Lambda ARN: {lambda_arn}")
        
        return agent_id, lambda_arn
    
    def _create_lambda_function(self):
        """Create Lambda function with all agents"""
        
        # Create deployment package
        self._create_deployment_package()
        
        with open('sustainability_agents.zip', 'rb') as f:
            zip_content = f.read()
        
        try:
            response = self.lambda_client.create_function(
                FunctionName='sustainability-agents-orchestrator',
                Runtime='python3.9',
                Role='arn:aws:iam::557017932249:role/AmazonBedrockExecutionRoleForAgents_SustainabilityAgent',
                Handler='lambda_handler.handler',
                Code={'ZipFile': zip_content},
                Description='Sustainability Supply Chain Agents Orchestrator',
                Timeout=300,
                MemorySize=512
            )
            return response['FunctionArn']
        except Exception as e:
            print(f"Lambda function may already exist: {e}")
            return f"arn:aws:lambda:us-west-2:557017932249:function:sustainability-agents-orchestrator"
    
    def _create_deployment_package(self):
        """Create deployment ZIP package"""
        with zipfile.ZipFile('sustainability_agents.zip', 'w') as zipf:
            # Add all agent files
            for root, dirs, files in os.walk('agents'):
                for file in files:
                    if file.endswith('.py'):
                        zipf.write(os.path.join(root, file), f'agents/{file}')
            
            # Add Lambda handler
            zipf.writestr('lambda_handler.py', self._get_lambda_handler_code())
    
    def _get_lambda_handler_code(self):
        """Generate Lambda handler code"""
        return '''
import json
from agents import AgentCore

def handler(event, context):
    """Main Lambda handler for Bedrock Agent requests"""
    
    try:
        action_group = event.get('actionGroup', '')
        function = event.get('function', '')
        parameters = event.get('parameters', {})
        
        # Initialize agent core
        agent_core = AgentCore()
        
        if function == 'analyze_sustainability':
            # Extract supply chain data from parameters
            supply_chain_data = {
                'suppliers': json.loads(parameters.get('suppliers_data', '[]')),
                'routes': json.loads(parameters.get('routes_data', '[]')),
                'inventory': json.loads(parameters.get('inventory_data', '[]'))
            }
            
            # Run complete analysis
            results = agent_core.orchestrate_sustainability_analysis(supply_chain_data)
            
            response_body = json.dumps(results, indent=2)
            
        else:
            response_body = "Function not supported"
        
        return {
            'response': {
                'actionGroup': action_group,
                'function': function,
                'functionResponse': {
                    'responseBody': {
                        'TEXT': {
                            'body': response_body
                        }
                    }
                }
            }
        }
        
    except Exception as e:
        return {
            'response': {
                'actionGroup': action_group,
                'function': function,
                'functionResponse': {
                    'responseBody': {
                        'TEXT': {
                            'body': f"Error: {str(e)}"
                        }
                    }
                }
            }
        }
'''
    
    def _create_bedrock_agent(self, lambda_arn):
        """Create main Bedrock Agent"""
        try:
            response = self.bedrock_agent.create_agent(
                agentName='sustainability-supply-chain-optimizer',
                description='AI agent for comprehensive supply chain sustainability analysis',
                foundationModel='anthropic.claude-3-sonnet-20240229-v1:0',
                instruction='''You are a sustainability expert AI agent that helps companies optimize their supply chain for environmental impact. 

You can analyze:
- Supplier sustainability profiles and certifications
- Transportation route emissions and optimization
- Inventory waste reduction opportunities  
- Overall carbon footprint calculation

When users ask for sustainability analysis, use the analyze_sustainability function with their supply chain data including suppliers, routes, and inventory information.

Provide actionable recommendations and clear metrics to help companies reduce their environmental impact.''',
                agentResourceRoleArn='arn:aws:iam::557017932249:role/WSParticipantRole'
            )
            return response['agent']['agentId']
        except Exception as e:
            print(f"Agent creation error: {e}")
            return "existing-agent-id"
    
    def _create_action_groups(self, agent_id, lambda_arn):
        """Create action groups for sustainability analysis"""
        
        schema = {
            "openAPISchemaVersion": "3.0.0",
            "info": {
                "title": "Sustainability Analysis API",
                "version": "1.0.0"
            },
            "paths": {
                "/analyze-sustainability": {
                    "post": {
                        "description": "Analyze complete supply chain sustainability",
                        "operationId": "analyze_sustainability",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "suppliers_data": {
                                                "type": "string",
                                                "description": "JSON string of supplier data"
                                            },
                                            "routes_data": {
                                                "type": "string", 
                                                "description": "JSON string of route data"
                                            },
                                            "inventory_data": {
                                                "type": "string",
                                                "description": "JSON string of inventory data"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        try:
            self.bedrock_agent.create_agent_action_group(
                agentId=agent_id,
                agentVersion='DRAFT',
                actionGroupName='sustainability-analysis',
                description='Complete sustainability analysis actions',
                actionGroupExecutor={'lambda': lambda_arn},
                apiSchema={'payload': json.dumps(schema)}
            )
        except Exception as e:
            print(f"Action group creation error: {e}")
    
    def _prepare_agent(self, agent_id):
        """Prepare agent for use"""
        try:
            self.bedrock_agent.prepare_agent(agentId=agent_id)
            print("Agent prepared successfully")
        except Exception as e:
            print(f"Agent preparation error: {e}")

if __name__ == "__main__":
    deployer = BedrockAgentDeployer()
    deployer.deploy_complete_solution()