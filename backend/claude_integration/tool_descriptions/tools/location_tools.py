# Sydney Guide - Location Tools Descriptions
# Konum araçları için Claude açıklamaları

from typing import Dict, Any

LOCATION_TOOL_DESCRIPTIONS = {
    "get_current_location": {
        "name": "get_current_location",
        "description": "Get user's current GPS location with address information.",
        "when_to_use": [
            "User asks 'Where am I?' or needs current location",
            "Before searching for nearby places or transport",
            "When planning routes or journeys",
            "At start of conversation to understand user context"
        ],
        "parameters": {
            "accuracy": {
                "type": "string",
                "enum": ["high", "medium", "low"],
                "default": "high",
                "description": "Location accuracy level - use 'high' for precise recommendations"
            }
        },
        "response_format": {
            "status": "success/error",
            "data": {
                "lat": "float - latitude coordinate",
                "lng": "float - longitude coordinate", 
                "address": "string - formatted address",
                "city": "string - city name",
                "country": "string - country name"
            }
        },
        "usage_tips": [
            "Always ask permission before getting location",
            "Use high accuracy for restaurant/attraction recommendations",
            "Use medium accuracy for general area suggestions",
            "Handle permission denied gracefully"
        ]
    },
    
    "calculate_distance": {
        "name": "calculate_distance",
        "description": "Calculate distance between two geographic points.",
        "when_to_use": [
            "User asks 'How far is...' or distance questions",
            "Before recommending places (to show distance)",
            "When comparing multiple options by proximity",
            "For journey planning and time estimates"
        ],
        "parameters": {
            "start_lat": {"type": "number", "description": "Starting point latitude"},
            "start_lng": {"type": "number", "description": "Starting point longitude"},
            "end_lat": {"type": "number", "description": "Destination latitude"},
            "end_lng": {"type": "number", "description": "Destination longitude"},
            "unit": {
                "type": "string",
                "enum": ["km", "miles", "meters"],
                "default": "km",
                "description": "Distance unit - use 'meters' for walking distances under 1km"
            }
        },
        "usage_tips": [
            "Use meters for walking distances under 1km",
            "Use km for driving/transport distances",
            "Always include distance in your recommendations"
        ]
    }
} 