import pytest
from app import create_app
from app.extensions import db


@pytest.fixture
def app():
    app = create_app()

    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def test_user(client):

    client.post("/auth/register", json={
        "username": "tester",
        "email": "tester@mail.com",
        "password": "123456"
    })


@pytest.fixture
def auth_headers(client, test_user):

    response = client.post("/auth/login", json={
        "email": "tester@mail.com",
        "password": "123456"
    })

    token = response.get_json()["data"]["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture
def auth_client(client, auth_headers):

    class AuthClient:
        def __init__(self, client, headers):
            self.client = client
            self.headers = headers

        def get(self, url):
            return self.client.get(url, headers=self.headers)

        def post(self, url, json=None):
            return self.client.post(url, json=json, headers=self.headers)

        def put(self, url, json=None):
            return self.client.put(url, json=json, headers=self.headers)

        def delete(self, url):
            return self.client.delete(url, headers=self.headers)

    return AuthClient(client, auth_headers)
