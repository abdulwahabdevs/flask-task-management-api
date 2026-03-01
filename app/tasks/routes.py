from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.tasks import tasks_bp
from app.models import Task
from app.extensions import db

@tasks_bp.route("/", methods=["POST"])
@jwt_required()
def create_task():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data:
        return jsonify({"error":"Invalid JSON"}), 400

    title = data.get("title")
    description = data.get("description")

    if not title or not description:
        return jsonify({"error": "Title and description is required"}), 400
    
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
