# Sydney Guide - Scenario-Specific Prompts Aggregator
# Senaryo-spesifik prompt'lari toplayan modul

from .first_time_visitor import FIRST_TIME_VISITOR_PROMPT
from .food_explorer import FOOD_EXPLORER_PROMPT
from .budget_traveler import BUDGET_TRAVELER_PROMPT
from .family_with_kids import FAMILY_WITH_KIDS_PROMPT
from .business_traveler import BUSINESS_TRAVELER_PROMPT

# Tum senaryo prompt'larini topla
SCENARIO_PROMPTS = {
    "first_time_visitor": FIRST_TIME_VISITOR_PROMPT,
    "food_explorer": FOOD_EXPLORER_PROMPT,
    "budget_traveler": BUDGET_TRAVELER_PROMPT,
    "family_with_kids": FAMILY_WITH_KIDS_PROMPT,
    "business_traveler": BUSINESS_TRAVELER_PROMPT
}

def get_scenario_prompt(scenario: str) -> str:
    """
    Belirtilen senaryo icin prompt dondur
    
    Args:
        scenario: Senaryo adi
        
    Returns:
        str: Senaryo-spesifik prompt veya bos string
    """
    return SCENARIO_PROMPTS.get(scenario, "") 