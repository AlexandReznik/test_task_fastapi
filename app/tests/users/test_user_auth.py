import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.common.auth_utils import decode_token
from app.common.database import Base, get_db
from app.main import app
from app.users.model import User


TEST_DATABASE_URL = "sqlite://"
SECRET_KEY = "test-secret"
ALGORITHM = "HS256"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_client(db_session):

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def user_payload():
    return {
        'username': 'test_username',
        'login': 'test_login',
        'password': 'testpassword'
    }


def signup_request(user_payload, test_client):
    return test_client.post('user/sign-up/', json=user_payload)


def login_request(user_payload, test_client):
    return test_client.post('user/login/', json=user_payload)


def test_registration(test_client, db_session, user_payload):
    response = signup_request(user_payload, test_client)
    user = db_session.query(User).filter_by(login=user_payload['login']).first()
    assert response.status_code == 200
    assert user.username == user_payload['username']


def test_authorization(test_client, db_session, user_payload):
    signup_request(user_payload, test_client)
    response = login_request(user_payload, test_client)
    assert response.status_code == 200
    assert decode_token(response.json()['token'])['sub'] == user_payload['login']


def test_registration_with_existing_login(test_client, db_session, user_payload):
    signup_request(user_payload, test_client)
    response = signup_request(user_payload, test_client)
    assert response.status_code == 400
    assert response.json()['detail'] == 'User already exists'


def test_wrong_authorization_credentials(test_client, db_session, user_payload):
    signup_request(user_payload, test_client)
    response = login_request({'login': 'wronglogin', 'password': 'wrongpasswd'}, test_client)
    assert response.status_code == 400
    assert response.json()['detail'] == "User doesn't exist"
