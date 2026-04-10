from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app
import time

db = SQLAlchemy()

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime, default=datetime.isoformat)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "due_date": self.due_date,
            "category_id": self.category_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
def deliver_notification(task_id):
    time.sleep(5)
    with app.app_context():
        task = Task.query.get(task_id)

        if not Task:
            print(f"[Worker] Notification {notification_id} not found!")
            return
        
        print(f"[Worker] Reminder: Task {task.title} is due soon!")


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    color = db.Column(db.String(7))
    tasks = db.relationship('TaskModel', back_populates='tasks', lazy='dynamic')

    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color
        }