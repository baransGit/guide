# Sydney Guide - Location Tracker
# Konum takip sistemi

from typing import Dict, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

@dataclass
class LocationData:
    """Konum verisi sinifi"""
    latitude: float
    longitude: float
    accuracy: float
    timestamp: datetime
    address: Optional[str] = None
    place_name: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Konum verisini dict'e cevir"""
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "accuracy": self.accuracy,
            "timestamp": self.timestamp.isoformat(),
            "address": self.address,
            "place_name": self.place_name
        }

class LocationTracker:
    """Konum takip sinifi"""
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.current_location: Optional[LocationData] = None
        self.tracking_enabled = False
        self.update_interval = 30  # seconds
        
    def update_location(self, lat: float, lng: float, accuracy: float, address: str = None, place_name: str = None):
        """Konum bilgisini guncelle"""
        self.current_location = LocationData(
            latitude=lat,
            longitude=lng,
            accuracy=accuracy,
            timestamp=datetime.now(),
            address=address,
            place_name=place_name
        )
    
    def get_current_location(self) -> Optional[LocationData]:
        """Mevcut konumu getir"""
        return self.current_location
    
    def enable_tracking(self):
        """Konum takibini etkinlestir"""
        self.tracking_enabled = True
    
    def disable_tracking(self):
        """Konum takibini devre disi birak"""
        self.tracking_enabled = False
    
    def calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Iki nokta arasindaki mesafeyi hesapla (km)"""
        import math
        
        # Haversine formula
        R = 6371  # Earth radius in km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c

# Global location trackers (production'da Redis kullanilacak)
_location_trackers: Dict[str, LocationTracker] = {}

def update_location(session_id: str, lat: float, lng: float, accuracy: float, address: str = None, place_name: str = None):
    """Oturum konumunu guncelle"""
    if session_id not in _location_trackers:
        _location_trackers[session_id] = LocationTracker(session_id)
    
    _location_trackers[session_id].update_location(lat, lng, accuracy, address, place_name)

def get_current_location(session_id: str) -> Optional[LocationData]:
    """Oturum mevcut konumunu getir"""
    tracker = _location_trackers.get(session_id)
    if tracker:
        return tracker.get_current_location()
    return None 