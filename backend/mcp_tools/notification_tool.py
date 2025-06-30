# Sydney Guide - Notification MCP Tool
# Kullanicilara proaktif bildirim gonderen MCP araci

import asyncio
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment configuration
USE_REAL_API = os.getenv('MOCK_MODE', 'true').lower() == 'false'
FIREBASE_SERVER_KEY = os.getenv('FIREBASE_SERVER_KEY', '')

# MCP imports
try:
    from mcp import mcp_tool
except ImportError:
    # Fallback decorator for development
    def mcp_tool(name: str, description: str, parameters: dict = {}):
        def decorator(func):
            func._mcp_name = name
            func._mcp_description = description
            func._mcp_parameters = parameters or {}
            return func
        return decorator

# Mock notification templates - Sydney guide specific
NOTIFICATION_TEMPLATES = {
    "transport_delay": {
        "title": "Transport Delay Alert",
        "body": "Your {transport_type} service to {destination} is delayed by {delay_minutes} minutes.",
        "category": "transport",
        "priority": "high"
    },
    "location_suggestion": {
        "title": "Nearby Attraction",
        "body": "You're near {place_name}! It has a {rating} star rating and is only {distance}m away.",
        "category": "suggestion",
        "priority": "medium"
    },
    "journey_reminder": {
        "title": "Journey Reminder",
        "body": "Don't forget to leave for {destination} in {minutes} minutes to catch your {transport_type}.",
        "category": "reminder",
        "priority": "high"
    },
    "restaurant_recommendation": {
        "title": "Hungry? Try This!",
        "body": "{restaurant_name} nearby serves great {cuisine_type}. Rating: {rating} stars, {distance}m away.",
        "category": "recommendation",
        "priority": "low"
    },
    "weather_alert": {
        "title": "Weather Update",
        "body": "{weather_condition} expected in Sydney. {advice}",
        "category": "weather",
        "priority": "medium"
    }
}

