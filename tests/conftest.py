
import os, sys
import pytest
import os
from os.path import join, dirname
from dotenv import load_dotenv

DOTENV_FILENAME = '.test.env'

sys.path.append("..")

# load dotenv that sets env variable APP_SETTINGS
# this should be done before importing src.restapi.app:app
# or else it will raise an error as it will not found this variable
dotenv_path = join(dirname(__file__), DOTENV_FILENAME)
load_dotenv(dotenv_path)

from src.restapi.app import app as _app
from src.restapi.database import db as _db

@pytest.fixture
def client():
    _app.config.from_object('src.restapi.config.TestingConfig')

    with _app.test_client() as client:
        _db.init_app(_app)
        with _app.app_context():
            _db.create_all()
        yield client
        with _app.app_context():
            _db.session.remove()
            _db.drop_all()

