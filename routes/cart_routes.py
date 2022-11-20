from flask import request, jsonify
from models import db, Cart
from __main__ import app, admin_only
from datetime import datetime


# get cart
@app.route('/api/cart/<int:cart_id>')
def get_cart(cart_id):
    pass


# create cart
@app.route('/api/cart/', methods=["POST"])
@admin_only
def create_cart():
    pass


# update cart
@app.route('/api/cart/<int:cart_id>', methods=["PATCH"])
@admin_only
def update_cart(cart_id):
    pass


# delete cart
@app.route('/api/cart/<int:product_id>', methods=["DELETE"])
@admin_only
def delete_cart(cart_id):
    pass