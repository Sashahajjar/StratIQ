"""
External API clients for fetching market data
"""

import requests
from typing import Dict, List, Optional
from utils.config import settings
import json
import os


class YahooFinanceClient:
    """Client for Yahoo Finance (free, no API key needed)"""
    
    def get_company_data(self, symbol: str) -> Optional[Dict]:
        """Get company data from Yahoo Finance"""
        try:
            # Use yfinance library if available, otherwise use web scraping
            try:
                import yfinance as yf
                ticker = yf.Ticker(symbol)
                info = ticker.info
                return {
                    "name": info.get("longName", symbol),
                    "sector": info.get("sector", ""),
                    "industry": info.get("industry", ""),
                    "market_cap": info.get("marketCap", 0),
                    "revenue": info.get("totalRevenue", 0),
                    "growth_rate": info.get("revenueGrowth", 0) * 100 if info.get("revenueGrowth") else 0
                }
            except ImportError:
                # Fallback to web scraping
                return None
        except Exception as e:
            print(f"Error fetching Yahoo Finance data: {e}")
            return None
    
    def get_industry_data(self, industry: str) -> Optional[Dict]:
        """Get industry-level data"""
        # Yahoo Finance doesn't have direct industry APIs
        # This would need to aggregate from multiple companies
        return None


class NewsAPIClient:
    """Client for NewsAPI"""
    
    def __init__(self):
        self.api_key = settings.NEWS_API_KEY
        self.base_url = "https://newsapi.org/v2"
    
    def get_industry_news(self, industry: str, limit: int = 10) -> List[Dict]:
        """Fetch news articles for a specific industry"""
        if not self.api_key:
            return []
        
        try:
            response = requests.get(
                f"{self.base_url}/everything",
                params={
                    "q": industry,
                    "apiKey": self.api_key,
                    "sortBy": "publishedAt",
                    "pageSize": limit
                }
            )
            response.raise_for_status()
            data = response.json()
            return data.get("articles", [])
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []
    
    def get_company_news(self, company: str, limit: int = 10) -> List[Dict]:
        """Fetch news articles for a specific company"""
        return self.get_industry_news(company, limit)


class CrunchbaseClient:
    """Client for Crunchbase API (placeholder)"""
    
    def __init__(self):
        self.api_key = settings.CRUNCHBASE_API_KEY
        self.base_url = "https://api.crunchbase.com/v4"
    
    def get_company_data(self, company_name: str) -> Optional[Dict]:
        """Fetch company data from Crunchbase"""
        if not self.api_key:
            return None
        
        # Placeholder implementation
        # Crunchbase API requires specific setup
        return None
    
    def get_funding_data(self, company_name: str) -> List[Dict]:
        """Fetch funding data for a company"""
        if not self.api_key:
            return []
        
        # Placeholder implementation
        return []


class FreeDataClient:
    """Client for free data sources (no API keys needed)"""
    
    def get_market_data(self, industry: str) -> Dict:
        """Get market data from free sources"""
        # Use web scraping or public APIs
        try:
            # Example: Use public data sources
            # This is a placeholder - would need actual implementation
            return {
                "industry": industry,
                "source": "public_data"
            }
        except Exception:
            return {}
    
    def get_company_info(self, company: str) -> Optional[Dict]:
        """Get company info from free sources"""
        # Could use Wikipedia, company websites, etc.
        return None


# Initialize clients
news_client = NewsAPIClient()
crunchbase_client = CrunchbaseClient()
yahoo_client = YahooFinanceClient()
free_data_client = FreeDataClient()

