#!/usr/bin/python3
"""Creating a new view for the link between Place and Amenity objects"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from flask import jsonify, abort

@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def all_amenities(place_id):
    """Retrieve the list of all Amenity objects of a Place from storage"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if storage.__class__.__name__ == 'DBStorage':
        amenities = place.amenities
    else:
        amenities = [storage.get(Amenity, amenity_id) for amenity_id in place.amenity_ids]

    return jsonify([amenity.to_dict() for amenity in amenities if amenity])

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity_from_place(place_id, amenity_id):
    """Delete an Amenity object from a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if type(storage).__name__ == 'DBStorage':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_amenity_to_place(place_id, amenity_id):
    """Link an amenity object to a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if storage.__class__.__name__ == 'DBStorage':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
