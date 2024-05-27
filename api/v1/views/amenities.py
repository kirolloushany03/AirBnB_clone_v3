#!/usr/bin/python3
"""Creating a new view for Amenity objects"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.get("/amenities")
def all_amenities():
    """Retrieve the list of all Amenity objects"""
    amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.get("/amenities/<amenity_id>")
def get_amenity(amenity_id):
    """Retrieve an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.delete("/amenities/<amenity_id>")
def delete_amenity(amenity_id):
    """Delete an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.post("/amenities")
def create_amenity():
    """Create an Amenity"""
    amenity_data = request.get_json(silent=True)
    if amenity_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in amenity_data:
        return jsonify({"error": "Missing name"}), 400
    new_amenity = Amenity(**amenity_data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.put("/amenities/<amenity_id>")
def update_amenity(amenity_id):
    """Update an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity_data = request.get_json(silent=True)
    if amenity_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in amenity_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
