from abc import ABC, abstractmethod
from typing import List, Dict
import json
import boto3
from openai import OpenAI

class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate_chat_response(self, prompt: str) -> str:
        """Generate chat response from prompt"""
        pass
    
    @abstractmethod
    def generate_embedding(self, text: str) -> List[float]:
        """Generate text embedding"""
        pass


class BedrockLLMProvider(LLMProvider):
    """AWS Bedrock LLM provider"""
    
    def __init__(self, model_id: str, profile_name: str = 'default'):
        self.model_id = model_id
        session = boto3.Session(profile_name=profile_name)
        self.bedrock_runtime = session.client('bedrock-runtime', region_name='us-east-1')
    
    def generate_chat_response(self, prompt: str) -> str:
        """Generate chat response using Bedrock"""
        try:
            # Claude 3 format
            if 'claude-3' in self.model_id:
                body = json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 2000,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                })
            else:
                # Generic format
                body = json.dumps({
                    "prompt": prompt,
                    "max_tokens": 2000
                })
            
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                body=body,
                contentType="application/json",
                accept="application/json"
            )
            
            response_body = json.loads(response['body'].read())
            
            # Extract text based on model
            if 'claude-3' in self.model_id:
                return response_body['content'][0]['text']
            elif 'claude' in self.model_id:
                return response_body.get('completion', '')
            else:
                return response_body.get('results', [{}])[0].get('outputText', '')
        
        except Exception as e:
            raise Exception(f"Bedrock invocation failed: {str(e)}")
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding using AWS Bedrock Titan"""
        try:
            body = json.dumps({"inputText": text})
            response = self.bedrock_runtime.invoke_model(
                modelId="amazon.titan-embed-text-v1",
                body=body,
                contentType="application/json",
                accept="application/json"
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['embedding']
        except Exception as e:
            raise Exception(f"Failed to generate embedding: {str(e)}")


class OpenAILLMProvider(LLMProvider):
    """OpenAI LLM provider"""
    
    def __init__(self, model_id: str, api_key: str):
        self.model_id = model_id
        self.client = OpenAI(api_key=api_key)
        self.embedding_model = "text-embedding-3-small"  # Cost-effective option
    
    def generate_chat_response(self, prompt: str) -> str:
        """Generate chat response using OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            raise Exception(f"OpenAI invocation failed: {str(e)}")
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding using OpenAI"""
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Failed to generate embedding: {str(e)}")


def get_llm_provider(provider: str, model_id: str, api_key: str = None, profile_name: str = 'default') -> LLMProvider:
    """Factory function to get the appropriate LLM provider"""
    if provider == 'bedrock':
        return BedrockLLMProvider(model_id, profile_name)
    elif provider == 'openai':
        if not api_key:
            raise ValueError("API key is required for OpenAI provider")
        return OpenAILLMProvider(model_id, api_key)
    else:
        raise ValueError(f"Unknown provider: {provider}")
