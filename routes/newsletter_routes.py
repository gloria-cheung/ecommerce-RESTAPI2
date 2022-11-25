from flask import request, jsonify
from flask_login import login_required, current_user
from models import db, Newsletter, User
from __main__ import app
from datetime import datetime


# get all emails
@app.route('/api/newsletter/', methods=["GET"])
def get_emails():
    try:
        emails = Newsletter.query.all()
        results = [item.obj_to_dict() for item in emails]
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# add email to newsletter
@app.route('/api/newsletter', methods=["POST"])
@login_required
def add_email():
    try:
        found_user = User.query.get(int(current_user.get_id()))
        if found_user.email == request.json.get("email"):
            newsletter = Newsletter(
                email=request.json.get("email"),
                user_id=int(current_user.get_id())
            )
            db.session.add(newsletter)
            db.session.commit()

            return jsonify(newsletter.obj_to_dict())

        else:
            return jsonify(error="can only sign up for email for own user")

    except Exception as e:
        return jsonify({"error": str(e)}), 500



