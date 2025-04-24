import pytest
from src.util.dao import DAO
from pymongo.errors import WriteError

@pytest.fixture
def dao():
    dao_instance = DAO("user")
    yield dao_instance

    dao_instance.collection.delete_one({'email': 'jane.doe@gmail.com'})

@pytest.mark.integration
def test_create_valid(dao):
    data = [('firstName', 'Jane'), ('lastName', 'Doe'), ('email', 'jane.doe@gmail.com')]
    obj = dao.create(data)
    
    assert obj.get('firstName') == 'Jane'
    assert obj.get('lastName') == 'Doe'
    assert obj.get('email') == 'jane.doe@gmail.com'

@pytest.mark.integration()
def test_create_invalid_missing(dao):
    data = [('firstName', 'John'), ('lastName', 'Smith')]

    with pytest.raises(WriteError):
        dao.create(data)

@pytest.mark.integration()
def test_create_invalid_misspelled(dao):
    data = [('frstName', 'John'), ('lastName', 'Smith'), ('email', 'john.smith@gmail.com')]

    with pytest.raises(WriteError):
        dao.create(data)





