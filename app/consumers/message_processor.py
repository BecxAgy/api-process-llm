"""
Message Processor - Handle message processing logic
"""
import logging
import asyncio
from typing import Dict, Any, Optional
from app.services.s3_service import S3Service
from app.services.pdf_service import PDFProcessingService
from app.services.bidding_service import BiddingService
from app.models.llm_models import DocumentChecklistResponse
from app.config.config import DEFAULT_LLM_MODEL

logger = logging.getLogger(__name__)


class MessageProcessor:
    """Handle message processing logic"""
    
    def __init__(self):
        self.s3_service = S3Service()
        self.pdf_service = PDFProcessingService()
        self.bidding_service = BiddingService()
    
    def process_message(self, message_content: Dict[str, Any]) -> bool:
        """Process a single message"""
        try:
            logger.info(f"Processando mensagem: {message_content}")
            
            # Extract bidding ID from message
            bidding_id = message_content.get("id", "")
            if not bidding_id:
                logger.warning("ID do bidding não encontrado na mensagem")
                return False
            
            # Extract filename/URL from message
            url = message_content.get("filename", "")
            if not url:
                logger.warning("URL de arquivo não encontrada na mensagem")
                return False
            
            
            # Extract model preference from message (optional)
            model = message_content.get("model", DEFAULT_LLM_MODEL)
            logger.info(f"Usando modelo: {model}")
            
            # Download file from S3
            file_content = self.s3_service.process_file_from_url(url)
            if not file_content:
                logger.warning("Falha ao baixar arquivo do S3")
                return False
            
            # Process PDF with AI
            result = self.pdf_service.process_pdf(file_content, model)
            if not result:
                logger.warning("Falha ao processar PDF")
                return False
            
            # Log processing results
            self._log_processing_results(result)
            
            # Send checklist to bidding API
            success = asyncio.run(self.bidding_service.update_bidding_checklist(bidding_id, result))
            if not success:
                logger.warning(f"Falha ao enviar checklist para API para bidding {bidding_id}")
                # Don't return False here - PDF was processed successfully
                # Just log the warning and continue
            
            logger.info("Mensagem processada com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
            return False
    
    def _log_processing_results(self, result: DocumentChecklistResponse) -> None:
        """Log the results of PDF processing"""
        logger.info(f"Documentos encontrados: {result.total_documents}")
        logger.info(f"Obrigatórios: {result.mandatory_count}")
        logger.info(f"Opcionais: {result.optional_count}")
        
        for doc in result.documents:
            if hasattr(doc, 'name') and hasattr(doc, 'exigenceStatus'):
                logger.info(f"- {doc.name} ({doc.exigenceStatus})")
            else:
                logger.info(f"- {doc.get('name', 'Unknown')} ({doc.get('exigenceStatus', 'Unknown')})")