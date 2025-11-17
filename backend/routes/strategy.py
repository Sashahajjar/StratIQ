"""
Strategy routes
"""

from fastapi import APIRouter, HTTPException
from models.schemas import StrategyRequest, StrategyResponse
from services.strategy_service import StrategyService

router = APIRouter()
strategy_service = StrategyService()


@router.post("/", response_model=StrategyResponse)
async def generate_strategy(request: StrategyRequest):
    """
    Generate SWOT / PESTEL / growth recommendations
    """
    try:
        strategy = await strategy_service.generate_strategy(
            industry=request.industry,
            company=request.company,
            analysis_type=request.analysis_type
        )
        return strategy
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/swot")
async def generate_swot(request: StrategyRequest):
    """Generate SWOT analysis specifically"""
    request.analysis_type = "swot"
    return await generate_strategy(request)


@router.post("/pestel")
async def generate_pestel(request: StrategyRequest):
    """Generate PESTEL analysis specifically"""
    request.analysis_type = "pestel"
    return await generate_strategy(request)

