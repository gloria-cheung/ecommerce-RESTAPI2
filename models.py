from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin
db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    address = relationship("UserAddress", back_populates="user")
    cart = relationship("Cart", back_populates="user")
    orders = relationship("Order", back_populates="user")

    def obj_to_dict(self):
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


class UserAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = relationship("User", back_populates="address")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    address = db.Column(db.String(250), nullable=False)
    city = db.Column(db.String(250), nullable=False)
    postal_code = db.Column(db.String(250), nullable=False)
    country = db.Column(db.String(250), nullable=False)
    phone = db.Column(db.String(250), nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())

    def obj_to_dict(self):
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    desc = db.Column(db.Text, nullable=False)
    inventory = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = relationship("Category", back_populates="products")
    cart_item = relationship("CartItem", back_populates="product")
    order_item = relationship("OrderItem", back_populates="product")

    def obj_to_dict(self):
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    products = relationship("Product", back_populates="category")
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def obj_to_dict(self):
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = relationship("User", back_populates="cart")
    cart_items = relationship("CartItem", back_populates="cart")
    total = db.Column(db.Float, nullable=False, default=0)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def obj_to_dict(self):
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"))
    cart = relationship("Cart", back_populates="cart_items")
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    product = relationship("Product", back_populates="cart_item")
    quantity = db.Column(db.Integer, nullable=False)

    def obj_to_dict(self):
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")
    total = db.Column(db.Float, nullable=False, default=0)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def obj_to_dict(self):
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    order = relationship("Order", back_populates="order_items")
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    product = relationship("Product", back_populates="order_item")
    quantity = db.Column(db.Integer, nullable=False)

    def obj_to_dict(self):
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary
