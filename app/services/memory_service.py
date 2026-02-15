import json
import os
from pathlib import Path
from datetime import datetime
from uuid import uuid4
from typing import List, Dict, Optional

class MemoryService:
    """Service for managing conversation memory (file-based)"""
    
    def __init__(self, memory_dir: str = "./memory"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
    
    def get_user_dir(self, user_id: str) -> Path:
        """Get user's memory directory"""
        user_dir = self.memory_dir / user_id
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir
    
    async def create_chat(self, user_id: str) -> str:
        """Create new chat session"""
        chat_id = str(uuid4())
        user_dir = self.get_user_dir(user_id)
        chat_file = user_dir / f"{chat_id}.json"
        
        chat_data = {
            "chat_id": chat_id,
            "messages": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        with open(chat_file, "w") as f:
            json.dump(chat_data, f, indent=2)
        
        return chat_id
    
    async def add_message(self, user_id: str, chat_id: str, role: str, content: str):
        """Add message to chat"""
        user_dir = self.get_user_dir(user_id)
        chat_file = user_dir / f"{chat_id}.json"
        
        if not chat_file.exists():
            # Create chat if doesn't exist
            await self.create_chat(user_id)
        
        with open(chat_file, "r") as f:
            chat_data = json.load(f)
        
        chat_data["messages"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        chat_data["updated_at"] = datetime.now().isoformat()
        
        with open(chat_file, "w") as f:
            json.dump(chat_data, f, indent=2)
    
    async def get_chat(self, user_id: str, chat_id: str) -> Optional[Dict]:
        """Get chat history"""
        user_dir = self.get_user_dir(user_id)
        chat_file = user_dir / f"{chat_id}.json"
        
        if not chat_file.exists():
            return None
        
        with open(chat_file, "r") as f:
            return json.load(f)
    
    async def list_chats(self, user_id: str) -> List[Dict]:
        """List all chats for user"""
        user_dir = self.get_user_dir(user_id)
        chats = []
        
        for chat_file in sorted(user_dir.glob("*.json"), reverse=True):
            with open(chat_file, "r") as f:
                chat_data = json.load(f)
                chats.append({
                    "chat_id": chat_data["chat_id"],
                    "created_at": chat_data["created_at"],
                    "updated_at": chat_data["updated_at"],
                    "message_count": len(chat_data["messages"]),
                    "preview": chat_data["messages"][0]["content"][:50] if chat_data["messages"] else ""
                })
        
        return chats
    
    async def delete_chat(self, user_id: str, chat_id: str) -> bool:
        """Delete chat"""
        user_dir = self.get_user_dir(user_id)
        chat_file = user_dir / f"{chat_id}.json"
        
        if chat_file.exists():
            chat_file.unlink()
            return True
        return False
    
    async def get_context(self, user_id: str, chat_id: str) -> str:
        """Get formatted context for model input"""
        chat_data = await self.get_chat(user_id, chat_id)
        if not chat_data:
            return ""
        
        context = ""
        for msg in chat_data["messages"]:
            role = msg["role"].upper()
            content = msg["content"]
            context += f"{role}: {content}\n"
        
        return context