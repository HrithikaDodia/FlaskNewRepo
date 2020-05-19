import pytest
from diaryapp.models import User
from flask import Flask
import os
import tempfile
from diaryapp import db
from diaryapp import create_app
import diaryapp


class TestConfig(object):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = os.environ.get('SECRET_KEY', '62582fc136cac3457137050bc8d857c4')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


# @pytest.fixture(scope='module')
# def client(request):
#     flask_app = create_app(TestConfig)

#     # Flask provides a way to test your application by exposing the Werkzeug test Client
#     # and handling the context locals for you.

#     testing_client = flask_app.test_client()

#     # Establish an application context before running the tests.
#     ctx = flask_app.app_context()
#     ctx.push()

#     def teardown():
#         ctx.pop()

#     request.addfinalizer(teardown)
#     return testing_client

# @pytest.fixture(scope='function')
# def session(request):
#     """Creates a new database session for a test."""
#     # connect to the database
#     _db.app = client
#     _db.create_all()
#     connection = _db.engine.connect()
#     # begin a non-ORM transaction
#     transaction = connection.begin()

#     # bind an individual session to the connection
#     options = dict(bind=connection, binds={})
#     session = _db.create_scoped_session(options=options)

#     # overload the default session with the session above
#     _db.session = session

#     user = User(email = 'abc@gmail.com', username = 'abc', password='Flaskisawesome')
#     session.add(user)
#     session.commit()
    

#     def teardown():
#         session.close()
#         # rollback - everything that happened with the
#         # session above (including calls to commit())
#         # is rolled back.
#         transaction.rollback()
#         # return connection to the Engine
#         connection.close()
#         session.remove()

#     request.addfinalizer(teardown)
#     return session

@pytest.fixture(scope='module')
def client():
    flask_app = create_app(TestConfig)
 
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
 
    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
 
    yield testing_client  # this is where the testing happens!
 
    ctx.pop()

@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table
    db.create_all()
 
    # Commit the changes for the users
    db.session.commit()
 
    yield db  # this is where the testing happens!
 
    db.drop_all()

@pytest.fixture(scope='module')
def new_user():

    user = User(username='abc', email='flask@email.com', password='flaskpass')
    db.session.add(user)
    db.session.commit()
    return User.query.filter_by(email = 'flask@email.com').first()