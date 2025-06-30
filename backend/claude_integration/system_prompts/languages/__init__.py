# Sydney Guide - Language-Specific Prompts Aggregator
# Dil-spesifik prompt'lari toplayan modul

from .turkish import TURKISH_PROMPT
from .english import ENGLISH_PROMPT
from .chinese import CHINESE_PROMPT
from .japanese import JAPANESE_PROMPT

# Tum dil prompt'larini topla
LANGUAGE_SPECIFIC_PROMPTS = {
    "turkish": TURKISH_PROMPT,
    "english": ENGLISH_PROMPT,
    "chinese": CHINESE_PROMPT,
    "japanese": JAPANESE_PROMPT
}

def get_language_prompt(language: str) -> str:
    """
    Belirtilen dil icin prompt dondur
    
    Args:
        language: Dil kodu
        
    Returns:
        str: Dil-spesifik prompt veya bos string
    """
    return LANGUAGE_SPECIFIC_PROMPTS.get(language, "") 