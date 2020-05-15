import pytest
from diaryapp.models import User
from flask import Flask
import os
import tempfile
from diaryapp import db
import diaryapp

@pytest.fixture
def client():
    db_fd, diaryapp.app.config['DATABASE'] = tempfile.mkstemp()
    diaryapp.app.config['TESTING'] = True

    with diaryapp.app.test_client() as client:
        with diaryapp.app.app_context():
            diaryapp.init_db()
        yield client

    os.close(db_fd)
    os.unlink(diaryapp.app.config['DATABASE'])
 
@pytest.fixture(scope='module')
def new_user():
    user = User(username='abc', email='abc@gmail.com', password='FlaskIsAwesome')
    return user