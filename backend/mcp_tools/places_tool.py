#!/usr/bin/env python3
"""
Places Tool - Clean Architecture Version
Uses organized fixtures from tests/fixtures/ instead of hardcoded data
Proper USE_REAL_API logic for all functions
"""

import logging
import os
from datetime import datetime
from typing import Dict, Any, List
import googlemaps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from correct location
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

# Environment variables
USE_REAL_API = os.getenv('MOCK_MODE', 'true').lower() == 'false'
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

# Import clean fixtures from tests directory  
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from tests.fixtures.mock_places_data import get_all_mock_places
    logger.info("✅ Successfully imported clean fixtures from tests/fixtures/")
except ImportError as e:
    logger.warning(f"❌ Could not import fixtures: {e}, using fallback")
    # Fallback to minimal mock data if fixtures fail
    def get_all_mock_places():
        return {
            "place_001": {
                "place_id": "place_001",
                "name": "Sydney Opera House", 
                "place_type": "tourist_attraction",
                "lat": -33.8568,
                "lng": 151.2153,
                "rating": 4.6,
                "price_level": 4,
                "description": "World-famous performing arts venue",
                "address": "Bennelong Point, Sydney NSW 2000"
            }
        }

# MCP Tool Decorator
def mcp_tool(name: str, description: str, parameters: dict = {}):
    """MCP tool decorator - enhanced version"""
    def decorator(func):
        func.mcp_tool_name = name
        func.mcp_tool_description = description
        func.mcp_tool_parameters = parameters
        return func
    return decorator

# =====================================
# MCP TOOLS - All with proper USE_REAL_API logic
# =====================================

@mcp_tool(
    name="search_places",
    description="Search places in Sydney with query, location, type and radius filters",
    parameters={
        "query": {"type": "string", "default": "", "description": "Search query"},
        "lat": {"type": "number", "default": -33.8688, "description": "Latitude coordinate"},
        "lng": {"type": "number", "default": 151.2093, "description": "Longitude coordinate"},
        "place_type": {
            "type": "string", 
            "enum": ["all", "restaurant", "tourist_attraction", "shopping_mall", "museum", "park", "transport"],
            "default": "all",
            "description": "Place type filter"
        },
        "radius": {"type": "number", "default": 5.0, "description": "Search radius in km"},
        "max_results": {"type": "integer", "default": 10, "description": "Maximum number of results"}
    }
)
async def search_places(query: str = "", 
                       lat: float = -33.8688, 
                       lng: float = 151.2093,
                       place_type: str = "all",
                       radius: float = 5.0,
                       max_results: int = 10) -> Dict[str, Any]:
    """
    Sydney'de mekan arama (mock veya gercek API)
    
    Returns:
        Dict: Arama sonuclari ve metadata
    """
    try:
        if USE_REAL_API and GOOGLE_MAPS_API_KEY:
            # Gercek Google Places API kullan
            return await _search_places_real_api(query, lat, lng, place_type, radius, max_results)
        else:
            # Mock data kullan
            return await _search_places_mock_data(query, lat, lng, place_type, radius, max_results)
        
    except Exception as error:
        return {
            "status": "error",
            "message": f"Places search failed: {str(error)}",
            "error_code": "SEARCH_ERROR",
            "timestamp": datetime.now().isoformat()
        }

@mcp_tool(
    name="get_place_details",
    description="Get detailed information for a specific place",
    parameters={
        "place_id": {"type": "string", "description": "Place ID (example: place_001)"}
    }
)
async def get_place_details(place_id: str) -> Dict[str, Any]:
    """
    Belirli bir mekanin detaylarini al
    
    Args:
        place_id: Mekan ID'si
        
    Returns:
        Dict: Mekan detaylari
    """
    try:
        if USE_REAL_API and GOOGLE_MAPS_API_KEY:
            # Gercek Google Places API kullan
            return await _get_place_details_real_api(place_id)
        else:
            # Mock data kullan
            return await _get_place_details_mock_data(place_id)
        
    except Exception as error:
        return {
            "status": "error",
            "message": f"Failed to get place details: {str(error)}",
            "error_code": "DETAIL_ERROR",
            "timestamp": datetime.now().isoformat()
        }

