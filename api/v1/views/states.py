#!/usr/bin/python3
"""createing a new view for state"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify

@app_views.get('/states')
@app_views.get('/states/')
def all_states():
    """return all the list of all state"""
    states_dict = storage.all(State)
    return jsonify([obj.to_dict() for  obj in states_dict.values()])
