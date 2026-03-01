import re
from typing import Tuple

def validate_email(email: str) -> bool:
    if not email or len(email) > 120:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> Tuple[bool, str]:
    if not password:
        return False, "A jelszó megadása kötelező"
    
    if len(password) < 8:
        return False, "A jelszónak legalább 8 karakter hosszúnak kell lennie"
    
    if len(password) > 128:
        return False, "A jelszó túl hosszú"
    return True, ""

def validate_photo_name(name: str) -> Tuple[bool, str]:
    if not name or len(name) == 0:
        return False, "A fénykép neve nem lehet üres"
    
    if len(name) > 40:
        return False, "A fénykép neve maximum 40 karakter lehet"
    
    # Allow alphanumeric, spaces, hyphens, dots, and Hungarian characters
    if not re.match(r'^[\w\s\-\.áéíóöőúüűÁÉÍÓÖŐÚÜŰ]+$', name):
        return False, "A fénykép neve érvénytelen karaktereket tartalmaz"
    
    return True, ""

def sanitize_input(text: str, max_length: int = None) -> str:
    if not text:
        return ""
    
    # Remove null bytes
    text = text.replace('\0', '')
    
    # Trim whitespace
    text = text.strip()
    
    # Limit length if specified
    if max_length:
        text = text[:max_length]
    
    return text
