# Sydney Guide - Transport MCP Tool
# Sydney'de ulasim planlamasi ve istasyon bulan MCP araci

import asyncio
import json
import os
import math
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment configuration
USE_REAL_API = os.getenv('MOCK_MODE', 'true').lower() == 'false'
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')
NSW_TRANSPORT_API_KEY = os.getenv('NSW_TRANSPORT_API_KEY', '')

# Google Maps import (conditional)
try:
    import googlemaps
except ImportError:
    googlemaps = None

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

# Transport API integration configuration

# Mock transport data - Sydney ulasim verileri
TRANSPORT_STATIONS = {
    "central_station": {
        "stop_id": "central_station",
        "name": "Central Station",
        "type": "train",
        "lat": -33.8830,
        "lng": 151.2063,
        "address": "Central Station, Eddy Ave, Sydney NSW 2000",
        "services": ["t1", "t2", "t3", "t4", "t8", "airport_link"],
        "facilities": ["wheelchair_accessible", "parking", "shops", "toilets"]
    },
    "circular_quay": {
        "stop_id": "circular_quay",
        "name": "Circular Quay",
        "type": "ferry",
        "lat": -33.8611,
        "lng": 151.2107,
        "address": "Alfred St, Sydney NSW 2000",
        "services": ["ferry_manly", "ferry_parramatta", "ferry_taronga"],
        "facilities": ["wheelchair_accessible", "parking", "food"]
    },
    "wynyard_station": {
        "stop_id": "wynyard_station", 
        "name": "Wynyard Station",
        "type": "train",
        "lat": -33.8655,
        "lng": 151.2065,
        "address": "York St, Sydney NSW 2000",
        "services": ["t1", "t2", "t3", "t9"],
        "facilities": ["wheelchair_accessible", "shops", "underground"]
    },
    "qvb_bus_stop": {
        "stop_id": "qvb_bus_stop",
        "name": "QVB Bus Stop",
        "type": "bus",
        "lat": -33.8719,
        "lng": 151.2062,
        "address": "George St, Sydney NSW 2000",
        "services": ["bus_555", "bus_333", "bus_200"],
        "facilities": ["shelter", "real_time_display"]
    }
}

@mcp_tool(
    name="find_nearby_transport",
    description="Find nearby transport stations and stops",
    parameters={
        "lat": {"type": "number", "description": "Latitude coordinate"},
        "lng": {"type": "number", "description": "Longitude coordinate"},
        "transport_type": {
            "type": "string",
            "enum": ["all", "train", "bus", "ferry", "light_rail"],
            "default": "all",
            "description": "Type of transport to search for"
        },
        "radius": {"type": "number", "default": 1.0, "description": "Search radius in kilometers"},
        "max_results": {"type": "integer", "default": 5, "description": "Maximum number of results"}
    }
)
async def find_nearby_transport(lat: float, lng: float, transport_type: str = "all", 
                               radius: float = 1.0, max_results: int = 5) -> Dict[str, Any]:
    """
    Kullanicinin konumuna yakin ulasim duragi ve istasyonlari bul (mock veya gercek API)
    
    Args:
        lat: Enlem koordinati
        lng: Boylam koordinati
        transport_type: Ulasim tipi filtresi
        radius: Arama yaricapi (km)
        max_results: Maksimum sonuc sayisi
        
    Returns:
        Dict: Bulunan ulasim durakları ve istasyonlar
    """
    try:
        # Gercek Google Places API kullan (transit istasyonlari icin)
        if USE_REAL_API and GOOGLE_MAPS_API_KEY and GOOGLE_MAPS_API_KEY != "your_google_maps_api_key_here":
            return await _find_transport_real_api(lat, lng, transport_type, radius, max_results)
        
        # Mock verileri kullan (development icin)
        nearby_stations = []
        for station_id, station_data in TRANSPORT_STATIONS.items():
            # Transport tipi filtresi
            if transport_type != "all" and station_data["type"] != transport_type:
                continue
                
            # Mesafe hesapla
            distance = _calculate_distance(
                lat, lng, station_data["lat"], station_data["lng"]
            )
            
            # Radius filtresi
            if distance <= radius:
                station_with_distance = station_data.copy()
                station_with_distance["distance_km"] = round(distance, 2)
                nearby_stations.append(station_with_distance)
        
        # Mesafeye gore sirala
        nearby_stations.sort(key=lambda x: x["distance_km"])
        
        # Limit uygula
        limited_stations = nearby_stations[:max_results]
        
        return {
            "status": "success",
            "data": {
                "stations": limited_stations,
                "total_found": len(nearby_stations),
                "search_params": {
                    "location": {"lat": lat, "lng": lng},
                    "transport_type": transport_type,
                    "radius_km": radius,
                    "max_results": max_results
                },
                "timestamp": datetime.now().isoformat(),
                "source": "mock_database"
            }
        }
        
    except Exception as error:
        return {
            "status": "error",
            "message": f"Transport search failed: {str(error)}",
            "error_code": "TRANSPORT_SEARCH_ERROR",
            "timestamp": datetime.now().isoformat()
        }

