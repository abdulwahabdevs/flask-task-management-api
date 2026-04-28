from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User
from app.errors.exceptions import AuthError
from app.services.auth_service import AuthService
from app.utils.response import success_response, error_response
from app.utils.token_blacklist import add_token_to_blacklist
from app.schemas.auth_schema import RegisterSchema, LoginSchema
from flask_jwt_extended import jwt_required, get_jwt



register_schema = RegisterSchema()
login_schema = LoginSchema()

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = register_schema.load(request.json)
        
        AuthService.register(data)
        
        return jsonify(
            success_response(message="User registered successfully")
            ), 201
    except AuthError as e:
        return jsonify(error_response(message=e.message)), e.status_code
    
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = login_schema.load(request.json)

        result = AuthService.login(data)

        return jsonify(success_response(result)), 200
    except AuthError as e:
        return jsonify(error_response(message=e.message)), e.status_code


from flask_jwt_extended import jwt_required, get_jwt_identity


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        token = get_jwt()

        user_id = get_jwt_identity()

        AuthService.refresh(token, user_id)

        return jsonify(
            success_response(message="Successfully refreshed")
            ), 200
    except AuthError as e:
        return jsonify(
            error_response(message=e.message)
        ), e.status_code


from flask_jwt_extended import jwt_required, get_jwt_identity

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return jsonify(error_response(message="User not found")), 404
    
    return jsonify({
        "id": user.id,
        "email": user.email,
        "username": user.username
    }), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    try:
        token = get_jwt()
        AuthService.logout(token)
        
        return jsonify(success_response(
                message="Logged out successfully"
            )), 200
    except AuthError as e:
        return jsonify(
            error_response(message=e.message)
        ), e.status_code