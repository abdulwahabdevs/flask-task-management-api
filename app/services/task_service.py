from app.models import Task
from app.extensions import db


def create_task(user_id, title, description, completed=False):
    task = Task(
        title=title,
        description=description,
        completed=completed,
        user_id=user_id
    )

    db.session.add(task)
    db.session.commit()

    return task


def get_user_tasks(user_id, page, per_page):
    return Task.query.filter_by(user_id=user_id).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )


def get_task_by_id(task_id):
    return Task.query.get_or_404(task_id)


def update_task(task, data):
    if "title" in data:
        task.title = data["title"]

    if "description" in data:
        task.description = data["description"]

    if "completed" in data:
        task.completed = data["completed"]

    db.session.commit()

    return task


def delete_task(task):
    db.session.delete(task)
    db.session.commit()