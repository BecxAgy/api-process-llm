"""
OpenRouter LLM Client configuration
Provides access to multiple LLM models through OpenRouter API
"""
from openai import OpenAI  # Mudança aqui
from typing import Optional, Dict, Any
from enum import Enum
from app.config.config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, LLM_MODELS, DEFAULT_LLM_MODEL


class LLMModel(Enum):
    """Available LLM models"""
    GEMMA = "gemma"
    DEEPSEEK = "deepseek" 
    DOLPHIN = "dolphin"


class OpenRouterClient:
    """Factory and singleton for OpenRouter client"""
    
    _instance: Optional[OpenAI] = None  # Mudança aqui
    
    @classmethod
    def get_client(cls) -> OpenAI:  # Mudança aqui
        """Get or create OpenRouter client instance"""
        if cls._instance is None:
            cls._instance = OpenAI(  # Mudança aqui - removido 'openai.'
                api_key=OPENROUTER_API_KEY,
                base_url=OPENROUTER_BASE_URL
            )
        return cls._instance
    
    @classmethod
    def reset_client(cls) -> None:
        """Reset client instance (useful for testing)"""
        cls._instance = None
    
    @classmethod
    def get_model_name(cls, model: str) -> str:
        """Get full model name for OpenRouter API"""
        return LLM_MODELS.get(model, LLM_MODELS[DEFAULT_LLM_MODEL])
    
    @classmethod
    def get_available_models(cls) -> Dict[str, str]:
        """Get dictionary of available models"""
        return LLM_MODELS.copy()


class LLMService:
    """Service for LLM operations with model selection"""
    
    def __init__(self):
        self.client = OpenRouterClient.get_client()
    
    def generate_completion(
        self, 
        prompt: str, 
        model: str = DEFAULT_LLM_MODEL,
        max_tokens: int = 4000,
        temperature: float = 0.1
    ) -> Optional[str]:
        """Generate completion using specified model"""
        try:
            model_name = OpenRouterClient.get_model_name(model)
            
            response = self.client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise RuntimeError(f"Erro ao gerar completion com modelo {model}: {e}")


# Global instances for easy import
openrouter_client = OpenRouterClient.get_client()
llm_service = LLMService()