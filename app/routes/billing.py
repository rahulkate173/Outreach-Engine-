from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from bson import ObjectId
from pymongo import MongoClient

from app.config import settings
from app.middleware.rate_limiter import get_current_user
from app.services.subscription_service import SubscriptionService
from app.models.user_model import QuotaStatus, PlanUpgrade

router = APIRouter()
subscription_service = SubscriptionService()

@router.get("/quota", response_model=QuotaStatus)
async def get_quota(user: dict = Depends(get_current_user)):
    """Get user's quota status"""
    quota_status = await subscription_service.get_quota_status(user)
    return quota_status

@router.get("/plans")
async def get_plans():
    """Get available plans"""
    return {
        "plans": [
            {
                "name": "FREE",
                "daily_limit": 3,
                "price": 0,
                "features": ["3 requests/day", "Basic features"]
            },
            {
                "name": "PRO",
                "daily_limit": 200,
                "price": 29,
                "features": ["200 requests/day", "Advanced features"]
            },
            {
                "name": "ULTRA",
                "daily_limit": 1000,
                "price": 99,
                "features": ["1000 requests/day", "Premium support"]
            },
            {
                "name": "BUSINESS",
                "daily_limit": 999999,
                "price": "contact",
                "features": ["Unlimited requests", "Dedicated support", "Custom integration"]
            }
        ]
    }

@router.post("/upgrade")
async def upgrade_plan(upgrade: PlanUpgrade, user_id: str = Depends(get_current_user)):
    """Upgrade user plan"""
    
    success = await subscription_service.upgrade_plan(user_id, upgrade.new_plan)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Plan upgrade failed"
        )
    
    return {
        "status": "upgraded",
        "new_plan": upgrade.new_plan,
        "message": f"Successfully upgraded to {upgrade.new_plan} plan"
    }