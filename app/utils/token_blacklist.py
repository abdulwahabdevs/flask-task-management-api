from flask_jwt_extended import get_jwt
from datetime import datetime, timezone


def add_token_to_blacklist(jti, exp):
    from app.extensions import redis_client

    now = datetime.now(timezone.utc)
    ttl = int(exp - now.timestamp())

    redis_client.setex(jti, ttl, "true")


def is_token_blacklisted(jti):
    from app.extensions import redis_client

    return redis_client.exists(jti) == 1