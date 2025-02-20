from app.common.auth_utils import decode_token
from app.tests.test_helpers import login_request, signup_request
from app.users.model import User


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
