# Sydney Guide - Conversation Utilities
# Konusma yardimci fonksiyonlari

import re
from typing import Dict, Any, List, Optional

def detect_conversation_intent(user_message: str) -> str:
    """
    Kullanici mesajindan konusma niyetini tespit et
    
    Args:
        user_message: Kullanici mesaji
        
    Returns:
        str: Tespit edilen niyet
    """
    message_lower = user_message.lower()
    
    # Acil durum anahtar kelimeleri
    emergency_keywords = ["lost", "help", "emergency", "stuck", "problem", "kayboldum", "yardim"]
    if any(keyword in message_lower for keyword in emergency_keywords):
        return "emergency_assistance"
    
    # Restoran anahtar kelimeleri
    food_keywords = ["restaurant", "food", "eat", "dining", "hungry", "dine", "meal", "breakfast", "lunch", "dinner"]
    if any(keyword in message_lower for keyword in food_keywords):
        return "restaurant_discovery"
    
    # Yolculuk anahtar kelimeleri
    journey_keywords = ["how to get", "directions", "transport", "travel", "go to", "get to", "route", "bus", "train"]
    if any(keyword in message_lower for keyword in journey_keywords):
        return "journey_planning"
    
    # Turistik yer anahtar kelimeleri
    attraction_keywords = ["visit", "see", "attraction", "tourist", "sightseeing", "explore", "museum", "beach"]
    if any(keyword in message_lower for keyword in attraction_keywords):
        return "attraction_discovery"
    
    # Varsayilan: genel kesif
    return "general_exploration"