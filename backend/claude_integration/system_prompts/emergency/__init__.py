# Sydney Guide - Emergency Prompts Aggregator
# Acil durum prompt'lari toplayan modul

from .lost_tourist import LOST_TOURIST_PROMPT
from .transport_disruption import TRANSPORT_DISRUPTION_PROMPT
from .weather_emergency import WEATHER_EMERGENCY_PROMPT

# Tum acil durum prompt'larini topla
EMERGENCY_PROMPTS = {
    "lost_tourist": LOST_TOURIST_PROMPT,
    "transport_disruption": TRANSPORT_DISRUPTION_PROMPT,
    "weather_emergency": WEATHER_EMERGENCY_PROMPT
}

def get_emergency_prompt(emergency_type: str) -> str:
    """
    Belirtilen acil durum icin prompt dondur
    
    Args:
        emergency_type: Acil durum tipi
        
    Returns:
        str: Acil durum prompt'u veya bos string
    """
    return EMERGENCY_PROMPTS.get(emergency_type, "") 