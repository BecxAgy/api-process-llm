"""
FastAPI main application
"""
import logging
from contextlib import asynccontextmanager
from threading import Thread
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config.logging_config import setup_logging
from app.sqs_consumer import poll_messages
from app.api.routes import router as api_router


setup_logging()
logger = logging.getLogger(__name__)

# Global variable to store the consumer thread
consumer_thread = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager"""
    global consumer_thread
    
    
    logger.info("Iniciando aplicação...")
    try:
        consumer_thread = Thread(target=poll_messages, daemon=True)
        consumer_thread.start()
        logger.info("SQS Consumer iniciado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao iniciar SQS Consumer: {e}")
        raise
    
    yield
    
    
    logger.info("Finalizando aplicação...")



app = FastAPI(
    title="API Process Edict",
    description="API para processamento de documentos via SQS e S3",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Erro não tratado: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Erro interno do servidor"}
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "api-process-edict",
        "consumer_running": consumer_thread and consumer_thread.is_alive() if consumer_thread else False
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "API Process Edict",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/consumer/status")
async def consumer_status():
    """Check consumer thread status"""
    if not consumer_thread:
        raise HTTPException(status_code=503, detail="Consumer não foi iniciado")
    
    return {
        "consumer_running": consumer_thread.is_alive(),
        "thread_name": consumer_thread.name,
        "is_daemon": consumer_thread.daemon
    }
