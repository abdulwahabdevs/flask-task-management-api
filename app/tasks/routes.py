from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.tasks import tasks_bp
from app.services import task_service
from app.schemas.task_schema import TaskSchema
from app.utils.response import success_response, error_response

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


@tasks_bp.route("/", methods=["POST"])
@jwt_required()
def create_task():
    user_id = int(get_jwt_identity())
    
    data = task_schema.load(request.json)

    response, status = task_service.create_task(user_id, data)
    
    return jsonify(response), status


@tasks_bp.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = int(get_jwt_identity())

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    response, status = task_service.get_tasks(
        user_id,
        page,
        per_page
    )

    return jsonify(response), status


@tasks_bp.route("/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    user_id = int(get_jwt_identity())

    response, status = task_service.get_task(task_id, user_id)

    return jsonify(response), status


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    user_id = int(get_jwt_identity())
    
    data = task_schema.load(request.json, partial=True)
    
    response, status = task_service.update_task(
        task_id,
        user_id,
        data
    )

    return jsonify(response), status


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    user_id = int(get_jwt_identity())

    response, status = task_service.delete_task(task_id, user_id)

    return jsonify(response), status