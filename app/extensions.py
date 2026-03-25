from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.utils.token_blacklist import is_token_blacklisted


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return is_token_blacklisted(jti)