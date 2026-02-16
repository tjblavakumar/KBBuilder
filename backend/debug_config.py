#!/usr/bin/env python3
"""
Debug config loading
"""
from config import get_config

config = get_config()

print("=" * 50)
print("Config Debug")
print("=" * 50)
print()

api_key = config.get_openai_api_key()

if api_key:
    print(f"✓ API key found in config")
    print(f"  Length: {len(api_key)} characters")
    print(f"  Starts with: {api_key[:10]}")
    print(f"  Ends with: {api_key[-10:]}")
    print(f"  Full key (first 20 chars): {api_key[:20]}...")
    print()
    
    # Check for common issues
    if api_key.startswith('"') or api_key.endswith('"'):
        print("⚠️  WARNING: API key has quotes - this might be the issue!")
        print("   Remove quotes from config.yml")
    
    if ' ' in api_key:
        print("⚠️  WARNING: API key contains spaces!")
    
    if '\n' in api_key or '\r' in api_key:
        print("⚠️  WARNING: API key contains newlines!")
    
    if api_key == "your-openai-api-key-here":
        print("✗ API key is still the placeholder!")
        print("  Please replace it with your actual key")
else:
    print("✗ No API key found in config")
    print("  Check backend/config.yml")

print()
print("Default model:", config.get_openai_default_model())
print()
