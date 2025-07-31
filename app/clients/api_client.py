"""
API Client for bidding checklist operations
"""
import httpx
import logging
from typing import Optional, Dict, Any
from app.config.config import BIDDING_API_BASE_URL, BIDDING_API_TIMEOUT

logger = logging.getLogger(__name__)


class BiddingAPIClient:
    """Client for bidding API operations"""
    
    def __init__(self):
        self.base_url = BIDDING_API_BASE_URL
        self.timeout = BIDDING_API_TIMEOUT
    
    async def update_checklist(self, bidding_id: str, checklist_data: Dict[str, Any]) -> bool:
        """Update bidding checklist via PATCH request"""
        try:
            url = f"{self.base_url}/v1/bidding/checklist/{bidding_id}"
            
            logger.info(f"Enviando checklist para API: {url}")
            logger.info(f"Dados do checklist: {len(checklist_data.get('checklistItems', []))} itens")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.patch(
                    url,
                    json=checklist_data,
                    headers={
                        "accept": "*/*",
                        "Content-Type": "application/json"
                    }
                )
                
                if response.status_code == 200:
                    logger.info(f"Checklist atualizado com sucesso para bidding ID: {bidding_id}")
                    return True
                else:
                    logger.error(f"Erro ao atualizar checklist. Status: {response.status_code}")
                    logger.error(f"Resposta: {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Erro ao enviar checklist para API: {e}")
            return False


# Global instance for easy import
bidding_api_client = BiddingAPIClient()