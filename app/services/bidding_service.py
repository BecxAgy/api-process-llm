"""
Bidding Service - Handle bidding API operations
"""
import logging
from typing import Dict, Any, Optional
from app.clients.api_client import bidding_api_client
from app.models.llm_models import DocumentChecklistResponse

logger = logging.getLogger(__name__)


class BiddingService:
    """Service to handle bidding operations"""
    
    def __init__(self):
        self.api_client = bidding_api_client
    
    def convert_checklist_to_api_format(self, checklist: DocumentChecklistResponse) -> Dict[str, Any]:
        """Convert DocumentChecklistResponse to API format"""
        try:
            checklist_items = []
            
            for doc in checklist.documents:
                # Handle both dict and object formats
                if hasattr(doc, '__dict__'):
                    item = {
                        "name": doc.name,
                        "exigenceStatus": doc.exigenceStatus,
                        "additionalInfo": doc.additionalInfo,
                        "possibleToAttach": doc.possibleToAttach
                    }
                else:
                    # Already a dict
                    item = {
                        "name": doc.get("name", ""),
                        "exigenceStatus": doc.get("exigenceStatus", "OPCIONAL"),
                        "additionalInfo": doc.get("additionalInfo", ""),
                        "possibleToAttach": doc.get("possibleToAttach", True)
                    }
                
                checklist_items.append(item)
            
            return {"checklistItems": checklist_items}
            
        except Exception as e:
            logger.error(f"Erro ao converter checklist para formato da API: {e}")
            return {"checklistItems": []}
    
    async def update_bidding_checklist(
        self, 
        bidding_id: str, 
        checklist: DocumentChecklistResponse
    ) -> bool:
        """Update bidding checklist in the API"""
        try:
            logger.info(f"Atualizando checklist para bidding ID: {bidding_id}")
            
            # Convert to API format
            api_data = self.convert_checklist_to_api_format(checklist)
            
            # Send to API
            success = await self.api_client.update_checklist(bidding_id, api_data)
            
            if success:
                logger.info(f"Checklist atualizado com sucesso para bidding {bidding_id}")
            else:
                logger.error(f"Falha ao atualizar checklist para bidding {bidding_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Erro ao atualizar checklist do bidding {bidding_id}: {e}")
            return False