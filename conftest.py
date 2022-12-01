import base64

import pytest
from flask_sqlalchemy import SQLAlchemy

from main import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    db = SQLAlchemy(app)

    with app.app_context():
        with app.test_client() as client:
            yield client


def user_id(auth_headers, client):
    resp = client.get(f'/user', headers=auth_headers)
    return resp.json['user_id']


@pytest.fixture
def auth_headers():
    valid_credentials = base64.b64encode(str.encode("testUser:pass")).decode("utf-8")
    auth_headers = {"Authorization": "Basic " + valid_credentials}
    return auth_headers


@pytest.fixture
def auth_admin_headers():
    valid_credentials = base64.b64encode(str.encode("testAdmin:password")).decode("utf-8")
    auth_headers = {"Authorization": "Basic " + valid_credentials}
    return auth_headers
