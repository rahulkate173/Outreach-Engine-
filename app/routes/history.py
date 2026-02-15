from fastapi import APIRouter, Depends, HTTPException, status
from app.services.memory_service import MemoryService
from app.middleware.rate_limiter import get_current_user
from bson import ObjectId

router = APIRouter()
memory_service = MemoryService()

@router.get("/chats")
async def list_chats(user_id: str = Depends(get_current_user)):
    """List all chats for user"""
    chats = await memory_service.list_chats(user_id)
    return {"chats": chats}

@router.get("/chat/{chat_id}")
async def get_chat(chat_id: str, user_id: str = Depends(get_current_user)):
    """Get specific chat"""
    chat = await memory_service.get_chat(user_id, chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    return chat

@router.delete("/chat/{chat_id}")
async def delete_chat(chat_id: str, user_id: str = Depends(get_current_user)):
    """Delete chat"""
    success = await memory_service.delete_chat(user_id, chat_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    return {"status": "deleted"}