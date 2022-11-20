from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from flask_login import login_user, logout_user
from __main__ import app


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


@app.route('/api/auth/logout', methods=["POST"])
def logout():
    try:
        logout_user()
        return jsonify({"success": "logout successful"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
