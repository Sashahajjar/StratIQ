"""
Forecast routes
"""

from fastapi import APIRouter, HTTPException
from models.schemas import ForecastRequest, ForecastResponse
from services.forecast_service import ForecastService

router = APIRouter()
forecast_service = ForecastService()


@router.post("/", response_model=ForecastResponse)
async def generate_forecast(request: ForecastRequest):
    """
    Predict trends or funding growth using Prophet with real historical data
    """
    try:
        forecast = await forecast_service.generate_forecast(
            metric=request.metric,
            data=request.data,
            periods=request.periods,
            industry=request.industry,
            company=request.company
        )
        return forecast
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

