# Project Description

Sydney Guide is a mobile application designed for tourists visiting Sydney, featuring an AI-powered chatbot (Claude with MCP integration) that provides personalized travel assistance. The app helps users find nearby restaurants, suggests optimal public transport routes, and provides real-time travel guidance with proactive notifications. The architecture leverages MCP (Model Context Protocol) to simplify development and reduce costs by allowing Claude to directly interact with external APIs through custom tools.

**Key Innovation: MCP Integration**

- Claude directly accesses Google Maps, NSW Transport, and other APIs through MCP tools
- Eliminates complex backend business logic
- Reduces API costs through intelligent orchestration
- Enables natural language interaction with multiple services

# Cursor Project Rules

## General Architecture Philosophy

- **MCP-First Approach**: Claude handles complex orchestration through MCP tools
- **Simplified Backend**: Focus on MCP tool development rather than business logic
- **AI-Native Design**: Let Claude make intelligent decisions about API usage
- **CRITICAL: Comments in code must be in Turkish, but ALL CODE CONTENT must be in English (variables, functions, class names, strings, dictionary keys, etc.)**
- Every feature should be developed as MCP tools first, then integrated into the app

## Code Language Standards

- **Variable Names**: English only (user_location, restaurant_data, transport_route)
- **Function Names**: English only (get_location, find_restaurants, send_notification)
- **Class Names**: English only (LocationService, RestaurantFinder, NotificationManager)
- **File Names**: English only (location_tool.py, maps_service.js, chat_screen.tsx)
- **String Values**: English only ("success", "error", "restaurant", "location")
- **Dictionary Keys**: English only ({"status": "success", "data": result})
- **API Responses**: English only ({"message": "Location found", "status": "ok"})
- **Comments**: Turkish only (# Kullanicinin konumunu al, // Restoran listesini filtrele)
- **Docstrings**: Turkish only ("""Bu fonksiyon kullanicinin mevcut konumunu alir""")
- **Error Messages**: English for all system messages, Turkish only in user-facing UI text

## Frontend (React Native)

- **Simplified Structure**: Focus on chat interface and basic navigation
- Components organized in folders: `components/`, `screens/`, `services/`, `hooks/`
- **Chat-Centric Design**: Main interface is conversational with Claude
- Use Context API for lightweight state management (Redux not needed with MCP)
- **MCP Integration Layer**: Dedicated service for Claude MCP communication
- Real-time location sharing with Claude through MCP tools
- Push notification handling for Claude-initiated alerts

## Backend (Python) - MCP Tools Focus

- **Primary Purpose**: Develop and serve MCP tools for Claude
- Use FastAPI for MCP tool endpoints and WebSocket connections
- **MCP Tools Structure**:
  ```
  mcp_tools/
  ├── location_tools.py      # GPS, geofencing, location tracking
  ├── maps_tools.py          # Google Maps integration
  ├── transport_tools.py     # NSW Transport API
  ├── notification_tools.py  # Push notifications
  ├── preference_tools.py    # User preferences
  └── analytics_tools.py     # Usage tracking
  ```
- **Minimal Business Logic**: Let Claude orchestrate through MCP tools
- Environment variables for all API keys and sensitive data
- Type hints and docstrings for all MCP tool functions

## MCP Tools Development - Cost-Conscious Approach

- **Mock-First Development**: Develop and test all tools with comprehensive mock data
- **Environment-Based API Selection**: Switch between mock and real APIs via environment variables
- **Stateless Tools**: Tools should be independent and composable
- **Dual Implementation**: Each tool has both mock and real API implementations
- **Error Handling**: Robust error handling for both mock and real API scenarios
- **Documentation**: Clear descriptions for Claude including mock/real API modes
- **Testing Strategy**: Extensive testing with mocks, minimal validation with real APIs
- **Cost Controls**: Built-in spending limits and usage monitoring

## Mock vs Real API Development Strategy

### Development Philosophy

- **Primary Development**: Use comprehensive mock data that mirrors real API responses
- **Cost Control**: Real APIs only used for final validation and production
- **Quality Assurance**: Mock data should be realistic and comprehensive
- **Testing Strategy**: 95% testing with mocks, 5% validation with real APIs

### MCP Tool Implementation Pattern

```python
import os
from typing import Dict, Any

# Cevre degiskeninden API modunu al
USE_REAL_API = os.getenv('MOCK_MODE', 'true').lower() == 'false'

@mcp_tool(name="search_places")
async def search_places(query: str, location: str) -> Dict[str, Any]:
    """
    Verilen konumda yer arama (mock veya gercek API)

    Args:
        query: Arama sorgusu (ornek: "vegan restaurant")
        location: Konum bilgisi (ornek: "Sydney Opera House")

    Returns:
        dict: Yer arama sonuclari
    """
    if USE_REAL_API:
        # Gercek Google Places API cagrisi
        return await search_places_real_api(query, location)
    else:
        # Mock veri dondur
        return await search_places_mock_data(query, location)
```

### Mock Data Quality Standards

- **Realistic Data**: Mock data should match real API response structure exactly
- **Comprehensive Coverage**: Include edge cases and error scenarios in mock data
- **Sydney-Specific**: All mock data should be relevant to Sydney tourism
- **Regular Updates**: Mock data should be updated based on real API responses
- **Error Simulation**: Mock functions should simulate API errors and rate limits

### Real API Usage Guidelines

- **Before Real API Testing**: Ensure all functionality works with mock data
- **Batch Testing**: Plan real API tests to minimize individual calls
- **Response Caching**: Cache real API responses for reuse in testing
- **Cost Monitoring**: Track API usage costs during real API testing sessions

## Environment Configuration for Cost Control

### Required Environment Variables

```bash
# API Mode Control
MOCK_MODE=true  # Set to 'false' for real API testing

# API Keys (only needed when MOCK_MODE=false)
GOOGLE_MAPS_API_KEY=your_google_api_key
NSW_TRANSPORT_API_KEY=your_nsw_transport_key
ANTHROPIC_API_KEY=your_claude_api_key

# Cost Control
MAX_DAILY_API_CALLS=100  # Maximum API calls per day
COST_ALERT_THRESHOLD=10  # Alert when daily cost exceeds $10 USD
```

### Usage Patterns

- **Daily Development**: MOCK_MODE=true (no API costs)
- **Integration Testing**: MOCK_MODE=false (minimal API usage)
- **Production Deployment**: MOCK_MODE=false (real API usage)

## Claude Integration & Prompting

- **System Prompts**: Separate files for different conversation contexts
- **Multi-language Support**: Language-specific prompts and responses
- **Context Management**: Efficient conversation history handling
- **Tool Selection**: Guide Claude on when to use which tools
- **Personalization**: Learn user preferences through conversation

## Data Management - Simplified

- **SQLite for Local**: User preferences, chat history, cached data
- **Redis for Session**: Real-time conversation state
- **PostgreSQL Optional**: Only if advanced analytics needed
- **MCP Tool Data**: Each tool manages its own data requirements
- **Privacy First**: Minimal data collection, user consent for all tracking

## Location & Navigation - MCP Powered

- Location tools provide Claude with real-time position data
- Claude decides when to track, when to notify, when to guide
- **Intelligent Geofencing**: Claude sets up location-based triggers
- **Proactive Notifications**: Claude initiates notifications through MCP tools
- **Permission Management**: Handle through conversational flow

## API Management - Cost-Conscious Development

- **Mock-First Development**: Use mock data for development and most testing
- **Real API Testing Mode**: Environment variable to switch to real APIs when needed
- **Intelligent Caching**: Cache real API responses to minimize repeated calls
- **Cost Optimization**: Batch API calls and implement smart fallbacks
- **Rate Limiting**: Per-tool and per-user limits with cost tracking
- **Budget Monitoring**: Real-time cost tracking with spending alerts
- **API Usage Modes**:
  - `MOCK_MODE=true` (default): Use mock data for all operations
  - `MOCK_MODE=false`: Use real APIs (for final testing and production)

## Performance & Optimization

- **MCP Tool Performance**: Optimize individual tool response times
- **Lazy Loading**: Load MCP tools on demand
- **Background Processing**: Long-running tasks through async MCP tools
- **Memory Management**: Efficient conversation context handling
- **Network Optimization**: Batch API calls when possible through MCP

## Security & Privacy - MCP Focused

- **Tool Security**: Validate all inputs to MCP tools
- **API Key Management**: Secure handling within MCP tool layer
- **User Consent**: Conversational consent flow through Claude
- **Data Encryption**: Encrypt sensitive data in MCP tool responses
- **Audit Logging**: Track MCP tool usage for security monitoring

## Development Workflow - MCP Centric

1. **Design Conversation Flow**: How should Claude interact with user?
2. **Identify Required Tools**: What MCP tools does Claude need?
3. **Develop MCP Tools**: Create and test individual tools
4. **Configure Claude**: Set up prompts and tool descriptions
5. **Integrate Frontend**: Connect React Native to MCP-enabled Claude
6. **Test Conversations**: End-to-end conversation testing

## Testing Strategy - Cost-Optimized

### Mock Data Testing (Primary)

- **MCP Tool Testing**: Unit tests using mock data (99% of tests)
- **Conversation Testing**: Test Claude interactions with mock tools
- **Integration Testing**: Full conversation flows with mock data
- **Performance Testing**: Tool response times with mock data
- **Edge Case Testing**: Error scenarios and unusual inputs with mocks

### Real API Validation (Minimal)

- **API Integration Testing**: Validate real API connections work correctly
- **Data Accuracy Testing**: Compare mock vs real API response structures
- **Performance Benchmarking**: Real API response times and reliability
- **Cost Monitoring**: Track actual API usage and costs during testing

### Testing Workflow

1. **Develop with Mocks**: Build and test all functionality with mock data
2. **Mock Testing Complete**: Ensure 100% test coverage with mocks
3. **Real API Validation**: Run limited tests with real APIs to validate integration
4. **Production Deployment**: Deploy with confidence after mock testing

## Deployment & Infrastructure

- **Simplified Deployment**: Focus on MCP tool availability
- **Docker Optional**: Only if needed for production deployment
- **Environment Management**: Separate configs for MCP tools
- **Monitoring**: Track MCP tool usage and performance
- **Scaling**: Scale MCP tool endpoints independently

## Documentation Requirements

- **MCP Tool Documentation**: Clear descriptions for Claude
- **Conversation Examples**: Sample interactions for each feature
- **API Documentation**: Standard REST API docs for non-MCP endpoints
- **User Guide**: How to interact with the AI assistant

## Quality Assurance

- **Conversation Quality**: Ensure Claude provides accurate information
- **Tool Reliability**: MCP tools must be highly reliable
- **Response Time**: Optimize for quick conversational responses
- **Error Recovery**: Graceful handling of tool failures
- **User Satisfaction**: Focus on helpful, accurate assistance

---

This MCP-centric approach significantly simplifies development while enabling more sophisticated AI-powered features. The focus shifts from complex backend logic to creating powerful tools that Claude can orchestrate intelligently.

## MCP Implementation Guidelines

### MCP Server Setup

- Use `mcp` Python package for server implementation
- Each tool should be a separate function with proper MCP decorators
- Tools must return structured JSON responses
- Implement proper error handling and logging for each tool
- Use WebSocket connection for real-time communication with Claude

### MCP Tool Standards

```python
# MCP tool ornegi - dil standartlarina uygun
@mcp_tool(
    name="get_location",  # İngilizce tool adi
    description="Kullanicinin mevcut konumunu al",  # Turkce aciklama
    parameters={
        "accuracy": {"type": "string", "enum": ["high", "medium", "low"]}  # İngilizce parametre
    }
)
async def get_current_location(accuracy: str = "high") -> dict:
    """
    Kullanicinin GPS konumunu ve adres bilgisini dondur

    Args:
        accuracy: Konum dogruluk seviyesi (high/medium/low)

    Returns:
        dict: Konum bilgileri (lat, lng, address, accuracy)
    """
    try:
        # GPS koordinatlarini al
        coordinates = await get_gps_coordinates(accuracy)

        # Koordinatlari adrese cevir
        address = await reverse_geocode(coordinates['lat'], coordinates['lng'])

        # Sonucu dondur
        return {
            "status": "success",
            "data": {
                "lat": coordinates['lat'],
                "lng": coordinates['lng'],
                "address": address,
                "accuracy": accuracy
            }
        }
    except Exception as error:
        # Hata durumunda log kaydet
        logger.error(f"Location tool error: {str(error)}")
        return {
            "status": "error",
            "message": "Konum bilgisi alinamadi"  # Kullanici icin Turkce hata
        }
```

### Claude Integration Patterns

- **System Prompts**: Store in `prompts/` directory with language variants
- **Tool Descriptions**: Must be clear and actionable for Claude
- **Context Management**: Maintain conversation state through MCP session
- **Fallback Handling**: Provide alternative approaches when tools fail

## Development Workflow - Step by Step

### Phase 1: MCP Foundation (Week 1)

1. **Day 1-2**: Set up MCP server and basic tool structure
2. **Day 3-4**: Implement core tools (location, maps, transport)
3. **Day 5-6**: Test tools individually with MCP client
4. **Day 7**: Integration testing with Claude

### Phase 2: Frontend Integration (Week 2)

1. **Day 1-2**: React Native chat interface
2. **Day 3-4**: MCP WebSocket connection
3. **Day 5-6**: Real-time messaging with Claude
4. **Day 7**: End-to-end testing

### Phase 3: Enhancement (Week 3)

1. **Day 1-2**: Push notifications through MCP
2. **Day 3-4**: Offline capabilities and caching
3. **Day 5-6**: User preferences and personalization
4. **Day 7**: Performance optimization

## Prompt Engineering Guidelines

### System Prompt Structure

```
You are Sydney Guide, an AI assistant for tourists in Sydney.

CAPABILITIES:
- Real-time location tracking via get_location tool
- Restaurant search via search_places tool
- Public transport routing via get_transport tool
- Proactive notifications via send_notification tool

PERSONALITY:
- Friendly and helpful
- Proactive (offer suggestions without being asked)
- Multi-lingual (detect user language automatically)

CONVERSATION FLOW:
1. Greet user and ask for location permission
2. Understand their needs (food, transport, etc.)
3. Use appropriate tools to gather information
4. Provide clear, actionable recommendations
5. Offer to track their journey if they accept
```

### Tool Usage Patterns

- **Always ask permission** before using location tools
- **Batch API calls** when possible to reduce costs
- **Cache results** for similar requests within conversation
- **Provide fallbacks** when primary tools fail

### Code Generation Instructions for Claude

When generating code, ALWAYS follow these language rules:

- **All variables, functions, classes**: English names only
- **All string values, dictionary keys, API responses**: English only
- **All comments and docstrings**: Turkish only (without Turkish characters)
- **Example**:
  ```python
  user_location = get_current_position()  # Kullanicinin mevcut konumunu al
  result = {"status": "success", "message": "Location found"}  # Basarili sonuc
  ```
- **NOT**:
  ```python
  kullanici_konumu = get_current_position()  # Get user location
  result = {"durum": "basarili", "mesaj": "Konum bulundu"}  # Successful result
  ```

## Error Handling & Resilience

### MCP Tool Error Handling

```python
try:
    result = await external_api_call()
    return {"status": "success", "data": result}
except APIRateLimitError:
    return {"status": "rate_limited", "message": "API limit reached, trying alternative"}
except APIError as e:
    return {"status": "error", "message": f"API error: {str(e)}"}
```

### Frontend Error Handling

- **Connection Loss**: Show offline indicator, queue messages
- **Tool Failures**: Claude should explain what went wrong
- **Permission Denied**: Guide user through permission flow
- **API Limits**: Inform user and suggest alternatives

## Performance Optimization

### MCP Tool Performance

- **Async/Await**: All tools must be async for non-blocking execution
- **Connection Pooling**: Reuse HTTP connections for external APIs
- **Response Caching**: Cache API responses with appropriate TTL
- **Lazy Loading**: Load tools only when needed

### Claude Response Optimization

- **Streaming Responses**: Use streaming for long responses
- **Progressive Enhancement**: Show partial results while processing
- **Context Compression**: Summarize old conversation history
- **Tool Selection**: Guide Claude to use most efficient tools

## Testing & Quality Assurance

### MCP Tool Testing

```python
# Test each tool independently
async def test_location_tool():
    result = await get_current_location("high")
    assert result["status"] == "success"
    assert "lat" in result["data"]
    assert "lng" in result["data"]
```

### Conversation Testing

- **Happy Path**: Test successful conversation flows
- **Error Scenarios**: Test tool failures and recovery
- **Edge Cases**: Test unusual user inputs
- **Performance**: Test response times under load

### User Acceptance Testing

- **Real Tourists**: Test with actual visitors to Sydney
- **Multiple Languages**: Test non-English conversations
- **Different Devices**: Test on various phone models
- **Network Conditions**: Test on slow/intermittent connections

## Deployment & Monitoring

### MCP Server Deployment

- **Health Checks**: Endpoint to verify all tools are working
- **Logging**: Comprehensive logging of tool usage and errors
- **Metrics**: Track tool performance and usage patterns
- **Alerts**: Notify when tools fail or performance degrades

### Production Monitoring

- **Conversation Quality**: Monitor Claude response accuracy
- **Tool Reliability**: Track tool success/failure rates
- **User Satisfaction**: Collect feedback on assistant helpfulness
- **Cost Tracking**: Monitor API usage and costs

---

This comprehensive guide ensures successful MCP-based development with clear steps, patterns, and quality standards.
