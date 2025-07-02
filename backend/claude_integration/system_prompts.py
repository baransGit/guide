# Sydney Guide - System Prompts for Claude
# Claude'un kisilik, rol ve temel talimatlarini tanimlayan sistem prompt'lari

# Import from the system_prompts subdirectory __init__.py
from .system_prompts import (
    SYDNEY_GUIDE_SYSTEM_PROMPT,
    LANGUAGE_SPECIFIC_PROMPTS,
    SCENARIO_PROMPTS,
    EMERGENCY_PROMPTS,
    get_language_prompt,
    get_scenario_prompt,
    get_emergency_prompt,
    get_system_prompt,
    get_localized_prompt,
    get_food_explorer_prompt,
    get_first_time_visitor_prompt,
    get_emergency_prompt_for_situation
)

# Backward compatibility icin tum fonksiyonlari export et
__all__ = [
    'SYDNEY_GUIDE_SYSTEM_PROMPT',
    'LANGUAGE_SPECIFIC_PROMPTS',
    'SCENARIO_PROMPTS',
    'EMERGENCY_PROMPTS',
    'get_language_prompt',
    'get_scenario_prompt',
    'get_emergency_prompt',
    'get_system_prompt',
    'get_localized_prompt',
    'get_food_explorer_prompt',
    'get_first_time_visitor_prompt',
    'get_emergency_prompt_for_situation'
] 