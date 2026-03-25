# temporary in-memory blacklist
BLACKLIST = set()


def add_token_to_blacklist(jti):
    BLACKLIST.add(jti)


def is_token_blacklisted(jti):
    return jti in BLACKLIST