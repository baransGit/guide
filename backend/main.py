# Sydney Guide MCP Server
# Claude ile MCP protokolu uzerinden iletisim kuran ana server

import asyncio
import logging
import os
import json
from typing import Dict, Any, List
from pathlib import Path
from dotenv import load_dotenv

# .env dosyasini yukle
load_dotenv()

# MCP imports
try:
    from mcp import create_server, Server
    from mcp.types import Tool, TextContent
except ImportError:
    # Development fallback
    print("MCP package not found, using development mode")
    Server = None
    Tool = None
    TextContent = None

import websockets
from websockets.server import serve
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocketDisconnect
import uvicorn
from pydantic import BaseModel

# MCP Tools'lari import et
from mcp_tools.location_tool import get_current_location, calculate_distance
from mcp_tools.places_tool import search_places, get_place_details, get_places_by_type, get_popular_places
from mcp_tools.transport_tool import find_nearby_transport, plan_route, get_transport_status
from mcp_tools.notification_tool import send_notification, schedule_location_alerts, send_journey_reminders, start_journey_tracking, update_journey_location, stop_journey_tracking

# Logging ayarlari
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SydneyGuideMCPServer:
    """Sydney Guide MCP Server - Claude ile MCP protokolu uzerinden iletisim"""
    
    def __init__(self):
        self.is_running = False
        self.websocket_clients = set()
        
        # MCP tools'lari kaydet
        self.mcp_tools = {
            "get_current_location": get_current_location,
            "calculate_distance": calculate_distance,
            "search_places": search_places,
            "get_place_details": get_place_details,
            "get_places_by_type": get_places_by_type,
            "get_popular_places": get_popular_places,
            "find_nearby_transport": find_nearby_transport,
            "plan_route": plan_route,
            "get_transport_status": get_transport_status,
            "send_notification": send_notification,
            "schedule_location_alerts": schedule_location_alerts,
            "send_journey_reminders": send_journey_reminders,
            "start_journey_tracking": start_journey_tracking,
            "update_journey_location": update_journey_location,
            "stop_journey_tracking": stop_journey_tracking
        }
        
        # FastAPI app olustur
        self.app = FastAPI(
            title="Sydney Guide MCP Server",
            description="Claude ile MCP protokolu uzerinden iletisim kuran server",
            version="1.0.0"
        )
        self._setup_fastapi_routes()
        self._setup_cors()
        
        logger.info(f"MCP Server initialized with {len(self.mcp_tools)} tools")
    
    def _setup_cors(self):
        """CORS middleware ayarlari"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def _setup_fastapi_routes(self):
        """FastAPI routes - MCP WebSocket destegi icin"""
        
        @self.app.get("/")
        async def root():
            return {
                "message": "Sydney Guide MCP Server",
                "status": "running",
                "protocol": "MCP over WebSocket",
                "tools_count": len(self.mcp_tools),
                "tools": list(self.mcp_tools.keys())
            }
        
        @self.app.get("/health")
        async def health():
            return {
                "status": "healthy",
                "mcp_server": self.is_running,
                "tools": len(self.mcp_tools)
            }
        
        @self.app.websocket("/mcp")
        async def websocket_endpoint(websocket: WebSocket):
            """MCP WebSocket endpoint - Claude ile direkt iletisim"""
            await self.handle_mcp_websocket(websocket)
    
    async def handle_mcp_websocket(self, websocket: WebSocket):
        """MCP WebSocket baglantisini yonet"""
        await websocket.accept()
        self.websocket_clients.add(websocket)
        logger.info("new_mcp_websocket_connection")
        
        try:
            while True:
                try:
                    # Claude'dan gelen mesaji al
                    message = await websocket.receive_text()
                    logger.info(f"received_mcp_message: {message[:100]}...")
                    
                    # MCP mesajini parse et ve isle
                    response = await self.process_mcp_message(message)
                    
                    # Cevabi Claude'a gonder
                    await websocket.send_text(json.dumps(response))
                    logger.info(f"sent_mcp_response: {len(json.dumps(response))} bytes")
                    
                except WebSocketDisconnect:
                    logger.info("mcp_websocket_disconnected")
                    break
                except websockets.exceptions.ConnectionClosed:
                    logger.info("mcp_websocket_connection_closed_normally")
                    break
                except websockets.exceptions.ConnectionClosedError:
                    logger.info("mcp_websocket_connection_closed_error")
                    break
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error: {str(e)}")
                    error_response = {
                        "error": {
                            "code": -32700,
                            "message": "Parse error"
                        }
                    }
                    await websocket.send_text(json.dumps(error_response))
                except Exception as error:
                    logger.error(f"MCP message processing error: {str(error)}")
                    # Send error response but keep connection alive
                    error_response = {
                        "error": {
                            "code": -32603,
                            "message": f"Internal error: {str(error)}"
                        }
                    }
                    try:
                        await websocket.send_text(json.dumps(error_response))
                    except:
                        # If we can't send error response, connection is broken
                        break
                        
        except WebSocketDisconnect:
            logger.info("mcp_websocket_disconnected")
        except websockets.exceptions.ConnectionClosed:
            logger.info("mcp_websocket_connection_closed_normally")
        except Exception as error:
            logger.error(f"MCP WebSocket error: {error}")
        finally:
            self.websocket_clients.discard(websocket)
            logger.info("mcp_websocket_connection_closed")
    
    async def process_mcp_message(self, message: str) -> Dict[str, Any]:
        """MCP mesajini isle ve cevap dondur"""
        try:
            # JSON mesajini parse et
            mcp_request = json.loads(message)
            
            # MCP request tipine gore isle
            if mcp_request.get("method") == "tools/list":
                return self.list_tools()
            
            elif mcp_request.get("method") == "tools/call":
                tool_name = mcp_request.get("params", {}).get("name")
                tool_arguments = mcp_request.get("params", {}).get("arguments", {})
                return await self.call_tool(tool_name, tool_arguments)
            
            else:
                return {
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {mcp_request.get('method')}"
                    }
                }
                
        except json.JSONDecodeError:
            return {
                "error": {
                    "code": -32700,
                    "message": "parse_error_invalid_json"
                }
            }
        except Exception as error:
            return {
                "error": {
                    "code": -32603,
                    "message": f"internal_error: {str(error)}"
                }
            }
    
    def list_tools(self) -> Dict[str, Any]:
        """MCP tools listesini dondur"""
        tools = []
        
        for tool_name, tool_func in self.mcp_tools.items():
            try:
                # Tool metadata'sini guvende olustur
                mcp_parameters = getattr(tool_func, '_mcp_parameters', {})
                mcp_description = getattr(tool_func, '_mcp_description', None)
                
                # Eger parameters None ise bos dict kullan
                if mcp_parameters is None:
                    logger.warning(f"Tool {tool_name} has None parameters, using empty dict")
                    mcp_parameters = {}
                
                # Eger description None ise fallback kullan
                if mcp_description is None:
                    mcp_description = tool_func.__doc__ or f"{tool_name} tool"
                    logger.info(f"Tool {tool_name} using fallback description")
                
                # JSON serializable oldugunu kontrol et
                properties = dict(mcp_parameters) if isinstance(mcp_parameters, dict) else {}
                
                # Tool schema'yi olustur
                tool_schema = {
                    "name": tool_name,
                    "description": str(mcp_description).strip(),
                    "inputSchema": {
                        "type": "object",
                        "properties": properties,
                        "required": []
                    }
                }
                
                # JSON serialization test et
                json.dumps(tool_schema)
                tools.append(tool_schema)
                logger.debug(f"Tool {tool_name} added successfully")
                
            except Exception as error:
                logger.error(f"Error adding tool {tool_name}: {str(error)}")
                # Minimal fallback tool schema
                fallback_schema = {
                    "name": tool_name,
                    "description": f"Sydney Guide tool: {tool_name}",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
                tools.append(fallback_schema)
        
        logger.info(f"Returning {len(tools)} MCP tools to Claude")
        return {
            "result": {
                "tools": tools
            }
        }
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """MCP tool'u calistir"""
        try:
            if tool_name not in self.mcp_tools:
                return {
                    "error": {
                        "code": -32602,
                        "message": f"Tool not found: {tool_name}"
                    }
                }
            
            # Tool'u calistir
            tool_func = self.mcp_tools[tool_name]
            result = await tool_func(**arguments)
            
            return {
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            }
            
        except Exception as error:
            logger.error(f"Tool execution error: {str(error)}")
            return {
                "error": {
                    "code": -32603,
                    "message": f"Tool execution failed: {str(error)}"
                }
            }
    
    async def start_server(self, host: str = "localhost", port: int = 8888):
        """MCP server'i baslat"""
        logger.info(f"Starting Sydney Guide MCP Server on {host}:{port}")
        self.is_running = True
        
        # FastAPI server'i baslat
        config = uvicorn.Config(
            app=self.app,
            host=host,
            port=port,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()
    
    async def stop_server(self):
        """MCP server'i durdur"""
        logger.info("Stopping Sydney Guide MCP Server")
        self.is_running = False
        
        # Aktif WebSocket baglantilari kapat
        for websocket in self.websocket_clients:
            try:
                await websocket.close()
            except:
                pass
        
        self.websocket_clients.clear()

# Global server instance
server_instance = SydneyGuideMCPServer()

# FastAPI app instance for uvicorn (global olarak erisebilir)
app = server_instance.app

async def create_server():
    """Server instance olustur"""
    global server_instance
    return server_instance

if __name__ == "__main__":
    # Server'i baslat
    async def main():
        server = await create_server()
        await server.start_server()
    
    asyncio.run(main())