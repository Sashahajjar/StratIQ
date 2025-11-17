"""
Market data routes
"""

from fastapi import APIRouter, HTTPException
from models.schemas import MarketDataRequest, MarketDataResponse
from services.market_service import MarketService

router = APIRouter()
market_service = MarketService()


@router.post("/", response_model=MarketDataResponse)
async def fetch_market_data(request: MarketDataRequest):
    """
    Fetch and preprocess market or industry data
    """
    try:
        data = await market_service.get_market_data(
            industry=request.industry,
            company=request.company,
            timeframe=request.timeframe
        )
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/industries")
async def list_industries():
    """Get list of available industries"""
    return {
        "industries": [
            "Technology",
            "Healthcare",
            "Finance",
            "Retail",
            "Manufacturing",
            "Energy",
            "Education",
            "Real Estate",
            "Fashion"
        ]
    }
