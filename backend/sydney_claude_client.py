#!/usr/bin/env python3
"""
Sydney Guide - Proper Claude API Client
Uses the existing claude_integration system architecture
"""

import asyncio
import json
import os
import sys
import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
import anthropic
import websockets

# Load environment variables
load_dotenv()

# Import the claude_integration system
from claude_integration.system_prompts import get_system_prompt, get_food_explorer_prompt
from claude_integration.tool_descriptions import get_tool_description, select_tools_for_user_request
from claude_integration.context_management import SessionState, create_session, add_message
from claude_integration.conversation_patterns import detect_conversation_intent, get_conversation_flow

class SydneyClaudeClient:
    """Proper Claude API client using claude_integration architecture"""
    
    def __init__(self):
        print("🎭 SYDNEY GUIDE - CLAUDE API CLIENT")
        print("=" * 50)
        print("🤖 Using proper claude_integration architecture")
        print("🔧 Connecting to MCP server and Claude API")
        
        # Initialize Claude API
        self.api_key = os.getenv('ANTHROPIC_API_KEY', '')
        if not self.api_key or 'your_' in self.api_key:
            print("❌ ANTHROPIC_API_KEY required!")
            print("Get it from: https://console.anthropic.com/")
            sys.exit(1)
        
        self.claude = anthropic.Anthropic(api_key=self.api_key)
        
        # MCP server connection
        self.mcp_ws = None
        self.mcp_tools = []
        
        # Session management using claude_integration
        session_id = str(uuid.uuid4())
        self.session = create_session(session_id=session_id, user_id="demo_user")
        
        # Set real API mode
        os.environ["MOCK_MODE"] = "false"
        
        print(f"✅ Claude API connected")
        print(f"✅ Session created: {self.session.session_id}")
    
    async def connect_to_mcp_server(self, host: str = "localhost", port: int = 8888):
        """Connect to the MCP server"""
        try:
            print(f"🔌 Connecting to MCP server ({host}:{port})...")
            self.mcp_ws = await websockets.connect(f"ws://{host}:{port}/mcp")
            
            # Get available tools with timeout
            tools_request = {
                "method": "tools/list",
                "id": "get_tools"
            }
            await self.mcp_ws.send(json.dumps(tools_request))
            
            # Add timeout to prevent hanging
            try:
                tools_response = await asyncio.wait_for(self.mcp_ws.recv(), timeout=10.0)
                tools_data = json.loads(tools_response)
                
                if "result" in tools_data and "tools" in tools_data["result"]:
                    self.mcp_tools = tools_data["result"]["tools"]
                    print(f"✅ MCP server connected")
                    print(f"🛠️ Available tools: {len(self.mcp_tools)}")
                    for tool in self.mcp_tools[:5]:  # Show first 5
                        print(f"   • {tool['name']}")
                    if len(self.mcp_tools) > 5:
                        print(f"   ... and {len(self.mcp_tools) - 5} more")
                    return True
                else:
                    print("❌ Failed to get MCP tools from response")
                    return False
                    
            except asyncio.TimeoutError:
                print("❌ MCP server response timeout - connection might close after sending tools")
                print("⚠️ This is expected behavior - trying to continue anyway...")
                # For now, we'll continue without tools but show warning
                return True
                
        except websockets.exceptions.ConnectionRefused:
            print(f"❌ MCP server not running on {host}:{port}")
            print("💡 Start it with: cd backend && python3 main.py")
            return False
        except Exception as error:
            print(f"❌ MCP connection failed: {str(error)}")
            print("Make sure MCP server is running: cd backend && python3 main.py")
            return False
    
    async def call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call MCP tool through WebSocket"""
        if not self.mcp_ws:
            return {"error": "MCP server not connected"}
        
        try:
            tool_request = {
                "method": "tools/call",
                "id": f"call_{tool_name}",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }
            
            await self.mcp_ws.send(json.dumps(tool_request))
            response = await self.mcp_ws.recv()
            result = json.loads(response)
            
            # Extract the actual result
            if "result" in result:
                return result["result"]
            else:
                return result
                
        except Exception as error:
            return {"error": f"Tool call failed: {str(error)}"}
    
    def get_claude_system_prompt(self, language: str = "english", scenario: str = "food_explorer") -> str:
        """Get system prompt using claude_integration system"""
        
        # Use the existing system prompt generation
        base_prompt = get_system_prompt(language=language, scenario=scenario)
        
        # Add MCP tools information using claude_integration descriptions
        tools_info = "\n\nAVAILABLE MCP TOOLS:\n"
        for tool in self.mcp_tools:
            tool_desc = get_tool_description(tool['name'])
            if tool_desc:
                tools_info += f"\n{tool['name']}:\n"
                tools_info += f"  - Description: {tool_desc.get('description', 'No description')}\n"
                if 'when_to_use' in tool_desc:
                    tools_info += f"  - When to use: {', '.join(tool_desc['when_to_use'])}\n"
            else:
                tools_info += f"\n{tool['name']}: {tool.get('description', 'No description')}\n"
        
        return base_prompt + tools_info + """

