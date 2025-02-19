from unittest import mock
from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from app.users import crud
from app.users.model import User


@pytest.fixture
def db_session():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_user():
    return User(
        id=1,
        username="John Doe",
        login="johndoe@example.com",
        password="hashedpassword",
    )


@pytest.fixture
def user_create():
    return {
        "username": "John Doe",
        "login": "john@example.com",
        "password": "password",
    }


def test_create_user(db_session, user_create):
    db_session.query().filter_by().first.return_value = None 

    with mock.patch("app.users.crud.get_password_hash", return_value="hashedpassword"):
        result = crud.create_user(
            user_create["username"],
            user_create["login"],
            user_create["password"],
            db_session,
        )

    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once()
    
    assert result.login == user_create["login"]
    assert result.password == "hashedpassword"



def test_create_user_already_exists(db_session, user_create):
    db_session.query().filter_by().first.return_value = True 

    with pytest.raises(Exception) as exc_info:
        crud.create_user(
            user_create["username"],
            user_create["login"],
            user_create["password"],
            db_session,
        )

    assert "User already exists" in str(exc_info.value)
    db_session.add.assert_not_called()
    db_session.commit.assert_not_called()


def test_authenticate_user_success(db_session, mock_user):
    db_session.query().filter_by().first.return_value = mock_user  

    with mock.patch("app.users.crud.verify_password", return_value=True), \
         mock.patch("app.users.crud.create_token", return_value="mocked_token"):
        result = crud.authenticate_user(
            login="johndoe@example.com",
            password="password",
            db=db_session
        )

    assert result == "mocked_token"


def test_authenticate_user_invalid_email(db_session):
    db_session.query().filter_by().first.return_value = None  

    with pytest.raises(Exception) as exc_info:
        crud.authenticate_user(
            login="unknown@example.com",
            password="password",
            db=db_session
        )

    assert "User doesn't exist" in str(exc_info.value)


def test_authenticate_user_invalid_password(db_session, mock_user):
    db_session.query().filter_by().first.return_value = mock_user  

    with mock.patch("app.users.crud.verify_password", return_value=False):
        with pytest.raises(Exception) as exc_info:
            crud.authenticate_user(
                login="johndoe@example.com",
                password="wrongpassword",
                db=db_session
            )

    assert "User doesn't exist" in str(exc_info.value)
