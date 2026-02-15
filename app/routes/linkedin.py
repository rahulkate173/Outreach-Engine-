from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.apify_service import ApifyService
from app.middleware.rate_limiter import increment_usage

router = APIRouter()
apify_service = ApifyService()

class LinkedInAnalysisRequest(BaseModel):
    profile_url: str

@router.post("/analyze")
async def analyze_linkedin(
    request: LinkedInAnalysisRequest,
    user: dict = Depends(increment_usage)
):
    """Analyze LinkedIn profile"""
    
    analysis = await apify_service.analyze_profile(request.profile_url)
    return analysis

@router.get("/insights")
async def get_profile_insights(user: dict = Depends(increment_usage)):
    """Get profile insights"""
    
    return {
        "insights": [
            "Profile analysis feature",
            "Outreach recommendations",
            "LinkedIn integration placeholder"
        ]
    }