from app.models import Task
from app.extensions import db

def create(task):
    db.session.add(task)
    db.session.commit()
    return task

def get_by_id(task_id):
    return Task.query.get_or_404(task_id)

def get_user_tasks(user_id, page, per_page):
    return Task.query.filter_by(user_id=user_id).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

def update():
    db.session.commit()


def delete(task):
    db.session.delete(task)
    db.session.commit()
    