# Sydney Guide - Tool Descriptions Main Aggregator
# Arac aciklamalarinin ana toplama modulu

from typing import Dict, Any, List, Optional

# Import tool descriptions from moved tools module
from .tools import ALL_TOOL_DESCRIPTIONS

# Import modular components
from .strategies import TOOL_USAGE_STRATEGIES, get_usage_strategy
from .combinations import TOOL_COMBINATIONS, get_recommended_tools_for_scenario
from .error_handling import ERROR_HANDLING_GUIDELINES, get_error_handling_guideline
from .utils import select_tools_for_user_request

# Main tool descriptions (imported from tools module)
MCP_TOOL_DESCRIPTIONS = ALL_TOOL_DESCRIPTIONS

def get_tool_description(tool_name: str) -> Dict[str, Any]:
    """
    Belirtilen arac icin aciklama dondur
    
    Args:
        tool_name: MCP arac adi
        
    Returns:
        Dict: Arac aciklamasi ve kullanim bilgileri
    """
    return MCP_TOOL_DESCRIPTIONS.get(tool_name, {})

# Re-export all functions for backward compatibility
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