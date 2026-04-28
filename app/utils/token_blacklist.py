def add_token_to_blacklist(jti, exp):
    from app.extensions import redis_client
    from datetime import datetime, timezone

    try:
        now = datetime.now(timezone.utc)
        ttl = max(int(exp - now.timestamp()), 0)

        if ttl > 0:
            redis_client.setex(jti, ttl, "true")
    except Exception:
        pass


def is_token_blacklisted(jti):
    from app.extensions import redis_client

    try:
        return redis_client.exists(jti) == 1
    except Exception:
        return False