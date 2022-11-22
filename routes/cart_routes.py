from flask import jsonify
from models import db, Cart, CartItem
from flask_login import current_user, login_required
from __main__ import app


# get cart
@app.route('/api/cart')
def get_cart():
    try:
        found_cart = Cart.query.filter_by(user_id=int(current_user.get_id())).first()
        if not found_cart:
            return jsonify({"error": "could not find cart based on user_id"})
        return jsonify(cart=found_cart.obj_to_dict(), cart_items=[item.obj_to_dict() for item in found_cart.cart_items])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# create cart
@app.route('/api/cart', methods=["POST"])
@login_required
def create_cart():
    try:
        new_cart = Cart(
            user_id=int(current_user.get_id())
        )
        db.session.add(new_cart)
        db.session.commit()
        return jsonify(new_cart.obj_to_dict())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# clear cart of items
@app.route('/api/cart/', methods=["PATCH"])
@login_required
def update_cart():
    try:
        # find cart, delete all cart items associated with this cart and update cart total to be 0
        found_cart = Cart.query.filter_by(user_id=int(current_user.get_id())).first()
        if not found_cart:
            return jsonify({"error": "could not find cart based on user_id"}), 400

        cart_items = CartItem.query.filter_by(cart_id=found_cart.id).all()
        for item in cart_items:
            db.session.delete(item)
            db.session.commit()

        found_cart.total = 0
        db.session.commit()

        return jsonify(cart=found_cart.obj_to_dict(), cart_items=[item.obj_to_dict() for item in found_cart.cart_items])

    except Exception as e:
        return jsonify({"error": str(e)}), 500
