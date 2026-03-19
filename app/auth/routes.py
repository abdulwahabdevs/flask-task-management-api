from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User
from app.utils.response import success_response, error_response
from app.schemas.auth_schema import RegisterSchema, LoginSchema
from werkzeug.security import generate_password_hash


register_schema = RegisterSchema()
login_schema = LoginSchema()

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = register_schema.load(request.json)

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify(error_response(message="Missing required details")), 400
    
    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        return jsonify(error_response(message="User already exists")), 400
    
    hashed_password = generate_password_hash(password)

    user = User(
        username=username,
        email=email,
        password_hash=hashed_password
    )
    db.session.add(user)
    db.session.commit()

    return jsonify(success_response(message="User registered successfully")), 201

from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

@auth_bp.route("/login", methods=["POST"])
def login():
    data = login_schema.load(request.json)

    if not data:
        return jsonify(error_response(message="Invalid JSON")), 400
    
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify(error_response(message="Missing email or password")), 400
    
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify(error_response(message="Invalid credentials")), 401
    
    if not check_password_hash(user.password_hash, password):
        return jsonify(error_response(message="Invalid credentials")), 401
    
    access_token = create_access_token(identity=str(user.id))

    return jsonify(success_response({
        "access_token": access_token
    })), 200

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