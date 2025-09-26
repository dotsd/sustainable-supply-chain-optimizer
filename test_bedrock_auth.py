#!/usr/bin/env python3
"""
Test Bedrock Agent authentication
"""

import requests
import json

def test_bedrock_authentication():
    """Test Bedrock agent authentication endpoints"""
    
    print("🔐 Testing Bedrock Agent Authentication")
    print("=" * 50)
    
    base_url = "http://localhost:5001"
    api_key = "strands_api_key_ai_hackathon"
    
    # Test 1: Validate API Key
    print("\n🔑 Test 1: API Key Validation")
    print("-" * 30)
    
    try:
        # Valid key test
        response = requests.post(
            f"{base_url}/bedrock/auth/validate",
            json={"api_key": api_key}
        )
        print(f"✅ Valid Key Test: {response.json()}")
        
        # Invalid key test
        response = requests.post(
            f"{base_url}/bedrock/auth/validate",
            json={"api_key": "invalid_key"}
        )
        print(f"❌ Invalid Key Test: {response.json()}")
        
    except Exception as e:
        print(f"❌ API Key validation failed: {e}")
    
    # Test 2: Chat with Authentication
    print(f"\n💬 Test 2: Authenticated Chat")
    print("-" * 30)
    
    try:
        chat_data = {
            "message": "Analyze sustainability for my supply chain with 5 suppliers",
            "api_key": api_key
        }
        
        response = requests.post(
            f"{base_url}/bedrock/agent/chat",
            json=chat_data,
            headers={'X-API-Key': api_key}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Chat Response: {result.get('response', 'No response')[:100]}...")
            print(f"   Session ID: {result.get('session_id')}")
        else:
            print(f"❌ Chat failed: {response.json()}")
            
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
    
    # Test 3: Direct Agent Invocation
    print(f"\n🤖 Test 3: Direct Agent Invocation")
    print("-" * 30)
    
    try:
        invoke_data = {
            "agent_id": "sustainability-supply-chain-optimizer",
            "input_text": "Generate sustainability analysis for 3 suppliers and 5 routes",
            "api_key": api_key
        }
        
        response = requests.post(
            f"{base_url}/bedrock/agent/invoke",
            json=invoke_data,
            headers={'X-API-Key': api_key}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Agent Response: {result.get('result', 'No result')[:100]}...")
            print(f"   Authenticated: {result.get('authenticated')}")
        else:
            print(f"❌ Agent invocation failed: {response.json()}")
            
    except Exception as e:
        print(f"❌ Agent invocation test failed: {e}")
    
    # Test 4: Unauthorized Access
    print(f"\n🚫 Test 4: Unauthorized Access")
    print("-" * 30)
    
    try:
        # Test without API key
        response = requests.post(
            f"{base_url}/bedrock/agent/chat",
            json={"message": "Test without auth"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 400:
            print("✅ Correctly blocked unauthorized access")
        else:
            print("⚠️ Security issue: Unauthorized access allowed")
            
    except Exception as e:
        print(f"❌ Unauthorized test failed: {e}")
    
    print(f"\n🎉 Bedrock Authentication Tests Complete!")
    print(f"🔑 API Key: {api_key}")
    print(f"🌐 Bedrock Endpoint: {base_url}")

if __name__ == "__main__":
    test_bedrock_authentication()