from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.tasks import tasks_bp
from app.services import task_service
from app.schemas.task_schema import TaskSchema

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


@tasks_bp.route("/", methods=["POST"])
@jwt_required()
def create_task():
    user_id = int(get_jwt_identity())
    data = task_schema.load(request.json)

    task = task_service.create_task(
        user_id,
        data["title"],
        data["description"],
        data.get("completed", False)
    )

    return jsonify(task_schema.dump(task)), 201


@tasks_bp.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = int(get_jwt_identity())

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    pagination = task_service.get_user_tasks(user_id, page, per_page)

    tasks = pagination.items

    result = tasks_schema.dump(tasks)

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
    
    return jsonify(task_schema.dump(task)), 200


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    user_id = int(get_jwt_identity())
    task = task_service.get_task_by_id(task_id)

    if task.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403
    
    data = task_schema.load(request.json, partial=True)

    if not data:
        return jsonify({
            "error": "At least one of title, description, or completed must be provided"
        }), 400
    
    task = task_service.update_task(task, data)

    return jsonify(task_schema.dump(task)), 200


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    user_id = int(get_jwt_identity())
    task = task_service.get_task_by_id(task_id)

    if task.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403
    
    task_service.delete_task(task)

    return jsonify({"message": "Task deleted successfully"}), 200