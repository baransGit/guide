# Sydney Guide - Location MCP Tool
# Kullanici konum bilgilerini yoneten MCP araci

import asyncio
import json
import math
import os
import logging
from typing import Dict, Any, Tuple, Optional
from datetime import datetime
import aiohttp
import googlemaps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment configuration
USE_REAL_API = os.getenv('MOCK_MODE', 'true').lower() == 'false'
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')

# Logging configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# API usage tracking for cost monitoring
api_usage_counter = {"geocoding_calls": 0, "total_cost_usd": 0.0}

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

# Mock data icin varsayilan Sydney koordinatlari
DEFAULT_LOCATION = {
    "lat": -33.8688,
    "lng": 151.2093,
    "address": "Sydney Opera House, Bennelong Point, Sydney NSW 2000, Australia",
    "city": "Sydney",
    "country": "Australia"
}

@mcp_tool(
    name="get_current_location",
    description="Get user current location",
    parameters={
        "accuracy": {
            "type": "string", 
            "enum": ["high", "medium", "low"],
            "default": "high",
            "description": "Location accuracy level"
        }
    }
)
async def get_current_location(accuracy: str = "high") -> Dict[str, Any]:
    """
    Kullanicinin mevcut konumunu dondur (mock veya gercek API)
    
    Args:
        accuracy: Konum dogruluk seviyesi ("high", "medium", "low")
        
    Returns:
        Dict: Konum bilgileri iceren sozluk
    """
    try:
        if USE_REAL_API and GOOGLE_MAPS_API_KEY:
            logger.info(f"Using real Google Geocoding API for location (accuracy: {accuracy})")
            # Gercek Google Geocoding API kullan
            return await _get_location_real_api(accuracy)
        else:
            logger.info(f"Using mock location data (accuracy: {accuracy})")
            # Mock data kullan
            return await _get_location_mock_data(accuracy)
        
    except googlemaps.exceptions.ApiError as api_error:
        logger.error(f"Google API error: {str(api_error)}")
        return {
            "status": "error",
            "message": "Google API service unavailable",
            "error_code": "GOOGLE_API_ERROR",
            "timestamp": datetime.now().isoformat()
        }
    except googlemaps.exceptions.Timeout as timeout_error:
        logger.error(f"Google API timeout: {str(timeout_error)}")
        return {
            "status": "error",
            "message": "Location service timeout",
            "error_code": "API_TIMEOUT",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as error:
        # Hata durumunda log kaydet ve hata mesaji dondur
        logger.error(f"Location tool error: {str(error)}")
        return {
            "status": "error",
            "message": "Location data unavailable",
            "error_code": "LOCATION_ERROR",
            "timestamp": datetime.now().isoformat()
        }

@mcp_tool(
    name="calculate_distance",
    description="Calculate distance between two points",
    parameters={
        "start_lat": {"type": "number", "description": "Start point latitude"},
        "start_lng": {"type": "number", "description": "Start point longitude"},
        "end_lat": {"type": "number", "description": "End point latitude"},
        "end_lng": {"type": "number", "description": "End point longitude"},
        "unit": {
            "type": "string", 
            "enum": ["km", "miles", "meters"],
            "default": "km",
            "description": "Distance unit"
        }
    }
)
async def calculate_distance(start_lat: float, 
                           start_lng: float,
                           end_lat: float, 
                           end_lng: float,
                           unit: str = "km") -> Dict[str, Any]:
    """
    Iki nokta arasindaki mesafeyi hesapla
    
    Args:
        start_lat: Baslangic noktasi enlemi
        start_lng: Baslangic noktasi boylamı
        end_lat: Bitis noktasi enlemi  
        end_lng: Bitis noktasi boylamı
        unit: Mesafe birimi ("km", "miles", "meters")
        
    Returns:
        Dict: Mesafe bilgileri iceren sozluk
    """
    try:
        # Haversine formulunu kullanarak mesafe hesapla
        distance_km = _calculate_haversine_distance(
            start_lat, start_lng, end_lat, end_lng
        )
        
        # Birim donusumu yap
        distance_value = _convert_distance_unit(distance_km, unit)
        
        return {
            "status": "success",
            "data": {
                "distance": round(distance_value, 2),
                "unit": unit,
                "start_coordinates": {
                    "lat": start_lat,
                    "lng": start_lng
                },
                "end_coordinates": {
                    "lat": end_lat,
                    "lng": end_lng
                },
                "calculation_method": "haversine",
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as error:
        return {
            "status": "error", 
            "message": "Distance calculation failed",
            "error_code": "CALCULATION_ERROR",
            "timestamp": datetime.now().isoformat()
        }

def _get_precision_by_accuracy(accuracy: str) -> int:
    """Dogruluk seviyesine gore koordinat hassasiyeti dondur"""
    accuracy_map = {
        "high": 6,    # ~0.1 metre hassasiyet
        "medium": 4,  # ~10 metre hassasiyet  
        "low": 2      # ~1 km hassasiyet
    }
    return accuracy_map.get(accuracy, 4)

def _calculate_haversine_distance(lat1: float, lng1: float,
                                lat2: float, lng2: float) -> float:
    """
    Haversine formulu ile iki nokta arasi mesafeyi km cinsinden hesapla
    """
    # Koordinatlari radyana cevir
    lat1_rad = math.radians(lat1)
    lng1_rad = math.radians(lng1)
    lat2_rad = math.radians(lat2)
    lng2_rad = math.radians(lng2)
    
    # Farkları hesapla
    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad
    
    # Haversine formulu
    a = (math.sin(dlat / 2) ** 2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    
    # Dunyanin yaricapi (km)
    earth_radius_km = 6371
    
    return earth_radius_km * c

def _convert_distance_unit(distance_km: float, unit: str) -> float:
    """Mesafe birimini donustur"""
    unit_conversions = {
        "km": 1.0,
        "miles": 0.621371,
        "meters": 1000.0
    }
    
    conversion_factor = unit_conversions.get(unit, 1.0)
    return distance_km * conversion_factor

# Mock ve Real API implementation functions

async def _get_location_mock_data(accuracy: str) -> Dict[str, Any]:
    """Mock location data dondur"""
    # Dogruluk seviyesine gore koordinat hassasiyeti ayarla
    lat_precision = _get_precision_by_accuracy(accuracy)
    lng_precision = _get_precision_by_accuracy(accuracy)
    
    location_data = {
        "status": "success",
        "data": {
            "lat": round(DEFAULT_LOCATION["lat"], lat_precision),
            "lng": round(DEFAULT_LOCATION["lng"], lng_precision),
            "address": DEFAULT_LOCATION["address"],
            "city": DEFAULT_LOCATION["city"],
            "country": DEFAULT_LOCATION["country"],
            "accuracy": accuracy,
            "timestamp": datetime.now().isoformat(),
            "source": "mock_gps"
        }
    }
    
    return location_data

async def _get_location_real_api(accuracy: str) -> Dict[str, Any]:
    """Gercek Google Geocoding API kullanarak konum bilgisi al"""
    try:
        # Cost monitoring - track API usage
        api_usage_counter["geocoding_calls"] += 1
        api_usage_counter["total_cost_usd"] += 0.005  # $0.005 per geocoding request
        
        logger.info(f"Making Google Geocoding API call #{api_usage_counter['geocoding_calls']} (Total cost: ${api_usage_counter['total_cost_usd']:.3f})")
        
        # Cost alert if exceeding daily budget
        if api_usage_counter["total_cost_usd"] > 10.0:  # $10 daily limit
            logger.warning(f"Daily API cost limit exceeded: ${api_usage_counter['total_cost_usd']:.2f}")
        
        # Google Maps client olustur
        gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        
        # Simdilik Sydney Opera House koordinatlarini Google API ile dogrula
        # Gercek implementasyonda kullanicinin gercek GPS koordinatlari kullanilacak
        result = gmaps.reverse_geocode((DEFAULT_LOCATION["lat"], DEFAULT_LOCATION["lng"]))
        
        if result:
            # API response'undan adres bilgisini cek
            address_components = result[0]
            formatted_address = address_components.get('formatted_address', DEFAULT_LOCATION["address"])
            
            # Sehir ve ulke bilgisini cek
            city = _extract_city_from_geocode_result(address_components)
            country = _extract_country_from_geocode_result(address_components)
            
            logger.info("Google Geocoding API call successful")
            location_data = {
                "status": "success",
                "data": {
                    "lat": DEFAULT_LOCATION["lat"],
                    "lng": DEFAULT_LOCATION["lng"],
                    "address": formatted_address,
                    "city": city,
                    "country": country,
                    "accuracy": accuracy,
                    "timestamp": datetime.now().isoformat(),
                    "source": "google_geocoding_api",
                    "api_cost_usd": 0.005
                }
            }
            
            return location_data
        else:
            logger.warning("Google Geocoding API returned no results, falling back to mock data")
            # API'den sonuc alamazsa mock data kullan
            return await _get_location_mock_data(accuracy)
            
    except googlemaps.exceptions.ApiError as api_error:
        logger.error(f"Google Geocoding API error: {str(api_error)}")
        # Google API hatasi durumunda mock data'ya dusur
        return await _get_location_mock_data(accuracy)
    except googlemaps.exceptions.Timeout as timeout_error:
        logger.error(f"Google API timeout: {str(timeout_error)}")
        return await _get_location_mock_data(accuracy)
    except Exception as error:
        logger.error(f"Unexpected error in Google API call: {str(error)}")
        # Google API hatasi durumunda mock data'ya dusur
        return await _get_location_mock_data(accuracy)

def _extract_city_from_geocode_result(address_components: Dict) -> str:
    """Geocoding sonucundan sehir bilgisini cek"""
    components = address_components.get('address_components', [])
    for component in components:
        if 'locality' in component.get('types', []):
            return component.get('long_name', 'Sydney')
    return 'Sydney'

def _extract_country_from_geocode_result(address_components: Dict) -> str:
    """Geocoding sonucundan ulke bilgisini cek"""
    components = address_components.get('address_components', [])
    for component in components:
        if 'country' in component.get('types', []):
            return component.get('long_name', 'Australia')
    return 'Australia'

# Backward compatibility icin wrapper class
class LocationTool:
    """Backward compatibility icin LocationTool class wrapper"""
    
    def __init__(self):
        self.default_location = DEFAULT_LOCATION
    
    async def get_current_location(self, accuracy: str = "high") -> Dict[str, Any]:
        """Wrapper method - MCP tool'u cagir"""
        return await get_current_location(accuracy)
    
    async def calculate_distance(self, start_lat: float, start_lng: float,
                               end_lat: float, end_lng: float,
                               unit: str = "km") -> Dict[str, Any]:
        """Wrapper method - MCP tool'u cagir"""
        return await calculate_distance(start_lat, start_lng, end_lat, end_lng, unit)

# MCP tool instance'i olustur
location_tool = LocationTool() 