import jwt
import datetime
import os
from typing import Dict, Any

def generate_jwt(user_id: str, jwt_secret: str) -> str:
    """
    Generates a JWT token for a given user ID.

    Args:
        user_id: The user's unique identifier (e.g., a UUID) to include in the token payload.
        jwt_secret: The secret key to sign the JWT.

    Returns:
        A JWT token string.
    """
    payload: Dict[str, Any] = {
        'sub': user_id,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
        'role': 'ROLE_CLIENTE'
    }
    token: str = jwt.encode(payload, jwt_secret, algorithm="HS256")
    return token
