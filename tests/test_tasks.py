def test_create_task(auth_client):

    response = auth_client.post("/tasks/", json={
        "title": "Test Task",
        "description": "Testing pytest"
    })
    print(response.get_json())
    assert response.status_code == 201


def test_get_tasks(auth_client):

    auth_client.post("/tasks/", json={
        "title": "Task 1",
        "description": "First Task"
    })

    response = auth_client.get("/tasks/")

    assert response.status_code == 200

    data = response.get_json()
    print(data)
    assert len(data["tasks"]) == 1


def test_update_taks(auth_client):

    create = auth_client.post("/tasks/", json={
        "title": "Test",
        "description": "Testing"
    })

    task_id = create.get_json()["id"]

    response = auth_client.put(f"/tasks/{task_id}", json={
        "completed": True
    })

    assert response.status_code == 200

    data = response.get_json()

    assert data["completed"] is True


def test_delete_task(auth_client):

    create = auth_client.post("/tasks/", json={
        "title": "Delete Task",
        "description": "testing deleting task"
    })

    task_id = create.get_json()["id"]

    response = auth_client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200


def test_user_cannot_access_other_users_task(client, auth_client):

    # user 1 creates task
    task = auth_client.post("/tasks/", json={
        "title": "Private Task",
        "description": "Secret tshssh"
    })

    task_id = task.get_json()["id"]

    # register 2nd user
    client.post("/auth/register", json={
        "username": "user2",
        "email": "user2@mail.com",
        "password": "123456"
    })

    login = client.post("/auth/login", json={
        "email": "user2@mail.com",
        "password": "123456"
    })

    token = login.get_json()["access_token"]

    response = client.get(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    print(response.get_json())
    assert response.status_code == 403
