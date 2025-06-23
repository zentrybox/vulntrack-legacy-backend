from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.supabase_client import SUPABASE_KEY, SUPABASE_URL

app = FastAPI(
    title="VulnTrack Core Scanning Engine",
    description="A FastAPI application for vulnerability scanning using Supabase as backend",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the VulnTrack Core Scanning Engine!",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "supabase_url": SUPABASE_URL,
        "supabase_configured": bool(SUPABASE_URL and SUPABASE_KEY),
    }
