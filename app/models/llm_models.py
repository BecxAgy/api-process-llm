"""
LLM Models and Data Classes
"""
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum


class DocumentStatus(Enum):
    """Document requirement status"""
    OBRIGATORIO = "OBRIGATORIO"
    OPCIONAL = "OPCIONAL"


@dataclass
class DocumentRequirement:
    """Individual document requirement"""
    name: str
    exigenceStatus: str  # OBRIGATORIO or OPCIONAL
    additionalInfo: str
    possibleToAttach: bool


@dataclass
class DocumentChecklistResponse:
    """Response model for document checklist extraction"""
    documents: List[DocumentRequirement]
    total_documents: int
    mandatory_count: int
    optional_count: int
    processing_error: bool = False
    error_message: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "documents": [doc.__dict__ if hasattr(doc, '__dict__') else doc for doc in self.documents],
            "total_documents": self.total_documents,
            "mandatory_count": self.mandatory_count,
            "optional_count": self.optional_count,
            "processing_error": self.processing_error,
            "error_message": self.error_message
        }


class LLMPromptTemplate:
    """Template for LLM prompts"""
    
    @staticmethod
    def get_document_extraction_prompt() -> str:
        """Get prompt for document extraction from bidding notice"""
        return """Você deve extrair desse edital de licitação no contexto brasileiro quais os documentos necessários para entrar nesse edital.

Uma vez que os documentos de habilitação exigidos foram identificados e mapeados, o sistema deve gerar um checklist claro e organizado.

IMPORTANTE: Sua resposta deve ser APENAS um JSON válido, sem texto adicional, markdown ou explicações.

Formato da resposta JSON:
{{{{
    "checklistItems": [
        {{{{
            "name": "Nome do documento",
            "exigenceStatus": "OBRIGATORIO",
            "additionalInfo": "Informações adicionais sobre o documento",
            "possibleToAttach": true
        }}}}
    ]
}}}}

Regras:
1. exigenceStatus deve ser exatamente "OBRIGATORIO" ou "OPCIONAL"
2. possibleToAttach indica se é possível anexar este documento digitalmente
3. Inclua todos os documentos mencionados no edital
4. Se não encontrar documentos específicos, retorne um array vazio

Edital para análise:

{document_content}

Responda APENAS com o JSON válido:"""


@dataclass
class LLMRequest:
    """Request model for LLM operations"""
    prompt: str
    model: str
    max_tokens: int = 4000
    temperature: float = 0.1


@dataclass
class LLMResponse:
    """Response model for LLM operations"""
    content: str
    model: str
    tokens_used: Optional[int] = None
    success: bool = True
    error_message: Optional[str] = None