# Sydney Guide - User Preferences Management
# Kullanici tercihleri yonetimi

from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, asdict

@dataclass
class UserPreferences:
    """Kullanici tercihleri sinifi"""
    user_id: str
    language: str = "english"
    preferred_transport: List[str] = None
    dietary_restrictions: List[str] = None
    budget_range: str = "medium"  # low, medium, high
    accessibility_needs: List[str] = None
    notification_preferences: Dict[str, bool] = None
    location_sharing: bool = True
    journey_tracking: bool = True
    last_updated: datetime = None
    
    def __post_init__(self):
        """Post-init varsayilan degerleri ayarla"""
        if self.preferred_transport is None:
            self.preferred_transport = ["train", "bus", "ferry"]
        if self.dietary_restrictions is None:
            self.dietary_restrictions = []
        if self.accessibility_needs is None:
            self.accessibility_needs = []
        if self.notification_preferences is None:
            self.notification_preferences = {
                "journey_reminders": True,
                "location_alerts": True,
                "transport_updates": True,
                "recommendations": True
            }
        if self.last_updated is None:
            self.last_updated = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Tercihleri dict'e cevir"""
        data = asdict(self)
        data["last_updated"] = self.last_updated.isoformat()
        return data
    
    def update_preference(self, key: str, value: Any):
        """Tek bir tercihi guncelle"""
        if hasattr(self, key):
            setattr(self, key, value)
            self.last_updated = datetime.now()
    
    def add_dietary_restriction(self, restriction: str):
        """Diyet kisitlamasi ekle"""
        if restriction not in self.dietary_restrictions:
            self.dietary_restrictions.append(restriction)
            self.last_updated = datetime.now()
    
    def remove_dietary_restriction(self, restriction: str):
        """Diyet kisitlamasi kaldir"""
        if restriction in self.dietary_restrictions:
            self.dietary_restrictions.remove(restriction)
            self.last_updated = datetime.now()
    
    def set_notification_preference(self, notification_type: str, enabled: bool):
        """Bildirim tercihini ayarla"""
        self.notification_preferences[notification_type] = enabled
        self.last_updated = datetime.now()

# Global preferences storage (production'da database kullanilacak)
_user_preferences: Dict[str, UserPreferences] = {}

def save_preferences(user_id: str, preferences: Dict[str, Any]) -> UserPreferences:
    """Kullanici tercihlerini kaydet"""
    if user_id in _user_preferences:
        # Mevcut tercihleri guncelle
        existing = _user_preferences[user_id]
        for key, value in preferences.items():
            existing.update_preference(key, value)
        return existing
    else:
        # Yeni tercihler olustur
        prefs = UserPreferences(user_id=user_id, **preferences)
        _user_preferences[user_id] = prefs
        return prefs

def get_user_preferences(user_id: str) -> Optional[UserPreferences]:
    """Kullanici tercihlerini getir"""
    return _user_preferences.get(user_id)

def create_default_preferences(user_id: str) -> UserPreferences:
    """Varsayilan tercihlerle yeni kullanici olustur"""
    prefs = UserPreferences(user_id=user_id)
    _user_preferences[user_id] = prefs
    return prefs 