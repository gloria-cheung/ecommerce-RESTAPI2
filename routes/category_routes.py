from flask import request, jsonify
from models import db, Category
from __main__ import app, admin_only
from datetime import datetime


# create category
@app.route('/api/categories', methods=["POST"])
@admin_only
def create_category():
    data = request.json
    try:
        new_category = Category(name=data.get("name"))
        db.session.add(new_category)
        db.session.commit()
        return jsonify(new_category.obj_to_dict())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# update category
@app.route('/api/categories/<int:category_id>', methods=["PATCH"])
@admin_only
def update_category(category_id):
    data = request.json
    try:
        found_category = Category.query.get(category_id)
        if not found_category:
            return jsonify({"error": "could not find category"}), 400
        found_category.name = data.get("name")
        found_category.updated_on = datetime.now()
        db.session.commit()
        return jsonify(found_category.obj_to_dict())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# delete category
@app.route('/api/categories/<int:category_id>', methods=["DELETE"])
@admin_only
def delete_category(category_id):
    try:
        found_category = Category.query.get(category_id)
        if not found_category:
            return jsonify({"error": "could not find category"}), 400
        db.session.delete(found_category)
        db.session.commit()
        return jsonify({"success": "category deleted"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# get category
@app.route('/api/categories/<name>')
def get_category(name):
    try:
        found_category = Category.query.filter_by(name=name).first()
        if not found_category:
            return jsonify({"error": "could not find category"}), 400
        products = [product.obj_to_dict() for product in found_category.products]
        return jsonify(products=products, category_name=found_category.name)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# get categories
@app.route('/api/categories')
def get_categories():
    try:
        categories = Category.query.all()
        return jsonify(categories=[category.obj_to_dict() for category in categories])

    except Exception as e:
        return jsonify({"error": str(e)}), 500
