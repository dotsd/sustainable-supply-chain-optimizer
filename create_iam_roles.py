#!/usr/bin/env python3
"""
Create required IAM roles for Bedrock Agent deployment
"""

import boto3
import json

def create_bedrock_execution_role():
    """Create IAM role for Bedrock Agent execution"""
    
    iam = boto3.client('iam')
    
    # Trust policy for Bedrock
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "bedrock.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    # Permissions policy
    permissions_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "bedrock:InvokeModel",
                    "bedrock:InvokeAgent",
                    "lambda:InvokeFunction",
                    "s3:GetObject",
                    "s3:PutObject",
                    "glue:GetDatabase",
                    "glue:GetTable",
                    "glue:CreateTable"
                ],
                "Resource": "*"
            }
        ]
    }
    
    role_name = "AmazonBedrockExecutionRoleForAgents_SustainabilityAgent"
    
    try:
        # Create role
        role_response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Execution role for Sustainability Supply Chain Bedrock Agent'
        )
        
        print(f"✅ Created role: {role_name}")
        print(f"   ARN: {role_response['Role']['Arn']}")
        
        # Attach permissions policy
        iam.put_role_policy(
            RoleName=role_name,
            PolicyName='BedrockAgentPermissions',
            PolicyDocument=json.dumps(permissions_policy)
        )
        
        print(f"✅ Attached permissions policy")
        
        return role_response['Role']['Arn']
        
    except iam.exceptions.EntityAlreadyExistsException:
        # Role already exists, get ARN
        role_response = iam.get_role(RoleName=role_name)
        print(f"⚠️ Role already exists: {role_name}")
        print(f"   ARN: {role_response['Role']['Arn']}")
        return role_response['Role']['Arn']

def create_lambda_execution_role():
    """Create IAM role for Lambda function execution"""
    
    iam = boto3.client('iam')
    
    # Trust policy for Lambda
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    role_name = "SustainabilityAgentLambdaExecutionRole"
    
    try:
        # Create role
        role_response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Execution role for Sustainability Agent Lambda functions'
        )
        
        print(f"✅ Created Lambda role: {role_name}")
        print(f"   ARN: {role_response['Role']['Arn']}")
        
        # Attach AWS managed policies
        managed_policies = [
            'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole',
            'arn:aws:iam::aws:policy/AmazonBedrockFullAccess',
            'arn:aws:iam::aws:policy/AmazonS3FullAccess',
            'arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole'
        ]
        
        for policy_arn in managed_policies:
            iam.attach_role_policy(
                RoleName=role_name,
                PolicyArn=policy_arn
            )
            print(f"   ✅ Attached policy: {policy_arn.split('/')[-1]}")
        
        return role_response['Role']['Arn']
        
    except iam.exceptions.EntityAlreadyExistsException:
        # Role already exists, get ARN
        role_response = iam.get_role(RoleName=role_name)
        print(f"⚠️ Lambda role already exists: {role_name}")
        print(f"   ARN: {role_response['Role']['Arn']}")
        return role_response['Role']['Arn']

if __name__ == "__main__":
    print("🔐 Creating IAM Roles for Bedrock Agent Deployment")
    print("=" * 55)
    
    try:
        # Create Bedrock execution role
        bedrock_role_arn = create_bedrock_execution_role()
        
        # Create Lambda execution role  
        lambda_role_arn = create_lambda_execution_role()
        
        print(f"\n🎉 IAM Roles Created Successfully!")
        print(f"\n📋 Update these ARNs in your deployment files:")
        print(f"   Bedrock Role ARN: {bedrock_role_arn}")
        print(f"   Lambda Role ARN: {lambda_role_arn}")
        
        # Save ARNs to file for easy reference
        with open('iam_role_arns.txt', 'w') as f:
            f.write(f"BEDROCK_ROLE_ARN={bedrock_role_arn}\n")
            f.write(f"LAMBDA_ROLE_ARN={lambda_role_arn}\n")
        
        print(f"\n💾 ARNs saved to: iam_role_arns.txt")
        
    except Exception as e:
        print(f"❌ Error creating roles: {str(e)}")
        print(f"   Make sure you have IAM permissions to create roles")