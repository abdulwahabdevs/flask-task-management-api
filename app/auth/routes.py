from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User
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
    data = register_schema.load(request.json)
    response, status = AuthService.register(data)
    return jsonify(response), status

    
@auth_bp.route("/login", methods=["POST"])
def login():
    data = login_schema.load(request.json)
    response, status = AuthService.login(data)
    return jsonify(response), status


from flask_jwt_extended import jwt_required, get_jwt_identity


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    token = get_jwt()
    user_id = get_jwt_identity()

    return AuthService.refresh(token, user_id)


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
    token = get_jwt()

    return AuthService.logout(token)