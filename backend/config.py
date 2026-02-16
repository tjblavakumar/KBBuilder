"""
Configuration loader for KB Builder
"""
import yaml
from pathlib import Path
from typing import Optional, Dict, Any

class Config:
    """Configuration manager"""
    
    def __init__(self, config_path: str = "config.yml"):
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self.load()
    
    def load(self):
        """Load configuration from YAML file"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f) or {}
        else:
            print(f"Config file not found: {self.config_path}")
            print("Using default configuration")
            self.config = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'openai.api_key')"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            
            if value is None:
                return default
        
        return value
    
    def get_openai_api_key(self) -> Optional[str]:
        """Get OpenAI API key from config"""
        return self.get('openai.api_key')
    
    def get_openai_default_model(self) -> str:
        """Get OpenAI default model"""
        return self.get('openai.default_model', 'gpt-4o-mini')
    
    def get_bedrock_profile(self) -> str:
        """Get AWS Bedrock profile name"""
        return self.get('bedrock.profile_name', 'default')
    
    def get_bedrock_region(self) -> str:
        """Get AWS Bedrock region"""
        return self.get('bedrock.region', 'us-east-1')
    
    def get_bedrock_default_model(self) -> str:
        """Get Bedrock default model"""
        return self.get('bedrock.default_model', 'anthropic.claude-3-5-sonnet-20240620-v1:0')
    
    def get_data_path(self) -> str:
        """Get data storage path"""
        return self.get('app.data_path', '../data')
    
    def get_log_level(self) -> str:
        """Get log level"""
        return self.get('app.log_level', 'INFO')


# Global config instance
_config = None

def get_config() -> Config:
    """Get global config instance"""
    global _config
    if _config is None:
        _config = Config()
    return _config
