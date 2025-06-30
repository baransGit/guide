# Sydney Guide - Restaurant Discovery Pattern
# Restoran kesfi konusma deseni

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

RESTAURANT_PATTERN = ConversationPattern(
    name="restaurant_discovery",
    description="Kullanici restoran ararken izlenecek konusma akisi",
    steps=[
        "greet_and_understand_food_preference",
        "request_location_permission", 
        "get_current_location",
        "gather_specific_preferences",
        "search_restaurants",
        "present_recommendations",
        "offer_detailed_info",
        "suggest_journey_planning"
    ],
    required_tools=[
        "get_current_location",
        "search_places", 
        "get_place_details",
        "calculate_distance"
    ],
    fallback_actions=[
        "expand_search_radius",
        "try_different_cuisine",
        "suggest_popular_alternatives",
        "offer_manual_location_input"
    ]
) 