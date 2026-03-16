from app.models import Task
from app.repositories import task_repository


def create_task(user_id, title, description, completed=False):
    task = Task(
        title=title,
        description=description,
        completed=completed,
        user_id=user_id
    )

    return task_repository.create(task)


def get_user_tasks(user_id, page, per_page):
    return task_repository.get_user_tasks(user_id, page, per_page)


def get_task_by_id(task_id):
    return task_repository.get_by_id(task_id)


def update_task(task, data):
    if "title" in data:
        task.title = data["title"]

    if "description" in data:
        task.description = data["description"]

    if "completed" in data:
        task.completed = data["completed"]

    task_repository.update()

    return task


def delete_task(task):
    task_repository.delete(task)