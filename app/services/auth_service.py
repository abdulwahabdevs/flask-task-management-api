from app.models import User
from app.extensions import db
from app.errors.exceptions import AuthError
from app.utils.response import success_response, error_response
from app.utils.token_blacklist import add_token_to_blacklist
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

class AuthService:

    @staticmethod
    def register(data):
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            raise AuthError("User already exists", 400)
        
        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            password_hash=hashed_password
        )
        db.session.add(user)
        db.session.commit()

        return True


    @staticmethod
    def login(data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise AuthError("Missing email or password", 400)
        
        user = User.query.filter_by(email=email).first()

        if not user:
            raise AuthError("Invalid credentials", 401)
        
        if not check_password_hash(user.password_hash, password):
            raise AuthError("Invalid credentials", 401)
        
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }


    @staticmethod
    def refresh(token, user_id):
        jti = token["jti"]
        exp = token["exp"]

        # revoke used refresh token
        add_token_to_blacklist(jti, exp)

        new_access_token = create_access_token(identity=user_id)
        new_refresh_token = create_refresh_token(identity=user_id)

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }

    @staticmethod
    def logout(token):
        jti = token["jti"]
        exp = token["exp"]

        add_token_to_blacklist(jti, exp)

        return True

