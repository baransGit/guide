# Sydney Guide - Transport MCP Tool (Real NSW Transport API Implementation)
# Ulasim bilgilerini yoneten MCP araci - FIXED: Real NSW Transport API integration

import asyncio
import json
import math
import os
import logging
from typing import Dict, Any, List
from datetime import datetime
import aiohttp
from dotenv import load_dotenv

# Try to import googlemaps, but don't fail if not available
try:
    import googlemaps
except ImportError:
    googlemaps = None
    logger = logging.getLogger(__name__)
    logger.warning("googlemaps package not available, Google API features will be limited")

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

# Environment configuration
USE_REAL_API = os.getenv('MOCK_MODE', 'true').lower() == 'false'
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')
NSW_TRANSPORT_API_KEY = os.getenv('NSW_TRANSPORT_API_KEY', '')

# Logging configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Import pricing configuration
try:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from pricing_config import get_transport_pricing, get_api_costs
    logger.info("✅ Pricing config imported successfully")
except ImportError as e:
    logger.warning(f"⚠️ Could not import pricing_config: {e}")
    # Fallback pricing data
    def get_transport_pricing():
        return {
            "base_fare": 4.50,
            "distance_rate": 0.65,
            "daily_cap": 16.10,
            "off_peak_discount": 0.70
        }
    def get_api_costs():
        return {
            "nsw_transport": 0.01,
            "google_directions": 0.005,
            "google_places": 0.017
        }

# API usage tracking for cost monitoring with real pricing
api_usage_counter = {"directions_calls": 0, "transport_calls": 0, "total_cost_usd": 0.0}

def track_api_usage(api_type: str, calls: int = 1):
    """Track API usage with real costs from pricing config"""
    try:
        costs = get_api_costs()
        cost_per_call = costs.get(api_type, 0.01)
        
        api_usage_counter[f"{api_type}_calls"] = api_usage_counter.get(f"{api_type}_calls", 0) + calls
        api_usage_counter["total_cost_usd"] += (cost_per_call * calls)
        
        logger.info(f"API Usage: {api_type} +{calls} calls, cost: ${cost_per_call * calls:.4f}")
    except Exception as e:
        logger.warning(f"Could not track API usage: {e}")

def calculate_journey_fare(distance_km: float, peak_time: bool = True, transport_type: str = "train") -> float:
    """Calculate journey fare using real pricing config"""
    try:
        pricing = get_transport_pricing()
        base_fare = pricing["base_fare"]
        distance_rate = pricing["distance_rate"]
        daily_cap = pricing["daily_cap"]
        
        # Calculate base cost
        total_cost = base_fare + (distance_km * distance_rate)
        
        # Apply off-peak discount if applicable
        if not peak_time:
            off_peak_discount = pricing.get("off_peak_discount", 0.70)
            total_cost *= off_peak_discount
        
        # Apply daily cap
        return min(total_cost, daily_cap)
        
    except Exception as e:
        logger.warning(f"Could not calculate fare: {e}, using fallback")
        return round(4.50 + (distance_km * 0.65), 2)

async def find_nearby_transport(lat: float, lng: float, transport_type: str = "all", 
                               radius: float = 1.0, max_results: int = 5) -> Dict[str, Any]:
    """
    Yakin ulasim duraklarini bul (mock veya gercek API) - Same structure as places tool
    """
    try:
        if USE_REAL_API and GOOGLE_MAPS_API_KEY:
            # Gercek Google Places API kullan (transit stations)
            logger.info(f"Using real Google Places API for transport (type: {transport_type}, radius: {radius}km)")
            return await _find_transport_real_api(lat, lng, transport_type, radius, max_results)
        else:
            # Mock data kullan
            logger.info(f"Using mock transport data (type: {transport_type}, radius: {radius}km)")
            return await _find_transport_mock_data(lat, lng, transport_type, radius, max_results)
        
    except Exception as error:
        return {
            "status": "error",
            "message": f"Transport search failed: {str(error)}",
            "error_code": "TRANSPORT_SEARCH_ERROR",
            "timestamp": datetime.now().isoformat()
        }

