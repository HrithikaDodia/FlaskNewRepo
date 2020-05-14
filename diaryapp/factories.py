import pytest
from diaryapp.models import User
 
 
@pytest.fixture(scope='module')
def new_user():
    user = User(username='abc', email='abc@gmail.com', password='FlaskIsAwesome')
    return user