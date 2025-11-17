"""
Insight generation service using LangChain and OpenAI
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from models.schemas import InsightResponse
from services.ai_service import AIService


class InsightService:
    """Service for generating AI insights"""
    
    def __init__(self):
        self.ai_service = AIService()
    
    async def generate_insights(
        self,
        industry: Optional[str] = None,
        company: Optional[str] = None,
        data: Dict[str, Any] = {}
    ) -> InsightResponse:
        """Generate AI-written summaries and key takeaways"""
        
        # Prepare context
        context = self._prepare_context(industry, company, data)
        
        # Generate summary using AI with actual metrics analysis
        metrics_info = ""
        if data:
            growth_rate = data.get("growth_rate", 0)
            funding_volume = data.get("funding_volume", 0)
            market_size = data.get("market_size", 0)
            competition = data.get("competition_level", "Medium")
            
            metrics_info = f"""
        Market Metrics:
        - Growth Rate: {growth_rate:.1f}%
        - Funding Volume: ${funding_volume:,.0f}
        - Market Size: ${market_size:,.0f}
        - Competition Level: {competition}
        
        Analyze these specific numbers and provide insights based on the actual data.
        """
        
        prompt = f"""
        Analyze the following business data and provide a concise summary with key takeaways.
        
        Context:
        {context}
        {metrics_info}
        
        Provide:
        1. A brief executive summary (2-3 sentences, maximum 200 words) that references the specific metrics above
        2. Exactly 5-7 key takeaways as bullet points (each takeaway should be 1 sentence, maximum 20 words each) that analyze the actual numbers
        
        Focus on interpreting the growth rate, funding volume, and market size. Compare them to industry standards if relevant.
        Keep responses concise and focused. Format as JSON with 'summary' and 'key_takeaways' fields.
        """
        
        ai_response = await self.ai_service.generate_text(prompt)
        
        # Parse response - use actual AI response
        summary, takeaways = self._parse_ai_response(ai_response, industry)
        
        # Ensure takeaways exist (use fallback if empty)
        if not takeaways or len(takeaways) == 0:
            # Get fallback takeaways
            industry_takeaways = {
                "Technology": ["AI and machine learning are transforming business operations", "Cloud adoption continues to accelerate", "Cybersecurity is a critical priority", "Remote work technologies are in high demand", "Developer tools and platforms are key differentiators"],
                "Healthcare": ["Telemedicine adoption is accelerating", "Personalized medicine is the future", "Regulatory compliance is essential", "Data privacy and security are paramount", "Partnerships with providers are crucial"],
                "Finance": ["Digital banking is becoming the norm", "FinTech partnerships are essential", "Cybersecurity is a top priority", "Regulatory technology (RegTech) is growing", "Customer experience is key differentiator"],
                "Retail": ["Omnichannel experience is essential", "E-commerce continues to grow", "Supply chain optimization is key", "Personalization drives customer loyalty", "Sustainability is increasingly important"],
                "Manufacturing": ["Automation is transforming operations", "IoT integration is accelerating", "Supply chain resilience is critical", "Sustainability is a key focus", "Skills training is essential"],
                "Energy": ["Renewable energy adoption is accelerating", "Battery technology is critical", "Smart grid solutions are emerging", "Energy efficiency is a priority", "Government support is strong"],
                "Education": ["Online learning is here to stay", "Skills-based training is in demand", "Personalization improves outcomes", "Partnerships with employers are valuable", "Technology integration is essential"],
                "Real Estate": ["PropTech is transforming the industry", "Smart buildings are the future", "Data analytics drive decisions", "Sustainability is a key focus", "Tenant experience matters"],
                "Fashion": ["Sustainable fashion is gaining momentum", "E-commerce and omnichannel are essential", "Social media and influencer marketing drive sales", "Personalization enhances customer experience", "Fast fashion faces sustainability challenges"]
            }
            takeaways = industry_takeaways.get(industry or "", [
                "Market trends are evolving", "Innovation is key", "Customer focus is essential", "Digital transformation is critical", "Strategic partnerships matter"
            ])
        
        return InsightResponse(
            summary=summary or "Industry analysis reveals key trends and opportunities.",
            key_takeaways=takeaways[:7],  # Limit to 7
            created_at=datetime.now()
        )
    
    async def get_insight(self, insight_id: int) -> Optional[Dict[str, Any]]:
        """Get insight by ID (placeholder)"""
        # In production, fetch from database
        return None
    
    def _prepare_context(
        self,
        industry: Optional[str],
        company: Optional[str],
        data: Dict[str, Any]
    ) -> str:
        """Prepare context string for AI"""
        context_parts = []
        
        if industry:
            context_parts.append(f"Industry: {industry}")
        if company:
            context_parts.append(f"Company: {company}")
        if data:
            context_parts.append(f"Data: {data}")
        
        return "\n".join(context_parts)
    
    def _parse_ai_response(self, response: str, industry: Optional[str] = None) -> tuple:
        """Parse AI response into summary and takeaways"""
        import re
        import json
        
        # Try to extract JSON first
        json_match = re.search(r'\{[^{}]*"summary"[^{}]*\}', response, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group())
                if "summary" in data and "key_takeaways" in data:
                    return data["summary"], data["key_takeaways"]
            except json.JSONDecodeError:
                pass
        
        # Parse from text format
        lines = response.split("\n")
        summary = ""
        takeaways = []
        
        # Look for summary section
        summary_keywords = ["Executive Summary", "Summary", "Analysis"]
        in_summary = False
        in_takeaways = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect summary section
            if any(keyword in line for keyword in summary_keywords):
                in_summary = True
                in_takeaways = False
                # Remove the keyword and continue
                for kw in summary_keywords:
                    line = line.replace(kw, "").strip(": ").strip()
                if line:
                    summary += line + " "
                continue
            
            # Detect takeaways section
            if "takeaway" in line.lower() or "key point" in line.lower():
                in_takeaways = True
                in_summary = False
                continue
            
            # Collect summary
            if in_summary and not in_takeaways:
                if line.startswith("-") or line.startswith("•") or line.startswith("*"):
                    in_summary = False
                    in_takeaways = True
                    takeaways.append(line.lstrip("- •*").strip())
                else:
                    summary += line + " "
            
            # Collect takeaways
            elif in_takeaways or line.startswith("-") or line.startswith("•") or line.startswith("*"):
                item = line.lstrip("- •*").strip()
                if item and len(item) > 10:  # Filter out very short items
                    takeaways.append(item)
        
        # If we have a response but no structured parsing, use the whole response
        if not summary and response:
            # Split response into summary and takeaways
            paragraphs = [p.strip() for p in response.split("\n\n") if p.strip()]
            if paragraphs:
                summary = paragraphs[0][:300]  # Limit summary to 300 chars
                # Remaining paragraphs as takeaways
                for para in paragraphs[1:]:
                    if len(para) > 20:
                        takeaways.append(para[:100])  # Limit each takeaway to 100 chars
        
        # Use fallback only if we truly have nothing from AI
        # But also use fallback if response is too short or clearly a sample
        if (not summary and not takeaways) or (response and len(response) < 100):
            industry_insights = {
                "Technology": {
                    "summary": "The technology sector is experiencing rapid growth driven by AI, cloud computing, and digital transformation. Companies are investing heavily in innovation to stay competitive in an increasingly digital world.",
                    "takeaways": [
                        "AI and machine learning are transforming business operations",
                        "Cloud adoption continues to accelerate",
                        "Cybersecurity is a critical priority",
                        "Remote work technologies are in high demand",
                        "Developer tools and platforms are key differentiators"
                    ]
                },
                "Healthcare": {
                    "summary": "The healthcare industry is undergoing digital transformation with telemedicine, personalized medicine, and digital health solutions gaining traction. Regulatory compliance and patient data security remain critical concerns.",
                    "takeaways": [
                        "Telemedicine adoption is accelerating",
                        "Personalized medicine is the future",
                        "Regulatory compliance is essential",
                        "Data privacy and security are paramount",
                        "Partnerships with providers are crucial"
                    ]
                },
                "Finance": {
                    "summary": "The financial services sector is embracing digital transformation with FinTech innovations, digital banking, and blockchain technologies reshaping traditional banking models.",
                    "takeaways": [
                        "Digital banking is becoming the norm",
                        "FinTech partnerships are essential",
                        "Cybersecurity is a top priority",
                        "Regulatory technology (RegTech) is growing",
                        "Customer experience is key differentiator"
                    ]
                },
                "Retail": {
                    "summary": "Retail is evolving with omnichannel strategies, e-commerce growth, and supply chain optimization becoming critical for success in a competitive market.",
                    "takeaways": [
                        "Omnichannel experience is essential",
                        "E-commerce continues to grow",
                        "Supply chain optimization is key",
                        "Personalization drives customer loyalty",
                        "Sustainability is increasingly important"
                    ]
                },
                "Manufacturing": {
                    "summary": "Manufacturing is adopting Industry 4.0 technologies including automation, IoT, and smart manufacturing to improve efficiency and competitiveness.",
                    "takeaways": [
                        "Automation is transforming operations",
                        "IoT integration is accelerating",
                        "Supply chain resilience is critical",
                        "Sustainability is a key focus",
                        "Skills training is essential"
                    ]
                },
                "Energy": {
                    "summary": "The energy sector is transitioning to renewable sources with solar, wind, and battery technologies driving innovation and sustainability initiatives.",
                    "takeaways": [
                        "Renewable energy adoption is accelerating",
                        "Battery technology is critical",
                        "Smart grid solutions are emerging",
                        "Energy efficiency is a priority",
                        "Government support is strong"
                    ]
                },
                "Education": {
                    "summary": "Education is embracing online learning, skills-based training, and personalized learning experiences to meet evolving student needs and market demands.",
                    "takeaways": [
                        "Online learning is here to stay",
                        "Skills-based training is in demand",
                        "Personalization improves outcomes",
                        "Partnerships with employers are valuable",
                        "Technology integration is essential"
                    ]
                },
                "Real Estate": {
                    "summary": "Real estate is adopting PropTech solutions, smart buildings, and data analytics to improve efficiency, sustainability, and tenant experiences.",
                    "takeaways": [
                        "PropTech is transforming the industry",
                        "Smart buildings are the future",
                        "Data analytics drive decisions",
                        "Sustainability is a key focus",
                        "Tenant experience matters"
                    ]
                },
                "Fashion": {
                    "summary": "The fashion industry is experiencing digital transformation with e-commerce growth, sustainable fashion initiatives, and personalized shopping experiences reshaping consumer behavior and brand strategies.",
                    "takeaways": [
                        "Sustainable fashion is gaining momentum",
                        "E-commerce and omnichannel are essential",
                        "Social media and influencer marketing drive sales",
                        "Personalization enhances customer experience",
                        "Fast fashion faces sustainability challenges",
                        "Supply chain transparency is increasingly important"
                    ]
                }
            }
            
            if industry and industry in industry_insights:
                fallback = industry_insights[industry]
                if not summary:
                    summary = fallback["summary"]
                if not takeaways:
                    takeaways = fallback["takeaways"]
            else:
                if not summary:
                    summary = response[:500] if response else "Industry analysis reveals key trends and opportunities."
                if not takeaways:
                    takeaways = ["Market trends are evolving", "Innovation is key", "Customer focus is essential"]
        
        # Truncate summary if too long
        summary = summary.strip()[:300] if summary else ""
        
        # Limit takeaways to 7 and truncate each if too long
        takeaways = [t[:100] for t in takeaways[:7]]
        
        return summary, takeaways

