from flask import jsonify
from models import db, Order, OrderItem, Cart
from flask_login import current_user, login_required
from __main__ import app


# get orders
@app.route('/api/orders')
@login_required
def get_orders():
    try:
        orders = Order.query.filter_by(user_id=int(current_user.get_id())).all()

        return jsonify(orders=[order.obj_to_dict() for order in orders])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# get single order
@app.route('/api/orders/<int:order_id>')
@login_required
def get_order(order_id):
    try:
        found_order = Order.query.get(order_id)
        if not found_order:
            return jsonify({"error": "could not find order based on order_id"}), 400

        order_items = []
        for item in found_order.order_items:
            result = item.obj_to_dict()
            result["product"] = item.product.obj_to_dict()
            order_items.append(result)

        return jsonify(order=found_order.obj_to_dict(), order_items=order_items)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# create order
@app.route('/api/orders', methods=["POST"])
@login_required
def create_order():
    try:
        found_cart = Cart.query.filter_by(user_id=int(current_user.get_id())).first()
        if not found_cart:
            return jsonify({"error": "could not find cart based on current user"}), 400

        new_order = Order(
            user_id=int(current_user.get_id()),
            total=found_cart.total
        )
        db.session.add(new_order)
        db.session.commit()

        for cart_item in found_cart.cart_items:
            new_order_item = OrderItem(
                order_id=new_order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity
            )
            db.session.add(new_order_item)
            db.session.commit()
        return jsonify(new_order.obj_to_dict())

    except Exception as e:
        return jsonify({"error": str(e)}), 500




