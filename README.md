# Sydney Guide - Personal Project

AI-powered tourism assistant for Sydney with Claude + MCP integration.

## Current Status

- ⚠️ **Migrating to Official MCP Python SDK**
- 🔧 Cleaning up scattered test files
- 🎯 Next: Update MCP decorators in tool files

## Quick Start

```bash
cd backend
python main.py
# Server: http://localhost:8888
```

## Structure

```
backend/mcp_tools/           # MCP tool implementations
backend/claude_integration/  # Claude prompts & patterns
backend/main.py             # MCP server
tests/                      # All tests go here
```

## Environment

```bash
MOCK_MODE=true              # Development mode
GOOGLE_MAPS_API_KEY=        # For real API
ANTHROPIC_API_KEY=          # For Claude
```

---

_Personal development repository_
