from flask import Flask, request, jsonify
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
import os
from dotenv import load_dotenv
from models import db, User, UserAddress, Product, Category, Cart, CartItem, Order, OrderItem
from werkzeug.security import generate_password_hash, check_password_hash


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

# AUTHENTICATION
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
            return jsonify({"error": "cannot find email, please register"})
        else:
            found_user = User.query.filter_by(email=data["email"]).first()
            if check_password_hash(found_user.password, data["password"]):
                login_user(found_user)
                return jsonify(found_user.obj_to_dict())
            else:
                return jsonify({"error": "password incorrect, please try again"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
