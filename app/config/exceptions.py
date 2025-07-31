"""
Custom exceptions for the application
"""


class AppException(Exception):
    """Base exception class for the application"""
    pass


class ConfigurationError(AppException):
    """Raised when there's a configuration error"""
    pass


class S3Error(AppException):
    """Raised when there's an S3 operation error"""
    pass


class SQSError(AppException):
    """Raised when there's an SQS operation error"""
    pass


class PDFProcessingError(AppException):
    """Raised when there's a PDF processing error"""
    pass


class AIServiceError(AppException):
    """Raised when there's an AI service error"""
    pass
