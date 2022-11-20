from flask import request, jsonify
from models import db, Product
from __main__ import app, admin_only
from datetime import datetime


# get product
@app.route('/api/products/<int:product_id>')
def get_product(product_id):
    try:
        found_product = Product.query.get(product_id)
        if not found_product:
            return jsonify({"error": "could not find product"}), 400
        return jsonify(found_product.obj_to_dict())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# get all products
@app.route('/api/products/', methods=["GET"])
def get_products():
    try:
        products = Product.query.all()
        results = [product.obj_to_dict() for product in products]
        return jsonify(products=results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# create product
@app.route('/api/products/', methods=["POST"])
@admin_only
def create_product():
    data = request.json
    try:
        new_product = Product(
            name=data.get("name"),
            desc=data.get("desc"),
            inventory=int(data.get("inventory")),
            price=float(data.get("price")),
            category_id=int(data.get("category_id")),
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify(new_product.obj_to_dict())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# update product
@app.route('/api/products/<int:product_id>', methods=["PATCH"])
@admin_only
def update_product(product_id):
    data = request.json
    try:
        found_product = Product.query.get(product_id)
        if not found_product:
            return jsonify({"error": "could not find product"}), 400

        found_product.name = data.get("name")
        found_product.desc = data.get("desc")
        found_product.inventory = int(data.get("inventory"))
        found_product.price = float(data.get("price"))
        found_product.category_id = int(data.get("category_id"))
        found_product.updated_on = datetime.now()

        db.session.commit()
        return jsonify(found_product.obj_to_dict())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# delete product
@app.route('/api/products/<int:product_id>', methods=["DELETE"])
@admin_only
def delete_product(product_id):
    try:
        found_product = Product.query.get(product_id)
        if not found_product:
            return jsonify({"error": "could not find product"}), 400
        db.session.delete(found_product)
        db.session.commit()
        return jsonify({"success": "product deleted"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
