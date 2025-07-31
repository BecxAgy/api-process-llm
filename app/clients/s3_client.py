"""
AWS S3 Client configuration and factory
"""
import boto3
from typing import Optional
from app.config.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION


class S3Client:
    """Factory and singleton for S3 client"""
    
    _instance: Optional[boto3.client] = None
    
    @classmethod
    def get_client(cls) -> boto3.client:
        """Get or create S3 client instance"""
        if cls._instance is None:
            cls._instance = boto3.client(
                's3',
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
s3 = S3Client.get_client()
