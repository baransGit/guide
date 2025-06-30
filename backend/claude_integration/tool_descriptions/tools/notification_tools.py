# Sydney Guide - Notification Tools Descriptions
# Bildirim araçları için Claude açıklamaları

from typing import Dict, Any

NOTIFICATION_TOOL_DESCRIPTIONS = {
    "send_notification": {
        "name": "send_notification",
        "description": "Send push notification to user.",
        "when_to_use": [
            "User requests reminders or alerts",
            "Important updates about journey or transport",
            "Proactive suggestions based on location",
            "Emergency or time-sensitive information"
        ],
        "parameters": {
            "user_token": {"type": "string", "description": "User's push notification token"},
            "title": {"type": "string", "description": "Notification title"},
            "body": {"type": "string", "description": "Notification message"},
            "priority": {
                "type": "string",
                "enum": ["low", "medium", "high"],
                "default": "medium",
                "description": "Use 'high' for urgent transport updates"
            }
        },
        "usage_tips": [
            "Keep titles short and clear",
            "Use high priority for transport delays or emergencies",
            "Always ask permission before sending notifications"
        ]
    },

    "schedule_location_alerts": {
        "name": "schedule_location_alerts",
        "description": "Set up location-based alerts for user journey.",
        "when_to_use": [
            "User wants to be notified when near attractions",
            "User requests journey tracking with alerts",
            "For proactive suggestions during travel",
            "When user wants location-based reminders"
        ],
        "parameters": {
            "user_token": {"type": "string", "description": "User's notification token"},
            "journey_waypoints": {
                "type": "array",
                "items": {"type": "object"},
                "description": "List of journey points with lat/lng"
            },
            "alert_radius": {
                "type": "number",
                "default": 500,
                "description": "Alert radius in meters - use 200-500m for walking"
            },
            "alert_types": {
                "type": "array",
                "items": {"type": "string", "enum": ["attractions", "restaurants", "transport", "all"]},
                "default": ["all"]
            }
        }
    },

    "send_journey_reminders": {
        "name": "send_journey_reminders",
        "description": "Send reminders for upcoming transport connections.",
        "when_to_use": [
            "User has planned a journey and wants reminders",
            "User requests departure notifications",
            "For time-sensitive transport connections",
            "When user wants to be reminded to leave"
        ],
        "parameters": {
            "user_token": {"type": "string", "description": "User's notification token"},
            "journey_plan": {"type": "object", "description": "Journey plan with transport steps"},
            "reminder_minutes": {
                "type": "array",
                "items": {"type": "integer"},
                "default": [15, 5],
                "description": "Minutes before departure for reminders"
            }
        }
    },

    "start_journey_tracking": {
        "name": "start_journey_tracking",
        "description": "Start real-time GPS journey tracking with alerts.",
        "when_to_use": [
            "User wants live journey tracking",
            "User requests 'track my journey' or 'guide me'",
            "For real-time navigation assistance",
            "When user wants proximity alerts during travel"
        ],
        "parameters": {
            "user_token": {"type": "string", "description": "User's notification token"},
            "journey_plan": {"type": "object", "description": "Complete journey plan"},
            "tracking_options": {
                "type": "object",
                "properties": {
                    "alert_distance_meters": {"type": "number", "default": 200},
                    "stops_ahead_warning": {"type": "number", "default": 2},
                    "gps_update_interval": {"type": "number", "default": 10}
                }
            }
        }
    },

    "update_journey_location": {
        "name": "update_journey_location",
        "description": "Update user's GPS location during journey tracking.",
        "when_to_use": [
            "During active journey tracking sessions",
            "To provide real-time location updates",
            "For calculating proximity to destinations",
            "Internal tool - usually called automatically"
        ],
        "parameters": {
            "session_id": {"type": "string", "description": "Active tracking session ID"},
            "current_location": {"type": "object", "description": "Current GPS coordinates"},
            "movement_data": {"type": "object", "description": "Speed, direction, accuracy"}
        }
    },

    "stop_journey_tracking": {
        "name": "stop_journey_tracking",
        "description": "Stop active journey tracking session.",
        "when_to_use": [
            "User reaches destination",
            "User requests to stop tracking",
            "Journey is completed or cancelled",
            "When user wants to end GPS monitoring"
        ],
        "parameters": {
            "session_id": {"type": "string", "description": "Journey tracking session ID"}
        }
    }
} 