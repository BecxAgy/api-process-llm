"""
S3 Service - Handle S3 operations
"""
import logging
from typing import Optional, Dict, Any
from urllib.parse import unquote, urlparse
from app.clients.s3_client import s3
from app.config.config import AWS_S3_BUCKET

logger = logging.getLogger(__name__)


class S3Service:
    """Service to handle S3 operations"""
    
    def __init__(self):
        self.s3_client = s3
        self.bucket_name = AWS_S3_BUCKET
    
    def extract_key_from_url(self, url: str) -> Optional[str]:
        """Extract S3 object key from URL"""
        try:
            if not url:
                logger.warning("URL de arquivo não encontrada")
                return None
                
            parsed_url = urlparse(unquote(url))  # Desfaz o %3A etc.
            key = parsed_url.path.lstrip("/")  # Remove a barra inicial
            
            logger.info(f"Chave extraída: {key}")
            return key
            
        except Exception as e:
            logger.error(f"Erro ao extrair chave da URL: {e}")
            return None
    
    def is_pdf_file(self, key: str) -> bool:
        """Check if file is a PDF"""
        return key.lower().endswith('.pdf')
    
    def download_file(self, key: str) -> Optional[bytes]:
        """Download file from S3"""
        try:
            logger.info(f"Baixando arquivo: {key} do bucket: {self.bucket_name}")
            
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
            file_content = response['Body'].read()
            
            logger.info(f"Arquivo baixado com sucesso. Tamanho: {len(file_content)} bytes")
            return file_content
            
        except Exception as e:
            logger.error(f"Erro ao baixar objeto do S3: {e}")
            return None
    
    def process_file_from_url(self, url: str) -> Optional[bytes]:
        """Complete process: extract key from URL and download file"""
        key = self.extract_key_from_url(url)
        if not key:
            return None
            
        if not self.is_pdf_file(key):
            logger.warning(f"Arquivo {key} não é PDF. Pulando.")
            return None
            
        return self.download_file(key)
