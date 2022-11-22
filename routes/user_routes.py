from flask import request, jsonify
from werkzeug.security import generate_password_hash
from models import db, User
from flask_login import current_user
from __main__ import app, admin_only


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
@app.route('/api/users/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):
    try:
        if current_user.get_id() != str(user_id):
            return jsonify({"error": "can only delete own user"}), 400

        found_user = User.query.get(user_id)
        if not found_user:
            return jsonify({"error": "cannot find user with that user_id"}), 400
        else:
            db.session.delete(found_user)
            db.session.commit()

            return jsonify({"success": "user deleted"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# get user (only admin has access)
@app.route('/api/users/find/<int:user_id>')
@admin_only
def get_user(user_id):
    try:
        found_user = User.query.get(user_id)
        if not found_user:
            return jsonify({"error": "cannot find user with that user_id"}), 400
        else:
            return jsonify(found_user.obj_to_dict())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# get all users (only admin has access)
@app.route('/api/users')
@admin_only
def get_users():
    try:
        users = User.query.all()
        result = [user.obj_to_dict() for user in users]
        return jsonify(users=result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500