# Sydney Guide - Conversation Flows Aggregator
# Konusma akislari toplayici

from .restaurant_flow import RESTAURANT_SEARCH_FLOW
from .journey_flow import JOURNEY_PLANNING_FLOW  
from .attraction_flow import ATTRACTION_DISCOVERY_FLOW

# Tum konusma akislarini topla
CONVERSATION_FLOWS = {
    "restaurant_search_flow": RESTAURANT_SEARCH_FLOW,
    "journey_planning_flow": JOURNEY_PLANNING_FLOW,
    "attraction_discovery_flow": ATTRACTION_DISCOVERY_FLOW
}

def get_conversation_flow(flow_name: str):
    """
    Belirtilen isimde konusma akisi dondur
    
    Args:
        flow_name: Akis ismi
        
    Returns:
        dict veya None
    """
    return CONVERSATION_FLOWS.get(flow_name) 