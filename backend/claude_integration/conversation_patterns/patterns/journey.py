# Sydney Guide - Journey Planning Pattern
# Yolculuk planlama konusma deseni

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

JOURNEY_PATTERN = ConversationPattern(
    name="journey_planning",
    description="Kullanici bir yerden bir yere gitmek istediginde",
    steps=[
        "understand_destination_intent",
        "get_origin_location",
        "clarify_destination",
        "find_transport_options",
        "plan_optimal_route",
        "present_route_options",
        "offer_journey_tracking",
        "provide_departure_reminders"
    ],
    required_tools=[
        "get_current_location",
        "find_nearby_transport",
        "plan_route",
        "get_transport_status"
    ],
    fallback_actions=[
        "suggest_alternative_routes",
        "recommend_different_transport",
        "provide_walking_directions",
        "offer_taxi_alternative"
    ]
) 