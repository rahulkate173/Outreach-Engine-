from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timedelta
import jwt
import bcrypt
from pymongo import MongoClient
from bson import ObjectId

from app.config import settings
from app.models.user_model import UserCreate, UserLogin, TokenResponse, UserResponse

router = APIRouter()

# MongoDB connection
client = MongoClient(settings.mongodb_uri)
db = client[settings.mongodb_db]
users_collection = db["users"]

def hash_password(password: str) -> str:
    """Hash password with bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hash_password: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode(), hash_password.encode())

def create_access_token(user_id: str, expires_delta: timedelta = None):
    """Create JWT token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    
    to_encode = {"sub": str(user_id), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

@router.post("/register", response_model=TokenResponse)
async def register(user: UserCreate):
    """Register new user"""
    
    # Check if user exists
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    new_user = {
        "email": user.email,
        "password_hash": hash_password(user.password),
        "plan": "FREE",
        "daily_requests": 0,
        "last_request_date": None,
        "created_at": datetime.utcnow()
    }
    
    result = users_collection.insert_one(new_user)
    user_id = result.inserted_id
    
    # Create token
    access_token = create_access_token(user_id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user_id),
            "email": user.email,
            "plan": "FREE",
            "daily_requests": 0,
            "created_at": new_user["created_at"]
        }
    }

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """Login user"""
    
    # Find user
    user = users_collection.find_one({"email": credentials.email})
    if not user or not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create token
    access_token = create_access_token(user["_id"])
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "email": user["email"],
            "plan": user["plan"],
            "daily_requests": user["daily_requests"],
            "created_at": user["created_at"]
        }
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user(user_id: str):
    """Get current user info"""
    from app.middleware.rate_limiter import get_current_user
    
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "plan": user["plan"],
        "daily_requests": user["daily_requests"],
        "created_at": user["created_at"]
    }