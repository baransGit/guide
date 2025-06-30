# Sydney Guide - Transport Tools Descriptions
# Ulaşım araçları için Claude açıklamaları

from typing import Dict, Any

TRANSPORT_TOOL_DESCRIPTIONS = {
    "find_nearby_transport": {
        "name": "find_nearby_transport",
        "description": "Find nearby transport stations and stops.",
        "when_to_use": [
            "User asks 'How do I get to...' or needs transport",
            "User wants to find train stations, bus stops, ferry terminals",
            "Before planning routes to show transport options",
            "When user asks about public transport access"
        ],
        "parameters": {
            "lat": {"type": "number", "description": "Search location latitude"},
            "lng": {"type": "number", "description": "Search location longitude"},
            "transport_type": {
                "type": "string",
                "enum": ["all", "train", "bus", "ferry", "light_rail"],
                "default": "all",
                "description": "Type of transport to find"
            },
            "radius": {
                "type": "number",
                "default": 1.0,
                "description": "Search radius in km - use 0.5-1km for walking distance"
            },
            "max_results": {"type": "integer", "default": 5}
        },
        "usage_tips": [
            "Use small radius (0.5-1km) for walking to transport",
            "Show multiple transport types when available",
            "Include distance and walking time to stations"
        ]
    },

    "plan_route": {
        "name": "plan_route",
        "description": "Plan public transport route between two locations.",
        "when_to_use": [
            "User asks 'How do I get from A to B?'",
            "User needs detailed journey instructions",
            "User wants transport options and times",
            "For complete journey planning with connections"
        ],
        "parameters": {
            "origin_lat": {"type": "number", "description": "Starting point latitude"},
            "origin_lng": {"type": "number", "description": "Starting point longitude"},
            "destination_lat": {"type": "number", "description": "Destination latitude"},
            "destination_lng": {"type": "number", "description": "Destination longitude"},
            "travel_modes": {
                "type": "array",
                "items": {"type": "string", "enum": ["walking", "transit", "bus", "train", "ferry"]},
                "default": ["transit", "walking"],
                "description": "Preferred transport modes"
            },
            "departure_time": {
                "type": "string",
                "default": "now",
                "description": "Departure time (ISO format or 'now')"
            }
        },
        "usage_tips": [
            "Always provide step-by-step instructions",
            "Include total time, cost, and walking distances",
            "Mention any transfers or connections",
            "Offer alternative routes when possible"
        ]
    },

    "get_transport_status": {
        "name": "get_transport_status",
        "description": "Get real-time transport status and departures.",
        "when_to_use": [
            "User asks about delays or service status",
            "User wants to know next departure times",
            "For real-time transport information",
            "When user is at a station and needs current info"
        ],
        "parameters": {
            "stop_id": {"type": "string", "description": "Transport stop or station ID"},
            "transport_type": {
                "type": "string",
                "enum": ["train", "bus", "ferry", "light_rail"],
                "default": "train"
            },
            "limit": {"type": "integer", "default": 5, "description": "Number of upcoming departures"}
        }
    }
} 