from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredential
from datetime import datetime, date
import jwt
from typing import Optional

from app.config import settings
from app.services.subscription_service import SubscriptionService

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthCredential = Depends(security)):
    """Extract and validate JWT token"""
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_id

async def check_quota(user_id: str = Depends(get_current_user)):
    """Middleware to check subscription quota"""
    subscription_service = SubscriptionService()
    
    # Get user from database
    user = await subscription_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if daily counter needs reset
    await subscription_service.reset_daily_counter_if_needed(user)
    
    # Check quota
    if not await subscription_service.check_quota(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Daily quota exceeded for {user['plan']} plan. Please upgrade or try again tomorrow.",
            headers={"X-Quota-Exceeded": "true"}
        )
    
    return user

async def increment_usage(user: dict = Depends(check_quota)):
    """Increment user's daily request count"""
    subscription_service = SubscriptionService()
    await subscription_service.increment_usage(user)
    return user