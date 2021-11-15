
import os, sys
import pytest

sys.path.append("..")

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

