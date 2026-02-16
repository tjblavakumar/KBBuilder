"""
Test script for OpenAI integration
"""
import sys
from services.openai_client import OpenAIClient
from services.llm_provider import OpenAILLMProvider

def test_openai_client():
    """Test OpenAI client for listing models"""
    print("Testing OpenAI Client...")
    print("-" * 50)
    
    try:
        client = OpenAIClient()
        models = client.list_available_models()
        default = client.get_default_model()
        
        print(f"✓ Found {len(models)} models")
        print(f"✓ Default model: {default}")
        print("\nAvailable models:")
        for model in models:
            print(f"  - {model.model_name} ({model.model_id})")
        
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def test_openai_provider():
    """Test OpenAI provider with API key"""
    print("\n\nTesting OpenAI Provider...")
    print("-" * 50)
    
    api_key = input("Enter your OpenAI API key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("⊘ Skipped (no API key provided)")
        return True
    
    try:
        provider = OpenAILLMProvider("gpt-4o-mini", api_key)
        
        # Test chat
        print("\nTesting chat completion...")
        response = provider.generate_chat_response("Say 'Hello, World!' in one word.")
        print(f"✓ Chat response: {response[:100]}")
        
        # Test embeddings
        print("\nTesting embeddings...")
        embedding = provider.generate_embedding("This is a test sentence.")
        print(f"✓ Embedding generated: {len(embedding)} dimensions")
        
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def main():
    print("=" * 50)
    print("OpenAI Integration Test Suite")
    print("=" * 50)
    print()
    
    results = []
    
    # Test 1: OpenAI Client
    results.append(("OpenAI Client", test_openai_client()))
    
    # Test 2: OpenAI Provider (optional)
    results.append(("OpenAI Provider", test_openai_provider()))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
