from app.models import Task
from app.repositories import task_repository
from app.schemas.task_schema import TaskSchema
from app.utils.response import success_response, error_response

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

def create_task(user_id, data):
    task = Task(
        title=data["title"],
        description=data["description"],
        completed=data.get("completed", False),
        user_id=user_id
    )

    task_repository.create(task)

    return success_response(task_schema.dump(task)), 201



def get_tasks(user_id, page, per_page):
    pagination = task_repository.get_user_tasks(
        user_id,
        page, 
        per_page
    )

    tasks = tasks_schema.dump(pagination.items)

    return success_response({
        "tasks": tasks,
        "page": pagination.page,
        "pages": pagination.pages,
        "total": pagination.total
    }), 200

def get_task(task_id, user_id):
    task = task_repository.get_by_id(task_id)

    if not task:
        return error_response(message="Task not found"), 404

    if task.user_id != user_id:
        return error_response(message="Forbidden"), 403
    
    return success_response(task_schema.dump(task)), 200


def update_task(task_id, user_id, data):
    task = task_repository.get_by_id(task_id)

    if not task:
        return error_response(message="Task not found"), 404

    if task.user_id != user_id:
        return error_response(message="Forbidden"), 403
    
    if not data:
        return error_response(
            message="At least one of title, description, or completed must be provided"
        ), 400

    if "title" in data:
        task.title = data["title"]

    if "description" in data:
        task.description = data["description"]

    if "completed" in data:
        task.completed = data["completed"]

    task_repository.update()

    return success_response(task_schema.dump(task)), 200


def delete_task(task_id, user_id):
    task = task_repository.get_by_id(task_id)

    if not task:
        return error_response(message="Task not found"), 404

    if task.user_id != user_id:
        return error_response(message="Forbidden"), 403
    
    task_repository.delete(task)

    return success_response(
        message="Task deleted successfully"
    ), 200