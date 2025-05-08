import pytest
from src.util.dao import DAO
from pymongo.errors import WriteError

@pytest.fixture
def dao():
    dao_instance = DAO("test_user")
    yield dao_instance

    dao_instance.collection.delete_many({})

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

@pytest.mark.integration
def test_create_unique_email(dao):
    data1 = [('firstName', 'Jane'), ('lastName', 'Doe'), ('email', 'jane.doe@gmail.com')]
    obj1 = dao.create(data1)
    assert obj1.get('email') == 'jane.doe@gmail.com'

    data2 = [('firstName', 'John'), ('lastName', 'Smith'), ('email', 'jane.doe@gmail.com')]

    with pytest.raises(WriteError):
        dao.create(data2)


