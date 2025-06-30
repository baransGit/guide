# Sydney Guide - Location First Strategy
# Konum oncelikli strateji

LOCATION_FIRST_STRATEGY = {
    "description": "Always get user location before making recommendations",
    "pattern": [
        "Ask permission for location access",
        "Call get_current_location",
        "Use location for nearby searches",
        "Calculate distances for recommendations"
    ]
} 