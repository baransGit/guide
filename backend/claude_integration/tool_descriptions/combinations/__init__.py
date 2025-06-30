# Sydney Guide - Tool Combinations Aggregator
# Arac kombinasyonlarini toplayan modul

from .restaurant_finding import RESTAURANT_FINDING_COMBINATION
from .journey_planning import JOURNEY_PLANNING_COMBINATION
from .attraction_exploration import ATTRACTION_EXPLORATION_COMBINATION
from .transport_assistance import TRANSPORT_ASSISTANCE_COMBINATION

# Tum arac kombinasyonlari
TOOL_COMBINATIONS = {
    "find_nearby_restaurant": RESTAURANT_FINDING_COMBINATION,
    "plan_complete_journey": JOURNEY_PLANNING_COMBINATION,
    "explore_attractions": ATTRACTION_EXPLORATION_COMBINATION,
    "transport_assistance": TRANSPORT_ASSISTANCE_COMBINATION
}

def get_recommended_tools_for_scenario(scenario: str) -> list:
    """
    Belirtilen senaryo icin onerilen araclari dondur
    
    Args:
        scenario: Kullanim senaryosu
        
    Returns:
        list: Onerilen arac adlari listesi
    """
    return TOOL_COMBINATIONS.get(scenario, []) 