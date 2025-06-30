# Sydney Guide - System Prompts Utilities
# Sistem prompt'lari icin yardimci fonksiyonlar

from typing import Optional
from .core_identity import SYDNEY_GUIDE_SYSTEM_PROMPT
from .languages import get_language_prompt
from .scenarios import get_scenario_prompt
from .emergency import get_emergency_prompt

def get_system_prompt(language: str = "english", scenario: Optional[str] = None, emergency: Optional[str] = None) -> str:
    """
    Kullanicinin durumuna gore uygun sistem prompt'unu dondur
    
    Args:
        language: Kullanicinin dili
        scenario: Ozel senaryo (opsiyonel)
        emergency: Acil durum tipi (opsiyonel)
        
    Returns:
        str: Tam sistem prompt'u
    """
    # Ana prompt ile basla
    full_prompt = SYDNEY_GUIDE_SYSTEM_PROMPT
    
    # Dil-spesifik prompt ekle
    language_prompt = get_language_prompt(language)
    if language_prompt:
        full_prompt += "\n\n" + language_prompt
    
    # Senaryo-spesifik prompt ekle
    if scenario:
        scenario_prompt = get_scenario_prompt(scenario)
        if scenario_prompt:
            full_prompt += "\n\n" + scenario_prompt
    
    # Acil durum prompt'u ekle (en yuksek oncelik)
    if emergency:
        emergency_prompt = get_emergency_prompt(emergency)
        if emergency_prompt:
            full_prompt = emergency_prompt + "\n\n" + full_prompt
    
    return full_prompt

def get_localized_prompt(language: str, scenario: Optional[str] = None) -> str:
    """
    Herhangi bir dil icin yerellestirilmis prompt dondur
    
    Args:
        language: Kullanicinin dili (turkish, english, chinese, japanese, etc.)
        scenario: Ozel senaryo (opsiyonel)
        
    Returns:
        str: Yerellestirilmis prompt
    """
    return get_system_prompt(language=language, scenario=scenario)

def get_food_explorer_prompt(language: str = "english") -> str:
    """
    Yemek kesfi icin ozellestirilmis prompt dondur
    
    Args:
        language: Kullanicinin dili
        
    Returns:
        str: Yemek kesfi prompt'u
    """
    return get_system_prompt(language=language, scenario="food_explorer")

def get_first_time_visitor_prompt(language: str = "english") -> str:
    """
    Ilk kez gelen ziyaretci icin ozellestirilmis prompt dondur
    
    Args:
        language: Kullanicinin dili
        
    Returns:
        str: Ilk ziyaret prompt'u
    """
    return get_system_prompt(language=language, scenario="first_time_visitor")

def get_emergency_prompt_for_situation(emergency_type: str, language: str = "english") -> str:
    """
    Acil durum icin ozellestirilmis prompt dondur
    
    Args:
        emergency_type: Acil durum tipi
        language: Kullanicinin dili
        
    Returns:
        str: Acil durum prompt'u
    """
    return get_system_prompt(language=language, emergency=emergency_type) 