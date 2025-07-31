"""
SQS Consumer - Polls messages from SQS queue and processes them
"""
import time
import logging
from app.config.logging_config import setup_logging
from app.services.sqs_service import SQSService
from app.consumers.message_processor import MessageProcessor
from app.config.config import MAX_MESSAGES_PER_POLL, POLL_WAIT_TIME

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


class SQSConsumer:
    """Main SQS consumer class"""
    
    def __init__(self):
        self.sqs_service = SQSService()
        self.message_processor = MessageProcessor()
    
    def process_single_message(self, message: dict) -> bool:
        """Process a single SQS message"""
        try:
            # Parse message body
            message_body = message.get("Body", "")
            parsed_message = self.sqs_service.parse_message_body(message_body)
            
            if parsed_message["type"] == "empty":
                logger.info("Mensagem vazia recebida, pulando...")
                return True
            
            # Process message content
            success = self.message_processor.process_message(parsed_message["content"])
            
            if success:
                logger.info("Mensagem processada com sucesso")
            else:
                logger.warning("Falha ao processar mensagem")
            
            return success
            
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
            return False
    
    def poll_messages(self):
        """Main polling loop for SQS messages"""
        logger.info("Iniciando polling da fila SQS...")
        
        while True:
            try:
                # Receive messages from SQS
                messages = self.sqs_service.receive_messages(
                    max_messages=MAX_MESSAGES_PER_POLL,
                    wait_time=POLL_WAIT_TIME
                )
                
                for message in messages:
                    try:
                        # Process message
                        success = self.process_single_message(message)
                        
                        # Always delete message to avoid reprocessing
                        # Even if processing failed, we don't want infinite retries
                        receipt_handle = message["ReceiptHandle"]
                        self.sqs_service.delete_message(receipt_handle)
                        
                        if not success:
                            logger.warning("Mensagem deletada após falha no processamento")
                            
                    except Exception as e:
                        logger.error(f"Erro crítico ao processar mensagem: {e}")
                        # Delete message to prevent infinite reprocessing
                        try:
                            receipt_handle = message["ReceiptHandle"]
                            self.sqs_service.delete_message(receipt_handle)
                            logger.info("Mensagem deletada após erro crítico")
                        except Exception as delete_error:
                            logger.error(f"Erro ao deletar mensagem com falha: {delete_error}")
                
            except Exception as e:
                logger.error(f"Erro ao consumir fila: {e}")
                time.sleep(5)  # Wait before retrying


# Global instance and functions for backward compatibility
_consumer = SQSConsumer()

def poll_messages():
    """Backward compatible function"""
    _consumer.poll_messages()
