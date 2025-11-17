"""
Market data service
"""

from typing import Optional, Dict, Any
from models.schemas import MarketDataResponse
from utils.api_clients import news_client, crunchbase_client, yahoo_client, free_data_client
from utils.rapidapi_clients import alpha_vantage_client, yahoo_rapid_client, market_data_client, crunchbase_rapid_client
from datetime import datetime


class MarketService:
    """Service for fetching and processing market data"""
    
    async def get_market_data(
        self,
        industry: Optional[str] = None,
        company: Optional[str] = None,
        timeframe: str = "1y"
    ) -> MarketDataResponse:
        """Fetch market data for industry or company"""
        
        # Fetch news data
        news = []
        if industry:
            news = news_client.get_industry_news(industry, limit=10)
        elif company:
            news = news_client.get_company_news(company, limit=10)
        
        # Fetch real market metrics from APIs
        metrics = await self._fetch_real_metrics(industry, company, news)
        
        # Prepare data structure
        data = {
            "timeframe": timeframe,
            "timestamp": datetime.now().isoformat(),
            "sources": ["newsapi", "crunchbase"]
        }
        
        return MarketDataResponse(
            industry=industry,
            company=company,
            data=data,
            news=news,
            metrics=metrics
        )
    
    async def _fetch_real_metrics(
        self,
        industry: Optional[str],
        company: Optional[str],
        news: list = None
    ) -> Dict[str, Any]:
        """Fetch real metrics from APIs and free sources"""
        
        # Try RapidAPI sources first (most reliable)
        if company:
            # Try Alpha Vantage for stock data
            if alpha_vantage_client.api_key:
                try:
                    # Try to get stock symbol from company name
                    symbol = self._company_to_symbol(company)
                    if symbol:
                        overview = alpha_vantage_client.get_company_overview(symbol)
                        if overview and overview.get("MarketCapitalization"):
                            market_cap = float(overview.get("MarketCapitalization", 0))
                            revenue_growth = float(overview.get("QuarterlyRevenueGrowthYOY", 0)) * 100 if overview.get("QuarterlyRevenueGrowthYOY") else 0
                            
                            return {
                                "growth_rate": revenue_growth or float(overview.get("EPSGrowth", 0)) * 100 if overview.get("EPSGrowth") else 0,
                                "funding_volume": int(market_cap * 0.1),  # Estimate from market cap
                                "top_sectors": [overview.get("Sector", ""), overview.get("Industry", "")],
                                "market_size": int(market_cap),
                                "competition_level": "Very High" if market_cap > 100000000000 else "High" if market_cap > 10000000000 else "Medium",
                                "data_source": "real_time_api",
                                "source_api": "alpha_vantage"
                            }
                except Exception as e:
                    print(f"Alpha Vantage error: {e}")
            
            # Try Yahoo Finance RapidAPI
            if yahoo_rapid_client.api_key:
                try:
                    symbol = self._company_to_symbol(company)
                    if symbol:
                        stock_info = yahoo_rapid_client.get_stock_info(symbol)
                        if stock_info and stock_info.get("marketCap"):
                            return {
                                "growth_rate": stock_info.get("revenueGrowth", 0) * 100 if stock_info.get("revenueGrowth") else 0,
                                "funding_volume": int(stock_info.get("marketCap", 0) * 0.1),
                                "top_sectors": [stock_info.get("sector", ""), stock_info.get("industry", "")],
                                "market_size": int(stock_info.get("marketCap", 0)),
                                "competition_level": "High",
                                "data_source": "real_time_api",
                                "source_api": "yahoo_finance_rapid"
                            }
                except Exception as e:
                    print(f"Yahoo RapidAPI error: {e}")
            
            # Try Crunchbase RapidAPI
            if crunchbase_rapid_client.api_key:
                try:
                    cb_data = crunchbase_rapid_client.get_company_data(company)
                    if cb_data:
                        # Parse Crunchbase response structure
                        entities = cb_data.get("entities", [])
                        if entities:
                            entity = entities[0]
                            return {
                                "growth_rate": entity.get("growth_rate", 0),
                                "funding_volume": entity.get("total_funding_usd", 0),
                                "top_sectors": entity.get("categories", []),
                                "market_size": entity.get("valuation_usd", 0),
                                "competition_level": "High",
                                "data_source": "real_time_api",
                                "source_api": "crunchbase_rapid"
                            }
                except Exception as e:
                    print(f"Crunchbase RapidAPI error: {e}")
        
        # Try free Yahoo Finance (fallback)
        if company:
            try:
                yahoo_data = yahoo_client.get_company_data(company)
                if yahoo_data and yahoo_data.get("market_cap"):
                    return {
                        "growth_rate": yahoo_data.get("growth_rate", 0),
                        "funding_volume": int(yahoo_data.get("revenue", 0) * 0.1),
                        "top_sectors": [yahoo_data.get("sector", ""), yahoo_data.get("industry", "")],
                        "market_size": yahoo_data.get("market_cap", 0),
                        "competition_level": "High" if yahoo_data.get("market_cap", 0) > 1000000000 else "Medium",
                        "data_source": "real_time_api",
                        "source_api": "yahoo_finance_free"
                    }
            except Exception as e:
                print(f"Yahoo Finance error: {e}")
        
        # Try industry-level data from RapidAPI
        if industry and market_data_client.api_key:
            try:
                industry_data = market_data_client.get_industry_data(industry)
                if industry_data:
                    return {
                        "growth_rate": industry_data.get("growth_rate", 0),
                        "funding_volume": industry_data.get("funding_volume", 0),
                        "top_sectors": industry_data.get("sectors", []),
                        "market_size": industry_data.get("market_size", 0),
                        "competition_level": industry_data.get("competition_level", "Medium")
                    }
            except Exception as e:
                print(f"Market data API error: {e}")
        
        # Try to aggregate real company data for industry metrics
        if industry:
            aggregated_metrics = await self._aggregate_industry_from_companies(industry)
            if aggregated_metrics:
                return aggregated_metrics
        
        # Calculate metrics from available data sources
        # Use industry baselines with adjustments based on news volume
        base_metrics = self._get_industry_baseline(industry)
        
        if news and len(news) > 0:
            # Adjust metrics based on news volume (more news = more activity)
            news_factor = min(len(news) / 10.0, 1.5)  # Cap at 1.5x
            return {
                "growth_rate": base_metrics["growth_rate"] * news_factor,
                "funding_volume": int(base_metrics["funding_volume"] * news_factor),
                "top_sectors": base_metrics["top_sectors"],
                "market_size": int(base_metrics["market_size"] * news_factor),
                "competition_level": base_metrics["competition_level"],
                "data_source": "estimated_fallback",
                "source_api": "industry_baseline_with_news_adjustment",
                "note": "⚠️ Estimated values based on 2024 market research, adjusted by news volume. Real-time API data unavailable."
            }
        
        # Return baseline metrics if no news available
        base_metrics["data_source"] = "estimated_fallback"
        base_metrics["source_api"] = "industry_baseline"
        base_metrics["note"] = "⚠️ Estimated values based on 2024 market research. Real-time API data unavailable."
        return base_metrics
    
    def _get_industry_baseline(self, industry: Optional[str]) -> Dict[str, Any]:
        """Get baseline metrics for an industry (ESTIMATED FALLBACK DATA)
        
        ⚠️  WARNING: These are ESTIMATED industry averages based on 2024 market research.
        Used as fallback when real-time API data is unavailable.
        These values are NOT real-time and should be clearly marked as estimates.
        """
        baselines = {
            "Technology": {
                "growth_rate": 12.5,  # ⚠️ ESTIMATED: Tech sector average growth (2024)
                "funding_volume": 45000000000,  # ⚠️ ESTIMATED: $45B annual VC funding in tech
                "top_sectors": ["Software", "AI", "Cloud", "SaaS"],  # ⚠️ ESTIMATED
                "market_size": 8500000000000,  # ⚠️ ESTIMATED: $8.5T global tech market
                "competition_level": "Very High",
                "data_source": "estimated_fallback",
                "note": "⚠️ Estimated values - fallback data when APIs unavailable"
            },
            "Healthcare": {
                "growth_rate": 8.5,  # ⚠️ ESTIMATED: Healthcare sector growth
                "funding_volume": 32000000000,  # ⚠️ ESTIMATED: $32B annual healthcare funding
                "top_sectors": ["Biotech", "Digital Health", "Pharma", "MedTech"],  # ⚠️ ESTIMATED
                "market_size": 12000000000000,  # ⚠️ ESTIMATED: $12T global healthcare market
                "competition_level": "High",
                "data_source": "estimated_fallback",
                "note": "⚠️ Estimated values - fallback data when APIs unavailable"
            },
            "Finance": {
                "growth_rate": 9.2,  # ⚠️ ESTIMATED: FinTech growth rate
                "funding_volume": 28000000000,  # ⚠️ ESTIMATED: $28B annual FinTech funding
                "top_sectors": ["FinTech", "Banking", "Insurance", "Payments"],  # ⚠️ ESTIMATED
                "market_size": 28000000000000,  # ⚠️ ESTIMATED: $28T global financial services
                "competition_level": "Very High",
                "data_source": "estimated_fallback",
                "note": "⚠️ Estimated values - fallback data when APIs unavailable"
            },
            "Retail": {
                "growth_rate": 6.8,  # ⚠️ ESTIMATED: Retail sector growth
                "funding_volume": 18000000000,  # ⚠️ ESTIMATED: $18B annual retail/e-commerce funding
                "top_sectors": ["E-commerce", "Consumer Goods", "Marketplace"],  # ⚠️ ESTIMATED
                "market_size": 32000000000000,  # ⚠️ ESTIMATED: $32T global retail market
                "competition_level": "Very High",
                "data_source": "estimated_fallback",
                "note": "⚠️ Estimated values - fallback data when APIs unavailable"
            },
            "Manufacturing": {
                "growth_rate": 4.5,  # ⚠️ ESTIMATED: Manufacturing growth
                "funding_volume": 8500000000,  # ⚠️ ESTIMATED: $8.5B annual manufacturing tech funding
                "top_sectors": ["Industrial", "Automation", "IoT", "3D Printing"],  # ⚠️ ESTIMATED
                "market_size": 15000000000000,  # ⚠️ ESTIMATED: $15T global manufacturing
                "competition_level": "High",
                "data_source": "estimated_fallback",
                "note": "⚠️ Estimated values - fallback data when APIs unavailable"
            },
            "Energy": {
                "growth_rate": 11.5,  # ⚠️ ESTIMATED: Energy sector growth (renewables driving)
                "funding_volume": 42000000000,  # ⚠️ ESTIMATED: $42B annual energy funding
                "top_sectors": ["Renewable", "Solar", "Battery", "CleanTech"],  # ⚠️ ESTIMATED
                "market_size": 8000000000000,  # ⚠️ ESTIMATED: $8T global energy market
                "competition_level": "High",
                "data_source": "estimated_fallback",
                "note": "⚠️ Estimated values - fallback data when APIs unavailable"
            },
            "Education": {
                "growth_rate": 9.8,  # ⚠️ ESTIMATED: EdTech growth
                "funding_volume": 12000000000,  # ⚠️ ESTIMATED: $12B annual EdTech funding
                "top_sectors": ["EdTech", "Online Learning", "Corporate Training"],  # ⚠️ ESTIMATED
                "market_size": 2800000000000,  # ⚠️ ESTIMATED: $2.8T global education market
                "competition_level": "Medium",
                "data_source": "estimated_fallback",
                "note": "⚠️ Estimated values - fallback data when APIs unavailable"
            },
            "Real Estate": {
                "growth_rate": 5.2,  # ⚠️ ESTIMATED: Real estate growth
                "funding_volume": 15000000000,  # ⚠️ ESTIMATED: $15B annual PropTech funding
                "top_sectors": ["PropTech", "Commercial", "Residential", "iBuying"],  # ⚠️ ESTIMATED
                "market_size": 35000000000000,  # ⚠️ ESTIMATED: $35T global real estate
                "competition_level": "Medium",
                "data_source": "estimated_fallback",
                "note": "⚠️ Estimated values - fallback data when APIs unavailable"
            },
            "Fashion": {
                "growth_rate": 7.5,  # ⚠️ ESTIMATED: Fashion industry growth
                "funding_volume": 8500000000,  # ⚠️ ESTIMATED: $8.5B annual fashion tech funding
                "top_sectors": ["Apparel", "E-commerce", "Sustainable Fashion", "Luxury"],  # ⚠️ ESTIMATED
                "market_size": 3200000000000,  # ⚠️ ESTIMATED: $3.2T global fashion market
                "competition_level": "Very High",
                "data_source": "estimated_fallback",
                "note": "⚠️ Estimated values - fallback data when APIs unavailable"
            }
        }
        
        if industry and industry in baselines:
            return baselines[industry]
        
        # Default baseline for unknown industries
        return {
            "growth_rate": 8.0,
            "funding_volume": 200000000,
            "top_sectors": ["General"],
            "market_size": 3000000000,
            "competition_level": "Medium",
            "data_source": "estimated_fallback",
            "source_api": "default_baseline",
            "note": "⚠️ Estimated default values. Industry-specific data unavailable."
        }
    
    async def _aggregate_industry_from_companies(self, industry: str) -> Optional[Dict[str, Any]]:
        """Aggregate real company data to calculate industry metrics"""
        # Industry representative companies (top companies in each sector)
        industry_companies = {
            "Technology": ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA"],
            "Healthcare": ["JNJ", "UNH", "PFE", "ABBV", "TMO", "ABT"],
            "Finance": ["JPM", "BAC", "WFC", "GS", "MS", "C"],
            "Retail": ["WMT", "TGT", "HD", "COST", "LOW", "TJX"],
            "Manufacturing": ["CAT", "DE", "GE", "HON", "EMR", "ITW"],
            "Energy": ["XOM", "CVX", "COP", "SLB", "EOG", "MPC"],
            "Education": ["CHGG", "LRN", "GS", "TAL", "EDU"],
            "Real Estate": ["AMT", "PLD", "EQIX", "PSA", "WELL", "SPG"],
            "Fashion": ["NKE", "LULU", "RL", "PVH", "VFC", "HBI"]
        }
        
        if industry not in industry_companies:
            return None
        
        symbols = industry_companies[industry]
        company_data_list = []
        total_market_cap = 0
        total_growth = 0
        sectors = set()
        valid_count = 0
        
        # Fetch data for representative companies
        for symbol in symbols[:5]:  # Limit to 5 to avoid rate limits
            try:
                # Try Alpha Vantage first
                if alpha_vantage_client.api_key:
                    overview = alpha_vantage_client.get_company_overview(symbol)
                    if overview and overview.get("MarketCapitalization"):
                        market_cap = float(overview.get("MarketCapitalization", 0))
                        growth = float(overview.get("QuarterlyRevenueGrowthYOY", 0)) * 100 if overview.get("QuarterlyRevenueGrowthYOY") else 0
                        sector = overview.get("Sector", "")
                        
                        total_market_cap += market_cap
                        if growth > 0:
                            total_growth += growth
                            valid_count += 1
                        if sector:
                            sectors.add(sector)
                        company_data_list.append({
                            "market_cap": market_cap,
                            "growth": growth,
                            "sector": sector
                        })
                        continue
                
                # Try Yahoo Finance RapidAPI
                if yahoo_rapid_client.api_key:
                    stock_info = yahoo_rapid_client.get_stock_info(symbol)
                    if stock_info and stock_info.get("marketCap"):
                        market_cap = float(stock_info.get("marketCap", 0))
                        growth = stock_info.get("revenueGrowth", 0) * 100 if stock_info.get("revenueGrowth") else 0
                        sector = stock_info.get("sector", "")
                        
                        total_market_cap += market_cap
                        if growth > 0:
                            total_growth += growth
                            valid_count += 1
                        if sector:
                            sectors.add(sector)
                        company_data_list.append({
                            "market_cap": market_cap,
                            "growth": growth,
                            "sector": sector
                        })
                        continue
                
                # Try free Yahoo Finance
                yahoo_data = yahoo_client.get_company_data(symbol)
                if yahoo_data and yahoo_data.get("market_cap"):
                    market_cap = yahoo_data.get("market_cap", 0)
                    growth = yahoo_data.get("growth_rate", 0)
                    sector = yahoo_data.get("sector", "")
                    
                    total_market_cap += market_cap
                    if growth > 0:
                        total_growth += growth
                        valid_count += 1
                    if sector:
                        sectors.add(sector)
                    company_data_list.append({
                        "market_cap": market_cap,
                        "growth": growth,
                        "sector": sector
                    })
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")
                continue
        
        # If we got enough data, calculate industry metrics
        if len(company_data_list) >= 2:
            avg_growth = total_growth / valid_count if valid_count > 0 else 0
            # Use the baseline market size as a reference, but adjust based on real company data
            # The aggregated market cap represents top companies, so we use it as a lower bound
            baseline = self._get_industry_baseline(industry)
            baseline_market_size = baseline.get("market_size", total_market_cap * 2)
            
            # Use the larger of: baseline or aggregated (scaled up by 2x to account for smaller companies)
            estimated_industry_size = max(baseline_market_size, total_market_cap * 2)
            
            return {
                "growth_rate": round(avg_growth, 1) if avg_growth > 0 else baseline.get("growth_rate", 0),
                "funding_volume": int(total_market_cap * 0.1) if total_market_cap > 0 else baseline.get("funding_volume", 0),
                "top_sectors": list(sectors)[:3] if sectors else baseline.get("top_sectors", []),
                "market_size": int(estimated_industry_size),
                "competition_level": "Very High" if total_market_cap > 5000000000000 else "High" if total_market_cap > 1000000000000 else baseline.get("competition_level", "Medium"),
                "data_source": "aggregated_real_data" if avg_growth > 0 else "estimated_fallback",
                "source_api": "company_aggregation",
                "note": "Aggregated from real company data" if avg_growth > 0 else "Using estimated baseline (API unavailable)"
            }
        
        return None
    
    def _company_to_symbol(self, company: str) -> Optional[str]:
        """Convert company name to stock symbol"""
        # Common company to symbol mappings
        company_symbols = {
            "apple": "AAPL",
            "microsoft": "MSFT",
            "google": "GOOGL",
            "amazon": "AMZN",
            "meta": "META",
            "tesla": "TSLA",
            "nvidia": "NVDA",
            "netflix": "NFLX",
            "salesforce": "CRM",
            "oracle": "ORCL",
            "ibm": "IBM",
            "intel": "INTC",
            "adobe": "ADBE",
            "paypal": "PYPL",
            "visa": "V",
            "mastercard": "MA",
            "jpmorgan": "JPM",
            "bank of america": "BAC",
            "walmart": "WMT",
            "target": "TGT",
            "nike": "NKE",
            "starbucks": "SBUX",
        }
        
        company_lower = company.lower().strip()
        # Direct match
        if company_lower in company_symbols:
            return company_symbols[company_lower]
        
        # Partial match
        for key, symbol in company_symbols.items():
            if key in company_lower or company_lower in key:
                return symbol
        
        # If company name looks like a symbol (all caps, short)
        if len(company) <= 5 and company.isupper():
            return company
        
        return None
    
    def _generate_sample_metrics(
        self,
        industry: Optional[str],
        company: Optional[str]
    ) -> Dict[str, Any]:
        """DEPRECATED: Generate sample metrics - use _fetch_real_metrics instead"""
        
        # Industry-specific metrics (fallback only)
        industry_metrics = {
            "Technology": {
                "growth_rate": 18.5,
                "funding_volume": 450000000,
                "top_sectors": ["AI", "SaaS", "Cloud Computing"],
                "market_size": 8000000000,
                "competition_level": "Very High"
            },
            "Healthcare": {
                "growth_rate": 12.3,
                "funding_volume": 320000000,
                "top_sectors": ["Telemedicine", "Biotech", "Digital Health"],
                "market_size": 6000000000,
                "competition_level": "High"
            },
            "Finance": {
                "growth_rate": 15.8,
                "funding_volume": 380000000,
                "top_sectors": ["FinTech", "Blockchain", "Digital Banking"],
                "market_size": 7000000000,
                "competition_level": "High"
            },
            "Retail": {
                "growth_rate": 8.2,
                "funding_volume": 180000000,
                "top_sectors": ["E-commerce", "Omnichannel", "Supply Chain"],
                "market_size": 4000000000,
                "competition_level": "Very High"
            },
            "Manufacturing": {
                "growth_rate": 6.5,
                "funding_volume": 150000000,
                "top_sectors": ["Automation", "IoT", "Smart Manufacturing"],
                "market_size": 3500000000,
                "competition_level": "Medium"
            },
            "Energy": {
                "growth_rate": 14.7,
                "funding_volume": 420000000,
                "top_sectors": ["Renewable Energy", "Battery Tech", "Smart Grid"],
                "market_size": 5500000000,
                "competition_level": "High"
            },
            "Education": {
                "growth_rate": 10.4,
                "funding_volume": 220000000,
                "top_sectors": ["EdTech", "Online Learning", "Skills Training"],
                "market_size": 3000000000,
                "competition_level": "Medium"
            },
            "Real Estate": {
                "growth_rate": 7.8,
                "funding_volume": 200000000,
                "top_sectors": ["PropTech", "Smart Buildings", "Virtual Tours"],
                "market_size": 4500000000,
                "competition_level": "Medium"
            },
            "Fashion": {
                "growth_rate": 11.2,
                "funding_volume": 280000000,
                "top_sectors": ["Sustainable Fashion", "E-commerce", "Fast Fashion", "Luxury"],
                "market_size": 4800000000,
                "competition_level": "Very High"
            }
        }
        
        # Return industry-specific metrics or default
        if industry and industry in industry_metrics:
            return industry_metrics[industry]
        elif industry:
            # Generic metrics for unknown industries
            return {
                "growth_rate": 10.0,
                "funding_volume": 200000000,
                "top_sectors": ["Innovation", "Digital Transformation"],
                "market_size": 3000000000,
                "competition_level": "Medium"
            }
        else:
            # Default metrics
            return {
                "growth_rate": 15.5,
                "funding_volume": 250000000,
                "top_sectors": ["AI", "SaaS", "FinTech"],
                "market_size": 5000000000,
                "competition_level": "High"
            }

