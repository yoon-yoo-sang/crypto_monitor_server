import jwt
from dotenv import load_dotenv

from src.utils.jwt_utils import create_access_token, verify_token
from src.config.settings import JWT_SECRET_KEY


load_dotenv()


def test_create_access_token():
    data = {"sub": "test_user"}
    token = create_access_token(data)
    assert token is not None
    decoded_data = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    assert decoded_data["sub"] == "test_user"


def test_verify_token():
    data = {"sub": "test_user"}
    token = create_access_token(data)
    result = verify_token(token)
    assert result is not None
    assert result["sub"] == "test_user"


def test_invalid_token():
    token = "invalid.token.string"
    result = verify_token(token)
    assert result is None
