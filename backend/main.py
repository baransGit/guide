#!/usr/bin/env python3
"""
Sydney Guide MCP Server - BEST PRACTICE IMPLEMENTATION
Official MCP Python SDK + FastMCP Integration + Claude Integration System
"""

import os
import logging
from typing import Dict, Any, List
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables from parent directory  
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Import Claude Integration System
from claude_integration.system_prompts import get_system_prompt, get_localized_prompt
from claude_integration.tool_descriptions import get_tool_description, get_recommended_tools_for_scenario
from claude_integration.conversation_patterns import get_conversation_flow, format_response_template

# Import all MCP tools
from mcp_tools.location_tool import get_current_location, calculate_distance
from mcp_tools.places_tool import search_places, get_place_details, get_places_by_type, get_popular_places
from mcp_tools.transport_tool import find_nearby_transport, plan_route, get_transport_status
from mcp_tools.notification_tool import send_notification, schedule_location_alerts, send_journey_reminders, start_journey_tracking, update_journey_location, stop_journey_tracking

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP with Claude Integration
mcp = FastMCP("Sydney Guide MCP Server")

# Add system prompt configuration
@mcp.prompt()
def sydney_guide_system_prompt(language: str = "english", scenario: str = "general") -> str:
    """Sydney Guide sistem prompt'u - Claude icin kisilik ve talimatlar"""
    return get_localized_prompt(language, scenario)

# Register all MCP tools with Claude Integration descriptions
@mcp.tool()
async def get_current_location_mcp(accuracy: str = "high") -> Dict[str, Any]:
    """Kullanicinin mevcut konumunu al - Claude Integration enabled"""
    return await get_current_location(accuracy)

@mcp.tool()
async def calculate_distance_mcp(start_lat: float, start_lng: float, 
                               end_lat: float, end_lng: float, unit: str = "km") -> Dict[str, Any]:
    """Iki nokta arasindaki mesafeyi hesapla"""
    return await calculate_distance(start_lat, start_lng, end_lat, end_lng, unit)

@mcp.tool()
async def search_places_mcp(query: str = "", lat: float = -33.8688, lng: float = 151.2093,
                           place_type: str = "all", radius: float = 5.0, max_results: int = 10) -> Dict[str, Any]:
    """Sydney'de yer ara - Claude Integration enabled"""
    return await search_places(query, lat, lng, place_type, radius, max_results)

@mcp.tool()
async def get_place_details_mcp(place_id: str) -> Dict[str, Any]:
    """Yer detaylarini al"""
    return await get_place_details(place_id)

@mcp.tool()
async def get_places_by_type_mcp(place_type: str, limit: int = 10) -> Dict[str, Any]:
    """Tip bazinda yer listesi al"""
    return await get_places_by_type(place_type, limit)

@mcp.tool()
async def get_popular_places_mcp(limit: int = 5) -> Dict[str, Any]:
    """Populer yerleri al"""
    return await get_popular_places(limit)

@mcp.tool()
async def find_nearby_transport_mcp(lat: float, lng: float, transport_type: str = "all",
                                  radius: float = 1.0, max_results: int = 5) -> Dict[str, Any]:
    """Yakin ulasim duraklarini bul - Claude Integration enabled"""
    return await find_nearby_transport(lat, lng, transport_type, radius, max_results)

@mcp.tool()
async def plan_route_mcp(origin_lat: float, origin_lng: float, destination_lat: float, destination_lng: float,
                        travel_modes: List[str] = ["transit", "walking"], departure_time: str = "now") -> Dict[str, Any]:
    """Rota planla - Claude Integration enabled"""
    return await plan_route(origin_lat, origin_lng, destination_lat, destination_lng, travel_modes, departure_time)

@mcp.tool()
async def get_transport_status_mcp(stop_id: str, transport_type: str = "train", limit: int = 5) -> Dict[str, Any]:
    """Ulasim durum bilgisi al"""
    return await get_transport_status(stop_id, transport_type, limit)

@mcp.tool()
async def send_notification_mcp(user_token: str, title: str, body: str, priority: str = "medium") -> Dict[str, Any]:
    """Bildirim gonder - Claude Integration enabled"""
    return await send_notification(user_token, title, body, priority)

@mcp.tool()
async def schedule_location_alerts_mcp(user_token: str, journey_waypoints: List[Dict[str, Any]],
                                     alert_radius: float = 500, alert_types: List[str] = ["all"]) -> Dict[str, Any]:
    """Konum bazli uyari ayarla"""
    return await schedule_location_alerts(user_token, journey_waypoints, alert_radius, alert_types)

@mcp.tool()
async def send_journey_reminders_mcp(user_token: str, journey_plan: Dict[str, Any],
                                   reminder_minutes: List[int] = [15, 5]) -> Dict[str, Any]:
    """Yolculuk hatirlatici gonder"""
    return await send_journey_reminders(user_token, journey_plan, reminder_minutes)

@mcp.tool()
async def start_journey_tracking_mcp(user_token: str, journey_plan: Dict[str, Any],
                                   tracking_options: Dict[str, Any] = {}) -> Dict[str, Any]:
    """Yolculuk takibini baslat"""
    return await start_journey_tracking(user_token, journey_plan, tracking_options or {})

@mcp.tool()
async def update_journey_location_mcp(session_id: str, current_location: Dict[str, Any],
                                    movement_data: Dict[str, Any] = {}) -> Dict[str, Any]:
    """Yolculuk konumunu guncelle"""  
    return await update_journey_location(session_id, current_location, movement_data or {})

@mcp.tool()
async def stop_journey_tracking_mcp(session_id: str) -> Dict[str, Any]:
    """Yolculuk takibini durdur"""
    return await stop_journey_tracking(session_id)

if __name__ == "__main__":
    # Run with FastMCP + Claude Integration System
    logger.info("Starting Sydney Guide MCP Server with Claude Integration")
    logger.info("System prompts, conversation patterns, and tool descriptions loaded")
    logger.info("All MCP tools registered for Claude")
    
    # Log integration status
    try:
        system_prompt = get_system_prompt("english", "general")
        logger.info("✅ Claude Integration System loaded successfully")
    except Exception as e:
        logger.warning(f"⚠️ Claude Integration System error: {e}")
        logger.info("Server will run with basic MCP tools only")
    
    # Run the MCP server
    mcp.run() 