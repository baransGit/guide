# Sydney Guide - Error Handling Guidelines Aggregator
# Hata yonetim kilavuzlarini toplayan modul

from .location_errors import LOCATION_PERMISSION_DENIED
from .api_errors import API_SERVICE_UNAVAILABLE
from .search_errors import NO_RESULTS_FOUND
from .transport_errors import TRANSPORT_DELAYS

# Tum hata yonetim kilavuzlari
ERROR_HANDLING_GUIDELINES = {
    "location_permission_denied": LOCATION_PERMISSION_DENIED,
    "api_service_unavailable": API_SERVICE_UNAVAILABLE,
    "no_results_found": NO_RESULTS_FOUND,
    "transport_delays": TRANSPORT_DELAYS
}

def get_error_handling_guideline(error_type: str) -> dict:
    """
    Belirtilen hata tipi icin yonetim kilavuzunu dondur
    
    Args:
        error_type: Hata tipi
        
    Returns:
        dict: Hata yonetim kilavuzu
    """
    return ERROR_HANDLING_GUIDELINES.get(error_type, {}) 