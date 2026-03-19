from flask import jsonify
from marshmallow import ValidationError
from app.utils.response import error_response
from werkzeug.exceptions import NotFound

def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify(error_response(
            message="Validation error",
            errors=e.messages
        )), 400
    
    @app.errorhandler(NotFound)
    def handle_not_found(err):
        return jsonify(error_response(
            message="Resource not found"
    )), 404
    
    @app.errorhandler(500)
    def handle_internal_error(err):
        return jsonify(error_response(
            message="Internal server error"
    )), 500