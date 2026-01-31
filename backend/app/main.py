"""
PULSE FastAPI Application
==========================
REST API for the PULSE intelligence platform.

Endpoints:
- GET /api/insights - Fetch market insights
- GET /api/signals - Fetch Reddit signals
- GET /api/stats - Get dashboard statistics
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import routers
from app.api.routes import insights, signals, stats

# Create FastAPI app
app = FastAPI(
    title="PULSE API",
    description="Market intelligence insights from Reddit discussions",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "http://localhost:5173",  # Vite default
        "https://*.vercel.app",   # Vercel deployments
        "https://*.up.railway.app",  # Railway deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(insights.router, prefix="/api", tags=["insights"])
app.include_router(signals.router, prefix="/api", tags=["signals"])
app.include_router(stats.router, prefix="/api", tags=["stats"])


@app.get("/")
async def root():
    """
    API root endpoint.
    """
    return {
        "name": "PULSE API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "insights": "/api/insights",
            "signals": "/api/signals",
            "stats": "/api/stats",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {
        "status": "healthy",
        "service": "PULSE API"
    }


if __name__ == "__main__":
    import uvicorn

    # Get port from environment or use default
    port = int(os.getenv("PORT", "8000"))

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True  # Enable auto-reload for development
    )
