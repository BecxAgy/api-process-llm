"""
SQS Service - Handle SQS message operations
"""
import json
import logging
from typing import Dict, Any, List, Optional
from app.clients.sqs_client import sqs
from app.config.config import SQS_QUEUE_URL

logger = logging.getLogger(__name__)


class SQSService:
    """Service to handle SQS operations"""
    
    def __init__(self):
        self.sqs_client = sqs
        self.queue_url = SQS_QUEUE_URL
    
    def receive_messages(self, max_messages: int = 1, wait_time: int = 10) -> List[Dict[str, Any]]:
        """Receive messages from SQS queue"""
        try:
            response = self.sqs_client.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=wait_time  # Long polling
            )
            
            messages = response.get("Messages", [])
            logger.info(f"Recebidas {len(messages)} mensagens da fila")
            return messages
            
        except Exception as e:
            logger.error(f"Erro ao receber mensagens da fila: {e}")
            return []
    
    def delete_message(self, receipt_handle: str) -> bool:
        """Delete message from SQS queue"""
        try:
            self.sqs_client.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle
            )
            logger.info("Mensagem deletada com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao deletar mensagem: {e}")
            return False
    
    def parse_message_body(self, message_body: str) -> Dict[str, Any]:
        """Parse message body (JSON or text)"""
        if not message_body.strip():
            logger.warning("Mensagem vazia recebida")
            return {"type": "empty", "content": ""}
        
        try:
            # Try to parse as JSON
            body = json.loads(message_body)
            logger.info("Mensagem JSON recebida")
            return {"type": "json", "content": body}
            
        except json.JSONDecodeError:
            # Handle as text message
            logger.info("Mensagem de texto simples recebida")
            return {
                "type": "text", 
                "content": {"message": message_body, "type": "text"}
            }
