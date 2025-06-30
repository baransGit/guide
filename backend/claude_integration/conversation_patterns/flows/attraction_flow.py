# Sydney Guide - Attraction Discovery Flow
# Turistik yer kesfi akisi

ATTRACTION_DISCOVERY_FLOW = {
    "trigger_keywords": ["visit", "see", "attraction", "tourist", "sightseeing", "explore"],
    "initial_response": "Sydney has so many amazing places to explore! Let me help you discover the perfect spots.",
    "steps": {
        1: {
            "action": "understand_interests",
            "message": "What interests you most? Museums, outdoor activities, architecture, beaches, or something else?",
            "tools": [],
            "next_step": 2,
            "fallback": "general_attractions"
        },
        2: {
            "action": "get_location",
            "message": "Let me find attractions near your location.",
            "tools": ["get_current_location"],
            "next_step": 3,
            "fallback": "city_center_attractions"
        },
        3: {
            "action": "search_attractions",
            "message": "Searching for the best attractions matching your interests...",
            "tools": ["get_places_by_type", "get_popular_places"],
            "next_step": 4,
            "fallback": "popular_attractions"
        },
        4: {
            "action": "create_itinerary",
            "message": "Here's a suggested itinerary based on your location and interests:",
            "tools": ["calculate_distance", "plan_route"],
            "next_step": 5,
            "fallback": "simple_list"
        },
        5: {
            "action": "offer_alerts",
            "message": "Would you like location-based alerts as you explore the city?",
            "tools": ["schedule_location_alerts"],
            "next_step": "completed",
            "fallback": "manual_exploration"
        }
    }
} 