import boto3
import json

def create_bedrock_agent():
    """Create Bedrock Agent with CSV ingestion capability"""
    bedrock_agent = boto3.client('bedrock-agent')
    
    # Create agent
    agent_response = bedrock_agent.create_agent(
        agentName='csv-ingestion-agent',
        description='Agent for ingesting CSV files from S3 to Glue tables',
        foundationModel='anthropic.claude-3-sonnet-20240229-v1:0',
        instruction='You are an agent that helps ingest CSV files from S3 buckets into AWS Glue tables. When asked to ingest CSV files, use the ingest_csv_files function with the required parameters.',
        agentResourceRoleArn='arn:aws:iam::<account-id>:role/AmazonBedrockExecutionRoleForAgents_<role-suffix>'
    )
    
    agent_id = agent_response['agent']['agentId']
    
    # Create action group
    with open('bedrock_agent_schema.json', 'r') as f:
        api_schema = json.load(f)
    
    bedrock_agent.create_agent_action_group(
        agentId=agent_id,
        agentVersion='DRAFT',
        actionGroupName='csv-ingestion-actions',
        description='Actions for CSV file ingestion',
        actionGroupExecutor={
            'lambda': 'arn:aws:lambda:<region>:<account-id>:function:bedrock-csv-ingestion'
        },
        apiSchema={
            'payload': json.dumps(api_schema)
        }
    )
    
    # Prepare agent
    bedrock_agent.prepare_agent(
        agentId=agent_id
    )
    
    print(f"Bedrock Agent created with ID: {agent_id}")
    return agent_id

if __name__ == "__main__":
    create_bedrock_agent()