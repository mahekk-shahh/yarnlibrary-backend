from secrets import token_urlsafe
import hashlib

def generate_reset_token():
    raw_token = token_urlsafe(32)
    hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()

    return raw_token, hashed_token