async def plan_route(origin_lat: float, origin_lng: float, 
                    destination_lat: float, destination_lng: float,
                    travel_modes: List[str] = ["transit", "walking"],
                    departure_time: str = "now") -> Dict[str, Any]:
    """
    Rota planla (mock veya gercek API) - Same structure as places tool
    """
    try:
        if USE_REAL_API and GOOGLE_MAPS_API_KEY:
            # Gercek Google Directions API kullan
            logger.info(f"Using real Google Directions API for route planning")
            return await _plan_route_real_api(origin_lat, origin_lng, destination_lat, destination_lng, travel_modes, departure_time)
        else:
            # Mock data kullan
            logger.info(f"Using mock route data")
            return await _plan_route_mock_data(origin_lat, origin_lng, destination_lat, destination_lng, travel_modes, departure_time)
        
    except Exception as error:
        return {
            "status": "error",
            "message": f"Route planning failed: {str(error)}",
            "error_code": "ROUTE_PLANNING_ERROR",
            "timestamp": datetime.now().isoformat()
        }

async def get_transport_status(stop_id: str, transport_type: str = "train", limit: int = 5) -> Dict[str, Any]:
    """
    Ulasim durum bilgisi al (mock veya gercek API) - Same structure as places tool
    """
    try:
        if USE_REAL_API and NSW_TRANSPORT_API_KEY:
            # Gercek NSW Transport API kullan
            logger.info(f"Using real NSW Transport API for status (stop: {stop_id}, type: {transport_type})")
            return await _get_transport_status_real_api(stop_id, transport_type, limit)
        else:
            # Mock data kullan
            logger.info(f"Using mock transport status data (stop: {stop_id}, type: {transport_type})")
            return await _get_transport_status_mock_data(stop_id, transport_type, limit)
        
    except Exception as error:
        return {
            "status": "error",
            "message": f"Transport status failed: {str(error)}",
            "error_code": "TRANSPORT_STATUS_ERROR",
            "timestamp": datetime.now().isoformat()
        }

# Mock data implementations
async def _find_transport_mock_data(lat: float, lng: float, transport_type: str, radius: float, max_results: int) -> Dict[str, Any]:
    """Mock transport stations data"""
    mock_stations = [
        {
            "stop_id": "central_station",
            "name": "Central Station",
            "type": "train",
            "lat": -33.8830,
            "lng": 151.2063,
            "distance_km": round(_calculate_distance(lat, lng, -33.8830, 151.2063), 2),
            "services": ["T1", "T2", "T3", "T8"],
            "facilities": ["wheelchair_accessible", "shops"]
        },
        {
            "stop_id": "circular_quay",
            "name": "Circular Quay",
            "type": "ferry",
            "lat": -33.8611,
            "lng": 151.2107,
            "distance_km": round(_calculate_distance(lat, lng, -33.8611, 151.2107), 2),
            "services": ["Manly Ferry", "Parramatta Ferry"],
            "facilities": ["wheelchair_accessible", "food"]
        },
        {
            "stop_id": "wynyard_station",
            "name": "Wynyard Station", 
            "type": "train",
            "lat": -33.8655,
            "lng": 151.2065,
            "distance_km": round(_calculate_distance(lat, lng, -33.8655, 151.2065), 2),
            "services": ["T1", "T2", "T3", "T9"],
            "facilities": ["wheelchair_accessible", "shops", "underground"]
        }
    ]
    
    # Filter by transport type
    if transport_type != "all":
        mock_stations = [s for s in mock_stations if s["type"] == transport_type]
    
    # Filter by radius
    nearby_stations = [s for s in mock_stations if s["distance_km"] <= radius]
    
    # Sort by distance
    nearby_stations.sort(key=lambda x: x["distance_km"])
    
    # Apply limit
    limited_stations = nearby_stations[:max_results]
    
    return {
        "status": "success",
        "data": {
            "stations": limited_stations,
            "total_found": len(nearby_stations),
            "search_params": {
                "location": {"lat": lat, "lng": lng},
                "transport_type": transport_type,
                "radius_km": radius
            },
            "timestamp": datetime.now().isoformat(),
            "source": "mock_database"
        }
    }

