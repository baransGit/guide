# Sydney Guide - Conversation History Management
# Konusma gecmisi yonetimi

from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Message:
    """Konusma mesaji sinifi"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime
    message_id: str
    session_id: str
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Mesaji dict'e cevir"""
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "message_id": self.message_id,
            "session_id": self.session_id,
            "metadata": self.metadata or {}
        }

class ConversationHistory:
    """Konusma gecmisi yonetim sinifi"""
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.messages: List[Message] = []
        self.max_messages = 100  # Maksimum mesaj sayisi
        
    def add_message(self, role: str, content: str, message_id: str, metadata: Dict[str, Any] = None):
        """Yeni mesaj ekle"""
        message = Message(
            role=role,
            content=content,
            timestamp=datetime.now(),
            message_id=message_id,
            session_id=self.session_id,
            metadata=metadata
        )
        
        self.messages.append(message)
        
        # Mesaj limitini kontrol et
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def get_recent_messages(self, count: int = 10) -> List[Message]:
        """Son mesajlari getir"""
        return self.messages[-count:]
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Konusma ozetini getir"""
        if not self.messages:
            return {"message_count": 0, "summary": "No conversation yet"}
            
        user_messages = [m for m in self.messages if m.role == "user"]
        assistant_messages = [m for m in self.messages if m.role == "assistant"]
        
        return {
            "message_count": len(self.messages),
            "user_message_count": len(user_messages),
            "assistant_message_count": len(assistant_messages),
            "first_message_time": self.messages[0].timestamp.isoformat(),
            "last_message_time": self.messages[-1].timestamp.isoformat(),
            "recent_topics": self._extract_topics()
        }
    
    def _extract_topics(self) -> List[str]:
        """Son mesajlardan konulari cikart"""
        recent_messages = self.get_recent_messages(5)
        topics = []
        
        # Basit konu cikarimi (production'da NLP kullanilacak)
        keywords = ["restaurant", "food", "transport", "attraction", "hotel", "weather"]
        for message in recent_messages:
            for keyword in keywords:
                if keyword.lower() in message.content.lower():
                    if keyword not in topics:
                        topics.append(keyword)
        
        return topics

# Global conversation storage (production'da database kullanilacak)
_conversations: Dict[str, ConversationHistory] = {}

def add_message(session_id: str, role: str, content: str, message_id: str, metadata: Dict[str, Any] = None):
    """Oturuma mesaj ekle"""
    if session_id not in _conversations:
        _conversations[session_id] = ConversationHistory(session_id)
    
    _conversations[session_id].add_message(role, content, message_id, metadata)

def get_conversation_summary(session_id: str) -> Dict[str, Any]:
    """Oturum konusma ozetini getir"""
    if session_id not in _conversations:
        return {"message_count": 0, "summary": "No conversation found"}
    
    return _conversations[session_id].get_conversation_summary() 