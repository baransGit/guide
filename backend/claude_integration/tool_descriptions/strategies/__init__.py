# Sydney Guide - Tool Usage Strategies Aggregator
# Arac kullanim stratejilerini toplayan modul

from .location_first import LOCATION_FIRST_STRATEGY
from .comprehensive_search import COMPREHENSIVE_SEARCH_STRATEGY
from .journey_planning import JOURNEY_PLANNING_STRATEGY
from .proactive_assistance import PROACTIVE_ASSISTANCE_STRATEGY

# Tum strateji tanimlari
TOOL_USAGE_STRATEGIES = {
    "location_first": LOCATION_FIRST_STRATEGY,
    "comprehensive_search": COMPREHENSIVE_SEARCH_STRATEGY,
    "journey_planning": JOURNEY_PLANNING_STRATEGY,
    "proactive_assistance": PROACTIVE_ASSISTANCE_STRATEGY
}

def get_usage_strategy(strategy_name: str) -> dict:
    """
    Belirtilen strateji icin kullanim desenini dondur
    
    Args:
        strategy_name: Strateji adi
        
    Returns:
        dict: Strateji aciklamasi ve deseni
    """
    return TOOL_USAGE_STRATEGIES.get(strategy_name, {}) 