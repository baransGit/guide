# Sydney Guide - Context Management for Claude
# Claude icin baglam yonetimi  
# FULLY MODULARIZED: Now imports from context_management/ subdirectory

from typing import Dict, Any, List, Optional

# Import everything from the modular context_management package
from .context_management import (
    # Session Management
    SessionState, create_session, get_session, update_session,
    ConversationHistory, add_message, get_conversation_summary,
    UserPreferences, save_preferences, get_user_preferences,
    
    # Location Management  
    LocationTracker, update_location, get_current_location
)

# Re-export everything for backward compatibility
__all__ = [
    # Session Management
    'SessionState', 'create_session', 'get_session', 'update_session',
    'ConversationHistory', 'add_message', 'get_conversation_summary', 
    'UserPreferences', 'save_preferences', 'get_user_preferences',
    
    # Location Management
    'LocationTracker', 'update_location', 'get_current_location'
]
