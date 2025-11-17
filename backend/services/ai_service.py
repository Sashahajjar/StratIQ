"""
AI service using LangChain with OpenAI or Groq (free alternative)
"""

try:
    from langchain_openai import ChatOpenAI
except ImportError:
    ChatOpenAI = None

try:
    from langchain_groq import ChatGroq
except ImportError:
    ChatGroq = None

from utils.config import settings
from typing import Optional


class AIService:
    """Service for AI text generation using OpenAI or Groq (free)"""
    
    def __init__(self):
        self.llm = None
        self.provider = None
        
        # Try OpenAI first if key is available
        if settings.OPENAI_API_KEY:
            try:
                self.llm = ChatOpenAI(
                    model="gpt-4o",
                    temperature=0.7,
                    api_key=settings.OPENAI_API_KEY
                )
                self.provider = "openai"
                print("✅ Using OpenAI GPT-4o")
            except Exception as e:
                print(f"⚠️ OpenAI failed: {e}")
                # Try gpt-3.5-turbo as fallback
                try:
                    self.llm = ChatOpenAI(
                        model="gpt-3.5-turbo",
                        temperature=0.7,
                        api_key=settings.OPENAI_API_KEY
                    )
                    self.provider = "openai"
                    print("✅ Using OpenAI GPT-3.5-turbo")
                except Exception:
                    self.llm = None
        
        # If OpenAI not available, try Groq (FREE)
        if not self.llm and ChatGroq and settings.GROQ_API_KEY:
            try:
                # Groq offers free tier with fast inference
                self.llm = ChatGroq(
                    model="llama-3.3-70b-versatile",  # Current free model on Groq
                    temperature=0.7,
                    groq_api_key=settings.GROQ_API_KEY
                )
                self.provider = "groq"
                print("✅ Using Groq (FREE) - llama-3.3-70b-versatile")
            except Exception as e:
                print(f"⚠️ Groq failed: {e}")
                self.llm = None
        
        if not self.llm:
            print("⚠️ No AI provider available - using fallback templates")
    
    async def generate_text(self, prompt: str) -> str:
        """Generate text using OpenAI"""
        
        if not self.llm:
            # Return sample response if API key not configured
            return self._get_sample_response(prompt)
        
        try:
            response = await self.llm.ainvoke(prompt)
            content = response.content if hasattr(response, 'content') else str(response)
            print(f"✅ AI response generated ({self.provider})")
            return content
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error generating AI text ({self.provider}): {error_msg[:200]}")
            
            # If OpenAI fails (quota, invalid key, or any error), try Groq if available
            if self.provider == "openai" and ChatGroq and settings.GROQ_API_KEY:
                print("🔄 Switching to Groq (FREE) due to OpenAI error...")
                try:
                    groq_llm = ChatGroq(
                        model="llama-3.3-70b-versatile",
                        temperature=0.7,
                        groq_api_key=settings.GROQ_API_KEY
                    )
                    response = await groq_llm.ainvoke(prompt)
                    content = response.content if hasattr(response, 'content') else str(response)
                    print("✅ Successfully used Groq (FREE)")
                    return content
                except Exception as groq_error:
                    print(f"⚠️ Groq also failed: {groq_error}")
            
            # Return fallback
            return self._get_sample_response(prompt)
    
    def _get_sample_response(self, prompt: str) -> str:
        """Return sample response when AI is not configured"""
        if "SWOT" in prompt or "swot" in prompt.lower():
            return """
            SWOT Analysis:
            
            Strengths:
            - Strong market position
            - Innovative technology stack
            - Experienced leadership team
            
            Weaknesses:
            - Limited market share
            - High competition
            - Resource constraints
            
            Opportunities:
            - Market expansion potential
            - Emerging technologies
            - Strategic partnerships
            
            Threats:
            - Economic uncertainty
            - Regulatory changes
            - Intense competition
            
            Recommendations:
            1. Focus on core strengths
            2. Explore new market segments
            3. Invest in innovation
            """
        elif "PESTEL" in prompt or "pestel" in prompt.lower():
            return """
            PESTEL Analysis:
            
            Political: Stable regulatory environment
            Economic: Growing market conditions
            Social: Changing consumer preferences
            Technological: Rapid AI adoption
            Environmental: Sustainability focus
            Legal: Data privacy regulations
            
            Recommendations:
            1. Monitor regulatory changes
            2. Invest in sustainable practices
            3. Leverage technological advances
            """
        else:
            return """
            Executive Summary:
            The market analysis reveals significant growth opportunities in the technology sector.
            Key trends include increased adoption of AI and cloud technologies, along with
            growing demand for digital transformation solutions.
            
            Key Takeaways:
            - Market growth rate of 15.5% annually
            - Strong funding activity in AI and SaaS sectors
            - Increasing competition requires differentiation
            - Opportunities in emerging markets
            - Focus on innovation and partnerships
            """

