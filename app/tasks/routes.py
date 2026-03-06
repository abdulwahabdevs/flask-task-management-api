from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.tasks import tasks_bp
from app.models import Task
from app.extensions import db

@tasks_bp.route("/", methods=["POST"])
@jwt_required()
def create_task():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    if data is None:
        return jsonify({"error":"Invalid JSON"}), 400
    
    title = data.get("title")
    description = data.get("description")
    
    errors = {}

    if not title:
        errors["title"] = "Title is required"
    
    if not description:
        errors["description"] = "Description is required!"

    if errors:
        return jsonify({"errors": errors}), 400
    
    task = Task(
                title=title,
                description=description,
                user_id=user_id
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description
    }), 201

@tasks_bp.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = int(get_jwt_identity())

    tasks = Task.query.filter_by(user_id=user_id).all()

    result = []
    for task in tasks:
        result.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        })

    return jsonify(result), 200

@tasks_bp.route("/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    user_id = int(get_jwt_identity())

    task = Task.query.get_or_404(task_id)

    if task.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403
    
    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    }), 200

@tasks_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    user_id = int(get_jwt_identity())
    task = Task.query.get_or_404(task_id)

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
    
    errors = {}
    
    if "title" in data and not isinstance(data["title"], str):
        errors["title"] = "Title must be string"

    if "description" in data and not isinstance(data["description"], str):
        errors["description"] = "Description must be a string"

    if "completed" in data and not isinstance(data["completed"], bool):
        errors["completed"] = "Completed must be true or false"

    if errors:
        return jsonify({"errors": errors}), 400

    if "title" in data:
        task.title = data["title"]

    if "description" in data:
        task.description = data["description"]

    if "completed" in data:
        task.completed = data["completed"]
    
    db.session.commit()

    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    }), 200

@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    user_id = int(get_jwt_identity())
    task = Task.query.get_or_404(task_id)

    if task.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403
    
    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted successfully"}), 200