@mcp_tool(
    name="get_places_by_type",
    description="List places of specific type",
    parameters={
        "place_type": {
            "type": "string",
            "enum": ["restaurant", "tourist_attraction", "shopping_mall", "museum", "park", "transport"],
            "description": "Place type"
        },
        "limit": {"type": "integer", "default": 10, "description": "Maximum number of results"}
    }
)
async def get_places_by_type(place_type: str, limit: int = 10) -> Dict[str, Any]:
    """
    Tip bazinda mekan listesi - NOW WITH PROPER USE_REAL_API LOGIC
    
    Args:
        place_type: Mekan tipi
        limit: Maksimum sonuc sayisi
        
    Returns:
        Dict: Mekan listesi
    """
    try:
        if USE_REAL_API and GOOGLE_MAPS_API_KEY:
            # Gercek Google Places API kullan
            return await _get_places_by_type_real_api(place_type, limit)
        else:
            # Mock data kullan
            return await _get_places_by_type_mock_data(place_type, limit)
        
    except Exception as error:
        return {
            "status": "error",
            "message": f"Failed to get places by type: {str(error)}",
            "error_code": "TYPE_ERROR",
            "timestamp": datetime.now().isoformat()
        }

@mcp_tool(
    name="get_popular_places",
    description="Get most popular places by rating",
    parameters={
        "limit": {"type": "integer", "default": 5, "description": "Maximum number of results"}
    }
)
async def get_popular_places(limit: int = 5) -> Dict[str, Any]:
    """
    En populer mekanları al - NOW WITH PROPER USE_REAL_API LOGIC
    
    Args:
        limit: Maksimum sonuc sayisi
        
    Returns:
        Dict: Populer mekanlar
    """
    try:
        if USE_REAL_API and GOOGLE_MAPS_API_KEY:
            # Gercek Google Places API kullan
            return await _get_popular_places_real_api(limit)
        else:
            # Mock data kullan
            return await _get_popular_places_mock_data(limit)
        
    except Exception as error:
        return {
            "status": "error",
            "message": f"Failed to get popular places: {str(error)}",
            "error_code": "POPULAR_ERROR",
            "timestamp": datetime.now().isoformat()
        }

# =====================================
# MOCK DATA IMPLEMENTATIONS - Using Clean Fixtures
# =====================================

async def _search_places_mock_data(query: str, lat: float, lng: float, 
                                  place_type: str, radius: float, max_results: int) -> Dict[str, Any]:
    """Mock data ile mekan arama - using clean fixtures"""
    matching_places = []
    
    # Get clean fixtures data
    all_places = get_all_mock_places()
    
    # Tum mekanları tara
    for place_id, place_data in all_places.items():
        place_matches = True
        
        # Tip filtresi kontrolu
        if place_type != "all" and place_data.get("place_type") != place_type:
            place_matches = False
        
        # Sorgu filtresi kontrolu
        if query and place_matches:
            query_lower = query.lower()
            if not (query_lower in place_data.get("name", "").lower() or 
                   query_lower in place_data.get("description", "").lower()):
                place_matches = False
        
        # Mesafe filtresi kontrolu
        if place_matches:
            distance = _calculate_distance(
                lat, lng, place_data.get("lat", 0), place_data.get("lng", 0)
            )
            if distance <= radius:
                # Mesafe bilgisini ekle
                place_data_with_distance = place_data.copy()
                place_data_with_distance["distance_km"] = round(distance, 2)
                matching_places.append(place_data_with_distance)
    
    # Mesafeye gore sirala
    matching_places.sort(key=lambda x: x.get("distance_km", 0))
    
    # Maksimum sonuc sayisini uygula
    limited_places = matching_places[:max_results]
    
    return {
        "status": "success",
        "data": {
            "places": limited_places,
            "total_found": len(matching_places),
            "search_params": {
                "query": query,
                "location": {"lat": lat, "lng": lng},
                "place_type": place_type,
                "radius_km": radius,
                "max_results": max_results
            },
            "timestamp": datetime.now().isoformat(),
            "source": "clean_fixtures"
        }
    }