async def _plan_route_mock_data(origin_lat: float, origin_lng: float, destination_lat: float, destination_lng: float, travel_modes: List[str], departure_time: str) -> Dict[str, Any]:
    """Mock route planning data with real pricing calculations"""
    distance_km = _calculate_distance(origin_lat, origin_lng, destination_lat, destination_lng)
    
    # Use real pricing calculations
    journey_cost = calculate_journey_fare(distance_km, peak_time=True, transport_type="train")
    
    mock_route = {
        "overview": {
            "total_distance_km": round(distance_km, 2),
            "total_duration_minutes": round(distance_km * 8, 0),  # 8 min/km average
            "total_cost_aud": round(journey_cost, 2),
            "departure_time": departure_time,
            "pricing_method": "real_opal_calculation"
        },
        "steps": [
            {
                "step_number": 1,
                "mode": "walking",
                "instruction": "Walk to transport",
                "distance_km": 0.3,
                "duration_minutes": 4
            },
            {
                "step_number": 2,
                "mode": "train",
                "instruction": "Take train to destination area",
                "distance_km": distance_km - 0.6,
                "duration_minutes": round((distance_km - 0.6) * 5, 0),
                "line": "T1 Western Line"
            },
            {
                "step_number": 3,
                "mode": "walking", 
                "instruction": "Walk to destination",
                "distance_km": 0.3,
                "duration_minutes": 4
            }
        ]
    }
    
    return {
        "status": "success",
        "data": mock_route,
        "timestamp": datetime.now().isoformat(),
        "source": "mock_directions"
    }

async def _get_transport_status_mock_data(stop_id: str, transport_type: str, limit: int) -> Dict[str, Any]:
    """Mock transport status data"""
    mock_status = {
        "stop_info": {
            "stop_id": stop_id,
            "name": f"{stop_id.replace('_', ' ').title()}",
            "type": transport_type
        },
        "services": [
            {
                "service_id": "T1_001",
                "line": "T1 Western Line",
                "destination": "Emu Plains",
                "scheduled_time": "10:25",
                "estimated_time": "10:27",
                "delay_minutes": 2,
                "platform": "1"
            },
            {
                "service_id": "T2_002", 
                "line": "T2 Inner West",
                "destination": "Leppington",
                "scheduled_time": "10:30",
                "estimated_time": "10:30",
                "delay_minutes": 0,
                "platform": "2"
            }
        ][:limit]
    }
    
    return {
        "status": "success",
        "data": mock_status,
        "timestamp": datetime.now().isoformat(),
        "source": "mock_realtime"
    }

# Real API implementations
async def _find_transport_real_api(lat: float, lng: float, transport_type: str, radius: float, max_results: int) -> Dict[str, Any]:
    """Real Google Places API for transport stations"""
    try:
        # Track API cost using real pricing
        track_api_usage("google_places", 1)
        
        # Google Maps client
        if googlemaps is None:
            logger.error("googlemaps package not available")
            return await _find_transport_mock_data(lat, lng, transport_type, radius, max_results)
        
        gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        
        # Map transport type to Google Places type
        place_types = {
            "train": "train_station",
            "bus": "bus_station", 
            "ferry": "ferry_terminal",
            "all": "transit_station"
        }
        
        google_type = place_types.get(transport_type, "transit_station")
        
        # Search for nearby transport
        places_result = gmaps.places_nearby(
            location=(lat, lng),
            radius=int(radius * 1000),  # Convert km to meters
            type=google_type
        )
        
        stations = []
        for place in places_result.get('results', [])[:max_results]:
            station_data = {
                "stop_id": place.get('place_id', ''),
                "name": place.get('name', ''),
                "type": transport_type if transport_type != "all" else "station",
                "lat": place.get('geometry', {}).get('location', {}).get('lat', 0),
                "lng": place.get('geometry', {}).get('location', {}).get('lng', 0),
                "distance_km": round(_calculate_distance(lat, lng, 
                    place.get('geometry', {}).get('location', {}).get('lat', 0),
                    place.get('geometry', {}).get('location', {}).get('lng', 0)), 2),
                "rating": place.get('rating', 0),
                "services": ["Real API - Check details"],
                "facilities": ["Real station data"]
            }
            stations.append(station_data)
        
        return {
            "status": "success",
            "data": {
                "stations": stations,
                "total_found": len(stations),
                "search_params": {
                    "location": {"lat": lat, "lng": lng},
                    "transport_type": transport_type,
                    "radius_km": radius
                },
                "timestamp": datetime.now().isoformat(),
                "source": "google_places_api",
                "api_cost_usd": 0.017
            }
        }
        
    except Exception as error:
        logger.error(f"Google Places API error: {str(error)}")
        return await _find_transport_mock_data(lat, lng, transport_type, radius, max_results)

