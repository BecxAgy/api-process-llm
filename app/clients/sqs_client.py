"""
AWS SQS Client configuration and factory
"""
import boto3
from typing import Optional
from app.config.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION


class SQSClient:
    """Factory and singleton for SQS client"""
    
    _instance: Optional[boto3.client] = None
    
    @classmethod
    def get_client(cls) -> boto3.client:
        """Get or create SQS client instance"""
        if cls._instance is None:
            cls._instance = boto3.client(
                'sqs',
                region_name=AWS_REGION,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            )
        return cls._instance
    
    @classmethod
    def reset_client(cls) -> None:
        """Reset client instance (useful for testing)"""
        cls._instance = None


# Global instance for easy import
sqs = SQSClient.get_client()
