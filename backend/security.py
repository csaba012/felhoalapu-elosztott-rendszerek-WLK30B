from functools import wraps
from flask import request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import hashlib
from typing import Optional, Tuple

def rate_limit_key():
    return request.remote_addr

def allowed_file(filename: str, allowed_extensions: set) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def sanitize_filename(filename: str) -> str:
    # Get secure filename
    secure_name = secure_filename(filename)
    
    # Split name and extension
    name, ext = os.path.splitext(secure_name)
    
    # Create unique timestamp
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')
    
    # Create hash for extra uniqueness
    hash_suffix = hashlib.md5(f"{name}{timestamp}".encode()).hexdigest()[:8]
    
    return f"{name}_{timestamp}_{hash_suffix}{ext}"

def validate_file_size(file, max_size: int) -> Tuple[bool, Optional[str]]:
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > max_size:
        max_mb = max_size / 1024 / 1024
        return False, f"A fájl mérete meghaladja a megengedett {max_mb:.1f}MB limitet"
    
    if file_size == 0:
        return False, "A fájl üres"
    
    return True, None

def verify_image_file(filepath: str) -> Tuple[bool, Optional[str]]:
    try:
        from PIL import Image
        
        with Image.open(filepath) as img:
            img.verify()
        
        # Reopen to check for decompression bombs
        with Image.open(filepath) as img:
            # PIL will raise an exception if the image is a decompression bomb
            img.load()
        
        return True, None
        
    except Exception as e:
        return False, "Érvénytelen vagy sérült képfájl"

def prevent_directory_traversal(filename: str) -> bool:
    return '..' not in filename and not filename.startswith('/')

def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    return response

def require_content_type(*content_types):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.content_type not in content_types:
                return jsonify({'error': 'Nem támogatott tartalomtípus'}), 415
            return f(*args, **kwargs)
        return decorated_function
    return decorator
