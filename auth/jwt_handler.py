import time
from typing import Dict

import jwt
from decouple import config


JWT_SECRET = config('secret')


def token_response(token: str):
    return {
        "access_token": token
    }


def sign_jwt(user_id: str) -> Dict[str, str]:
    # Set the expiry time.
    payload = {
        'user_id': user_id,
        'expires': time.time() + 2400
    }
    return token_response(jwt.encode(payload, JWT_SECRET, algorithm="HS256"))


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token.encode(), JWT_SECRET, algorithms=["HS256"])
        return decoded_token if decoded_token['expires'] >= time.time() else None
    except:
        return {}
