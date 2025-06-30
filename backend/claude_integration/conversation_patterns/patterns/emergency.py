# Sydney Guide - Emergency Assistance Pattern
# Acil durum yardimi konusma deseni

from typing import List

class ConversationPattern:
    """Konusma deseni sinifi"""
    
    def __init__(self, name: str, description: str, steps: List[str], 
                 required_tools: List[str], fallback_actions: List[str]):
        self.name = name
        self.description = description
        self.steps = steps
        self.required_tools = required_tools
        self.fallback_actions = fallback_actions

EMERGENCY_PATTERN = ConversationPattern(
    name="emergency_assistance",
    description="Kullanici kaybolmus veya acil yardima ihtiyaci var",
    steps=[
        "assess_emergency_level",
        "get_current_location_urgently",
        "provide_immediate_guidance",
        "find_nearest_help",
        "offer_continuous_support",
        "connect_to_services"
    ],
    required_tools=[
        "get_current_location",
        "search_places",
        "send_notification"
    ],
    fallback_actions=[
        "provide_emergency_numbers",
        "guide_to_landmark",
        "connect_to_human_help",
        "use_alternative_location_methods"
    ]
) 