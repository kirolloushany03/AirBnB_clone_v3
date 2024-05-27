#!/usr/bin/python3
"""Creating a new view for state"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route("/api/v1/states", methods=["GET"])
def all_states():
    """Return the list of all state objects"""
    states_dic = storage.all(State)
    return jsonify([obj.to_dict() for obj in states_dic.values()])


@app_views.route("/api/v1/states/<state_id>", methods=["GET"])
def get_state(state_id):
    """Retrieve a State object by ID"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/api/v1/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Delete a State object by ID"""
    state_d = storage.get(State, state_id)
    if not state_d:
        abort(404)
    storage.delete(state_d)
    storage.save()
    return jsonify({}), 200


@app_views.route("/api/v1/states", methods=["POST"])
def create_state():
    """Create a new State object"""
    state_data = request.get_json()
    if state_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in state_data:
        return jsonify({"error": "Missing name"}), 400
    new_state = State(**state_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/api/v1/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """Update a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state_data = request.get_json(silent=True)
    if state_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in state_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
