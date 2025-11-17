"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel
from typing import Optional, Dict, List, Any
from datetime import datetime


class MarketDataRequest(BaseModel):
    """Request schema for market data"""
    industry: Optional[str] = None
    company: Optional[str] = None
    timeframe: Optional[str] = "1y"  # 1m, 3m, 6m, 1y


class MarketDataResponse(BaseModel):
    """Response schema for market data"""
    industry: Optional[str] = None
    company: Optional[str] = None
    data: Dict[str, Any]
    news: List[Dict[str, Any]] = []
    metrics: Dict[str, Any] = {}


class InsightRequest(BaseModel):
    """Request schema for generating insights"""
    industry: Optional[str] = None
    company: Optional[str] = None
    data: Dict[str, Any] = {}


class InsightResponse(BaseModel):
    """Response schema for insights"""
    summary: str
    key_takeaways: List[str]
    created_at: datetime


class StrategyRequest(BaseModel):
    """Request schema for generating strategy"""
    industry: Optional[str] = None
    company: Optional[str] = None
    analysis_type: str = "swot"  # swot, pestel, growth


class StrategyResponse(BaseModel):
    """Response schema for strategy"""
    type: str
    content: Dict[str, Any]  # SWOT matrix, PESTEL analysis, etc.
    recommendations: List[str]
    created_at: datetime


class ForecastRequest(BaseModel):
    """Request schema for forecasting"""
    metric: str  # funding, growth, revenue
    data: List[Dict[str, Any]] = []
    periods: int = 12  # months
    industry: Optional[str] = None
    company: Optional[str] = None


class ForecastResponse(BaseModel):
    """Response schema for forecast"""
    metric: str
    historical: List[Dict[str, Any]]
    forecast: List[Dict[str, Any]]
    confidence_interval: Dict[str, Any]

