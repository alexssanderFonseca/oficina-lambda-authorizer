import jwt
import datetime
from app.service.jwt_generator import generate_jwt

def test_generate_jwt():
    """
    Tests the generation of a JWT token.
    """
    user_id = "test_user_id"
    jwt_secret = "test_secret"

    token = generate_jwt(user_id, jwt_secret)

    decoded_payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])

    assert decoded_payload['sub'] == user_id
    assert 'exp' in decoded_payload

    # Check that the expiration is in the future
    expiration_time = datetime.datetime.fromtimestamp(decoded_payload['exp'], tz=datetime.timezone.utc)
    assert expiration_time > datetime.datetime.now(datetime.timezone.utc)
