from flask import Flask, request, jsonify
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
import os
from dotenv import load_dotenv
from models import db, User, UserAddress, Product, Category, Cart, CartItem, Order, OrderItem
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


load_dotenv()
mysql = os.getenv('mysql')
secret_key = os.getenv('secret_key')
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = mysql
app.config['SECRET_KEY'] = secret_key
db.init_app(app)


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

## AUTHENTICATION ROUTES
@app.route('/api/auth/register', methods=["POST"])
def register():
    if request.method == "POST":
        data = request.json
        try:
            # check if email already in db before saving as new user
            if User.query.filter_by(email=data["email"]).first():
                return jsonify({"error": "email already used, please try again"}), 400

            hashed_password = generate_password_hash(password=data["password"], salt_length=8)
            new_user = User(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                password=hashed_password,
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return jsonify(new_user.obj_to_dict())

        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route('/api/auth/login', methods=["POST"])
def login():
    data = request.json
    try:
        # check if email in db and then compare password
        if not User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "cannot find email, please register"}), 400
        else:
            found_user = User.query.filter_by(email=data["email"]).first()
            if check_password_hash(found_user.password, data["password"]):
                login_user(found_user)
                return jsonify(found_user.obj_to_dict())
            else:
                return jsonify({"error": "password incorrect, please try again"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


## USER ROUTES
# update user
@app.route('/api/users/<int:user_id>', methods=["PATCH"])
def update_user(user_id):
    data = request.json
    try:
        if current_user.get_id() != str(user_id):
            return jsonify({"error": "can only update own user"}), 400

        found_user = User.query.get(user_id)
        if not found_user:
            return jsonify({"error": "cannot find user with that user_id"}), 400
        else:
            hashed_password = generate_password_hash(data["password"], salt_length=8)
            found_user.password = hashed_password
            found_user.first_name = data["first_name"]
            found_user.last_name = data["last_name"]
            db.session.commit()

            return jsonify(User.query.get(user_id).obj_to_dict())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# delete user
@app.route('/api/auth/users/<int:user_id>', methods=["DELETE"])
def delete_user():
    pass


# get user (only admin has access)
@app.route('/api/auth/users/find/<int:user_id>')
def get_user():
    pass


# get all users (only admin has access)
@app.route('/api/auth/users/')
def get_users():
    pass


# get user stats for given month of current year(only admin has access)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
