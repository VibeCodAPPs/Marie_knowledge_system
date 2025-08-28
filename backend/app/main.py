"""
Marie - Personal Knowledge Management System
Main FastAPI application entry point
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
import os
from pathlib import Path

from app.core.config import settings
from app.core.database import init_db
from app.api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("🧪 Starting Marie Knowledge System...")
    
    # Initialize database
    await init_db()
    print("✅ Database initialized")
    
    # Initialize AI models (placeholder for now)
    print("🤖 AI models ready")
    
    yield
    
    # Shutdown
    print("🔄 Shutting down Marie...")


# Create FastAPI app
app = FastAPI(
    title="Marie Knowledge System",
    description="AI-powered personal knowledge management system inspired by Marie Curie",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Marie Knowledge System",
        "version": "0.1.0"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with welcome message"""
    return {
        "message": "Welcome to Marie Knowledge System",
        "description": "AI-powered personal knowledge management inspired by Marie Curie",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
