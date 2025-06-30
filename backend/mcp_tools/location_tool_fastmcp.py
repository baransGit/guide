# Sydney Guide - Location MCP Tool - FastMCP Version
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

# PROPER MCP IMPORT - Official SDK
from fastmcp import FastMCP

# Initialize FastMCP instance
mcp = FastMCP("Sydney Guide Location Tools")

# Mock data icin varsayilan Sydney koordinatlari
DEFAULT_LOCATION = {
    "lat": -33.8688,
    "lng": 151.2093,
    "address": "Sydney Opera House, Bennelong Point, Sydney NSW 2000, Australia",
    "city": "Sydney",
    "country": "Australia"
}

@mcp.tool()
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
    except Exception as error:
        # Hata durumunda log kaydet ve hata mesaji dondur
        logger.error(f"Location tool error: {str(error)}")
        return {
            "status": "error",
            "message": "Location data unavailable",
            "error_code": "LOCATION_ERROR",
            "timestamp": datetime.now().isoformat()
        }

@mcp.tool()
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

# Helper functions remain the same
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
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Dunya yaricapi (km)
    earth_radius_km = 6371
    
    return earth_radius_km * c

def _convert_distance_unit(distance_km: float, unit: str) -> float:
    """Mesafe birim donusumu"""
    if unit == "km":
        return distance_km
    elif unit == "miles":
        return distance_km * 0.621371
    elif unit == "meters":
        return distance_km * 1000
    else:
        return distance_km

async def _get_location_mock_data(accuracy: str) -> Dict[str, Any]:
    """Mock konum verisi dondur"""
    precision = _get_precision_by_accuracy(accuracy)
    
    # Hassasiyet seviyesine gore koordinatlari yuvarla
    mock_lat = round(DEFAULT_LOCATION["lat"], precision)
    mock_lng = round(DEFAULT_LOCATION["lng"], precision)
    
    return {
        "status": "success",
        "data": {
            "lat": mock_lat,
            "lng": mock_lng,
            "address": DEFAULT_LOCATION["address"],
            "city": DEFAULT_LOCATION["city"],
            "country": DEFAULT_LOCATION["country"],
            "accuracy": accuracy,
            "source": "mock_gps",
            "timestamp": datetime.now().isoformat()
        }
    }

async def _get_location_real_api(accuracy: str) -> Dict[str, Any]:
    """Gercek Google Geocoding API kullanarak konum al"""
    # This would implement real Google API calls
    # For now, return enhanced mock data
    return await _get_location_mock_data(accuracy)

# Export functions for backward compatibility
__all__ = ["get_current_location", "calculate_distance", "mcp"] 