# Sydney Guide - Conversation States and Transitions
# Konusma durumlari ve gecisleri

from enum import Enum
from typing import Dict

class ConversationState(Enum):
    """Konusma durumu enum'u"""
    GREETING = "greeting"
    LOCATION_REQUEST = "location_request"
    PREFERENCE_GATHERING = "preference_gathering"
    SEARCHING = "searching"
    RECOMMENDING = "recommending"
    JOURNEY_PLANNING = "journey_planning"
    TRACKING_OFFERED = "tracking_offered"
    EMERGENCY = "emergency"
    COMPLETED = "completed"

# Konusma durumu gecisleri
STATE_TRANSITIONS = {
    ConversationState.GREETING: {
        "food_request": ConversationState.PREFERENCE_GATHERING,
        "location_question": ConversationState.LOCATION_REQUEST,
        "journey_request": ConversationState.JOURNEY_PLANNING,
        "emergency": ConversationState.EMERGENCY
    },
    ConversationState.LOCATION_REQUEST: {
        "permission_granted": ConversationState.SEARCHING,
        "permission_denied": ConversationState.PREFERENCE_GATHERING,
        "manual_input": ConversationState.PREFERENCE_GATHERING
    },
    ConversationState.PREFERENCE_GATHERING: {
        "preferences_clear": ConversationState.SEARCHING,
        "need_clarification": ConversationState.PREFERENCE_GATHERING,
        "emergency": ConversationState.EMERGENCY
    },
    ConversationState.SEARCHING: {
        "results_found": ConversationState.RECOMMENDING,
        "no_results": ConversationState.PREFERENCE_GATHERING,
        "error": ConversationState.PREFERENCE_GATHERING
    },
    ConversationState.RECOMMENDING: {
        "satisfied": ConversationState.COMPLETED,
        "need_directions": ConversationState.JOURNEY_PLANNING,
        "need_alternatives": ConversationState.SEARCHING
    },
    ConversationState.JOURNEY_PLANNING: {
        "route_planned": ConversationState.TRACKING_OFFERED,
        "need_alternatives": ConversationState.JOURNEY_PLANNING,
        "completed": ConversationState.COMPLETED
    },
    ConversationState.TRACKING_OFFERED: {
        "tracking_accepted": ConversationState.COMPLETED,
        "tracking_declined": ConversationState.COMPLETED
    },
    ConversationState.EMERGENCY: {
        "resolved": ConversationState.COMPLETED,
        "escalated": ConversationState.EMERGENCY
    }
}

def get_next_state(current_state: ConversationState, trigger: str) -> ConversationState:
    """
    Mevcut durumdan sonraki durumu belirle
    
    Args:
        current_state: Şu anki konusma durumu
        trigger: Durum degisikligini tetikleyen olay
        
    Returns:
        ConversationState: Sonraki durum
    """
    transitions = STATE_TRANSITIONS.get(current_state, {})
    return transitions.get(trigger, current_state) 