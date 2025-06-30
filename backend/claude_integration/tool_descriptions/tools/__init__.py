# Sydney Guide - Tools Module
# Claude tool descriptions aggregator

from .location_tools import LOCATION_TOOL_DESCRIPTIONS
from .places_tools import PLACES_TOOL_DESCRIPTIONS
from .transport_tools import TRANSPORT_TOOL_DESCRIPTIONS
from .notification_tools import NOTIFICATION_TOOL_DESCRIPTIONS

# Tüm tool descriptions'ları birleştir
ALL_TOOL_DESCRIPTIONS = {
    **LOCATION_TOOL_DESCRIPTIONS,
    **PLACES_TOOL_DESCRIPTIONS,
    **TRANSPORT_TOOL_DESCRIPTIONS,
    **NOTIFICATION_TOOL_DESCRIPTIONS,
}

__all__ = [
    'ALL_TOOL_DESCRIPTIONS',
    'LOCATION_TOOL_DESCRIPTIONS', 
    'PLACES_TOOL_DESCRIPTIONS',
    'TRANSPORT_TOOL_DESCRIPTIONS',
    'NOTIFICATION_TOOL_DESCRIPTIONS',
] 