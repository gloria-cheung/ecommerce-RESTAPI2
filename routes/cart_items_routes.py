from flask import request, jsonify
from models import db, CartItem, User, Cart, Product
from flask_login import current_user, login_required
from __main__ import app


# create cart item
@app.route('/api/cart_items', methods=["POST"])
@login_required
def add_cart_item_to_cart():
    data = request.json
    try:
        cart_id = User.query.get(int(current_user.get_id())).cart[0].id
        new_cart_item = CartItem(
            cart_id=cart_id,
            product_id=int(data.get("product_id")),
            quantity=int(data.get("quantity"))
        )
        found_cart = Cart.query.get(cart_id)
        found_cart.total += Product.query.get(int(data.get("product_id"))).price * int(data.get("quantity"))
        db.session.add(new_cart_item)
        db.session.commit()
        return jsonify({"success": "item successfully added to cart"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# update cart item
@app.route('/api/cart_items/<int:cart_item_id>', methods=["PATCH"])
@login_required
def update_cart_item(cart_item_id):
    try:
        # find cart item and update qty, then update the cart total based on this change
        cart_item = CartItem.query.get(cart_item_id)
        if not cart_item:
            return jsonify({"error": "could not find cart item based on id given"}), 400

        difference_in_qty = cart_item.quantity - request.json.get("quantity")
        found_cart = Cart.query.get(cart_item.cart_id)
        found_cart.total -= cart_item.product.price * difference_in_qty
        cart_item.quantity = request.json.get("quantity")
        db.session.commit()
        return jsonify({"success": "cart item quantity successfully updated"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# delete cart item
@app.route('/api/cart_items/<int:cart_item_id>', methods=["DELETE"])
@login_required
def delete_cart_item(cart_item_id):
    try:
        # find cart item and remove from cart, then update cart total based on this removal
        cart_item = CartItem.query.get(cart_item_id)
        if not cart_item:
            return jsonify({"error": "could not find cart item based on id given"}), 400

        found_cart = Cart.query.get(cart_item.cart_id)
        found_cart.total -= cart_item.product.price * cart_item.quantity
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"success": "cart item deleted"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
