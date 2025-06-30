# Sydney Guide - Conversation Patterns for Claude
# Claude icin konusma desenleri
# FULLY MODULARIZED: Now imports from conversation_patterns/ subdirectory

from typing import Dict, Any, List, Optional

# Import everything from the modular conversation_patterns package
from .conversation_patterns import (
    # States
    ConversationState,
    STATE_TRANSITIONS, 
    get_next_state,
    
    # Patterns
    CONVERSATION_PATTERNS,
    get_conversation_pattern,
    get_fallback_action,
    
    # Flows
    CONVERSATION_FLOWS,
    get_conversation_flow,
    
    # Templates
    RESPONSE_TEMPLATES,
    format_response_template,
    
    # Utils
    detect_conversation_intent
)

# Re-export everything for backward compatibility
__all__ = [
    # States
    'ConversationState',
    'STATE_TRANSITIONS', 
    'get_next_state',
    
    # Patterns
    'CONVERSATION_PATTERNS',
    'get_conversation_pattern',
    'get_fallback_action',
    
    # Flows
    'CONVERSATION_FLOWS',
    'get_conversation_flow',
    
    # Templates
    'RESPONSE_TEMPLATES',
    'format_response_template',
    
    # Utils
    'detect_conversation_intent'
] 