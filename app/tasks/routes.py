from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.tasks import tasks_bp
from app.services import task_service


def validate_task_data(data, require_all_fields=False):
    errors = {}

    title = data.get("title")
    description = data.get("description")
    completed = data.get("completed")

    if require_all_fields:
        if not title:
            errors["title"] = "Title is required"
        
        if not description:
            errors["description"] = "Description is required"

    if title is not None and not isinstance(title, str):
        errors["title"] = "Title must be string"
    
    if description is not None and not isinstance(description, str):
        errors["description"] = "Description must be string"

    if completed is not None and not isinstance(completed, bool):
        errors["completed"] = "Completed must be true or false"

    return errors


def serialize_task(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    }


@tasks_bp.route("/", methods=["POST"])
@jwt_required()
def create_task():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if data is None:
        return jsonify({"error":"Invalid JSON"}), 400
    
    title = data.get("title")
    description = data.get("description")
    completed = data.get("completed", False)
    
    errors = validate_task_data(data, require_all_fields=True)
    
    if errors:
        return jsonify({"errors": errors}), 400
    
    task = task_service.create_task(
        user_id,
        title,
        description,
        completed
    )

    return jsonify(serialize_task(task)), 201


@tasks_bp.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = int(get_jwt_identity())

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    pagination = task_service.get_user_tasks(user_id, page, per_page)

    tasks = pagination.items

    result = [serialize_task(task) for task in tasks]

    return jsonify({
        "tasks": result,
        "page": pagination.page,
        "pages": pagination.pages,
        "total": pagination.total
    }), 200


@tasks_bp.route("/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    user_id = int(get_jwt_identity())

    task = task_service.get_task_by_id(task_id)

    if task.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403
    
    return jsonify(serialize_task(task)), 200


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    user_id = int(get_jwt_identity())
    task = task_service.get_task_by_id(task_id)

    if task.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403
    
    data = request.get_json()

    if data is None:
        return jsonify({"error":"Invalid JSON"}), 400

    allowed_fields = {"title", "description", "completed"}

    if not any(field in data for field in allowed_fields):
        return jsonify({
            "error": "At least one of title, description, or completed must be provided"
        }), 400
    
    errors = validate_task_data(data)
    
    if errors:
        return jsonify({"errors": errors}), 400

    task = task_service.update_task(task, data)

    return jsonify(serialize_task(task)), 200


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    user_id = int(get_jwt_identity())
    task = task_service.get_task_by_id(task_id)

    if task.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403
    
    task_service.delete_task(task)

    return jsonify({"message": "Task deleted successfully"}), 200