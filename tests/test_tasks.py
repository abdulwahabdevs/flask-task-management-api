def test_create_task(auth_client):

    response = auth_client.post("/tasks/", json={
        "title": "Test Task",
        "description": "Testing pytest"
    })

    assert response.status_code == 201

    data = response.get_json()["data"]

    assert data["title"] == "Test Task"
    assert data["description"] == "Testing pytest"
    assert data["completed"] is False

def test_get_tasks(auth_client):

    auth_client.post("/tasks/", json={
        "title": "Task 1",
        "description": "First Task"
    })

    response = auth_client.get("/tasks/")

    assert response.status_code == 200

    data = response.get_json()["data"]
  
    assert len(data["tasks"]) == 1


def test_update_task(auth_client):

    create = auth_client.post("/tasks/", json={
        "title": "Test",
        "description": "Testing"
    })

    task_id = create.get_json()["data"]["id"]

    response = auth_client.put(f"/tasks/{task_id}", json={
        "completed": True
    })

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert data["completed"] is True


def test_delete_task(auth_client):

    create = auth_client.post("/tasks/", json={
        "title": "Delete Task",
        "description": "testing deleting task"
    })

    task_id = create.get_json()["data"]["id"]

    response = auth_client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["message"] == "Task deleted successfully"

def test_user_cannot_access_other_users_task(client, auth_client):

    # user 1 creates task
    task = auth_client.post("/tasks/", json={
        "title": "Private Task",
        "description": "Secret tshssh"
    })

    task_id = task.get_json()["data"]["id"]

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

    print(login.get_json())
    token = login.get_json()["data"]["access_token"]


    response = client.get(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403


def test_create_task_missing_title(auth_client):

    response = auth_client.post("/tasks/", json={
        "description": "no title"
    })

    assert response.status_code == 400


def test_create_task_invalid_completed(auth_client):

    response = auth_client.post("/tasks/", json={
        "title": "Task",
        "description": "test",
        "completed": "yes"
    })

    assert response.status_code == 400