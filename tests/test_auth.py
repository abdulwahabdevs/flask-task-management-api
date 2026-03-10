def test_register(client):

    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@mail.com",
        "password": "123456"
    })

    assert response.status_code == 201
