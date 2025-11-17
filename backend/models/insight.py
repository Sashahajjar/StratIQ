"""
Insight model for storing AI-generated insights
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from utils.database import Base


class Insight(Base):
    """Insight model"""
    
    __tablename__ = "insights"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50))  # 'summary', 'swot', 'strategy', 'forecast'
    content = Column(Text)
    meta_data = Column(JSON)  # Store additional data like SWOT matrix, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

