import jwt
import datetime
from typing import Dict, Any

# TODO: Store this secret securely, for example in AWS Secrets Manager
JWT_SECRET: str = "your-super-secret"

def generate_jwt(user_id: str) -> str:
    """
    Generates a JWT token for a given user ID.

    Args:
        user_id: The user's unique identifier (e.g., a UUID) to include in the token payload.

    Returns:
        A JWT token string.
    """
    payload: Dict[str, Any] = {
        'sub': user_id,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }
    token: str = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token
