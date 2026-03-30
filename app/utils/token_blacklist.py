TOKEN_BLOCKLIST = "token_blocklist"


def add_token_to_blacklist(jti):
    from app.extensions import redis_client
    redis_client.sadd(TOKEN_BLOCKLIST, jti)


def is_token_blacklisted(jti):
    from app.extensions import redis_client
    return redis_client.sismember(TOKEN_BLOCKLIST, jti)