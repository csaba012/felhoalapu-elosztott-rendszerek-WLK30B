from flask import jsonify

class AppError(Exception):
    """Base application error"""
    status_code = 500
    
    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message
        return rv

class ValidationError(AppError):
    """Validation error"""
    status_code = 400

class AuthenticationError(AppError):
    """Authentication error"""
    status_code = 401

class AuthorizationError(AppError):
    """Authorization error"""
    status_code = 403

class NotFoundError(AppError):
    """Not found error"""
    status_code = 404

class ConflictError(AppError):
    """Conflict error"""
    status_code = 409

def register_error_handlers(app):
    """Register error handlers for the application"""
    
    @app.errorhandler(AppError)
    def handle_app_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Az erőforrás nem található'}), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'error': 'A HTTP metódus nem engedélyezett'}), 405
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({'error': 'A fájl túl nagy'}), 413
    
    @app.errorhandler(415)
    def unsupported_media_type(error):
        return jsonify({'error': 'Nem támogatott média típus'}), 415
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'error': 'Belső szerver hiba'}), 500
