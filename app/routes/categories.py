from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from app import app, db
from app.models import Category
from app.schemas import CategorySchema


@app.post("/categories")
def create_category():
    payload = request.get_json(silent=True) or {}

    try:
        data = CategorySchema().load(payload)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    category = Category(name=data["name"], color=data.get("color"))
    db.session.add(category)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"errors": {"name": ["Category name must be unique."]}}), 400

    return jsonify({"category": {"id": category.id, "name": category.name, "color": category.color}}), 201


@app.get("/categories")
def list_categories():
    categories = Category.query.order_by(Category.id.asc()).limit(100).all()

    result = []
    for category in categories:
        result.append(
            {
                "id": category.id,
                "name": category.name,
                "color": category.color,
                "task_count": len(category.tasks),
            }
        )

    return jsonify({"categories": result}), 200


@app.get("/categories/<int:category_id>")
def get_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    tasks = [
        {
            "id": task.id,
            "title": task.title,
            "completed": task.completed,
        }
        for task in category.tasks
    ]

    return (
        jsonify(
            {
                "id": category.id,
                "name": category.name,
                "color": category.color,
                "tasks": tasks,
            }
        ),
        200,
    )


@app.delete("/categories/<int:category_id>")
def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    if len(category.tasks) > 0:
        return (
            jsonify(
                {
                    "error": "Cannot delete category with existing tasks. Move or delete tasks first."
                }
            ),
            400,
        )

    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted"}), 200
