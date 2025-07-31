"""
API routes for LLM and PDF processing operations
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from typing import Optional
from app.services.pdf_service import PDFProcessingService
from app.clients.llm_client import OpenRouterClient, LLMModel
from app.models.llm_models import DocumentChecklistResponse
from app.config.config import DEFAULT_LLM_MODEL

router = APIRouter(prefix="/api/v1", tags=["Processing"])

pdf_service = PDFProcessingService()


@router.get("/models")
async def get_available_models():
    """Get list of available LLM models"""
    return {
        "models": OpenRouterClient.get_available_models(),
        "default": DEFAULT_LLM_MODEL
    }


@router.post("/test-llm")
async def test_llm_endpoint(
    prompt: str,
    model: str = Query(DEFAULT_LLM_MODEL, description="LLM model to use")
):
    """Test LLM with custom prompt"""
    
    # Validate model
    available_models = OpenRouterClient.get_available_models()
    if model not in available_models:
        raise HTTPException(
            status_code=400,
            detail=f"Modelo '{model}' não disponível. Modelos disponíveis: {list(available_models.keys())}"
        )
    
    try:
        from app.clients.llm_client import llm_service
        
        response = llm_service.generate_completion(
            prompt=prompt,
            model=model
        )
        
        if not response:
            raise HTTPException(status_code=500, detail="Falha ao gerar resposta")
        
        return {
            "model_used": model,
            "prompt": prompt,
            "response": response
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
