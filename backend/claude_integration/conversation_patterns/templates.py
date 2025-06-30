# Sydney Guide - Response Templates
# Yanit sablonlari

from typing import Dict, Any

# Yanit sablonlari
RESPONSE_TEMPLATES = {
    "greeting": {
        "first_time": "G'day! Welcome to Sydney! I'm your personal AI guide. How can I help you explore our beautiful city today?",
        "returning": "Welcome back! Ready for another Sydney adventure? What would you like to discover today?",
        "multilingual": "Hello! Merhaba! 你好! こんにちは! I speak multiple languages. How can I assist you in Sydney today?"
    },
    
    "location_request": {
        "initial": "To give you the best recommendations, I'd like to know your current location. May I access your GPS?",
        "permission_needed": "I need location access to find nearby places. You can grant permission in your device settings.",
        "manual_input": "No worries! You can tell me your location or a nearby landmark, and I'll work from there."
    },
    
    "search_results": {
        "found": "Great! I found {count} excellent options for you. Here are my top recommendations:",
        "no_results": "I couldn't find exactly what you're looking for nearby. Let me suggest some alternatives:",
        "limited_results": "I found a few options, but let me expand the search to give you more choices:"
    },
    
    "recommendations": {
        "restaurant": "🍽️ **{name}** ({rating}⭐)\n📍 {address}\n🚶 {distance} walk from you\n💰 {price_level}\n{description}",
        "attraction": "🎯 **{name}** ({rating}⭐)\n📍 {address}\n🚶 {distance} from you\n⏰ {opening_hours}\n{description}",
        "transport": "🚌 **{route}** - {type}\n📍 {stop_name}\n🚶 {walk_time} walk to stop\n⏰ Next: {next_departure}\n🕒 Journey time: {duration}"
    },
    
    "journey_planning": {
        "route_found": "🗺️ I found the best route for you! Here are your options:",
        "multiple_options": "You have {count} different ways to get there. Here's what I recommend:",
        "no_direct_route": "There's no direct route, but I can get you there with {transfers} transfer(s):"
    },
    
    "tracking_offers": {
        "journey_tracking": "Would you like me to track your journey and send you helpful updates along the way?",
        "location_alerts": "I can send you notifications about interesting places as you explore. Would you like that?",
        "departure_reminders": "Shall I remind you when it's time to leave for your next destination?"
    },
    
    "emergency": {
        "lost_tourist": "I'm here to help! Let me find your location and guide you to safety or your destination.",
        "transport_disruption": "I see there's a transport issue. Let me find alternative routes for you right away.",
        "general_help": "Don't worry, I'm here to help! Tell me what's wrong and I'll do my best to assist you."
    }
}

def format_response_template(template_key: str, **kwargs) -> str:
    """
    Yanit sablonunu formatla
    
    Args:
        template_key: Sablon anahtari (ornek: "greeting.first_time")
        **kwargs: Sablon degiskenleri
        
    Returns:
        str: Formatlanmis yanit
    """
    try:
        # Anahtari parcala (ornek: "greeting.first_time" -> ["greeting", "first_time"])
        keys = template_key.split('.')
        
        # Sablonu bul
        template = RESPONSE_TEMPLATES
        for key in keys:
            template = template[key]
        
        # Degiskenleri formatla
        if isinstance(template, str):
            return template.format(**kwargs)
        else:
            return str(template)
            
    except (KeyError, AttributeError):
        # Sablon bulunamazsa varsayilan yanit dondur
        return "I'm here to help! How can I assist you in Sydney today?"