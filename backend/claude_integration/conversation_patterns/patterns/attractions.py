# Sydney Guide - Attractions Discovery Pattern
# Turistik yerler kesfi konusma deseni

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

ATTRACTIONS_PATTERN = ConversationPattern(
    name="attraction_discovery",
    description="Kullanici gezilecek yer ararken",
    steps=[
        "understand_interest_type",
        "get_current_location",
        "gather_time_constraints",
        "search_attractions",
        "prioritize_by_distance_rating",
        "present_itinerary_suggestions",
        "offer_location_alerts",
        "suggest_transport_connections"
    ],
    required_tools=[
        "get_current_location",
        "get_places_by_type",
        "get_popular_places",
        "calculate_distance"
    ],
    fallback_actions=[
        "expand_to_nearby_areas",
        "suggest_different_categories",
        "recommend_indoor_alternatives",
        "provide_weather_considerations"
    ]
) 