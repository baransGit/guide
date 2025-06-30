# Sydney Guide - Tool Description Utilities
# Arac aciklama yardimci fonksiyonlari

from typing import Dict, Any, List, Optional

def select_tools_for_user_request(user_message: str, user_context: Optional[Dict[str, Any]] = None) -> List[str]:
    """
    Kullanici istegine gore uygun araclari sec
    
    Args:
        user_message: Kullanicinin mesaji
        user_context: Kullanici baglami (konum, tercihler vb.)
        
    Returns:
        List: Onerilen arac adlari
    """
    message_lower = user_message.lower()
    recommended_tools = []
    
    # Konum ile ilgili istekler
    if any(keyword in message_lower for keyword in ['where am i', 'current location', 'my location']):
        recommended_tools.append('get_current_location')
    
    # Mekan arama istekleri
    if any(keyword in message_lower for keyword in ['restaurant', 'food', 'eat', 'dining', 'dine']):
        recommended_tools.extend(['get_current_location', 'search_places', 'get_place_details'])
    
    # Turistik yerler
    if any(keyword in message_lower for keyword in ['attraction', 'tourist', 'visit', 'see', 'sightseeing']):
        recommended_tools.extend(['get_current_location', 'get_places_by_type', 'get_popular_places'])
    
    # Ulasim istekleri
    if any(keyword in message_lower for keyword in ['transport', 'train', 'bus', 'ferry', 'how to get', 'get to', 'nearest train', 'bus routes']):
        recommended_tools.extend(['get_current_location', 'find_nearby_transport', 'plan_route'])
    
    # Mesafe sorulari
    if any(keyword in message_lower for keyword in ['how far', 'distance', 'close', 'near']):
        recommended_tools.append('calculate_distance')
    
    # Takip ve bildirim istekleri
    if any(keyword in message_lower for keyword in ['track', 'remind', 'alert', 'notify', 'journey', 'trip', 'travel', 'leave', 'notifications']):
        recommended_tools.extend(['start_journey_tracking', 'send_journey_reminders'])
    
    return list(set(recommended_tools))  # Tekrarlari kaldir 