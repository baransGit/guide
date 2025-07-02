# Sydney Guide - Location MCP Tool (MCP-Enhanced Version)
# Kullanici konum bilgilerini yoneten MCP araci - Proper MCP tool decorators added

import asyncio
import json
import math
import os
import logging
from typing import Dict, Any, Tuple, Optional
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment configuration
USE_REAL_API = os.getenv('MOCK_MODE', 'true').lower() == 'false'
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')

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

# Logging configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# API usage tracking for cost monitoring
api_usage_counter = {"geocoding_calls": 0, "total_cost_usd": 0.0}

def _get_location_fixtures():
    """Location fixtures'tan mock data al"""
    try:
        # Import fixtures from tests directory
        import sys
        import os
        
        # Add tests directory to path - 3 levels up to reach project root
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        tests_dir = os.path.join(project_root, 'tests')
        if tests_dir not in sys.path:
            sys.path.append(tests_dir)
            logger.info(f"Added tests directory to path: {tests_dir}")
        
        from tests.fixtures.mock_location_data import get_location_fixtures
        return get_location_fixtures()
        
    except ImportError as e:
        logger.warning(f"Could not import location fixtures: {e}, using fallback data")
        # Fallback data if fixtures not available
        return {
            "default_location": {
                "lat": -33.8688,
                "lng": 151.2093,
                "address": "Sydney Opera House, Bennelong Point, Sydney NSW 2000, Australia",
                "city": "Sydney",
                "country": "Australia"
            },
            "accuracy_config": {
                "high": {"precision": 6},
                "medium": {"precision": 4},
                "low": {"precision": 2}
            }
        }

def _get_precision_by_accuracy(accuracy: str) -> int:
    """Dogruluk seviyesine gore koordinat hassasiyeti dondur"""
    precision_map = {"high": 6, "medium": 4, "low": 2}
    return precision_map.get(accuracy, 4)

@mcp_tool(
    name="get_current_location",
    description="Kullanicinin mevcut konumunu al - GPS koordinatlari ve adres bilgisi",
    parameters={
        "accuracy": {
            "type": "string",
            "enum": ["high", "medium", "low"],
            "default": "high",
            "description": "Konum dogruluk seviyesi - high: en hassas, medium: orta, low: genel"
        }
    }
)
async def get_current_location(accuracy: str = "high") -> Dict[str, Any]:
    """
    Kullanicinin mevcut konumunu dondur (mock veya gercek API)
    """
    try:
        logger.info(f"Using mock location data (accuracy: {accuracy})")
        return await _get_location_mock_data(accuracy)
        
    except Exception as error:
        logger.error(f"Location tool error: {str(error)}")
        return {
            "status": "error",
            "message": "Location data unavailable",
            "error_code": "LOCATION_ERROR",
            "timestamp": datetime.now().isoformat()
        }

@mcp_tool(
    name="calculate_distance",
    description="Iki nokta arasindaki mesafeyi hesapla - Haversine formulu kullanarak",
    parameters={
        "start_lat": {
            "type": "number",
            "description": "Baslangic noktasinin enlem degeri"
        },
        "start_lng": {
            "type": "number", 
            "description": "Baslangic noktasinin boylam degeri"
        },
        "end_lat": {
            "type": "number",
            "description": "Bitis noktasinin enlem degeri"
        },
        "end_lng": {
            "type": "number",
            "description": "Bitis noktasinin boylam degeri"
        },
        "unit": {
            "type": "string",
            "enum": ["km", "miles", "meters"],
            "default": "km",
            "description": "Mesafe birimi"
        }
    }
)
async def calculate_distance(start_lat: float, start_lng: float, end_lat: float, end_lng: float, unit: str = "km") -> Dict[str, Any]:
    """Iki nokta arasindaki mesafeyi hesapla"""
    try:
        distance_km = _calculate_haversine_distance(start_lat, start_lng, end_lat, end_lng)
        distance_value = _convert_distance_unit(distance_km, unit)
        
        return {
            "status": "success",
            "data": {
                "distance": round(distance_value, 2),
                "unit": unit,
                "start_coordinates": {"lat": start_lat, "lng": start_lng},
                "end_coordinates": {"lat": end_lat, "lng": end_lng},
                "calculation_method": "haversine",
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as error:
        return {"status": "error", "message": "Distance calculation failed", "error_code": "CALCULATION_ERROR", "timestamp": datetime.now().isoformat()}

def _calculate_haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Haversine formulu ile iki nokta arasi mesafeyi km cinsinden hesapla"""
    lat1_rad = math.radians(lat1)
    lng1_rad = math.radians(lng1)
    lat2_rad = math.radians(lat2)
    lng2_rad = math.radians(lng2)
    
    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad
    
    a = (math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    
    earth_radius_km = 6371
    return earth_radius_km * c

def _convert_distance_unit(distance_km: float, unit: str) -> float:
    """Mesafe birimini donustur"""
    unit_conversions = {"km": 1.0, "miles": 0.621371, "meters": 1000.0}
    return distance_km * unit_conversions.get(unit, 1.0)

async def _get_location_mock_data(accuracy: str) -> Dict[str, Any]:
    """Mock location data dondur - fixtures'tan veri al"""
    try:
        # Fixtures'tan mock data al
        fixtures = _get_location_fixtures()
        default_location = fixtures["default_location"]
        
        # Dogruluk seviyesine gore koordinat hassasiyeti ayarla
        lat_precision = _get_precision_by_accuracy(accuracy)
        lng_precision = _get_precision_by_accuracy(accuracy)
        
        location_data = {
            "status": "success",
            "data": {
                "lat": round(default_location["lat"], lat_precision),
                "lng": round(default_location["lng"], lng_precision),
                "address": default_location["address"],
                "city": default_location["city"],
                "country": default_location["country"],
                "accuracy": accuracy,
                "timestamp": datetime.now().isoformat(),
                "source": "mock_gps"
            }
        }
        
        return location_data
        
    except Exception as error:
        logger.error(f"Mock location data error: {str(error)}")
        # Fallback to basic Sydney location if fixtures fail
        return {
            "status": "success",
            "data": {
                "lat": -33.8688,
                "lng": 151.2093,
                "address": "Sydney Opera House, Sydney NSW, Australia",
                "city": "Sydney",
                "country": "Australia",
                "accuracy": accuracy,
                "timestamp": datetime.now().isoformat(),
                "source": "mock_gps_fallback"
            }
        }

class LocationTool:
    """Backward compatibility icin LocationTool class wrapper"""
    
    def __init__(self):
        try:
            fixtures = _get_location_fixtures()
            self.default_location = fixtures["default_location"]
        except Exception as e:
            logger.warning(f"Could not load fixtures for LocationTool: {e}")
            self.default_location = {
                "lat": -33.8688,
                "lng": 151.2093,
                "address": "Sydney Opera House, Sydney NSW, Australia",
                "city": "Sydney",
                "country": "Australia"
            }
    
    async def get_current_location(self, accuracy: str = "high") -> Dict[str, Any]:
        return await get_current_location(accuracy)
    
    async def calculate_distance(self, start_lat: float, start_lng: float, end_lat: float, end_lng: float, unit: str = "km") -> Dict[str, Any]:
        return await calculate_distance(start_lat, start_lng, end_lat, end_lng, unit)

location_tool = LocationTool()
