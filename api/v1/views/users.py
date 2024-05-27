#!/usr/bin/python3
"""Creating a new view for User objects"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request


@app_views.get("/users")
def all_users():
    """Retrieve the list of all User objects"""
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.get("/users/<user_id>")
def get_user(user_id):
    """Retrieve a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.delete("/users/<user_id>")
def delete_user(user_id):
    """Delete a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.post("/users")
def create_user():
    """Create a User"""
    user_data = request.get_json(silent=True)
    if user_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in user_data:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in user_data:
        return jsonify({"error": "Missing password"}), 400
    new_user = User(**user_data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.put("/users/<user_id>")
def update_user(user_id):
    """Update a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user_data = request.get_json(silent=True)
    if user_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in user_data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
