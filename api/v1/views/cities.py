#!/usr/bin/python3
"""Creating a new view for City objects"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request


@app_views.get("/states/<state_id>/cities")
def all_cities(state_id):
    """Retrieve the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.get("/cities/<city_id>")
def get_city(city_id):
    """Retrieve a City object from the storage"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.delete("/cities/<city_id>")
def delete_city(city_id):
    """Delete a City object from the storage"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.post("/states/<state_id>/cities")
def create_city(state_id):
    """Create a City object in storage"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    city_data = request.get_json(silent=True)
    if city_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in city_data:
        return jsonify({"error": "Missing name"}), 400
    city_data["state_id"] = state_id
    new_city = City(**city_data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.put("/cities/<city_id>")
def update_city(city_id):
    """Update a City object in the storage"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city_data = request.get_json(silent=True)
    if city_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in city_data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
