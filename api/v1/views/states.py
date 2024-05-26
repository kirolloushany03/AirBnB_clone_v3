#!/usr/bin/python3
"""createing a new view for state"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort

@app_views.get('/states')
@app_views.get('/states/')
def all_states():
    """return all the list of all state"""
    states_dic = storage.all(State)
    return jsonify([obj.to_dict() for  obj in states_dic.values()])

@app_views.route('/api/v1/states/<state_id>', methods=['GET'])
def all_state(state_id):
    """will get one object and check if it is ok will return the obj
    if not will send 404"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'])
def all_state_delete(state_id):
    """delete a state with id"""
    state_d = storage.get(State, state_id)
    if not state_d:
        abort(404)
        storage.delete(state)
        storage.save()
    return jsonify({}), 200
