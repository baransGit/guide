# Sydney Guide - Session State Management
# Oturum durumu yonetimi

from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum

class SessionState(Enum):
    """Oturum durumu enum'u"""
    ACTIVE = "active"
    IDLE = "idle"
    EXPIRED = "expired"
    TERMINATED = "terminated"

class Session:
    """Kullanici oturumu sinifi"""
    def __init__(self, session_id: str, user_id: Optional[str] = None):
        self.session_id = session_id
        self.user_id = user_id
        self.state = SessionState.ACTIVE
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.context_data = {}
        self.conversation_count = 0
        
    def to_dict(self) -> Dict[str, Any]:
        """Oturum bilgilerini dict'e cevir"""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "state": self.state.value,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "context_data": self.context_data,
            "conversation_count": self.conversation_count
        }

# Global session storage (production'da Redis kullanilacak)
_sessions: Dict[str, Session] = {}

def create_session(session_id: str, user_id: Optional[str] = None) -> Session:
    """Yeni oturum olustur"""
    session = Session(session_id, user_id)
    _sessions[session_id] = session
    return session

def get_session(session_id: str) -> Optional[Session]:
    """Oturum bilgilerini getir"""
    return _sessions.get(session_id)

def update_session(session_id: str, **kwargs) -> bool:
    """Oturum bilgilerini guncelle"""
    session = _sessions.get(session_id)
    if not session:
        return False
        
    session.last_activity = datetime.now()
    for key, value in kwargs.items():
        if hasattr(session, key):
            setattr(session, key, value)
        else:
            session.context_data[key] = value
    
    return True 