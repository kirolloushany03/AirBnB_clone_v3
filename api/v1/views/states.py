#!/usr/bin/python3
"""createing a new view for state"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.get('/states')
@app_views.get('/states/')
def all_states():
    """return all the list of all state"""
    states_dic = storage.all(State)
    return jsonify([obj.to_dict() for  obj in states_dic.values()])


@app_views.get('/states/<state_id>')
def all_state(state_id):
    """will get one object and check if it is ok will return the obj
    if not will send 404"""
    state = storage.get(State, state_id)
    print(state)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.delete('/states/<state_id>')
def all_state_delete(state_id):
    """delete a state with id"""
    state_d = storage.get(State, state_id)
    if not state_d:
        abort(404)
    storage.delete(state_d)
    storage.save()
    return jsonify({}), 200


@app_views.post('/states')
@app_views.post('/states/')
def all_state_post():
    """create a new state"""
    state = request.get_json()
    if not state:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in state:
        return jsonify({"error": "Missing name"}), 400
    new_state = State(**state)
    new_state.save()
    return jsonify(new_state.to_dict()), 201

@app_views.put('/states/<state_id>')
def all_state_put(state_id):
    """update a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state_data = request.get_json()
    if not state_data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in state_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
