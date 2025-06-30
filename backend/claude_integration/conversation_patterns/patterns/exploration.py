# Sydney Guide - General Exploration Pattern
# Genel kesif konusma deseni

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

EXPLORATION_PATTERN = ConversationPattern(
    name="general_exploration",
    description="Kullanici genel olarak Sydney'i kesfetmek istiyor",
    steps=[
        "welcome_to_sydney",
        "understand_visit_duration",
        "get_current_location",
        "assess_interests",
        "create_personalized_suggestions",
        "offer_comprehensive_planning",
        "provide_ongoing_assistance"
    ],
    required_tools=[
        "get_current_location",
        "get_popular_places",
        "search_places",
        "plan_route"
    ],
    fallback_actions=[
        "provide_general_recommendations",
        "suggest_popular_areas",
        "offer_guided_tours",
        "recommend_information_centers"
    ]
) 