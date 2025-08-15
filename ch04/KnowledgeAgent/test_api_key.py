#!/usr/bin/env python3
"""
Simple script to test OpenAI API key and diagnose issues.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file into OS environment
print("📁 Loading .env file into OS environment variables...")
load_dotenv(override=True)

def test_api_key():
    """Test the OpenAI API key."""
    print("🔍 Testing OpenAI API Key")
    print("=" * 50)
    
    # Get API key from environment
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No API key found in environment")
        print("💡 Make sure your .env file contains: OPENAI_API_KEY=your_key_here")
        return False
    
    print(f"📋 API Key found: {api_key[:20]}...{api_key[-10:]}")
    print(f"📏 Key length: {len(api_key)} characters")
    
    # Check key format
    if api_key.startswith('sk-'):
        print("✅ Valid OpenAI API key format")
    else:
        print("❌ Unknown API key format")
        print("💡 Valid OpenAI API keys should start with 'sk-'")
        return False
    
    # Test API connection
    try:
        client = OpenAI(api_key=api_key)
        
        # Test 1: Simple completion
        print("\n🧪 Test 1: Testing completion API...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'Hello, API test successful!'"}],
            max_tokens=10
        )
        print(f"✅ Completion test passed: {response.choices[0].message.content}")
        
        # Test 2: Embeddings API
        print("\n🧪 Test 2: Testing embeddings API...")
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input="Test text for embedding"
        )
        print(f"✅ Embeddings test passed: {len(response.data[0].embedding)} dimensions")
        
        # Test 3: List models
        print("\n🧪 Test 3: Testing model access...")
        models = client.models.list()
        gpt4_available = any('gpt-4' in model.id for model in models.data)
        embedding_available = any('text-embedding-3-small' in model.id for model in models.data)
        
        print(f"✅ GPT-4 available: {gpt4_available}")
        print(f"✅ text-embedding-3-small available: {embedding_available}")
        
        if not gpt4_available:
            print("⚠️  GPT-4 not available - check your plan/quotas")
        if not embedding_available:
            print("⚠️  text-embedding-3-small not available - check your plan/quotas")
        
        print("\n🎉 All API tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ API test failed: {str(e)}")
        
        # Provide specific guidance based on error
        if "401" in str(e) and "invalid_api_key" in str(e):
            print("\n💡 Troubleshooting suggestions:")
            print("   1. Check if the API key is correct")
            print("   2. Ensure the API key has proper permissions")
            print("   3. Check if your OpenAI account has the required models enabled")
            print("   4. Verify your OpenAI account billing status")
        elif "quota" in str(e).lower():
            print("\n💡 You may have hit your quota limit")
        elif "rate_limit" in str(e).lower():
            print("\n💡 You may have hit rate limits")
        
        return False

def check_environment():
    """Check environment setup."""
    print("\n🔧 Environment Check")
    print("=" * 30)
    
    # Check .env file
    if os.path.exists('.env'):
        print("✅ .env file exists")
        
        # Show .env file contents (without revealing sensitive data)
        try:
            with open('.env', 'r') as f:
                lines = f.readlines()
                print(f"📄 .env file has {len(lines)} lines:")
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if 'OPENAI_API_KEY' in line:
                            # Show only first and last few characters of API key
                            parts = line.split('=')
                            if len(parts) >= 2:
                                key_value = parts[1].strip()
                                if key_value:
                                    print(f"   {parts[0]}=sk-...{key_value[-10:]}")
                                else:
                                    print(f"   {parts[0]}=<empty>")
                        else:
                            print(f"   {line}")
        except Exception as e:
            print(f"⚠️  Could not read .env file: {e}")
    else:
        print("❌ .env file not found")
    
    # Check if environment variables are loaded
    print("\n🌍 Environment Variables Check:")
    api_key = os.environ.get('OPENAI_API_KEY')
    if api_key:
        print(f"✅ OPENAI_API_KEY loaded: {api_key[:20]}...{api_key[-10:]}")
    else:
        print("❌ OPENAI_API_KEY not found in environment")
    
    llm_model = os.environ.get('LLM_MODEL')
    if llm_model:
        print(f"✅ LLM_MODEL loaded: {llm_model}")
    else:
        print("❌ LLM_MODEL not found in environment")
    
    embedding_model = os.environ.get('EMBEDDING_MODEL')
    if embedding_model:
        print(f"✅ EMBEDDING_MODEL loaded: {embedding_model}")
    else:
        print("❌ EMBEDDING_MODEL not found in environment")
    
    # Check knowledge_files
    if os.path.exists('./knowledge_files'):
        pdf_files = [f for f in os.listdir('./knowledge_files') if f.endswith('.pdf')]
        print(f"✅ knowledge_files folder exists with {len(pdf_files)} PDF files")
    else:
        print("❌ knowledge_files folder not found")
    
    # Check required packages
    try:
        import openai
        print("✅ openai package installed")
    except ImportError:
        print("❌ openai package not installed")
    
    try:
        import dotenv
        print("✅ python-dotenv package installed")
    except ImportError:
        print("❌ python-dotenv package not installed")

if __name__ == "__main__":
    check_environment()
    success = test_api_key()
    
    if success:
        print("\n🎯 Ready to run RAG system tests!")
        print("   Run: python test_rag_system_simple.py")
    else:
        print("\n🔧 Please fix the API key issue before running tests")
        exit(1) 