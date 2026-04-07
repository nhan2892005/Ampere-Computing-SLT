import pytest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

os.environ["DB_PATH"] = ":memory:"
os.environ["TESTING"] = "1"

import db
from be import app as flask_app


@pytest.fixture()
def app():
    flask_app.config["TESTING"] = True
    db.init_db()
    yield flask_app


@pytest.fixture()
def client(app):
    return app.test_client()