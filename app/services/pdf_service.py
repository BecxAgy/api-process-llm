"""
PDF Processing Service - Handle PDF processing with AI
"""
import json
import logging
from typing import Optional
from app.clients.llm_client import llm_service, LLMModel
from app.models.llm_models import DocumentChecklistResponse, LLMPromptTemplate
from app.config.config import DEFAULT_LLM_MODEL

logger = logging.getLogger(__name__)


class PDFProcessingService:
    """Service to handle PDF processing operations"""
    
    def __init__(self):
        self.llm_service = llm_service
        self.prompt_template = LLMPromptTemplate()
    
    def extract_text_from_pdf(self, file_content: bytes) -> Optional[str]:
        """Extract text from PDF content"""
        try:
            import PyPDF2
            import io
            
            logger.info(f"Extraindo texto de PDF de {len(file_content)} bytes")
            
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            
            # Extract text from all pages
            extracted_text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                extracted_text += page.extract_text() + "\n"
            
            if not extracted_text.strip():
                logger.warning("Nenhum texto extraído do PDF")
                return None
                
            logger.info(f"Texto extraído com sucesso: {len(extracted_text)} caracteres")
            return extracted_text.strip()
            
        except Exception as e:
            logger.error(f"Erro ao extrair texto do PDF: {e}")
            return None
    
    def process_pdf_with_llm(
        self, 
        pdf_text: str, 
        model: str = DEFAULT_LLM_MODEL
    ) -> Optional[DocumentChecklistResponse]:
        """Process PDF text with LLM to extract document requirements"""
        try:
            logger.info(f"Processando PDF com modelo {model}")
            
            # Prepare prompt
            prompt = self.prompt_template.get_document_extraction_prompt()
            formatted_prompt = prompt.format(document_content=pdf_text)
            
            # Generate completion
            response = self.llm_service.generate_completion(
                prompt=formatted_prompt,
                model=model,
                max_tokens=4000,
                temperature=0.1
            )
            logger.info(f"Resposta do LLM: {response}")
            
            if not response:
                logger.error("Resposta vazia do LLM")
                return None
            
            # Clean response - remove markdown code blocks
            cleaned_response = self._clean_llm_response(response)
            
            # Parse JSON response
            try:
                response_json = json.loads(cleaned_response)
                
                # Handle different response formats
                documents = []
                if "checklistItems" in response_json:
                    documents = response_json["checklistItems"]
                elif "documents" in response_json:
                    documents = response_json["documents"]
                else:
                    logger.error("Formato de resposta desconhecido")
                    return None
                
                # Calculate counts
                mandatory_count = sum(1 for doc in documents if doc.get("exigenceStatus") == "OBRIGATORIO")
                optional_count = len(documents) - mandatory_count
                
                # Create complete response
                checklist_response = DocumentChecklistResponse(
                    documents=documents,
                    total_documents=len(documents),
                    mandatory_count=mandatory_count,
                    optional_count=optional_count
                )
                
                logger.info(f"Checklist gerado com {len(documents)} documentos")
                return checklist_response
                
            except json.JSONDecodeError as e:
                logger.error(f"Erro ao fazer parse do JSON da resposta LLM: {e}")
                logger.error(f"Resposta limpa recebida: {cleaned_response}")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao processar PDF com LLM: {e}")
            return None
    
    def _clean_llm_response(self, response: str) -> str:
        """Clean LLM response by removing markdown code blocks and extra whitespace"""
        try:
            # Remove markdown code blocks
            if response.startswith("```json"):
                response = response[7:]  # Remove ```json
            elif response.startswith("```"):
                response = response[3:]   # Remove ```
            
            if response.endswith("```"):
                response = response[:-3]  # Remove trailing ```
            
            # Strip whitespace
            return response.strip()
            
        except Exception as e:
            logger.error(f"Erro ao limpar resposta do LLM: {e}")
            return response
        
    def process_pdf(
        self, 
        file_content: bytes, 
        model: str = DEFAULT_LLM_MODEL
    ) -> Optional[DocumentChecklistResponse]:
        """Complete PDF processing pipeline"""
        try:
            logger.info(f"Iniciando processamento completo de PDF de {len(file_content)} bytes")
            
            # Extract text from PDF
            pdf_text = self.extract_text_from_pdf(file_content)
            if not pdf_text:
                logger.error("Falha na extração de texto do PDF")
                return None
            
            # Process with LLM
            result = self.process_pdf_with_llm(pdf_text, model)
            logger.info(f"Resultado do processamento com LLM: {result}")
           
            if not result:
                logger.error("Falha no processamento com LLM")
                return None
            
            logger.info("PDF processado com sucesso")
            return result
            
        except Exception as e:
            logger.error(f"Erro no processamento completo do PDF: {e}")
            return None
