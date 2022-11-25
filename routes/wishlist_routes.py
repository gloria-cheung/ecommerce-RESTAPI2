from flask import jsonify, request
from models import db, WishList, WishListItem
from flask_login import current_user, login_required
from __main__ import app

# create wishlist
@app.route('/api/wishlist', methods=["POST"])
@login_required
def create_wishlist():
    try:
        wishlist = WishList(user_id=int(current_user.get_id()))
        db.session.add(wishlist)
        db.session.commit()

        return jsonify(wishlist.obj_to_dict())

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# get wishlist
@app.route('/api/wishlist')
@login_required
def get_wishlist():
    try:
        found_wishlist = WishList.query.filter_by(user_id=int(current_user.get_id())).first()
        if not found_wishlist:
            return jsonify({"error": "could not find wishlist based on user_id"}), 200

        wishlist_items = []
        for item in found_wishlist.wish_list_items:
            result = item.obj_to_dict()
            result["product"] = item.product.obj_to_dict()
            wishlist_items.append(result)

        return jsonify(wishlist=found_wishlist.obj_to_dict(), wishlist_items=wishlist_items)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# add item to wishlist
@app.route('/api/wishlist/<int:wishlist_id>', methods=["POST"])
@login_required
def add_to_wishlist(wishlist_id):
    try:
        new_wishlist_item = WishListItem(
            wishlist_id=wishlist_id,
            product_id=request.json.get("product_id")
        )
        db.session.add(new_wishlist_item)
        db.session.commit()

        return jsonify(new_wishlist_item.obj_to_dict())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# remove item from wishlist
@app.route('/api/wishlist/<int:item_id>', methods=["DELETE"])
@login_required
def delete_from_wishlist(item_id):
    try:
        found_item = WishListItem.query.get(item_id)
        if not found_item:
            return jsonify({"error": "could not find wishlist item based on id"}), 400

        db.session.delete(found_item)
        db.session.commit()

        return jsonify({"success": "wish list item deleted"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