async def _plan_route_real_api(origin_lat: float, origin_lng: float, destination_lat: float, destination_lng: float, travel_modes: List[str], departure_time: str) -> Dict[str, Any]:
    """Real Google Directions API for route planning"""
    try:
        # Track API cost using real pricing
        track_api_usage("google_directions", 1)
        
        # Google Maps client
        if googlemaps is None:
            logger.error("googlemaps package not available")
            return await _plan_route_mock_data(origin_lat, origin_lng, destination_lat, destination_lng, travel_modes, departure_time)
        
        gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        
        # Convert travel modes to Google format
        mode = "transit" if "transit" in travel_modes else "walking"
        
        # Get directions
        directions_result = gmaps.directions(
            origin=(origin_lat, origin_lng),
            destination=(destination_lat, destination_lng),
            mode=mode,
            departure_time="now"
        )
        
        if directions_result:
            route = directions_result[0]
            leg = route['legs'][0]
            
            # Parse steps
            steps = []
            for i, step in enumerate(leg['steps']):
                step_data = {
                    "step_number": i + 1,
                    "mode": step.get('travel_mode', '').lower(),
                    "instruction": step.get('html_instructions', '').replace('<', '').replace('>', ''),
                    "distance_km": round(step['distance']['value'] / 1000, 2),
                    "duration_minutes": round(step['duration']['value'] / 60, 0)
                }
                
                if 'transit_details' in step:
                    transit = step['transit_details']
                    step_data.update({
                        "line": transit.get('line', {}).get('short_name', ''),
                        "start_station": transit.get('departure_stop', {}).get('name', ''),
                        "end_station": transit.get('arrival_stop', {}).get('name', '')
                    })
                
                steps.append(step_data)
            
            mock_route = {
                "overview": {
                    "total_distance_km": round(leg['distance']['value'] / 1000, 2),
                    "total_duration_minutes": round(leg['duration']['value'] / 60, 0),
                    "total_cost_aud": 5.50,  # Approximate Sydney transit cost
                    "departure_time": departure_time
                },
                "steps": steps
            }
            
            # Add source to data for consistency
            mock_route["source"] = "google_directions_api"
            mock_route["api_cost_usd"] = 0.005
            
            return {
                "status": "success",
                "data": mock_route,
                "timestamp": datetime.now().isoformat(),
                "source": "google_directions_api",
                "api_cost_usd": 0.005
            }
        else:
            logger.warning("Google Directions API returned no results, falling back to mock data")
            return await _plan_route_mock_data(origin_lat, origin_lng, destination_lat, destination_lng, travel_modes, departure_time)
            
    except Exception as error:
        logger.error(f"Google Directions API error: {str(error)}")
        return await _plan_route_mock_data(origin_lat, origin_lng, destination_lat, destination_lng, travel_modes, departure_time)

