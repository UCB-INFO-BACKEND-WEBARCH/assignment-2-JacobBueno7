from datetime import datetime, timezone
from app import db

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    due_date = db.Column(db.DateTime, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.fromisoformat(datetime.now(timezone.utc).isoformat()),
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.fromisoformat(datetime.now(timezone.utc).isoformat()),
        onupdate=lambda: datetime.fromisoformat(datetime.now(timezone.utc).isoformat()),
    )

    category = db.relationship("Category", back_populates="tasks")
    
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


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    color = db.Column(db.String(7), nullable=True)
    tasks = db.relationship("Task", back_populates="category", lazy="select")

    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color
        }