#!/usr/bin/python3
"""createing a new view for state"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.get('/states')
def all_states():
    """return all the list of all state"""
    states_dic = storage.all(State)
    return jsonify([obj.to_dict() for obj in states_dic.values()])


@app_views.get('/states/<state_id>')
def get_state(state_id):
    """will get one object and check if it is ok will return the obj
    if not will send 404"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.delete('/states/<state_id>')
def delete_state(state_id):
    """delete a state with id"""
    state_d = storage.get(State, state_id)
    if not state_d:
        abort(404)
    storage.delete(state_d)
    storage.save()
    return jsonify({}), 200


@app_views.post('/states')
def create_state():
    """create a new state"""
    state = request.get_json(silent=True)
    if state is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in state:
        return jsonify({"error": "Missing name"}), 400
    new_state = State(**state)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.put('/states/<state_id>')
def update_state(state_id):
    """update a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state_data = request.get_json(silent=True)
    if state_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in state_data.items():
        if key not in ['id', 'created_at', 'updated_at']\
           and hasattr(state, key):
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