@mcp_tool(
    name="plan_route",
    description="Plan route between two locations using public transport",
    parameters={
        "origin_lat": {"type": "number", "description": "Origin latitude"},
        "origin_lng": {"type": "number", "description": "Origin longitude"},
        "destination_lat": {"type": "number", "description": "Destination latitude"},
        "destination_lng": {"type": "number", "description": "Destination longitude"},
        "travel_modes": {
            "type": "array",
            "items": {"type": "string", "enum": ["walking", "transit", "bus", "train", "ferry"]},
            "default": ["transit", "walking"],
            "description": "Preferred travel modes"
        },
        "departure_time": {"type": "string", "default": "now", "description": "Departure time (ISO format or 'now')"}
    }
)
async def plan_route(origin_lat: float, origin_lng: float, 
                    destination_lat: float, destination_lng: float,
                    travel_modes: List[str] = ["transit", "walking"],
                    departure_time: str = "now") -> Dict[str, Any]:
    """
    Iki nokta arasinda toplu tasima ile rota planla
    
    Args:
        origin_lat: Baslangic noktasi enlemi
        origin_lng: Baslangic noktasi boylamı
        destination_lat: Varis noktasi enlemi
        destination_lng: Varis noktasi boylamı
        travel_modes: Tercih edilen ulasim turleri
        departure_time: Kalkis zamani
        
    Returns:
        Dict: Planlanan rota bilgileri
    """
    try:
        # Google Maps API'sini gercek projede kullan
        if USE_REAL_API and GOOGLE_MAPS_API_KEY and GOOGLE_MAPS_API_KEY != "your_google_maps_api_key_here":
            return await _get_real_directions(
                origin_lat, origin_lng, destination_lat, destination_lng,
                travel_modes, departure_time
            )
        
        # Mock rota verisi dondur
        total_distance = _calculate_distance(
            origin_lat, origin_lng, destination_lat, destination_lng
        )
        
        # Mock rota olustur - ama mantikli sekilde
        if total_distance < 0.5:  # Cok yakin mesafeler icin
            mock_route = {
                "overview": {
                    "total_distance_km": round(total_distance, 2),
                    "total_duration_minutes": max(round(total_distance * 12, 0), 1),  # Yuruyus hizi
                    "total_cost_aud": 0.0,  # Yakin mesafe, ucretsiz
                    "departure_time": departure_time,
                    "arrival_time": _calculate_arrival_time(departure_time, max(total_distance * 12, 1))
                },
                "steps": [
                    {
                        "step_number": 1,
                        "mode": "walking",
                        "instruction": "Walk directly to destination",
                        "distance_km": round(total_distance, 2),
                        "duration_minutes": max(round(total_distance * 12, 0), 1),
                        "start_location": {"lat": origin_lat, "lng": origin_lng},
                        "end_location": {"lat": destination_lat, "lng": destination_lng}
                    }
                ]
            }
        else:  # Uzak mesafeler icin toplu tasima
            walking_to_station = min(0.3, total_distance * 0.2)
            walking_from_station = min(0.3, total_distance * 0.2) 
            transit_distance = max(0.1, total_distance - walking_to_station - walking_from_station)
            
            mock_route = {
                "overview": {
                    "total_distance_km": round(total_distance, 2),
                    "total_duration_minutes": round(total_distance * 5, 0),  # 5 dakika/km ortalama
                    "total_cost_aud": round(total_distance * 2.5, 2),  # Ortalama maliyet
                    "departure_time": departure_time,
                    "arrival_time": _calculate_arrival_time(departure_time, total_distance * 5)
                },
                "steps": [
                    {
                        "step_number": 1,
                        "mode": "walking",
                        "instruction": "Walk to nearest transport station",
                        "distance_km": round(walking_to_station, 2),
                        "duration_minutes": round(walking_to_station * 12, 0),
                        "start_location": {"lat": origin_lat, "lng": origin_lng},
                        "end_location": {"lat": -33.8830, "lng": 151.2063}
                    },
                    {
                        "step_number": 2,
                        "mode": "train",
                        "instruction": "Take T1 Western Line to destination area",
                        "distance_km": round(transit_distance, 2),
                        "duration_minutes": round(transit_distance * 3, 0),
                        "line": "T1 Western Line",
                        "start_station": "Central Station",
                        "end_station": "Destination Station"
                    },
                    {
                        "step_number": 3,
                        "mode": "walking",
                        "instruction": "Walk to final destination",
                        "distance_km": round(walking_from_station, 2),
                        "duration_minutes": round(walking_from_station * 12, 0),
                        "start_location": {"lat": -33.8700, "lng": 151.2100},
                        "end_location": {"lat": destination_lat, "lng": destination_lng}
                    }
                ]
            }
        
        return {
            "status": "success",
            "data": {
                "route": mock_route,
                "alternative_routes": [],
                "travel_modes_used": travel_modes,
                "api_source": "google_directions_api" if (USE_REAL_API and GOOGLE_MAPS_API_KEY) else "mock_data",
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as error:
        return {
            "status": "error",
            "message": f"Route planning failed: {str(error)}",
            "error_code": "ROUTE_PLANNING_ERROR",
            "timestamp": datetime.now().isoformat()
        }

@mcp_tool(
    name="get_transport_status",
    description="Get real-time transport status and departures",
    parameters={
        "stop_id": {"type": "string", "description": "Transport stop or station ID"},
        "transport_type": {
            "type": "string", 
            "enum": ["train", "bus", "ferry", "light_rail"],
            "default": "train",
            "description": "Type of transport"
        },
        "limit": {"type": "integer", "default": 5, "description": "Number of upcoming departures"}
    }
)
async def get_transport_status(stop_id: str, transport_type: str = "train", 
                              limit: int = 5) -> Dict[str, Any]:
    """
    Ulasim duragi icin gercek zamanli kalkis bilgilerini al
    
    Args:
        stop_id: Durak veya istasyon ID'si
        transport_type: Ulasim tipi
        limit: Gosterilecek kalkis sayisi
        
    Returns:
        Dict: Gercek zamanli durak bilgileri
    """
    try:
        # Gercek NSW Transport API kullan
        if USE_REAL_API and NSW_TRANSPORT_API_KEY and NSW_TRANSPORT_API_KEY != "your_nsw_transport_api_key_here":
            return await _get_real_transport_status(stop_id, transport_type, limit)
        
        # Mock kalkis verileri olustur (sadece development modunda)
        departures = []
        base_time = datetime.now()
        
        # Gercek Sydney otobus numaralari kullan (mock data icin)
        real_bus_routes = {
            "bus": ["200", "333", "378", "380", "394", "396", "400", "L28", "M20", "M30"],
            "train": ["T1", "T2", "T3", "T4", "T8", "T9"],
            "ferry": ["F1", "F3", "F4", "F7", "F8"],
            "light_rail": ["L1", "L2", "L3"]
        }
        
        available_routes = real_bus_routes.get(transport_type, ["MOCK_001", "MOCK_002"])
        
        for i in range(limit):
            departure_time = base_time + timedelta(minutes=(i + 1) * 8)
            route_index = i % len(available_routes)
            
            departure = {
                "service_id": available_routes[route_index],
                "destination": f"City via {available_routes[route_index]}",
                "scheduled_time": departure_time.strftime("%H:%M"),
                "estimated_time": departure_time.strftime("%H:%M"),
                "delay_minutes": 0,
                "platform": f"Platform {(i % 4) + 1}",
                "service_status": "on_time",
                "wheelchair_accessible": True,
                "is_mock_data": True  # Acikca belirt ki bu mock data
            }
            departures.append(departure)
        
        # Durak bilgilerini al
        station_info = TRANSPORT_STATIONS.get(stop_id, {
            "stop_id": stop_id,
            "name": f"Station {stop_id}",
            "type": transport_type,
            "status": "operational"
        })
        
        return {
            "status": "success",
            "data": {
                "station_info": station_info,
                "departures": departures,
                "last_updated": datetime.now().isoformat(),
                "data_source": "mock_data_development_only",
                "service_alerts": [],
                "warning": "This is mock data for development - not real transport information"
            }
        }
        
    except Exception as error:
        return {
            "status": "error",
            "message": f"Transport status failed: {str(error)}",
            "error_code": "TRANSPORT_STATUS_ERROR",
            "timestamp": datetime.now().isoformat()
        }

async def _get_real_directions(origin_lat: float, origin_lng: float,
                              destination_lat: float, destination_lng: float,
                              travel_modes: List[str], departure_time: str) -> Dict[str, Any]:
    """
    Google Maps Directions API'sinden gercek rota verisi al
    """
    try:
        url = "https://maps.googleapis.com/maps/api/directions/json"
        
        params = {
            "origin": f"{origin_lat},{origin_lng}",
            "destination": f"{destination_lat},{destination_lng}",
            "mode": "transit",
            "key": GOOGLE_MAPS_API_KEY,
            "departure_time": "now" if departure_time == "now" else departure_time
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return _parse_google_directions(data)
                else:
                    raise Exception(f"Google Maps API error: {response.status}")
                    
    except Exception as error:
        # Hata durumunda mock data dondur
        return {
            "status": "error",
            "message": f"Google Maps API unavailable, using mock data: {str(error)}",
            "error_code": "API_FALLBACK"
        }

def _parse_google_directions(api_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Google Directions API cevabini standart formata cevir
    """
    try:
        if api_response.get('status') != 'OK':
            raise Exception(f"Google Directions API error: {api_response.get('status')}")
        
        routes = api_response.get('routes', [])
        if not routes:
            raise Exception("No routes found")
        
        # Ilk rota'yi al (genellikle en iyi rota)
        route = routes[0]
        legs = route.get('legs', [])
        if not legs:
            raise Exception("No route legs found")
        
        leg = legs[0]  # Tek leg varsayimi (tek destinasyon)
        
        # Rota adimlarini parse et
        steps = []
        step_number = 1
        
        for step_data in leg.get('steps', []):
            travel_mode = step_data.get('travel_mode', 'WALKING').lower()
            
            # Transit bilgilerini al
            transit_details = step_data.get('transit_details', {})
            
            step = {
                "step_number": step_number,
                "mode": _convert_google_travel_mode(travel_mode),
                "instruction": step_data.get('html_instructions', '').replace('<b>', '').replace('</b>', ''),
                "distance_km": round(step_data.get('distance', {}).get('value', 0) / 1000, 2),
                "duration_minutes": round(step_data.get('duration', {}).get('value', 0) / 60, 0),
                "start_location": {
                    "lat": step_data.get('start_location', {}).get('lat'),
                    "lng": step_data.get('start_location', {}).get('lng')
                },
                "end_location": {
                    "lat": step_data.get('end_location', {}).get('lat'),
                    "lng": step_data.get('end_location', {}).get('lng')
                }
            }
            
            # Transit detaylarini ekle
            if transit_details:
                line = transit_details.get('line', {})
                step.update({
                    "line": line.get('short_name', line.get('name', 'Unknown')),
                    "start_station": transit_details.get('departure_stop', {}).get('name'),
                    "end_station": transit_details.get('arrival_stop', {}).get('name'),
                    "agency": line.get('agencies', [{}])[0].get('name', 'Unknown'),
                    "vehicle_type": line.get('vehicle', {}).get('type', 'Unknown')
                })
            
            steps.append(step)
            step_number += 1
        
        # Genel rota bilgileri
        total_distance = leg.get('distance', {}).get('value', 0) / 1000  # km
        total_duration = leg.get('duration', {}).get('value', 0) / 60     # dakika
        
        # Transit bilgileri varsa ucret hesapla (tahmini)
        total_cost = _estimate_transit_cost(steps, total_distance)
        
        # Varis zamanini hesapla
        departure_time = "now"  # Placeholder
        arrival_time = _calculate_arrival_time(departure_time, total_duration)
        
        parsed_route = {
            "overview": {
                "total_distance_km": round(total_distance, 2),
                "total_duration_minutes": round(total_duration, 0),
                "total_cost_aud": total_cost,
                "departure_time": departure_time,
                "arrival_time": arrival_time,
                "start_address": leg.get('start_address', ''),
                "end_address": leg.get('end_address', '')
            },
            "steps": steps
        }
        
        return {
            "status": "success",
            "data": {
                "route": parsed_route,
                "alternative_routes": [],  # Diger rotalar burada eklenir
                "api_source": "google_directions_api",
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as error:
        return {
            "status": "error",
            "message": f"Failed to parse Google Directions response: {str(error)}",
            "error_code": "DIRECTIONS_PARSE_ERROR"
        }

def _convert_google_travel_mode(google_mode: str) -> str:
    """
    Google travel mode'unu bizim standart formata cevir
    """
    mapping = {
        "walking": "walking",
        "transit": "transit", 
        "driving": "driving",
        "bicycling": "cycling"
    }
    return mapping.get(google_mode.lower(), "walking")

def _estimate_transit_cost(steps: List[Dict], total_distance: float) -> float:
    """
    Transit adimlarindan tahmini ucret hesapla (Sydney Opal Card sistemi)
    """
    transit_steps = [step for step in steps if step.get('mode') == 'transit']
    
    if not transit_steps:
        return 0.0
    
    # Sydney Opal Card ucret sistemi (basit tahmini)
    base_fare = 4.20  # AUD - temel ucret
    distance_fare = total_distance * 0.50  # Distance-based ek ucret
    
    return round(min(base_fare + distance_fare, 15.80), 2)  # Maksimum gunluk cap

def _calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
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

def _calculate_arrival_time(departure_time: str, duration_minutes: float) -> str:
    """
    Kalkis zamani ve sure bilgisinden varis zamanini hesapla
    """
    if departure_time == "now":
        arrival = datetime.now() + timedelta(minutes=duration_minutes)
    else:
        # ISO format departure time'i parse et
        departure = datetime.fromisoformat(departure_time.replace('Z', '+00:00'))
        arrival = departure + timedelta(minutes=duration_minutes)
    
    return arrival.strftime("%H:%M")

async def _find_transport_real_api(lat: float, lng: float, transport_type: str, 
                                 radius: float, max_results: int) -> Dict[str, Any]:
    """
    Google Places API ile gercek transit istasyonlari bul
    """
    try:
        # Google Places API ile transit istasyonlari ara
        if not googlemaps:
            raise Exception("googlemaps package not installed")
        gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        
        # Transport tipine gore place type belirle
        place_types = {
            "train": ["train_station", "subway_station"],
            "bus": ["bus_station"],
            "ferry": ["ferry_terminal"],
            "light_rail": ["light_rail_station", "transit_station"],
            "all": ["transit_station", "train_station", "bus_station", "ferry_terminal"]
        }
        
        search_types = place_types.get(transport_type, ["transit_station"])
        all_stations = []
        
        for place_type in search_types:
            # Nearby search yap
            places_result = gmaps.places_nearby(
                location=(lat, lng),
                radius=int(radius * 1000),  # km'yi metre'ye cevir
                type=place_type
            )
            
            # Sonuclari parse et
            for place in places_result.get('results', []):
                distance = _calculate_distance(
                    lat, lng, 
                    place['geometry']['location']['lat'],
                    place['geometry']['location']['lng']
                )
                
                if distance <= radius:
                    station = {
                        "stop_id": place['place_id'],
                        "name": place['name'],
                        "type": _convert_google_type_to_transport_type(place.get('types', [])),
                        "lat": place['geometry']['location']['lat'],
                        "lng": place['geometry']['location']['lng'],
                        "address": place.get('vicinity', ''),
                        "rating": place.get('rating'),
                        "distance_km": round(distance, 2),
                        "google_place_id": place['place_id']
                    }
                    all_stations.append(station)
        
        # Mesafeye gore sirala ve limit uygula
        all_stations.sort(key=lambda x: x["distance_km"])
        limited_stations = all_stations[:max_results]
        
        return {
            "status": "success",
            "data": {
                "stations": limited_stations,
                "total_found": len(all_stations),
                "search_params": {
                    "location": {"lat": lat, "lng": lng},
                    "transport_type": transport_type,
                    "radius_km": radius,
                    "max_results": max_results
                },
                "timestamp": datetime.now().isoformat(),
                "source": "google_places_api"
            }
        }
        
    except Exception as error:
        # Hata durumunda mock data dondur
        return {
            "status": "error",
            "message": f"Google Places API error, falling back to mock data: {str(error)}",
            "error_code": "API_FALLBACK"
        }

async def _get_real_transport_status(stop_id: str, transport_type: str, limit: int) -> Dict[str, Any]:
    """
    NSW Transport API'den gercek zamanli durak bilgilerini al
    """
    try:
        # NSW Transport API endpoint
        base_url = "https://api.transport.nsw.gov.au/v1/tp"
        
        # Stop ID'yi NSW Transport format'a cevir
        nsw_stop_id = _convert_to_nsw_stop_id(stop_id, transport_type)
        
        # API request headers
        headers = {
            "Authorization": f"apikey {NSW_TRANSPORT_API_KEY}",
            "Accept": "application/json"
        }
        
        # Departures endpoint'ini cagir
        url = f"{base_url}/departure_mon"
        params = {
            "outputFormat": "rapidJSON",
            "coordOutputFormat": "EPSG:4326",
            "mode": _convert_transport_type_to_nsw_mode(transport_type),
            "type_dm": "stop",
            "name_dm": nsw_stop_id,
            "limit": limit,
            "departureMonitorMacro": "true",
            "itdDate": datetime.now().strftime("%Y%m%d"),
            "itdTime": datetime.now().strftime("%H%M")
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return _parse_nsw_transport_response(data, stop_id, transport_type)
                else:
                    error_text = await response.text()
                    raise Exception(f"NSW Transport API error {response.status}: {error_text}")
                    
    except Exception as error:
        # Hata durumunda mock data dondur ama WARNING ile
        return {
            "status": "warning",
            "message": f"NSW Transport API unavailable: {str(error)}",
            "data": {
                "station_info": {"stop_id": stop_id, "name": f"Station {stop_id}", "type": transport_type},
                "departures": [],
                "service_alerts": ["Real-time data temporarily unavailable"],
                "data_source": "api_fallback_mock",
                "last_updated": datetime.now().isoformat()
            }
        }

def _convert_to_nsw_stop_id(stop_id: str, transport_type: str) -> str:
    """
    Stop ID'yi NSW Transport API format'ina cevir
    """
    # Bu fonksiyon gercek NSW stop ID mapping'i icin kullanilir
    # Simdilik basit bir mapping
    mapping = {
        "central_station": "10101100",
        "circular_quay": "10101120", 
        "wynyard_station": "10101121",
        "qvb_bus_stop": "2121101"
    }
    return mapping.get(stop_id, stop_id)

def _convert_transport_type_to_nsw_mode(transport_type: str) -> str:
    """
    Transport tipini NSW API mode'una cevir
    """
    mapping = {
        "train": "1",
        "bus": "5", 
        "ferry": "9",
        "light_rail": "11"
    }
    return mapping.get(transport_type, "1")

def _convert_google_type_to_transport_type(google_types: List[str]) -> str:
    """
    Google Places API tiplerini bizim transport tipimize cevir
    """
    if "train_station" in google_types or "subway_station" in google_types:
        return "train"
    elif "bus_station" in google_types:
        return "bus"
    elif "ferry_terminal" in google_types:
        return "ferry"
    elif "light_rail_station" in google_types:
        return "light_rail"
    else:
        return "transit"

def _parse_nsw_transport_response(api_response: Dict[str, Any], stop_id: str, transport_type: str) -> Dict[str, Any]:
    """
    NSW Transport API cevabini standart formata cevir
    """
    try:
        departures = []
        
        # NSW API response structure'unu parse et
        stopEvents = api_response.get("stopEvents", [])
        
        for event in stopEvents:
            departure_data = event.get("departureTimePlanned", "")
            estimated_data = event.get("departureTimeEstimated", departure_data)
            
            # Route bilgilerini al
            transportation = event.get("transportation", {})
            route_number = transportation.get("number", "Unknown")
            destination = transportation.get("destination", {}).get("text", "Unknown")
            
            departure = {
                "service_id": route_number,
                "destination": destination,
                "scheduled_time": departure_data,
                "estimated_time": estimated_data,
                "delay_minutes": _calculate_delay_minutes(departure_data, estimated_data),
                "platform": event.get("location", {}).get("name", ""),
                "service_status": "on_time" if departure_data == estimated_data else "delayed",
                "wheelchair_accessible": transportation.get("properties", {}).get("WheelchairAccess", False),
                "is_real_time": True
            }
            departures.append(departure)
        
        return {
            "status": "success",
            "data": {
                "station_info": {
                    "stop_id": stop_id,
                    "name": api_response.get("locations", [{}])[0].get("name", f"Station {stop_id}"),
                    "type": transport_type,
                    "status": "operational"
                },
                "departures": departures,
                "last_updated": datetime.now().isoformat(),
                "data_source": "nsw_transport_api",
                "service_alerts": _extract_service_alerts(api_response)
            }
        }
        
    except Exception as error:
        raise Exception(f"Failed to parse NSW Transport response: {str(error)}")

def _calculate_delay_minutes(scheduled: str, estimated: str) -> int:
    """
    Scheduled ve estimated time'dan gecikme dakikasini hesapla
    """
    try:
        if not scheduled or not estimated or scheduled == estimated:
            return 0
        
        # Time parsing logic burada implement edilecek
        return 0  # Placeholder
    except:
        return 0

def _extract_service_alerts(api_response: Dict[str, Any]) -> List[str]:
    """
    NSW API response'undan service alert'leri cek
    """
    alerts = []
    # Service alerts parsing logic burada implement edilecek
    return alerts

# Backward compatibility icin wrapper class
class TransportTool:
    """Backward compatibility icin TransportTool class wrapper"""
    
    def __init__(self):
        self.stations_data = TRANSPORT_STATIONS
    
    async def find_nearby_transport(self, lat: float, lng: float, 
                                   transport_type: str = "all", radius: float = 1.0,
                                   max_results: int = 5) -> Dict[str, Any]:
        """Wrapper method - MCP tool'u cagir"""
        return await find_nearby_transport(lat, lng, transport_type, radius, max_results)
    
    async def plan_route(self, origin_lat: float, origin_lng: float,
                        destination_lat: float, destination_lng: float,
                        travel_modes: List[str] = ["transit", "walking"],
                        departure_time: str = "now") -> Dict[str, Any]:
        """Wrapper method - MCP tool'u cagir"""
        return await plan_route(origin_lat, origin_lng, destination_lat, 
                               destination_lng, travel_modes, departure_time)
    
    async def get_transport_status(self, stop_id: str, transport_type: str = "train",
                                  limit: int = 5) -> Dict[str, Any]:
        """Wrapper method - MCP tool'u cagir"""
        return await get_transport_status(stop_id, transport_type, limit)

# MCP tool instance'i olustur
transport_tool = TransportTool() 