#!/usr/bin/env python3
"""
Deploy only Lambda function (skip Bedrock Agent due to permissions)
"""

import boto3
import json
import zipfile
import os

class LambdaDeployer:
    def __init__(self):
        self.lambda_client = boto3.client('lambda')
        
    def deploy_lambda_function(self):
        """Deploy Lambda function for agent orchestration"""
        
        print("🚀 Deploying Lambda Function Only...")
        
        # Create deployment package
        self._create_deployment_package()
        
        with open('sustainability_agents.zip', 'rb') as f:
            zip_content = f.read()
        
        try:
            # Try to update existing function first
            try:
                response = self.lambda_client.update_function_code(
                    FunctionName='sustainability-agents-orchestrator',
                    ZipFile=zip_content
                )
                print("✅ Updated existing Lambda function")
                return response['FunctionArn']
                
            except self.lambda_client.exceptions.ResourceNotFoundException:
                # Function doesn't exist, create new one
                response = self.lambda_client.create_function(
                    FunctionName='sustainability-agents-orchestrator',
                    Runtime='python3.9',
                    Role='arn:aws:iam::557017932249:role/LabRole',  # Use LabRole
                    Handler='lambda_handler.handler',
                    Code={'ZipFile': zip_content},
                    Description='Sustainability Supply Chain Agents Orchestrator',
                    Timeout=300,
                    MemorySize=512,
                    Environment={
                        'Variables': {
                            'STRANDS_API_KEY': 'strands_api_key_ai_hackathon'
                        }
                    }
                )
                print("✅ Created new Lambda function")
                return response['FunctionArn']
                
        except Exception as e:
            print(f"❌ Lambda deployment error: {e}")
            return None
    
    def _create_deployment_package(self):
        """Create deployment ZIP package"""
        with zipfile.ZipFile('sustainability_agents.zip', 'w') as zipf:
            # Add all agent files
            for root, dirs, files in os.walk('agents'):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, f'agents/{file}')
            
            # Add orchestration files
            for root, dirs, files in os.walk('orchestration'):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, f'orchestration/{file}')
            
            # Add support files
            support_files = ['strands_client.py', 'integration_adapter.py']
            for file in support_files:
                if os.path.exists(file):
                    zipf.write(file, file)
            
            # Add Lambda handler
            zipf.writestr('lambda_handler.py', self._get_lambda_handler_code())
    
    def _get_lambda_handler_code(self):
        """Generate Lambda handler code"""
        return '''
import json
import sys
import os

# Add current directory to path
sys.path.append('/var/task')

try:
    from agents import AgentCore
    from integration_adapter import IntegrationAdapter
    AGENTS_AVAILABLE = True
except ImportError as e:
    print(f"Import error: {e}")
    AGENTS_AVAILABLE = False

def handler(event, context):
    """Main Lambda handler for sustainability analysis"""
    
    try:
        print(f"Received event: {json.dumps(event)}")
        
        if not AGENTS_AVAILABLE:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': 'Agents not available',
                    'message': 'Agent modules could not be imported'
                })
            }
        
        # Handle different event types
        if 'Records' in event:
            # S3 trigger
            return handle_s3_event(event)
        elif 'httpMethod' in event:
            # API Gateway
            return handle_api_event(event)
        else:
            # Direct invocation
            return handle_direct_invocation(event)
            
    except Exception as e:
        print(f"Handler error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'message': 'Lambda execution failed'
            })
        }

def handle_direct_invocation(event):
    """Handle direct Lambda invocation"""
    
    # Check if it's a test event
    if event.get('test', False):
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Lambda function is working',
                'agents_available': AGENTS_AVAILABLE,
                'event': event
            })
        }
    
    # Handle sustainability analysis
    supply_chain_data = event.get('supply_chain_data')
    if not supply_chain_data:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'Missing supply_chain_data'
            })
        }
    
    # Run analysis
    agent_core = AgentCore()
    results = agent_core.orchestrate_sustainability_analysis(supply_chain_data)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'results': results,
            'message': 'Analysis completed successfully'
        })
    }

def handle_api_event(event):
    """Handle API Gateway event"""
    
    try:
        body = json.loads(event.get('body', '{}'))
        supply_chain_data = body.get('supply_chain_data')
        
        if not supply_chain_data:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing supply_chain_data'})
            }
        
        agent_core = AgentCore()
        results = agent_core.orchestrate_sustainability_analysis(supply_chain_data)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'results': results,
                'message': 'Analysis completed successfully'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def handle_s3_event(event):
    """Handle S3 trigger event"""
    
    results = []
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        print(f"Processing S3 object: s3://{bucket}/{key}")
        
        # Add S3 processing logic here if needed
        results.append({
            'bucket': bucket,
            'key': key,
            'status': 'processed'
        })
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'Processed {len(results)} S3 objects',
            'results': results
        })
    }
'''

    def test_lambda_function(self, function_arn):
        """Test the deployed Lambda function"""
        
        print("\n🧪 Testing Lambda Function...")
        
        try:
            # Test with simple event
            test_event = {
                'test': True,
                'message': 'Testing sustainability agents Lambda'
            }
            
            response = self.lambda_client.invoke(
                FunctionName='sustainability-agents-orchestrator',
                Payload=json.dumps(test_event)
            )
            
            result = json.loads(response['Payload'].read())
            print(f"✅ Lambda test result: {result}")
            
            return True
            
        except Exception as e:
            print(f"❌ Lambda test failed: {e}")
            return False

if __name__ == "__main__":
    deployer = LambdaDeployer()
    
    print("🚀 Deploying Lambda Function (Bedrock Agent skipped due to permissions)")
    print("=" * 70)
    
    # Deploy Lambda
    lambda_arn = deployer.deploy_lambda_function()
    
    if lambda_arn:
        print(f"\n✅ Lambda Function Deployed Successfully!")
        print(f"   ARN: {lambda_arn}")
        
        # Test Lambda
        test_success = deployer.test_lambda_function(lambda_arn)
        
        if test_success:
            print(f"\n🎉 Deployment Complete!")
            print(f"📋 Next Steps:")
            print(f"   1. Start local API: python api_endpoint.py")
            print(f"   2. Test system: python test_integration.py")
            print(f"   3. Use Lambda ARN for manual Bedrock Agent setup if needed")
        else:
            print(f"\n⚠️ Lambda deployed but test failed")
    else:
        print(f"\n❌ Lambda deployment failed")