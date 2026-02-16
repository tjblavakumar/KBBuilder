from typing import List
from models import OpenAIModel

class OpenAIClient:
    """OpenAI client for listing available models"""
    
    def __init__(self):
        pass
    
    def list_available_models(self) -> List[OpenAIModel]:
        """List available OpenAI models for chat"""
        models = [
            OpenAIModel(
                model_id="gpt-4o",
                model_name="GPT-4o (Latest)"
            ),
            OpenAIModel(
                model_id="gpt-4o-mini",
                model_name="GPT-4o Mini"
            ),
            OpenAIModel(
                model_id="gpt-4-turbo",
                model_name="GPT-4 Turbo"
            ),
            OpenAIModel(
                model_id="gpt-3.5-turbo",
                model_name="GPT-3.5 Turbo"
            )
        ]
        return models
    
    def get_default_model(self) -> str:
        """Return the default model ID"""
        return "gpt-4o-mini"
