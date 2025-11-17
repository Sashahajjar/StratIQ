"""
Strategy generation service
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from models.schemas import StrategyResponse
from services.ai_service import AIService


class StrategyService:
    """Service for generating strategic analyses"""
    
    def __init__(self):
        self.ai_service = AIService()
    
    async def generate_strategy(
        self,
        industry: Optional[str] = None,
        company: Optional[str] = None,
        analysis_type: str = "swot"
    ) -> StrategyResponse:
        """Generate SWOT, PESTEL, or growth recommendations"""
        
        if analysis_type == "swot":
            return await self._generate_swot(industry, company)
        elif analysis_type == "pestel":
            return await self._generate_pestel(industry, company)
        elif analysis_type == "growth":
            return await self._generate_growth_recommendations(industry, company)
        else:
            return await self._generate_swot(industry, company)
    
    async def _generate_swot(
        self,
        industry: Optional[str],
        company: Optional[str]
    ) -> StrategyResponse:
        """Generate SWOT analysis"""
        
        # Get market metrics for analysis
        from services.market_service import MarketService
        market_service = MarketService()
        market_data = await market_service.get_market_data(industry=industry, company=company)
        metrics = market_data.metrics if market_data else {}
        
        context = f"Industry: {industry or 'General'}, Company: {company or 'N/A'}"
        metrics_info = ""
        if metrics:
            growth_rate = metrics.get("growth_rate", 0)
            funding_volume = metrics.get("funding_volume", 0)
            market_size = metrics.get("market_size", 0)
            competition = metrics.get("competition_level", "Medium")
            
            metrics_info = f"""
        Market Metrics:
        - Growth Rate: {growth_rate:.1f}%
        - Funding Volume: ${funding_volume:,.0f}
        - Market Size: ${market_size:,.0f}
        - Competition Level: {competition}
        """
        
        prompt = f"""
        Generate a concise SWOT analysis for the following:
        {context}
        {metrics_info}
        
        Analyze the strengths, weaknesses, opportunities, and threats based on the actual market metrics provided.
        
        Provide a SWOT matrix with:
        - Strengths (exactly 4 items, each 1 sentence, max 15 words) - reference the metrics
        - Weaknesses (exactly 4 items, each 1 sentence, max 15 words) - consider low growth or high competition
        - Opportunities (exactly 4 items, each 1 sentence, max 15 words) - based on market size and growth
        - Threats (exactly 4 items, each 1 sentence, max 15 words) - consider competition level
        
        Also provide exactly 4 strategic recommendations (each 1 sentence, max 20 words) that address the specific metrics.
        
        Keep all items brief and focused. Format as JSON with 'swot' object and 'recommendations' array.
        """
        
        ai_response = await self.ai_service.generate_text(prompt)
        
        # Parse response - actually use AI response
        swot_content, recommendations = self._parse_strategy_response(ai_response, "swot", industry)
        
        # Ensure recommendations exist (use fallback if empty)
        if not recommendations or len(recommendations) == 0:
            # Get fallback recommendations
            industry_recommendations = {
                "Technology": ["Invest in AI and machine learning capabilities", "Focus on cloud-native solutions", "Build strong developer ecosystems", "Prioritize cybersecurity"],
                "Healthcare": ["Leverage telemedicine and digital health", "Invest in personalized medicine", "Focus on regulatory compliance", "Build partnerships with providers"],
                "Finance": ["Embrace digital transformation", "Invest in cybersecurity", "Develop mobile-first solutions", "Explore blockchain applications"],
                "Retail": ["Enhance omnichannel experience", "Invest in supply chain optimization", "Leverage data for personalization", "Focus on sustainability"],
                "Manufacturing": ["Adopt Industry 4.0 technologies", "Invest in automation", "Optimize supply chains", "Focus on sustainability"],
                "Energy": ["Accelerate renewable energy adoption", "Invest in battery technology", "Develop smart grid solutions", "Focus on energy efficiency"],
                "Education": ["Expand online learning offerings", "Focus on skills-based training", "Leverage AI for personalization", "Build partnerships with employers"],
                "Real Estate": ["Adopt PropTech solutions", "Focus on smart buildings", "Invest in sustainability", "Leverage data analytics"],
                "Fashion": ["Embrace sustainable and ethical fashion", "Invest in e-commerce and digital presence", "Leverage influencer and social media marketing", "Focus on personalization and customization"]
            }
            recommendations = industry_recommendations.get(industry or "", [
                "Focus on core strengths", "Explore new market segments", "Invest in innovation", "Build strategic partnerships"
            ])
        
        return StrategyResponse(
            type="swot",
            content=swot_content,
            recommendations=recommendations[:4],  # Limit to 4
            created_at=datetime.now()
        )
    
    async def _generate_pestel(
        self,
        industry: Optional[str],
        company: Optional[str]
    ) -> StrategyResponse:
        """Generate PESTEL analysis"""
        
        context = f"Industry: {industry or 'General'}, Company: {company or 'N/A'}"
        
        prompt = f"""
        Generate a comprehensive PESTEL analysis for the following:
        {context}
        
        Analyze:
        - Political factors
        - Economic factors
        - Social factors
        - Technological factors
        - Environmental factors
        - Legal factors
        
        Provide 3-5 strategic recommendations.
        
        Format as JSON with 'pestel' object and 'recommendations' array.
        """
        
        ai_response = await self.ai_service.generate_text(prompt)
        
        pestel_content, recommendations = self._parse_strategy_response(ai_response, "pestel", industry)
        
        return StrategyResponse(
            type="pestel",
            content=pestel_content,
            recommendations=recommendations,
            created_at=datetime.now()
        )
    
    async def _generate_growth_recommendations(
        self,
        industry: Optional[str],
        company: Optional[str]
    ) -> StrategyResponse:
        """Generate growth recommendations"""
        
        # Get market metrics for analysis
        from services.market_service import MarketService
        market_service = MarketService()
        market_data = await market_service.get_market_data(industry=industry, company=company)
        metrics = market_data.metrics if market_data else {}
        
        context = f"Industry: {industry or 'General'}, Company: {company or 'N/A'}"
        metrics_info = ""
        if metrics:
            growth_rate = metrics.get("growth_rate", 0)
            funding_volume = metrics.get("funding_volume", 0)
            market_size = metrics.get("market_size", 0)
            competition = metrics.get("competition_level", "Medium")
            
            metrics_info = f"""
        Market Metrics:
        - Growth Rate: {growth_rate:.1f}%
        - Funding Volume: ${funding_volume:,.0f}
        - Market Size: ${market_size:,.0f}
        - Competition Level: {competition}
        """
        
        prompt = f"""
        Generate strategic growth recommendations for:
        {context}
        {metrics_info}
        
        Analyze the specific metrics and provide exactly 4-5 strategic recommendations (each 1 sentence, maximum 20 words each).
        
        Focus on:
        - Market opportunities based on the growth rate and market size
        - Growth strategies that leverage the funding volume
        - Risk mitigation considering the competition level
        - Implementation priorities based on the actual metrics
        
        Reference the specific numbers in your recommendations. Keep recommendations concise and actionable. Format as JSON with 'growth' object and 'recommendations' array.
        """
        
        ai_response = await self.ai_service.generate_text(prompt)
        
        growth_content, recommendations = self._parse_strategy_response(ai_response, "growth", industry)
        
        # Ensure recommendations exist (use fallback if empty)
        if not recommendations or len(recommendations) == 0:
            # Get fallback recommendations
            industry_recommendations = {
                "Technology": ["Invest in AI and machine learning capabilities", "Focus on cloud-native solutions", "Build strong developer ecosystems", "Prioritize cybersecurity"],
                "Healthcare": ["Leverage telemedicine and digital health", "Invest in personalized medicine", "Focus on regulatory compliance", "Build partnerships with providers"],
                "Finance": ["Embrace digital transformation", "Invest in cybersecurity", "Develop mobile-first solutions", "Explore blockchain applications"],
                "Retail": ["Enhance omnichannel experience", "Invest in supply chain optimization", "Leverage data for personalization", "Focus on sustainability"],
                "Manufacturing": ["Adopt Industry 4.0 technologies", "Invest in automation", "Optimize supply chains", "Focus on sustainability"],
                "Energy": ["Accelerate renewable energy adoption", "Invest in battery technology", "Develop smart grid solutions", "Focus on energy efficiency"],
                "Education": ["Expand online learning offerings", "Focus on skills-based training", "Leverage AI for personalization", "Build partnerships with employers"],
                "Real Estate": ["Adopt PropTech solutions", "Focus on smart buildings", "Invest in sustainability", "Leverage data analytics"],
                "Fashion": ["Embrace sustainable and ethical fashion", "Invest in e-commerce and digital presence", "Leverage influencer and social media marketing", "Focus on personalization and customization"]
            }
            recommendations = industry_recommendations.get(industry or "", [
                "Focus on core strengths", "Explore new market segments", "Invest in innovation", "Build strategic partnerships"
            ])
        
        return StrategyResponse(
            type="growth",
            content=growth_content,
            recommendations=recommendations[:4],  # Limit to 4
            created_at=datetime.now()
        )
    
    def _parse_strategy_response(
        self,
        response: str,
        analysis_type: str,
        industry: Optional[str] = None
    ) -> tuple:
        """Parse strategy response from AI"""
        # Try to parse the actual AI response first
        parsed_content, parsed_recommendations = self._extract_from_ai_response(response, analysis_type)
        
        if parsed_content and parsed_recommendations:
            return parsed_content, parsed_recommendations
        
        # If AI response exists but parsing failed, try to extract any useful content
        if response and len(response) > 50:
            # Try one more time with more lenient parsing
            parsed_content, parsed_recommendations = self._extract_from_ai_response(response, analysis_type)
            if parsed_content:
                return parsed_content, parsed_recommendations or []
        
        # Only use industry baseline as last resort if AI completely failed
        # Industry-specific SWOT data (baseline templates)
        industry_swot = {
            "Technology": {
                "strengths": ["Rapid innovation cycles", "Strong talent pool", "High scalability"],
                "weaknesses": ["Intense competition", "Rapid obsolescence", "High R&D costs"],
                "opportunities": ["AI/ML adoption", "Cloud migration", "Cybersecurity demand"],
                "threats": ["Regulatory scrutiny", "Talent shortage", "Market saturation"]
            },
            "Healthcare": {
                "strengths": ["Growing demand", "Regulatory protection", "High barriers to entry"],
                "weaknesses": ["Long development cycles", "High compliance costs", "Complex regulations"],
                "opportunities": ["Aging population", "Telemedicine growth", "Personalized medicine"],
                "threats": ["Price pressure", "Regulatory changes", "Data privacy concerns"]
            },
            "Finance": {
                "strengths": ["Digital transformation", "Regulatory framework", "Customer trust"],
                "weaknesses": ["Legacy systems", "Regulatory compliance", "Cybersecurity risks"],
                "opportunities": ["FinTech innovation", "Digital banking", "Cryptocurrency adoption"],
                "threats": ["Regulatory changes", "Cybersecurity threats", "Economic volatility"]
            },
            "Retail": {
                "strengths": ["Omnichannel presence", "Customer data", "Brand recognition"],
                "weaknesses": ["Thin margins", "Inventory management", "Competition from e-commerce"],
                "opportunities": ["E-commerce growth", "Personalization", "Supply chain optimization"],
                "threats": ["Amazon competition", "Changing consumer behavior", "Economic downturns"]
            },
            "Manufacturing": {
                "strengths": ["Operational efficiency", "Supply chain", "Quality control"],
                "weaknesses": ["High capital requirements", "Labor costs", "Environmental regulations"],
                "opportunities": ["Automation", "IoT integration", "Sustainable manufacturing"],
                "threats": ["Supply chain disruptions", "Trade tensions", "Labor shortages"]
            },
            "Energy": {
                "strengths": ["Renewable technology", "Government support", "Growing demand"],
                "weaknesses": ["High initial costs", "Intermittency issues", "Infrastructure needs"],
                "opportunities": ["Energy transition", "Battery technology", "Smart grid"],
                "threats": ["Policy changes", "Fossil fuel competition", "Technology disruption"]
            },
            "Education": {
                "strengths": ["Growing demand", "Technology integration", "Flexible delivery"],
                "weaknesses": ["Quality concerns", "Competition", "Student acquisition costs"],
                "opportunities": ["Online learning", "Skills training", "Lifelong learning"],
                "threats": ["Regulatory changes", "Competition", "Economic downturns"]
            },
            "Real Estate": {
                "strengths": ["Asset value", "Location advantages", "Market knowledge"],
                "weaknesses": ["High capital requirements", "Market cycles", "Maintenance costs"],
                "opportunities": ["PropTech", "Smart buildings", "Sustainable development"],
                "threats": ["Interest rate changes", "Economic downturns", "Regulatory changes"]
            },
            "Fashion": {
                "strengths": ["Brand recognition", "Creative talent", "Global reach"],
                "weaknesses": ["Fast-changing trends", "Inventory management", "Sustainability challenges"],
                "opportunities": ["Sustainable fashion", "E-commerce growth", "Personalization", "Influencer marketing"],
                "threats": ["Economic downturns", "Changing consumer values", "Counterfeit products", "Supply chain disruptions"]
            }
        }
        
        # Get industry-specific content or default
        if analysis_type == "swot":
            if industry and industry in industry_swot:
                content = industry_swot[industry]
            else:
                content = {
                    "strengths": ["Market position", "Innovation", "Team expertise"],
                    "weaknesses": ["Market share", "Competition", "Resources"],
                    "opportunities": ["Market expansion", "New technologies", "Partnerships"],
                    "threats": ["Economic conditions", "Regulatory changes", "Competition"]
                }
        elif analysis_type == "pestel":
            content = {
                "political": ["Regulatory environment", "Government policies"],
                "economic": ["Market conditions", "Economic growth"],
                "social": ["Consumer trends", "Demographic changes"],
                "technological": ["Digital transformation", "Innovation"],
                "environmental": ["Sustainability", "Climate regulations"],
                "legal": ["Compliance requirements", "Data privacy"]
            }
        else:
            content = {
                "opportunities": ["Market expansion", "New segments"],
                "strategies": ["Product diversification", "Innovation"],
                "risks": ["Market volatility", "Competition"]
            }
        
        # Industry-specific recommendations
        industry_recommendations = {
            "Technology": [
                "Invest in AI and machine learning capabilities",
                "Focus on cloud-native solutions",
                "Build strong developer ecosystems",
                "Prioritize cybersecurity"
            ],
            "Healthcare": [
                "Leverage telemedicine and digital health",
                "Invest in personalized medicine",
                "Focus on regulatory compliance",
                "Build partnerships with providers"
            ],
            "Finance": [
                "Embrace digital transformation",
                "Invest in cybersecurity",
                "Develop mobile-first solutions",
                "Explore blockchain applications"
            ],
            "Retail": [
                "Enhance omnichannel experience",
                "Invest in supply chain optimization",
                "Leverage data for personalization",
                "Focus on sustainability"
            ],
            "Manufacturing": [
                "Adopt Industry 4.0 technologies",
                "Invest in automation",
                "Optimize supply chains",
                "Focus on sustainability"
            ],
            "Energy": [
                "Accelerate renewable energy adoption",
                "Invest in battery technology",
                "Develop smart grid solutions",
                "Focus on energy efficiency"
            ],
            "Education": [
                "Expand online learning offerings",
                "Focus on skills-based training",
                "Leverage AI for personalization",
                "Build partnerships with employers"
            ],
            "Real Estate": [
                "Adopt PropTech solutions",
                "Focus on smart buildings",
                "Invest in sustainability",
                "Leverage data analytics"
            ],
            "Fashion": [
                "Embrace sustainable and ethical fashion",
                "Invest in e-commerce and digital presence",
                "Leverage influencer and social media marketing",
                "Focus on personalization and customization",
                "Optimize supply chain and inventory management"
            ]
        }
        
        if industry and industry in industry_recommendations:
            recommendations = industry_recommendations[industry]
        else:
            recommendations = [
                "Focus on core strengths",
                "Explore new market segments",
                "Invest in innovation",
                "Build strategic partnerships"
            ]
        
        return content, recommendations
    
    def _extract_from_ai_response(self, response: str, analysis_type: str) -> tuple:
        """Extract structured data from AI response"""
        import re
        import json
        
        # Try to find JSON in the response
        json_match = re.search(r'\{[^{}]*"swot"[^{}]*\{[^{}]*\}', response, re.DOTALL)
        if not json_match:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
        
        if json_match:
            try:
                data = json.loads(json_match.group())
                if analysis_type == "swot" and "swot" in data:
                    swot = data["swot"]
                    # Truncate SWOT items
                    for key in ["strengths", "weaknesses", "opportunities", "threats"]:
                        if key in swot and isinstance(swot[key], list):
                            swot[key] = [item[:100] if isinstance(item, str) else str(item)[:100] for item in swot[key][:4]]
                    recommendations = [r[:100] if isinstance(r, str) else str(r)[:100] for r in data.get("recommendations", [])[:4]]
                    return swot, recommendations
                elif analysis_type == "pestel" and "pestel" in data:
                    pestel = data["pestel"]
                    recommendations = [r[:100] if isinstance(r, str) else str(r)[:100] for r in data.get("recommendations", [])[:4]]
                    return pestel, recommendations
                elif analysis_type == "growth" and "growth" in data:
                    growth = data["growth"]
                    recommendations = [r[:100] if isinstance(r, str) else str(r)[:100] for r in data.get("recommendations", [])[:4]]
                    return growth, recommendations
            except json.JSONDecodeError:
                pass
        
        # Try to extract from text format
        if analysis_type == "swot":
            strengths = self._extract_list(response, ["Strengths:", "Strengths"])
            weaknesses = self._extract_list(response, ["Weaknesses:", "Weaknesses"])
            opportunities = self._extract_list(response, ["Opportunities:", "Opportunities"])
            threats = self._extract_list(response, ["Threats:", "Threats"])
            recommendations = self._extract_list(response, ["Recommendations:", "Recommendations"])
            
            if strengths or weaknesses or opportunities or threats:
                # Ensure we have at least empty lists
                swot_dict = {
                    "strengths": (strengths or [])[:4],
                    "weaknesses": (weaknesses or [])[:4],
                    "opportunities": (opportunities or [])[:4],
                    "threats": (threats or [])[:4]
                }
                # Truncate recommendations and limit to 4
                recs = [r[:100] for r in (recommendations or [])[:4]]
                return swot_dict, recs
        
        return None, None
    
    def _extract_list(self, text: str, keywords: List[str]) -> List[str]:
        """Extract list items from text after keywords"""
        import re
        items = []
        for keyword in keywords:
            pattern = rf"{re.escape(keyword)}[:\s]*(.*?)(?=\n\s*(?:[A-Z][a-z]+:|$))"
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                content = match.group(1)
                # Extract bullet points or numbered items
                lines = re.findall(r'[-•*]\s*(.+?)(?=\n|$)', content)
                if not lines:
                    lines = re.findall(r'\d+\.\s*(.+?)(?=\n|$)', content)
                items.extend([line.strip()[:100] for line in lines if line.strip()])  # Truncate each item
        return items[:4]  # Limit to 4 items