async def _get_transport_status_real_api(stop_id: str, transport_type: str, limit: int) -> Dict[str, Any]:
    """Real NSW Transport API for real-time status - FIXED IMPLEMENTATION"""
    try:
        # Track API cost using real pricing
        track_api_usage("nsw_transport", 1)
        
        # NSW Transport API v1 - Fallback to v1 due to v2 authentication issues
        # Documentation: https://opendata.transport.nsw.gov.au/
        departure_url = "https://api.transport.nsw.gov.au/v1/tp/departure_mon"
        
        headers = {
            "Authorization": f"apikey {NSW_TRANSPORT_API_KEY}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Parameters for NSW Transport Departure API v2
        now = datetime.now()
        current_date = now.strftime("%Y%m%d")  # YYYYMMDD format
        current_time = now.strftime("%H%M")    # HHMM format
        
        params = {
            "outputFormat": "rapidJSON",
            "coordOutputFormat": "EPSG:4326",
            "mode": "direct",
            "type_dm": "stop",  # departure monitor for stops
            "name_dm": stop_id,  # stop identifier
            "departureMonitorMacro": "true",
            "itdDate": current_date,
            "itdTime": current_time,
            "useRealtime": "1",  # enable real-time data
            "excludedMeans": "checkbox",  # additional parameter for v2
            "TfNSWDM": "true"  # Transport for NSW departure monitor
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(departure_url, headers=headers, params=params) as response:
                logger.info(f"NSW Transport API response status: {response.status}")
                
                if response.status == 200:
                    try:
                        data = await response.json()
                        logger.info(f"NSW Transport API response received for stop: {stop_id}")
                        
                        # Parse NSW Transport API response - Handle different response formats
                        arrivals = []
                        
                        # Try different response structure formats
                        stop_events = None
                        if "stopEvents" in data:
                            stop_events = data["stopEvents"]
                        elif "departureList" in data:
                            stop_events = data["departureList"]
                        elif "departures" in data:
                            stop_events = data["departures"]
                        
                        if stop_events and len(stop_events) > 0:
                            for stop_event in stop_events[:limit]:
                                try:
                                    # Extract departure times
                                    departure = (stop_event.get("departureTimeEstimated") or 
                                               stop_event.get("estimatedTime") or 
                                               stop_event.get("departureTimePlanned", ""))
                                    planned = (stop_event.get("departureTimePlanned") or 
                                             stop_event.get("scheduledTime", ""))
                                    
                                    # Calculate delay
                                    delay_minutes = 0
                                    if departure and planned and departure != planned:
                                        try:
                                            if 'T' in departure and 'T' in planned:
                                                dep_time = datetime.fromisoformat(departure.replace('Z', '+00:00'))
                                                plan_time = datetime.fromisoformat(planned.replace('Z', '+00:00'))
                                                delay_minutes = int((dep_time - plan_time).total_seconds() / 60)
                                        except Exception as time_error:
                                            logger.warning(f"Time parsing error: {time_error}")
                                            delay_minutes = 0
                                    
                                    # Extract transportation info
                                    transportation = stop_event.get("transportation", {})
                                    if not transportation:
                                        transportation = stop_event.get("transport", {})
                                    
                                    # Build arrival data
                                    arrival_data = {
                                        "service_id": (transportation.get("number") or 
                                                     transportation.get("routeNo") or 
                                                     transportation.get("service_id", "Unknown")),
                                        "line": _format_transport_line(transportation),
                                        "destination": _extract_destination(transportation, stop_event),
                                        "scheduled_time": planned,
                                        "estimated_time": departure,
                                        "delay_minutes": delay_minutes,
                                        "platform": _extract_platform(stop_event),
                                        "realtime": stop_event.get("isRealtimeControlled", True)
                                    }
                                    arrivals.append(arrival_data)
                                    
                                except Exception as parse_error:
                                    logger.warning(f"Error parsing stop event: {parse_error}")
                                    continue
                        
                        # Get stop information
                        stop_info = _extract_stop_info(data, stop_id, transport_type)
                        
                        return {
                            "status": "success",
                            "data": {
                                "stop_info": stop_info,
                                "services": arrivals,
                                "total_services": len(arrivals)
                            },
                            "timestamp": datetime.now().isoformat(),
                            "source": "nsw_transport_api_v2",
                            "api_cost_usd": get_api_costs().get("nsw_transport", 0.01)
                        }
                        
                    except json.JSONDecodeError as json_error:
                        logger.error(f"NSW Transport API JSON decode error: {json_error}")
                        response_text = await response.text()
                        logger.error(f"Response content: {response_text[:500]}...")
                        return await _fallback_to_mock_with_error("json_decode_error", stop_id, transport_type, limit)
                    
                elif response.status == 401:
                    logger.error("NSW Transport API: Invalid API key")
                    return {
                        "status": "error",
                        "message": "NSW Transport API authentication failed",
                        "error_code": "API_AUTH_ERROR",
                        "timestamp": datetime.now().isoformat()
                    }
                    
                elif response.status == 429:
                    logger.error("NSW Transport API: Rate limit exceeded")
                    return {
                        "status": "error", 
                        "message": "NSW Transport API rate limit exceeded",
                        "error_code": "API_RATE_LIMIT",
                        "timestamp": datetime.now().isoformat()
                    }
                    
                else:
                    logger.error(f"NSW Transport API error: HTTP {response.status}")
                    error_text = await response.text()
                    logger.error(f"Response: {error_text}")
                    
                    # Fall back to mock data if API fails
                    logger.info("NSW Transport API failed, falling back to mock data")
                    return await _get_transport_status_mock_data(stop_id, transport_type, limit)
        
    except Exception as error:
        logger.error(f"NSW Transport API error: {str(error)}")
        # Fall back to mock data on exception
        return await _get_transport_status_mock_data(stop_id, transport_type, limit)

def _calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Calculate distance using Haversine formula"""
    lat1_rad = math.radians(lat1)
    lng1_rad = math.radians(lng1)
    lat2_rad = math.radians(lat2)
    lng2_rad = math.radians(lng2)
    
    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad
    
    a = (math.sin(dlat / 2) ** 2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    
    earth_radius_km = 6371
    return earth_radius_km * c

class TransportTool:
    """Transport tool wrapper for backward compatibility"""
    
    async def find_nearby_transport(self, lat: float, lng: float, transport_type: str = "all", radius: float = 1.0, max_results: int = 5) -> Dict[str, Any]:
        return await find_nearby_transport(lat, lng, transport_type, radius, max_results)
    
    async def plan_route(self, origin_lat: float, origin_lng: float, destination_lat: float, destination_lng: float, travel_modes: List[str] = ["transit", "walking"], departure_time: str = "now") -> Dict[str, Any]:
        return await plan_route(origin_lat, origin_lng, destination_lat, destination_lng, travel_modes, departure_time)
    
    async def get_transport_status(self, stop_id: str, transport_type: str = "train", limit: int = 5) -> Dict[str, Any]:
        return await get_transport_status(stop_id, transport_type, limit)

# Helper functions for NSW Transport API parsing
def _format_transport_line(transportation: Dict[str, Any]) -> str:
    """Format transport line information"""
    try:
        product_name = transportation.get('product', {}).get('name', '')
        number = transportation.get('number', '')
        route_no = transportation.get('routeNo', '')
        
        if product_name and number:
            return f"{product_name} {number}".strip()
        elif route_no:
            return f"Route {route_no}"
        elif number:
            return f"Service {number}"
        else:
            return "Unknown Service"
    except Exception:
        return "Unknown Service"

def _extract_destination(transportation: Dict[str, Any], stop_event: Dict[str, Any]) -> str:
    """Extract destination information"""
    try:
        # Try different destination fields
        destination = (transportation.get("destination", {}).get("name") or
                      transportation.get("destination") or
                      stop_event.get("destination", {}).get("name") or
                      stop_event.get("destination") or
                      "Unknown Destination")
        return str(destination)
    except Exception:
        return "Unknown Destination"

def _extract_platform(stop_event: Dict[str, Any]) -> str:
    """Extract platform/bay information"""
    try:
        platform = (stop_event.get("location", {}).get("name") or
                   stop_event.get("platform") or
                   stop_event.get("bay") or
                   "")
        return str(platform)
    except Exception:
        return ""

def _extract_stop_info(data: Dict[str, Any], stop_id: str, transport_type: str) -> Dict[str, Any]:
    """Extract stop information from API response"""
    try:
        locations = data.get("locations", [])
        if locations and len(locations) > 0:
            location = locations[0]
            return {
                "stop_id": stop_id,
                "name": location.get("name", stop_id),
                "type": transport_type,
                "coordinates": {
                    "lat": location.get("coord", [0, 0])[1] if location.get("coord") else 0,
                    "lng": location.get("coord", [0, 0])[0] if location.get("coord") else 0
                }
            }
        else:
            return {
                "stop_id": stop_id,
                "name": stop_id.replace("_", " ").title(),
                "type": transport_type,
                "coordinates": {"lat": 0, "lng": 0}
            }
    except Exception:
        return {
            "stop_id": stop_id,
            "name": stop_id,
            "type": transport_type,
            "coordinates": {"lat": 0, "lng": 0}
        }

async def _fallback_to_mock_with_error(error_type: str, stop_id: str, transport_type: str, limit: int) -> Dict[str, Any]:
    """Fallback to mock data when API fails"""
    logger.warning(f"Falling back to mock data due to {error_type}")
    mock_result = await _get_transport_status_mock_data(stop_id, transport_type, limit)
    mock_result["api_error"] = error_type
    mock_result["source"] = "mock_fallback"
    return mock_result
transport_tool = TransportTool()

