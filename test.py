"""
Debug script to test components individually
"""
import sys
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_imports():
    """Test all imports"""
    try:
        logger.info("=== TESTANDO IMPORTS ===")
        
        logger.info("Importando config...")
        from app.config.config import DEFAULT_LLM_MODEL, OPENROUTER_API_KEY, OPENROUTER_BASE_URL
        logger.info(f"✓ Config OK. API Key: {'Presente' if OPENROUTER_API_KEY else 'Ausente'}")
        
        logger.info("Importando llm_models...")
        from app.models.llm_models import LLMPromptTemplate, DocumentChecklistResponse
        logger.info("✓ llm_models OK")
        
        logger.info("Importando llm_client...")
        from app.clients.llm_client import llm_service
        logger.info(f"✓ llm_client OK. Service: {llm_service}")
        
        logger.info("Importando pdf_service...")
        from app.services.pdf_service import PDFProcessingService
        logger.info("✓ pdf_service OK")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro nos imports: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

def test_prompt_template():
    """Test prompt template"""
    try:
        logger.info("=== TESTANDO PROMPT TEMPLATE ===")
        
        from app.models.llm_models import LLMPromptTemplate
        
        template = LLMPromptTemplate()
        prompt = template.get_document_extraction_prompt()
        
        logger.info(f"✓ Template OK. Tamanho: {len(prompt)}")
        
        # Test formatting
        test_text = "Este é um edital de teste"
        formatted = prompt.format(document_content=test_text)
        
        logger.info(f"✓ Formatação OK. Tamanho formatado: {len(formatted)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro no template: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

def test_llm_service():
    """Test LLM service"""
    try:
        logger.info("=== TESTANDO LLM SERVICE ===")
        
        from app.clients.llm_client import llm_service
        
        if llm_service is None:
            logger.error("❌ llm_service é None")
            return False
        
        # Test simple completion
        response = llm_service.generate_completion(
            prompt="Responda apenas: OK",
            model="dolphin",
            max_tokens=10
        )
        
        logger.info(f"✓ LLM Service OK. Response: {response}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro no LLM service: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    logger.info("🔧 INICIANDO TESTES DE DEBUG")
    
    if test_imports():
        logger.info("✅ Imports OK")
        
        if test_prompt_template():
            logger.info("✅ Prompt Template OK")
            
            if test_llm_service():
                logger.info("✅ LLM Service OK")
                logger.info("🎉 TODOS OS TESTES PASSARAM!")
            else:
                logger.error("❌ LLM Service FALHOU")
        else:
            logger.error("❌ Prompt Template FALHOU")
    else:
        logger.error("❌ Imports FALHARAM")