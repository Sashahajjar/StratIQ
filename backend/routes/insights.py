"""
Insights routes
"""

from fastapi import APIRouter, HTTPException
from models.schemas import InsightRequest, InsightResponse
from services.insight_service import InsightService

router = APIRouter()
insight_service = InsightService()


@router.post("/", response_model=InsightResponse)
async def generate_insights(request: InsightRequest):
    """
    Generate AI-written summaries and key takeaways
    """
    try:
        insights = await insight_service.generate_insights(
            industry=request.industry,
            company=request.company,
            data=request.data
        )
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{insight_id}")
async def get_insight(insight_id: int):
    """Get a specific insight by ID"""
    try:
        insight = await insight_service.get_insight(insight_id)
        if not insight:
            raise HTTPException(status_code=404, detail="Insight not found")
        return insight
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

