import pytest
from unittest.mock import patch
from app.common.jwt import create_token


SECRET_KEY = "test-secret"
ALGORITHM = "HS256"


@pytest.fixture
def mock_encode():
    with patch("app.common.jwt.jwt.encode") as mock:
        yield mock


def test_create_token(mock_encode):
    mock_encode.return_value = "mocked-token"
    data = {"sub": "test@example.com"}
    token = create_token(data)
    assert isinstance(token, str)
    assert token == "mocked-token"
    mock_encode.assert_called_once()