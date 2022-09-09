import time
from typing import Dict

import jwt
from decouple import config


JWT_SECRET = "e9d12d19fde9c17df7279785ab7470f0224fc5bd2e449313394101591fb7aad1"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 60000
    }
    token = jwt.encode(payload, JWT_SECRET,algorithm=JWT_ALGORITHM)
    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}