async def _get_place_details_mock_data(place_id: str) -> Dict[str, Any]:
    """Mock data'dan mekan detayları - using clean fixtures"""
    try:
        all_places = get_all_mock_places()
        
        if place_id in all_places:
            place_data = all_places[place_id]
            return {
                "status": "success", 
                "data": place_data,
                "timestamp": datetime.now().isoformat(),
                "source": "clean_fixtures"
            }
        else:
            return {
                "status": "error",
                "message": "Place not found in mock data",
                "error_code": "PLACE_NOT_FOUND",
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as error:
        return {
            "status": "error",
            "message": f"Failed to get mock place details: {str(error)}",
            "error_code": "MOCK_DETAIL_ERROR",
            "timestamp": datetime.now().isoformat()
        }

async def _get_places_by_type_mock_data(place_type: str, limit: int) -> Dict[str, Any]:
    """Mock data'dan tip bazinda mekan listesi - using clean fixtures"""
    try:
        all_places = get_all_mock_places()
        type_places = []
        
        for place_id, place_data in all_places.items():
            if place_data.get("place_type") == place_type:
                type_places.append(place_data.copy())
        
        # Rating'e gore sirala (yuksekten dusuge)
        type_places.sort(key=lambda x: x.get("rating", 0), reverse=True)
        
        # Limit uygula
        limited_places = type_places[:limit]
        
        return {
            "status": "success",
            "data": {
                "places": limited_places,
                "place_type": place_type,
                "total_found": len(type_places),
                "limit": limit,
                "timestamp": datetime.now().isoformat(),
                "source": "clean_fixtures"
            }
        }
        
    except Exception as error:
        return {
            "status": "error",
            "message": f"Failed to get mock places by type: {str(error)}",
            "error_code": "MOCK_TYPE_ERROR",
            "timestamp": datetime.now().isoformat()
        }

async def _get_popular_places_mock_data(limit: int) -> Dict[str, Any]:
    """Mock data'dan populer mekanlar - using clean fixtures"""
    try:
        all_places = get_all_mock_places()
        places_list = list(all_places.values())
        
        # Rating'e gore sirala (yuksekten dusuge)
        popular_places = sorted(places_list, key=lambda x: x.get("rating", 0), reverse=True)
        
        # Limit uygula
        top_places = popular_places[:limit]
        
        return {
            "status": "success",
            "data": {
                "places": top_places,
                "criteria": "highest_rating",
                "limit": limit,
                "timestamp": datetime.now().isoformat(),
                "source": "clean_fixtures"
            }
        }
        
    except Exception as error:
        return {
            "status": "error",
            "message": f"Failed to get popular places: {str(error)}",
            "error_code": "POPULAR_ERROR",
            "timestamp": datetime.now().isoformat()
        }

# =====================================
# REAL API IMPLEMENTATIONS - Google Places API
# =====================================

async def _search_places_real_api(query: str, lat: float, lng: float,
                                 place_type: str, radius: float, max_results: int) -> Dict[str, Any]:
    """Gercek Google Places API ile mekan arama"""
    try:
        gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        
        # Place type'i Google Places API formatina cevir
        google_place_type = _convert_place_type_to_google_format(place_type)
        
        # Text search if query provided, otherwise nearby search
        if query:
            places_result = gmaps.places(
                query=f"{query} in Sydney",
                location=(lat, lng),
                radius=radius * 1000,  # Convert km to meters
                type=google_place_type if place_type != "all" else None,
                language='en'
            )
        else:
            places_result = gmaps.places_nearby(
                location=(lat, lng),
                radius=radius * 1000,  # Convert km to meters
                type=google_place_type if place_type != "all" else None,
                language='en'
            )
        
        if not places_result or 'results' not in places_result:
            return {
                "status": "success",
                "data": {
                    "places": [],
                    "total_found": 0,
                    "search_params": {
                        "query": query,
                        "location": {"lat": lat, "lng": lng},
                        "place_type": place_type,
                        "radius_km": radius,
                        "max_results": max_results
                    },
                    "timestamp": datetime.now().isoformat(),
                    "source": "google_places_api"
                }
            }
        
        # Format results
        formatted_places = []
        for place in places_result['results'][:max_results]:
            formatted_place = _format_google_place_response(place, lat, lng)
            formatted_places.append(formatted_place)
        
        return {
            "status": "success",
            "data": {
                "places": formatted_places,
                "total_found": len(places_result['results']),
                "search_params": {
                    "query": query,
                    "location": {"lat": lat, "lng": lng},
                    "place_type": place_type,
                    "radius_km": radius,
                    "max_results": max_results
                },
                "timestamp": datetime.now().isoformat(),
                "source": "google_places_api"
            }
        }
        
    except Exception as error:
        logger.error(f"Google Places API error: {error}")
        return {
            "status": "error",
            "message": f"Google Places API error: {str(error)}",
            "error_code": "API_ERROR",
            "timestamp": datetime.now().isoformat()
        }

async def _get_place_details_real_api(place_id: str) -> Dict[str, Any]:
    """Gercek Google Places API'den mekan detayları"""
    try:
        gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        
        # Get place details from Google
        place_details = gmaps.place(
            place_id=place_id,
            fields=['name', 'rating', 'formatted_address', 'geometry', 'type', 
                   'opening_hours', 'formatted_phone_number', 'website', 'price_level',
                   'photo', 'review', 'user_ratings_total'],
            language='en'
        )
        
        if 'result' not in place_details:
            return {
                "status": "error",
                "message": "Place not found",
                "error_code": "PLACE_NOT_FOUND",
                "timestamp": datetime.now().isoformat()
            }
        
        place_data = place_details['result']
        formatted_place = _format_google_place_response(place_data, -33.8688, 151.2093)
        
        return {
            "status": "success",
            "data": formatted_place,
            "timestamp": datetime.now().isoformat(),
            "source": "google_places_api"
        }
        
    except Exception as error:
        logger.error(f"Google Place Details API error: {error}")
        return {
            "status": "error",
            "message": f"Google Places API error: {str(error)}",
            "error_code": "API_ERROR", 
            "timestamp": datetime.now().isoformat()
        }

async def _get_places_by_type_real_api(place_type: str, limit: int) -> Dict[str, Any]:
    """Gercek Google Places API'den tip bazinda mekan listesi"""
    try:
        gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        
        # Sydney center coordinates
        sydney_center = (-33.8688, 151.2093)
        
        # Convert to Google place type
        google_type = _convert_place_type_to_google_format(place_type)
        
        # Nearby search
        places_result = gmaps.places_nearby(
            location=sydney_center,
            radius=10000,  # 10km radius for city-wide search
            type=google_type,
            language='en'
        )
        
        if not places_result or 'results' not in places_result:
            return {
                "status": "success",
                "data": {
                    "places": [],
                    "place_type": place_type,
                    "total_found": 0,
                    "limit": limit,
                    "timestamp": datetime.now().isoformat(),
                    "source": "google_places_api"
                }
            }
        
        # Format results
        formatted_places = []
        for place in places_result['results'][:limit]:
            formatted_place = _format_google_place_response(place, sydney_center[0], sydney_center[1])
            formatted_places.append(formatted_place)
        
        # Sort by rating
        formatted_places.sort(key=lambda x: x.get("rating", 0), reverse=True)
        
        return {
            "status": "success",
            "data": {
                "places": formatted_places,
                "place_type": place_type,
                "total_found": len(places_result['results']),
                "limit": limit,
                "timestamp": datetime.now().isoformat(),
                "source": "google_places_api"
            }
        }
        
    except Exception as error:
        logger.error(f"Google Places API error: {error}")
        return {
            "status": "error",
            "message": f"Google Places API error: {str(error)}",
            "error_code": "API_ERROR",
            "timestamp": datetime.now().isoformat()
        }

async def _get_popular_places_real_api(limit: int) -> Dict[str, Any]:
    """Gercek Google Places API'den populer mekanlar"""
    try:
        gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        
        # Sydney center coordinates
        sydney_center = (-33.8688, 151.2093)
        
        # Search for highly rated places in Sydney
        places_result = gmaps.places(
            query="popular attractions restaurants Sydney",
            location=sydney_center,
            radius=15000,  # 15km radius for wider search
            language='en'
        )
        
        if not places_result or 'results' not in places_result:
            return {
                "status": "success",
                "data": {
                    "places": [],
                    "criteria": "highest_rating",
                    "limit": limit,
                    "timestamp": datetime.now().isoformat(),
                    "source": "google_places_api"
                }
            }
        
        # Format and filter highly rated places
        formatted_places = []
        for place in places_result['results']:
            if place.get('rating', 0) >= 4.0:  # Only highly rated places
                formatted_place = _format_google_place_response(place, sydney_center[0], sydney_center[1])
                formatted_places.append(formatted_place)
        
        # Sort by rating (highest first)
        formatted_places.sort(key=lambda x: x.get("rating", 0), reverse=True)
        
        # Apply limit
        top_places = formatted_places[:limit]
        
        return {
            "status": "success",
            "data": {
                "places": top_places,
                "criteria": "highest_rating",
                "limit": limit,
                "timestamp": datetime.now().isoformat(),
                "source": "google_places_api"
            }
        }
        
    except Exception as error:
        logger.error(f"Google Places API error: {error}")
        return {
            "status": "error",
            "message": f"Google Places API error: {str(error)}",
            "error_code": "API_ERROR",
            "timestamp": datetime.now().isoformat()
        }

# =====================================
# UTILITY FUNCTIONS
# =====================================

def _calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Haversine formulu ile iki nokta arasi mesafeyi km cinsinden hesapla"""
    import math
    
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

def _convert_place_type_to_google_format(place_type: str) -> str:
    """Yer tipini Google Places API formatina cevir"""
    type_mapping = {
        'restaurant': 'restaurant',
        'cafe': 'cafe',
        'tourist_attraction': 'tourist_attraction',
        'shopping_mall': 'shopping_mall',
        'park': 'park',
        'museum': 'museum',
        'bar': 'bar',
        'night_club': 'night_club',
        'gym': 'gym',
        'hospital': 'hospital',
        'bank': 'bank',
        'gas_station': 'gas_station',
        'lodging': 'lodging',
        'transport': 'transit_station'
    }
    return type_mapping.get(place_type, place_type)

def _format_google_place_response(google_place: Dict, search_lat: float, search_lng: float) -> Dict[str, Any]:
    """Google Places API yaniti format"""
    try:
        location = google_place.get('geometry', {}).get('location', {})
        place_lat = location.get('lat', 0)
        place_lng = location.get('lng', 0)
        
        # Calculate distance
        distance = _calculate_distance(search_lat, search_lng, place_lat, place_lng)
        
        # Format the response to match our standard structure
        formatted_place = {
            'place_id': google_place.get('place_id', ''),
            'name': google_place.get('name', ''),
            'address': google_place.get('formatted_address', google_place.get('vicinity', '')),
            'rating': google_place.get('rating', 0.0),
            'user_ratings_total': google_place.get('user_ratings_total', 0),
            'price_level': google_place.get('price_level', 0),
            'location': {
                'lat': place_lat,
                'lng': place_lng
            },
            'distance_km': round(distance, 2),
            'phone': google_place.get('formatted_phone_number', ''),
            'website': google_place.get('website', ''),
            'opening_hours': {
                'open_now': google_place.get('opening_hours', {}).get('open_now', False)
            },
            'photos': _extract_photo_references(google_place.get('photos', [])),
            'types': google_place.get('types', []),
            'place_type': _convert_google_type_to_our_format(google_place.get('types', []))
        }
        
        return formatted_place
        
    except Exception as error:
        logger.error(f"Error formatting Google place: {error}")
        return {}

def _convert_google_type_to_our_format(google_types: List[str]) -> str:
    """Google place types'i bizim formatimiza cevir"""
    # Priority mapping - first match wins
    type_priority = [
        'restaurant', 'tourist_attraction', 'shopping_mall', 
        'museum', 'park', 'cafe', 'bar', 'lodging'
    ]
    
    for our_type in type_priority:
        if our_type in google_types:
            return our_type
    
    # Fallback to first type or unknown
    return google_types[0] if google_types else 'unknown'

def _extract_photo_references(photos_data: list) -> list:
    """Google Photos data'dan referanslari cikart"""
    try:
        photo_refs = []
        for photo in photos_data[:3]:  # Maximum 3 photos
            if 'photo_reference' in photo:
                photo_refs.append({
                    'photo_reference': photo['photo_reference'],
                    'width': photo.get('width', 400),
                    'height': photo.get('height', 400)
                })
        return photo_refs
    except Exception as error:
        logger.error(f"Error extracting photo references: {error}")
        return []

# =====================================
# WRAPPER CLASS FOR COMPATIBILITY
# =====================================

class PlacesTool:
    """MCP Places Tool wrapper class - clean architecture version"""
    
    def __init__(self):
        logger.info("🏗️ PlacesTool initialized with clean fixtures architecture")
    
    async def search_places(self, query: str = "", lat: float = -33.8688, 
                           lng: float = 151.2093, place_type: str = "all",
                           radius: float = 5.0, max_results: int = 10) -> Dict[str, Any]:
        """Wrapper method - MCP tool'u cagir"""
        return await search_places(query, lat, lng, place_type, radius, max_results)
    
    async def get_place_details(self, place_id: str) -> Dict[str, Any]:
        """Wrapper method - MCP tool'u cagir"""
        return await get_place_details(place_id)
    
    async def get_places_by_type(self, place_type: str, limit: int = 10) -> Dict[str, Any]:
        """Wrapper method - MCP tool'u cagir"""
        return await get_places_by_type(place_type, limit)
    
    async def get_popular_places(self, limit: int = 5) -> Dict[str, Any]:
        """Wrapper method - MCP tool'u cagir"""
        return await get_popular_places(limit)

# MCP tool instance'i olustur
places_tool = PlacesTool()

# Export for backward compatibility
__all__ = [
    'search_places',
    'get_place_details', 
    'get_places_by_type',
    'get_popular_places',
    'places_tool'
] 