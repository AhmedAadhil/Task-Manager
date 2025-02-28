from flask import Blueprint, request, jsonify
from models import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import logger
tasks_bp = Blueprint("tasks", __name__)

# A sample model for task
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


#creation of new task
@tasks_bp.route("/tasks", methods=["POST"])
@jwt_required()
def add_task():
    data = request.get_json()
    user = get_jwt_identity()  # Get logged-in user
    title = data.get("title")

    if not title:
        logger.warning(f"Task creation failed: Missing title for user '{user}'.")
        return jsonify({"error": "Task title is required"}), 400

    new_task = Task(user=user, title=title)
    new_task.save()
    logger.info(f"Task '{title}' created by user '{user}'.")
    return jsonify({"message": "Task added successfully"}), 201


#fetching task details here
@tasks_bp.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    user = get_jwt_identity()
    tasks = Task.query.filter_by(user=user).all()
    
    return jsonify([{"id": task.id, "title": task.title, "completed": task.completed} for task in tasks])


#toggling task status
@tasks_bp.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()
def toggle_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    task.completed = not task.completed  # Toggle completion status
    db.session.commit()
    return jsonify({"message": "Task updated", "completed": task.completed})

#deleting task
@tasks_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    task.delete()
    return jsonify({"message": "Task deleted successfully"}), 200
