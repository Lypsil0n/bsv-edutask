import pytest
from src.controllers.usercontroller import UserController
from unittest.mock import MagicMock

mockeddao = MagicMock()

@pytest.mark.unit
def test_get_user_by_email_unique():
    email = "jane.doe@gmail.com"
    mockeddao.find.return_value = [{'email': email}]

    sut = UserController(mockeddao)
    result = sut.get_user_by_email(email)
    assert result['email'] == email

@pytest.mark.unit
def test_get_user_by_email_not_unique():
    email = "john.smith@gmail.com"
    mockeddao.find.return_value = [{'email': email}, {'email': email}]

    sut = UserController(mockeddao)
    result = sut.get_user_by_email(email)
    assert result['email'] == email
    
@pytest.mark.unit
def test_get_user_by_email_does_not_exist():
    email = "missing.user@gmail.com"
    mockeddao.find.return_value = []

    sut = UserController(mockeddao)
    result = sut.get_user_by_email(email)
    assert result is None

@pytest.mark.unit
def test_get_user_by_email_value_error():
    email = "not-an-email"
    mockeddao.find.return_value = [{'email': email}]

    sut = UserController(mockeddao)
    with pytest.raises(ValueError):
        sut.get_user_by_email(email)