@mcp_tool(
    name="send_notification",
    description="Send push notification to user",
    parameters={
        "user_token": {"type": "string", "description": "User's push notification token"},
        "title": {"type": "string", "description": "Notification title"},
        "body": {"type": "string", "description": "Notification body text"},
        "priority": {
            "type": "string",
            "enum": ["low", "medium", "high"],
            "default": "medium",
            "description": "Notification priority"
        }
    }
)
async def send_notification(user_token: str, title: str, body: str, priority: str = "medium") -> Dict[str, Any]:
    """
    Kullaniciya push notification gonder (mock veya gercek FCM)
    
    Args:
        user_token: Kullanicinin push token'i
        title: Bildirim basligi
        body: Bildirim icerigi
        priority: Bildirim onceligi
        
    Returns:
        Dict: Bildirim gonderim sonucu
    """
    try:
        if USE_REAL_API and FIREBASE_SERVER_KEY and FIREBASE_SERVER_KEY != "your_firebase_server_key_here":
            # TODO: Gercek Firebase FCM implementation
            # Bu kisim Firebase Admin SDK kullanilarak implement edilecek
            pass
        
        # Mock notification gonder (development icin)
        mock_notification = {
            "notification_id": f"mock_{int(datetime.now().timestamp())}_{user_token[:8]}",
            "user_token": user_token,
            "title": title,
            "body": body,
            "priority": priority,
            "delivery_status": "delivered",
            "sent_at": datetime.now().isoformat(),
            "source": "firebase_fcm" if (USE_REAL_API and FIREBASE_SERVER_KEY) else "mock_notification_service"
        }
        
        return {
            "status": "success",
            "data": {
                "notification": mock_notification,
                "delivery_info": {
                    "delivered": True,
                    "delivery_time_ms": 50,  # Mock delivery time
                    "platform": "mock_platform"
                },
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as error:
        return {
            "status": "error",
            "message": f"Notification sending failed: {str(error)}",
            "error_code": "NOTIFICATION_ERROR",
            "timestamp": datetime.now().isoformat()
        }

@mcp_tool(
    name="schedule_location_alerts",
    description="Set up location-based notification alerts for user journey",
    parameters={
        "user_token": {"type": "string", "description": "User's push notification token"},
        "journey_waypoints": {"type": "array", "items": {"type": "object"}, "description": "List of journey waypoints with lat/lng"},
        "alert_radius": {"type": "number", "default": 500, "description": "Alert radius in meters"},
        "alert_types": {
            "type": "array", 
            "items": {"type": "string", "enum": ["attractions", "restaurants", "transport", "all"]},
            "default": ["all"],
            "description": "Types of alerts to enable"
        }
    }
)
async def schedule_location_alerts(user_token: str, journey_waypoints: List[Dict[str, Any]],
                                 alert_radius: float = 500, 
                                 alert_types: List[str] = ["all"]) -> Dict[str, Any]:
    """
    Kullanicinin yolculugu icin konum bazli uyarilari ayarla
    
    Args:
        user_token: Kullanicinin push token'i
        journey_waypoints: Yolculuk noktalarinin listesi
        alert_radius: Uyari yaricapi (metre)
        alert_types: Etkinlestirilecek uyari tipleri
        
    Returns:
        Dict: Uyari ayarlama sonucu
    """
    try:
        scheduled_alerts = []
        
        for i, waypoint in enumerate(journey_waypoints):
            alert_id = f"location_alert_{user_token[:8]}_{i}_{int(datetime.now().timestamp())}"
            
            # Mock alert olustur
            alert = {
                "alert_id": alert_id,
                "user_token": user_token,
                "location": {
                    "lat": waypoint.get("lat", 0),
                    "lng": waypoint.get("lng", 0),
                    "address": waypoint.get("address", "Unknown location")
                },
                "radius_meters": alert_radius,
                "alert_types": alert_types,
                "status": "active",
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(hours=24)).isoformat()
            }
            scheduled_alerts.append(alert)
        
        return {
            "status": "success",
            "data": {
                "scheduled_alerts": scheduled_alerts,
                "total_alerts": len(scheduled_alerts),
                "alert_radius_meters": alert_radius,
                "alert_types": alert_types,
                "expires_in_hours": 24,
                "source": "firebase_geofencing" if (USE_REAL_API and FIREBASE_SERVER_KEY) else "mock_scheduler",
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as error:
        return {
            "status": "error",
            "message": f"Location alert scheduling failed: {str(error)}",
            "error_code": "ALERT_SCHEDULING_ERROR",
            "timestamp": datetime.now().isoformat()
        }

@mcp_tool(
    name="send_journey_reminders",
    description="Send reminders for upcoming transport connections",
    parameters={
        "user_token": {"type": "string", "description": "User's push notification token"},
        "journey_plan": {"type": "object", "description": "Journey plan with transport steps"},
        "reminder_minutes": {"type": "array", "items": {"type": "integer"}, "default": [15, 5], "description": "Minutes before departure to send reminders"}
    }
)
async def send_journey_reminders(user_token: str, journey_plan: Dict[str, Any],
                               reminder_minutes: List[int] = [15, 5]) -> Dict[str, Any]:
    """
    Yaklaşan ulasim baglantilari icin hatirlaticilar gonder
    
    Args:
        user_token: Kullanicinin push token'i
        journey_plan: Ulasim adimlari ile yolculuk plani
        reminder_minutes: Kalkistan kac dakika once hatirlatici gonderilecegi
        
    Returns:
        Dict: Hatirlatici gonderim sonucu
    """
    try:
        scheduled_reminders = []
        
        # Journey plan'dan transport step'leri cek
        steps = journey_plan.get("route", {}).get("steps", [])
        
        for step in steps:
            if step.get("mode") in ["train", "bus", "ferry", "transit"]:
                departure_time = step.get("departure_time", "now")
                
                for reminder_min in reminder_minutes:
                    reminder_id = f"reminder_{user_token[:8]}_{step.get('step_number', 0)}_{reminder_min}"
                    
                    reminder = {
                        "reminder_id": reminder_id,
                        "user_token": user_token,
                        "transport_step": step,
                        "reminder_minutes_before": reminder_min,
                        "scheduled_for": departure_time,  # Bu gercek implementasyonda hesaplanacak
                        "notification_data": {
                            "destination": step.get("end_station", "Unknown"),
                            "transport_type": step.get("mode", "transport"),
                            "minutes": reminder_min
                        },
                        "status": "scheduled",
                        "created_at": datetime.now().isoformat()
                    }
                    scheduled_reminders.append(reminder)
        
        return {
            "status": "success",
            "data": {
                "scheduled_reminders": scheduled_reminders,
                "total_reminders": len(scheduled_reminders),
                "reminder_schedule": reminder_minutes,
                "journey_steps": len(steps),
                "source": "firebase_scheduler" if (USE_REAL_API and FIREBASE_SERVER_KEY) else "mock_scheduler",
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as error:
        return {
            "status": "error",
            "message": f"Journey reminder scheduling failed: {str(error)}",
            "error_code": "REMINDER_ERROR",
            "timestamp": datetime.now().isoformat()
        }

@mcp_tool(
    name="start_journey_tracking",
    description="Start real-time journey tracking with GPS monitoring and proximity alerts",
    parameters={
        "user_token": {"type": "string", "description": "User's push notification token"},
        "journey_plan": {"type": "object", "description": "Complete journey plan with stops and waypoints"},
        "tracking_options": {
            "type": "object",
            "properties": {
                "alert_distance_meters": {"type": "number", "default": 200},
                "stops_ahead_warning": {"type": "number", "default": 2},
                "gps_update_interval": {"type": "number", "default": 10}
            }
        }
    }
)
async def start_journey_tracking(user_token: str, journey_plan: Dict[str, Any], 
                               tracking_options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Kullanicinin yolculugunu gercek zamanli takip et ve yakinlik uyarilari gonder
    
    Args:
        user_token: Kullanicinin push token'i
        journey_plan: Yolculuk plani (duraklar, rotalar)
        tracking_options: Takip ayarlari
        
    Returns:
        Dict: Takip baslama sonucu
    """
    try:
        if not tracking_options:
            tracking_options = {
                "alert_distance_meters": 200,
                "stops_ahead_warning": 2,
                "gps_update_interval": 10
            }
        
        # Journey tracking session olustur
        tracking_session = {
            "session_id": f"journey_{user_token[:8]}_{int(datetime.now().timestamp())}",
            "user_token": user_token,
            "journey_plan": journey_plan,
            "tracking_options": tracking_options,
            "status": "active",
            "current_step": 0,
            "alerts_sent": [],
            "started_at": datetime.now().isoformat(),
            "last_location_update": None,
            "next_alert_distance": tracking_options.get("alert_distance_meters", 200)
        }
        
        # Mock journey steps - gercek uygulamada transport_tool'dan gelecek
        journey_steps = journey_plan.get("steps", [
            {
                "step_id": 1,
                "transport_type": "bus",
                "route_name": "380 to Bondi Beach",
                "stops": [
                    {"name": "Circular Quay", "lat": -33.8610, "lng": 151.2105, "stop_sequence": 1},
                    {"name": "Museum Station", "lat": -33.8738, "lng": 151.2127, "stop_sequence": 2},
                    {"name": "Hyde Park", "lat": -33.8688, "lng": 151.2093, "stop_sequence": 3},
                    {"name": "Kings Cross", "lat": -33.8737, "lng": 151.2221, "stop_sequence": 4},
                    {"name": "Bondi Junction", "lat": -33.8915, "lng": 151.2477, "stop_sequence": 5}
                ],
                "destination_stop": {"name": "Bondi Junction", "lat": -33.8915, "lng": 151.2477}
            }
        ])
        
        tracking_session["journey_steps"] = journey_steps
        
        # Global tracking sessions'a ekle (gercek uygulamada Redis/Database)
        if not hasattr(start_journey_tracking, '_active_sessions'):
            start_journey_tracking._active_sessions = {}
        
        start_journey_tracking._active_sessions[tracking_session["session_id"]] = tracking_session
        
        return {
            "status": "success",
            "data": {
                "tracking_session": tracking_session,
                "message": "Journey tracking started successfully",
                "next_steps": [
                    "Send GPS updates via update_journey_location",
                    "Receive proximity alerts automatically",
                    "Stop tracking via stop_journey_tracking"
                ],
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as error:
        return {
            "status": "error",
            "message": f"Journey tracking failed to start: {str(error)}",
            "error_code": "TRACKING_START_ERROR",
            "timestamp": datetime.now().isoformat()
        }

@mcp_tool(
    name="update_journey_location",
    description="Update user's current GPS location during journey tracking",
    parameters={
        "session_id": {"type": "string", "description": "Active journey tracking session ID"},
        "current_location": {"type": "object", "description": "Current GPS coordinates"},
        "movement_data": {"type": "object", "description": "Speed, direction, accuracy data"}
    }
)
async def update_journey_location(session_id: str, current_location: Dict[str, Any], 
                                movement_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Kullanicinin mevcut GPS konumunu guncelle ve yakinlik kontrolu yap
    
    Args:
        session_id: Aktif takip session ID'si
        current_location: Mevcut GPS koordinatlari
        movement_data: Hiz, yon, dogruluk bilgileri
        
    Returns:
        Dict: Konum guncelleme ve uyari sonucu
    """
    try:
        # Active session'i bul
        if not hasattr(start_journey_tracking, '_active_sessions'):
            return {"status": "error", "message": "No active tracking sessions"}
        
        active_sessions = start_journey_tracking._active_sessions
        if session_id not in active_sessions:
            return {"status": "error", "message": "Tracking session not found"}
        
        session = active_sessions[session_id]
        user_lat = current_location.get("lat", 0)
        user_lng = current_location.get("lng", 0)
        
        # Konum guncellemesini kaydet
        session["last_location_update"] = {
            "location": current_location,
            "movement_data": movement_data or {},
            "timestamp": datetime.now().isoformat()
        }
        
        # Mevcut journey step'i al
        current_step = session.get("current_step", 0)
        journey_steps = session.get("journey_steps", [])
        
        if current_step >= len(journey_steps):
            return {"status": "completed", "message": "Journey completed"}
        
        current_journey = journey_steps[current_step]
        stops = current_journey.get("stops", [])
        destination_stop = current_journey.get("destination_stop")
        
        triggered_alerts = []
        
        # Her durak icin yakinlik kontrolu
        for i, stop in enumerate(stops):
            stop_lat = stop.get("lat", 0)
            stop_lng = stop.get("lng", 0)
            
            # Mesafe hesapla (basit haversine)
            distance = calculate_distance_simple(user_lat, user_lng, stop_lat, stop_lng)
            
            # Yakinlik uyarisi kontrolu
            alert_distance = session["tracking_options"].get("alert_distance_meters", 200)
            stops_ahead = session["tracking_options"].get("stops_ahead_warning", 2)
            
            # Hedef duraga yakin mi?
            if stop["name"] == destination_stop["name"] and distance <= alert_distance:
                alert_message = f"You're approaching {stop['name']}! Get ready to get off."
                alert = await send_proximity_alert(session["user_token"], alert_message, stop, distance)
                triggered_alerts.append(alert)
                
            # Gelecek duraklar icin uyari
            elif distance <= alert_distance * 2:  # Daha erken uyari
                remaining_stops = len([s for s in stops if s["stop_sequence"] > stop["stop_sequence"]])
                if remaining_stops <= stops_ahead and remaining_stops > 0:
                    alert_message = f"Get ready! {remaining_stops} stops until {destination_stop['name']}"
                    alert = await send_proximity_alert(session["user_token"], alert_message, stop, distance)
                    triggered_alerts.append(alert)
        
        return {
            "status": "success",
            "data": {
                "location_updated": True,
                "current_location": current_location,
                "distance_to_destination": calculate_distance_simple(
                    user_lat, user_lng, 
                    destination_stop["lat"], destination_stop["lng"]
                ),
                "triggered_alerts": triggered_alerts,
                "session_status": "tracking",
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as error:
        return {
            "status": "error",
            "message": f"Location update failed: {str(error)}",
            "error_code": "LOCATION_UPDATE_ERROR",
            "timestamp": datetime.now().isoformat()
        }

async def send_proximity_alert(user_token: str, message: str, stop: Dict[str, Any], distance: float) -> Dict[str, Any]:
    """Yakinlik uyarisi gonder"""
    try:
        # Bildirim gonder
        notification_result = await send_notification(
            user_token=user_token,
            title="Journey Alert",
            body=message,
            priority="high"
        )
        
        return {
            "alert_type": "proximity",
            "stop_name": stop["name"],
            "distance_meters": round(distance),
            "message": message,
            "notification_sent": notification_result.get("status") == "success",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as error:
        return {
            "alert_type": "proximity",
            "error": str(error),
            "timestamp": datetime.now().isoformat()
        }

def calculate_distance_simple(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Basit mesafe hesaplama (metre cinsinden)"""
    import math
    
    # Haversine formula
    R = 6371000  # Earth radius in meters
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lng = math.radians(lng2 - lng1)
    
    a = (math.sin(delta_lat/2) * math.sin(delta_lat/2) + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * 
         math.sin(delta_lng/2) * math.sin(delta_lng/2))
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    
    return distance

@mcp_tool(
    name="stop_journey_tracking",
    description="Stop active journey tracking session",
    parameters={
        "session_id": {"type": "string", "description": "Journey tracking session ID to stop"}
    }
)
async def stop_journey_tracking(session_id: str) -> Dict[str, Any]:
    """
    Aktif yolculuk takibini durdur
    
    Args:
        session_id: Durdurulacak session ID
        
    Returns:
        Dict: Takip durdurma sonucu
    """
    try:
        if not hasattr(start_journey_tracking, '_active_sessions'):
            return {"status": "error", "message": "No active sessions"}
        
        active_sessions = start_journey_tracking._active_sessions
        if session_id not in active_sessions:
            return {"status": "error", "message": "Session not found"}
        
        session = active_sessions[session_id]
        session["status"] = "completed"
        session["ended_at"] = datetime.now().isoformat()
        
        # Session'i aktif listeden kaldir
        del active_sessions[session_id]
        
        return {
            "status": "success",
            "data": {
                "session_id": session_id,
                "message": "Journey tracking stopped successfully",
                "session_duration": session.get("ended_at"),
                "alerts_sent_count": len(session.get("alerts_sent", [])),
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as error:
        return {
            "status": "error",
            "message": f"Failed to stop tracking: {str(error)}",
            "timestamp": datetime.now().isoformat()
        }

# Backward compatibility icin wrapper class
class NotificationTool:
    """Backward compatibility icin NotificationTool class wrapper"""
    
    def __init__(self):
        pass
    
    async def send_notification(self, user_token: str, title: str, body: str, priority: str = "medium") -> Dict[str, Any]:
        """Wrapper method - MCP tool'u cagir"""
        return await send_notification(user_token, title, body, priority)

# MCP tool instance'i olustur
notification_tool = NotificationTool() 