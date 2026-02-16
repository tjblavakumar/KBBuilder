#!/usr/bin/env python3
"""
Test your OpenAI API key
"""
import sys
from openai import OpenAI

def test_api_key(api_key):
    """Test if API key is valid"""
    print("Testing OpenAI API key...")
    print(f"Key: {api_key[:10]}...{api_key[-4:]}")
    print()
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Test with a simple embedding request
        print("Testing embeddings API...")
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input="test"
        )
        
        print("✓ API key is VALID!")
        print(f"✓ Embedding dimension: {len(response.data[0].embedding)}")
        print()
        print("Your API key is working correctly!")
        return True
        
    except Exception as e:
        print("✗ API key is INVALID!")
        print(f"Error: {str(e)}")
        print()
        print("Possible issues:")
        print("1. API key is incorrect or expired")
        print("2. No credits in your OpenAI account")
        print("3. API key doesn't have embeddings permission")
        print()
        print("Solutions:")
        print("1. Go to https://platform.openai.com/api-keys")
        print("2. Create a new API key")
        print("3. Make sure you have credits: https://platform.openai.com/account/billing")
        return False

if __name__ == "__main__":
    # Try to read from config first
    try:
        from config import get_config
        config = get_config()
        api_key = config.get_openai_api_key()
        
        if api_key and api_key != "your-openai-api-key-here":
            print("Using API key from config.yml")
            print()
            test_api_key(api_key)
        else:
            print("No valid API key found in config.yml")
            print()
            api_key = input("Enter your OpenAI API key to test: ").strip()
            if api_key:
                test_api_key(api_key)
            else:
                print("No API key provided")
    except Exception as e:
        print(f"Error: {e}")
        print()
        api_key = input("Enter your OpenAI API key to test: ").strip()
        if api_key:
            test_api_key(api_key)
