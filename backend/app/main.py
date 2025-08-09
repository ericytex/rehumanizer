from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
from app.api import humanize

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure CORS origins
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

# Add production origins from environment
if os.getenv("ENVIRONMENT") == "production":
    production_origins = os.getenv("CORS_ORIGINS", "").split(",")
    origins.extend([origin.strip() for origin in production_origins if origin.strip()])
else:
    # Allow all origins in development
    origins = ["*"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting ReHumanizer API...")
    print(f"🌐 CORS Origins: {origins}")
    yield
    # Shutdown
    print("👋 Shutting down ReHumanizer API...")

app = FastAPI(
    title="ReHumanizer API",
    description="AI-powered text humanization service",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware with configurable origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(humanize.router, prefix="/api/humanize", tags=["Humanization"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to ReHumanizer API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "ui": "/static/index.html",
            "humanize_text": "/api/humanize/text",
            "humanize_file": "/api/humanize/file",
            "demo": "/api/humanize/demo",
            "health": "/api/humanize/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "rehumanizer-api"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 