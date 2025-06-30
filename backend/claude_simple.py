#!/usr/bin/env python3
"""
Sydney Guide - Simplified Claude API Client
Working version without complex imports
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
import anthropic
import websockets

# Load environment variables
load_dotenv()

class SydneyClaudeSimple:
    """Simplified Claude API client"""
    
    def __init__(self):
        print("🎭 SYDNEY GUIDE - CLAUDE API")
        print("=" * 40)
        print("🤖 Real Claude + Sydney MCP Tools")
        
        # Initialize Claude API
        self.api_key = os.getenv('ANTHROPIC_API_KEY', '')
        if not self.api_key or 'your_' in self.api_key:
            print("❌ ANTHROPIC_API_KEY required!")
            sys.exit(1)
        
        self.claude = anthropic.Anthropic(api_key=self.api_key)
        self.mcp_ws = None
        self.mcp_tools = []
        
        # Set real API mode
        os.environ["MOCK_MODE"] = "false"
        
        print(f"✅ Claude API connected")
    
    async def connect_to_mcp_server(self, host: str = "localhost", port: int = 8888):
        """Connect to the MCP server"""
        try:
            print(f"🔌 Connecting to MCP server ({host}:{port})...")
            self.mcp_ws = await websockets.connect(f"ws://{host}:{port}/mcp")
            
            # Get available tools
            tools_request = {"method": "tools/list", "id": "get_tools"}
            await self.mcp_ws.send(json.dumps(tools_request))
            tools_response = await self.mcp_ws.recv()
            tools_data = json.loads(tools_response)
            
            if "result" in tools_data and "tools" in tools_data["result"]:
                self.mcp_tools = tools_data["result"]["tools"]
                print(f"✅ MCP server connected")
                print(f"🛠️ Available tools: {len(self.mcp_tools)}")
                for tool in self.mcp_tools[:5]:
                    print(f"   • {tool['name']}")
                if len(self.mcp_tools) > 5:
                    print(f"   ... and {len(self.mcp_tools) - 5} more")
                return True
            else:
                print("❌ Failed to get MCP tools")
                return False
                
        except Exception as error:
            print(f"❌ MCP connection failed: {str(error)}")
            return False
    
    async def call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call MCP tool through WebSocket"""
        if not self.mcp_ws:
            return {"error": "MCP server not connected"}
        
        try:
            tool_request = {
                "method": "tools/call",
                "id": f"call_{tool_name}",
                "params": {"name": tool_name, "arguments": arguments}
            }
            
            await self.mcp_ws.send(json.dumps(tool_request))
            response = await self.mcp_ws.recv()
            result = json.loads(response)
            
            return result.get("result", result)
                
        except Exception as error:
            return {"error": f"Tool call failed: {str(error)}"}
    
    def get_system_prompt(self) -> str:
        """Get system prompt for Claude"""
        return """You are Sydney Guide, an AI assistant for tourists visiting Sydney, Australia.

PERSONALITY:
- Friendly, helpful Australian local guide
- Proactive with suggestions
- Ask for location permission before using tools
- Explain you're using real-time Sydney data

AVAILABLE TOOLS:
- get_current_location: Get user's GPS location (ask permission first!)
- search_places: Find restaurants, attractions in Sydney  
- plan_route: Get transport directions
- calculate_distance: Calculate distances between places

CONVERSATION FLOW:
1. Introduce yourself warmly
2. Ask permission to access location for personalized recommendations  
3. When they agree, use get_current_location
4. Provide location-specific suggestions
5. Use search_places for food/attraction requests

Always mention you're using real-time Sydney data when calling tools."""
    
    async def process_with_claude(self, user_message: str, conversation_history: List[Dict]) -> str:
        """Process message with Claude API and MCP tools"""
        
        # Build messages for Claude
        messages = conversation_history + [{"role": "user", "content": user_message}]
        
        try:
            # Get Claude's response
            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                system=self.get_system_prompt(),
                messages=messages
            )
            
            claude_text = response.content[0].text
            
            # Enhance with MCP tools
            enhanced_text = await self.enhance_with_tools(claude_text, user_message)
            
            return enhanced_text
            
        except Exception as e:
            return f"Claude API error: {str(e)}"
    
    async def enhance_with_tools(self, claude_response: str, user_message: str) -> str:
        """Enhance Claude's response with MCP tool data"""
        
        user_lower = user_message.lower()
        enhanced_response = claude_response
        
        # Location permission granted
        if any(word in user_lower for word in ['yes', 'sure', 'ok', 'allow', 'permission']):
            print(f"📍 Getting user location...")
            location_result = await self.call_mcp_tool('get_current_location', {'accuracy': 'high'})
            
            if location_result.get('status') == 'success':
                address = location_result['data'].get('address', 'Sydney, Australia')
                enhanced_response += f"\n\n📍 **Perfect! You're at:** {address}\n\nNow I can provide personalized recommendations for your area!"
        
        # Food/restaurant requests
        food_keywords = ['food', 'restaurant', 'eat', 'hungry', 'vegan', 'halal', 'sushi', 'laksa', 'chinese', 'turkish', 'pizza', 'coffee']
        if any(word in user_lower for word in food_keywords):
            
            # Extract search terms
            search_terms = []
            if 'vegan' in user_lower: search_terms.append('vegan')
            if 'halal' in user_lower: search_terms.append('halal')
            if 'sushi' in user_lower: search_terms.append('sushi')
            if 'laksa' in user_lower: search_terms.append('laksa')
            if 'chinese' in user_lower: search_terms.append('chinese')
            if 'turkish' in user_lower: search_terms.append('turkish')
            if 'pizza' in user_lower: search_terms.append('pizza')
            if 'coffee' in user_lower: search_terms.append('coffee')
            
            if not search_terms:
                search_terms = ['restaurant']
            
            query = ' '.join(search_terms)
            
            print(f"🔍 Searching for: {query}")
            search_result = await self.call_mcp_tool('search_places', {
                'query': query,
                'lat': -33.8688,  # Sydney Opera House
                'lng': 151.2093,
                'max_results': 3
            })
            
            if search_result.get('status') == 'success' and search_result.get('data', {}).get('places'):
                places = search_result['data']['places']
                
                enhanced_response += f"\n\n🍽️ **I found some excellent {query} options using real-time data:**\n\n"
                
                for i, place in enumerate(places, 1):
                    enhanced_response += f"**{i}. {place['name']}**\n"
                    if place.get('rating'):
                        enhanced_response += f"   ⭐ {place['rating']}/5\n"
                    if place.get('address'):
                        enhanced_response += f"   📍 {place['address']}\n"
                    if place.get('distance'):
                        enhanced_response += f"   🚶 {place['distance']:.1f}km away\n"
                    enhanced_response += "\n"
                
                enhanced_response += "Would you like more details about any of these places?"
        
        return enhanced_response
    
    async def start_conversation(self):
        """Main conversation loop"""
        
        print(f"\n💬 **SYDNEY GUIDE CONVERSATION**")
        print("Real Claude API + Real Sydney Data")
        print("-" * 50)
        
        # Connect to MCP server first
        if not await self.connect_to_mcp_server():
            print("❌ Cannot start without MCP server")
            print("Start it with: cd backend && python3 main.py")
            return
        
        conversation_history = []
        
        # Initial greeting
        welcome = await self.process_with_claude(
            "Hello! I'm a tourist in Sydney. Please introduce yourself and ask for my location permission.",
            []
        )
        print(f"\n🤖 **Sydney Guide**: {welcome}")
        
        while True:
            try:
                user_input = input(f"\n👤 **You**: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    goodbye = await self.process_with_claude(
                        "The user is saying goodbye. Give a warm farewell.",
                        conversation_history
                    )
                    print(f"\n🤖 **Sydney Guide**: {goodbye}")
                    break
                
                if not user_input:
                    continue
                
                # Process with Claude + MCP tools
                print(f"\n🤖 **Sydney Guide**: ", end="", flush=True)
                response = await self.process_with_claude(user_input, conversation_history)
                print(response)
                
                # Update conversation history
                conversation_history.append({"role": "user", "content": user_input})
                conversation_history.append({"role": "assistant", "content": response})
                
                # Keep conversation manageable
                if len(conversation_history) > 10:
                    conversation_history = conversation_history[-8:]
                
            except KeyboardInterrupt:
                print(f"\n\n🤖 **Sydney Guide**: Thanks for using Sydney Guide! 🇦🇺")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
        
        # Close MCP connection
        if self.mcp_ws:
            await self.mcp_ws.close()

async def main():
    """Main function"""
    os.environ["MOCK_MODE"] = "false"
    client = SydneyClaudeSimple()
    await client.start_conversation()

if __name__ == "__main__":
    asyncio.run(main()) 