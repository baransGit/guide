# Sydney Guide - Conversation Patterns Base
# Konusma desenleri taban sinifi ve toplayici

from typing import Dict, Any, List, Optional
from .restaurant import RESTAURANT_PATTERN, ConversationPattern
from .journey import JOURNEY_PATTERN
from .attractions import ATTRACTIONS_PATTERN
from .emergency import EMERGENCY_PATTERN
from .exploration import EXPLORATION_PATTERN

# Tum konusma desenlerini topla
CONVERSATION_PATTERNS = {
    "restaurant_discovery": RESTAURANT_PATTERN,
    "journey_planning": JOURNEY_PATTERN,
    "attraction_discovery": ATTRACTIONS_PATTERN,
    "emergency_assistance": EMERGENCY_PATTERN,
    "general_exploration": EXPLORATION_PATTERN
}

def get_conversation_pattern(pattern_name: str) -> Optional[ConversationPattern]:
    """
    Belirtilen isimde konusma deseni dondur
    
    Args:
        pattern_name: Desen ismi
        
    Returns:
        ConversationPattern veya None
    """
    return CONVERSATION_PATTERNS.get(pattern_name)

def get_fallback_action(pattern_name: str, step: str) -> List[str]:
    """
    Belirtilen desen ve adim icin yedek aksiyonlari dondur
    
    Args:
        pattern_name: Desen ismi
        step: Adim ismi
        
    Returns:
        List[str]: Yedek aksiyonlar listesi
    """
    pattern = get_conversation_pattern(pattern_name)
    if pattern:
        return pattern.fallback_actions
    return ["provide_general_help", "ask_for_clarification"] 