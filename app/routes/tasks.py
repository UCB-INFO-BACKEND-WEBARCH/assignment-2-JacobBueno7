from flask import Flask, request, jsonify
from datetime import datetime

from app import app, task_queue
from app.models import db, Task
from schemas import TaskSchema, deliver_notification, TaskResponseSchema

@app.post("/tasks")
def create_task():
    send_notif = False
    data = request.get_json()
    schema = TaskSchema()
    try:
        data = schema.load(data)
    except Exception as err:
        return jsonify({"errors": str(err)}), 400
    
    task = Task(
        title=data["title"],
        description=data["description"],
        completed=False,
        due_date=data["due_date"],
        category_id=data["category_id"],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.session.add(task)
    db.session.commit()

    try:
        due_date = task.due_date
        diff = due_date - datetime.utcnow
        hrs = diff / 3600
        if diff <= 24 and diff >=0:
            task_queue.enqueue(deliver_notification, task.id)
            send_notif = True
    except:
        print("No due date")

    task_response_schema = TaskResponseSchema()

    return jsonify({"task": task_response_schema.dump(task), "notification_queued": send_notif}), 201


@app.get('/tasks')
def list_tasks():

    completed = request.args.get("completed")

    query = Task.query

    if completed:
        query = query.filter_by(completed=completed)

    tasks = query.order_by(Task.created_at.desc()).limit(100).all()

    schema = TaskResponseSchema(many=True)
    return jsonify(schema.dump(tasks)), 200

@app.get('/tasks/<int:task_id>')
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    schema = TaskResponseSchema()
    return jsonify(schema.dump(task)), 200


@app.put('/tasks/<int:task_id>')
def update_task(task_id):
    data = request.get_json()
    schema = TaskSchema()

    try:
        data = schema.load(data)
    except Exception as err:
        return jsonify({"errors": str(err)}), 400
    

    task = Task.query.get_or_404(task_id)

    task.completed = data.get("completed", False)
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.due_date = data.get("due_date", task.due_date)
    task.updated_at = datetime.utcnow()

    db.session.commit()

    schema = TaskResponseSchema()
    return jsonify(schema.dump(task)), 200

@app.delete("/task/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted"}), 200