import pytest
from src.util.dao import DAO
from pymongo.errors import WriteError

dao = DAO("user")

@pytest.mark.integration
def test_create_valid():
    data = [('firstName', 'Jane'), ('lastName', 'Doe'), ('email', 'jane.doe@gmail.com')]
    obj = dao.create(data)
    
    assert obj.get('firstName') == 'Jane'
    assert obj.get('lastName') == 'Doe'
    assert obj.get('email') == 'jane.doe@gmail.com'

@pytest.mark.integration()
def test_create_invalid_missing():
    data = [('firstName', 'John'), ('lastName', 'Smith')]

    with pytest.raises(WriteError):
        dao.create(data)

@pytest.mark.integration()
def test_create_invalid_misspelled():
    data = [('frstName', 'John'), ('lastName', 'Smith'), ('email', 'john.smith@gmail.com')]

    with pytest.raises(WriteError):
        dao.create(data)





