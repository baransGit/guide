# Sydney Guide - Places MCP Tool
# Sydney'deki mekanları ve yerleri bulan kapsamlı MCP araci

import asyncio
import json
import math
import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import aiohttp
import googlemaps
from dotenv import load_dotenv

# Setup logger
logger = logging.getLogger(__name__)

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

# Sydney'nin zengin mock verileri
PLACES_DATABASE = {
    # Tourist Attractions - Turistik Yerler
    "place_001": {
        "place_id": "place_001",
        "name": "Sydney Opera House",
        "place_type": "tourist_attraction",
        "lat": -33.8568,
        "lng": 151.2153,
        "address": "Bennelong Point, Sydney NSW 2000",
        "rating": 4.6,
        "price_level": 4,
        "description": "World-famous performing arts venue and architectural icon",
        "opening_hours": "Tours: 9:00 AM - 5:00 PM",
        "phone": "+61 2 9250 7111",
        "website": "sydneyoperahouse.com",
        "features": ["tours", "performances", "dining", "gift_shop"]
    },
    "place_002": {
        "place_id": "place_002", 
        "name": "Sydney Harbour Bridge",
        "place_type": "tourist_attraction",
        "lat": -33.8523,
        "lng": 151.2108,
        "address": "Sydney Harbour Bridge, Sydney NSW",
        "rating": 4.5,
        "price_level": 3,
        "description": "Iconic steel arch bridge with BridgeClimb experiences",
        "opening_hours": "BridgeClimb: Various times",
        "phone": "+61 2 8274 7777",
        "website": "bridgeclimb.com",
        "features": ["bridge_climb", "pylon_lookout", "walking", "cycling"]
    },
    
    # Restaurants - Restoranlar
    "place_003": {
        "place_id": "place_003",
        "name": "Quay Restaurant",
        "place_type": "restaurant",
        "lat": -33.8584,
        "lng": 151.2106,
        "address": "Upper Level, Overseas Passenger Terminal, The Rocks NSW 2000",
        "rating": 4.4,
        "price_level": 4,
        "cuisine": "modern_australian",
        "description": "Award-winning fine dining with harbour views",
        "opening_hours": "Tue-Sat: 6:00 PM - 10:00 PM",
        "phone": "+61 2 9251 5600",
        "website": "quay.com.au",
        "features": ["harbour_view", "fine_dining", "wine_list", "romantic"]
    },
    "place_004": {
        "place_id": "place_004",
        "name": "Bennelong Restaurant",
        "place_type": "restaurant", 
        "lat": -33.8568,
        "lng": 151.2153,
        "address": "Sydney Opera House, Bennelong Point NSW 2000",
        "rating": 4.2,
        "price_level": 4,
        "cuisine": "modern_australian",
        "description": "Fine dining inside the iconic Opera House",
        "opening_hours": "Tue-Sat: 5:30 PM - 10:00 PM",
        "phone": "+61 2 9240 8000",
        "website": "bennelong.com.au",
        "features": ["opera_house", "fine_dining", "harbour_view", "special_occasion"]
    },
    
    # Shopping - Alisveris
    "place_005": {
        "place_id": "place_005",
        "name": "Queen Victoria Building (QVB)",
        "place_type": "shopping_mall",
        "lat": -33.8719,
        "lng": 151.2062,
        "address": "455 George St, Sydney NSW 2000",
        "rating": 4.3,
        "price_level": 3,
        "description": "Historic shopping centre with luxury boutiques",
        "opening_hours": "Mon-Sat: 9:00 AM - 6:00 PM, Sun: 11:00 AM - 5:00 PM",
        "phone": "+61 2 9265 6800",
        "website": "qvb.com.au",
        "features": ["luxury_shopping", "historic_building", "dining", "fashion"]
    },
    "place_006": {
        "place_id": "place_006",
        "name": "Westfield Sydney",
        "place_type": "shopping_mall",
        "lat": -33.8704,
        "lng": 151.2065,
        "address": "188 Pitt St, Sydney NSW 2000",
        "rating": 4.1,
        "price_level": 3,
        "description": "Modern shopping center in Sydney CBD",
        "opening_hours": "Mon-Wed,Fri-Sat: 9:30 AM - 7:00 PM, Thu: 9:30 AM - 9:00 PM",
        "phone": "+61 2 8236 9200",
        "website": "westfield.com.au",
        "features": ["department_stores", "fashion", "food_court", "electronics"]
    },
    
    # Museums - Muzeler
    "place_007": {
        "place_id": "place_007",
        "name": "Australian Museum",
        "place_type": "museum",
        "lat": -33.8742,
        "lng": 151.2135,
        "address": "1 William St, Sydney NSW 2010",
        "rating": 4.2,
        "price_level": 2,
        "description": "Australia's first museum with natural history collections",
        "opening_hours": "Daily: 9:30 AM - 5:00 PM",
        "phone": "+61 2 9320 6000",
        "website": "australian.museum",
        "features": ["natural_history", "exhibitions", "planetarium", "family_friendly"]
    },
    "place_008": {
        "place_id": "place_008",
        "name": "Art Gallery of NSW",
        "place_type": "museum",
        "lat": -33.8688,
        "lng": 151.2168,
        "address": "Art Gallery Rd, The Domain NSW 2000",
        "rating": 4.4,
        "price_level": 1,
        "description": "Premier art gallery with Australian and international works",
        "opening_hours": "Daily: 10:00 AM - 5:00 PM",
        "phone": "+61 2 9225 1700",
        "website": "artgallery.nsw.gov.au",
        "features": ["australian_art", "international_art", "free_entry", "temporary_exhibitions"]
    },
    
    # Parks - Parklar
    "place_009": {
        "place_id": "place_009",
        "name": "Royal Botanic Gardens Sydney",
        "place_type": "park",
        "lat": -33.8642,
        "lng": 151.2166,
        "address": "Mrs Macquaries Rd, Sydney NSW 2000",
        "rating": 4.6,
        "price_level": 0,
        "description": "Historic botanical gardens with harbour views",
        "opening_hours": "Daily: 7:00 AM - sunset",
        "phone": "+61 2 9231 8111",
        "website": "botanicgardens.org.au",
        "features": ["botanical_gardens", "harbour_views", "walking_trails", "free_entry"]
    },
    "place_010": {
        "place_id": "place_010",
        "name": "Hyde Park",
        "place_type": "park",
        "lat": -33.8732,
        "lng": 151.2104,
        "address": "Elizabeth St, Sydney NSW 2000",
        "rating": 4.3,
        "price_level": 0,
        "description": "Historic city park in the heart of Sydney CBD",
        "opening_hours": "24 hours",
        "phone": "+61 2 9265 9333",
        "website": "cityofsydney.nsw.gov.au",
        "features": ["historic_park", "anzac_memorial", "walking_paths", "events"]
    },
    
    # Transport - Ulasim
    "place_011": {
        "place_id": "place_011",
        "name": "Circular Quay Station",
        "place_type": "transport",
        "lat": -33.8611,
        "lng": 151.2107,
        "address": "Alfred St, Sydney NSW 2000",
        "rating": 4.0,
        "price_level": 0,
        "description": "Major transport hub for trains, buses, and ferries",
        "opening_hours": "24 hours",
        "phone": "+61 131 500",
        "website": "transportnsw.info",
        "features": ["train_station", "ferry_terminal", "bus_stop", "taxi_rank"]
    },
    
    # Entertainment - Eglence
    "place_012": {
        "place_id": "place_012",
        "name": "State Theatre",
        "place_type": "entertainment",
        "lat": -33.8721,
        "lng": 151.2076,
        "address": "49 Market St, Sydney NSW 2000",
        "rating": 4.5,
        "price_level": 3,
        "description": "Historic theatre hosting musicals, concerts and events",
        "opening_hours": "Event dependent",
        "phone": "+61 2 9373 6655",
        "website": "statetheatre.com.au",
        "features": ["live_music", "theatre", "concerts", "historic_venue"]
    },
    
    # Vegan Restaurants - Surry Hills & Newtown (Gercek Sydney vegan sahnesi)
    "place_013": {
        "place_id": "place_013", 
        "name": "Yellow Food Store",
        "place_type": "restaurant",
        "lat": -33.8847,
        "lng": 151.2099,
        "address": "57 Macleay St, Potts Point NSW 2011",
        "rating": 4.7,
        "price_level": 2,
        "cuisine": "vegan",
        "description": "100% plant-based organic vegan restaurant and grocer",
        "opening_hours": "Daily: 7:00 AM - 8:00 PM",
        "phone": "+61 2 9357 3400",
        "website": "yellowfoodstore.com.au",
        "features": ["vegan", "organic", "gluten_free", "raw_food", "grocery"]
    },
    "place_014": {
        "place_id": "place_014",
        "name": "Gigi Pizzeria",
        "place_type": "restaurant", 
        "lat": -33.8964,
        "lng": 151.1794,
        "address": "379 King St, Newtown NSW 2042",
        "rating": 4.5,
        "price_level": 2,
        "cuisine": "vegan",
        "description": "Plant-based pizza with creative vegan toppings",
        "opening_hours": "Wed-Sun: 5:00 PM - 10:00 PM",
        "phone": "+61 2 9557 4332",
        "website": "gigipizzeria.com.au",
        "features": ["vegan", "pizza", "newtown", "casual_dining"]
    },
    "place_015": {
        "place_id": "place_015",
        "name": "Bodhi Restaurant Bar",
        "place_type": "restaurant",
        "lat": -33.8836,
        "lng": 151.2006,
        "address": "2/24 College St, Darlinghurst NSW 2010",
        "rating": 4.6,
        "price_level": 3,
        "cuisine": "vegan",
        "description": "Upscale vegan dining with innovative plant-based cuisine",
        "opening_hours": "Tue-Sat: 6:00 PM - 11:00 PM",
        "phone": "+61 2 9360 2523",
        "website": "bodhirestaurantbar.com.au",
        "features": ["vegan", "fine_dining", "cocktails", "date_night"]
    },
    "place_016": {
        "place_id": "place_016",
        "name": "About Life Newtown",
        "place_type": "restaurant",
        "lat": -33.8964,
        "lng": 151.1822,
        "address": "407-409 King St, Newtown NSW 2042", 
        "rating": 4.3,
        "price_level": 2,
        "cuisine": "vegan",
        "description": "Health food store with extensive vegan cafe menu",
        "opening_hours": "Daily: 8:00 AM - 8:00 PM",
        "phone": "+61 2 9517 4000",
        "website": "aboutlife.com.au",
        "features": ["vegan", "health_food", "organic", "grocery", "newtown"]
    },
    "place_017": {
        "place_id": "place_017",
        "name": "Baxter's Inn",
        "place_type": "entertainment",
        "lat": -33.8739,
        "lng": 151.2071,
        "address": "152-156 Clarence St, Sydney NSW 2000",
        "rating": 4.3,
        "price_level": 3,
        "description": "Hidden whiskey bar with extensive collection",
        "opening_hours": "Tue-Sat: 4:00 PM - 1:00 AM",
        "phone": "+61 2 9264 2382",
        "website": "baxtersinn.com",
        "features": ["whiskey_bar", "cocktails", "intimate", "hidden_entrance"]
    },
    
    # More Restaurants - Daha fazla restoran
    "place_014": {
        "place_id": "place_014",
        "name": "Din Tai Fung",
        "place_type": "restaurant",
        "lat": -33.8704,
        "lng": 151.2065,
        "address": "Level 1, Westfield Sydney, 188 Pitt St, Sydney NSW 2000",
        "rating": 4.1,
        "price_level": 2,
        "cuisine": "chinese",
        "description": "Famous taiwanese restaurant chain known for xiaolongbao",
        "opening_hours": "Daily: 11:00 AM - 9:00 PM",
        "phone": "+61 2 8236 9200",
        "website": "dintaifung.com.au",
        "features": ["xiaolongbao", "dumpling", "casual_dining", "family_friendly"]
    },
    "place_015": {
        "place_id": "place_015",
        "name": "Pancakes on the Rocks",
        "place_type": "restaurant",
        "lat": -33.8590,
        "lng": 151.2096,
        "address": "4 Hickson Rd, The Rocks NSW 2000",
        "rating": 4.0,
        "price_level": 2,
        "cuisine": "american",
        "description": "Popular pancake house with 24/7 service",
        "opening_hours": "Open 24 hours",
        "phone": "+61 2 9247 6371",
        "website": "pancakesontherocks.com.au",
        "features": ["24_hours", "pancakes", "casual_dining", "family_friendly"]
    },
    
    # More Shopping - Daha fazla alisveris
    "place_016": {
        "place_id": "place_016",
        "name": "The Strand Arcade",
        "place_type": "shopping_mall",
        "lat": -33.8697,
        "lng": 151.2078,
        "address": "412-414 George St, Sydney NSW 2000",
        "rating": 4.4,
        "price_level": 3,
        "description": "Beautiful Victorian-era shopping arcade",
        "opening_hours": "Mon-Sat: 9:00 AM - 6:00 PM, Sun: 11:00 AM - 5:00 PM",
        "phone": "+61 2 9232 4199",
        "website": "strandarcade.com.au",
        "features": ["historic_arcade", "boutique_shopping", "fashion", "jewelry"]
    },
    
    # More Tourist Attractions - Daha fazla turistik yerler
    "place_017": {
        "place_id": "place_017",
        "name": "Sydney Observatory",
        "place_type": "tourist_attraction",
        "lat": -33.8568,
        "lng": 151.2044,
        "address": "1003 Upper Fort St, Millers Point NSW 2000",
        "rating": 4.3,
        "price_level": 2,
        "description": "Historic observatory with telescope shows and harbor views",
        "opening_hours": "Daily: 10:00 AM - 5:00 PM",
        "phone": "+61 2 9921 3485",
        "website": "sydneyobservatory.com.au",
        "features": ["astronomy", "telescope", "harbor_views", "educational"]
    }
}

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
        if place_id not in PLACES_DATABASE:
            return {
                "status": "error",
                "message": f"Place with ID '{place_id}' not found",
                "error_code": "PLACE_NOT_FOUND",
                "timestamp": datetime.now().isoformat()
            }
        
        place_data = PLACES_DATABASE[place_id].copy()
        
        return {
            "status": "success",
            "data": {
                "place": place_data,
                "timestamp": datetime.now().isoformat()
            }
        }
        
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
    Tip bazinda mekan listesi
    
    Args:
        place_type: Mekan tipi
        limit: Maksimum sonuc sayisi
        
    Returns:
        Dict: Mekan listesi
    """
    try:
        type_places = []
        
        for place_id, place_data in PLACES_DATABASE.items():
            if place_data["place_type"] == place_type:
                type_places.append(place_data.copy())
        
        # Rating'e gore sirala (yuksekten dusuge)
        type_places.sort(key=lambda x: x["rating"], reverse=True)
        
        # Limit uygula
        limited_places = type_places[:limit]
        
        return {
            "status": "success",
            "data": {
                "places": limited_places,
                "place_type": place_type,
                "total_found": len(type_places),
                "limit": limit,
                "timestamp": datetime.now().isoformat()
            }
        }
        
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
    En populer mekanları al
    
    Args:
        limit: Maksimum sonuc sayisi
        
    Returns:
        Dict: Populer mekanlar
    """
    try:
        all_places = list(PLACES_DATABASE.values())
        
        # Rating'e gore sirala (yuksekten dusuge)
        popular_places = sorted(all_places, key=lambda x: x["rating"], reverse=True)
        
        # Limit uygula
        top_places = popular_places[:limit]
        
        return {
            "status": "success",
            "data": {
                "places": top_places,
                "criteria": "highest_rating",
                "limit": limit,
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as error:
        return {
            "status": "error",
            "message": f"Failed to get popular places: {str(error)}",
            "error_code": "POPULAR_ERROR",
            "timestamp": datetime.now().isoformat()
        }

def _calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Haversine formulu ile iki nokta arasi mesafeyi km cinsinden hesapla
    """
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

async def _get_location_name(lat: float, lng: float) -> str:
    """Koordinatlardan konum adini al (reverse geocoding)"""
    try:
        if USE_REAL_API and GOOGLE_MAPS_API_KEY:
            gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
            result = gmaps.reverse_geocode((lat, lng))
            if result:
                # Suburb/locality adini bul
                for component in result[0].get('address_components', []):
                    if 'locality' in component.get('types', []) or 'sublocality' in component.get('types', []):
                        return component['long_name']
                # Fallback olarak formatted_address'den suburb cikarmaya calis
                formatted_address = result[0].get('formatted_address', '')
                if 'NSW' in formatted_address:
                    parts = formatted_address.split(',')
                    for part in parts:
                        if 'NSW' in part:
                            suburb = part.replace('NSW', '').strip()
                            if suburb and len(suburb) > 2:
                                return suburb
        return ""
    except Exception as error:
        logger.error(f"Location name lookup error: {error}")
        return ""

# Mock ve Real API implementation functions

async def _search_places_mock_data(query: str, lat: float, lng: float, 
                                  place_type: str, radius: float, max_results: int) -> Dict[str, Any]:
    """Mock data ile mekan arama"""
    matching_places = []
    
    # Tum mekanları tara
    for place_id, place_data in PLACES_DATABASE.items():
        place_matches = True
        
        # Tip filtresi kontrolu
        if place_type != "all" and place_data["place_type"] != place_type:
            place_matches = False
        
        # Sorgu filtresi kontrolu
        if query and place_matches:
            query_lower = query.lower()
            if not (query_lower in place_data["name"].lower() or 
                   query_lower in place_data["description"].lower()):
                place_matches = False
        
        # Mesafe filtresi kontrolu
        if place_matches:
            distance = _calculate_distance(
                lat, lng, place_data["lat"], place_data["lng"]
            )
            if distance > radius:
                place_matches = False
            else:
                # Mesafe bilgisini ekle
                place_data_with_distance = place_data.copy()
                place_data_with_distance["distance_km"] = round(distance, 2)
                matching_places.append(place_data_with_distance)
    
    # Mesafeye gore sirala
    matching_places.sort(key=lambda x: x["distance_km"])
    
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
            "source": "mock_database"
        }
    }

async def _search_places_real_api(query: str, lat: float, lng: float,
                                 place_type: str, radius: float, max_results: int) -> Dict[str, Any]:
    """Gercek Google Places API ile mekan arama - gelismis konum tabanli arama"""
    try:
        # Google Maps client olustur
        gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        
        # Place type'i Google Places API formatina cevir
        google_place_type = _convert_place_type_to_google_format(place_type)
        
        # IMPROVED: Use text search for better location-specific results
        # Text search is better for finding specific cuisine types in specific areas
        if query and query.strip():
            # Try location-specific search first
            location_name = await _get_location_name(lat, lng)
            location_specific_query = f"{query} {location_name}" if location_name else query
            
            logger.info(f"Searching with location-specific query: '{location_specific_query}'")
            places_result = gmaps.places(
                query=location_specific_query,
                location=(lat, lng),
                radius=int(radius * 1000),  # km'yi metre'ye cevir
                language='en'
            )
            
            # If no results with location-specific query, try broader search
            if not places_result.get('results'):
                logger.info(f"No results with location-specific query, trying broader search: '{query}'")
                places_result = gmaps.places(
                    query=query,
                    location=(lat, lng),
                    radius=int(radius * 1000),
                    language='en'
                )
        else:
            # Fallback to nearby search if no query
            places_result = gmaps.places_nearby(
                location=(lat, lng),
                radius=int(radius * 1000),
                type=google_place_type if google_place_type != "all" else None,
                language='en'
            )
        
        if places_result.get('results'):
            formatted_places = []
            for place in places_result['results']:
                # Google API response'unu bizim formata cevir
                formatted_place = _format_google_place_response(place, lat, lng)
                
                # Apply place type filter if specified
                if place_type != "all":
                    place_types = place.get('types', [])
                    if not any(ptype in place_types for ptype in ['restaurant', 'food', 'establishment']):
                        continue
                
                formatted_places.append(formatted_place)
            
            # CRITICAL FIX: Sort by distance (closest first) - Google doesn't always return sorted
            formatted_places.sort(key=lambda x: x.get('distance_km', 999))
            
            # Apply max_results limit after sorting
            limited_places = formatted_places[:max_results]
            
            logger.info(f"Found {len(limited_places)} places, closest: {limited_places[0]['name'] if limited_places else 'none'} at {limited_places[0]['distance_km'] if limited_places else 'N/A'}km")
            
            return {
                "status": "success",
                "data": {
                    "places": limited_places,
                    "total_found": len(formatted_places),
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
        else:
            # API'den sonuc alamazsa mock data'ya dusur
            logger.warning("No results from Google Places API, falling back to mock data")
            return await _search_places_mock_data(query, lat, lng, place_type, radius, max_results)
            
    except Exception as error:
        # Google API hatasi durumunda mock data'ya dusur
        logger.error(f"Google Places API error, falling back to mock data: {error}")
        return await _search_places_mock_data(query, lat, lng, place_type, radius, max_results)

def _convert_place_type_to_google_format(place_type: str) -> str:
    """Bizim place type'ları Google Places API formatina cevir"""
    type_mapping = {
        "restaurant": "restaurant",
        "tourist_attraction": "tourist_attraction",
        "shopping_mall": "shopping_mall",
        "museum": "museum",
        "park": "park",
        "transport": "transit_station",
        "all": "all"
    }
    return type_mapping.get(place_type, "establishment")

def _format_google_place_response(google_place: Dict, search_lat: float, search_lng: float) -> Dict[str, Any]:
    """Google Places API response'unu bizim formata cevir"""
    place_lat = google_place['geometry']['location']['lat']
    place_lng = google_place['geometry']['location']['lng']
    
    # Mesafeyi hesapla
    distance_km = _calculate_distance(search_lat, search_lng, place_lat, place_lng)
    
    return {
        "place_id": google_place.get('place_id', 'unknown'),
        "name": google_place.get('name', 'Unknown Place'),
        "place_type": _convert_google_type_to_our_format(google_place.get('types', [])),
        "lat": place_lat,
        "lng": place_lng,
        "address": google_place.get('vicinity', 'Address not available'),
        "rating": google_place.get('rating', 0.0),
        "price_level": google_place.get('price_level', 0),
        "description": f"Google Places result: {google_place.get('name', 'Unknown Place')}",
        "opening_hours": "Check Google for hours",
        "distance_km": round(distance_km, 2),
        "source": "google_places_api"
    }

def _convert_google_type_to_our_format(google_types: List[str]) -> str:
    """Google Places API type'larini bizim formatimiza cevir"""
    # Oncelik sirasi ile type mapping
    priority_mapping = {
        "restaurant": "restaurant",
        "food": "restaurant", 
        "tourist_attraction": "tourist_attraction",
        "shopping_mall": "shopping_mall",
        "museum": "museum",
        "park": "park",
        "transit_station": "transport",
        "subway_station": "transport",
        "bus_station": "transport"
    }
    
    for google_type in google_types:
        if google_type in priority_mapping:
            return priority_mapping[google_type]
    
    return "tourist_attraction"  # Default

# Backward compatibility icin wrapper class
class PlacesTool:
    """Backward compatibility icin PlacesTool class wrapper"""
    
    def __init__(self):
        self.places_database = PLACES_DATABASE
    
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