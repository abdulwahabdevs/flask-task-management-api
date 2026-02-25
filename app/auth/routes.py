from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User
from werkzeug.security import generate_password_hash


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing required details"}), 400
    
    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        return jsonify({"error": "User already exists"}), 400
    
    hashed_password = generate_password_hash(password)

    user = User(
        username=username,
        email=email,
        password_hash=hashed_password
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201