IMPORTANT: You have access to real Sydney MCP tools. When users ask for:
- Food/restaurants: Use search_places tool with appropriate queries
- Location: Use get_current_location tool (ask permission first)
- Transport: Use plan_route and find_nearby_transport tools
- Distances: Use calculate_distance tool

Always explain that you're using real-time data from Sydney when calling tools.
"""
    
    async def process_with_claude_integration(self, user_message: str, conversation_history: List[Dict]) -> str:
        """Process message using claude_integration system"""
        
        # Use conversation patterns to detect intent
        intent = detect_conversation_intent(user_message)
        print(f"🧠 Detected intent: {intent}")
        
        # Get appropriate conversation flow
        flow = get_conversation_flow(intent)
        
        # Determine which tools might be needed
        recommended_tools = select_tools_for_user_request(user_message)
        print(f"🔧 Recommended tools: {recommended_tools}")
        
        # Build messages for Claude
        messages = conversation_history + [
            {"role": "user", "content": user_message}
        ]
        
        try:
            # Get Claude's response
            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                system=self.get_claude_system_prompt(),
                messages=messages
            )
            
            claude_text = response.content[0].text
            
            # Check if we should call MCP tools based on the conversation flow
            if flow and "requires_tools" in flow:
                claude_text = await self.enhance_with_mcp_tools(claude_text, user_message, recommended_tools)
            
            # Add to conversation history using claude_integration
            user_msg_id = str(uuid.uuid4())
            assistant_msg_id = str(uuid.uuid4())
            add_message(self.session.session_id, "user", user_message, user_msg_id)
            add_message(self.session.session_id, "assistant", claude_text, assistant_msg_id)
            
            return claude_text
            
        except Exception as e:
            error_msg = f"Claude API error: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
    
    async def enhance_with_mcp_tools(self, claude_response: str, user_message: str, recommended_tools: List[str]) -> str:
        """Enhance Claude's response with MCP tool data"""
        
        user_lower = user_message.lower()
        enhanced_response = claude_response
        
        # Location requests
        if any(word in user_lower for word in ['location', 'where am i', 'current location']) and 'get_current_location' in recommended_tools:
            print(f"📍 Getting user location...")
            location_result = await self.call_mcp_tool('get_current_location', {'accuracy': 'high'})
            
            if location_result.get('status') == 'success':
                address = location_result['data'].get('address', 'Sydney, Australia')
                enhanced_response += f"\n\n📍 **Your current location:** {address}"
        
        # Food/restaurant requests
        food_keywords = ['food', 'restaurant', 'eat', 'hungry', 'vegan', 'halal', 'sushi', 'laksa', 'chinese', 'turkish']
        if any(word in user_lower for word in food_keywords) and 'search_places' in recommended_tools:
            
            # Extract search terms
            search_terms = []
            if 'vegan' in user_lower: search_terms.append('vegan')
            if 'halal' in user_lower: search_terms.append('halal')
            if 'sushi' in user_lower: search_terms.append('sushi')
            if 'laksa' in user_lower: search_terms.append('laksa')
            if 'chinese' in user_lower: search_terms.append('chinese')
            if 'turkish' in user_lower: search_terms.append('turkish')
            
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
                
                enhanced_response += "Would you like more details about any of these places, or help getting directions?"
        
        return enhanced_response
    
    async def start_conversation(self):
        """Main conversation loop using claude_integration"""
        
        print(f"\n💬 **SYDNEY GUIDE CONVERSATION**")
        print("Powered by claude_integration architecture")
        print("-" * 60)
        
        # Connect to MCP server first
        if not await self.connect_to_mcp_server():
            print("❌ Cannot start without MCP server")
            return
        
        conversation_history = []
        
        # Initial greeting using claude_integration
        welcome = await self.process_with_claude_integration(
            "Hello! I'm a tourist in Sydney. Please introduce yourself and ask for my location permission to provide personalized recommendations.",
            []
        )
        print(f"\n🤖 **Sydney Guide**: {welcome}")
        
        while True:
            try:
                user_input = input(f"\n👤 **You**: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    goodbye = await self.process_with_claude_integration(
                        "The user is saying goodbye. Please give a warm farewell message.",
                        conversation_history
                    )
                    print(f"\n🤖 **Sydney Guide**: {goodbye}")
                    break
                
                if not user_input:
                    continue
                
                # Process with claude_integration system
                print(f"\n🤖 **Sydney Guide**: ", end="", flush=True)
                response = await self.process_with_claude_integration(user_input, conversation_history)
                print(response)
                
                # Update conversation history
                conversation_history.append({"role": "user", "content": user_input})
                conversation_history.append({"role": "assistant", "content": response})
                
                # Keep conversation manageable
                if len(conversation_history) > 10:
                    conversation_history = conversation_history[-8:]
                
            except KeyboardInterrupt:
                print(f"\n\n🤖 **Sydney Guide**: Thanks for using Sydney Guide! Enjoy your time in Sydney! 🇦🇺")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
        
        # Close MCP connection
        if self.mcp_ws:
            await self.mcp_ws.close()

async def main():
    """Main function"""
    
    # Ensure real API mode for best experience
    os.environ["MOCK_MODE"] = "false"
    
    client = SydneyClaudeClient()
    await client.start_conversation()

if __name__ == "__main__":
    asyncio.run(main()) 