"""
RapidAPI clients for real market and company data
"""

import requests
import os
from typing import Dict, List, Optional
from utils.config import settings


class RapidAPIClient:
    """Base client for RapidAPI services"""
    
    def __init__(self, api_key: str = None, host: str = None):
        self.api_key = api_key or settings.RAPIDAPI_KEY
        self.host = host or settings.RAPIDAPI_HOST
        self.base_headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host
        } if self.api_key else {}
    
    def _make_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        """Make a request to RapidAPI"""
        if not self.api_key:
            return None
        
        try:
            response = requests.get(url, headers=self.base_headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"RapidAPI error: {e}")
            return None


class AlphaVantageClient(RapidAPIClient):
    """Client for Alpha Vantage API (stock market data)"""
    
    def __init__(self):
        # Allow custom host or use default
        host = os.getenv("ALPHA_VANTAGE_HOST", "alpha-vantage.p.rapidapi.com")
        super().__init__(settings.RAPIDAPI_KEY, host)
        self.base_url = f"https://{host}"
        self.host = host
        self.base_headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host
        } if self.api_key else {}
    
    def get_company_overview(self, symbol: str) -> Optional[Dict]:
        """Get company overview data"""
        if not self.api_key:
            return None
        
        url = f"{self.base_url}/query"
        params = {
            "function": "OVERVIEW",
            "symbol": symbol,
            "datatype": "json"
        }
        return self._make_request(url, params)
    
    def get_income_statement(self, symbol: str) -> Optional[Dict]:
        """Get company income statement"""
        if not self.api_key:
            return None
        
        url = f"{self.base_url}/query"
        params = {
            "function": "INCOME_STATEMENT",
            "symbol": symbol,
            "datatype": "json"
        }
        return self._make_request(url, params)


class YahooFinanceRapidClient(RapidAPIClient):
    """Client for Yahoo Finance via RapidAPI"""
    
    def __init__(self):
        host = os.getenv("YAHOO_FINANCE_HOST", "yahoo-finance15.p.rapidapi.com")
        super().__init__(settings.RAPIDAPI_KEY, host)
        self.base_url = f"https://{host}"
        self.host = host
        self.base_headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host
        } if self.api_key else {}
    
    def get_stock_info(self, symbol: str) -> Optional[Dict]:
        """Get stock information"""
        if not self.api_key:
            return None
        
        url = f"{self.base_url}/api/v1/markets/stock/info"
        params = {"ticker": symbol}
        return self._make_request(url, params)
    
    def get_market_summary(self) -> Optional[Dict]:
        """Get market summary"""
        if not self.api_key:
            return None
        
        url = f"{self.base_url}/api/v1/markets/summary"
        return self._make_request(url)


class MarketDataClient(RapidAPIClient):
    """Client for general market data APIs"""
    
    def __init__(self):
        super().__init__()
        # Can be configured for different market data APIs
        self.base_url = "https://market-data-api.p.rapidapi.com"
        self.host = "market-data-api.p.rapidapi.com"
        self.base_headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host
        } if self.api_key else {}
    
    def get_industry_data(self, industry: str) -> Optional[Dict]:
        """Get industry-level market data"""
        if not self.api_key:
            return None
        
        # This would depend on the specific API endpoint
        # Placeholder for now
        return None


class CrunchbaseRapidClient(RapidAPIClient):
    """Client for Crunchbase via RapidAPI"""
    
    def __init__(self):
        host = os.getenv("CRUNCHBASE_HOST", "crunchbase-crunchbase-com.p.rapidapi.com")
        super().__init__(settings.RAPIDAPI_KEY, host)
        self.base_url = f"https://{host}"
        self.host = host
        self.base_headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host
        } if self.api_key else {}
    
    def get_company_data(self, company_name: str) -> Optional[Dict]:
        """Get company data from Crunchbase"""
        if not self.api_key:
            return None
        
        url = f"{self.base_url}/v4/searches/organizations"
        params = {"query": company_name}
        return self._make_request(url, params)


# Initialize clients
alpha_vantage_client = AlphaVantageClient()
yahoo_rapid_client = YahooFinanceRapidClient()
market_data_client = MarketDataClient()
crunchbase_rapid_client = CrunchbaseRapidClient()

