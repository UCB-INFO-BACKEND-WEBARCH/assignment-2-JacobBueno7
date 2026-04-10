from flask import Flask, request, jsonify
from datetime import datetime

from app import app, task_queue
from app.models import db, Category
from schemas import CategorySchema, CategoryResponseSchema

app.post('/categories')
def create_category():
    data = request.get_json()

    schema = CategorySchema()

    try:
        data = schema.load(data)
    except Exception as err:
        return jsonify({"errors": str(err)}), 400
    
    category = Category(
        name=data["name"],
        color=data["color"]
    )

    db.session.add(category)
    db.session.commit()

    response_schema = CategoryResponseSchema()
    return jsonify(response_schema.dump(category)), 201

app.get('/categories')
def list_categories():
    query = Category.query

    categories = query.limit(100).all() # not sure how to aggregate the tasks as an attribute

    response_schema = CategoryResponseSchema(many=True)
    return jsonify(response_schema.dump(categories)), 200

@app.get('/categories/<int:category_id>')
def get_category(category_id):
    category = Category.query.get_or_404(category_id)
    schema = CategoryResponseSchema()
    return jsonify(schema.dump(category)), 200

@app.delete('/categories/<int:category_id>')
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)

    db.session.delete(category)
    db.session.commit()

    if len(category.tasks) > 0:
        return jsonify({"error": "Cannot delete category with existing tasks. Move or delete tasks first."}), 400
        

    return jsonify({"message": "Category deleted"}), 200