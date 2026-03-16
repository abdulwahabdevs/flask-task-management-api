def test_register(client):

    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@mail.com",
        "password": "123456"
    })

    assert response.status_code == 201


def test_register_diplicate_user(client, test_user):

    response = client.post("/auth/register", json={
        "username": "tester",
        "email": "tester@mail.com",
        "password": "123456"
    })

    assert response.status_code == 400


def test_login_success(client, test_user):

    response = client.post("/auth/login", json={
        "email": "tester@mail.com",
        "password": "123456"
    })

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert "access_token" in data


def test_login_wrong_password(client, test_user):

    response = client.post("/auth/login", json={
        "email": "tester@mail.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 401

def test_access_without_token(client):

    response = client.get("/tasks/")

    assert response.status_code == 401

