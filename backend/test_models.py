"""
Quick test to verify Pydantic models work without warnings
"""
import warnings

# Capture warnings
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    
    from models import BedrockModel, OpenAIModel
    
    # Create test instances
    bedrock_model = BedrockModel(model_id="test-id", model_name="Test Model")
    openai_model = OpenAIModel(model_id="gpt-4o", model_name="GPT-4o")
    
    # Check for warnings
    pydantic_warnings = [warning for warning in w if 'protected namespace' in str(warning.message)]
    
    if pydantic_warnings:
        print("✗ FAILED: Pydantic warnings still present:")
        for warning in pydantic_warnings:
            print(f"  - {warning.message}")
    else:
        print("✓ SUCCESS: No Pydantic warnings!")
        print(f"  - BedrockModel: {bedrock_model.model_name}")
        print(f"  - OpenAIModel: {openai_model.model_name}")
