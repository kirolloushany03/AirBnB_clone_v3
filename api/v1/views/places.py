#!/usr/bin/python3
"""Creating a new view for Place objects"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, abort, request


@app_views.get("/cities/<city_id>/places")
def all_places(city_id):
    """Retrieve the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.get("/places/<place_id>")
def get_place(place_id):
    """Retrieve a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.delete("/places/<place_id>")
def delete_place(place_id):
    """Delete a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.post("/cities/<city_id>/places")
def create_place(city_id):
    """Create a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    place_data = request.get_json(silent=True)
    if place_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in place_data:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, place_data["user_id"])
    if not user:
        abort(404)
    if "name" not in place_data:
        return jsonify({"error": "Missing name"}), 400
    place_data["city_id"] = city_id
    new_place = Place(**place_data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.put("/places/<place_id>")
def update_place(place_id):
    """Update a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place_data = request.get_json(silent=True)
    if place_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in place_data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
