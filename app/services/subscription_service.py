from datetime import datetime, date
from app.config import settings
from pymongo import MongoClient
from bson import ObjectId

class SubscriptionService:
    """Service for managing user subscriptions and quotas"""
    
    def __init__(self):
        self.client = MongoClient(settings.mongodb_uri)
        self.db = self.client[settings.mongodb_db]
        self.users_collection = self.db["users"]
    
    async def get_user(self, user_id: str):
        """Get user by ID"""
        try:
            user = self.users_collection.find_one({"_id": ObjectId(user_id)})
            return user
        except:
            return None
    
    async def get_plan_limit(self, plan: str) -> int:
        """Get request limit for a plan"""
        return settings.plan_limits.get(plan.upper(), 3)
    
    async def reset_daily_counter_if_needed(self, user: dict):
        """Reset daily counter if it's a new day"""
        today = date.today().isoformat()
        last_request_date = user.get("last_request_date")
        
        if last_request_date != today:
            self.users_collection.update_one(
                {"_id": user["_id"]},
                {
                    "$set": {
                        "daily_requests": 0,
                        "last_request_date": today
                    }
                }
            )
    
    async def check_quota(self, user: dict) -> bool:
        """Check if user has remaining quota"""
        plan = user.get("plan", "FREE")
        limit = await self.get_plan_limit(plan)
        daily_requests = user.get("daily_requests", 0)
        
        # BUSINESS plan has no limits
        if plan == "BUSINESS":
            return True
        
        return daily_requests < limit
    
    async def increment_usage(self, user: dict):
        """Increment user's daily request count"""
        self.users_collection.update_one(
            {"_id": user["_id"]},
            {"$inc": {"daily_requests": 1}}
        )
    
    async def get_quota_status(self, user: dict) -> dict:
        """Get user's quota status"""
        plan = user.get("plan", "FREE")
        limit = await self.get_plan_limit(plan)
        daily_requests = user.get("daily_requests", 0)
        
        return {
            "plan": plan,
            "daily_limit": limit,
            "daily_requests": daily_requests,
            "remaining": max(0, limit - daily_requests),
            "quota_exceeded": daily_requests >= limit
        }
    
    async def upgrade_plan(self, user_id: str, new_plan: str) -> bool:
        """Upgrade user's plan"""
        if new_plan not in settings.plan_limits:
            return False
        
        result = self.users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"plan": new_plan.upper()}}
        )
        
        return result.modified_count > 0