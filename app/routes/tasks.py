from datetime import datetime, timezone

from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from app import app, db, task_queue
from app.jobs import deliver_notification
from app.models import Category, Task
from app.schemas import TaskResponseSchema, TaskSchema, TaskUpdateSchema


def _task_to_response(task: Task) -> dict:
    data = TaskResponseSchema().dump(task)
    data["category"] = (
        {
            "id": task.category.id,
            "name": task.category.name,
            "color": task.category.color,
        }
        if task.category
        else None
    )
    return data


def _validate_category(category_id):
    if category_id is None:
        return None
    category = Category.query.get(category_id)
    if not category:
        raise ValidationError({"category_id": ["Category does not exist."]})
    return category


@app.post("/tasks")
def create_task():
    payload = request.get_json(silent=True) or {}

    try:
        data = TaskSchema().load(payload)
        _validate_category(data.get("category_id"))
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    task = Task(
        title=data["title"],
        description=data.get("description"),
        completed=data.get("completed", False),
        due_date=data.get("due_date"),
        category_id=data.get("category_id"),
        created_at=datetime.fromisoformat(datetime.now(timezone.utc).isoformat()),
        updated_at=datetime.fromisoformat(datetime.now(timezone.utc).isoformat()),
    )

    db.session.add(task)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"errors": {"category_id": ["Invalid category reference."]}}), 400

    notification_queued = False
    if task.due_date:
        now = datetime.fromisoformat(datetime.now(timezone.utc).isoformat())
        compare_now = now if task.due_date.tzinfo is not None else now.replace(tzinfo=None)
        delta_seconds = (task.due_date - compare_now).total_seconds()
        if 0 <= delta_seconds <= 24 * 3600:
            try:
                task_queue.enqueue(deliver_notification, task.id)
                notification_queued = True
            except Exception:
                notification_queued = False

    return jsonify({"task": _task_to_response(task), "notification_queued": notification_queued}), 201


@app.get("/tasks")
def list_tasks():
    completed = request.args.get("completed")
    query = Task.query

    if completed is not None:
        normalized = completed.strip().lower()
        if normalized not in {"true", "false"}:
            return jsonify({"errors": {"completed": ["Must be true or false."]}}), 400
        query = query.filter(Task.completed.is_(normalized == "true"))

    tasks = query.order_by(Task.created_at.desc()).limit(100).all()
    return jsonify({"tasks": [_task_to_response(task) for task in tasks]}), 200


@app.get("/tasks/<int:task_id>")
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"task": _task_to_response(task)}), 200


@app.put("/tasks/<int:task_id>")
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    payload = request.get_json(silent=True) or {}
    try:
        data = TaskUpdateSchema().load(payload)
        if "category_id" in data:
            _validate_category(data.get("category_id"))
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    if "title" in data:
        task.title = data["title"]
    if "description" in data:
        task.description = data["description"]
    if "completed" in data:
        task.completed = data["completed"]
    if "due_date" in data:
        task.due_date = data["due_date"]
    if "category_id" in data:
        task.category_id = data["category_id"]
    task.updated_at = datetime.fromisoformat(datetime.now(timezone.utc).isoformat())

    db.session.commit()
    return jsonify({"task": _task_to_response(task)}), 200


@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200
