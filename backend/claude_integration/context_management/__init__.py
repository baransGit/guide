# Sydney Guide - Context Management Main Aggregator  
# Baglam yonetimi ana toplama modulu

from typing import Dict, Any, List, Optional

# Import session management
from .session import (
    SessionState, create_session, get_session, update_session,
    ConversationHistory, add_message, get_conversation_summary,
    UserPreferences, save_preferences, get_user_preferences
)

# Import location management  
from .location import (
    LocationTracker, update_location, get_current_location
)

# Re-export everything for backward compatibility
__all__ = [
    # Session Management
    'SessionState', 'create_session', 'get_session', 'update_session',
    'ConversationHistory', 'add_message', 'get_conversation_summary',
    'UserPreferences', 'save_preferences', 'get_user_preferences',
    
    # Location Management
    'LocationTracker', 'update_location', 'get_current_location',
    'LocationHistory', 'add_location_point', 'get_location_history',
    'GeofenceManager', 'create_geofence', 'check_geofence_triggers',
    
    # Journey Management
    'JourneyState', 'start_journey', 'update_journey_progress', 'complete_journey',
    'RouteContext', 'save_route_context', 'get_route_context',
    'TransportContext', 'update_transport_status', 'get_transport_updates',
    
    # Memory Management
    'ShortTermMemory', 'add_to_short_term', 'get_short_term_context',
    'LongTermMemory', 'save_to_long_term', 'get_user_patterns',
    'compress_context', 'summarize_conversation',
    
    # Utilities
    'create_context_snapshot', 'merge_context_data',
    'clean_expired_context', 'validate_context_data'
] 