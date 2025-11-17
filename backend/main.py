"""
StratIQ Backend - Main Entry Point
FastAPI application for AI-powered business intelligence
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from routes import market, insights, strategy, forecast

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="StratIQ API",
    description="AI-powered business intelligence and strategy assistant",
    version="1.0.0"
)

# Configure CORS
from utils.config import settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(market.router, prefix="/api/market", tags=["Market"])
app.include_router(insights.router, prefix="/api/insights", tags=["Insights"])
app.include_router(strategy.router, prefix="/api/strategy", tags=["Strategy"])
app.include_router(forecast.router, prefix="/api/forecast", tags=["Forecast"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "StratIQ API is running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

