# Sydney Guide - Restaurant Search Flow
# Restoran arama akisi

RESTAURANT_SEARCH_FLOW = {
    "trigger_keywords": ["restaurant", "food", "eat", "dining", "hungry", "dine"],
    "initial_response": "I'd love to help you find a great restaurant! To give you the best recommendations, I'll need to know your location and food preferences.",
    "steps": {
        1: {
            "action": "request_location",
            "message": "May I access your current location to find nearby restaurants?",
            "tools": ["get_current_location"],
            "next_step": 2,
            "fallback": "manual_location_request"
        },
        2: {
            "action": "gather_preferences", 
            "message": "What type of cuisine are you in the mood for? Any dietary restrictions or preferences?",
            "tools": [],
            "next_step": 3,
            "fallback": "general_search"
        },
        3: {
            "action": "search_restaurants",
            "message": "Let me find the best restaurants matching your preferences nearby...",
            "tools": ["search_places", "calculate_distance"],
            "next_step": 4,
            "fallback": "expand_search"
        },
        4: {
            "action": "present_recommendations",
            "message": "Here are some excellent options I found for you:",
            "tools": ["get_place_details"],
            "next_step": 5,
            "fallback": "alternative_suggestions"
        },
        5: {
            "action": "offer_directions",
            "message": "Would you like directions to any of these restaurants?",
            "tools": ["plan_route", "find_nearby_transport"],
            "next_step": "completed",
            "fallback": "basic_directions"
        }
    }
} 