import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from typing import List
from models import BedrockModel

class BedrockClient:
    def __init__(self, profile_name: str = 'default'):
        try:
            session = boto3.Session(profile_name=profile_name)
            self.client = session.client('bedrock', region_name='us-east-1')
        except Exception as e:
            raise Exception(f"Failed to initialize Bedrock client: {str(e)}")
    
    def list_available_models(self) -> List[BedrockModel]:
        """List all available foundation models in AWS Bedrock"""
        try:
            response = self.client.list_foundation_models()
            
            models = []
            for model in response.get('modelSummaries', []):
                model_id = model.get('modelId', '')
                model_name = model.get('modelName', model_id)
                
                # Filter for text generation models
                if 'TEXT' in model.get('outputModalities', []):
                    models.append(BedrockModel(
                        model_id=model_id,
                        model_name=model_name
                    ))
            
            return models
        
        except NoCredentialsError:
            raise Exception("AWS credentials not found. Please configure AWS SSO.")
        except ClientError as e:
            raise Exception(f"AWS Bedrock error: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to list models: {str(e)}")
    
    def get_default_model(self) -> str:
        """Return the default model ID"""
        return "anthropic.claude-3-5-sonnet-20240620-v1:0"
