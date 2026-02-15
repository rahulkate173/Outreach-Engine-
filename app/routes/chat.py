from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from app.services.memory_service import MemoryService
from app.services.mail_generator import MailGenerator
from app.middleware.rate_limiter import increment_usage
from app.services.subscription_service import SubscriptionService

router = APIRouter()

class ChatMessage(BaseModel):
    chat_id: str
    content: str
    recipient_name: str = ""
    company: str = ""
    job_title: str = ""

class ChatResponse(BaseModel):
    chat_id: str
    message: str
    generated_mail: dict
    quota_remaining: int

memory_service = MemoryService()
mail_generator = MailGenerator()

@router.post("/message", response_model=ChatResponse)
async def send_message(
    request: ChatMessage,
    user: dict = Depends(increment_usage)
):
    """Send chat message and generate outreach email"""
    
    user_id = str(user["_id"])
    chat_id = request.chat_id or await memory_service.create_chat(user_id)
    
    # Add user message to memory
    await memory_service.add_message(user_id, chat_id, "user", request.content)
    
    # Generate cold mail
    mail = await mail_generator.generate_cold_mail(
        recipient_name=request.recipient_name,
        company=request.company,
        job_title=request.job_title,
        context=request.content
    )
    
    # Get context for model
    context = await memory_service.get_context(user_id, chat_id)
    
    # Generate response (using BitNet)
    # For now, return template response
    response_text = f"Generated outreach for {request.recipient_name} at {request.company}"
    
    # Add assistant message to memory
    await memory_service.add_message(user_id, chat_id, "assistant", response_text)
    
    # Get quota status
    subscription_service = SubscriptionService()
    quota_status = await subscription_service.get_quota_status(user)
    
    return {
        "chat_id": chat_id,
        "message": response_text,
        "generated_mail": mail,
        "quota_remaining": quota_status["remaining"]
    }

@router.post("/create-chat")
async def create_chat(user: dict = Depends(increment_usage)):
    """Create new chat session"""
    user_id = str(user["_id"])
    chat_id = await memory_service.create_chat(user_id)
    return {"chat_id": chat_id}