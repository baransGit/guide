# Sydney Guide - System Prompts Module
# Sistem prompt'lari modulu

from .core_identity import SYDNEY_GUIDE_SYSTEM_PROMPT
from .languages import LANGUAGE_SPECIFIC_PROMPTS, get_language_prompt
from .scenarios import SCENARIO_PROMPTS, get_scenario_prompt
from .emergency import EMERGENCY_PROMPTS, get_emergency_prompt
from .utils import (
    get_system_prompt,
    get_localized_prompt,
    get_food_explorer_prompt,
    get_first_time_visitor_prompt,
    get_emergency_prompt_for_situation
)

# Tum ana fonksiyonlari export et
__all__ = [
    # Core
    'SYDNEY_GUIDE_SYSTEM_PROMPT',
    
    # Collections
    'LANGUAGE_SPECIFIC_PROMPTS',
    'SCENARIO_PROMPTS', 
    'EMERGENCY_PROMPTS',
    
    # Getters
    'get_language_prompt',
    'get_scenario_prompt',
    'get_emergency_prompt',
    
    # Main functions
    'get_system_prompt',
    'get_localized_prompt',
    'get_food_explorer_prompt',
    'get_first_time_visitor_prompt',
    'get_emergency_prompt_for_situation'
] 