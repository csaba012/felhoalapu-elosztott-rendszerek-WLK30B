from flask import Flask, request, jsonify, send_from_directory
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import modules
from models import db, User, Photo
from config import config
from validators import validate_email, validate_password, validate_photo_name, sanitize_input
from security import (
    allowed_file, sanitize_filename, validate_file_size, 
    verify_image_file, prevent_directory_traversal, add_security_headers
)
from errors import (
    register_error_handlers, ValidationError, AuthenticationError, 
    NotFoundError, ConflictError
)
from logging_config import setup_logging

# Create Flask app
app = Flask(__name__)

# Load configuration
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Configure CORS
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173", "https://frontend.gentleglacier-43da7a67.eastus.azurecontainerapps.io"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Register error handlers
register_error_handlers(app)

# Setup logging
setup_logging(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Apply security headers to all responses
@app.after_request
def after_request(response):
    return add_security_headers(response)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

# ============================================================================
# Authentication Routes
# ============================================================================

@app.route('/auth/register', methods=['POST'])
@limiter.limit("5 per hour")
def register():
    data = request.get_json()
    
    if not data:
        raise ValidationError('Hiányzó adatok')
    
    email = sanitize_input(data.get('email', '').strip().lower(), 120)
    password = data.get('password', '')
    
    # Validate email
    if not email:
        raise ValidationError('Az email cím megadása kötelező')
    
    if not validate_email(email):
        raise ValidationError('Érvénytelen email cím')
    
    # Validate password
    is_valid_password, password_error = validate_password(password)
    if not is_valid_password:
        raise ValidationError(password_error)
    
    # Check if user exists
    if User.query.filter_by(email=email).first():
        raise ConflictError('Ez az email cím már regisztrálva van')
    
    # Create new user
    user = User(email=email)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    app.logger.info(f'New user registered: {email}')
    
    return jsonify({
        'message': 'Sikeres regisztráció',
        'user': user.to_dict()
    }), 201

@app.route('/auth/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    data = request.get_json()
    
    if not data:
        raise ValidationError('Hiányzó adatok')
    
    email = sanitize_input(data.get('email', '').strip().lower(), 120)
    password = data.get('password', '')
    
    if not email or not password:
        raise ValidationError('Email cím és jelszó megadása kötelező')
    
    # Find user
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        raise AuthenticationError('Hibás email cím vagy jelszó')
    
    if not user.is_active:
        raise AuthenticationError('A fiók inaktív')
    
    # Create access token - ensure user.id is an integer
    access_token = create_access_token(identity=str(user.id))
    
    app.logger.info(f'User logged in: {email}')
    
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@app.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        raise NotFoundError('Felhasználó nem található')
    
    return jsonify(user.to_dict()), 200

# ============================================================================
# Photo Routes
# ============================================================================

@app.route('/photos', methods=['GET'])
@jwt_required()
def get_photos():
    user_id = get_jwt_identity()
    photos = Photo.query.filter_by(user_id=user_id).order_by(Photo.upload_date.desc()).all()
    
    return jsonify([photo.to_dict() for photo in photos]), 200

@app.route('/photos', methods=['POST'])
@jwt_required()
@limiter.limit("20 per hour")
def upload_photo():
    try:
        # Get user identity and convert to int
        user_identity = get_jwt_identity()
        user_id = int(user_identity)
        
        app.logger.info(f'Upload request from user: {user_id}')
        
        # Check if file is in request
        if 'file' not in request.files:
            raise ValidationError('Nincs fájl kiválasztva')
        
        file = request.files['file']
        name = sanitize_input(request.form.get('name', '').strip(), 40)
        
        # Validate file
        if file.filename == '':
            raise ValidationError('Nincs fájl kiválasztva')
        
        if not allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
            raise ValidationError('Nem támogatott fájl formátum')
        
        # Validate file size
        is_valid_size, size_error = validate_file_size(file, app.config['MAX_CONTENT_LENGTH'])
        if not is_valid_size:
            raise ValidationError(size_error)
        
        # Validate photo name
        is_valid_name, name_error = validate_photo_name(name)
        if not is_valid_name:
            raise ValidationError(name_error)
        
        # Sanitize and save file
        filename = sanitize_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        file.save(filepath)
        
        # Verify it's a valid image
        is_valid_image, image_error = verify_image_file(filepath)
        if not is_valid_image:
            os.remove(filepath)
            raise ValidationError(image_error)
        
        # Get file size
        file_size = os.path.getsize(filepath)
        
        # Create photo record
        photo = Photo(
            name=name,
            filename=filename,
            original_filename=file.filename,
            file_size=file_size,
            mime_type=file.content_type,
            user_id=user_id
        )
        
        db.session.add(photo)
        db.session.commit()
        
        app.logger.info(f'Photo uploaded by user {user_id}: {name}')
        
        return jsonify({
            'message': 'Fénykép sikeresen feltöltve',
            'photo': photo.to_dict()
        }), 201
        
    except ValueError as e:
        app.logger.error(f'Invalid user identity: {e}')
        raise AuthenticationError('Érvénytelen felhasználói azonosító')
    except ValidationError:
        raise
    except Exception as e:
        app.logger.error(f'Upload error: {str(e)}')
        db.session.rollback()
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        raise ValidationError('Hiba történt a feltöltés során')

@app.route('/photos/<int:photo_id>', methods=['GET'])
@jwt_required()
def get_photo(photo_id):
    """Get a specific photo"""
    user_id = get_jwt_identity()
    photo = Photo.query.filter_by(id=photo_id, user_id=user_id).first()
    
    if not photo:
        raise NotFoundError('Fénykép nem található')
    
    return jsonify(photo.to_dict()), 200

@app.route('/photos/<int:photo_id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("30 per hour")
def delete_photo(photo_id):
    """Delete a photo"""
    user_id = get_jwt_identity()
    photo = Photo.query.filter_by(id=photo_id, user_id=user_id).first()
    
    if not photo:
        raise NotFoundError('Fénykép nem található')
    
    # Delete file from filesystem
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    
    # Delete from database
    db.session.delete(photo)
    db.session.commit()
    
    app.logger.info(f'Photo deleted by user {user_id}: {photo.name}')
    
    return jsonify({'message': 'Fénykép sikeresen törölve'}), 200

# ============================================================================
# Static File Serving
# ============================================================================

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Security: prevent directory traversal
    if not prevent_directory_traversal(filename):
        raise ValidationError('Érvénytelen fájlnév')
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        raise NotFoundError('Fájl nem található')
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ============================================================================
# Database Initialization
# ============================================================================

with app.app_context():
    db.create_all()
    app.logger.info('Database tables created')
