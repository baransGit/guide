# Sydney Guide - Places Tools Descriptions
# Mekan araçları için Claude açıklamaları

from typing import Dict, Any

PLACES_TOOL_DESCRIPTIONS = {
    "search_places": {
        "name": "search_places",
        "description": "Search for places in Sydney by query, type, and location.",
        "when_to_use": [
            "User asks for restaurants, attractions, shops, etc.",
            "User wants to find specific types of places",
            "User asks 'What's nearby?' or 'Where can I...'",
            "When user mentions food preferences, activities, or shopping"
        ],
        "parameters": {
            "query": {
                "type": "string",
                "description": "Search terms - be specific (e.g., 'vegan restaurant', 'art museum')"
            },
            "lat": {"type": "number", "description": "Search center latitude"},
            "lng": {"type": "number", "description": "Search center longitude"},
            "place_type": {
                "type": "string",
                "enum": ["all", "restaurant", "tourist_attraction", "shopping_mall", "museum", "park", "transport"],
                "default": "all",
                "description": "Filter by place type"
            },
            "radius": {
                "type": "number",
                "default": 5.0,
                "description": "Search radius in km - use 1-2km for walking, 5-10km for transport"
            },
            "max_results": {
                "type": "integer", 
                "default": 10,
                "description": "Maximum results - use 5-10 for recommendations"
            }
        },
        "response_format": {
            "status": "success/error",
            "data": {
                "places": "array of place objects with name, rating, distance, etc.",
                "total_found": "integer - total places found",
                "search_location": "object - search center coordinates"
            }
        },
        "usage_tips": [
            "Use specific queries for better results ('Italian restaurant' not just 'food')",
            "Combine with user's current location for 'nearby' searches",
            "Filter by place_type when user specifies category",
            "Always mention ratings and distance in recommendations"
        ]
    },

    "get_place_details": {
        "name": "get_place_details",
        "description": "Get detailed information about a specific place.",
        "when_to_use": [
            "User asks for more details about a recommended place",
            "User wants hours, phone, website, or specific info",
            "After showing search results and user shows interest",
            "When user asks 'Tell me more about...' a specific place"
        ],
        "parameters": {
            "place_id": {
                "type": "string",
                "description": "Place ID from search results (e.g., 'place_001')"
            }
        },
        "usage_tips": [
            "Use place_id from search_places results",
            "Provide comprehensive details including hours, contact, features",
            "Mention special features like 'harbour_view' or 'wheelchair_accessible'"
        ]
    },

    "get_places_by_type": {
        "name": "get_places_by_type",
        "description": "List places of a specific type.",
        "when_to_use": [
            "User asks for categories like 'restaurants', 'museums', 'parks'",
            "User wants to explore a specific type of venue",
            "When providing themed recommendations",
            "For creating itineraries by category"
        ],
        "parameters": {
            "place_type": {
                "type": "string",
                "enum": ["restaurant", "tourist_attraction", "shopping_mall", "museum", "park", "transport"],
                "description": "Type of places to list"
            },
            "limit": {"type": "integer", "default": 10, "description": "Maximum results"}
        }
    },

    "get_popular_places": {
        "name": "get_popular_places",
        "description": "Get most popular places by rating.",
        "when_to_use": [
            "User asks for 'best', 'top', or 'popular' places",
            "User wants highly-rated recommendations",
            "For creating 'must-visit' lists",
            "When user asks for safe/reliable options"
        ],
        "parameters": {
            "limit": {"type": "integer", "default": 5, "description": "Number of top places"}
        }
    }
} 