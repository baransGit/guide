# Sydney Guide - MCP Tool Descriptions for Claude
# Claude'un MCP araçlarını nasıl kullanacağını tanımlayan açıklamalar
# FULLY MODULARIZED: Now imports from tool_descriptions/ subdirectory

from typing import Dict, Any, List, Optional

# Import everything from the modular tool_descriptions package
from .tool_descriptions import (
    MCP_TOOL_DESCRIPTIONS,
    TOOL_USAGE_STRATEGIES,
    TOOL_COMBINATIONS, 
    ERROR_HANDLING_GUIDELINES,
    get_tool_description,
    get_recommended_tools_for_scenario,
    get_usage_strategy,
    get_error_handling_guideline,
    select_tools_for_user_request
)

# Re-export everything for backward compatibility
__all__ = [
    'MCP_TOOL_DESCRIPTIONS',
    'TOOL_USAGE_STRATEGIES',
    'TOOL_COMBINATIONS',
    'ERROR_HANDLING_GUIDELINES',
    'get_tool_description',
    'get_recommended_tools_for_scenario', 
    'get_usage_strategy',
    'get_error_handling_guideline',
    'select_tools_for_user_request'
]
