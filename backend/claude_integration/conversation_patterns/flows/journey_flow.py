# Sydney Guide - Journey Planning Flow
# Yolculuk planlama akisi

JOURNEY_PLANNING_FLOW = {
    "trigger_keywords": ["how to get", "directions", "transport", "travel", "go to", "get to"],
    "initial_response": "I'll help you plan your journey! Let me find the best route for you.",
    "steps": {
        1: {
            "action": "get_origin",
            "message": "Where are you starting from? I can use your current location or you can tell me.",
            "tools": ["get_current_location"],
            "next_step": 2,
            "fallback": "manual_origin"
        },
        2: {
            "action": "get_destination",
            "message": "Where would you like to go?",
            "tools": ["search_places"],
            "next_step": 3,
            "fallback": "clarify_destination"
        },
        3: {
            "action": "find_routes",
            "message": "Let me find the best transport options for you...",
            "tools": ["find_nearby_transport", "plan_route"],
            "next_step": 4,
            "fallback": "alternative_routes"
        },
        4: {
            "action": "present_options",
            "message": "Here are your transport options:",
            "tools": ["get_transport_status"],
            "next_step": 5,
            "fallback": "basic_directions"
        },
        5: {
            "action": "offer_tracking",
            "message": "Would you like me to track your journey and send you updates?",
            "tools": ["start_journey_tracking", "send_journey_reminders"],
            "next_step": "completed",
            "fallback": "basic_guidance"
        }
    }
}