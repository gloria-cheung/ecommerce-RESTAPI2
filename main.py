from flask import Flask, abort
from flask_login import LoginManager, current_user
import os
from dotenv import load_dotenv
from models import db, User
from functools import wraps
from flask_cors import CORS


load_dotenv()
mysql = os.getenv('mysql')
secret_key = os.getenv('secret_key')
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = mysql
app.config['SECRET_KEY'] = secret_key
db.init_app(app)
CORS(app)


# Authenticate
login_manager = LoginManager()
login_manager.init_app(app)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def admin_only(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if current_user.get_id() != "1":
            return abort(404)
        return f(*args, **kwargs)
    return inner

# ROUTES
from routes import auth_routes, user_routes, category_routes, product_routes, cart_routes, cart_items_routes, order_routes


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
